---
name: handle-pr-review
description: Address and reply to PR review comments, from people or bots like Greptile. Use when asked to handle, address, fix, or respond to a PR review, its comments, or its findings.
---

1. Find the PR: use the argument if given, otherwise the current branch's PR (`gh pr view`). Pull the branch so the code matches what was reviewed.

2. Fetch the review comments:

   ```sh
   gh api repos/{owner}/{repo}/pulls/<n>/comments --paginate
   ```

   If the user names a reviewer (e.g. Greptile), only handle that reviewer's comments.

   Group them into threads (`in_reply_to_id`). A thread needs handling if it has no reply from you yet, or if the reviewer replied after your last reply (a follow-up). Skip threads where the last word is yours.

3. For each thread, check the comment against the actual code, then either:
   - make the change, or
   - answer the question or push back with the reason, leaving the code alone.

   A follow-up may or may not need a code change. If you're unsure what the reviewer wants, ask the user.

4. Commit by concern as you go: generally one commit per review change. Don't lump everything into a single commit. Don't run checks between commits. Once all changes are in, run tests, typecheck, and lint once, fix anything failing, then push.

5. Reply in each thread, briefly. When a code change was made, end the reply with the commit that made it, e.g. `(abc1234)`. Every reply ends with this footer:

   ```
   🤖 Posted by Claude Code
   ```

   ```sh
   gh api repos/{owner}/{repo}/pulls/<n>/comments/<comment-id>/replies -f body="..."
   ```

   Don't resolve the threads. The replies are the report — no need to summarize them back to the user.
