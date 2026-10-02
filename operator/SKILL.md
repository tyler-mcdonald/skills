---
name: operator
description: Take a GitHub issue to a ready-for-review PR, hands-off. Use when asked to run the operator on an issue.
---

# Operator

## Steps

1. **Setup.** Invoke `setup-issue` with the issue reference. Stay in that worktree for every step.

2. **Implement.** Spawn a dev subagent with the dev message and wait for the PR URL.

3. **Review.** Invoke `code-review-score` with the PR number. If it stops without a final score of 4 or 5, stop here and leave the PR as a draft. Otherwise continue to step 4 — its report is not the end of your run.

4. **Sync and ready.**
   1. `git fetch origin && git merge --no-edit origin/<target>`, where target is the PR's base branch.
   2. Resolve any conflicts, keeping the intent of both sides, then `git commit --no-edit`.
   3. Run the project's checks (tests, lint). If they fail, stop and leave the PR as a draft.
   4. `git push` (never force-push), then `gh pr ready <pr>`.

5. **Greptile.** Watch Greptile's check with `gh pr checks <pr> --watch`. Once it finishes, if it posted findings, invoke `handle-pr-review` with the PR number — once only; don't wait for or handle a second Greptile pass.

6. **Report.** Brief: where it stopped and why, or the final score, plus the PR's full URL.

## Spawn message

Dev:

> Implement `<issue url>`. Read the issue and its comments (`gh issue view <url> --json title,body,comments`), plus any linked or parent issues — together with any docs they link, they are the plan. Work in `<worktree path>`. Never force-push; to pick up changes from the base branch, merge it instead of rebasing. When done, commit, `git push -u origin <branch>`, and open a draft PR: `gh pr create --draft --title "<title>" --body "Closes #<issue number>"`. Reply with the PR URL.
