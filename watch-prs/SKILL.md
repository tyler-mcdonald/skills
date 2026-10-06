---
name: watch-prs
description: Sweep all of the user's open, non-draft PRs and handle review threads last commented on by the user or a bot. Use when asked to watch PRs, typically on a loop (`/loop 1m /watch-prs`).
---

# Watch PRs

One sweep per run. Drafts are never touched — the user keeps a PR in draft to keep it out of reach.

1. Find the PRs with threads to handle:

   ```sh
   ~/.claude/skills/watch-prs/pending-prs.sh
   ```

   It returns the user's open, non-draft PRs across all repos that have unresolved threads whose last comment is the user's or a bot's, skipping threads Claude replied to last. PRs it couldn't fetch are named on stderr — count them as skipped. If it returns `[]`, reply `No PRs need attention.` and stop.

2. For each PR, one at a time, from `~/Projects/<name>`, where `<name>` is the repo name without the owner:
   1. If the directory doesn't exist, `gh repo clone <repo> ~/Projects/<name>` first. If it exists but its `origin` isn't `<repo>`, skip the PR.
   2. Get the branch: `gh pr view <url> --json headRefName,isCrossRepository`. If `isCrossRepository` is true, skip the PR — its branch isn't on `origin`. Run `git fetch origin`.
   3. If `git worktree list` shows the branch checked out anywhere other than `.claude/worktrees/pr-<n>`, skip the PR — the user or another session is working there.
   4. If `.claude/worktrees/pr-<n>` doesn't exist, `git worktree add .claude/worktrees/pr-<n> <branch>`. Then inside it, `git checkout <branch>` and `git merge --ff-only origin/<branch>`. If either fails, skip the PR.
   5. Invoke `handle-pr-review` with:

      > `<url>` — work in `<absolute worktree path>`. Only handle threads whose last comment is from `<user login>` or a bot. Running unattended: never ask the user — when unsure what a comment wants, reply in the thread with a clarifying question instead. Reply in every thread you handle, even when nothing needs doing, so the next sweep skips it.

      Wait for its report before moving to the next PR.

3. Report: each PR's full URL followed by its `handle-pr-review` report, plus one line per skipped PR and why. Nothing else.
