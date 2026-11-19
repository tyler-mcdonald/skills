---
name: plan-issue
description: Plan a GitHub issue and write the plan into it, without implementing it. Use when an issue needs planning (asked for, labeled unplanned, or no requirements), to put a plan agreed in chat into an issue, or to split an issue into sub-issues.
---

# Plan Issue

Takes a GitHub issue to an agreed plan recorded on the issue. A separate agent implements it from there.

## Steps

1. Get the issue
   - If there is one, fetch it (`gh issue view <ref> --json number,title,body,comments`) and confirm its number and title with the user in one line.
   - If there isn't, **Write it** creates it.

2. Agree on a plan

   If the plan was already agreed in this chat, skip to **Scope it**. Otherwise:

   1. If there's an issue, set its Status to "Planning" with the `set-issue-status` skill.
   2. Explore the repo's local checkout, read-only (no worktree, no file changes), enough to see how this area is built: relevant files, patterns, conventions.
   3. Draft a concrete plan and present it.
   4. Spawn the **Engineering review** subagent given the plan and the repo path.
   5. Answer each question: look up facts yourself and ask the user only about decisions. Revise the plan or push back with reasoning.
   6. Present the final plan and wait for the user's explicit approval.

3. Scope it
   1. Split the plan into one issue per part that can ship on its own (e.g. a backend config change and a frontend behavior change). Keep parts together only when one can't work without the other.
   2. Present your recommendation for the user's approval.

4. Write it
   - Write the plan into the issue with the `write-issue` skill. When splitting, move the requirements into the sub-issues and leave the parent with only the overview and shared context.

5. Stress-test
   1. Spawn a fresh **Stress test** subagent given only the issue references, including any sub-issues.
   2. Answer its questions: look up facts yourself and ask the user only about decisions. If your answers leave open questions, send them back for another round.
   3. If the plan changed, rewrite it in the issue with the `write-issue` skill, replacing the version from **Write it**. If it changed in substance, get the user's approval first.

6. Mark it ready
   - Set every issue written in **Write it**, including new sub-issues, to "Ready to work" with the `set-issue-status` skill.

7. Report and stop
   - Give the issue URL.
   - Don't implement, branch, commit, or open a PR, even if the plan is small.

## Subagents

- **Engineering review** (Sonnet): raises specific questions on these concerns, engineering quality only, not scope, and only where a concern applies; no questions is a valid answer:
  - Scalability
  - Maintainability
  - Simplicity of design
- **Stress test** (Haiku): reads the issues and the code and systems the plan touches, then raises questions about the plan's assumptions and gaps that would change the requirements or need the user's decision. Skip implementation details. It doesn't need to suggest answers.

## Rules

- If a `gh` command fails, show the exact error instead of retrying blindly or guessing a workaround.
