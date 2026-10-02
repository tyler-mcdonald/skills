---
name: start-issue
description: Start end-to-end work on a GitHub issue — creates an isolated git worktree named after the issue, plans the change and sharpens it via grilling, implements it, then opens a draft PR linked to the issue once the work is done. Use when the user gives a GitHub issue (number, URL, or "owner/repo#N") and asks to start, pick up, tackle, or work on it.
---

# Start Issue

Takes a GitHub issue from "not started" to a draft PR, end to end.

## Phase 1: Set up

1. Fetch the issue (`gh issue view <ref> --json number,title`) and confirm it with the user in one line (number + title) — a cheap sanity check against grabbing the wrong issue.
2. Invoke `setup-issue` with the issue reference.

## Phase 2: Plan and implement

Do this directly rather than delegating to a planning/implementation skill.

1. Explore the codebase enough to understand how this issue's area is currently built (relevant files, existing patterns, conventions) and draft a concrete implementation plan.
2. Present the drafted plan, then invoke `grilling` on it.
3. Incorporate what surfaces — revise the plan, or push back with reasoning, rather than ignoring findings. Then confirm the (possibly revised) plan with the user and wait for explicit approval before writing any code. Do not skip or short-circuit this.
4. Implement the approved plan, then do a quality-review pass over the diff before moving to Phase 3.

## Phase 3: Commit, push, open the PR

Only after implementation + quality-review are done and the user is satisfied with the result — do not open the PR earlier, and do not use an empty/placeholder commit just to open it sooner:

1. Stage and commit the changes with a short, single-line descriptive commit message (no co-author trailer — follow this user's global git conventions).
2. `git push -u origin <branch>`
3. Open the PR with the `open-pr` skill, linked to the issue.
4. Report the PR URL back to the user and stop. Do not merge, or take any further action — that's the user's call.

## Notes

- Stay in the worktree once finished; the user will likely keep iterating there. Only exit it (`ExitWorktree`) if they explicitly ask.
- If any `gh` command fails (auth, permissions, rate limit, no default branch detected), surface the exact error instead of retrying blindly or guessing a workaround.
