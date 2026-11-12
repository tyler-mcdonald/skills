---
name: set-issue-status
description: Set a GitHub issue's Status on every project board it's in (e.g. "In review"). Use when asked to move an issue to a status or lane.
---

# Set Issue Status

Run `<skill dir>/set_issue_status.py <issue url> "<status>"` (`<skill dir>` is this skill's base directory) and relay what it prints.

It sets the status on every board that already has a Status option with that name, ignoring case, and skips the rest. Never create a board, add a Status option, or rename one.
