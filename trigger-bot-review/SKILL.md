---
name: trigger-bot-review
description: Trigger the repo's review bot on a pushed PR. Use when asked to trigger a bot review on a PR.
context: fork
model: haiku
background: false
---

# Trigger Bot Review

1. Pick the review bot from the table in `~/.claude/skills/trigger-bot-review/review-bots.md`. If no row matches, reply `none` and stop.
2. `gh pr comment <pr> --body "<trigger comment>"`.
3. Reply with the bot login you triggered.

Don't wait for the review, don't mark the PR ready, and don't handle the bot's threads.
