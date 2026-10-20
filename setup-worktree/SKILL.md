---
name: setup-worktree
description: Create or enter an isolated git worktree named after a short title. Use as the setup step before making changes on a new branch.
---

# Setup Worktree

Args: a short title, and optionally a base branch (defaults to the repo's default branch).

1. Slugify the title from the args into kebab-case: lowercase, collapse non-alphanumeric runs into a single hyphen, trim leading/trailing hyphens, truncate to 64 chars.
   - Example: "Fix static asset serving" -> `fix-static-asset-serving`
2. Run `git fetch origin` so the worktree branches from the latest base. If it fails, warn that the base may be stale and continue.
3. If no base was given and the session isn't already in a worktree, call `EnterWorktree` with `name: <slug>`; the worktree and its branch are both named `<slug>`. If a worktree with that name already exists, enter it with `path` instead.
4. Otherwise `EnterWorktree` can't create it: run `git worktree add <main checkout>/.claude/worktrees/<slug> -b <slug> origin/<base>`, with `<base>` defaulting to the repo's default branch, where `<main checkout>` is the parent of `git rev-parse --path-format=absolute --git-common-dir`, then enter it with `EnterWorktree` `path`. If that worktree already exists, just enter it.
5. Return the branch and worktree path.
