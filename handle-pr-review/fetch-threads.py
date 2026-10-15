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
    # gh fills in {owner}/{repo} from the current checkout when no repo is given.
    owner, name = repo.split("/", 1) if repo else ("{owner}", "{repo}")
    cmd = [
        "gh", "api", "graphql",
        "-F", f"owner={owner}",
        "-F", f"repo={name}",
        "-F", f"pr={pr}",
        "-f", f"query={QUERY}",
    ]
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    data = json.loads(result.stdout)["data"]
    return data["repository"]["pullRequest"]["reviewThreads"]["nodes"]


def format_comment(comment):
    # Deleted accounts come back as a null author.
    author = comment["author"] or {}
    return {
        "id": comment["databaseId"],
        "author": author.get("login"),
        "bot": is_bot(author) and not is_claude(author),
        "body": comment["body"],
    }


def format_thread(thread, last):
    return {
        "path": thread["path"],
        "line": thread["line"],
        "last": {"author": last.get("login"), "bot": is_bot(last)},
        "comments": [format_comment(c) for c in thread["comments"]["nodes"]],
    }


def threads_to_handle(threads):
    for thread in threads:
        if thread["isResolved"]:
            continue
        last = thread["lastComment"]["nodes"][0]["author"] or {}
        if is_claude(last):
            continue
        yield format_thread(thread, last)


if __name__ == "__main__":
    pr = sys.argv[1]
    repo = sys.argv[2] if len(sys.argv) > 2 else ""
    json.dump(list(threads_to_handle(fetch(pr, repo))), sys.stdout)
    print()
