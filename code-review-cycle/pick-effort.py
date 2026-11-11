#!/usr/bin/env python3
import subprocess
import sys
from pathlib import PurePosixPath

LOCKFILES = {
    "package-lock.json",
    "yarn.lock",
    "pnpm-lock.yaml",
    "uv.lock",
    "poetry.lock",
    "Cargo.lock",
    "go.sum",
}
LOW_MAX = 50
MEDIUM_MAX = 400


def git(*args):
    return subprocess.run(
        ["git", *args],
        check=True,
        capture_output=True,
        text=True,
        errors="surrogateescape",
    ).stdout


def changed_lines(numstat):
    total = 0
    fields = iter(numstat.split("\0"))
    for entry in fields:
        if not entry:
            continue
        added, deleted, path = entry.split("\t", 2)
        if not path:
            next(fields)
            path = next(fields)
        if added == "-" or deleted == "-":
            continue
        if PurePosixPath(path).name in LOCKFILES:
            continue
        total += int(added) + int(deleted)
    return total


def effort(lines):
    if lines <= LOW_MAX:
        return "low"
    if lines <= MEDIUM_MAX:
        return "medium"
    return "high"


def pick_effort(base):
    git("fetch", "origin", f"+refs/heads/{base}:refs/remotes/origin/{base}")
    return effort(
        changed_lines(git("diff", "--numstat", "-z", f"origin/{base}...HEAD"))
    )


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: pick-effort.py <base>")
    try:
        print(pick_effort(sys.argv[1]))
    except subprocess.CalledProcessError as error:
        sys.exit(f"{error}\n{error.stderr or ''}")
