---
name: manage-dependencies
description: Bump a dependency or fix an audit in a separate PR off the default branch. Use when asked to fix a dependency audit or update a dependency.
---

# Manage Dependencies

Dependency changes always get their own PR off the default branch. Never commit them onto a feature branch, even when that branch's audit check is what failed.

1. Invoke `setup-worktree` with a short title (e.g. "Bump certifi for GHSA-xxxx"). Stay in that worktree for every step.
2. Make the smallest change that does it: bump only the affected packages, to the lowest version that resolves the advisory for an audit, or else the version asked for (the latest if none was). Use the project's own tool and pin the exact version (e.g. `uv lock --upgrade-package <pkg>==<version>`, `npm install <pkg>@<version>`), so it regenerates the lockfile rather than you editing it by hand.
3. Run the project's checks (tests, lint), and re-run the audit if this is an audit fix. If the audit still fails or no fixed version exists, stop and report why.
4. Commit with a single line naming the package, version, and advisory if any (e.g. "Bump certifi to 2026.10.19 for GHSA-xxxx"). `git push -u origin HEAD`, then open the PR into the base (`--base <base>`) with the `open-pr` skill.
