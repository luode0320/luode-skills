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
GITATTRIBUTES_FILE="$REPO_DIR/.gitattributes"
EDITORCONFIG_FILE="$REPO_DIR/.editorconfig"

TEMPLATE_CONTENT=$(cat <<'TEMPLATE'
# AGENTS.md

## 适用范围
- 本文件适用于本仓库下所有代码与文档变更。

## Skill 命中强制规则
- 处理本仓库任务时，必须先命中并加载至少两个基础 skill。
- 最低要求：至少命中 `skill-hit-check-rules`、`parallel-task-dispatch-rules`。
- 若本轮涉及创建、补齐或更新仓库级 `AGENTS.md`，默认额外启用 `project-agents-bootstrap` 进行自举补齐；该规则同样适用于其他项目仓库。
- 必须在首条中间进度明确输出当前命中的 skill 列表。
- 若连 `skill-hit-check-rules` 或 `parallel-task-dispatch-rules` 任一都未命中，视为上下文丢失严重、当前基础规则没有正确加载；此时禁止直接进入主任务，必须先补做 skill 命中检查与上下文重同步。
- 若本轮任务存在多 skill 组合、并行拆分或规则收口风险，默认应额外启用 `skill-audit-rules` 进行只读审计。
- 所有审查类 skill 统一按强制自动触发处理；只要是只读检查、规则核对、实现自审、归位审查或回归风险审查，默认优先并行。

## 上下文压缩续做规则
- 若当前会话刚发生“压缩上下文 / 自动压缩上下文 / 上下文太多”后的重组，默认强制命中 `context-compression-rules`。
- 压缩后继续执行前，必须重新读取当前项目根目录 `AGENTS.md`，恢复仓库级硬规则、必命中 skill 和阻断条件。
- 若压缩后未重新读取 `AGENTS.md`，禁止直接进入任何需求、Bug、编码、测试或交付主任务。
- 若压缩后发现 `AGENTS.md` 缺失、损坏或规则不完整，必须先触发 `project-agents-bootstrap` 补齐，再继续主任务。

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

## Windows / WSL 执行规则
- Windows 下默认优先使用 Git Bash 或 WSL shell。
- 尽量不要用 Windows PowerShell 直接写入、格式化或批量修改仓库文件，避免换行和编码漂移。
- 若确需在 Windows 侧执行命令，优先只读检查；写入前必须显式指定 UTF-8，并在落盘后立即 `git diff` 核对仅有预期改动。
- 仓库应提交 `.gitattributes` 与 `.editorconfig`，显式固定 `LF`、`UTF-8`、末尾换行和基础编辑器行为。
- Windows 下若仓库出现 `.sh` 仅 `100755 => 100644` 之类伪改动，应优先关闭 `core.filemode` 并清理 mode change。
- Windows 下若仓库出现大量无关文件被带进改动，应优先检查 `core.autocrlf` 并通过 `.gitattributes` 固定换行策略。
TEMPLATE
)

GITATTRIBUTES_CONTENT=$(cat <<'TEMPLATE'
* text=auto

*.sh text eol=lf
*.bash text eol=lf

*.png binary
*.jpg binary
*.jpeg binary
*.gif binary
*.webp binary
*.ico binary
*.pdf binary
*.zip binary
*.gz binary
TEMPLATE
)

