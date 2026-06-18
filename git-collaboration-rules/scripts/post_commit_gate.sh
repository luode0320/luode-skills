#!/usr/bin/env bash
set -euo pipefail

TITLE_REGEX='^(feat|fix|refactor|style|docs|test|chore|perf|build|ci|revert): \[[^]]*[一-龥][^]]*\] .+'

subject="$(git log -1 --pretty=%s)"
body="$(git log -1 --pretty=%B)"

if ! printf '%s\n' "$subject" | rg -P "$TITLE_REGEX" >/dev/null; then
  echo "BLOCK: latest subject invalid" >&2
  echo "$subject" >&2
  exit 21
fi

if printf '%s\n' "$body" | rg '\\n' >/dev/null; then
  echo "BLOCK: literal \\n found in commit body" >&2
  exit 22
fi

echo "PASS: post-commit gate"
git log -1 --pretty=%B
git log -1 --pretty=%s
