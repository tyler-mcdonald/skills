---
name: open-pr
description: Open a pull request with the user's PR conventions — draft, Conventional Commit title, minimal body. Use whenever opening a PR, yourself or as directed by the user, including as the final step of another workflow.
---

# Open PR

- Always open PRs as drafts (`gh pr create --draft`). Never mark a PR as ready for review.
- If the PR resolves an issue, the body is exactly `Closes #<issue number>`. Otherwise leave the body empty. Add nothing else unless the user explicitly asks.
- After these rules, apply any PR conventions in the repo's CLAUDE.md (e.g. allowed scopes). They take precedence where they're more specific.

## PR title

PRs are squash-merged into a single commit, so the title follows Conventional Commits: `type(scope): summary`, with `!` after the type/scope for breaking changes. The scope is optional. Keep titles to 50 characters or fewer. For the types, see the `conventional-commits` skill.

Write the summary from what the branch actually changed, at a very high level. Use the linked issue as a reference point for intent, but don't copy its title — the squashed commit should record what landed, which can differ from how the issue was framed.

Judge what changed from the diff against the base branch (`git diff <base>...HEAD`), not the commit log. Commits from already squash-merged branches can still appear in the log even though their changes have already landed.
