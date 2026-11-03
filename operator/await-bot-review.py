#!/usr/bin/env python3
import json
import subprocess
import sys
import time

POLL_SECONDS = 60
TIMEOUT_SECONDS = 15 * 60


def fetch_comments(pr, repo):
    path = f"repos/{repo or '{owner}/{repo}'}/issues/{pr}/comments"
    cmd = ["gh", "api", "--paginate", path, "--jq", ".[]"]
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    return [json.loads(line) for line in result.stdout.splitlines() if line]


def login(comment):
    return ((comment.get("user") or {}).get("login") or "").removesuffix("[bot]")


def trigger_time(comments, trigger):
    times = [c["created_at"] for c in comments if c["body"].strip() == trigger]
    return max(times, default=None)


def is_done(comments, bot, trigger, done_text):
    since = trigger_time(comments, trigger)
    if since is None:
        sys.exit(f"no trigger comment {trigger!r} on the PR")
    return any(
        login(c) == bot and c["updated_at"] > since and done_text in c["body"]
        for c in comments
    )


def await_bot_review(pr, bot, trigger, done_text, repo):
    deadline = time.monotonic() + TIMEOUT_SECONDS
    while True:
        try:
            comments = fetch_comments(pr, repo)
        except subprocess.CalledProcessError as error:
            print(error.stderr, file=sys.stderr)
        else:
            if is_done(comments, bot, trigger, done_text):
                return "done"
        if time.monotonic() + POLL_SECONDS > deadline:
            return "timeout"
        time.sleep(POLL_SECONDS)


if __name__ == "__main__":
    pr, bot, trigger, done_text = sys.argv[1:5]
    repo = sys.argv[5] if len(sys.argv) > 5 else ""
    print(await_bot_review(pr, bot.removesuffix("[bot]"), trigger, done_text, repo))
