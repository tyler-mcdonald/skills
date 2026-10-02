---
name: setup-worktree
description: Create or enter an isolated git worktree named after a short title. Use as the setup step before making changes on a new branch.
---

# Setup Worktree

1. Slugify the title from the args into kebab-case: lowercase, collapse non-alphanumeric runs into a single hyphen, trim leading/trailing hyphens, truncate to 64 chars.
   - Example: "Fix static asset serving" -> `fix-static-asset-serving`
2. Run `git fetch origin` so the worktree branches from the latest default branch. If it fails, warn that the base may be stale and continue.
3. Call `EnterWorktree` with `name: <slug>`; the worktree and its branch are both named `<slug>`. If a worktree with that name already exists, enter it with `path` instead.
4. Return the branch and worktree path.
