---
name: setup-issue
description: Resolve a GitHub issue and create an isolated git worktree named after it. Use as the setup step before working on an issue, or when asked to set up a worktree for an issue.
---

# Setup Issue

1. Parse the issue reference from the args (bare number, full URL, or `owner/repo#N`).
2. Fetch it: `gh issue view <ref> --json number,title,body,url`. If `gh` fails or the issue doesn't exist, stop and surface the exact error.
3. Invoke `setup-worktree` with `<number> <title>`, so the worktree is named `<number>-<title-slug>`.
   - Example: issue 12 "Fix static asset serving" -> `12-fix-static-asset-serving`
4. Return the issue number, title, URL, branch, and worktree path.
