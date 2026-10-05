#!/usr/bin/env bash
set -euo pipefail

pr="$1"
skill_dir="$(dirname "${BASH_SOURCE[0]}")"

trusted_ids="$(grep -oE '^[0-9]+' "$skill_dir/trusted-authors.txt" | paste -sd, -)"
filter="[$trusted_ids] as \$trusted | $(cat "$skill_dir/filter-threads.jq")"

gh api graphql -F owner='{owner}' -F repo='{repo}' -F pr="$pr" -f query='
query($owner: String!, $repo: String!, $pr: Int!) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $pr) {
      reviewThreads(first: 100) {
        nodes {
          isResolved
          path
          line
          comments(first: 50) {
            nodes {
              databaseId
              author {
                login
                ... on User { databaseId }
                ... on Bot { databaseId }
              }
              body
            }
          }
        }
      }
    }
  }
}' --jq "$filter"
