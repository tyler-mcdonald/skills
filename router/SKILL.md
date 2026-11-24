---
name: router
description: Route a new chat's first message to the right workflow. Use on the first message of every chat.
---

## Routes

[Resolve the repo](#resolve-the-repo), pick one route from the first message, say it in one line, then follow it:

- **Plan an issue** — a new bug report, bug fix, idea, or proposal, or a request to plan an issue: invoke `plan-issue`.
- **Implement an issue** — the change has a GitHub issue: invoke `orchestrator`.
- **Run a PR** — "run" with a PR URL: invoke `run` to run the app locally from that PR's branch.
- **Dependency update** — bump a dependency or fix an audit (pip-audit, npm audit, an advisory): invoke `manage-dependencies`.
- **Direct change** — a code change with no GitHub issue: follow [Direct change](#direct-change).
- **Question or chat** — a one-off question: just answer.

## Resolve the repo

If the prompt requires a repo, take the first that matches:

1. An issue or PR URL, or `owner/repo#N`, in the message.
2. A project named in the message that matches a local checkout of a repo.
3. The current directory's repo.

If none match, ask which repo. Work from that repo's local checkout.

## Direct change

1. Setup
   - Invoke `setup-worktree` with a short title for the change.
   - Stay in that worktree for every step.

2. Change
   - Make the change.
   - Run the project's checks (tests, lint).

3. Ship
   - Commit and `git push -u origin HEAD`.
   - Open the PR with the `open-pr` skill.
   - Return the PR URL.
