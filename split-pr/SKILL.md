---
name: split-pr
description: Split a PR's behavior-preserving refactors and unrelated changes into stacked PRs, without changing its code. Use when asked to split a PR.
---

## Steps

1. Pick splits
   - On the PR's branch, read `git diff $(git merge-base origin/<base branch> HEAD)...HEAD`.
   - Pick pieces that change no behavior or are unrelated to the PR's goal, and can stand alone using only lines from the base or the PR.
   - If none is worth splitting, stop and say so.

2. Open the splits
   - For each, branch from the previous split (or the merge base), apply only its changes, push, and open it with `open-pr` stacked on the previous one (the first on the PR's base).

3. Restack the PR
   1. Check out the PR's branch, `git merge -s ours --no-edit <last split branch>`, then `git push`.
   2. `gh pr edit <pr> --base <last split branch>`.
   3. Reply with the stack's PR URLs in review order.
