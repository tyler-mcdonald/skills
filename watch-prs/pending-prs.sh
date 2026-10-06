#!/usr/bin/env bash
set -euo pipefail

fetch="$HOME/.claude/skills/handle-pr-review/fetch-threads.sh"
me=$(gh api user --jq .login)

gh search prs --author @me --state open --draft=false --json repository,number,url --limit 100 \
  --jq '.[] | "\(.repository.nameWithOwner) \(.number) \(.url)"' |
while read -r repo n url; do
  threads=$("$fetch" "$n" "$repo" | jq --arg me "$me" '[.[] | select(.comments[-1] | .author == $me or .bot)]')
  if [ "$threads" != "[]" ]; then
    jq -n --arg repo "$repo" --argjson n "$n" --arg url "$url" --argjson threads "$threads" \
      '{repo: $repo, number: $n, url: $url, threads: $threads}'
  fi
done | jq -s .
