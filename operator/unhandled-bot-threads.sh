#!/usr/bin/env bash
set -euo pipefail

pr="$1"
bot="${2%\[bot\]}"
repo="${3:-}"

"$(dirname "$0")/../handle-pr-review/fetch-threads.sh" "$pr" "$repo" | jq --arg bot "$bot" '
  [.[]
  | select(.comments[0] | .bot and .author == $bot)
  | select(any(.comments[]; .author == "claude") | not)
  | {path, line}]'
