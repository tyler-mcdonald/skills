#!/usr/bin/env bash
set -euo pipefail

pr="$1"

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
            nodes { databaseId author { login } body }
          }
        }
      }
    }
  }
}' --jq '[.data.repository.pullRequest.reviewThreads.nodes[]
  | select(.isResolved | not)
  | select(.comments.nodes[-1].body | contains("🤖 Posted by Claude Code") | not)
  | {path, line, comments: [.comments.nodes[] | {id: .databaseId, author: .author.login, body}]}]'
