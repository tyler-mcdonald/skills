---
name: operator
description: Take a GitHub issue to a ready-for-review PR, hands-off. Use when asked to run the operator on an issue.
---

# Operator

## Steps

1. **Setup.** Invoke `setup-issue` with the issue reference. Stay in that worktree for every step.

2. **Implement.** Spawn a dev subagent with the dev message and wait for the PR URL.

3. **Simplify.** Spawn a fresh subagent with the simplify message and wait for its reply.

4. **Review.** Invoke `code-review-cycle` with the PR number. If it stops without a final score of 4 or 5, stop here and leave the PR as a draft. Otherwise continue to step 5 — its report is not the end of your run.

5. **Sync and ready.**
   1. `git fetch origin && git merge --no-edit origin/<target>`, where target is the PR's base branch.
   2. Resolve any conflicts, keeping the intent of both sides, then `git commit --no-edit`.
   3. If HEAD is still the final review round's `head_sha` (in its `round-<n>.json`), the merge changed nothing and the reviewer already ran the checks there — skip to 4. Otherwise run the project's checks (tests, lint). If they fail, stop and leave the PR as a draft.
   4. `git push` (never force-push), then `gh pr ready <pr>`.

6. **External review.** Wait for the checks by running `gh pr checks <pr> --watch > /dev/null` with `run_in_background` — a review bot can outlast a foreground call's timeout, and unredirected, it reprints the whole table on every refresh. When it exits, note any failing checks for the report and carry on either way. Then list the review bots that commented: `gh api repos/{owner}/{repo}/pulls/<pr>/comments --jq '[.[] | select(.user.type == "Bot") | .user.login] | unique'`. If there are any, invoke `handle-pr-review` with `<pr> — comments from <logins> only` (it runs in its own subagent) and wait for its report — once only; don't wait for or handle a second review pass.

7. **Report.** Brief: where it stopped and why, or the final score, plus any failing checks and the PR's full URL.

## Spawn messages

Simplify:

> Invoke `simplify` on this branch's changes against `origin/<target>`, where target is PR `<pr>`'s base branch. Work in `<worktree path>`. If it changed anything, run the project's checks (tests, lint) and fix any failures it caused, then commit and `git push` (never force-push). Reply with one line: the commit you pushed, or "no changes".

Dev:

> Implement `<issue url>`. Read the issue and its comments (`gh issue view <url> --json title,body,comments`), plus any linked or parent issues — together with any docs they link, they are the plan. Work in `<worktree path>`. Never force-push; to pick up changes from the base branch, merge it instead of rebasing. When done, commit, `git push -u origin <branch>`, and open the PR with the `open-pr` skill, linked to the issue. Reply with the PR URL.
