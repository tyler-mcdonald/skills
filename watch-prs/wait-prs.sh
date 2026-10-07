#!/usr/bin/env bash
set -uo pipefail

interval=$1
pending="$(dirname "$0")/pending-prs.sh"
pidfile="${TMPDIR:-/tmp}/watch-prs-wait.pid"
max_failures=10

if [ -f "$pidfile" ] && kill -0 "$(cat "$pidfile")" 2>/dev/null; then
  echo "Already waiting"
  exit 0
fi
echo $$ > "$pidfile"
trap 'rm -f "$pidfile"' EXIT

failures=0
while :; do
  if out=$("$pending") && current=$(jq -r '.[] | "\(.url) \(.status)"' <<<"$out" | sort); then
    failures=0
    previous=${previous-$current}
    if [ -n "$(comm -13 <(echo "$previous") <(echo "$current"))" ]; then
      echo "Changed"
      exit 0
    fi
    previous=$current
  else
    failures=$((failures + 1))
    if [ "$failures" -ge "$max_failures" ]; then
      echo "Failed: pending-prs.sh failed $max_failures times in a row"
      exit 1
    fi
  fi
  sleep "$interval"
done
