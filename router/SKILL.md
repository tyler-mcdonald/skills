---
name: router
description: Route a new chat's first message to the right workflow — answer a question, create a GitHub issue, or start work on an existing issue via start-issue or operator. Use on the first message of every chat.
---

# Router

Pick one route from the first message, say it in one line (route, repo, issue if any), then follow it. If the message fits none of them, or a route is already obvious from an explicit skill or slash command in the message, skip routing and just do what was asked.

## 1. Resolve the repo

Only needed for the issue routes. Take the first that matches:

1. An issue URL or `owner/repo#N` in the message.
2. A project named in the message that matches a local checkout of a repo.
3. The current directory's repo.

If none match, ask which repo. Work from that repo's local checkout.

## 2. Pick a route

- **Question** — the message asks something rather than requesting work on an issue. Just answer it.
- **New issue** — the message asks to create, file, or open an issue. Draft a title and body, confirm them with the user, then `gh issue create --repo <owner/repo>`.
- **Existing issue** — the message references an issue to work on. Invoke `start-issue`.

