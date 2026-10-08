---
name: router
description: Route a new chat's first message to the right workflow. Use on the first message of every chat.
---

# Router

Pick one route from the first message, say it in one line, then follow it:

- **Plan an issue** — invoke `plan-issue`.
- **Implement an issue** — invoke `operator`.
- **Question or chat** — just answer.

## Resolve the repo

Only needed for the issue routes. Take the first that matches:

1. An issue URL or `owner/repo#N` in the message.
2. A project named in the message that matches a local checkout of a repo.
3. The current directory's repo.

If none match, ask which repo. Work from that repo's local checkout.
