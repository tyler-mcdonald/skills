---
name: code-review-score
description: Score a branch 1–5 for merge-readiness with /code-review and a fixed rubric, then fix correctness findings in a loop of fresh subagents until it scores 5 or a stop rule fires. Use when asked to score, grade, or rank a code review, or to review-and-fix a branch until it's ready to merge.
---

A harness around `/code-review`. It doesn't change how the review finds issues — it adds a goal to review against, a deterministic score (`rubric.md`), a fix loop, and stop rules. Correctness only: nits are reported, never fixed.

You are the operator. You never review or fix code yourself — every review and every fix runs in its own fresh subagent, so no agent grades its own work.

You also never reword or add to what passes between them. Fill the prompt templates below by their slots only. Findings travel as files, not paraphrase: create a run directory outside the repo (the session's temp dir), have each reviewer write its JSON block to `<run_dir>/round-<n>.json`, and give the fixer that path plus the finding ids to fix. The only thing you add is the caller's decisions.

0. **Grounding.** Find the goal the branch is meant to deliver:
   1. The PR for the target (`gh pr view`): its closing issues (`closingIssuesReferences`), then `Closes/Fixes/Resolves #N` in the body.
   2. Read each issue (`gh issue view <n> --comments`).
   3. If there's no linked issue, a PR description that states the goal and what "done" means counts as grounding.

   If none of these exist, stop before reviewing: `needs_grounding`. Report what you checked and ask the caller to link an issue or describe the goal. Never infer the goal from the diff or commit messages — that grades the code against itself.

   Summarize the goal as a few lines plus the acceptance criteria (stated or clearly implied by the issue). This is `<goal>` in both prompts.

   If the caller asks you to draft the issue, state acceptance criteria as outcomes ("prod can't boot local settings"), not mechanisms ("every error names the variable"), list anything extra under out of scope, and get the caller's approval before creating it.

1. **Target.** Use the argument (PR number or branch) if given, otherwise the current branch against the default branch. Effort level is `high` unless the argument names another; keep it the same for every round so scores are comparable.

   **Decisions.** Collect any rulings the caller has made on findings — "accepted as intended" with a reason. These are `<decisions>`. Only the caller makes decisions; a fixer's escalation is not one.

2. **Review round** (max 3). Spawn a fresh subagent with the reviewer prompt below. It returns a report and the JSON block.

3. **Stop check**, in order, after each review:
   1. Score is 5 → stop: `score_5`.
   2. This was round 3 → stop: `max_rounds`.
   3. Round ≥ 2 and neither the score went up nor the number of scored findings went down → stop: `no_progress`.
   4. Every remaining scored finding is escalated (by the fixer in an earlier round, matched by root cause) → stop: `needs_decision`.

   The loop always ends on a review, so the final score reflects the last fix.

4. **Fix round.** Spawn a separate fresh subagent with the fixer prompt below, the path to this round's JSON, and the ids of the scored findings (Blocker, Major, Minor) that aren't escalated. Collect its commit SHA and any new escalations, then go back to step 2.

5. **Report** to the caller: the goal it was reviewed against, final score, stop reason, a one-line-per-round score history, open escalations (each with the decision needed), accepted findings, beyond-the-goal findings (with their follow-up suggestions), and pre-existing issues. End with the JSON block from the last review, with `rounds`, `stop_reason`, and `escalations` filled in from the whole run.

## Reviewer prompt

> Review `<target>` against `<base>`. Do not edit files, commit, or push.
>
> The branch's goal (from `<issue or PR>`): `<goal>`
>
> Decisions already made by the user — report matching findings as `accepted`, don't score them, but do flag anything new about them: `<decisions>`
>
> 1. Run the project's checks — tests, lint, typecheck — using the commands its CI, Makefile, package scripts, or CLAUDE.md define. Record pass/fail per check.
> 2. Invoke the `code-review` skill with args `<effort>` (no `--fix`, no `--comment`). If it reports via a findings tool, also include every finding in your reply.
> 3. Check the diff against the goal: list each acceptance criterion as met / unmet / partly met, with evidence.
> 4. Apply `~/.claude/skills/code-review-score/rubric.md` exactly: filter which findings count, merge shared root causes, assign verdicts, answer the three severity questions per finding, and compute the score. Show the arithmetic.
> 5. Write the JSON block to `<run_dir>/round-<n>.json`.
> 6. Reply with the acceptance-criteria check, a findings table (id, file:line, summary, root cause, verdict, where/how/when, severity), the checks, the arithmetic, the score, any finding where the rubric forced a judgment call, and the JSON block from the rubric.

## Fixer prompt

> Fix findings `<ids>` on `<target>`, as described in `<run_dir>/round-<n>.json`. Read the code each one points to before changing it.
>
> The branch's goal (from `<issue or PR>`): `<goal>`
>
> Decisions already made by the user — don't change behavior they accept: `<decisions>`
>
> - Fix the root cause, not the symptom, in the way that serves the goal. Keep each fix minimal and inside the goal's scope. Never patch a symptom just to clear a finding — if the real fix is out of scope, escalate it as a follow-up.
> - Prefer removing code to adding it. If a fix needs a new mechanism (a subclass, wrapper, override, or hand-rolled parsing), escalate instead.
> - Escalate instead of fixing when the fix needs a design or scope change, a product decision, a change to a public contract (API shape, CLI, config), edits to code the branch didn't touch, or you aren't sure what the intended behavior is. Give one line on the decision needed.
> - Add or update a test when a finding is about untested behavior or when the fix changes behavior.
> - Run the project's tests, lint, and typecheck once all fixes are in; fix anything failing.
> - Make one commit for the round, following the repo's and user's commit conventions. Don't push unless the caller asked.
> - Reply with: each finding id → fixed / escalated (with the decision needed) / not reproducible (with why), the commit SHA, and the check results.
