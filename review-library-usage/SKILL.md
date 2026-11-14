---
name: review-library-usage
description: Report code in a branch's changes that rebuilds what its libraries already provide. Use as a `refine-diff` check, or when asked to check a branch leans on its libraries.
---

# Review Library Usage

## Libraries

| Library | Detected by |
|---|---|
| Mantine | an import from `@mantine/` |

## Steps

1. List the files changed in `origin/<base>...HEAD`. Base is the argument, else the default branch.
2. Match changed files that import a listed library, plus the stylesheets they import. No matches: reply "none" and stop.
3. Spawn one Sonnet subagent per matched library, in parallel, with the reviewer message.
4. Reply with every reviewer's findings, unchanged, or "none".

## Reviewer message

> You're a staff engineer with deep expertise in `<library>`. Review how this branch uses it, in `<files>` (diff against `origin/<base>`, in `<worktree path>`). Look for code that rebuilds what `<library>` already provides, and for places that don't follow its best practices or community standards.
>
> First read the installed version's types and source, only for the APIs these files use or rebuild. Fetch an official docs page only if that leaves a question open.
>
> Review only code the branch adds or changes. Don't edit files. For each finding, reply with the file and line, what to change, and the doc or source line that backs it. If there's nothing to change, reply "none".
