#!/usr/bin/env bash
set -euo pipefail

# project-agents-bootstrap: 检查并补齐仓库内已存在的 AGENTS.md
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

PYTHON_BIN=""

resolve_python() {
  if command -v python3 >/dev/null 2>&1; then
    PYTHON_BIN="$(command -v python3)"
    return 0
  fi

  if command -v python >/dev/null 2>&1; then
    PYTHON_BIN="$(command -v python)"
    return 0
  fi

  if command -v py >/dev/null 2>&1; then
    PYTHON_BIN="$(command -v py) -3"
    return 0
  fi

  echo "[ERROR] 未找到可用 Python 解释器（python3 / python / py -3）" >&2
  exit 1
}

is_godot_project() {
  if [[ -f "$REPO_DIR/project.godot" ]]; then
    return 0
  fi

  if find "$REPO_DIR" -maxdepth 3 -type f \
    \( -name "*.gd" -o -name "*.tscn" -o -name "*.scn" -o -name "*.tres" -o -name "*.res" -o -name "export_presets.cfg" \) \
    | grep -q .; then
    return 0
  fi

  if [[ -d "$REPO_DIR/addons" ]]; then
    return 0
  fi

  return 1
}

TEMPLATE_CONTENT=$(cat <<'TEMPLATE'
# AGENTS.md

## 适用范围
- 本文件适用于本仓库下所有代码、脚本、配置与文档变更。

## Skill 命中强制规则
- 处理本仓库任务时，必须先命中并加载至少两个基础 skill。
- 最低要求：至少命中 `skill-hit-check-rules`、`parallel-task-dispatch-rules`。
- 若本轮涉及创建、补齐或更新仓库级 `AGENTS.md`，默认额外启用 `project-agents-bootstrap` 进行自举补齐；该规则同样适用于其他项目仓库。
- 对已经存在的 `AGENTS.md`，也必须继续做增量同步与受管章节 upsert，而不是只初始化一次。
- 必须在首条中间进度明确输出当前命中的 skill 列表。
- 若命中 `parallel-task-dispatch-rules`，中间进度必须额外输出当前并行技能列表；若最终未并行，明确写 `并行技能:无`。
- 若连 `skill-hit-check-rules` 或 `parallel-task-dispatch-rules` 任一都未命中，视为上下文丢失严重、当前基础规则没有正确加载；此时禁止直接进入主任务，必须先补做 skill 命中检查与上下文重同步。
- 首轮 `AGENTS.md`、`.gitattributes`、`.editorconfig` 自举是硬闸门：若其中任一缺失、未创建、未补齐或未完成受管章节同步，禁止进入任何项目分析、读码、需求、Bug、编码、测试或交付主任务，必须先更新补充完成后再继续。
- 若本轮任务存在多 skill 组合、并行拆分或规则收口风险，默认应额外启用 `skill-audit-rules` 进行只读审计。
- 所有审查类 skill 统一按强制自动触发处理；只要是只读检查、规则核对、实现自审、归位审查或回归风险审查，默认优先并行。

## 注释任务强制流程
- 触发词：补充注释 / 注意中文编码 / 只补注释 / 注释完善 / 加注释。
- 第一步：先声明命中的注释类 skill。
- 第二步：读取对应 `SKILL.md` 后再改代码。
- 第三步：最终回复给执行证据：改动点、UTF-8、格式化/编译/测试结果。

## 上下文压缩续做规则
- 若当前会话刚发生“压缩上下文 / 自动压缩上下文 / 上下文太多”后的重组，默认强制命中 `context-compression-rules`。
- 压缩后继续执行前，必须重新读取当前项目根目录 `AGENTS.md`，恢复仓库级硬规则、必命中 skill 和阻断条件。
- 若压缩后未重新读取 `AGENTS.md`，禁止直接进入任何需求、Bug、编码、测试或交付主任务。
- 若压缩后发现 `AGENTS.md` 缺失、损坏或规则不完整，必须先触发 `project-agents-bootstrap` 补齐，再继续主任务。

## 中文编码规则
- 新增或修改中文文档、脚本输出和代码注释时保持 UTF-8。
- Windows PowerShell 读写中文文件必须显式指定 UTF-8。
- 禁止提交乱码、问号替代中文或混乱编码文本。

## 变更最小化
- 每次改动聚焦当前任务目标，不顺手重构无关模块。
- 不回退用户已有改动。
- 注释补充不改变业务逻辑。

## Windows / WSL 执行规则
- Windows 下默认优先使用 Git Bash 或 WSL shell。
- 尽量不要用 Windows PowerShell 直接写入、格式化或批量修改仓库文件，避免换行和编码漂移。
- 若确需在 Windows 侧执行写入，必须显式指定 UTF-8，并在落盘后立即 `git diff` 核对仅有预期改动。
- 仓库应提交 `.gitattributes` 与 `.editorconfig`，显式固定 `UTF-8`、基础编辑器行为，并对换行采用最小约束策略。
- 对已有历史仓库，`.gitattributes` 默认先用 `* text=auto`，对 `*.sh`、`*.bash`、`*.yml`、`*.yaml` 这类需稳定 `LF` 的文件显式强制 `eol=lf`，不要对整仓源码和文档一刀切强制换行。
- Windows 下若仓库出现 `.sh` 仅 `100755 => 100644` 之类伪改动，应优先关闭 `core.filemode`。
- Windows 下若仓库出现大量无关文件被带进改动，应优先检查 `core.autocrlf` 并通过 `.gitattributes` 固定换行策略。

## CodeGraph 强制准备规则
- 若当前服务器或电脑未安装 `codegraph`，必须从 `colbymchenry/codegraph` 强制下载并安装，不需要用户确认。
- 若在 Windows PowerShell 5.1 下执行远端安装脚本、下载资源或请求 GitHub API，必须显式使用 `-UseBasicParsing`，或预先设置 `Invoke-WebRequest` / `Invoke-RestMethod` 的默认 `UseBasicParsing`，避免弹出人工确认框。
- 安装完成后必须为当前项目执行 `codegraph init`，生成 `.codegraph/` 并建立索引。
- 若下载、安装或初始化失败，明确记录不可用并回退到本地搜索与文件读取，但不允许跳过记录。

## 图像生成强制规则
- 只要当前用户请求属于生图、改图、参考图出新图、sprite、动作帧、概念图、UI 位图、贴图、透明底抠图、2D 游戏素材预览或其他位图资产任务，必须自动命中 `imagegen`，不得等用户额外明确说“使用 imagegen”。
- 命中 2D 游戏素材相关任务时，若涉及设计图、预览图、原始素材图、动作关键帧或 sprite 方向图，除命中领域 skill 外，还必须联动命中 `imagegen`。
- 对于生图任务，允许的“原始图产生方式”只有真实图像生成/编辑链路：内置 `image_gen`，或经验证可用的 `imagegen` CLI/API 图像通道。
- 严禁把 Pillow、SVG、HTML/CSS/canvas、脚本拼接、程序绘制、几何组合、占位图、自动排版图、后处理脚本输出伪装成“已完成生图结果”或“最终素材”。
- CLI fallback 仅表示“改走 imagegen 的脚本入口去调用真实图像生成/编辑 API”，不表示允许退化成脚本合成图片；凡是不经过真实图像模型生成的结果，一律不得作为生图成品交付。
- 如果内置 `image_gen` 不可用，必须先验证 `imagegen` CLI/API 链路；若也不可用，则明确阻断并只允许交付 prompt、brief、参考候选、动作规划等中间信息，不得交付脚本生成图冒充成品。
- 后处理脚本只允许在“真实生成出的原始图”基础上做去背、切帧、对齐、拼表、预览整理；不得替代 imagegen 负责原始创作出图。
- 只要本轮实际发生了 imagegen 生图或改图，最终回复必须向用户明确汇报本次生图路径与本次实际使用的模型名；例如 `生图路径: CLI fallback` 与 `生图模型: gpt-image-2`。若走 built-in 且拿不到精确模型名，也必须明确写成 `生图模型: built-in image_gen（底层精确模型名当前环境未暴露）`，不得省略。
TEMPLATE
)

