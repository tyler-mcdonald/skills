---
name: router
description: Route a new chat's first message to the right workflow. Use on the first message of every chat.
---

# Router

Pick one route from the first message, say it in one line, then follow it:

- **Plan an issue** — invoke `plan-issue`.
- **Implement an issue** — the change has a GitHub issue: invoke `operator`.
- **Dependency update** — bump a dependency or fix an audit (pip-audit, npm audit, an advisory): invoke `manage-dependencies`.
- **Direct change** — a code change with no GitHub issue: follow [Direct change](#direct-change).
- **Question or chat** — just answer.

## Resolve the repo

Only needed for the issue and direct change routes. Take the first that matches:

1. An issue URL or `owner/repo#N` in the message.
2. A project named in the message that matches a local checkout of a repo.
3. The current directory's repo.

If none match, ask which repo. Work from that repo's local checkout.

## Direct change

No operator: no simplify, review cycle, QA, or bot review.

1. Invoke `setup-worktree` with a short title for the change. Stay in that worktree for every step.
2. Make the change and run the project's checks (tests, lint).
3. Commit, `git push -u origin HEAD`, and open the PR with the `open-pr` skill.
4. Return the PR URL.
