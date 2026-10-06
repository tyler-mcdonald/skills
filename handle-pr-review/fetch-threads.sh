#!/usr/bin/env bash
set -euo pipefail

pr="$1"
repo="${2:-}"

if [ -n "$repo" ]; then
  owner="${repo%/*}"
  name="${repo#*/}"
else
  owner='{owner}'
  name='{repo}'
fi

gh api graphql -F owner="$owner" -F repo="$name" -F pr="$pr" -f query='
query($owner: String!, $repo: String!, $pr: Int!) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $pr) {
      reviewThreads(first: 100) {
        nodes {
          isResolved
          path
          line
          comments(first: 50) {
            nodes { databaseId author { login __typename } body }
          }
          lastComment: comments(last: 1) {
            nodes { body author { login __typename } }
          }
        }
      }
    }
  }
}' --jq '[.data.repository.pullRequest.reviewThreads.nodes[]
  | select(.isResolved | not)
  | select(.lastComment.nodes[0].body | contains("🤖 Posted by Claude Code") | not)
  | .lastComment.nodes[0] as $last
  | {path, line, last: {author: $last.author.login, bot: ($last.author.__typename == "Bot")}, comments: [.comments.nodes[] | {id: .databaseId, author: .author.login, bot: (.author.__typename == "Bot"), body}]}]'
