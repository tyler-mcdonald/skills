import importlib.util
import subprocess
import unittest
from pathlib import Path
from unittest import mock

spec = importlib.util.spec_from_file_location(
    "determine_code_review_effort", Path(__file__).with_name("determine-code-review-effort.py")
)
pe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pe)


class ChangedLinesTest(unittest.TestCase):
    def test_sums_added_and_deleted(self):
        self.assertEqual(pe.changed_lines("3\t2\ta.py\x0010\t0\tdocs/b.md\x00"), 15)

    def test_skips_binary_files(self):
        self.assertEqual(pe.changed_lines("-\t-\timage.png\x004\t1\ta.py\x00"), 5)

    def test_skips_lockfiles_in_any_directory(self):
        numstat = "".join(f"100\t100\tsub/{name}\x00" for name in sorted(pe.LOCKFILES))
        self.assertEqual(pe.changed_lines(numstat + "1\t1\ta.py\x00"), 2)

    def test_counts_similarly_named_files(self):
        self.assertEqual(pe.changed_lines("5\t0\tyarn.lock.md\x00"), 5)

    def test_skips_renamed_lockfile(self):
        self.assertEqual(
            pe.changed_lines("7\t7\t\x00old/uv.lock\x00new/uv.lock\x00"), 0
        )
        self.assertEqual(
            pe.changed_lines("7\t7\t\x00tpl{x}/a/uv.lock\x00café/uv.lock\x00"), 0
        )

    def test_skips_renamed_binary_file(self):
        self.assertEqual(
            pe.changed_lines("-\t-\t\x00old.png\x00new.png\x004\t1\ta.py\x00"), 5
        )

    def test_counts_rename_away_from_lockfile_name(self):
        self.assertEqual(pe.changed_lines("2\t1\t\x00uv.lock\x00notes.txt\x00"), 3)

    def test_empty_diff(self):
        self.assertEqual(pe.changed_lines(""), 0)


class EffortTest(unittest.TestCase):
    def test_thresholds(self):
        cases = {0: "low", 50: "low", 51: "medium", 400: "medium", 401: "high"}
        for lines, expected in cases.items():
            with self.subTest(lines=lines):
                self.assertEqual(pe.effort(lines), expected)


class DetermineCodeReviewEffortTest(unittest.TestCase):
    def test_fetches_then_diffs_against_origin_base(self):
        calls = []

        def run(cmd, **kwargs):
            calls.append(cmd)
            self.assertEqual(kwargs.get("errors"), "surrogateescape")
            stdout = "30\t30\ta.py\x00" if cmd[1] == "diff" else ""
            return subprocess.CompletedProcess(cmd, 0, stdout=stdout)

        with mock.patch.object(pe.subprocess, "run", side_effect=run):
            self.assertEqual(pe.determine_code_review_effort("main"), "medium")
        self.assertEqual(
            calls,
            [
                ["git", "fetch", "origin", "+refs/heads/main:refs/remotes/origin/main"],
                ["git", "diff", "--numstat", "-z", "origin/main...HEAD"],
            ],
        )

    def test_git_failure_raises(self):
        error = subprocess.CalledProcessError(128, ["git"], stderr="bad")
        with (
            mock.patch.object(pe.subprocess, "run", side_effect=error),
            self.assertRaises(subprocess.CalledProcessError),
        ):
            pe.determine_code_review_effort("main")


if __name__ == "__main__":
    unittest.main()
