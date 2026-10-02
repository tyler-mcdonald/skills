---
name: code-review-score
description: Score a branch 1–5 for merge-readiness with /code-review and a fixed rubric, then fix the findings the rubric marks for fixing in a loop of fresh subagents until it scores 5 or a stop rule fires. Use when asked to score, grade, or rank a code review, or to review-and-fix a branch until it's ready to merge.
---

A harness around `/code-review`. It doesn't change how the review finds issues — it adds a goal to review against, a deterministic score (`rubric.md`), a fix loop, and stop rules. `rubric.md` decides which findings are fixed (`"fix": true`).

You are the coordinator. You never review or fix code yourself — every review and every fix runs in its own fresh subagent, so no agent grades its own work.

You also never summarize, reword, or add to anything that passes between agents. Everything travels as files in a run directory; subagents read the goal, decisions, and findings from their sources themselves.

**Decisions** are the user's `Decision:` comments on the PR (e.g. `Decision: WSGI/ASGI stay env-only (twelve-factor).`), as `inputs.md` defines them. Subagents read them from the PR; nobody copies them anywhere. No agent ever posts a comment starting with `Decision:`. Your spawn messages are the fixed templates at the bottom, with only their parameters filled in.

## Run directory

`<run_dir>` is `code-review-score/<branch>/` under the session's temp dir (`$CLAUDE_JOB_DIR/tmp` if set, otherwise a new `mktemp -d`). It holds:

| File | Written by | Contents |
|---|---|---|
| `run.json` | coordinator | `{ "repo_dir", "target", "base", "pr", "effort", "goal_source" }` |
| `round-<n>.json` | reviewer | The rubric's JSON block for round `n`. |
| `fix-<n>.json` | fixer | `{ "results": [{ "finding_id", "status", "note" }], "commit", "checks", "escalations": [{ "finding_id", "decision_needed" }] }` |

## Steps

0. **Grounding.** Find the source of the goal — don't read it for meaning, just confirm it exists:
   1. The PR for the target (`gh pr view`): its closing issues (`closingIssuesReferences`), then `Closes/Fixes/Resolves #N` in the body.
   2. If there's no linked issue, a PR description that states the goal and what "done" means.

   Record it as `goal_source` (`"#142"`, or `"PR #141 description"`). If neither exists, stop before reviewing: `needs_grounding`. Report what you checked and ask the caller to link an issue or describe the goal. Never derive the goal from the diff or commit messages.

   If the caller asks you to draft the issue, state acceptance criteria as outcomes ("prod can't boot local settings"), not mechanisms ("every error names the variable"), list anything extra under out of scope, and get the caller's approval before creating it.

1. **Set up the run.** Target is the argument (PR number or branch) if given, otherwise the current branch; base is the default branch. Effort is `high` unless the argument names another, and stays the same for every round. Write `run.json` with the Write tool, not a shell redirect. If the caller makes a ruling in chat, ask them to post it as a `Decision:` comment on the PR — don't post it for them.

2. **Review round** (max 2). Round 1's mode is `full`. Round 2's mode is `verify` if round 1 scored 4 or 5, otherwise `full`. Spawn a fresh subagent with the reviewer message. When it returns, read `round-<n>.json`.

3. **Stop check**, in order:
   1. Score is 5 and every `fix: true` finding is escalated (or there are none) → stop: `score_5`. A 5 with unescalated duplication goes on to a fix round, so duplication is fixed in the first fix round and that fix is reviewed.
   2. This was round 2 → stop: `max_rounds`.
   3. Every `fix: true` finding matches, by root cause, an escalation in an earlier `fix-<n>.json` → stop: `needs_decision`. The caller answers with `Decision:` comments, then re-runs.

   The loop always ends on a review, so the final score reflects the last fix.

4. **Fix round.** Spawn a separate fresh subagent with the fixer message, passing the ids of `fix: true` findings that aren't escalated. When it returns, read `fix-<n>.json`, then go back to step 2.

5. **Report** to the caller, built from the run files. Keep it brief: goal source, final score, stop reason, a summary table with one row per round (score, commit, what changed), open escalations with the decision needed, accepted findings, beyond-the-goal findings with their follow-ups, and pre-existing issues. Follow-ups are suggestions for the caller's review — never file issues for them or fix them. End with the PR's full URL. Fill in `rounds`, `stop_reason`, and `escalations` from the whole run in the last `round-<n>.json`, but don't include the JSON in the report.

## Spawn messages

Use these exactly. Add nothing.

Reviewer:

> Read and follow `~/.claude/skills/code-review-score/reviewer.md`. Run directory: `<run_dir>`. Round: `<n>`. Mode: `<mode>`.

Fixer:

> Read and follow `~/.claude/skills/code-review-score/fixer.md`. Run directory: `<run_dir>`. Round: `<n>`. Finding ids: `<ids>`.
