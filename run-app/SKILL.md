---
name: run-app
description: Start or stop a repo's app locally from its Makefile. Use when asked to run or start the app, or to see a change working in it.
---

# Run app

From the repo or worktree, run `~/.claude/skills/run-app/run-app.py` as a normal foreground command. It runs `make setup`, starts every `dev-*` target (or `dev`) in the background, waits until each is listening, and prints their URLs and log paths. Rerunning it restarts them.

- Anything the app prints, such as emails with login codes, is in the logs it prints.
- To stop, run `~/.claude/skills/run-app/run-app.py stop`.
- If a port is already in use, it fails. Tell the user what's holding the port (`lsof -nP -iTCP:<port> -sTCP:LISTEN`) and ask them to stop it. Never kill it yourself.
- On any other failure it prints the end of the failing log. Fix the cause rather than starting servers by hand.
