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
   - Scope: add only what the user asked for. No extra steps, lists, caveats, or constraints.
   - Markdown:
     - `##` headings with unique names.
     - Steps start with a short plain-text name on its own line (e.g. `3. Scope it`, not bold), with one action per sub-item under it.
     - Nested items use `-` bullets (or `1.` for ordered sub-steps), never lettered items like `a.`.
     - Lists over tables unless the data is two-dimensional.
     - Fenced code blocks with a language.
     - Backticks for commands, paths, and names.
     - No HTML.
3. Spawn a fresh Haiku subagent with only the changed skill files and the repo's other skills, for one review pass on the changed lines. Ask for:
   - Description: it says what the skill is for and when to use it, matches what the body does, and doesn't name the skills that call it.
   - Scope: cut anything added that the user didn't ask for.
   - Concision: the skill must stay very concise, simple, and direct. Cut lines an agent would get right without, and shorten verbose wording.
   - Existing skills: steps that redo another skill, to replace with invoking it.
   - Plain wording: unnecessary direction to remove, and LLM-sounding wording to make simple and direct. A human should be able to follow what the skill does.
   - Markdown: follows the Markdown rules above, and is simpler, more readable, and better organized.
   - Step references: refer to steps by name (e.g. "go to Report"), not number.

   Apply them, except any that drop something the user asked for.
4. Commit with a short, single-line message.
5. `git push -u origin HEAD`, then open the PR into main with the `open-pr` skill.
6. Return the PR URL.
