#!/usr/bin/env bash
set -euo pipefail

if [ $# -ne 2 ]; then
  echo "Usage: set-issue-status.sh <issue-url> <status>" >&2
  exit 1
fi

url=$1
status=$2

gh api graphql -f url="$url" -f query='
  query($url: URI!) {
    resource(url: $url) {
      ... on Issue {
        projectItems(first: 20) {
          nodes {
            id
            project {
              id
              title
              field(name: "Status") {
                ... on ProjectV2SingleSelectField { id options { id name } }
              }
            }
          }
        }
      }
    }
  }' |
  jq -r --arg status "$status" '
    .data.resource.projectItems.nodes[]?
    | . as $item
    | ($item.project.field.options // [])[]
    | select(.name == $status)
    | [$item.project.title, $item.id, $item.project.id, $item.project.field.id, .id] | @tsv' |
  while IFS=$'\t' read -r title item project field option; do
    gh project item-edit --id "$item" --project-id "$project" --field-id "$field" --single-select-option-id "$option" > /dev/null
    echo "$title: $status"
  done
