---
name: refactor-test-duplication
description: Refactors duplicated steps in the tests changed in the current diff into readable helpers, favoring readable (DAMP) tests over DRY ones. Invoke manually with /refactor-test-duplication.
disable-model-invocation: true
---

# Refactor Test Duplication

The goal is readability, understandability, and maintainability — not fewer lines. Tests
should be DAMP (Descriptive And Meaningful Phrases), not DRY: a reader should understand
each test top to bottom without jumping to its helpers. See "Tests and Code Sharing:
DAMP, Not DRY" in [Software Engineering at Google, ch. 12](https://abseil.io/resources/swe-book/html/ch12.html).

## Scope

Only the tests changed in the current diff:

1. If the user names files or a PR, use those. Otherwise take the changed files from
   `git diff @{upstream}...HEAD --name-only` (or `git diff main...HEAD --name-only`),
   plus `git diff HEAD --name-only` for uncommitted changes.
2. Keep only test files, per the project's test naming (e.g. `*.test.ts(x)`,
   `test_*.py`).
3. Within those files, look only at duplication involving changed tests. Touch an
   unchanged test only when it calls a helper you're generalizing or renaming.

## Extract when

- **The same action appears at different levels of abstraction** — a helper for one
  field, inline events for the others → generalize the helper so every step reads alike.
- **A non-obvious incantation repeats** → name it once, where its reason is visible
  (e.g. a mock's `calls[0][0]` → `submittedInput()`).
- **A multi-step user action repeats verbatim** → one helper named for the action
  (e.g. `createAccountNamed(name)`).

## Leave alone

- **Per-test setup** (mock return values, fixtures) stays in each test, not in
  `beforeEach`, unless it is identical for every test in the block.
- **The assertion that is the point of the test** — never wrap it in a helper.
- **Two short, similar lines** — cheaper than the indirection.
- **Cross-file sharing** — keep helpers in the test file; move one to shared test
  utilities only when a second file already needs the same helper.
- **Parametrizing** (`it.each`, `pytest.mark.parametrize`) only when tests differ solely
  in data and each case keeps a descriptive name.

Helpers are plain functions at the top of the test file, named for the user action or
intent rather than the mechanism. Generalize an existing helper before adding a sibling,
and don't add flags that switch a helper's behavior.

## Process

1. Gather the scope above.
2. Propose, without editing: each change (what repeats, the helper or change, why it
   reads better), then what you're deliberately leaving and why. Wait for the user's
   go-ahead.
3. Apply the approved changes, run the affected tests plus the project's typecheck and
   lint, and report the result.
