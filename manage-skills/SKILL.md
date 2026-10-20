---
name: manage-skills
description: Create a new skill or change an existing one in the skills repo (~/Projects/skills). Use whenever the user wants to add, edit, rename, or remove a skill.
---

# Manage Skills

1. From `~/Projects/skills`, invoke `setup-worktree` with a short title for the change (e.g. "Add update-skill"). Stay in that worktree for every step.
2. Make the changes. Each skill lives in `<skill-name>/SKILL.md` with `name` and `description` frontmatter; match the style of the existing skills. Use the simplest solution that works (e.g. don't default to a script when a setting alone will do).
   - Description: a short, high-level summary of what the skill is for, then when to use it. It's what agents read to pick the skill, so leave the steps and internals to the body.
   - Renaming a skill: search the other skills for references to the old name and update them too, so names don't drift out of sync.
3. Commit with a short, single-line message.
4. `git push -u origin HEAD`, then open the PR into main with the `open-pr` skill.
5. Return the PR URL.
