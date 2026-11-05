# Inputs

Shared by the reviewer and the fixer. Read these yourself — don't rely on anyone's summary of them:

- `<run_dir>/run.json` — `repo_dir`, `target`, `base`, `pr`, `effort`, `goal_source`. Work in `repo_dir`.
- The goal: if `goal_source` is an issue, `gh issue view <n> --json title,body,comments`; if it's a PR description, `gh pr view <target>`.
- The user's decisions: the requirements and notes in the goal's body (the issue body, or the PR description when the goal has no issue). Never treat a comment as a decision.
