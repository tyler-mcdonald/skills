---
name: handle-pr-review
description: Address and reply to PR review comments, from people or bots like Greptile. Use when asked to handle, address, fix, or respond to a PR review, its comments, or its findings.
---

1. Find the PR: use the argument if given, otherwise the current branch's PR (`gh pr view`). Pull the branch so the code matches what was reviewed.

2. Fetch the threads that need handling — unresolved, and not last replied to by Claude:

   ```sh
   ~/.claude/skills/handle-pr-review/fetch-threads.sh <n>
   ```

   Don't fetch the full comment list — this is the whole input. If the user names a reviewer (e.g. Greptile), only handle that reviewer's threads.

   If the last comment is the user's own (posted by hand, without the footer), judge from context whether it's an instruction to you or a reply to the reviewer; ask the user if unsure.

3. For each thread, check the comment against the actual code, then either:
   - make the change, or
   - answer the question or push back with the reason, leaving the code alone.

   A follow-up may or may not need a code change. If you're unsure what the reviewer wants, ask the user.

4. Commit by concern as you go: generally one commit per review change. Don't lump everything into a single commit. Don't run checks between commits. Once all changes are in, run tests, typecheck, and lint once, fix anything failing, then push. If you made no commits, skip the checks and the push — the code is unchanged.

5. Reply in each thread, briefly. When a code change was made, end the reply with the commit that made it, e.g. `(abc1234)`. Every reply ends with this footer:

   ```
   🤖 Posted by Claude Code
   ```

   ```sh
   gh api repos/{owner}/{repo}/pulls/<n>/comments/<comment-id>/replies -f body="..."
   ```

   `<comment-id>` is the `id` of the thread's first comment. Don't resolve the threads. The replies are the report — no need to summarize them back to the user.
