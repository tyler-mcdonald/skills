#!/usr/bin/env python3
import json
import subprocess
import sys

QUERY = """
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
            nodes { author { login __typename } }
          }
        }
      }
    }
  }
}
"""


def is_bot(author):
    return author.get("__typename") == "Bot"


def is_claude(author):
    return is_bot(author) and author.get("login") == "claude"


def fetch(pr, repo):
    owner, name = repo.split("/", 1) if repo else ("{owner}", "{repo}")
    out = subprocess.run(
        ["gh", "api", "graphql", "-F", f"owner={owner}", "-F", f"repo={name}", "-F", f"pr={pr}", "-f", f"query={QUERY}"],
        check=True, capture_output=True, text=True,
    ).stdout
    return json.loads(out)["data"]["repository"]["pullRequest"]["reviewThreads"]["nodes"]


def threads_to_handle(threads):
    for t in threads:
        if t["isResolved"]:
            continue
        last = t["lastComment"]["nodes"][0]["author"] or {}
        if is_claude(last):
            continue
        yield {
            "path": t["path"],
            "line": t["line"],
            "last": {"author": last.get("login"), "bot": is_bot(last)},
            "comments": [
                {
                    "id": c["databaseId"],
                    "author": (c["author"] or {}).get("login"),
                    "bot": is_bot(c["author"] or {}) and not is_claude(c["author"] or {}),
                    "body": c["body"],
                }
                for c in t["comments"]["nodes"]
            ],
        }


if __name__ == "__main__":
    pr = sys.argv[1]
    repo = sys.argv[2] if len(sys.argv) > 2 else ""
    json.dump(list(threads_to_handle(fetch(pr, repo))), sys.stdout)
    print()
