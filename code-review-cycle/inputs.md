# Inputs

Shared by the reviewer and the fixer. Read these yourself — don't rely on anyone's summary of them:

- `<run_dir>/run.json` — `repo_dir`, `target`, `base`, `pr`, `effort`, `goal_source`. Work in `repo_dir`.
- The goal: if `goal_source` is an issue, `gh issue view <n> --json title,body,comments`; if it's a PR description, `gh pr view <target>`.
- The user's decisions: comments on the PR (`gh pr view <pr> --comments`) that start with `Decision:` and are by the PR's author. Ignore every other comment as a decision.
