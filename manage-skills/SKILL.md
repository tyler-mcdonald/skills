---
name: manage-skills
description: Add, edit, or remove a skill. Use whenever the user wants to add, edit, rename, or remove a skill.
---

## Steps

1. Setup
   - From `~/Projects/skills`, invoke `setup-worktree` with a short title for the change (e.g. "Add update-skill").
   - Stay in that worktree for every step.

2. Change
   - Each skill lives in `<skill-name>/SKILL.md` with `name` and `description` frontmatter.
   - Follow the Writing rules, and match the style of the existing skills.
   - Use the simplest solution that works (e.g. don't default to a script when a setting alone will do).
   - Renaming a skill: search the other skills for references to the old name and update them too, so names don't drift out of sync.

3. Review
   - Spawn a fresh Haiku subagent with only the changed skill files and the repo's other skills, for one review pass on the changed lines. Include the Review checklist in its prompt.
   - Apply its findings, except any that drop something the user asked for.

4. Ship
   - Commit with a short, single-line message.
   - `git push -u origin HEAD`, then open the PR into main with the `open-pr` skill.
   - Return the PR URL.

## Writing rules

- Description: a short, high-level summary of what the skill is for, then when to use it. It's what agents read to pick the skill, so leave the steps and internals to the body.
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

## Review checklist

- Description: it says what the skill is for and when to use it, matches what the body does, doesn't name the skills that call it, and doesn't list its arguments, which go in `argument-hint`.
- Scope: cut anything added that the user didn't ask for.
- Concision: the skill must stay very concise, simple, and direct. Cut lines an agent would get right without, and shorten verbose wording.
- Existing skills: steps that redo another skill, to replace with invoking it.
- Plain wording: unnecessary direction to remove, and LLM-sounding wording to make simple and direct. A human should be able to follow what the skill does.
- Markdown: follows the Markdown rules under Writing rules, and is simpler, more readable, and better organized.
- Step references: refer to steps by name (e.g. "go to Report"), not number.
