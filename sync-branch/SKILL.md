---
name: sync-branch
description: Merge the base branch into the current branch, resolve conflicts, and push. Use when asked to sync a branch with main or resolve merge conflicts.
---

# Sync Branch

The argument is the base branch (e.g. `main`). With none, use the PR's base (`gh pr view --json baseRefName`), else the repo's default branch.

1. `git fetch origin`, then `git merge origin/<base>`. If nothing changed, report `Up To Date` and stop. If it merged cleanly, skip to step 4.
2. For each conflicted file (`git diff --name-only --diff-filter=U`), read both sides and their commits (`git log --oneline --merge -- <file>`), resolve it keeping both intents, and `git add` it.
3. If two sides make incompatible choices (e.g. one deletes what the other changes), `git merge --abort` and report `Needs Decision`, listing each file and what needs deciding. Otherwise `git commit --no-edit`.
4. `git push`, then report `Synced`, listing files resolved by judgment. If the push fails, report `Failed` with the error.
