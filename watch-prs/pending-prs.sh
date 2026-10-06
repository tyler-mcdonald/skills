#!/usr/bin/env bash
set -euo pipefail

fetch="$(dirname "$0")/../handle-pr-review/fetch-threads.sh"
projects="${WATCH_PRS_PROJECTS_DIR:-$HOME/Projects}"
me=$(gh api user --jq .login)

emit() {
  jq -n --arg repo "$repo" --argjson n "$n" --arg url "$url" --arg status "$1" \
    '{repo: $repo, number: $n, url: $url, status: $status}'
}

gh search prs --author @me --state open --draft=false --json repository,number,url --limit 1000 \
  --jq '.[] | "\(.repository.nameWithOwner) \(.number) \(.url)"' |
while read -r repo n url; do
  lock="$projects/${repo#*/}/.claude/worktrees/pr-$n.lock"
  if [ -n "$(find "$lock" -mmin -30 2>/dev/null)" ]; then
    emit "In Progress"
    continue
  fi
  if ! pending=$("$fetch" "$n" "$repo" | jq --arg me "$me" 'any(.[]; .last | .author == $me or .bot)'); then
    emit "Error"
    continue
  fi
  [ "$pending" = "true" ] || continue
  if ! review=$(gh api --paginate "repos/$repo/pulls/$n/reviews" \
    --jq ".[] | select(.state == \"PENDING\" and .user.login == \"$me\") | .id"); then
    emit "Error"
  elif [ -n "$review" ]; then
    emit "User Input Pending"
  else
    emit "Ready"
  fi
done | jq -s .
