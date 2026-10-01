---
name: operator
description: Take a GitHub issue to a ready-for-review PR mostly hands-off — sets up a worktree, has a dev subagent plan and implement it, runs code-review-score, then syncs the target branch and marks the PR ready. Use when asked to run the operator or the software factory on an issue.
---

# Operator

You manage agents; you don't write the feature code yourself. Only real decisions go to the user — everything else you settle from the issue and the codebase.

`<run_dir>` is `operator/<slug>/` under `$CLAUDE_JOB_DIR/tmp` if set, otherwise a new `mktemp -d`.

## Steps

1. **Setup.** Invoke `setup-issue` with the issue reference. Stay in that worktree for every step.

2. **Brief.** Spawn a dev subagent with the dev message. It writes `<run_dir>/brief.md` (plan, assumptions, gaps, discrepancies) and returns without coding.

3. **Resolve the brief.** Check each item against the issue and codebase. Settle what they answer. Ask the user only about genuine decisions. Write every resolution, including the user's answers, to `<run_dir>/resolutions.md`, then load `SendMessage` via ToolSearch and resume the same dev agent by its ID with the resume message. It implements, pushes, and opens a draft PR.

4. **Post decisions.** For each decision the user made, post a PR comment: `Decision: <their answer>`. Clean up wording into one or two readable sentences; never add to what they said. Never post a decision the user didn't make.

5. **Review.** Invoke `code-review-score` with the PR number. If it stops without a final score of 4 or 5, stop here and leave the PR as a draft. Otherwise continue to step 6 — its report is not the end of your run.

6. **Sync and ready.**
   1. `git fetch origin && git merge --no-edit origin/<target>`, where target is the PR's base branch.
   2. Resolve any conflicts, keeping the intent of both sides, then `git commit --no-edit`.
   3. Run the project's checks (tests, lint). If they fail, stop and leave the PR as a draft.
   4. `git push` (never force-push), then `gh pr ready <pr>`.

7. **Report.** Brief: where it stopped and why, or the final score, plus the PR's full URL.

## Spawn messages

Dev:

> Read and follow `~/.claude/skills/operator/dev.md`. Issue: `<url>`. Worktree: `<path>`. Run directory: `<run_dir>`.

Resume:

> Resolutions are in `<run_dir>/resolutions.md`. Continue with step 2 of `dev.md`.
