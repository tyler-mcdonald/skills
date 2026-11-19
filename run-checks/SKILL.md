---
name: run-checks
description: Run lint, typecheck, and the changed files' tests locally, leaving the full test suite to CI. Use only when a skill's step tells you to invoke it.
---

# Run Checks

Run lint, typecheck, and only the tests for the changed files, by passing those files to the repo's test command (e.g. `vitest related <files>`, `pytest <test files>`). Don't run the full test suite; CI runs it.
