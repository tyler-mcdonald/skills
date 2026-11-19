import importlib.util
import subprocess
import unittest
from pathlib import Path
from unittest import mock

spec = importlib.util.spec_from_file_location(
    "await_ci", Path(__file__).with_name("await_ci.py")
)
ac = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ac)


def check(bucket):
    return {"name": "ci", "bucket": bucket}


def gh_result(stdout="", stderr="", returncode=0):
    return subprocess.CompletedProcess([], returncode, stdout, stderr)


class OutcomeTest(unittest.TestCase):
    def test_all_passed_or_skipped(self):
        self.assertEqual(ac.outcome([check("pass"), check("skipping")]), "pass")

    def test_any_failure(self):
        self.assertEqual(ac.outcome([check("pending"), check("fail")]), "fail")

    def test_cancelled(self):
        self.assertEqual(ac.outcome([check("cancel")]), "fail")

    def test_pending(self):
        self.assertIsNone(ac.outcome([check("pass"), check("pending")]))

    def test_no_checks(self):
        self.assertIsNone(ac.outcome([]))


class FetchChecksTest(unittest.TestCase):
    def test_no_checks_reported_is_empty(self):
        result = gh_result(stderr="no checks reported on the 'x' branch", returncode=1)
        with mock.patch.object(ac.subprocess, "run", return_value=result):
            self.assertEqual(ac.fetch_checks("1", ""), [])

    def test_pending_exit_code_still_parses(self):
        result = gh_result(stdout='[{"name":"ci","bucket":"pending"}]', returncode=8)
        with mock.patch.object(ac.subprocess, "run", return_value=result):
            self.assertEqual(ac.fetch_checks("1", ""), [check("pending")])

    def test_other_error_raises(self):
        result = gh_result(stderr="no pull requests found", returncode=1)
        with (
            mock.patch.object(ac.subprocess, "run", return_value=result),
            self.assertRaises(subprocess.CalledProcessError),
        ):
            ac.fetch_checks("1", "")


class AwaitCiTest(unittest.TestCase):
    def run_with(self, fetches, times):
        with (
            mock.patch.object(ac, "fetch_checks", side_effect=fetches),
            mock.patch.object(ac.time, "monotonic", side_effect=times),
            mock.patch.object(ac.time, "sleep"),
        ):
            return ac.await_ci("1", "")

    def test_waits_for_checks_to_register(self):
        result = self.run_with([[], [check("pending")], [check("pass")]], [0] * 5)
        self.assertEqual(result, "pass")

    def test_none_when_no_checks_register(self):
        self.assertEqual(
            self.run_with([[], []], [0, 0, 0, ac.REGISTER_SECONDS]), "none"
        )

    def test_timeout_while_pending(self):
        result = self.run_with([[check("pending")]], [0, ac.TIMEOUT_SECONDS])
        self.assertEqual(result, "timeout")

    def test_first_fetch_error_exits(self):
        error = subprocess.CalledProcessError(1, "gh", stderr="bad auth")
        with self.assertRaises(SystemExit):
            self.run_with([error], [0])

    def test_later_fetch_error_retries(self):
        error = subprocess.CalledProcessError(1, "gh", stderr="blip")
        result = self.run_with([[check("pending")], error, [check("fail")]], [0] * 4)
        self.assertEqual(result, "fail")


if __name__ == "__main__":
    unittest.main()
