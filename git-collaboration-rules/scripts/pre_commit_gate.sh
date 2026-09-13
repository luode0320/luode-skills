#!/usr/bin/env bash
set -euo pipefail

TITLE="${1:-}"

# [参数] $@: 透传给 `git diff --cached --name-only` 的额外参数
# [返回] 输出保留中文路径原样的 staged 文件列表
# 最近修改时间: 2026-07-08 11:57:00 修复中文路径被 quotepath 转义后无法命中落点规则的问题
staged_name_only() {
  git -c core.quotepath=false diff --cached --name-only "$@"
}

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

# 2) 基础格式底线：只检查 staged diff 的空白错误；项目专用格式化检查由 skill 的基础代码核查执行
if ! git diff --cached --check; then
  echo "BLOCK: staged diff has whitespace errors" >&2
  exit 18
fi

# 3) README 必须在改动日志末尾追加本次标题日志
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

# 4) Go 测试文件位置扫描：只检查本次提交涉及的新增/修改 *_test.go
if staged_name_only --diff-filter=AM | rg '_test\.go$' | rg -v '^test/' >/dev/null; then
  echo "BLOCK: staged *_test.go must be under root test/" >&2
  staged_name_only --diff-filter=AM | rg '_test\.go$' | rg -v '^test/' >&2 || true
  exit 15
fi

# 5) staged 禁放扫描：internal/service/*.go 根目录直落
if staged_name_only | rg '^internal/service/[^/]+\.go$' >/dev/null; then
  echo "BLOCK: staged file in internal/service/*.go root" >&2
  staged_name_only | rg '^internal/service/[^/]+\.go$' >&2 || true
  exit 16
fi

# 6) 说明：提交粒度按业务目标划分，代码实现、可执行测试与流程文档可同笔提交；
#    本脚本不再做提交域隔离阻断，落点约束由第 4、5 步继续保护。

# 7) 盘点命令（供证据输出）
git status --short
git diff --cached --stat || true

echo "PASS: pre-commit gate"
