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

6. **QA.** Invoke `user-qa` in the worktree and wait for it to finish.

7. **Bot review.** `git push` (never force-push), then invoke `trigger-bot-review` with the PR number.
   - `none`: go to step 9.
   - `timed out`: stop here and leave the PR as a draft.

8. **Hand off to CI.** One pass only — don't re-trigger the bot or CI.
   1. Run the thread check. If it prints `[]`, go to step 9.
   2. If no file in `.github/workflows/` calls `tyler-mcdonald/agent-workflows/.github/workflows/handle-review.yml`, stop here, leave the PR as a draft, and report that the bot's threads need handling by hand.
   3. `gh api repos/<owner>/<repo>/issues/<pr>/comments -f body="@claude" --jq .created_at` — exactly that body. Note the `created_at` it prints.
   4. Wait for the `Handle review` run that comment started, then for it to finish (up to 35 minutes). Every PR comment, review, and review comment starts a run with that name, so pick it by all of:
      - listed by `gh run list --workflow "Handle review" --event issue_comment --created ">=<created_at>" --json databaseId,status,conclusion` (these runs report branch `main`, so don't filter by the PR branch);
      - in `gh run view <run-id> --json jobs`, the job whose name ends in `gate` has finished and the one whose name ends in `handle` is not `skipped`.
   5. If that run's `handle` job concludes anything but `success`, stop here and leave the PR as a draft.
   6. Run the thread check again. If it prints anything but `[]`, stop here and leave the PR as a draft.
   7. `git pull` so the worktree matches the PR.

9. **Ready.** `gh pr ready <pr>`, then invoke `set-issue-status` with the issue URL and `In review`.

10. **Report.** Brief: where it stopped and why, or the final score, plus the bot outcome, the CI outcome, and the PR's full URL.

## Thread check

```sh
~/.claude/skills/operator/unhandled-bot-threads.sh <pr> "<bot login>" <owner>/<repo>
```

Prints a JSON array of the unresolved review threads the bot opened that have no reply from Claude; `[]` means there are none. `<bot login>` is the active row's login in `trigger-bot-review/review-bots.md`.

If it exits non-zero or prints anything other than a JSON array, the check failed, which is not an empty result: stop there and leave the PR as a draft.

## Spawn messages

Simplify:

> Invoke `simplify` on this branch's changes against `origin/<target>`, where target is PR `<pr>`'s base branch. Work in `<worktree path>`. If it changed anything, run the project's checks (tests, lint) and fix any failures it caused, then commit and `git push` (never force-push). Reply with one line: the commit you pushed, or "no changes".

Dev:

> Implement `<issue url>`. Read the issue and its comments (`gh issue view <url> --json title,body,comments`), plus any linked or parent issues — together with any docs they link, they are the plan. Work in `<worktree path>`. Never force-push; to pick up changes from the base branch, merge it instead of rebasing. When done, commit, `git push -u origin <branch>`, and open the PR with the `open-pr` skill, linked to the issue. Reply with the PR URL.
