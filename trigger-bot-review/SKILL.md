---
name: trigger-bot-review
description: Trigger the repo's review bot on a pushed PR and wait for its review to finish. Use when asked to trigger a bot review on a PR.
---

# Trigger Bot Review

1. Pick the review bot from the table in `review-bots.md`. If no row matches, reply `none` and stop — nothing is triggered or waited on.
2. `gh pr comment <pr> --body "<trigger comment>"`.
3. If that row's "Done when" is `Unknown`, reply `timed out` and stop. Otherwise wait for the signal, checking once a minute for up to 15 minutes. Only count what the bot posted or edited after the trigger comment.
4. Reply with one word: `reviewed`, or `timed out` if the signal never came.

Don't mark the PR ready and don't handle the bot's threads.
