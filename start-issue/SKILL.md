---
name: start-issue
description: Start work on a GitHub issue by creating a worktree for it and setting it to In progress. Use before working on an issue, or when asked to start one or set up its worktree.
---

# Start Issue

1. Parse the issue reference from the args (bare number, full URL, or `owner/repo#N`).
2. Fetch it: `gh issue view <ref> --json number,title,body,url`. If `gh` fails or the issue doesn't exist, stop and surface the exact error.
3. Find its open blockers: `gh api repos/<owner>/<repo>/issues/<n>/dependencies/blocked_by`, keeping only open ones. For each, find its branch on origin, in order:
   1. Its open PR's head branch.
   2. A branch linked to it (`gh issue develop --list <n>`).
   3. A branch named after its title.

   If a blocker is in another repo, has no branch or more than one, or there's more than one open blocker, stop and ask the user what to stack on.
4. Invoke `setup-worktree` with the issue title.
5. If there's a blocker branch, `git fetch origin <branch>` and `git merge --no-edit origin/<branch>` (never rebase). That branch is the base; otherwise the base is the default branch. If the fetch or merge fails, stop and surface the exact error.
6. Invoke `set-issue-status` with the issue URL and `In progress`.
7. Return the issue number, title, URL, branch, base branch, and worktree path.
