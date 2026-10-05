#!/usr/bin/env bash
set -euo pipefail

pr="$1"
trusted_authors_file="$(dirname "${BASH_SOURCE[0]}")/trusted-authors.txt"

trusted_ids="$(grep -oE '^[0-9]+' "$trusted_authors_file" | jq -s .)"

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
}' | jq --argjson trusted "$trusted_ids" '[.data.repository.pullRequest.reviewThreads.nodes[]
  | select(.isResolved | not)
  | .comments.nodes |= map(select(.author.databaseId | IN($trusted[])))
  | select(.comments.nodes | length > 0)
  | select(.comments.nodes[-1].body | contains("🤖 Posted by Claude Code") | not)
  | {path, line, comments: [.comments.nodes[] | {id: .databaseId, author: .author.login, body}]}]'
