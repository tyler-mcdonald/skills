---
name: set-issue-status
description: Set a GitHub issue's Status on every project board it's in (e.g. "In review"). Use when asked to move an issue to a status or lane.
---

# Set Issue Status

1. List the boards the issue is on, with each board's Status options:

   ```sh
   gh api graphql -f url="<issue url>" -f query='
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
     }'
   ```

2. For each board that has the status as an option, set it:

   ```sh
   gh project item-edit --id <item id> --project-id <project id> --field-id <field id> --single-select-option-id <option id>
   ```
