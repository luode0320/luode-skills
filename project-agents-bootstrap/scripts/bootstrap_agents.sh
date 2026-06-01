#!/usr/bin/env bash
set -euo pipefail

# project-agents-bootstrap: 检查并补齐仓库根目录 AGENTS.md
# 用法:
#   bootstrap_agents.sh
#   bootstrap_agents.sh --repo /path/to/repo

REPO_DIR="$(pwd)"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo)
      if [[ $# -lt 2 ]]; then
        echo "[ERROR] --repo 需要一个目录参数" >&2
        exit 1
      fi
      REPO_DIR="$2"
      shift 2
      ;;
    -h|--help)
      echo "Usage: $0 [--repo /path/to/repo]"
      exit 0
      ;;
    *)
      echo "[ERROR] 未知参数: $1" >&2
      echo "Usage: $0 [--repo /path/to/repo]" >&2
      exit 1
      ;;
  esac
done

if [[ ! -d "$REPO_DIR" ]]; then
  echo "[ERROR] 仓库目录不存在: $REPO_DIR" >&2
  exit 1
fi

AGENTS_FILE="$REPO_DIR/AGENTS.md"

TEMPLATE_CONTENT=$(cat <<'TEMPLATE'
# AGENTS.md

## 适用范围
- 本文件适用于本仓库下所有代码与文档变更。

## 注释任务强制流程
- 触发词：补充注释 / 注意中文编码 / 只补注释 / 注释完善 / 加注释。
- 第一步：先声明命中的注释类 skill。
- 第二步：读取对应 `SKILL.md` 后再改代码。
- 第三步：最终回复给执行证据：改动点、UTF-8、格式化/编译/测试结果。

## 中文编码规则
- 新增或修改注释默认使用中文。
- 文件编码保持 UTF-8，禁止乱码。

## 变更最小化
- 注释补充不改变业务逻辑。
TEMPLATE
)

append_section_if_missing() {
  local file="$1"
  local header="$2"
  local body="$3"

  if rg -q "^## ${header}$" "$file"; then
    return 0
  fi

  {
    echo
    echo "## ${header}"
    echo "$body"
  } >> "$file"

  echo "[INFO] 已补充章节: ${header}"
}

if [[ ! -f "$AGENTS_FILE" ]]; then
  printf "%s\n" "$TEMPLATE_CONTENT" > "$AGENTS_FILE"
  echo "[OK] 已创建: $AGENTS_FILE"
  exit 0
fi

# 已存在则做增量补齐，不覆盖已有内容
append_section_if_missing "$AGENTS_FILE" "适用范围" "- 本文件适用于本仓库下所有代码与文档变更。"

append_section_if_missing "$AGENTS_FILE" "注释任务强制流程" "- 触发词：补充注释 / 注意中文编码 / 只补注释 / 注释完善 / 加注释。
- 第一步：先声明命中的注释类 skill。
- 第二步：读取对应 \`SKILL.md\` 后再改代码。
- 第三步：最终回复给执行证据：改动点、UTF-8、格式化/编译/测试结果。"

append_section_if_missing "$AGENTS_FILE" "中文编码规则" "- 新增或修改注释默认使用中文。
- 文件编码保持 UTF-8，禁止乱码。"

append_section_if_missing "$AGENTS_FILE" "变更最小化" "- 注释补充不改变业务逻辑。"

echo "[OK] 已检查并补齐: $AGENTS_FILE"
