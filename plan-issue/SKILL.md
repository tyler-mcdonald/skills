---
name: plan-issue
description: Plan a GitHub issue and write the agreed plan into the issue, so a separate agent can implement it. Planning only — no code, branch, or PR. Use when the user gives a GitHub issue (number, URL, or "owner/repo#N") and asks to plan, start, pick up, or tackle it.
---

# Plan Issue

Takes a GitHub issue from "not started" to an agreed plan recorded on the issue. The issue is the hand-off: a separate agent (e.g. `operator`) implements it from there.

1. Fetch the issue (`gh issue view <ref> --json number,title,body,comments`) and confirm it with the user in one line (number + title) — a cheap sanity check against grabbing the wrong issue.
2. Explore the repo's local checkout, read-only, enough to understand how this issue's area is currently built (relevant files, existing patterns, conventions). No worktree, no file changes.
3. Draft a concrete implementation plan, present it, then invoke `grilling` on it.
4. Incorporate what surfaces — revise the plan, or push back with reasoning, rather than ignoring findings. Then confirm the final plan with the user and wait for explicit approval. Do not skip or short-circuit this.
5. Write the approved plan into the issue body (`gh issue edit <ref> --body-file <file>`), keeping any existing body text above it. Write it for an implementer who wasn't in the conversation — it's their source of truth: goal, constraints, what to build and where, expected behavior, tests, decisions with the alternatives rejected and why, and any manual rollout steps.
6. Report the issue URL and stop. Do not implement, branch, commit, or open a PR, even if the plan looks small — that's the implementing agent's job.

If any `gh` command fails (auth, permissions, rate limit), surface the exact error instead of retrying blindly or guessing a workaround.
