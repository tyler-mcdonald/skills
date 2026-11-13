---
name: manage-dependencies
description: Bump a dependency or fix an audit in a separate PR off the default branch. Use when asked to fix a dependency audit or update a dependency.
model: sonnet
---

# Manage Dependencies

Dependency changes always get their own PR off the default branch. Never commit them onto a feature branch, even when that branch's audit check is what failed.

1. Invoke `setup-worktree` with a short title (e.g. "Bump certifi for GHSA-xxxx"). Stay in that worktree for every step.
2. Make the smallest change that does it: bump only the affected packages, to the lowest version that resolves the advisory for an audit, or else the version asked for (the latest if none was).
   - Update the package's entry in the manifest (`package.json`, `pyproject.toml`, etc.), adding one for a transitive dependency.
   - Run the project's lockfile update command (e.g. `uv lock`, `npm install`). Never only upgrade the package in the lockfile, and never edit the lockfile by hand.
3. Commit, `git push -u origin HEAD`, and open the PR with the `open-pr` skill.
