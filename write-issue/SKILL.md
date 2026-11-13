---
name: write-issue
description: How to write a GitHub issue's title and body. Use for issue text; to plan, split, or record an agreed plan, use `plan-issue`.
---

# Write Issue

Write it for the agent that implements it, in plain language a person can read. Keep it short. Use three parts, in this order:

1. **Overview:** one or two sentences on what this is.
2. **Requirements:** bullets for the main behavioral requirements, every decision the user made, and any manual rollout steps. One line each, saying what and why, not how. No code, API names, or file paths unless the user chose them.
3. **Notes (optional):** anything supporting, such as context, a mocks link, or screenshots. Leave it out if there's nothing to add.

Leave out headings, background, alternatives considered, file-by-file plans, and filler. Use a plain title, such as "Add dark mode".

Before posting, spawn a fresh Haiku subagent with the draft. Ask it to flag anything that isn't a behavioral requirement and suggest changes, treating details the user chose as requirements. Apply them.

To write into an existing issue, use `gh issue edit <ref> --body-file <file>`, keeping any existing body text above yours. Otherwise, `gh issue create`.

Example:

```markdown
Add a dark mode using Mantine's built-in color schemes. No custom theme.

- Default to the system setting.
- Add a sun/moon icon button in the header, next to Log out, that switches between light and dark. Remember the choice in the browser.
- Don't add an icon library.
- The page doesn't flash light on load.
- The login subtitle is readable on dark.

Mocks: <link>
```
