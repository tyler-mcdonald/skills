---
name: write-issue
description: How to write a GitHub issue's title and body. Use for issue text; to plan, split, or record an agreed plan, use `plan-issue`.
---

# Write Issue

Write it for the agent that implements it, in plain language a person can read. Keep it short.

## Title

- Use a plain title, such as "Add dark mode".

## Body

Use these parts, in this order, separated by a blank line:

1. Overview: one or two sentences that show at a glance what the issue is for. Start with why, the problem or goal, then optionally what changes. Don't repeat a requirement.
2. `Requirements:` bullets for the behavioral requirements. Each bullet is one short requirement that can be checked pass or fail; split a bullet that holds two. Say what, not how. No code, API names, or file paths unless the user chose them.
3. `Out of scope:` (optional) bullets for real boundaries only: things an agent would plausibly do otherwise, and exclusions the user chose.
4. `Notes:` (optional) bullets for anything supporting, such as context, a mocks link, screenshots, docs or tests to update, and manual rollout steps.

Leave out a section with nothing in it. Use only these plain-text labels, no headings. Leave out background, alternatives considered, file-by-file plans, and filler.

## Steps

1. Review the draft
   - Spawn a fresh Haiku subagent with the draft.
   - Ask it to flag each problem with a suggested fix, treating details the user chose as requirements:
     - The first sentence gives the why and doesn't repeat a requirement.
     - Each requirement is one behavior that can be checked pass or fail.
     - Requirements hold only behavior, with no chores, context, or implementation details the user didn't choose.
     - Out of scope holds only real boundaries, and keeps every exclusion the user chose.
     - Chores, context, and links are under Notes.
     - No vague words, such as "fast" or "clean", without a measure.
     - No empty sections, and no other headings or sections.
   - Apply them.

2. Post it
   - For an existing issue, use `gh issue edit <ref> --body-file <file>`, keeping any existing body text above yours.
   - Otherwise, `gh issue create`.
   - Add a new issue to the project board with `gh project item-add 1 --owner tyler-mcdonald --url <issue url>`.

## Example

```markdown
The bright UI is hard on the eyes at night. Add a dark mode using Mantine's built-in color schemes.

Requirements:
- Default to the system setting.
- A sun/moon icon button in the header, next to Log out, switches between light and dark.
- The choice is remembered in the browser.
- The page doesn't flash light on load.
- The login subtitle meets WCAG AA contrast on dark.

Out of scope:
- A custom theme.
- An icon library.

Notes:
- Mocks: <link>
```
