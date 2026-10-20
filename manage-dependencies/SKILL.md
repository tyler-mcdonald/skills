---
name: manage-dependencies
description: Bump a dependency or fix an audit in its own PR. Use when asked to fix a dependency audit or update a dependency.
---

# Manage Dependencies

Dependency changes always get their own PR off the base branch. Never commit them onto a feature branch, even when that branch's audit check is what failed.

1. Note the feature PR that surfaced the failure, if any. The base is that PR's base (`gh pr view --json baseRefName`), else the repo's default branch.
2. Invoke `setup-worktree` with a short title (e.g. "Bump certifi for GHSA-xxxx"). If the session is already in a worktree, `EnterWorktree` can't create another: instead run `git fetch origin`, then `git worktree add <main checkout>/.claude/worktrees/<slug> -b <slug> origin/<base>`, and enter it with `EnterWorktree` `path`. Stay in that worktree for every step.
3. Make the smallest change that fixes it: bump only the affected packages, to the lowest version that resolves the advisory, using the project's own tool (e.g. `uv lock --upgrade-package <pkg>`, `npm update <pkg>`). Regenerate the lockfile with that tool rather than editing it by hand.
4. Re-run the audit and the project's checks (tests, lint). If the audit still fails or no fixed version exists, stop and report why.
5. Commit with a single line naming the package, version, and advisory (e.g. "Bump certifi to 2026.10.19 for GHSA-xxxx"). `git push -u origin HEAD`, then open the PR with the `open-pr` skill.
6. If the feature PR already has a commit making this change, `git revert` it on that branch and push, so it picks the fix up from the base instead.
7. Return the dependency PR URL, plus the feature PR's URL with a note to run `sync-branch` on it once the dependency PR merges.
