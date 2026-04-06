---
name: debug-cross-repo
description: Debug issues across aisearch-frontend and aisearch-backend by searching both repos, tracing API boundaries, and reporting findings from both sides. Use when user has a bug that might span frontend and backend, mentions cross-repo debugging, or isn't sure which repo a bug is in.
---

# Debug Cross-Repo

Investigate a bug or unexpected behavior across both aisearch repos. Minimize questions — start investigating immediately.

## Inputs

Accept any of: error message, stack trace, behavior description, or screenshot. If the user hasn't provided anything, ask ONE question: "What's the problem you're seeing?"

## Process

### 1. Determine the sibling repo path

The two repos are siblings. Detect which one you're currently in and derive the other:

- If cwd contains `aisearch-frontend`: sibling is `../aisearch-backend`
- If cwd contains `aisearch-backend`: sibling is `../aisearch-frontend`
- If cwd is a parent of both: frontend is `aisearch-frontend/`, backend is `aisearch-backend/`

### 2. Identify the symptom layer

From the user's description, determine where the symptom originates:

- **Frontend**: UI misbehavior, rendering issues, client-side errors, wrong data displayed
- **Backend**: API errors, wrong response data, server logs, status codes
- **Unknown**: vague description — search both

### 3. Trace from symptom to API boundary

Use the Agent tool with subagent_type=Explore to investigate. Launch two agents in parallel:

**Agent A — Symptom repo** (where the bug appears):
- Find the code path involved
- Trace to the API call or endpoint at the boundary
- Identify the request shape (URL, method, params, body) or response shape expected

**Agent B — Other repo**:
- Find the corresponding endpoint or API call
- Check the request/response contract on that side
- Look for recent changes to the relevant code (`git log`)

### 4. Compare across the boundary

Once both agents report back, compare:

- Does the frontend send what the backend expects?
- Does the backend return what the frontend expects?
- Are there type mismatches, missing fields, changed URLs, or auth issues?
- Are there environment or config differences?

### 5. Report findings

Present a concise summary:

```
## Symptom
What the user reported

## Frontend side
What happens in the frontend code (file, function, API call)

## Backend side
What happens in the backend code (endpoint, handler, response)

## Mismatch / Root cause
Where the two sides disagree, or where the actual bug is

## Suggested fix
Which repo needs the change and what to do
```

If the bug is clearly in one repo only, say so. Don't force a cross-repo narrative if it's a single-repo issue.
