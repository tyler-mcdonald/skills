---
name: sync-branch
description: Sync the current branch with its base — fetch, merge the base branch in, resolve any conflicts, and push — aborting when a conflict needs the user to decide. Use when asked to sync or update a branch with main, merge the base branch in, or resolve merge conflicts with the base.
---

# Sync Branch

The argument is the base branch to merge in (e.g. `main`). With none, use the base of the current branch's PR (`gh pr view --json baseRefName`), or else the repo's default branch.

1. `git fetch origin`, then `git merge origin/<base>`. If nothing changed, report `Up To Date` and stop. If it merges cleanly, skip to step 4.
2. For each conflicted file (`git diff --name-only --diff-filter=U`), read both sides and what each branch was trying to do (`git log --oneline --merge -- <file>`), then resolve it keeping the intent of both. Remove every conflict marker and `git add` the file.
3. A conflict needs the user when the two sides make incompatible choices and keeping both isn't possible — e.g. one side deletes or rewrites what the other changes, or they pick different behavior for the same thing. If any does, `git merge --abort` and report `Needs Decision`, listing each file and what needs deciding. Don't guess. Once every conflict is resolved, commit with the default merge message (`git commit --no-edit`).
4. `git push`, then report `Synced`, listing the files whose conflicts you resolved by judgment. If the push fails, report `Failed` with the error.
