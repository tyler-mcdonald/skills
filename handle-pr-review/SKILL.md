---
name: handle-pr-review
description: Address and reply to PR review comments, from people or review bots. Use when asked to handle, address, fix, or respond to a PR review, its comments, or its findings.
context: fork
---

1. Find the PR: use the argument (number or URL) if given, otherwise the current branch's PR (`gh pr view`). Note its number `<n>` and `<owner>/<repo>` from its URL. Pull the branch so the code matches what was reviewed.

2. Fetch the threads that need handling — unresolved, and not last replied to by Claude:

   ```sh
   ~/.claude/skills/handle-pr-review/fetch-threads.sh <n> <owner>/<repo>
   ```

   Don't fetch the full comment list — this is the whole input. If the user names a reviewer (e.g. a review bot), only handle that reviewer's threads.

   If the last comment is the user's own, judge from context whether it's an instruction to you or a reply to the reviewer.

3. For each thread, check the comment against the actual code, then either:
   - make the change, or
   - answer the question or push back with the reason, leaving the code alone.

   A follow-up may or may not need a code change. If you're unsure what the reviewer wants, reply with a clarifying question and leave the code alone.

4. Commit by concern as you go: generally one commit per review change. Don't lump everything into a single commit. Don't run checks between commits. Once all changes are in, run tests, typecheck, and lint once, fix anything failing, then push. If you made no commits, skip the checks and the push — the code is unchanged.

   After pushing, if the PR title no longer describes the diff, update it with `gh pr edit <n> --title`, following the `open-pr` skill's title rules. Leave a title that's still accurate alone.

5. Reply in every thread you handle, briefly, even when nothing needs doing, so it isn't handled again. When a code change was made, end the reply with the commit that made it, e.g. `(abc1234)`.

   ```sh
   gh api repos/<owner>/<repo>/pulls/<n>/comments/<comment-id>/replies -f body="..."
   ```

   `<comment-id>` is the `id` of the thread's first comment. Don't resolve the threads.

6. Report back in a few lines the user can scan in seconds — the thread replies hold the detail:

   ```
   <file>:<line> — changed (abc1234) | answered | pushed back — <≤10 words on what>
   ```

   One line per thread, a `title — "<old>" → "<new>"` line if you retitled, then a line only for what needs the user: an open question, a failing check, a conflict you resolved by judgment. Nothing else — don't restate the comments, itemize what a commit removed, confirm what you didn't do, or add a summary.
