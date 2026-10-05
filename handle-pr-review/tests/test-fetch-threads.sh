#!/usr/bin/env bash
set -euo pipefail

tests_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
skill_dir="$(dirname "$tests_dir")"

export PATH="$tests_dir/bin:$PATH"
export GH_FIXTURE="$tests_dir/threads.json"

expected="$(jq . "$tests_dir/expected.json")"
failed=0

check() {
  local name="$1" actual
  actual="$("$2/fetch-threads.sh" 1 | jq .)"
  if [[ "$actual" == "$expected" ]]; then
    echo "pass: $name"
  else
    echo "fail: $name"
    diff <(echo "$expected") <(echo "$actual") || true
    failed=1
  fi
}

check "shipped trusted-authors.txt" "$skill_dir"

scratch="$(mktemp -d)"
trap 'rm -rf "$scratch"' EXIT
ln -s "$skill_dir/fetch-threads.sh" "$skill_dir/filter-threads.jq" "$scratch/"
cp "$tests_dir/trusted-authors.txt" "$scratch/"
check "blank lines, comments, commented-out ID" "$scratch"

exit "$failed"
