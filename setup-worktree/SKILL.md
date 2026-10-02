---
name: setup-worktree
description: Create or enter an isolated git worktree named after a short title. Use as the setup step before making changes on a new branch.
---

# Setup Worktree

1. Slugify the title from the args into kebab-case: lowercase, collapse non-alphanumeric runs into a single hyphen, trim leading/trailing hyphens, truncate to 64 chars.
   - Example: "Fix static asset serving" -> `fix-static-asset-serving`
2. Call `EnterWorktree` with `name: <slug>`; the worktree and its branch are both named `<slug>`. If a worktree with that name already exists, enter it with `path` instead.
3. Return the branch and worktree path.
