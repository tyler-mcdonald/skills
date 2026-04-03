---
name: fix-types
description: Iteratively runs mypy and fixes type errors until the project is clean. Use when user wants to fix type errors, mentions mypy failures, or asks to make types pass.
---

# Fix Types

Runs mypy, fixes errors, repeats until clean — up to 5 iterations. Never adds `# type: ignore`. Leaves all changes unstaged.

## Quick start

```
/fix-types              # check entire project
/fix-types path/to/app  # check specific module or file
```

## Workflow

### 1. Determine target

- If args provided, use them as the mypy target
- Otherwise, use `.` (entire project)

### 2. Run mypy

```bash
poetry run mypy <target>
```

If clean on first run: report success, stop.

### 3. Fix loop (max 5 iterations)

For each iteration:

1. Parse mypy output — group errors by file
2. For each file with errors, read the file and fix all errors in that file before moving to the next
3. Re-run mypy
4. If clean: report success and stop
5. If errors remain and iteration < 5: continue
6. If iteration == 5 and errors remain: report unfixed errors and stop

### 4. Fixing rules

**Never use `# type: ignore`** — always find a proper typed solution:

- Missing return type → add explicit return annotation
- Incompatible types → fix the actual type mismatch (correct the annotation or the value)
- Untyped function → add full signature annotations
- Missing stubs → add `py.typed`, use `TYPE_CHECKING` guards, or find the correct stub package
- `Any` where specific type needed → narrow the type; look at the actual values being passed
- Optional not handled → add explicit `None` check or use `assert`
- Dict/list type issues → use proper generic annotations (`dict[str, int]`, `list[str]`)

If an error genuinely cannot be fixed without `# type: ignore` (e.g., broken upstream stubs with no workaround): skip it, note it in the final report, do not add the ignore comment.

### 5. Final report

Always end with one of:
- "mypy clean after N iteration(s)" — if fully resolved
- "mypy clean" — if it was already passing
- "N errors remain after 5 iterations" + list of unfixed errors — if not fully resolved
