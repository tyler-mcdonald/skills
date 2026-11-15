---
name: review-clean-code
description: Review a diff for readability and maintainability against general clean code rules and the project's conventions. Use when asked to review clean code.
---

# Review Clean Code

## Steps

1. List the source files changed in `origin/<base>...HEAD`. Base is the argument, else the default branch. None: reply "none" and stop.
2. Spawn a Sonnet subagent with the reviewer message.
3. Reply with its findings, unchanged, or "none".

## Reviewer message

> Review the code this branch adds or changes in `<files>` (diff against `origin/<base>`, in `<worktree path>`) against the rules below. Be very nitpicky about readability and maintainability: prefer simple, readable, maintainable code over clever code.
>
> **General**
> - Each function and component does one job.
> - Return early instead of nesting conditions.
> - No dead code, unused parameters, commented-out code, or debug leftovers.
> - No abstraction, wrapper, or helper with a single trivial use.
> - Prefer built-in standard library helpers over hand-written loops or utilities, if the project's language version supports them.
>
> **Project**
> - The coding conventions in the project's CLAUDE.md files, including those in the changed files' directories.
>
> Don't edit files. For each finding, reply with the file and line, what to change, and the rule it breaks. If there's nothing to change, reply "none".
