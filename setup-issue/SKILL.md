---
name: setup-issue
description: Resolve a GitHub issue and create an isolated git worktree named after it. Use as the setup step before working on an issue, or when asked to set up a worktree for an issue.
---

# Setup Issue

1. Parse the issue reference from the args (bare number, full URL, or `owner/repo#N`).
2. Fetch it: `gh issue view <ref> --json number,title,body,url`. If `gh` fails or the issue doesn't exist, stop and surface the exact error.
3. Slugify the title into kebab-case: lowercase, collapse non-alphanumeric runs into a single hyphen, trim leading/trailing hyphens, truncate to 64 chars.
   - Example: "Fix static asset serving" -> `fix-static-asset-serving`
4. Call `EnterWorktree` with `name: <slug>`; the worktree and its branch are both named `<slug>`. If a worktree with that name already exists, enter it with `path` instead.
5. Return the issue number, title, URL, branch, and worktree path.
