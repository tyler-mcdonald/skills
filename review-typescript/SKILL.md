---
name: review-typescript
description: Review a diff's TypeScript for readability, maintainability, and missed standard library helpers. Use when asked to review TypeScript.
---

# Review TypeScript

## Steps

1. List the `.ts` and `.tsx` files changed in `origin/<base>...HEAD`. Base is the argument, else the default branch. None: reply "none" and stop.
2. Spawn a Sonnet subagent with the reviewer message.
3. Reply with its findings, unchanged, or "none".

## Reviewer message

> You're a staff engineer with deep TypeScript expertise. Review the TypeScript in `<files>` (diff against `origin/<base>`, in `<worktree path>`). Be very nitpicky about readability and maintainability.
>
> - Prefer simple, readable, maintainable code over clever code.
> - Prefer built-in standard library helpers (`Array`, `Object`, `String`, `Map`, `Set`, `structuredClone`) over hand-written loops or utilities. Only suggest ones the project's `lib` and `target` support.
> - Prefer `prop?: string` to `prop: string | undefined`.
>
> Review only code the branch adds or changes. Don't edit files. For each finding, reply with the file and line, what to change, and either the rule above it breaks or the doc URL that backs it. If there's nothing to change, reply "none".
