---
name: open-pr
description: Open a pull request. Use whenever opening a PR.
---

# Open PR

- Always open PRs as drafts (`gh pr create --draft`). Never mark a PR as ready for review.
- If the branch is stacked on another PR's branch, pass `--base <that branch>`.
- After this skill's rules, apply any PR conventions in the repo's CLAUDE.md (e.g. allowed scopes). They take precedence where they're more specific.

## PR body

- The body is one sentence, two at most: what changes and why. No headings, lists, or test plan unless the user explicitly asks.
- Omit how it works, what stays the same, edge cases, housekeeping like updated references or docs, and file, function, command, tool, model, or library names unless the change is about them.
- If the PR resolves an issue, end the body with `Closes #<issue number>` on its own line.

## PR title

PRs are squash-merged into a single commit, so the title follows Conventional Commits: `type(scope): summary`, with `!` after the type/scope for breaking changes. The scope is optional. Keep titles to 50 characters or fewer. For the types, see the `conventional-commits` skill.

Write the summary from what the branch actually changed, at a very high level. Use the linked issue as a reference point for intent, but don't copy its title — the squashed commit should record what landed, which can differ from how the issue was framed.

Judge what changed from the diff against the base branch (`git diff <base>...HEAD`), not the commit log. Commits from already squash-merged branches can still appear in the log even though their changes have already landed.
