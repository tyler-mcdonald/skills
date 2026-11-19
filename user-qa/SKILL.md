---
name: user-qa
description: Have the user test a UI change by hand and work through user feedback. Use when asked to QA a change with the user, or as the QA step of a workflow.
---

# User QA

QA is a quick loop with the user: make fixes until they say pass, without running tests or checks in between. Once they pass, run the checks once.

1. Invoke `run` in the worktree to start the app.
2. Give the user a short bulleted list of the high-level functionality to test — one line each: what to do and what should happen. End the message with `needs input: QA pass or fail` on its own line, then wait for their pass or fail.
3. On a fail, make the fixes yourself, then go back to 2.
4. On a pass, run the project's checks (tests, lint) and fix any failures, then stop the servers and reply "QA passed".
5. Update the issue
   - Invoke `write-issue` to draft the issue body changes for the decisions the user made during QA.
   - Show only the added and removed lines in a fenced `diff` block (e.g. `+ - <new bullet>`), not the whole body.
   - End the message with `needs input: approve issue update` on its own line.
   - Once the user approves, update the issue body.
