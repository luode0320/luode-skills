#!/usr/bin/env bash
set -euo pipefail

TITLE="${1:-}"
COMPILE_TIMEOUT="${COMPILE_GATE_TIMEOUT:-600}"

# [参数] $@: 透传给 `git diff --cached --name-only` 的额外参数
# [返回] 输出保留中文路径原样的 staged 文件列表
# 最近修改时间: 2026-07-08 11:57:00 修复中文路径被 quotepath 转义后无法命中落点规则的问题
staged_name_only() {
  git -c core.quotepath=false diff --cached --name-only "$@"
}

# [参数] label: 编译步骤名称；其余参数: 待执行编译命令
# [返回] 0=命令通过；非 0=工具链缺失、编译失败或超时，由调用方转成阻断
# 最近修改时间: 2026-10-22 10:00:00 为代码项目编译闸门提供带超时的统一执行入口
run_compile_command() {
  local label="$1"
  shift
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "BLOCK: ${label} 缺少命令 $1，无法验证最基本编译" >&2
    return 1
  fi
  echo "COMPILE: ${label} -> $*"
  if command -v timeout >/dev/null 2>&1; then
    timeout "$COMPILE_TIMEOUT" "$@"
  else
    "$@"
  fi
}

# [参数] 无
# [返回] 0=staged Python 文件语法全部通过或无需检查；非 0=存在语法错误
# 最近修改时间: 2026-10-22 10:00:00 用 ast 解析只做语法编译检查，读取索引版本避免工作区与暂存区不一致时漏检
compile_python_staged() {
  local -a files=()
  local path
  while IFS= read -r path; do
    [[ -n "$path" ]] && files+=("$path")
  done < <(staged_name_only --diff-filter=AM | rg '\.py$' || true)

  if [[ ${#files[@]} -eq 0 ]]; then
    echo "N/A: 无 staged Python 文件"
    return 0
  fi

  local python_bin="python"
  command -v python >/dev/null 2>&1 || python_bin="python3"
  command -v "$python_bin" >/dev/null 2>&1 || {
    echo "BLOCK: Python 代码项目缺少 python 工具链，无法验证最基本编译" >&2
    return 1
  }

  echo "COMPILE: Python ast 语法检查 -> ${#files[@]} 个 staged 文件"
  # 每个文件单独从索引取原文，经 git cat-file 送入 ast.parse，全程不写字节码。
  for path in "${files[@]}"; do
    if ! git cat-file blob ":$path" | "$python_bin" -X utf8 -B -c 'import ast, sys
source = sys.stdin.read()
try:
    ast.parse(source, sys.argv[1])
except SyntaxError as error:
    sys.stderr.write(f"SYNTAX: {error}\n")
    sys.exit(1)' "$path"; then
      echo "BLOCK: staged Python 文件语法错误 -> $path" >&2
      return 1
    fi
  done
}

# [参数] 无
# [返回] 0=代码项目编译通过或当前不是代码项目；1=编译失败、超时或工具链缺失
# 最近修改时间: 2026-10-22 10:40:00 改为按仓库根标记驱动，并把 node 不可用判为阻断而非跳过
compile_gate() {
  local -a markers=()
  local -a tsc_cmd=()
  local marker

  # 1) 只认仓库根构建标记，不按文件扩展名猜测，避免文档仓库被误判成代码项目。
  [[ -f go.mod ]] && markers+=("go")
  [[ -f Cargo.toml ]] && markers+=("rust")
  [[ -f tsconfig.json ]] && markers+=("ts")
  [[ -f pyproject.toml || -f setup.py ]] && markers+=("python")
  if [[ ! -f tsconfig.json && -f package.json ]]; then
    local node_probe=""
    node_probe="$(node -e 'try{const s=require("./package.json").scripts||{};console.log(s.build?"BUILD":"NOBUILD")}catch(e){console.log("ERROR")}' 2>/dev/null)" || node_probe="ERROR"
    if [[ "$node_probe" == "ERROR" ]]; then
      echo "BLOCK: package.json 无法解析或 node 不可用，无法判定编译入口" >&2
      return 1
    fi
    [[ "$node_probe" == "BUILD" ]] && markers+=("node")
  fi
  if [[ ${#markers[@]} -eq 0 ]]; then
    echo "N/A: 未检测到代码项目标记，跳过最基本编译闸门"
    return 0
  fi

  # 2) TypeScript 只认本地已安装的 tsc；缺失直接阻断，禁止 npx 联网拉取同名包。
  if [[ -f tsconfig.json ]]; then
    if [[ -x node_modules/.bin/tsc ]]; then tsc_cmd=(node_modules/.bin/tsc)
    elif [[ -f node_modules/typescript/bin/tsc ]]; then tsc_cmd=(node node_modules/typescript/bin/tsc)
    else
      echo "BLOCK: TypeScript 项目缺少本地 tsc（请先安装依赖），无法验证最基本编译" >&2
      return 1
    fi
  fi

  # 3) 逐项执行全部命中入口，全部通过才放行。
  for marker in "${markers[@]}"; do
    case "$marker" in
      go) run_compile_command "go build ./..." go build ./... || return 1 ;;
      rust) run_compile_command "cargo check" cargo check --quiet || return 1 ;;
      ts) run_compile_command "tsc --noEmit" "${tsc_cmd[@]}" --noEmit -p tsconfig.json || return 1 ;;
      node) run_compile_command "npm run build" npm run --silent build || return 1 ;;
      python) compile_python_staged || return 1 ;;
    esac
  done

  echo "PASS: compile gate"
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

# 6) 代码项目最基本编译闸门：只要求能编译通过，不替代真实测试与功能验证
if ! compile_gate; then
  echo "BLOCK: baseline compile failed for code project" >&2
  exit 19
fi

# 7) 说明：提交粒度按业务目标划分，代码实现、可执行测试与流程文档可同笔提交；
#    本脚本不再做提交域隔离阻断，落点约束由第 4、5 步继续保护。

# 8) 盘点命令（供证据输出）
git status --short
git diff --cached --stat || true

echo "PASS: pre-commit gate"
