---
name: plan-issue
description: Read a GitLab issue, draft an implementation plan, then stress-test it via /grill-me. Use when user provides a GitLab issue URL and wants to plan, break down, or implement a feature.
---

# Plan Issue

## Process

### 1. Read the issue

Extract the project path and issue number from the provided GitLab URL, then read it:

```bash
glab issue view <number> -R <project-path>
```

### 2. Explore the codebase

Use the Agent tool with subagent_type=Explore to understand:

- Current architecture and patterns relevant to the issue
- Existing code that will be touched or extended
- Integration points and dependencies

### 3. Draft the plan

Present a concise implementation plan:

- What changes are needed and where
- Key design decisions
- Vertical slices / phases if non-trivial
- Edge cases or risks

### 4. Stress-test

Invoke `/grill-me` to interrogate the plan with the user.
