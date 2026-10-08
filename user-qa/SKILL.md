---
name: user-qa
description: Start the app, have the user test a UI change by hand, and fix whatever they report failing until it passes. Use when asked to QA a change with the user, or as the QA step of a workflow.
---

# User QA

The argument is optional: `force` to always run QA, or `skip` to never. Without one, decide whether the change needs hands-on QA: it does only if it changes something a person can see or exercise through the app's UI. Skip it for backend or API-only changes (even ones that change API behavior or responses), docs, config, tests, or internal refactors — tests and review cover those. When skipping, reply "QA skipped" and stop.

1. Invoke `run` in the worktree to start the app.
2. Give the user a short bulleted list of the high-level functionality to test — one line each: what to do and what should happen. Then wait for their pass or fail.
3. On a fail, spawn a fresh subagent with the fix message, wait for its reply, then go back to 1.
4. On a pass, stop the servers and reply "QA passed".

## Fix message

> Fix these QA findings: `<findings>`. Work in `<worktree path>`. Run the project's checks (tests, lint) and fix any failures, then commit. Don't push. Reply with one line: the commit you made.
