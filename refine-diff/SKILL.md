---
name: refine-diff
description: Run a set of checks on a diff and apply the findings worth making. Use when asked to refine a diff.
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

1. Fetch `origin`. Base is the argument, else the default branch.
2. Invoke each check with the base.
3. For each finding, check its citation and decide: apply it, or reject it with a reason. Reject findings that conflict with the goal (the issue or request you were given) or with another finding.
4. If you applied any, run the project's checks, fix failures you caused, commit, and `git push -u origin HEAD` (never force-push).
5. Reply with the commit you pushed, or "no changes", then one line per finding: applied, or rejected and why.
