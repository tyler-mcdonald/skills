---
name: skill-cost
description: Measure where a skill's tokens go across its recent runs — per agent, plus waste signals — and compare against a stored baseline. Use when asked how much a skill costs, where its tokens go, or whether a change to a skill cut its cost.
disable-model-invocation: true
---

# Skill cost

Args: `<skill> [N]`. N defaults to 3. Read-only — never edit the measured skill.

1. **Find runs.** Search `~/.claude/projects/*/*.jsonl` for main-session transcripts that invoked the skill (`Launching skill: <skill>`, or a user turn starting with `<skill>`). Take the N most recent. Each one's subagents, including nested ones like `/code-review`'s, are in `<session>/subagents/agent-*.jsonl`.

2. **End of run.** For each run, find the timestamp of the main thread's last assistant turn that belongs to the skill (its final report). Turns after that are the user's follow-ups, not the skill.

3. **Count.** Run `python3 ~/.claude/skills/skill-cost/count.py <session.jsonl> <end timestamp>` for each run. It prints input, cache-write, cache-read, and output tokens and turns per transcript as separate columns, counting each message id once (streaming repeats them). Keep the four token types separate — never add them into one total. Transcripts undercount cache reads and output, the same way every run, so compare runs with each other, not with a bill. The script labels known agents from their first prompt; label any `?` row by its role in the skill from the prompt it prints. Inline skills the main thread invoked (e.g. `handle-pr-review`) don't get their own transcript — split the main thread at the turn that launched them.

4. **Waste signals.** Grep the transcripts for each of these, and report counts with an example:
   - Refused tool calls and the retry that followed.
   - The same fetch repeated (`gh issue view`, `gh pr view`, the same file read).
   - Check runs (tests, lint, typecheck) per commit SHA — the same SHA checked more than once.
   - Tool results over 10k chars, especially ones that repeat (polling, watch loops, full diffs).
   - Subagent replies that repeat a file the subagent also wrote, compared by size.

5. **Compare.** If `~/.claude/skills/skill-cost/baselines/<skill>.md` exists, compare each agent's token types and turns, and the waste signals, against it. Runs vary with the size of the issue, so treat a change under ~30% in one agent as noise. Note what changed in the skill since the baseline (`git log` in `~/.claude/skills`), and outcome metrics the baseline records (e.g. scores), so a cut that cost quality shows up.

6. **Report.** Numbers first: a table of agents × runs (input, cache write, cache read, output, turns), the waste signals, then the comparison. Under 500 words. Offer to update the baseline; only write it if the caller agrees.
