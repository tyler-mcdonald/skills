---
name: review-component-state
description: Review frontend components for state held at the wrong altitude and components that should be presentational. Use when the user asks to review component state or data flow.
---

# Review component state

Review frontend components for state held at the wrong altitude. State belongs in the
lowest common parent of everything that uses it — no higher, no lower. Components
below that owner should be presentational ("dummy"): they receive data and callbacks
as props.

Server data, mutations, and anything a parent needs to coordinate belong in the
owning component. Purely local UI state (input values, open/closed, hover) can stay
in a presentational component, as long as nothing above it needs it.

Be strict about what to flag: report every case, even small ones. Let each finding's
rating, tradeoff, and recommendation carry the judgment of whether it's worth doing.

This is a review only. Make no code changes.

## Scope

Review the components the user names. Otherwise, review the frontend components
changed on the current branch compared with `origin/main` (fetch it first).

## Steps

1. Read the components, their parents, their siblings, and the data hooks they call.
2. Look for state held too low, e.g.:
   - A parent needs a child's state and has to reach for it indirectly (global
     lookups, mutation keys, refs) instead of receiving it as a prop.
   - Sibling components duplicating the same state, fetching, or logic instead of
     sharing it from their common parent.
   - A presentational component interprets API shapes (errors, responses) instead of
     receiving display-ready values.
   - Leaf components calling data hooks that a parent could pass in as props.
3. Look for state held too high, e.g.:
   - A parent holding state that only one child uses.
   - Props passed through components that don't use them, just to reach a
     descendant.

## Output

Group findings under **High**, **Medium**, and **Low**:

- **High** — causes or risks a bug, or forces workarounds elsewhere (e.g. a parent
  reaching into a child's state indirectly, or siblings duplicating state that can
  drift apart).
- **Medium** — couples a component to data or API details it shouldn't know, making it
  harder to reuse or test.
- **Low** — optional tidying; worth doing only if the code is being touched anyway.

Number findings continuously across severities, and format every finding the same
way, keeping each line to a sentence:

```
## High

1. `ComponentName` (`path/to/file.tsx:12`) - Very concise summary of the finding.
   - Rule Failure: The specific rule or practice it breaks.
   - Tradeoff(s): The cost of changing it, or "None".
   - Recommendation: The concrete change.

## Medium

2. ...

## Low

3. ...
```

Omit a severity heading if it has no findings. End with a suggested order to tackle
the findings, noting which ones are worth skipping unless they come up.
