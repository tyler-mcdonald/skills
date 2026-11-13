---
name: user-qa
description: Have the user test a UI change by hand and work through user feedback. Use when asked to QA a change with the user, or as the QA step of a workflow.
argument-hint: "[force|skip]"
---

# User QA

`force` always runs QA and `skip` never does. Without an argument, decide whether the change needs hands-on QA: it does only if it changes something a person can see or exercise through the app's UI. Skip it for backend or API-only changes (even ones that change API behavior or responses), docs, config, tests, or internal refactors — tests and review cover those. When skipping, reply "QA skipped" and stop.

1. Invoke `run` in the worktree to start the app.
2. Give the user a short bulleted list of the high-level functionality to test — one line each: what to do and what should happen. End the message with `needs input: QA pass or fail` on its own line, then wait for their pass or fail.
3. On a fail, make the fixes yourself in this session, not in a subagent. Don't run tests or checks yet. Reload the app if needed, then go back to 2.
4. On a pass:
   1. Invoke `simplify` on the changes.
   2. Run the project's checks (tests, lint) and fix any failures.
   3. Commit. Don't push.
   4. Stop the servers and reply "QA passed".
