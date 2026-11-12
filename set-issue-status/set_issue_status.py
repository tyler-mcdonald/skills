#!/usr/bin/env python3
import json
import subprocess
import sys

QUERY = """
query($url: URI!, $cursor: String) {
  resource(url: $url) {
    ... on Issue {
      projectItems(first: 100, after: $cursor) {
        pageInfo { hasNextPage endCursor }
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
}
"""


def gh(*args):
    return subprocess.run(
        ["gh", *args], check=True, capture_output=True, text=True
    ).stdout


def project_items(url):
    items, cursor = [], None
    while True:
        args = ["api", "graphql", "-f", f"url={url}", "-f", f"query={QUERY}"]
        if cursor:
            args += ["-f", f"cursor={cursor}"]
        resource = json.loads(gh(*args))["data"]["resource"] or {}
        page = resource.get("projectItems") or {}
        items += page.get("nodes") or []
        info = page.get("pageInfo") or {}
        if not info.get("hasNextPage"):
            return items
        cursor = info["endCursor"]


def find_option(field, status):
    for option in (field or {}).get("options") or []:
        if option["name"].casefold() == status.casefold():
            return option
    return None


def set_issue_status(url, status):
    items = project_items(url)
    if not items:
        yield f"{url} is on no project boards."
        return
    for item in items:
        project = item["project"]
        option = find_option(project["field"], status)
        if option is None:
            yield f'{project["title"]}: skipped (no "{status}" option)'
            continue
        gh(
            "project",
            "item-edit",
            "--id",
            item["id"],
            "--project-id",
            project["id"],
            "--field-id",
            project["field"]["id"],
            "--single-select-option-id",
            option["id"],
        )
        yield f"{project['title']}: {option['name']}"


def main(argv):
    if len(argv) != 3:
        sys.exit('usage: set_issue_status.py <issue url> "<status>"')
    try:
        for line in set_issue_status(argv[1], argv[2]):
            print(line, flush=True)
    except subprocess.CalledProcessError as error:
        sys.stderr.write(error.stderr or "")
        sys.exit(error.returncode or 1)


if __name__ == "__main__":
    main(sys.argv)