EDITORCONFIG_CONTENT=$(cat <<'TEMPLATE'
root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
indent_style = space
indent_size = 2
trim_trailing_whitespace = true

[*.go]
indent_style = tab
indent_size = 4

[*.md]
trim_trailing_whitespace = false
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
fi

if [[ ! -f "$GITATTRIBUTES_FILE" ]]; then
  printf "%s\n" "$GITATTRIBUTES_CONTENT" > "$GITATTRIBUTES_FILE"
  echo "[OK] 已创建: $GITATTRIBUTES_FILE"
fi

if [[ ! -f "$EDITORCONFIG_FILE" ]]; then
  printf "%s\n" "$EDITORCONFIG_CONTENT" > "$EDITORCONFIG_FILE"
  echo "[OK] 已创建: $EDITORCONFIG_FILE"
fi

# 已存在则做增量补齐，不覆盖已有内容
append_section_if_missing "$AGENTS_FILE" "适用范围" "- 本文件适用于本仓库下所有代码与文档变更。"

append_section_if_missing "$AGENTS_FILE" "Skill 命中强制规则" "- 处理本仓库任务时，必须先命中并加载至少一个项目内 skill。
- 最低要求：至少命中 \`skill-hit-check-rules\`、\`parallel-task-dispatch-rules\`。
- 若本轮涉及创建、补齐或更新仓库级 \`AGENTS.md\`，默认额外启用 \`project-agents-bootstrap\` 进行自举补齐；该规则同样适用于其他项目仓库。
- 必须在首条中间进度明确输出当前命中的 skill 列表。
- 若连 \`skill-hit-check-rules\` 或 \`parallel-task-dispatch-rules\` 任一都未命中，视为上下文丢失严重、当前基础规则没有正确加载；此时禁止直接进入主任务，必须先补做 skill 命中检查与上下文重同步。
- 若本轮任务存在多 skill 组合、并行拆分或规则收口风险，默认应额外启用 \`skill-audit-rules\` 进行只读审计。
- 所有审查类 skill 统一按强制自动触发处理；只要是只读检查、规则核对、实现自审、归位审查或回归风险审查，默认优先并行。"

append_section_if_missing "$AGENTS_FILE" "上下文压缩续做规则" "- 若当前会话刚发生“压缩上下文 / 自动压缩上下文 / 上下文太多”后的重组，默认强制命中 \`context-compression-rules\`。
- 压缩后继续执行前，必须重新读取当前项目根目录 \`AGENTS.md\`，恢复仓库级硬规则、必命中 skill 和阻断条件。
- 若压缩后未重新读取 \`AGENTS.md\`，禁止直接进入任何需求、Bug、编码、测试或交付主任务。
- 若压缩后发现 \`AGENTS.md\` 缺失、损坏或规则不完整，必须先触发 \`project-agents-bootstrap\` 补齐，再继续主任务。"

append_section_if_missing "$AGENTS_FILE" "注释任务强制流程" "- 触发词：补充注释 / 注意中文编码 / 只补注释 / 注释完善 / 加注释。
- 第一步：先声明命中的注释类 skill。
- 第二步：读取对应 \`SKILL.md\` 后再改代码。
- 第三步：最终回复给执行证据：改动点、UTF-8、格式化/编译/测试结果。"

append_section_if_missing "$AGENTS_FILE" "中文编码规则" "- 新增或修改注释默认使用中文。
- 文件编码保持 UTF-8，禁止乱码。"

append_section_if_missing "$AGENTS_FILE" "变更最小化" "- 注释补充不改变业务逻辑。"

append_section_if_missing "$AGENTS_FILE" "Windows / WSL 执行规则" "- Windows 下默认优先使用 Git Bash 或 WSL shell。
- 尽量不要用 Windows PowerShell 直接写入、格式化或批量修改仓库文件，避免换行和编码漂移。
- 若确需在 Windows 侧执行命令，优先只读检查；写入前必须显式指定 UTF-8，并在落盘后立即 \`git diff\` 核对仅有预期改动。
- 仓库应提交 \`.gitattributes\` 与 \`.editorconfig\`，显式固定 \`LF\`、\`UTF-8\`、末尾换行和基础编辑器行为。
- Windows 下若仓库出现 \`.sh\` 仅 \`100755 => 100644\` 之类伪改动，应优先关闭 \`core.filemode\` 并清理 mode change。
- Windows 下若仓库出现大量无关文件被带进改动，应优先检查 \`core.autocrlf\` 并通过 \`.gitattributes\` 固定换行策略。"

echo "[OK] 已检查并补齐: $AGENTS_FILE"
