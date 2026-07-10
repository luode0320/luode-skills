#!/usr/bin/env bash
set -euo pipefail

TITLE="${1:-}"

# [参数] $1: 内部提交域标识
# [返回] 输出对应的中文域名，未知时回退原始标识
# 最近修改时间: 2026-07-08 11:57:00 为提交域隔离门禁补充可读的错误输出标签
domain_label() {
  case "${1:-}" in
    requirement) printf '需求' ;;
    implementation_doc) printf '实施' ;;
    bug) printf 'Bug' ;;
    test) printf '测试' ;;
    review) printf '审查' ;;
    acceptance) printf '验收' ;;
    implementation) printf '代码实现/运行配置' ;;
    *) printf '%s' "${1:-unknown}" ;;
  esac
}

# [参数] $1: staged 文件路径
# [返回] 输出该文件所属的提交流程域；README.md 返回空值以跳过域判定
# 最近修改时间: 2026-07-08 11:57:00 新增提交流程域分类，阻断代码实现与文档/测试混提
classify_commit_domain() {
  local path="${1:-}"
  case "$path" in
    README.md) printf '\n'; return 0 ;;
    doc/2-需求/*) printf 'requirement\n'; return 0 ;;
    doc/3-实施/*) printf 'implementation_doc\n'; return 0 ;;
    doc/4-bugs/*) printf 'bug\n'; return 0 ;;
    doc/5-tests/*) printf 'test\n'; return 0 ;;
    doc/6-审查/*) printf 'review\n'; return 0 ;;
    doc/7-验收/*) printf 'acceptance\n'; return 0 ;;
  esac

  case "$path" in
    *_test.*|*.spec.*|*.test.*) printf 'test\n'; return 0 ;;
  esac

  printf 'implementation\n'
}

# [参数] $@: 需要回显的域标识列表
# [返回] 将每个域对应的 staged 文件清单输出到标准错误
# 最近修改时间: 2026-07-08 11:57:00 新增阻断时的域明细输出，方便人工快速拆分提交
print_domain_details() {
  local domain
  for domain in "$@"; do
    [[ -z "$domain" ]] && continue
    echo "DOMAIN[$(domain_label "$domain")]" >&2
    printf '%s' "${DOMAIN_FILES[$domain]:-}" >&2
  done
}

# [参数] $@: 透传给 `git diff --cached --name-only` 的额外参数
# [返回] 输出保留中文路径原样的 staged 文件列表
# 最近修改时间: 2026-07-08 11:57:00 修复中文路径被 quotepath 转义后无法命中提交域规则的问题
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
if staged_name_only --diff-filter=AM | rg '_test\.go$' | rg -v '^doc/5-tests/' >/dev/null; then
  echo "BLOCK: staged *_test.go outside doc/5-tests/" >&2
  staged_name_only --diff-filter=AM | rg '_test\.go$' | rg -v '^doc/5-tests/' >&2 || true
  exit 15
fi

# 5) staged 禁放扫描：internal/service/*.go 根目录直落
if staged_name_only | rg '^internal/service/[^/]+\.go$' >/dev/null; then
  echo "BLOCK: staged file in internal/service/*.go root" >&2
  staged_name_only | rg '^internal/service/[^/]+\.go$' >&2 || true
  exit 16
fi

# 6) staged 提交域隔离扫描：流程文档域、测试域与代码实现域分开提交
declare -A DOMAIN_FILES=()
declare -A DOMAIN_SEEN=()
ARTIFACT_DOMAINS=()
HAS_IMPLEMENTATION=0
while IFS= read -r staged_path; do
  [[ -z "$staged_path" ]] && continue
  domain="$(classify_commit_domain "$staged_path")"
  [[ -z "$domain" ]] && continue
  DOMAIN_FILES["$domain"]+="$staged_path"$'\n'
  if [[ -z "${DOMAIN_SEEN[$domain]:-}" ]]; then
    DOMAIN_SEEN["$domain"]=1
    if [[ "$domain" == "implementation" ]]; then
      HAS_IMPLEMENTATION=1
    else
      ARTIFACT_DOMAINS+=("$domain")
    fi
  fi
done < <(staged_name_only)

if (( HAS_IMPLEMENTATION )) && ((${#ARTIFACT_DOMAINS[@]} > 0)); then
  echo "BLOCK: staged implementation files mixed with doc/test commit domains" >&2
  print_domain_details implementation "${ARTIFACT_DOMAINS[@]}"
  exit 17
fi

if ((${#ARTIFACT_DOMAINS[@]} > 1)); then
  echo "BLOCK: staged files span multiple doc/test commit domains" >&2
  print_domain_details "${ARTIFACT_DOMAINS[@]}"
  exit 17
fi

# 7) 盘点命令（供证据输出）
git status --short
git diff --cached --stat || true

echo "PASS: pre-commit gate"
