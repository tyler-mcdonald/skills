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

5. **Sync.**
   1. `git fetch origin && git merge --no-edit origin/<target>`, where target is the PR's base branch.
   2. Resolve any conflicts, keeping the intent of both sides, then `git commit --no-edit`.
   3. If HEAD is still the final review round's `head_sha` (in its `round-<n>.json`), the merge changed nothing and the reviewer already ran the checks there — skip this. Otherwise run the project's checks (tests, lint). If they fail, stop and leave the PR as a draft.

6. **Bot review.** The PR stays a draft until the review bot is done with it. Pick the bot by the config file in the repo root:

   | Config | Bot login | Trigger comment |
   | --- | --- | --- |
   | `.coderabbit.yaml` | `coderabbitai[bot]` | `@coderabbitai review` |
   | `.greptile/` | `greptile-apps[bot]` | `@greptileai` |

   If none is there, skip to step 7 and note it for the report. Otherwise run up to 3 rounds:
   1. `git push` (never force-push). Note `git rev-parse HEAD` as the round's sha and `date -u +%Y-%m-%dT%H:%M:%SZ` as its start time, then `gh pr comment <pr> --body "<trigger comment>"`.
   2. Run `~/.claude/skills/operator/wait-bot-review.sh <pr> <bot login> <sha> <start time>` with `run_in_background` and wait for it. It prints the number of new threads the bot opened. If it exits non-zero, the bot didn't review within 20 minutes — stop here and leave the PR as a draft.
   3. Invoke `handle-pr-review` with `<pr> — comments from <bot login> only` (it runs in its own subagent) and wait for its report, then `git pull`.
   4. If the bot opened no new threads, or HEAD is still the round's sha, the bot is done — go to step 7. If this was round 3, stop and leave the PR as a draft, listing the bot's open threads for the report. Otherwise start the next round.

7. **Re-sync.** `git fetch origin`. If `git merge-base --is-ancestor origin/<target> HEAD` succeeds, skip this. Otherwise repeat step 5's merge, resolve, and checks.

8. **Ready.** `git push` (never force-push), then `gh pr ready <pr>`.

9. **In review.** Invoke `set-issue-status` with the issue URL and `In review`.

10. **QA.** Decide whether the change needs hands-on QA: it does only if it changes something a person can see or exercise through the app's UI. Skip this step for backend or API-only changes (even ones that change API behavior or responses), docs, config, tests, or internal refactors — tests and the review cover those.
    1. Invoke `run` in the worktree to start the app.
    2. Give the user a short bulleted list of the high-level functionality to test — one line each: what to do and what should happen. Then wait for their pass or fail.
    3. On a fail, spawn a fresh subagent with the QA fix message, wait for its reply, then go back to 1. Don't trigger the review bot for QA fixes.
    4. On a pass, stop the servers.

11. **Report.** Brief: where it stopped and why, or the final score, plus the number of bot review rounds, any failing checks in `gh pr checks <pr>`, and the PR's full URL.

## Spawn messages

Simplify:

> Invoke `simplify` on this branch's changes against `origin/<target>`, where target is PR `<pr>`'s base branch. Work in `<worktree path>`. If it changed anything, run the project's checks (tests, lint) and fix any failures it caused, then commit and `git push` (never force-push). Reply with one line: the commit you pushed, or "no changes".

QA fix:

> Fix these QA findings on PR `<pr>`: `<findings>`. Work in `<worktree path>`. Before committing, invoke `code-review` with `--fix` on your uncommitted changes. Run the project's checks (tests, lint) and fix any failures, then commit and `git push` (never force-push). Reply with one line: the commit you pushed.

Dev:

> Implement `<issue url>`. Read the issue and its comments (`gh issue view <url> --json title,body,comments`), plus any linked or parent issues — together with any docs they link, they are the plan. Work in `<worktree path>`. Never force-push; to pick up changes from the base branch, merge it instead of rebasing. When done, commit, `git push -u origin <branch>`, and open the PR with the `open-pr` skill, linked to the issue. Reply with the PR URL.
