---
name: manage-dependencies
description: Bump a dependency or fix an audit in a separate PR off the base branch. Use when asked to fix a dependency audit or update a dependency.
---

# Manage Dependencies

Dependency changes always get their own PR off the base branch. Never commit them onto a feature branch, even when that branch's audit check is what failed.

1. Note the feature PR that surfaced the failure, if any. The base is that PR's base (`gh pr view <feature PR> --json baseRefName`), else the repo's default branch.
2. Invoke `setup-worktree` with a short title (e.g. "Bump certifi for GHSA-xxxx") and the base. Stay in that worktree through step 5.
3. Make the smallest change that does it: bump only the affected packages, to the lowest version that resolves the advisory for an audit, or else the version asked for (the latest if none was). Use the project's own tool and pin the exact version (e.g. `uv lock --upgrade-package <pkg>==<version>`, `npm install <pkg>@<version>`), so it regenerates the lockfile rather than you editing it by hand.
4. Run the project's checks (tests, lint), and re-run the audit if this is an audit fix. If the audit still fails or no fixed version exists, stop and report why.
5. Commit with a single line naming the package, version, and advisory if any (e.g. "Bump certifi to 2026.10.19 for GHSA-xxxx"). `git push -u origin HEAD`, then open the PR into the base (`--base <base>`) with the `open-pr` skill.
6. If the feature PR already has a commit making this change, enter the feature branch's worktree with `EnterWorktree` `path` (find it with `git worktree list`). If that commit touches only dependency files, `git revert` it and push, so the branch picks the fix up from the base instead. If it also has other changes, or the revert conflicts, abort and leave it for the user.
7. Return the dependency PR URL, plus the feature PR's URL with a note to run `sync-branch` on it once the dependency PR merges, and whether its dependency commit was reverted or left for the user.
