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
        ["git", *args], check=True, capture_output=True, text=True
    ).stdout


def new_path(path):
    if "=>" not in path:
        return path
    if "{" in path:
        prefix, rest = path.split("{", 1)
        inner, suffix = rest.split("}", 1)
        return prefix + inner.split("=>", 1)[1].strip() + suffix
    return path.split("=>", 1)[1].strip()


def changed_lines(numstat):
    total = 0
    for line in numstat.splitlines():
        if not line:
            continue
        added, deleted, path = line.split("\t", 2)
        if added == "-" or deleted == "-":
            continue
        if PurePosixPath(new_path(path)).name in LOCKFILES:
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
    git("fetch", "origin")
    return effort(changed_lines(git("diff", "--numstat", f"origin/{base}...HEAD")))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: pick-effort.py <base>")
    try:
        print(pick_effort(sys.argv[1]))
    except subprocess.CalledProcessError as error:
        sys.exit(f"{error}\n{error.stderr or ''}")
