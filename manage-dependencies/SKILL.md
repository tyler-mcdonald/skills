---
name: manage-dependencies
description: Bump a dependency or fix an audit in a separate PR off the default branch. Use when asked to fix a dependency audit or update a dependency.
model: sonnet
---

# Manage Dependencies

Dependency changes always get their own PR off the default branch. Never commit them onto a feature branch, even when that branch's audit check is what failed.

1. Invoke `setup-worktree` with a short title (e.g. "Bump certifi for GHSA-xxxx"). Stay in that worktree for every step.
2. Make the smallest change that does it: bump only the affected packages, to the lowest version that resolves the advisory for an audit, or else the version asked for (the latest if none was). Like Dependabot, update the version in the manifest (`package.json`, `pyproject.toml`, etc.) and let the project's own tool resolve the lockfile (e.g. `uv add <pkg>==<version>`, `npm install <pkg>@<version>`), so the diff shows what changed without reading the lockfile. For a transitive dependency with no manifest entry, upgrade just that package in the lockfile with the tool (e.g. `uv lock --upgrade-package <pkg>==<version>`). If its parent's constraint blocks the fix, bump the parent in the manifest to the lowest version that allows it instead, and if no parent release does, add a temporary override (e.g. `[tool.uv] constraint-dependencies`, `pnpm.overrides`). Never add a transitive dependency to the manifest, and never edit the lockfile by hand.
3. Commit, `git push -u origin HEAD`, and open the PR with the `open-pr` skill.
