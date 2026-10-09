---
name: trigger-bot-review
description: Push a PR's branch, trigger the repo's review bot on it, and mark it ready for review. Use when asked to trigger a bot review on a PR.
---

# Trigger Bot Review

1. `git push` (never force-push).
2. Pick the review bot by the config file in the repo root, using the table in `review-bots.md`. If there is one, `gh pr comment <pr> --body "<trigger comment>"` — `watch-prs` handles the bot's threads from here.
3. `gh pr ready <pr>`.
4. Reply with the review bot triggered, or that there was none.
