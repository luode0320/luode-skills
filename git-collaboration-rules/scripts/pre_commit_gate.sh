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

# 2) README 必须在改动日志末尾追加本次标题日志
if [[ ! -f README.md ]]; then
  echo "BLOCK: README.md not found at repo root" >&2
  exit 13
fi
LAST_LOG_LINE="$(awk '
  BEGIN { in_section=0; last="" }
  /^##[[:space:]]+改动日志[[:space:]]*$/ { in_section=1; next }
  /^##[[:space:]]+/ && in_section { in_section=0 }
  in_section {
    line=$0
    gsub(/\r$/, "", line)
    if (line ~ /^[[:space:]]*$/) next
    last=line
  }
  END { print last }
' README.md)"
if [[ -z "$LAST_LOG_LINE" ]]; then
  echo "BLOCK: README.md change log section missing or empty" >&2
  exit 14
fi
# Strip timestamp prefix if present (yyyy-MM-dd HH:mm:ss followed by space)
LOG_TITLE="$LAST_LOG_LINE"
if [[ "$LAST_LOG_LINE" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}\ [0-9]{2}:[0-9]{2}:[0-9]{2}\ (.+)$ ]]; then
  LOG_TITLE="${BASH_REMATCH[1]}"
fi
if [[ "$LOG_TITLE" != "$TITLE" ]]; then
  echo "BLOCK: README.md last change log entry (title part) does not match this title" >&2
  echo "EXPECT_LAST: $TITLE" >&2
  echo "ACTUAL_LAST: $LOG_TITLE (raw: $LAST_LOG_LINE)" >&2
  exit 14
fi

# 3) Go 测试文件位置扫描：只检查本次提交涉及的新增/修改 *_test.go
if git diff --cached --name-only --diff-filter=AM | rg '_test\.go$' | rg -v '^doc/5-tests/' >/dev/null; then
  echo "BLOCK: staged *_test.go outside doc/5-tests/" >&2
  git diff --cached --name-only --diff-filter=AM | rg '_test\.go$' | rg -v '^doc/5-tests/' >&2 || true
  exit 15
fi

# 4) staged 禁放扫描：internal/service/*.go 根目录直落
if git diff --cached --name-only | rg '^internal/service/[^/]+\.go$' >/dev/null; then
  echo "BLOCK: staged file in internal/service/*.go root" >&2
  git diff --cached --name-only | rg '^internal/service/[^/]+\.go$' >&2 || true
  exit 16
fi

# 5) 审查文档闸门：检查 doc/6-审查/ 下最近一份审查文档
REVIEW_DIR="doc/6-审查"
if [[ ! -d "$REVIEW_DIR" ]]; then
  echo "BLOCK: review directory $REVIEW_DIR not found" >&2
  exit 17
fi
LATEST_REVIEW=$(ls -1 "$REVIEW_DIR"/[0-9]*.md 2>/dev/null | sort -r | head -1)
if [[ -z "$LATEST_REVIEW" ]]; then
  echo "BLOCK: no review document found in $REVIEW_DIR" >&2
  exit 17
fi
REVIEW_CONTENT=$(cat "$LATEST_REVIEW")
if ! printf '%s\n' "$REVIEW_CONTENT" | rg -P '审查结论:\s*通过' >/dev/null; then
  echo "BLOCK: review document conclusion is not 通过" >&2
  echo "REVIEW_FILE: $LATEST_REVIEW" >&2
  exit 17
fi
if ! printf '%s\n' "$REVIEW_CONTENT" | rg -P '是否允许提交:\s*是' >/dev/null; then
  echo "BLOCK: review document does not allow commit" >&2
  echo "REVIEW_FILE: $LATEST_REVIEW" >&2
  exit 17
fi
if printf '%s\n' "$REVIEW_CONTENT" | rg -P '阻断问题:' | rg -iP '\[P[01]\]' >/dev/null; then
  echo "BLOCK: review document has unresolved P0/P1" >&2
  echo "REVIEW_FILE: $LATEST_REVIEW" >&2
  exit 17
fi
echo "REVIEW_PASS: $LATEST_REVIEW"

# 6) 盘点命令（供证据输出）
git status --short
git diff --cached --stat || true

echo "PASS: pre-commit gate"
