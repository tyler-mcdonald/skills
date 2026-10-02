# operator baseline

Measured 2026-10-01, before #10–#14. Runs in cardcase. Tokens = input + cache creation + cache read + output, each message id once, the user's turns after the final report excluded.

| Agent | #132 (9.33M) | #130 (5.87M) | #139 (3.55M) |
|---|---|---|---|
| Main coordinator | 0.98M 10.6% | 1.05M 17.9% | 1.26M 35.6% |
| handle-pr-review (inline in main) | 0.95M 10.2% | 0.84M 14.4% | 0.72M 20.4% |
| Dev | 2.26M 24.2% | 1.28M 21.9% | 0.49M 13.9% |
| Reviewer R1 | 1.04M 11.1% | 0.95M 16.1% | 0.56M 15.9% |
| R1's /code-review | 1.28M 13.7% | 0.26M 4.5% | 0.50M 14.1% |
| Fixer 1 | 1.56M 16.8% | 0.78M 13.3% | – |
| Reviewer R2 | 0.94M 10.0% | 0.43M 7.3% | – |
| R2's /code-review | 0.32M 3.4% | 0.28M 4.7% | – |

## Outcomes

- #132: R1 full 4 → fix → R2 verify 4, stopped at max_rounds. Greptile: 5 comments, 3 repeated the reviewer's beyond-goal findings.
- #130: R1 full 4 → fix → R2 verify 5. Greptile: 2 comments overlapped the reviewer's beyond-goal findings.
- #139: R1 full 5. Greptile: 1 comment.

## Waste signals

| Signal | #132 | #130 | #139 |
|---|---|---|---|
| Refused writes | 15 | 9 | 3 |
| Issue fetches | 7–10 per run | | |
| Full check-suite runs | 6 (same SHA ×3) | 8 (same SHA ×3) | 3 |
| `gh pr checks --watch` output | 1.5k (piped to tail) | 1.5k (piped to tail) | 21.3k |
| Full diff printed | 37.6k chars | 64.2k chars | |
| Reviewer replies vs round JSON | 3.9k / 3.8k vs 5.1k / 6.5k | 4.4k / 4.1k vs 6.1k / 7.5k | 3.1k vs 2.3k |
