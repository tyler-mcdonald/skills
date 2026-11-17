---
name: refine-diff
description: Run a set of checks on a diff and apply the findings worth making. Use when asked to refine a diff or a PR.
---

# Refine Diff

Checks only report. You decide on every finding and make the changes.

## Checks

- `review-clean-code`
- `review-component-state`
- `review-duplication`
- `review-library-usage`

To add a check, add a skill that reports findings with citations, and list it here.

## Steps

1. Fetch `origin`, then set the base and goal:
   - PR argument: work on its branch, in the worktree that already has it, else invoke `setup-worktree` and run `gh pr checkout <pr>`. The base is the PR's base branch. The goal is its linked issue (`closingIssuesReferences`), else its description.
   - Otherwise: the base is the argument, else the default branch. The goal is the issue or request you were given.
2. Read the goal, including an issue's comments.
3. Invoke each check with the base.
4. For each finding, check its citation and decide: apply it, or reject it with a reason. Reject findings that conflict with the goal or with another finding.
5. If you applied any, run lint, typecheck, and only the tests that cover the changed files (CI runs the full suite); fix failures you caused, commit, and `git push -u origin HEAD` (never force-push).
6. Reply with the commit you pushed, or "no changes", then one line per finding: applied, or rejected and why.
