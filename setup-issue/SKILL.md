---
name: setup-issue
description: Resolve a GitHub issue and create an isolated git worktree named after it. Use as the setup step before working on an issue, or when asked to set up a worktree for an issue.
---

# Setup Issue

1. Parse the issue reference from the args (bare number, full URL, or `owner/repo#N`).
2. Fetch it: `gh issue view <ref> --json number,title,body,url`. If `gh` fails or the issue doesn't exist, stop and surface the exact error.
3. Find its open blockers: `gh api repos/<owner>/<repo>/issues/<n>/dependencies/blocked_by`, keeping only those with `state` `open`. For each, find its open PR (one whose closing issue references include the blocker).
   1. If a blocker has no PR, poll every minute for up to 15 minutes. If none appears, stop and report that the blocker has no PR.
   2. If there's more than one open blocker PR, stop and ask which to stack on.
4. Invoke `setup-worktree` with the issue title.
5. If there's a blocker PR, `git merge --no-edit origin/<head>`, where head is that PR's head branch (never rebase). That branch is the base; otherwise the base is the default branch.
6. Invoke `set-issue-status` with the issue URL and `In progress`.
7. Return the issue number, title, URL, branch, base branch, and worktree path.
