---
name: review-clean-code
description: Review a diff for readability and maintainability against general, TypeScript, and React clean code rules. Use when asked to review clean code.
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
> - Names say what a thing is or does; no vague names like `data`, `handle`, `util`, or `temp`.
> - Each function and component does one job.
> - Return early instead of nesting conditions.
> - No dead code, unused parameters, commented-out code, or debug leftovers.
> - No abstraction, wrapper, or helper with a single trivial use.
> - Prefer built-in standard library helpers over hand-written loops or utilities, if the project's language version supports them.
>
> **TypeScript**
> - Prefer `prop?: string` to `prop: string | undefined`.
> - Derive types from existing ones (`Pick`, `Omit`, `ReturnType`, indexed access) instead of redeclaring them.
>
> **React**
> - Compute derived values during render instead of syncing them into state with an effect ([You Might Not Need an Effect](https://react.dev/learn/you-might-not-need-an-effect)).
> - Move non-trivial logic out of a component's body into a custom hook or plain function ([Reusing Logic with Custom Hooks](https://react.dev/learn/reusing-logic-with-custom-hooks)).
>
> Don't edit files. For each finding, reply with the file and line, what to change, and the rule it breaks. If there's nothing to change, reply "none".
