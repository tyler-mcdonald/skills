---
name: trigger-bot-review
description: Trigger the repo's review bot on a pushed PR and mark it ready for review. Use when asked to trigger a bot review on a PR.
---

# Trigger Bot Review

1. Pick the review bot by the config file in the repo root, using the table in `review-bots.md`. If there is one, `gh pr comment <pr> --body "<trigger comment>"` — `watch-prs` handles the bot's threads from here.
2. `gh pr ready <pr>`.
3. Reply with the review bot triggered, or that there was none.
