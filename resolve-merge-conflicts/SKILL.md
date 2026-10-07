---
name: resolve-merge-conflicts
description: Merge a branch into the current one and resolve any conflicts, aborting when a conflict needs the user to decide. Use when asked to merge a base branch in, update a branch from main, or resolve merge conflicts.
---

# Resolve Merge Conflicts

The argument is the branch to merge in (e.g. `origin/main`). With none, use `origin/<default branch>`.

1. `git fetch origin`, then `git merge <branch>`. If it merges cleanly, report `Merged` (or `Up To Date` if nothing changed) and stop.
2. For each conflicted file (`git diff --name-only --diff-filter=U`), read both sides and what each branch was trying to do (`git log --oneline --merge -- <file>`), then resolve it keeping the intent of both. Remove every conflict marker and `git add` the file.
3. A conflict needs the user when the two sides make incompatible choices and keeping both isn't possible — e.g. one side deletes or rewrites what the other changes, or they pick different behavior for the same thing. If any does, `git merge --abort` and report `Needs Decision`, listing each file and what needs deciding. Don't guess.
4. Once every conflict is resolved, commit with the default merge message (`git commit --no-edit`) and report `Merged`, listing the files whose conflicts you resolved by judgment.

Don't push — leave that to the caller.
