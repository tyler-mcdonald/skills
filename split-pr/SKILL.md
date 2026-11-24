---
name: split-pr
description: Split a PR's behavior-preserving refactors and unrelated changes into stacked PRs, without changing its code. Use when asked to split a PR.
---

## Steps

1. Setup
   - Work on the PR's branch in the worktree that already has it, else invoke `setup-worktree` and run `gh pr checkout <pr>`.
   - Fetch `origin`. Let M be `git merge-base origin/<base branch> HEAD`.

2. Pick splits
   - Read `git diff M...HEAD`.
   - Pick pieces that change no behavior (extractions, moves, renames) or are unrelated to the PR's goal.
   - Skip a piece if it can't stand alone without code that isn't in the diff.
   - If no split is worth making, stop and say so.

3. Open the splits

   For each split, in review order:

   1. Branch from the previous split, or from M for the first.
   2. Apply only this split's changes: whole files from the PR branch, or a file's base version with only this split's edits.
   3. Commit and `git push -u origin HEAD`.
   4. Open the PR with `open-pr`, based on the previous split's branch, or the PR's base for the first.

4. Restack the PR
   1. On the PR's branch, `git merge -s ours --no-edit <last split branch>`.
   2. `git push` (never force-push).
   3. `gh pr edit <pr> --base <last split branch>`.

5. Report
   - The stack in review order, with each PR's full URL.
   - GitHub's "Rebase stack" conflicts on this stack; after each PR merges, sync the next with `sync-branch`.
