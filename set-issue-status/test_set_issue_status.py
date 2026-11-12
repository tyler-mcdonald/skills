import importlib.util
import json
import subprocess
import unittest
from pathlib import Path
from unittest import mock

spec = importlib.util.spec_from_file_location(
    "set_issue_status", Path(__file__).with_name("set_issue_status.py")
)
sis = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sis)

URL = "https://github.com/o/r/issues/1"


def board(item_id, project_id, title, options):
    return {
        "id": item_id,
        "project": {
            "id": project_id,
            "title": title,
            "field": {
                "id": f"{project_id}-field",
                "options": [
                    {"id": f"{project_id}-{name}", "name": name} for name in options
                ],
            },
        },
    }


def graphql(nodes, end_cursor=None):
    page_info = {"hasNextPage": end_cursor is not None, "endCursor": end_cursor}
    return json.dumps(
        {
            "data": {
                "resource": {"projectItems": {"nodes": nodes, "pageInfo": page_info}}
            }
        }
    )


class SetIssueStatusTest(unittest.TestCase):
    def run_with(self, nodes, status, pages=None):
        calls = []
        pages = iter(pages or [graphql(nodes)])

        def run(cmd, **kwargs):
            calls.append(cmd)
            stdout = next(pages) if cmd[1] == "api" else ""
            return subprocess.CompletedProcess(cmd, 0, stdout=stdout)

        with mock.patch.object(sis.subprocess, "run", side_effect=run):
            lines = list(sis.set_issue_status(URL, status))
        return lines, calls

    def test_matches_option_ignoring_case(self):
        lines, calls = self.run_with(
            [board("I1", "P1", "Roadmap", ["Todo", "In review"])], "in REVIEW"
        )
        self.assertEqual(lines, ["Roadmap: In review"])
        self.assertEqual(calls[0][:4], ["gh", "api", "graphql", "-f"])
        self.assertEqual(calls[0][4], f"url={URL}")
        self.assertEqual(
            calls[1],
            [
                "gh",
                "project",
                "item-edit",
                "--id",
                "I1",
                "--project-id",
                "P1",
                "--field-id",
                "P1-field",
                "--single-select-option-id",
                "P1-In review",
            ],
        )

    def test_skips_board_without_option(self):
        lines, calls = self.run_with(
            [
                board("I1", "P1", "Roadmap", ["Todo"]),
                board("I2", "P2", "Sprint", ["In review"]),
            ],
            "In review",
        )
        self.assertEqual(
            lines, ['Roadmap: skipped (no "In review" option)', "Sprint: In review"]
        )
        self.assertEqual(len(calls), 2)
        self.assertEqual(calls[1][4], "I2")

    def test_follows_pagination(self):
        lines, calls = self.run_with(
            None,
            "Done",
            pages=[
                graphql([board("I1", "P1", "Roadmap", ["Done"])], end_cursor="C1"),
                graphql([board("I2", "P2", "Sprint", ["Done"])]),
            ],
        )
        self.assertEqual(lines, ["Roadmap: Done", "Sprint: Done"])
        self.assertEqual(calls[0][7:], [])
        self.assertEqual(calls[1][7:], ["-f", "cursor=C1"])

    def test_rejects_repeated_cursor(self):
        page = graphql([board("I1", "P1", "Roadmap", ["Done"])], end_cursor="C1")
        with self.assertRaises(RuntimeError):
            self.run_with(None, "Done", pages=[page, page])

    def test_no_boards(self):
        lines, calls = self.run_with([], "In review")
        self.assertEqual(lines, [f"{URL} is on no project boards."])
        self.assertEqual(len(calls), 1)

    def test_gh_failure_prints_stderr_and_exits_non_zero(self):
        error = subprocess.CalledProcessError(1, ["gh"], stderr="gh: not found\n")
        with (
            mock.patch.object(sis.subprocess, "run", side_effect=error) as run,
            mock.patch.object(sis.sys, "stderr") as stderr,
            self.assertRaises(SystemExit) as raised,
        ):
            sis.main(["set_issue_status.py", URL, "Done"])
        self.assertNotEqual(raised.exception.code, 0)
        run.assert_called_once_with(
            mock.ANY, check=True, capture_output=True, text=True
        )
        stderr.write.assert_called_with("gh: not found\n")


if __name__ == "__main__":
    unittest.main()
