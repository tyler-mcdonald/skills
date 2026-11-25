---
name: handle-pr-review
description: Address and reply to PR review comments, from people or review bots. Use when asked to handle, address, fix, or respond to a PR review, its comments, or its findings.
context: fork
---

## Steps

1. Find the PR
   - Use the argument (number or URL) if given, otherwise the current branch's PR (`gh pr view`).
   - Note its number `<n>` and `<owner>/<repo>` from its URL.
   - Pull the branch.
   - Invoke `sync-branch`. Keep going if it reports `Needs Decision`.

2. Fetch threads
   - Fetch the unresolved threads not last replied to by Claude. This is the whole input, so don't fetch the full comment list.

     ```sh
     ~/.claude/skills/handle-pr-review/fetch_threads.py <n> <owner>/<repo>
     ```

   - If the user names a reviewer (e.g. a review bot), only handle that reviewer's threads.
   - If a PR comment or review summary triggered this run, handle it too: do what it asks, or if it only mentions you, handle the threads. A triggering review thread comment is already in the fetched threads.
   - If the last comment is the user's own, judge from context whether it's an instruction to you or a reply to the reviewer.

3. Handle threads
   - Check each comment against the actual code.
   - Make the change, or answer the question or push back with the reason, leaving the code alone.
   - If you're unsure what the reviewer wants, reply with a clarifying question and leave the code alone.

4. Commit and push
   - Commit by concern as you go, generally one commit per review change.
   - Push once all changes are in. Skip the push if you made no commits.
   - After pushing, if the PR title no longer describes the diff, update it with `gh pr edit <n> --title`, following the `open-pr` skill's title rules. Leave an accurate title alone.

5. Reply
   - Reply briefly in every thread you handled, whether or not you changed code.
   - When you changed code, end the reply with the commit, e.g. `(abc1234)`.
   - `<comment-id>` is the `id` of the thread's first comment.

     ```sh
     gh api repos/<owner>/<repo>/pulls/<n>/comments/<comment-id>/replies -f body="..."
     ```

   - Don't resolve the threads.

6. Report
   - Keep it to a few lines the user can scan in seconds. The thread replies hold the detail.
   - One line per thread:

     ```text
     <file>:<line> — changed (abc1234) | answered | pushed back — <≤10 words on what>
     ```

   - A `title — "<old>" → "<new>"` line if you retitled.
   - A line only for what needs the user: an open question, a conflict you resolved by judgment, or a `Needs Decision` from the sync.
   - Nothing else: don't restate the comments, itemize what a commit removed, confirm what you didn't do, or add a summary.
