---
name: cite-source-docs
description: Find a link to the official source documentation for a pattern, piece of code, configuration, or directive that's been implemented, pointing to the exact section rather than a docs homepage. Use when the user asks where something came from in the docs, or wants a citation for a pattern/config/directive that was used.
---

Find the official source documentation backing the pattern, code, configuration, or directive in question.

First determine the subject: if the arguments name something specific, that is the subject — don't default to whatever was last discussed. Only fall back to the current conversation context when no specific subject is given (e.g. "on this").

Return a direct link to the specific page and section (not just the docs homepage) that documents the exact pattern or use case, along with a short quote or description of what that section says.

### Response format

URL Links

- Provide the direct link url, do not provide your own wording over the link.
- Prepend it with the link emoji
- Example
  - 🔗 https://react.dev/reference/react-dom/components/form#props

Provide a very short, quoted summary of the applicable section.