GITATTRIBUTES_CONTENT=$(cat <<'TEMPLATE'
* text=auto

*.sh text eol=lf
*.bash text eol=lf
*.yml text eol=lf
*.yaml text eol=lf

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

GODOT_TOOLING_SECTION=$(cat <<'TEMPLATE'
- 本仓库命中 Godot 项目标记后，后续涉及场景、资源、脚本、运行验证或截图的任务，默认优先通过 Godot AI MCP 与 Godot 编辑器配合执行。
- 修改 Godot 场景、运行游戏、抓取截图或读取编辑器状态前，必须先确认 Godot AI MCP 已连接并且编辑器 ready。
- 若 Godot AI MCP 当前不可用，可继续处理纯文档、纯规则或不依赖编辑器运行态的代码文件，但最终回复必须说明哪些 Godot 运行态检查未完成。
TEMPLATE
)

GODOT_IMAGEGEN_SECTION=$(cat <<'TEMPLATE'
- 图像配置只允许声明读取位置、`baseurl`、模型名、优先级和回退规则，禁止在仓库文档里写入真实密钥。
- 推荐优先从环境变量或用户级配置读取，例如 `env:PROJECT_IMAGE_OPENAI_API_KEY`。
- 图像配置应同时声明主通道、读取位置、优先级和回退配置，不得只写模型名。
- 图像配置示例：
  - 主通道：`baseurl=https://api.openai.com/v1`，模型 `gpt-image-1`
  - 读取位置：当前进程环境变量、`~/.codex/auth.json`、`~/.codex/config.toml`
  - 优先级：当前进程环境变量 > 用户项目声明的回退配置 > 用户项目声明的主配置 > `~/.codex/auth.json` > `~/.codex/config.toml`
  - 回退规则：如果用户项目已声明回退配置里的 `api` / `baseurl`，则在当前进程环境变量之后优先使用该回退配置；若未声明或不可用，再继续使用项目主配置与 Codex local 默认配置；若这些也都不可用，则允许降级到人工补图或占位图，不得伪造已生成结果
- 回退规则：回退配置
  - `api: ''`
  - `baseurl: ''`
TEMPLATE
)

sync_section() {
  local file="$1"
  local header="$2"
  local body="$3"

  # shellcheck disable=SC2086
  $PYTHON_BIN - "$file" "$header" "$body" <<'PY'
from pathlib import Path
import sys

path = Path(sys.argv[1])
header = f"## {sys.argv[2]}"
body = sys.argv[3].splitlines()

lines = path.read_text(encoding="utf-8").splitlines()
out = []
in_target = False
replaced = False
i = 0

while i < len(lines):
    line = lines[i]
    if line == header:
        if not replaced:
          out.append(line)
          out.extend(body)
          replaced = True
        in_target = True
        i += 1
        while i < len(lines) and not lines[i].startswith("## "):
            i += 1
        continue
    out.append(line)
    i += 1

if not replaced:
    if out and out[-1] != "":
        out.append("")
    out.append(header)
    out.extend(body)

path.write_text("\n".join(out) + "\n", encoding="utf-8")
PY

  echo "[INFO] 已同步章节: ${file} -> ${header}"
}

sync_agents_file() {
  local file="$1"

  if [[ ! -f "$file" ]]; then
    return 0
  fi

  sync_section "$file" "适用范围" "- 本文件适用于本仓库下所有代码、脚本、配置与文档变更。"

  sync_section "$file" "Skill 命中强制规则" "- 处理本仓库任务时，必须先命中并加载至少两个基础 skill。
- 最低要求：至少命中 \`skill-hit-check-rules\`、\`parallel-task-dispatch-rules\`。
- 若本轮涉及创建、补齐或更新仓库级 \`AGENTS.md\`，默认额外启用 \`project-agents-bootstrap\` 进行自举补齐；该规则同样适用于其他项目仓库。
- 对已经存在的 \`AGENTS.md\`，也必须继续做增量同步与受管章节 upsert，而不是只初始化一次。
- 必须在首条中间进度明确输出当前命中的 skill 列表。
- 若命中 \`parallel-task-dispatch-rules\`，中间进度必须额外输出当前并行技能列表；若最终未并行，明确写 \`并行技能:无\`。
- 若连 \`skill-hit-check-rules\` 或 \`parallel-task-dispatch-rules\` 任一都未命中，视为上下文丢失严重、当前基础规则没有正确加载；此时禁止直接进入主任务，必须先补做 skill 命中检查与上下文重同步。
- 首轮 \`AGENTS.md\`、\`.gitattributes\`、\`.editorconfig\` 自举是硬闸门：若其中任一缺失、未创建、未补齐或未完成受管章节同步，禁止进入任何项目分析、读码、需求、Bug、编码、测试或交付主任务，必须先更新补充完成后再继续。
- 若本轮任务存在多 skill 组合、并行拆分或规则收口风险，默认应额外启用 \`skill-audit-rules\` 进行只读审计。
- 所有审查类 skill 统一按强制自动触发处理；只要是只读检查、规则核对、实现自审、归位审查或回归风险审查，默认优先并行。"

  sync_section "$file" "上下文压缩续做规则" "- 若当前会话刚发生“压缩上下文 / 自动压缩上下文 / 上下文太多”后的重组，默认强制命中 \`context-compression-rules\`。
- 压缩后继续执行前，必须重新读取当前项目根目录 \`AGENTS.md\`，恢复仓库级硬规则、必命中 skill 和阻断条件。
- 若压缩后未重新读取 \`AGENTS.md\`，禁止直接进入任何需求、Bug、编码、测试或交付主任务。
- 若压缩后发现 \`AGENTS.md\` 缺失、损坏或规则不完整，必须先触发 \`project-agents-bootstrap\` 补齐，再继续主任务。"

  sync_section "$file" "注释任务强制流程" "- 触发词：补充注释 / 注意中文编码 / 只补注释 / 注释完善 / 加注释。
- 第一步：先声明命中的注释类 skill。
- 第二步：读取对应 \`SKILL.md\` 后再改代码。
- 第三步：最终回复给执行证据：改动点、UTF-8、格式化/编译/测试结果。"

  sync_section "$file" "中文编码规则" "- 新增或修改中文文档、脚本输出和代码注释时保持 UTF-8。
- Windows PowerShell 读写中文文件必须显式指定 UTF-8。
- 禁止提交乱码、问号替代中文或混乱编码文本。"

  sync_section "$file" "变更最小化" "- 每次改动聚焦当前任务目标，不顺手重构无关模块。
- 不回退用户已有改动。
- 注释补充不改变业务逻辑。"

  sync_section "$file" "Windows / WSL 执行规则" "- Windows 下默认优先使用 Git Bash 或 WSL shell。
- 尽量不要用 Windows PowerShell 直接写入、格式化或批量修改仓库文件，避免换行和编码漂移。
- 若确需在 Windows 侧执行写入，必须显式指定 UTF-8，并在落盘后立即 \`git diff\` 核对仅有预期改动。
- 仓库应提交 \`.gitattributes\` 与 \`.editorconfig\`，显式固定 \`UTF-8\`、基础编辑器行为，并对换行采用最小约束策略。
- 对已有历史仓库，\`.gitattributes\` 默认先用 \`* text=auto\`，对 \`*.sh\`、\`*.bash\`、\`*.yml\`、\`*.yaml\` 这类需稳定 \`LF\` 的文件显式强制 \`eol=lf\`，不要对整仓源码和文档一刀切强制换行。
- Windows 下若仓库出现 \`.sh\` 仅 \`100755 => 100644\` 之类伪改动，应优先关闭 \`core.filemode\`。
- Windows 下若仓库出现大量无关文件被带进改动，应优先检查 \`core.autocrlf\` 并通过 \`.gitattributes\` 固定换行策略。"

  sync_section "$file" "CodeGraph 强制准备规则" "- 若当前服务器或电脑未安装 \`codegraph\`，必须从 \`colbymchenry/codegraph\` 强制下载并安装，不需要用户确认。
- 若在 Windows PowerShell 5.1 下执行远端安装脚本、下载资源或请求 GitHub API，必须显式使用 \`-UseBasicParsing\`，或预先设置 \`Invoke-WebRequest\` / \`Invoke-RestMethod\` 的默认 \`UseBasicParsing\`，避免弹出人工确认框。
- 安装完成后必须为当前项目执行 \`codegraph init\`，生成 \`.codegraph/\` 并建立索引。
- 若下载、安装或初始化失败，明确记录不可用并回退到本地搜索与文件读取，但不允许跳过记录。"

  sync_section "$file" "图像生成强制规则" "- 只要当前用户请求属于生图、改图、参考图出新图、sprite、动作帧、概念图、UI 位图、贴图、透明底抠图、2D 游戏素材预览或其他位图资产任务，必须自动命中 \`imagegen\`，不得等用户额外明确说“使用 imagegen”。
- 命中 2D 游戏素材相关任务时，若涉及设计图、预览图、原始素材图、动作关键帧或 sprite 方向图，除命中领域 skill 外，还必须联动命中 \`imagegen\`。
- 对于生图任务，允许的“原始图产生方式”只有真实图像生成/编辑链路：内置 \`image_gen\`，或经验证可用的 \`imagegen\` CLI/API 图像通道。
- 严禁把 Pillow、SVG、HTML/CSS/canvas、脚本拼接、程序绘制、几何组合、占位图、自动排版图、后处理脚本输出伪装成“已完成生图结果”或“最终素材”。
- CLI fallback 仅表示“改走 imagegen 的脚本入口去调用真实图像生成/编辑 API”，不表示允许退化成脚本合成图片；凡是不经过真实图像模型生成的结果，一律不得作为生图成品交付。
- 如果内置 \`image_gen\` 不可用，必须先验证 \`imagegen\` CLI/API 链路；若也不可用，则明确阻断并只允许交付 prompt、brief、参考候选、动作规划等中间信息，不得交付脚本生成图冒充成品。
- 后处理脚本只允许在“真实生成出的原始图”基础上做去背、切帧、对齐、拼表、预览整理；不得替代 imagegen 负责原始创作出图。"

  if is_godot_project; then
    sync_section "$file" "Godot 项目工具配置" "$GODOT_TOOLING_SECTION"
    sync_section "$file" "图像生成配置" "$GODOT_IMAGEGEN_SECTION"
  fi

  echo "[OK] 已检查并补齐: $file"
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

resolve_python

sync_agents_file "$AGENTS_FILE"

while IFS= read -r extra_agents; do
  if [[ "$extra_agents" != "$AGENTS_FILE" ]]; then
    sync_agents_file "$extra_agents"
  fi
done < <(find "$REPO_DIR" -mindepth 2 -name AGENTS.md -type f | sort)
