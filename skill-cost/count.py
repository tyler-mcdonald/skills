import json
import sys
from pathlib import Path

USAGE_KEYS = ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens", "output_tokens")


def first_prompt(records):
    for r in records:
        if r.get("type") == "user":
            content = r["message"]["content"]
            if isinstance(content, list):
                content = " ".join(c.get("text", "") for c in content if isinstance(c, dict))
            return " ".join(content.split())[:80]
    return ""


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
            seen[msg.get("id") or r["uuid"]] = msg["usage"]
    return {k: sum(u.get(k, 0) for u in seen.values()) for k in USAGE_KEYS}


def main(session_path, until=None):
    session = Path(session_path)
    files = [session] + sorted((session.parent / session.stem / "subagents").glob("*.jsonl"))
    rows = []
    for f in files:
        records = load(f, until if f == session else None)
        totals = usage_totals(records)
        largest = max(tool_result_sizes(records), default=(0, ""))
        rows.append((f.name, sum(totals.values()), totals, largest[0], first_prompt(records)))
    grand = sum(r[1] for r in rows) or 1
    print(f"total {grand:,}")
    for name, total, totals, largest, prompt in sorted(rows, key=lambda r: -r[1]):
        print(f"{total:>12,} {100 * total / grand:5.1f}%  out={totals['output_tokens']:,}  largest_tool_result={largest:,}ch  {name}  {prompt}")


if __name__ == "__main__":
    main(*sys.argv[1:3])
