#!/usr/bin/env bash
set -uo pipefail

interval=$1
pending="$(dirname "$0")/pending-prs.sh"
lockdir="${TMPDIR:-/tmp}/watch-prs-wait.lock"
max_failures=10

if ! mkdir "$lockdir" 2>/dev/null; then
  pid=$(cat "$lockdir/pid" 2>/dev/null)
  if [ -z "$pid" ] || kill -0 "$pid" 2>/dev/null; then
    echo "Already waiting"
    exit 0
  fi
  rm -rf "$lockdir"
  if ! mkdir "$lockdir" 2>/dev/null; then
    echo "Already waiting"
    exit 0
  fi
fi
trap 'rm -rf "$lockdir"' EXIT
echo $$ > "$lockdir/pid"

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
