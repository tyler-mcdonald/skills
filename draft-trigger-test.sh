#!/usr/bin/env bash
set -euo pipefail

pr="$1"

gh pr view $pr --json isDraft --jq .isDraft
