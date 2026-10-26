import json
import sys
from pathlib import Path

USAGE_KEYS = (
    "input_tokens",
    "cache_creation_input_tokens",
    "cache_read_input_tokens",
    "output_tokens",
)

ROLES = (
    ("code-review-cycle/reviewer.md", "reviewer"),
    ("code-review-cycle/fixer.md", "fixer"),
    ("Invoke `simplify`", "simplify"),
    ("Implement ", "dev"),
    ("Review target:", "/code-review"),
    ("Fix these QA findings", "QA fixer"),
)


def first_prompt(records):
    for r in records:
        if r.get("type") == "user":
            content = r["message"]["content"]
            if isinstance(content, list):
                content = " ".join(
                    c.get("text", "") for c in content if isinstance(c, dict)
                )
            return " ".join(content.split())[:80]
    return ""


def role(prompt):
    for marker, name in ROLES:
        if marker in prompt:
            return name
    return "?"


def tool_result_sizes(records):
    for r in records:
        content = r.get("message", {}).get("content")
        if r.get("type") != "user" or not isinstance(content, list):
            continue
        for c in content:
            if isinstance(c, dict) and c.get("type") == "tool_result":
                yield len(json.dumps(c.get("content"))), r.get("timestamp", "")


def load(path, until):
    records = []
    for line in path.open():
        r = json.loads(line)
        if until and r.get("timestamp", "") > until:
            break
        records.append(r)
    return records


def usage_totals(records):
    seen = {}
    for r in records:
        msg = r.get("message", {})
        if r.get("type") == "assistant" and msg.get("usage"):
            u = seen.setdefault(msg.get("id") or r["uuid"], {})
            for k in USAGE_KEYS:
                u[k] = max(u.get(k, 0), msg["usage"].get(k) or 0)
    totals = {k: sum(u[k] for u in seen.values()) for k in USAGE_KEYS}
    totals["turns"] = len(seen)
    return totals


def main(session_path, until=None):
    session = Path(session_path)
    files = [session] + sorted(
        (session.parent / session.stem / "subagents").glob("*.jsonl")
    )
    rows = []
    for f in files:
        records = load(f, until if f == session else None)
        prompt = first_prompt(records)
        largest = max(tool_result_sizes(records), default=(0, ""))
        name = "main" if f == session else role(prompt)
        rows.append((name, usage_totals(records), largest[0], f.name, prompt))
    columns = ("input", "cache_write", "cache_read", "output", "turns")
    keys = USAGE_KEYS + ("turns",)
    print(f"{'agent':<14}" + "".join(f"{c:>13}" for c in columns))
    for name, totals, largest, file, prompt in sorted(
        rows, key=lambda r: -r[1]["cache_read_input_tokens"]
    ):
        cells = "".join(f"{totals[k]:>13,}" for k in keys)
        print(f"{name:<14}{cells}  largest_tool_result={largest:,}ch  {file}  {prompt}")
    grand = {k: sum(r[1][k] for r in rows) for k in keys}
    print(f"{'total':<14}" + "".join(f"{grand[k]:>13,}" for k in keys))


if __name__ == "__main__":
    main(*sys.argv[1:3])
