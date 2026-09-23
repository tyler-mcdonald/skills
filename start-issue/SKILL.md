---
name: start-issue
description: Start end-to-end work on a GitHub issue — creates an isolated git worktree named after the issue, plans the change and sharpens it via grill-me, implements it, then opens a PR linked to the issue once the work is ready for review. Use when the user gives a GitHub issue (number, URL, or "owner/repo#N") and asks to start, pick up, tackle, or work on it.
---

# Start Issue

Takes a GitHub issue from "not started" to "PR ready for review," end to end.

## Phase 1: Resolve the issue

1. Parse the issue reference from the skill args (bare number, full URL, or `owner/repo#N`).
2. Fetch it: `gh issue view <ref> --json number,title,body,url`. If `gh` isn't authenticated or the issue doesn't exist, stop and tell the user rather than guessing.
3. Confirm the issue with the user in one line (number + title) before proceeding — a cheap sanity check against grabbing the wrong issue.

## Phase 2: Create and enter the worktree

1. Slugify the issue title into kebab-case: lowercase, collapse non-alphanumeric runs into a single hyphen, trim leading/trailing hyphens, truncate to 64 chars (EnterWorktree's limit).
   - Example: "Fix static asset serving" -> `fix-static-asset-serving`
2. Call `EnterWorktree` with `name: <slug>`. This branches from `origin/<default-branch>` and switches the session into it.
3. If a worktree with that name already exists, ask the user whether to resume it (`EnterWorktree` with `path`) rather than silently overwriting or picking a different name.

## Phase 3: Plan and implement

Do this directly rather than delegating to a planning/implementation skill.

1. Explore the codebase enough to understand how this issue's area is currently built (relevant files, existing patterns, conventions) and draft a concrete implementation plan.
2. `grill-me` cannot be invoked via the Skill tool — its frontmatter sets `disable-model-invocation: true`, reserved for the user typing `/grill-me` themselves. So: present the drafted plan, then explicitly ask the user to run `/grill-me` on it before you proceed (they may also choose to skip this step). Pause and wait for them to do so, or to tell you to move on.
3. If they run it, incorporate what surfaces — revise the plan, or push back with reasoning, rather than ignoring findings. Then confirm the (possibly revised) plan with the user and wait for explicit approval before writing any code. Do not skip or short-circuit this.
4. Implement the approved plan, then do a quality-review pass over the diff before moving to Phase 4.

## Phase 4: Commit, push, open the PR

Only after implementation + quality-review are done and the user is satisfied with the result — do not open the PR earlier, and do not use an empty/placeholder commit just to open it sooner:

1. Stage and commit the changes with a short, single-line descriptive commit message (no co-author trailer — follow this user's global git conventions).
2. `git push -u origin <branch>`
3. Open the PR, linked to the issue, with no generated description — title only, body is just the closing keyword:
   ```
   gh pr create --title "<title>" --body "Closes #<issue number>"
   ```
   This user has a standing preference against Claude writing PR summaries/descriptions — leave the body at just the linking keyword and let them fill in the rest if they want to.
4. Report the PR URL back to the user and stop. Do not merge, or take any further action — that's the user's call.

## Notes

- Stay in the worktree once finished; the user will likely keep iterating there. Only exit it (`ExitWorktree`) if they explicitly ask.
- If any `gh` command fails (auth, permissions, rate limit, no default branch detected), surface the exact error instead of retrying blindly or guessing a workaround.
