#!/usr/bin/env python3
import os
import re
import signal
import subprocess
import sys
import time
from pathlib import Path

TIMEOUT_SECONDS = 120


def git(*args):
    return subprocess.run(
        ["git", *args], check=True, capture_output=True, text=True
    ).stdout.strip()


ROOT = Path(git("rev-parse", "--show-toplevel"))
STATE = Path(git("rev-parse", "--absolute-git-dir")) / "run-app"


def tail(path, lines=20):
    return "\n".join(path.read_text(errors="replace").splitlines()[-lines:])


def stop():
    for pidfile in STATE.glob("*.pid"):
        pgid = int(pidfile.read_text())
        try:
            os.killpg(pgid, signal.SIGTERM)
            for _ in range(20):
                time.sleep(0.5)
                os.killpg(pgid, 0)
        except (ProcessLookupError, PermissionError):
            pass
        pidfile.unlink()


def fail(message, log=None):
    print(message, file=sys.stderr)
    if log:
        print(f"Last lines of {log}:\n{tail(log)}", file=sys.stderr)
    stop()
    sys.exit(1)


def make_targets():
    makefile = ROOT / "Makefile"
    if not makefile.exists():
        fail(f"No Makefile in {ROOT}.")
    names = re.findall(r"^([\w-]+):", makefile.read_text(), re.M)
    dev = [n for n in names if n.startswith("dev-")] or [n for n in names if n == "dev"]
    if not dev:
        fail("The Makefile has no dev or dev-* targets.")
    return "setup" in names, dev


def listening_ports(pgid):
    out = subprocess.run(
        ["lsof", "-nP", "-a", "-g", str(pgid), "-iTCP", "-sTCP:LISTEN", "-Fn"],
        capture_output=True,
        text=True,
    ).stdout
    return sorted({int(p) for p in re.findall(r"^n.*:(\d+)$", out, re.M)})


def start():
    STATE.mkdir(exist_ok=True)
    stop()
    has_setup, targets = make_targets()

    if has_setup:
        log = STATE / "setup.log"
        print(f"==> make setup (log: {log})")
        with log.open("w") as f:
            if subprocess.run(["make", "setup"], cwd=ROOT, stdout=f, stderr=f).returncode:
                fail("make setup failed.", log)

    procs = {}
    for target in targets:
        log = STATE / f"{target}.log"
        proc = subprocess.Popen(
            ["make", target],
            cwd=ROOT,
            stdin=subprocess.DEVNULL,
            stdout=log.open("w"),
            stderr=subprocess.STDOUT,
            env={**os.environ, "PYTHONUNBUFFERED": "1"},
            start_new_session=True,
        )
        (STATE / f"{target}.pid").write_text(str(proc.pid))
        procs[target] = (proc, log)

    ports = {}
    deadline = time.time() + TIMEOUT_SECONDS
    while len(ports) < len(procs):
        for target, (proc, log) in procs.items():
            if "in use" in log.read_text(errors="replace"):
                fail(f"make {target}: a port is already in use, likely by another app instance.", log)
            if proc.poll() is not None:
                fail(f"make {target} exited with code {proc.returncode}.", log)
            if target not in ports and (found := listening_ports(proc.pid)):
                ports[target] = found
        if time.time() > deadline:
            waiting = ", ".join(t for t in procs if t not in ports)
            fail(f"Timed out waiting for {waiting} to listen.", procs[waiting.split(", ")[0]][1])
        time.sleep(1)

    for target, (_, log) in procs.items():
        urls = " ".join(f"http://localhost:{p}" for p in ports[target])
        print(f"{target}: {urls}  (log: {log})")
    print(f"Stop: {Path(__file__).resolve()} stop")


if __name__ == "__main__":
    if sys.argv[1:] == ["stop"]:
        if STATE.exists():
            stop()
        print("Stopped.")
    else:
        start()
