#!/usr/bin/env bash
set -euo pipefail

skill_dir="$(dirname "${BASH_SOURCE[0]}")/.."
tests_dir="$skill_dir/tests"

trusted_ids="$(grep -oE '^[0-9]+' "$skill_dir/trusted-authors.txt" | paste -sd, -)"
filter="[$trusted_ids] as \$trusted | $(cat "$skill_dir/filter-threads.jq")"

actual="$(jq "$filter" "$tests_dir/threads.json")"
expected="$(jq . "$tests_dir/expected.json")"

if [[ "$actual" != "$expected" ]]; then
  diff <(echo "$expected") <(echo "$actual")
  exit 1
fi
echo "pass"
