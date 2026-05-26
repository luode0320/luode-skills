#!/usr/bin/env bash
set -euo pipefail

TITLE="${1:-}"

if [[ -z "$TITLE" ]]; then
  echo "BLOCK: missing commit title" >&2
  exit 11
fi

# 1) 标题闸门
TITLE_REGEX='^(feat|fix|refactor|style|docs|test|chore|perf|build|ci|revert): \[[^]]*[一-龥][^]]*\] .+'
if ! printf '%s\n' "$TITLE" | rg -P "$TITLE_REGEX" >/dev/null; then
  echo "BLOCK: invalid title format" >&2
  echo "EXPECT: <type>: [中文简要说明] 标题说明" >&2
  exit 12
fi

# 2) README 必须包含本次标题日志（时间正序由人工插入点保证）
if [[ ! -f README.md ]]; then
  echo "BLOCK: README.md not found at repo root" >&2
  exit 13
fi
if ! rg -n --fixed-strings "$TITLE" README.md >/dev/null; then
  echo "BLOCK: README.md missing change log entry for this title" >&2
  exit 14
fi

# 3) Go 禁放扫描：test/ 外 *_test.go
if rg --files -g '*_test.go' | rg -v '^test/' >/dev/null; then
  echo "BLOCK: found *_test.go outside test/" >&2
  rg --files -g '*_test.go' | rg -v '^test/' >&2 || true
  exit 15
fi

# 4) staged 禁放扫描：internal/service/*.go 根目录直落
if git diff --cached --name-only | rg '^internal/service/[^/]+\.go$' >/dev/null; then
  echo "BLOCK: staged file in internal/service/*.go root" >&2
  git diff --cached --name-only | rg '^internal/service/[^/]+\.go$' >&2 || true
  exit 16
fi

# 5) 盘点命令（供证据输出）
git status --short
git diff --cached --stat || true

echo "PASS: pre-commit gate"
