---
name: plan-issue
description: Plan a GitHub issue and write the plan into it, without implementing it. Use when an issue needs planning (asked for, labeled unplanned, or no requirements), to put a plan agreed in chat into an issue, or to split an issue into sub-issues.
---

# Plan Issue

Takes a GitHub issue to an agreed plan recorded on the issue. A separate agent implements it from there.

1. Get the issue
   - If there is one, fetch it (`gh issue view <ref> --json number,title,body,comments`) and confirm its number and title with the user in one line.
   - If there isn't, **Write it** creates it.

2. Agree on a plan

   If the plan was already agreed in this chat, skip to **Scope it**. Otherwise:

   1. If there's an issue, set its Status to "Planning" with the `set-issue-status` skill.
   2. Explore the repo's local checkout, read-only (no worktree, no file changes), enough to see how this area is built: relevant files, patterns, conventions.
   3. Draft a concrete plan and present it.
   4. In parallel, spawn two subagents given the plan and the repo path:
      - Sonnet: raises specific questions on these concerns, engineering quality only, not scope, and only where a concern applies; no questions is a valid answer:
        - Scalability
        - Maintainability
        - Simplicity of design
      - Haiku, fresh, given only the plan and the repo path: reads the code and systems the plan touches, then raises questions about the plan's assumptions and gaps that would change the requirements or need the user's decision. Skip implementation details.
   5. Answer each question: look up facts yourself and ask the user only about decisions. Revise the plan or push back with reasoning. If the Haiku subagent's questions are still open, send them back to it for another round.
   6. Present the final plan and wait for the user's explicit approval.

3. Scope it
   1. Split the plan into one issue per part that can ship on its own (e.g. a backend config change and a frontend behavior change). Keep parts together only when one can't work without the other.
   2. Present your recommendation for the user's approval.

4. Write it
   - Write the plan into the issue with the `write-issue` skill. When splitting, move the requirements into the sub-issues and leave the parent with only the overview and shared context.

5. Mark it ready
   - Set every issue written in **Write it**, including new sub-issues, to "Ready to work" with the `set-issue-status` skill.

6. Report and stop
   - Give the issue URL.
   - Don't implement, branch, commit, or open a PR, even if the plan is small.

If a `gh` command fails, show the exact error instead of retrying blindly or guessing a workaround.
