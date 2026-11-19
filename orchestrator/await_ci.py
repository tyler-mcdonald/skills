#!/usr/bin/env python3
import json
import subprocess
import sys
import time

POLL_SECONDS = 15
REGISTER_SECONDS = 2 * 60
TIMEOUT_SECONDS = 30 * 60
FETCH_TIMEOUT_SECONDS = 30
NO_CHECKS = "no checks reported"


def fetch_checks(pr, repo):
    cmd = ["gh", "pr", "checks", pr, "--json", "name,bucket"]
    if repo:
        cmd += ["--repo", repo]
    result = subprocess.run(
        cmd,
        check=False,
        capture_output=True,
        text=True,
        timeout=FETCH_TIMEOUT_SECONDS,
    )
    if NO_CHECKS in result.stderr:
        return []
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        raise subprocess.CalledProcessError(
            result.returncode, cmd, result.stdout, result.stderr
        ) from None


def outcome(checks):
    buckets = {c["bucket"] for c in checks}
    if buckets & {"fail", "cancel"}:
        return "fail"
    if "pending" in buckets or not checks:
        return None
    return "pass"


def await_ci(pr, repo):
    start = time.monotonic()
    fetched = False
    while True:
        try:
            checks = fetch_checks(pr, repo)
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as error:
            if not fetched:
                sys.exit(f"{error}\n{error.stderr or ''}")
            print(error, error.stderr or "", sep="\n", file=sys.stderr)
        else:
            fetched = True
            result = outcome(checks)
            if result:
                return result
            if not checks and time.monotonic() - start >= REGISTER_SECONDS:
                return "none"
        if time.monotonic() - start >= TIMEOUT_SECONDS:
            return "timeout"
        time.sleep(POLL_SECONDS)


if __name__ == "__main__":
    pr = sys.argv[1]
    repo = sys.argv[2] if len(sys.argv) > 2 else ""
    print(await_ci(pr, repo))
