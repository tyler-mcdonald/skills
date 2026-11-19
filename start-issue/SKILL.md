---
name: start-issue
description: Set up a GitHub issue for work and mark it In progress. Use before working on an issue, or when asked to start one or set up its worktree.
---

# Start Issue

1. Parse the issue reference from the args (bare number, full URL, or `owner/repo#N`).
2. Fetch it: `gh issue view <ref> --json number,title,body,url`. If `gh` fails or the issue doesn't exist, stop and surface the exact error.
3. Find its open blockers: `gh api repos/<owner>/<repo>/issues/<n>/dependencies/blocked_by`, keeping only open ones. For each, find its branch on origin, in order:
   1. Its open PR's head branch.
   2. A branch linked to it (`gh issue develop --list <n>`).
   3. A branch named after its title.

   Skip blockers with no branch yet. If a blocker has a branch but no open PR, it's still in progress: stop and report it. If one blocker branch contains all the others (or it's the only one), stack on it. Stop and ask the user what to stack on only if a blocker is in another repo, a blocker has more than one branch, or the blocker branches diverge.
4. Invoke `setup-worktree` with the issue title, then `git push -u origin HEAD` so issues blocked by this one can find its branch.
5. If there's a branch to stack on, `git fetch origin <branch>` and `git merge --no-edit origin/<branch>` (never rebase). That branch is the base; otherwise the base is the default branch. If the fetch or merge fails, stop and surface the exact error.
6. Invoke `set-issue-status` with the issue URL and `In progress`. Then check for a parent with `gh api repos/<owner>/<repo>/issues/<n>/parent` (a 404 means none). If there is one, invoke `set-issue-status` again with the parent's URL.
7. Return the issue number, title, URL, branch, base branch, and worktree path.
