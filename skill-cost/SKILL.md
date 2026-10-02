---
name: skill-cost
description: Measure where a skill's tokens go across its recent runs — per agent, plus waste signals — and compare against a stored baseline. Use when asked how much a skill costs, where its tokens go, or whether a change to a skill cut its cost.
disable-model-invocation: true
---

# Skill cost

Args: `<skill> [N]`. N defaults to 3. Read-only — never edit the measured skill.

1. **Find runs.** Search `~/.claude/projects/*/*.jsonl` for main-session transcripts that invoked the skill (`Launching skill: <skill>`, or a user turn starting with `<skill>`). Take the N most recent. Each one's subagents, including nested ones like `/code-review`'s, are in `<session>/subagents/agent-*.jsonl`.

2. **End of run.** For each run, find the timestamp of the main thread's last assistant turn that belongs to the skill (its final report). Turns after that are the user's follow-ups, not the skill.

3. **Count.** Run `python3 ~/.claude/skills/skill-cost/count.py <session.jsonl> <end timestamp>` for each run. It sums input, cache-creation, cache-read, and output tokens per transcript, counting each message id once (streaming repeats them). Subagent output counts run low; cache reads dominate anyway, so say so rather than correct for it. Label each transcript by its role in the skill (from its first prompt, which the script prints). Inline skills the main thread invoked (e.g. `handle-pr-review`) don't get their own transcript — split the main thread at the turn that launched them.

4. **Waste signals.** Grep the transcripts for each of these, and report counts with an example:
   - Refused tool calls and the retry that followed.
   - The same fetch repeated (`gh issue view`, `gh pr view`, the same file read).
   - Check runs (tests, lint, typecheck) per commit SHA — the same SHA checked more than once.
   - Tool results over 10k chars, especially ones that repeat (polling, watch loops, full diffs).
   - Subagent replies that repeat a file the subagent also wrote, compared by size.

5. **Compare.** If `~/.claude/skills/skill-cost/baselines/<skill>.md` exists, compare totals, per-agent shares, and waste signals against it. Note what changed in the skill since the baseline (`git log` in `~/.claude/skills`), and outcome metrics the baseline records (e.g. scores), so a cut that cost quality shows up.

6. **Report.** Numbers first: a table of agents × runs (tokens, % of run), the waste signals, then the comparison. Under 500 words. Offer to update the baseline; only write it if the caller agrees.
