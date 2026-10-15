| Config | Bot login | Trigger comment | Done when |
| --- | --- | --- | --- |
| `.coderabbit.yaml` | `coderabbitai[bot]` | `@coderabbitai review` | The bot's reply to the trigger comment says `Review finished`. |
| `.greptile/` | `greptile-apps[bot]` | `@greptileai` | `Unknown` |

The top-most row whose config exists in the repo root wins. To switch a repo's bot, add that bot's config file.
