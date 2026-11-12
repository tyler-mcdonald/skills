---
name: manage-skills
description: Add, edit, or remove a skill. Use whenever the user wants to add, edit, rename, or remove a skill.
---

# Manage Skills

1. From `~/Projects/skills`, invoke `setup-worktree` with a short title for the change (e.g. "Add update-skill"). Stay in that worktree for every step.
2. Make the changes. Each skill lives in `<skill-name>/SKILL.md` with `name` and `description` frontmatter; match the style of the existing skills. Use the simplest solution that works (e.g. don't default to a script when a setting alone will do).
   - Description: a short, high-level summary of what the skill is for, then when to use it. It's what agents read to pick the skill, so leave the steps and internals to the body.
   - Body: open with a `#` title of the skill name in Title Case (e.g. `# Setup Worktree`), the only `#` heading in the file.
   - Renaming a skill: search the other skills for references to the old name and update them too, so names don't drift out of sync.
   - Writing: prefer brevity, simplicity, and readability. Be very concise.
3. Spawn a fresh Sonnet subagent with only the changed skill files and the repo's other skills. Ask for:
   - Cuts: lines an agent would get right without, and wording to shorten.
   - Existing skills: steps that redo another skill, to replace with invoking it.
   - Plain wording: unnecessary direction to remove, and LLM-sounding wording to make simple and direct. A human should be able to follow what the skill does.

   Apply them, except any that drop something the user asked for.
4. Spawn a fresh Haiku subagent the same way, as a markdown expert, to suggest markdown changes for simplicity, readability, and organization. Apply them the same way.
5. Commit with a short, single-line message.
6. `git push -u origin HEAD`, then open the PR into main with the `open-pr` skill.
7. Return the PR URL.
