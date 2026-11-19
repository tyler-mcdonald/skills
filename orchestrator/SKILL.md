---
name: orchestrator
description: Take a GitHub issue to a ready-for-review PR, hands-off. Use when asked to run the orchestrator on an issue.
model: sonnet
---

# Orchestrator

## Steps

1. Setup
   - Invoke `start-issue` with the issue reference.
   - If it reports a blocker that's still in progress, stop here and raise it to the user.
   - Stay in that worktree for every step.

2. Implement
   1. Spawn an Opus dev subagent with the dev message.
   2. Wait for the PR URL.

3. QA
   1. Skip this unless the change affects something a person can see or use in the app's UI. Backend or API-only changes (even ones that change API behavior), docs, config, tests, and internal refactors don't count.
   2. Otherwise invoke `user-qa` in the worktree and wait for it to finish, then commit and `git push` any fixes.

4. Refine
   1. Spawn a fresh Opus subagent with the refine message.
   2. Wait for its reply.

5. Review
   1. Invoke `code-review-cycle` with the PR number.
   2. If it stops without a final score of 4 or 5, stop here and leave the PR as a draft.
   3. Otherwise continue to step 6 — its report is not the end of your run.

6. Sync
   1. `git fetch origin && git merge --no-edit origin/<target>`, where target is the PR's base branch.
   2. Resolve any conflicts, keeping the intent of both sides, then `git commit --no-edit`.

7. Bot review
   1. `git push` (never force-push).
   2. Run `gh pr checks <pr> --watch --fail-fast` in the background.
   3. If CI fails, fix it and push until it passes.
   4. Invoke `trigger-bot-review` with the PR number.
   5. `gh pr ready <pr>`.
   6. Invoke `set-issue-status` with the issue URL and `In review`.
   7. If `trigger-bot-review` replied `none`, go to step 9 (Report).
   8. Read the triggered bot's row in `trigger-bot-review/review-bots.md`. If its "Done when" is `Unknown`, stop here.
   9. Run the bot wait in the background and wait for it to exit. If it prints anything other than `done`, stop here.

8. Hand off to CI

   One pass only — don't re-trigger the bot or CI.

   1. Run the thread check. If it prints `[]`, go to step 9.
   2. If no file in `.github/workflows/` calls `tyler-mcdonald/agent-workflows/.github/workflows/handle-review.yml`, stop here and report that the bot's threads need handling by hand.
   3. `gh pr comment <pr> --body "@claude"`.
   4. Rerun the thread check once a minute for up to 35 minutes, until it prints `[]`. If it never does, stop here.
   5. `git pull` so the worktree matches the PR.

9. Report
   - Keep it brief: where it stopped and why, or the final score, plus the refine findings applied and rejected, the bot outcome, the CI outcome, and the PR's full URL.

## Thread check

```sh
<skill dir>/unhandled_bot_threads.py <pr> "<bot login>" <owner>/<repo>
```

`<skill dir>` is this skill's base directory. Prints a JSON array of the unresolved review threads the bot opened that have no reply from Claude; `[]` means there are none. `<bot login>` is the login `trigger-bot-review` replied with.

If it exits non-zero or prints anything other than a JSON array, the check failed, which is not an empty result: stop there.

## Bot wait

```sh
<skill dir>/await_bot_review.py <pr> "<bot login>" "<trigger comment>" "<done text>" <owner>/<repo>
```

Takes the trigger comment and the backticked text in "Done when" from the bot's row in `trigger-bot-review/review-bots.md`. Checks the PR's comments once a minute for up to 15 minutes, and prints `done` once a comment the bot posted or edited after the latest trigger comment contains the done text, or `timeout` if none does. Exits non-zero if the first check fails, since a wrong PR, repo, or gh auth won't fix itself; later failed checks are retried. It can outlast a foreground Bash call, so always run it with `run_in_background`.

## Spawn messages

Refine:

> Invoke `refine-diff` with base `<target>`, where target is PR `<pr>`'s base branch, and goal `<issue url>`. Work in `<worktree path>`.

Dev:

> Implement `<issue url>`. Read the issue and its comments (`gh issue view <url> --json title,body,comments`), plus any linked or parent issues — together with any docs they link, they are the plan. Work in `<worktree path>`. Never force-push; to pick up changes from the base branch, merge it instead of rebasing. When all the code is written, run lint, typecheck, and only the tests for your changes (CI runs the full suite), then commit, `git push -u origin <branch>`, and open the PR against `<base branch>` with the `open-pr` skill, linked to the issue. Reply with the PR URL.
