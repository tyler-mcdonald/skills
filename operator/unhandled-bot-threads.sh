#!/usr/bin/env bash
set -euo pipefail

pr="$1"
bot="${2%\[bot\]}"
repo="${3:-}"

if [ -n "$repo" ]; then
  owner="${repo%/*}"
  name="${repo#*/}"
else
  owner='{owner}'
  name='{repo}'
fi

BOT="$bot" gh api graphql -F owner="$owner" -F repo="$name" -F pr="$pr" -f query='
query($owner: String!, $repo: String!, $pr: Int!) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $pr) {
      reviewThreads(first: 100) {
        nodes {
          isResolved
          path
          line
          comments(first: 100) {
            nodes { url author { login __typename } }
          }
        }
      }
    }
  }
}' --jq 'def by($login): .author.__typename == "Bot" and .author.login == $login;
  [.data.repository.pullRequest.reviewThreads.nodes[]
  | select(.isResolved | not)
  | select(.comments.nodes[0] | by($ENV.BOT))
  | select(any(.comments.nodes[]; by("claude")) | not)
  | {path, line, url: .comments.nodes[0].url}]'
