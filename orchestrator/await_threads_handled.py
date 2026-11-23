#!/usr/bin/env python3
import subprocess
import sys
import time

from unhandled_bot_threads import fetch_threads, unhandled_bot_threads

POLL_SECONDS = 60
TIMEOUT_SECONDS = 35 * 60


def await_threads_handled(pr, bot, repo):
    deadline = time.monotonic() + TIMEOUT_SECONDS
    fetched = False
    while True:
        try:
            threads = fetch_threads(pr, repo)
        except (subprocess.CalledProcessError, ValueError) as error:
            if not fetched:
                sys.exit(f"{error}\n{getattr(error, 'stderr', '') or ''}")
            print(error, file=sys.stderr)
        else:
            fetched = True
            if not unhandled_bot_threads(threads, bot):
                return "done"
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            return "timeout"
        time.sleep(min(POLL_SECONDS, remaining))


if __name__ == "__main__":
    pr = sys.argv[1]
    bot = sys.argv[2].removesuffix("[bot]")
    repo = sys.argv[3] if len(sys.argv) > 3 else ""
    print(await_threads_handled(pr, bot, repo))
