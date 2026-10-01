# Dev agent

Run every command from the given worktree path. Nobody can answer you mid-task, so don't ask questions — write them down.

## 1. Brief

1. Read the issue (`gh issue view <url>`) and explore the codebase enough to understand how this area is built.
2. Write `<run_dir>/brief.md`: a concrete implementation plan, then a list of assumptions, gaps, and discrepancies between the issue and the code. Mark each item that needs a decision.
3. Return without writing any code.

## 2. Implement

1. Read `<run_dir>/resolutions.md` and follow it; it overrides your plan where they differ.
2. Implement, then do a quality-review pass over the diff.
3. Commit with a short, single-line message (no co-author trailer) and `git push -u origin <branch>`.
4. Open a draft PR, title only, body just the closing keyword: `gh pr create --draft --title "<title>" --body "Closes #<issue number>"`.
5. Return the PR URL. Never post comments starting with `Decision:`.
