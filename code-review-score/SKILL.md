---
name: code-review-score
description: Score a branch 1–5 for merge-readiness with /code-review and a fixed rubric, then fix correctness findings in a loop of fresh subagents until it scores 5 or a stop rule fires. Use when asked to score, grade, or rank a code review, or to review-and-fix a branch until it's ready to merge.
---

A harness around `/code-review`. It doesn't change how the review finds issues — it adds a deterministic score (`rubric.md`), a fix loop, and stop rules. Correctness only: nits are reported, never fixed.

You are the operator. You never review or fix code yourself — every review and every fix runs in its own fresh subagent, so no agent grades its own work.

1. **Target.** Use the argument (PR number or branch) if given, otherwise the current branch against the default branch. Effort level is `high` unless the argument names another; keep it the same for every round so scores are comparable.

2. **Review round** (max 3). Spawn a fresh subagent with the reviewer prompt below. It returns a report and the JSON block.

3. **Stop check**, in order, after each review:
   1. Score is 5 → stop: `score_5`.
   2. This was round 3 → stop: `max_rounds`.
   3. Round ≥ 2 and the score didn't go up → stop: `no_progress`.
   4. Every remaining scored finding is escalated (by the fixer in an earlier round, matched by root cause) → stop: `needs_decision`.

   The loop always ends on a review, so the final score reflects the last fix.

4. **Fix round.** Spawn a separate fresh subagent with the fixer prompt below and the scored findings (Blocker, Major, Minor) that aren't escalated. Collect its commit SHA and any new escalations, then go back to step 2.

5. **Report** to the caller: final score, stop reason, a one-line-per-round score history, open escalations (each with the decision needed), and pre-existing issues. End with the JSON block from the last review, with `rounds`, `stop_reason`, and `escalations` filled in from the whole run.

## Reviewer prompt

> Review `<target>` against `<base>`. Do not edit files, commit, or push.
>
> 1. Run the project's checks — tests, lint, typecheck — using the commands its CI, Makefile, package scripts, or CLAUDE.md define. Record pass/fail per check.
> 2. Invoke the `code-review` skill with args `<effort>` (no `--fix`, no `--comment`). If it reports via a findings tool, also include every finding in your reply.
> 3. Apply `~/.claude/skills/code-review-score/rubric.md` exactly: filter which findings count, merge shared root causes, assign verdicts, answer the three severity questions per finding, and compute the score. Show the arithmetic.
> 4. Reply with a findings table (id, file:line, summary, root cause, verdict, where/how/when, severity), the checks, the arithmetic, the score, any finding where the rubric forced a judgment call, and the JSON block from the rubric.

## Fixer prompt

> Fix these findings on `<target>`: `<findings>`. Read the code each one points to before changing it.
>
> - Fix the root cause, not the symptom. Keep each fix minimal and inside the diff's scope.
> - Escalate instead of fixing when the fix needs a design or scope change, a product decision, a change to a public contract (API shape, CLI, config), edits to code the branch didn't touch, or you aren't sure what the intended behavior is. Give one line on the decision needed.
> - Add or update a test when a finding is about untested behavior or when the fix changes behavior.
> - Run the project's tests, lint, and typecheck once all fixes are in; fix anything failing.
> - Make one commit for the round, following the repo's and user's commit conventions. Don't push unless the caller asked.
> - Reply with: each finding id → fixed / escalated (with the decision needed) / not reproducible (with why), the commit SHA, and the check results.
