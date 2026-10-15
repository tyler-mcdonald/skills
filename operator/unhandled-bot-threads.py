#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path

FETCH_THREADS = Path(__file__).parent / "../handle-pr-review/fetch-threads.py"


def fetch_threads(pr, repo):
    cmd = [sys.executable, str(FETCH_THREADS), pr, repo]
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    return json.loads(result.stdout)


def unhandled_bot_threads(threads, bot):
    return [
        {"path": thread["path"], "line": thread["line"]}
        for thread in threads
        if thread["comments"][0]["bot"]
        and thread["comments"][0]["author"] == bot
        and not any(c["author"] == "claude" for c in thread["comments"])
    ]


if __name__ == "__main__":
    pr = sys.argv[1]
    bot = sys.argv[2].removesuffix("[bot]")
    repo = sys.argv[3] if len(sys.argv) > 3 else ""
    json.dump(unhandled_bot_threads(fetch_threads(pr, repo), bot), sys.stdout)
    print()
