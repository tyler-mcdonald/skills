#!/usr/bin/env bash
set -euo pipefail

pr="$1"
bot="$2"
sha="$3"
since="$4"
deadline=$(( $(date +%s) + 20 * 60 ))

while :; do
  reviewed=$(gh api "repos/{owner}/{repo}/pulls/$pr/reviews" --paginate \
    --jq "[.[] | select(.user.login == \"$bot\" and .commit_id == \"$sha\" and .submitted_at >= \"$since\")] | length" \
    | awk '{s += $1} END {print s + 0}')
  status=$(gh api "repos/{owner}/{repo}/commits/$sha/statuses" \
    --jq "[.[] | select(.creator.login == \"$bot\" and .state == \"success\" and .updated_at >= \"$since\" and ((.description // \"\") | test(\"skipped\"; \"i\") | not))] | length")

  if [ "$reviewed" -gt 0 ] || [ "$status" -gt 0 ]; then
    gh api "repos/{owner}/{repo}/pulls/$pr/comments" --paginate \
      --jq "[.[] | select(.user.login == \"$bot\" and .in_reply_to_id == null and .created_at >= \"$since\")] | length" \
      | awk '{s += $1} END {print s + 0}'
    exit 0
  fi

  if [ "$(date +%s)" -ge "$deadline" ]; then
    echo "timeout" >&2
    exit 1
  fi
  sleep 30
done
