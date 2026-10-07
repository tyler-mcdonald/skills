#!/usr/bin/env bash
set -uo pipefail

interval=$1
rerun="/watch-prs${2:+ $2}"
pending="$(dirname "$0")/pending-prs.sh"
pidfile="${TMPDIR:-/tmp}/watch-prs-wait.pid"
max_failures=10

if [ -f "$pidfile" ] && kill -0 "$(cat "$pidfile")" 2>/dev/null; then
  echo "Already waiting"
  exit 0
fi
echo $$ > "$pidfile"
trap 'rm -f "$pidfile"' EXIT

baseline=""
failures=0
while :; do
  if out=$("$pending"); then
    failures=0
    if [ -z "$baseline" ]; then
      baseline=$out
    elif [ "$out" != "$baseline" ]; then
      echo "Changed: run $rerun"
      exit 0
    fi
  else
    failures=$((failures + 1))
    if [ "$failures" -ge "$max_failures" ]; then
      echo "Failed: pending-prs.sh failed $max_failures times in a row"
      exit 1
    fi
  fi
  sleep "$interval"
done
