---
name: set-issue-status
description: Set a GitHub issue's Status on every project board it's in (e.g. "In review"). Use when asked to move an issue to a status or lane.
---

# Set Issue Status

Run:

```sh
~/.claude/skills/set-issue-status/set-issue-status.sh <issue url> "<status>"
```

The status must match the board's option name exactly. It prints one line per project it updated; no output means the issue isn't on a board with that status.
