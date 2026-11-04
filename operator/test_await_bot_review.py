import importlib.util
import subprocess
import unittest
from pathlib import Path
from unittest import mock

spec = importlib.util.spec_from_file_location(
    "await_bot_review", Path(__file__).with_name("await-bot-review.py")
)
abr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(abr)

TRIGGER = "@coderabbitai review"
DONE = "Review finished"


def comment(user, body, created, updated=None):
    return {
        "user": {"login": user},
        "body": body,
        "created_at": created,
        "updated_at": updated or created,
    }


def trigger(created):
    return comment("someone", TRIGGER, created)


class IsDoneTest(unittest.TestCase):
    def check(self, comments):
        return abr.is_done(comments, "coderabbitai", TRIGGER, DONE)

    def test_done_reply_after_trigger(self):
        self.assertTrue(
            self.check(
                [
                    trigger("2026-01-01T00:00:00Z"),
                    comment("coderabbitai[bot]", DONE, "2026-01-01T00:00:08Z"),
                ]
            )
        )

    def test_reply_edited_to_done_after_trigger(self):
        self.assertTrue(
            self.check(
                [
                    comment(
                        "coderabbitai[bot]",
                        DONE,
                        "2025-12-31T00:00:00Z",
                        "2026-01-01T00:05:00Z",
                    ),
                    trigger("2026-01-01T00:00:00Z"),
                ]
            )
        )

    def test_done_reply_before_latest_trigger(self):
        self.assertFalse(
            self.check(
                [
                    trigger("2026-01-01T00:00:00Z"),
                    comment("coderabbitai[bot]", DONE, "2026-01-01T00:00:08Z"),
                    trigger("2026-01-02T00:00:00Z"),
                ]
            )
        )

    def test_reply_without_done_text(self):
        self.assertFalse(
            self.check(
                [
                    trigger("2026-01-01T00:00:00Z"),
                    comment(
                        "coderabbitai[bot]", "Review started", "2026-01-01T00:00:08Z"
                    ),
                ]
            )
        )

    def test_done_text_from_another_user(self):
        self.assertFalse(
            self.check(
                [
                    trigger("2026-01-01T00:00:00Z"),
                    comment("someone", DONE, "2026-01-01T00:00:08Z"),
                ]
            )
        )

    def test_trigger_must_match_whole_body(self):
        with self.assertRaises(SystemExit):
            self.check(
                [comment("someone", f"{TRIGGER} please", "2026-01-01T00:00:00Z")]
            )

    def test_no_trigger(self):
        with self.assertRaises(SystemExit):
            self.check([comment("coderabbitai[bot]", DONE, "2026-01-01T00:00:08Z")])


class AwaitBotReviewTest(unittest.TestCase):
    def run_polls(self, responses):
        self.clock = clock = [0.0]

        def sleep(seconds):
            clock[0] += seconds

        with (
            mock.patch.object(abr, "fetch_comments", side_effect=responses) as fetch,
            mock.patch.object(abr.time, "sleep", side_effect=sleep),
            mock.patch.object(abr.time, "monotonic", side_effect=lambda: clock[0]),
            mock.patch("sys.stderr"),
        ):
            result = abr.await_bot_review("1", "coderabbitai", TRIGGER, DONE, "o/r")
        return result, fetch.call_count

    def test_failed_fetch_retries_next_poll(self):
        pending = [trigger("2026-01-01T00:00:00Z")]
        done = pending + [comment("coderabbitai[bot]", DONE, "2026-01-01T00:00:08Z")]
        error = subprocess.CalledProcessError(1, "gh", stderr="HTTP 502")
        self.assertEqual(self.run_polls([pending, error, done]), ("done", 3))

    def test_hung_fetch_retries_next_poll(self):
        pending = [trigger("2026-01-01T00:00:00Z")]
        done = pending + [comment("coderabbitai[bot]", DONE, "2026-01-01T00:00:08Z")]
        error = subprocess.TimeoutExpired("gh", abr.FETCH_TIMEOUT_SECONDS)
        self.assertEqual(self.run_polls([pending, error, done]), ("done", 3))

    def test_first_fetch_failure_exits(self):
        error = subprocess.CalledProcessError(1, "gh", stderr="HTTP 404")
        with self.assertRaises(SystemExit) as exit:
            self.run_polls([error])
        self.assertIn("HTTP 404", str(exit.exception.code))

    def test_timeout(self):
        pending = [trigger("2026-01-01T00:00:00Z")]
        result, calls = self.run_polls(lambda *_: pending)
        self.assertEqual(result, "timeout")
        self.assertEqual(calls, abr.TIMEOUT_SECONDS // abr.POLL_SECONDS + 1)

    def test_final_poll_at_deadline_after_slow_fetches(self):
        pending = [trigger("2026-01-01T00:00:00Z")]
        done = pending + [comment("coderabbitai[bot]", DONE, "2026-01-01T00:00:08Z")]

        def fetch(*_):
            started = self.clock[0]
            self.clock[0] += 45
            return done if started >= abr.TIMEOUT_SECONDS else pending

        self.assertEqual(self.run_polls(fetch)[0], "done")


if __name__ == "__main__":
    unittest.main()
