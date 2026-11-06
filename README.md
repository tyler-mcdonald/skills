# AI Agent Skills

Claude Code skills that plan, build, review, and ship code.

## Orchestrator

[Orchestrator](orchestrator/SKILL.md) takes a GitHub issue to a pull request that's ready for review. It hands each step to a separate agent.

Used to build [Cardcase](https://github.com/tyler-mcdonald/cardcase).

```mermaid
flowchart TD
    A([GitHub issue]) --> B["`**Dev agent**
Implements the issue`"]
    B --> C["`**Refactor agent**
Simplifies the diff`"]
    C --> D{"`**Review + fix loop**`"}
    D -->|scores at least 4/5| E["`**QA**
UI changes only`"]
    D -.->|fails| X([Draft PR + notify user])
    E --> F["`**External AI review**
CodeRabbit, Greptile, etc.`"]
    F --> G["`**CI agent**
Fixes issues flagged by external AI reviewer`"]
    G --> H([Ready for human review])
```

- Runs on its own from issue to PR, and stops only when it needs human input.
- Before the PR opens, a review agent scores the diff against the issue's requirements and a fix agent addresses what it finds.
- Never merges or force-pushes. A human approves every merge.
- Limits review rounds and wait times so cost and runtime stay predictable.

## Other skills

- [plan-issue](plan-issue/SKILL.md): writes an implementation plan into a GitHub issue
- [code-review-cycle](code-review-cycle/SKILL.md): reviews a branch and fixes findings until it's ready to merge
- [handle-pr-review](handle-pr-review/SKILL.md): addresses and replies to PR review comments

## Related

Automated bot review in CI uses [agent-workflows](https://github.com/tyler-mcdonald/agent-workflows).
