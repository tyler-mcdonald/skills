#!/usr/bin/env bash
set -euo pipefail

fetch="$(dirname "$0")/../handle-pr-review/fetch-threads.sh"
me=$(gh api user --jq .login)

gh search prs --author @me --state open --draft=false --json repository,number,url --limit 100 \
  --jq '.[] | "\(.repository.nameWithOwner) \(.number) \(.url)"' |
while read -r repo n url; do
  if ! pending=$("$fetch" "$n" "$repo" | jq --arg me "$me" 'any(.[]; .comments[-1] | .author == $me or .bot)'); then
    echo "$url: couldn't fetch threads" >&2
    continue
  fi
  if [ "$pending" = "true" ]; then
    jq -n --arg repo "$repo" --argjson n "$n" --arg url "$url" '{repo: $repo, number: $n, url: $url}'
  fi
done | jq -s .
