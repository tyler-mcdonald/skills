#!/usr/bin/env bash
set -uo pipefail

interval=${1-}
if ! [[ $interval =~ ^[1-9][0-9]*$ ]]; then
  echo "Failed: interval must be a positive number of seconds"
  exit 1
fi
pending="$(dirname "$0")/pending-prs.sh"
lockfile="${TMPDIR:-/tmp}/watch-prs-wait.flock"
max_failures=10

exec 9>"$lockfile"
if ! perl -MFcntl=:flock -e 'open(my $fh, ">&=", 9) or exit 2; flock($fh, LOCK_EX | LOCK_NB) or exit 1'; then
  echo "Already waiting"
  exit 0
fi

failures=0
while :; do
  if out=$("$pending" 9>&-) && current=$(jq -r '.[] | "\(.url) \(.status)"' <<<"$out" | sort); then
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
  sleep "$interval" 9>&-
done
