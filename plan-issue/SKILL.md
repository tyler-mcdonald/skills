---
name: plan-issue
description: Plan a GitHub issue and write the plan into it, without implementing it. Use when an issue needs planning (asked for, labeled unplanned, or no requirements), or to put a plan agreed in chat into an issue.
---

# Plan Issue

Takes a GitHub issue to an agreed plan recorded on the issue. A separate agent implements it from there.

1. **Get the issue.** If there is one, fetch it (`gh issue view <ref> --json number,title,body,comments`) and confirm its number and title with the user in one line. If there isn't, **Write it** creates it.
2. **Agree on a plan.** If the plan was already agreed in this chat, skip to **Stress-test**. Otherwise:
   1. If there's an issue, set its Status to "Planning" with the `set-issue-status` skill.
   2. Explore the repo's local checkout, read-only (no worktree, no file changes), enough to see how this area is built: relevant files, patterns, conventions.
   3. Draft a concrete plan, present it, and invoke `grilling` on it.
   4. Address each finding: revise the plan or push back with reasoning. Then present the final plan and wait for the user's explicit approval.
3. **Stress-test.**
   1. Spawn a fresh Haiku subagent with the plan and the code and systems it touches. Ask it to raise questions about the plan's assumptions and gaps. It doesn't need to suggest answers.
   2. Check its claims yourself, send it your answers for one more round, then update the plan.
   3. Look up facts yourself and ask the user only about decisions. If the plan changed in substance, get their approval again.
4. **Write it.** With the `write-issue` skill, write the plan into the issue, including every decision and any manual rollout steps (the implementer wasn't in the conversation):
   - Existing issue: `gh issue edit <ref> --body-file <file>`, keeping any existing body text above the plan.
   - No issue: `gh issue create`.
5. **Mark it ready.** Set every issue written in **Write it**, including new sub-issues, to "Ready to work" with the `set-issue-status` skill.
6. **Report and stop.** Give the issue URL. Don't implement, branch, commit, or open a PR, even if the plan is small.

If a `gh` command fails, show the exact error instead of retrying blindly or guessing a workaround.
