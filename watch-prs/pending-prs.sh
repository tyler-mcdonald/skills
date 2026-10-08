#!/usr/bin/env bash
set -euo pipefail

fetch_threads="$(dirname "$0")/../handle-pr-review/fetch-threads.sh"
projects="${WATCH_PRS_PROJECTS_DIR:-$HOME/Projects}"
lock_ttl_minutes=30
me=$(gh api user --jq .login)

open_prs() {
  gh search prs --author @me --state open --json repository,number,url --limit 1000 \
    --jq '.[] | "\(.repository.nameWithOwner) \(.number) \(.url)"'
}

lock_is_held() {
  local lock=$1
  [ -n "$(find "$lock" -maxdepth 0 -mmin "-$lock_ttl_minutes" 2>/dev/null)" ]
}

has_threads_to_handle() {
  local repo=$1 n=$2
  "$fetch_threads" "$n" "$repo" | jq --arg me "$me" 'any(.[]; .last | .author == $me or .bot)'
}

pending_review_ids() {
  local repo=$1 n=$2
  gh api --paginate "repos/$repo/pulls/$n/reviews" \
    --jq ".[] | select(.state == \"PENDING\" and .user.login == \"$me\") | .id"
}

pr_status() {
  local repo=$1 n=$2 lock=$3 has_threads review_ids

  if lock_is_held "$lock"; then
    echo "In Progress"
    return
  fi
  rm -rf "$lock"

  has_threads=$(has_threads_to_handle "$repo" "$n") || { echo "Error"; return; }
  [ "$has_threads" = "true" ] || return 0

  review_ids=$(pending_review_ids "$repo" "$n") || { echo "Error"; return; }
  if [ -n "$review_ids" ]; then
    echo "User Input Pending"
  else
    echo "Ready"
  fi
}

open_prs | while read -r repo n url; do
  dir="$projects/${repo#*/}"
  lock="$dir/.claude/worktrees/pr-$n.lock"
  status=$(pr_status "$repo" "$n" "$lock")
  [ -n "$status" ] || continue
  jq -n --arg repo "$repo" --argjson n "$n" --arg url "$url" --arg dir "$dir" --arg lock "$lock" --arg status "$status" \
    '{repo: $repo, number: $n, url: $url, dir: $dir, lock: $lock, status: $status}'
done | jq -s .
