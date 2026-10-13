| Config | Bot login | Trigger comment | Done when |
| --- | --- | --- | --- |
| `.coderabbit.yaml` | `coderabbitai[bot]` | `@coderabbitai review` | The bot's PR comment answering the trigger comment is edited to say `Review finished`. `Action not completed` there is not a review. A review from the bot is not the signal: a clean review posts none. |
| `.greptile/` | `greptile-apps[bot]` | `@greptileai` | Unverified — no signal known yet, so the wait times out. A review from the bot is not the signal: its out-of-credits notice arrives as one. |

The top-most row whose config exists in the repo root wins. To switch a repo's bot, add that bot's config file.
