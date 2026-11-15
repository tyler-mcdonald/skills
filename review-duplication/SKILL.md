---
name: review-duplication
description: Review a diff for code that duplicates itself or code already in the repo. Use when asked to review duplication.
---

# Review Duplication

## Steps

1. List the source files changed in `origin/<base>...HEAD`, skipping tests. Base is the argument, else the default branch. None: reply "none" and stop.
2. Spawn a Sonnet subagent with the reviewer message.
3. Reply with its findings, unchanged, or "none".

## Reviewer message

> Find duplication in the code this branch adds or changes in `<files>` (diff against `origin/<base>`, in `<worktree path>`).
>
> 1. List every function, component, hook, type, constant, and repeated block the diff adds.
> 2. For each one, search the whole repo for code with a similar name, shape, or logic.
> 3. Report duplication within the diff and between the diff and existing code, including near-copies that differ only in names or values.
>
> Don't report two short, similar lines, where sharing them costs more than it saves. Don't edit files. For each finding, reply with both locations and what to do: reuse the existing code, or extract a shared one and where it lives. If there's nothing to change, reply "none".
