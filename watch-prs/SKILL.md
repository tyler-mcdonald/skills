---
name: watch-prs
description: Sweep all of the user's open, non-draft PRs and handle review threads last commented on by the user or a bot. Use when asked to watch PRs, typically on a loop (`/loop 1m /watch-prs`).
---

# Watch PRs

One sweep per run. Drafts are never touched — the user keeps a PR in draft to keep it out of reach.

The user reads this like a log, not a chat. Print nothing except the result lines in step 3: no narration, no progress updates, no summary.

1. Find the PRs with threads to handle:

   ```sh
   ~/.claude/skills/watch-prs/pending-prs.sh
   ```

   It returns the user's open, non-draft PRs that have unresolved threads whose last comment is the user's or a bot's, skipping threads Claude replied to last. Each has a `status`: `Ready`, or a skip — `User Input Pending` (the user has an unsubmitted review), `In Progress` (an earlier sweep's handler is still running), or `Error`. If it returns `[]`, print nothing and stop.

2. Set `PROJECTS_DIR` to `${WATCH_PRS_PROJECTS_DIR:-$HOME/Projects}`. For each `Ready` PR, one at a time, from `$PROJECTS_DIR/<name>`, where `<name>` is the repo name without the owner:
   1. If the directory doesn't exist, `gh repo clone <repo> "$PROJECTS_DIR/<name>"` first. If it exists but its `origin` isn't `<repo>`, skip it as `Error`.
   2. Get the branch: `gh pr view <url> --json headRefName,isCrossRepository`. If `isCrossRepository` is true, skip it as `Error`. Run `git fetch origin`.
   3. If `git worktree list` shows the branch checked out anywhere other than `.claude/worktrees/pr-<n>`, skip it as `Branch In Use`.
   4. If `.claude/worktrees/pr-<n>` doesn't exist, `git worktree add .claude/worktrees/pr-<n> <branch>`. Then inside it, `git checkout <branch>` and `git merge --ff-only origin/<branch>`. If either fails, skip it as `Error`.
   5. `touch .claude/worktrees/pr-<n>.lock`, then invoke `handle-pr-review` with:

      > `<url>` — work in `<absolute worktree path>`. Only handle threads whose last comment is from `<user login>` or a bot. Running unattended: never ask the user — when unsure what a comment wants, reply in the thread with a clarifying question instead. Reply in every thread you handle, even when nothing needs doing, so the next sweep skips it. Report only one word, the first that applies: `Failed` (a check, the push, or a reply failed), `Asked` (you posted a clarifying question), `Changed` (you pushed code changes), `Replied`.

      Wait for its report, then `rm -f .claude/worktrees/pr-<n>.lock` before moving to the next PR.

3. Print one line per PR, nothing else:

   ```
   <url>: Skipped - User Input Pending | In Progress | Branch In Use | Error
   <url>: Done - Failed | Asked | Changed | Replied
   ```
