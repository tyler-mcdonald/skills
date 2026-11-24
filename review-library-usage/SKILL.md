---
name: review-library-usage
description: Review how a diff uses its libraries, and report code that rebuilds what they provide or skips their best practices. Use when asked to review library usage.
---

## Steps

1. List the source files and stylesheets changed in `origin/<base>...HEAD`. Base is the argument, else the default branch.
2. For each changed file, find its nearest package manifest (e.g. `package.json`, `pyproject.toml`). From each manifest's dependencies, pick the libraries the changed code uses or rebuilds. A library's files are the changed files under that manifest. No libraries: reply "none" and stop.
3. If a manifest's dependencies aren't installed in the worktree, install them from its lockfile (e.g. `npm ci`, `uv sync`).
4. Spawn one Sonnet subagent per library, in parallel, with the reviewer message.
5. Reply with every reviewer's findings, unchanged, or "none".

## Reviewer message

> You're a staff engineer with deep expertise in `<library>`. Review how this branch uses it, in `<files>` (diff against `origin/<base>`, in `<worktree path>`). Look for code that rebuilds what `<library>` already provides, and for places that don't follow its best practices or community standards.
>
> First read the installed version's types and source, only for the APIs these files use or rebuild. Fetch an official docs page only if that leaves a question open.
>
> Review only code the branch adds or changes. Don't edit files. For each finding, reply with the file and line, what to change, and the doc or source line that backs it. If there's nothing to change, reply "none".
