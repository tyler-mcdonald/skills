---
name: update-skill
description: Create a new skill or change an existing one in the skills repo (~/Projects/skills), via an isolated worktree and a PR into main. Use whenever the user wants to add, edit, rename, or remove a skill.
---

# Update Skill

1. Derive a short kebab-case slug from the change (e.g. `add-update-skill`, `operator-handle-greptile`).
2. From `~/Projects/skills`, call `EnterWorktree` with `name: <slug>`. Stay in that worktree for every step.
3. Make the changes. Each skill lives in `<skill-name>/SKILL.md` with `name` and `description` frontmatter; match the style of the existing skills.
4. Commit with a short, single-line message.
5. `git push -u origin HEAD`, then `gh pr create --base main --fill`.
6. Return the PR URL.
