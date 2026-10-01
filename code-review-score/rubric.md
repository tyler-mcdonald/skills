# Review score rubric

Score 1–5. 5 means ready to merge.

## 1. Which findings count

- **Scoped to the goal, not the diff.** A changed line isn't enough. A finding is scored only if it:
  - puts an acceptance criterion at risk, or
  - is a regression: something that worked on the base branch and now fails or behaves worse, other than changes the goal intends.

  Anything else is **beyond the goal**: report it with a one-line follow-up suggestion, but don't score it.
- **Scope creep is a finding.** Code the diff adds that no acceptance criterion needs is one **Minor**, and its fix is to remove that code. Don't score edge cases inside that code separately — they go away with it.
- **Pre-existing.** Issues in code the branch didn't change, and that it doesn't make worse, are reported separately, not scored.
- **One root cause, one finding.** Merge findings that share a cause; list each symptom under it. The merged finding takes the most severe symptom's severity.
- **Nits** — style, naming preference — are reported but not scored.
- **Duplication** — code the branch adds that duplicates logic, a rule, or a query already elsewhere — always goes in `findings`, as a Nit unless it has a behavioral effect, even when it's otherwise beyond the goal.
- **Accepted.** A finding whose root cause matches a user decision is reported as `accepted` with the decision's reason, not scored. If the finding shows something the decision didn't cover, score that part as a new finding.
- **Goal gaps.** Each acceptance criterion from the goal that the branch doesn't meet is a finding: unmet → **Major**, partly met → **Minor**. Skip the severity questions for these. Judge each criterion by the outcome it states, not the strictest reading of its wording. Items the goal lists as nice-to-have or out of scope aren't graded.

## 2. Verdict

- **CONFIRMED** — the mechanism was reproduced (you ran it) or is provable from the repo's code and its dependencies' documented behavior. A finding can be CONFIRMED even if it only triggers under specific tooling; that's handled by *When*.
- **PLAUSIBLE** — the mechanism itself is unverified: it relies on assumed behavior you didn't check.

PLAUSIBLE findings count one severity lower.

## 3. Severity

Answer three questions per finding:

| Question | Answers |
|---|---|
| **How** does it fail? | `silent` — wrong data, security hole, data loss · `loud` — crash, error, failed build/boot · `friction` — misleading message or docs, extra manual step |
| **Where** does it fail? | `prod` · `ci` — CI or deploy pipeline · `dev` — local development only |
| **When** does it fail? | `default` — normal usage, default config · `conditional` — specific input, tooling, or config · `contrived` — unrealistic setup |

Then:

- `friction` → **Minor** (Nit if `contrived`).
- `silent` or `loud` → start at **Blocker**, drop one level for `ci` or `dev`, one for `conditional`, two for `contrived`. Never below **Minor**, except `contrived` may reach **Nit**.
- **Override:** a security hole or data loss/corruption in `prod` that isn't `contrived` is always a **Blocker**.

Special cases:

- **Intended fail-fast.** A failure that is the goal's stated purpose, is documented, and has an error naming the fix is `friction`.
- **Untested behavior.** A changed behavior with no test is **Major** if it could fail `silent` in `prod`; otherwise **Minor**.

Levels, high to low: Blocker → Major → Minor → Nit.

## 4. Score

1. `score = 5 − Majors − (1 if any Minors else 0)`
2. Blockers: 1 → score is 2; 2 or more → score is 1.
3. Any project check (tests, lint, typecheck) failing → cap at 2.
4. Clamp to 1–5.

The score has roughly ±1 run-to-run variance because the review doesn't find identical issues every time. Always compare scores taken at the same effort level.

## 5. Which findings get fixed

This section is the only fix policy. Set `"fix"` on every finding:

- `true` — scored findings (Blocker, Major, Minor), and duplication at any severity.
- `false` — everything else: other Nits, accepted, beyond the goal, pre-existing.

Fixing never changes a finding's severity or the score.

## 6. JSON block

End the report with:

```json
{
  "target": { "base": "main", "head": "<branch>", "head_sha": "<sha>" },
  "effort": "high",
  "goal": {
    "source": "#123",
    "criteria": [{ "criterion": "...", "status": "met" }]
  },
  "score": 4,
  "checks": { "tests": "pass", "lint": "pass", "typecheck": "pass" },
  "counts": { "blocker": 0, "major": 0, "minor": 2, "nit": 1, "pre_existing": 0 },
  "findings": [
    {
      "id": "F1",
      "file": "path/to/file.py",
      "line": 12,
      "summary": "...",
      "root_cause": "...",
      "symptoms": ["..."],
      "verdict": "CONFIRMED",
      "how": "loud",
      "where": "dev",
      "when": "default",
      "severity": "minor",
      "fix": true,
      "judgment_call": null
    }
  ],
  "accepted": [{ "finding_id": "F3", "reason": "..." }],
  "beyond_goal": [{ "summary": "...", "follow_up": "..." }],
  "pre_existing": [],
  "rounds": [],
  "stop_reason": null,
  "escalations": []
}
```

The coordinator fills `rounds` (`{ "round", "score", "commit" }`), `stop_reason`, and `escalations` (`{ "finding_id", "decision_needed" }`).
