# AI Agent Skills

AI agent skills to plan, build, review, and ship code.

## Orchestrator

[Orchestrator](operator/SKILL.md) coordinates a team of agents to take a GitHub issue to a review-ready PR.

Used to build [Cardcase](https://github.com/tyler-mcdonald/cardcase), a live full-stack app.

```mermaid
flowchart LR
    A[Issue] --> B[Dev agent]
    B --> C[Refactor agent]
    C --> D{Review + fix<br/>loop}
    D -- fails --> X[Draft PR +<br/>notify user]
    D -- passes --> E[QA<br/>optional]
    E --> F[External AI review<br/>CodeRabbit]
    F --> G[Ready for<br/>human review]
```

- **Autonomous.** Runs from issue to PR and only stops when it needs a person.
- **Pre-reviewed.** Separate agents review and fix the code against the issue's goals, so PRs arrive already reviewed.
- **Safe by default.** Never merges or force-pushes. Every merge needs human approval.
- **Cost-controlled.** Caps review rounds and wait times to keep token use and runtime predictable.

## Setup

```sh
git clone https://github.com/tyler-mcdonald/skills.git ~/.claude/skills
```

Requires the `gh` CLI. Bot review in CI uses [agent-workflows](https://github.com/tyler-mcdonald/agent-workflows).
