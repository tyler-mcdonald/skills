---
name: write-issue
description: Write a short, plain GitHub issue body. Use whenever creating a GitHub issue or writing a plan into one.
---

# Write Issue

Write for a person skimming it, and keep it short. Use three parts, in this order:

1. **Overview:** one or two sentences on what this is.
2. **Requirements:** bullets for the main requirements and the decisions made. One line each.
3. **Notes (optional):** anything supporting, such as context, a mocks link, or screenshots. Leave it out if there's nothing to add.

Leave out headings, background, alternatives considered, file-by-file plans, and filler. Use a plain title, such as "Add dark mode".

Example:

```markdown
Add a dark mode using Mantine's built-in color schemes. No custom theme.

- Default to the system setting (`defaultColorScheme="auto"`).
- Add a sun/moon icon button in the header, next to Log out, that switches between light and dark. Mantine remembers the choice in the browser.
- Use inline SVG icons. Don't add an icon library.
- Add Mantine's color scheme script to `index.html` so the page doesn't flash light on load.
- Change the login subtitle from `c="gray.7"` to `c="dimmed"` so it's readable on dark.

Everything else already uses Mantine's color variables and should work as is.

Mocks: <link>
```
