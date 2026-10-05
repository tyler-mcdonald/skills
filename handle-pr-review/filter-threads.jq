[.data.repository.pullRequest.reviewThreads.nodes[]
  | select(.isResolved | not)
  | select(.comments.nodes[0].author.databaseId | IN($trusted[]))
  | .comments.nodes |= map(select(.author.databaseId | IN($trusted[])))
  | select(.comments.nodes[-1].body | contains("🤖 Posted by Claude Code") | not)
  | {path, line, comments: [.comments.nodes[] | {id: .databaseId, author: .author.login, body}]}]
