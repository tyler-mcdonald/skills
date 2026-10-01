---
name: code-review-score
description: Score a branch 1–5 for merge-readiness with /code-review and a fixed rubric, then fix correctness findings in a loop of fresh subagents until it scores 5 or a stop rule fires. Use when asked to score, grade, or rank a code review, or to review-and-fix a branch until it's ready to merge.
---

A harness around `/code-review`. It doesn't change how the review finds issues — it adds a goal to review against, a deterministic score (`rubric.md`), a fix loop, and stop rules. Correctness only: nits are reported, never fixed.

You are the operator. You never review or fix code yourself — every review and every fix runs in its own fresh subagent, so no agent grades its own work.

You also never summarize, reword, or add to anything that passes between agents. Everything travels as files in a run directory; subagents read the goal, decisions, and findings from their sources themselves. Your spawn messages are the fixed templates at the bottom, with only their parameters filled in.

## Run directory

`<run_dir>` is `code-review-score/<branch>/` under the session's temp dir (`$CLAUDE_JOB_DIR/tmp` if set, otherwise a new `mktemp -d`). It holds:

| File | Written by | Contents |
|---|---|---|
| `run.json` | operator | `{ "repo_dir", "target", "base", "effort", "goal_source" }` |
| `decisions.md` | operator | The caller's rulings on findings, quoted word for word, one per bullet. Empty if none. |
| `round-<n>.json` | reviewer | The rubric's JSON block for round `n`. |
| `fix-<n>.json` | fixer | `{ "results": [{ "finding_id", "status", "note" }], "commit", "checks", "escalations": [{ "finding_id", "decision_needed" }] }` |

## Steps

0. **Grounding.** Find the source of the goal — don't read it for meaning, just confirm it exists:
   1. The PR for the target (`gh pr view`): its closing issues (`closingIssuesReferences`), then `Closes/Fixes/Resolves #N` in the body.
   2. If there's no linked issue, a PR description that states the goal and what "done" means.

   Record it as `goal_source` (`"#142"`, or `"PR #141 description"`). If neither exists, stop before reviewing: `needs_grounding`. Report what you checked and ask the caller to link an issue or describe the goal. Never derive the goal from the diff or commit messages.

   If the caller asks you to draft the issue, state acceptance criteria as outcomes ("prod can't boot local settings"), not mechanisms ("every error names the variable"), list anything extra under out of scope, and get the caller's approval before creating it.

1. **Set up the run.** Target is the argument (PR number or branch) if given, otherwise the current branch; base is the default branch. Effort is `high` unless the argument names another, and stays the same for every round. Write `run.json`. Write `decisions.md` from the caller's own words — only the caller makes decisions; a fixer's escalation is not one.

2. **Review round** (max 3). Spawn a fresh subagent with the reviewer message. When it returns, read `round-<n>.json`.

3. **Stop check**, in order:
   1. Score is 5 → stop: `score_5`.
   2. This was round 3 → stop: `max_rounds`.
   3. Round ≥ 2 and neither the score went up nor the number of scored findings went down → stop: `no_progress`.
   4. Every scored finding matches, by root cause, an escalation in an earlier `fix-<n>.json` → stop: `needs_decision`.

   The loop always ends on a review, so the final score reflects the last fix.

4. **Fix round.** Spawn a separate fresh subagent with the fixer message, passing the ids of scored findings (Blocker, Major, Minor) that aren't escalated. When it returns, read `fix-<n>.json`, then go back to step 2.

5. **Report** to the caller, built from the run files: goal source, final score, stop reason, one line per round (score, commit), open escalations with the decision needed, accepted findings, beyond-the-goal findings with their follow-ups, and pre-existing issues. End with the last `round-<n>.json`, with `rounds`, `stop_reason`, and `escalations` filled in from the whole run.

## Spawn messages

Use these exactly. Add nothing.

Reviewer:

> Read and follow `~/.claude/skills/code-review-score/reviewer.md`. Run directory: `<run_dir>`. Round: `<n>`.

Fixer:

> Read and follow `~/.claude/skills/code-review-score/fixer.md`. Run directory: `<run_dir>`. Round: `<n>`. Finding ids: `<ids>`.
