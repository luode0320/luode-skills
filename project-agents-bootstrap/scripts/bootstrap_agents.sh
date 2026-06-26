#!/usr/bin/env bash
set -euo pipefail

# project-agents-bootstrap: 检查并补齐仓库内规则文件（AGENTS.md / CLAUDE.md）
# 用法:
#   bootstrap_agents.sh
#   bootstrap_agents.sh --repo /path/to/repo
#   bootstrap_agents.sh --target claude        # Claude Code 环境，创建/同步 CLAUDE.md
#   bootstrap_agents.sh --target codex         # Codex 环境，创建/同步 AGENTS.md（默认）
#   bootstrap_agents.sh --target both          # 同时创建/同步 AGENTS.md 与 CLAUDE.md
#
# 说明:
#   - --target 只决定根目录"缺失时创建哪个"规则文件；
#   - 无论 target 为何，根目录与子目录中所有已存在的 AGENTS.md / CLAUDE.md 都会被同步。

REPO_DIR="$(pwd)"
TARGET="codex"

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
    --target)
      if [[ $# -lt 2 ]]; then
        echo "[ERROR] --target 需要一个参数（codex|claude|both）" >&2
        exit 1
      fi
      case "$2" in
        codex|claude|both) TARGET="$2" ;;
        *) echo "[ERROR] --target 取值必须是 codex|claude|both" >&2; exit 1 ;;
      esac
      shift 2
      ;;
    -h|--help)
      echo "Usage: $0 [--repo /path/to/repo] [--target codex|claude|both]"
      exit 0
      ;;
    *)
      echo "[ERROR] 未知参数: $1" >&2
      echo "Usage: $0 [--repo /path/to/repo] [--target codex|claude|both]" >&2
      exit 1
      ;;
  esac
done

if [[ ! -d "$REPO_DIR" ]]; then
  echo "[ERROR] 仓库目录不存在: $REPO_DIR" >&2
  exit 1
fi

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

# ---- 受管章节正文（单引号 heredoc，原样保留反引号等特殊字符）----
# 章节内容以 project-agents-bootstrap 最小模板为权威源，创建与同步共用同一份正文，避免脱节。

BODY_SCOPE=$(cat <<'EOF'
- 本文件适用于本仓库下所有代码与文档变更。
EOF
)

BODY_SKILL_AUTO=$(cat <<'EOF'
- **所有 skill 的触发不依赖用户主动通知**，AI 必须基于任务内容、工作目录、用户意图主动检测并触发
- 每轮处理用户消息时，必须主动扫描所有可用 skill 的触发条件，符合条件的 skill 必须被调用
- `skill-hit-check-rules` 每轮必须作为第一个 tool call 被调用，无例外
- 禁止以下理由跳过应触发的 skill：
  - “用户没有明确说需要这个 skill”
  - “任务看起来简单，不需要 skill”
  - “我已经知道怎么做了”
  - “这不是核心 skill”
- 违反本规则视为流程违规，必须立即停止当前执行，回到命中检查重走
EOF
)

BODY_NO_HALLUCINATE=$(cat <<'EOF'
- 任何对文件、命令、搜索、网络的读取与执行，必须通过真实工具调用（独立 tool call）完成；严禁在回复正文里编写 `<invoke>` / `<result>` / 伪 function_calls 文本假装调用工具，也禁止凭记忆“想象”文件内容当作已读取结果。
- 引用任何文件内容、行号、函数名、配置值前，必须来自本轮真实工具返回；未真实读取不得断言具体代码或数据。
- 若发现输出出现大段重复行、错乱或重复行号、源码文件莫名以 Markdown 代码块结束符收尾、import 与实际用法矛盾等异常，立即判定为生成异常：停止后重新发起真实工具调用，并用 `md5sum` / `wc -c` 等独立命令交叉校验再继续。
- 关键文件读取建议附带指纹校验（`md5sum` + `wc -c`），确保所读即磁盘真实内容。
- 违反本条视为最高级别流程违规。
EOF
)

BODY_NO_AUTO_COMMIT=$(cat <<'EOF'
- 绝对禁止在用户未于「当前这轮消息」显式提出提交的前提下，执行任何写入仓库历史的 Git 动作（`git commit`、`git commit --amend`、`git push`、`git rebase`、`git merge --no-ff` 等）。
- 「显式提出提交」指用户在当前这轮消息里明确表达提交/推送意图，例如：`提交git`、`提交代码`、`commit一下`、`帮我提交`、`推送`、`push`、`同步到远端`。
- 仅完成代码改动、任务收尾、或上一轮提交过，都不构成本轮提交授权；缺少当轮显式授权时，必须停在「已改动未提交」状态并提示用户。
- 任何情况下都不得以「我以为你想提交」「按惯例提交」「顺手提交」为由自动提交。
- 只读盘点命令（`git status`、`git diff`、`git log`）不受限制；写入历史的动作严格受限。
- 本条与全局技能 `git-collaboration-rules` 的「1.-2」一致，为项目级重申，确保重启会话 / 无全局上下文时本规则仍在项目内生效。
- 违反本条视为最高级别流程违规。
EOF
)

BODY_SKILL_HIT=$(cat <<'EOF'
- 处理本仓库任务时，必须先命中并加载至少三个基础 skill。
- 最低要求：至少命中 `skill-hit-check-rules`、`parallel-task-dispatch-rules`、`reasoning-summary-structure-rules`。
- 若本轮涉及创建、补齐或更新仓库级规则文件，默认额外启用 `project-agents-bootstrap` 进行自举补齐；该规则同样适用于其他项目仓库。
- 必须在首条中间进度明确输出当前命中的 skill 列表。
- 若命中 `parallel-task-dispatch-rules`，中间进度必须额外输出当前并行技能列表；若最终未并行，明确写 `并行技能:无`。
- 若连 `skill-hit-check-rules` 或 `parallel-task-dispatch-rules` 任一都未命中，视为上下文丢失严重、当前基础规则没有正确加载；此时禁止直接进入主任务，必须先补做 skill 命中检查与上下文重同步。
- 若本轮任务存在多 skill 组合、并行拆分或规则收口风险，默认应额外启用 `skill-audit-rules` 进行只读审计。
- 所有审查类 skill 统一按强制自动触发处理；只要是只读检查、规则核对、实现自审、归位审查或回归风险审查，默认优先并行。
EOF
)

BODY_COMMENT_TASK=$(cat <<'EOF'
- 触发词：补充注释 / 注意中文编码 / 只补注释 / 注释完善 / 加注释。
- 第一步：先声明命中的注释类 skill。
- 第二步：读取对应 `SKILL.md` 后再改代码。
- 第三步：最终回复给执行证据：改动点、UTF-8、格式化/编译/测试结果。
EOF
)

BODY_CONTEXT_COMPRESS=$(cat <<'EOF'
- 若当前会话刚发生“压缩上下文 / 自动压缩上下文 / 上下文太多”后的重组，默认强制命中 `context-compression-rules`。
- 压缩后继续执行前，必须重新读取当前项目根目录规则文件（`AGENTS.md` / `CLAUDE.md`），恢复仓库级硬规则、必命中 skill 和阻断条件。
- 若压缩后未重新读取规则文件，禁止直接进入任何需求、Bug、编码、测试或交付主任务。
- 若压缩后发现规则文件缺失、损坏或规则不完整，必须先触发 `project-agents-bootstrap` 补齐，再继续主任务。
EOF
)

BODY_CHINESE_ENC=$(cat <<'EOF'
- 新增或修改注释默认使用中文。
- 文件编码保持 UTF-8，禁止乱码。
EOF
)

BODY_MIN_CHANGE=$(cat <<'EOF'
- 注释补充不改变业务逻辑。
EOF
)

BODY_WINDOWS_WSL=$(cat <<'EOF'
> 详细规则与命令模板见 `windows-wsl-execution-rules` skill。本节为写入规则文件的最小约束摘要。代码在 WSL 文件系统内（`/home/<user>/<project>`），编译/运行/测试/调试都在 WSL 完成。

**先看 agent 在哪运行：**

- **agent 在 WSL（推荐）**：直接 `cd /home/<user>/<project>` 执行 `go build`/`test`/`run`/`dlv`，无需任何包裹。
- **agent 在 Windows（如 Claude Desktop GUI）**：
  - shell 默认用 Git Bash
  - 看代码、改代码、git：经 `\\wsl.localhost\<distro>\home\<user>\<project>` 访问 WSL 文件
  - 编译、运行、测试、调试：`wsl.exe --cd /home/<user>/<project> <command>`

**为什么执行/调试在 WSL：** 只有 WSL 进程能正常联网，且二进制面向 Linux。

**命令格式：** `wsl.exe --cd /home/<user>/<project> <command>`（默认发行版省略 `-d`；多发行版时用 `wsl.exe -l -v` 查名后加 `-d <发行版名>`）。不再使用 `/mnt/<drive>`。

**编码约束：**

- 仓库提交 `.gitattributes` 与 `.editorconfig`，固定 UTF-8 和换行策略
- `.gitattributes` 默认 `* text=auto`，`*.sh`/`*.yaml` 显式 `eol=lf`
- 不对 `*.go`、`*.vue`、`*.md` 等全量强制 `eol=lf`
- Windows 下出现大量无关改动优先检查 `core.autocrlf`
EOF
)

BODY_CODEGRAPH=$(cat <<'EOF'
- 若当前服务器 / 电脑未安装 `codegraph`，必须从 `colbymchenry/codegraph` 强制下载并安装，不需要用户确认。
- 若在 Windows PowerShell 5.1 下执行安装，必须默认启用 `Invoke-WebRequest` / `Invoke-RestMethod` 的 `UseBasicParsing`，不得把人工点击确认当作标准流程。
- 安装完成后必须为当前项目执行 `codegraph init`，生成 `.codegraph/` 并建立索引。
- 若下载、安装或初始化失败，明确记录不可用并回退到本地搜索与文件读取。
- 架构层分析可配套 codebase-memory-mcp（`DeusData/codebase-memory-mcp`，按官方说明安装，非强制）作为 CodeGraph 的补充。
EOF
)

BODY_CODE_EXPLORE=$(cat <<'EOF'
1. 日常理解代码、定位实现、追踪调用链、分析改动影响时，优先使用 CodeGraph。
2. 修改代码前，先用 CodeGraph 获取相关源码和影响范围。
3. 不要在 CodeGraph 已经返回足够上下文时重复全仓库 grep。
4. 项目架构分析、跨模块依赖、函数调用频率、ADR 记录等架构层任务，用 codebase-memory-mcp 作补充。
5. CodeGraph 作默认入口，codebase-memory-mcp 作高级图分析工具；两者结果与当前代码不一致时，以当前代码为准并重新同步索引。
EOF
)

BODY_PLUGIN=$(cat <<'EOF'
- 涉及 AI 编码插件（如 Ponytail）的安装、启用、配置时，联动 `plugin-installation-rules`。
- Ponytail 为默认必装插件：会话 / 项目准备时默认安装并启用（详见 `plugin-installation-rules`）。
- 安装命令与配置一律以插件官方仓库为准，不沿用第三方博客 / 公众号转述的旧命名、旧参数。
- 通用支持 Claude Code / Codex 等环境，按当前 AI 选对应安装方式；安装或启用失败时回退到常规流程。
EOF
)

BODY_IMAGEGEN=$(cat <<'EOF'
- 只要当前用户请求属于生图、改图、参考图出新图、sprite、动作帧、概念图、UI 位图、贴图、透明底抠图、2D 游戏素材预览或其他位图资产任务，必须自动命中 `imagegen`，不得等用户额外明确说“使用 imagegen”。
- 命中 2D 游戏素材相关任务时，若涉及设计图、预览图、原始素材图、动作关键帧或 sprite 方向图，除命中领域 skill 外，还必须联动命中 `imagegen`。
- 对于生图任务，允许的“原始图产生方式”只有真实图像生成/编辑链路：内置 `image_gen`，或经验证可用的 `imagegen` CLI/API 图像通道。
- 严禁把 Pillow、SVG、HTML/CSS/canvas、脚本拼接、程序绘制、几何组合、占位图、自动排版图、后处理脚本输出伪装成“已完成生图结果”或“最终素材”。
- CLI fallback 仅表示“改走 imagegen 的脚本入口去调用真实图像生成/编辑 API”，不表示允许退化成脚本合成图片；凡是不经过真实图像模型生成的结果，一律不得作为生图成品交付。
- 如果内置 `image_gen` 不可用，必须先验证 `imagegen` CLI/API 链路；若也不可用，则明确阻断并只允许交付 prompt、brief、参考候选、动作规划等中间信息，不得交付脚本生成图冒充成品。
- 后处理脚本只允许在“真实生成出的原始图”基础上做去背、切帧、对齐、拼表、预览整理；不得替代 imagegen 负责原始创作出图。
EOF
)

GODOT_TOOLING_SECTION=$(cat <<'EOF'
- 本仓库命中 Godot 项目标记后，后续涉及场景、资源、脚本、运行验证或截图的任务，默认优先通过 Godot AI MCP 与 Godot 编辑器配合执行。
- 修改 Godot 场景、运行游戏、抓取截图或读取编辑器状态前，必须先确认 Godot AI MCP 已连接并且编辑器 ready。
- 若 Godot AI MCP 当前不可用，可继续处理纯文档、纯规则或不依赖编辑器运行态的代码文件，但最终回复必须说明哪些 Godot 运行态检查未完成。
EOF
)

GODOT_IMAGEGEN_SECTION=$(cat <<'EOF'
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
EOF
)

GITATTRIBUTES_CONTENT=$(cat <<'EOF'
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
EOF
)

EDITORCONFIG_CONTENT=$(cat <<'EOF'
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
EOF
)

# 在文件中按 "## header" 定位并 upsert 章节正文
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
replaced = False
i = 0

while i < len(lines):
    line = lines[i]
    if line == header:
        if not replaced:
            out.append(line)
            out.append("")
            out.extend(body)
            replaced = True
        i += 1
        while i < len(lines) and not lines[i].startswith("## "):
            i += 1
        if i < len(lines):
            out.append("")
        continue
    out.append(line)
    i += 1

if not replaced:
    if out and out[-1] != "":
        out.append("")
    out.append(header)
    out.append("")
    out.extend(body)

path.write_text("\n".join(out) + "\n", encoding="utf-8")
PY

  echo "[INFO] 已同步章节: ${file} -> ${header}"
}

create_rule_file() {
  local file="$1"
  printf '# AGENTS.md / CLAUDE.md\n\n' > "$file"
  cat >> "$file" <<'EOF'
> Codex 使用 `AGENTS.md`，Claude Code 使用 `CLAUDE.md`，内容规则相同。
EOF
  echo "[OK] 已创建: $file"
}

sync_agents_file() {
  local file="$1"

  if [[ ! -f "$file" ]]; then
    return 0
  fi

  sync_section "$file" "适用范围" "$BODY_SCOPE"
  sync_section "$file" "Skill 强制自动触发规则（最高优先级）" "$BODY_SKILL_AUTO"
  sync_section "$file" "严禁脑补工具调用与结果（最高优先级，强制）" "$BODY_NO_HALLUCINATE"
  sync_section "$file" "严禁自动提交 Git（最高优先级，强制）" "$BODY_NO_AUTO_COMMIT"
  sync_section "$file" "Skill 命中强制规则" "$BODY_SKILL_HIT"
  sync_section "$file" "注释任务强制流程" "$BODY_COMMENT_TASK"
  sync_section "$file" "上下文压缩续做规则" "$BODY_CONTEXT_COMPRESS"
  sync_section "$file" "中文编码规则" "$BODY_CHINESE_ENC"
  sync_section "$file" "变更最小化" "$BODY_MIN_CHANGE"
  sync_section "$file" "Windows / WSL 执行规则" "$BODY_WINDOWS_WSL"
  sync_section "$file" "CodeGraph 强制准备规则" "$BODY_CODEGRAPH"
  sync_section "$file" "代码库探索规则" "$BODY_CODE_EXPLORE"
  sync_section "$file" "插件检测安装规则" "$BODY_PLUGIN"
  sync_section "$file" "图像生成强制规则" "$BODY_IMAGEGEN"

  if is_godot_project; then
    sync_section "$file" "Godot 项目工具配置" "$GODOT_TOOLING_SECTION"
    sync_section "$file" "图像生成配置" "$GODOT_IMAGEGEN_SECTION"
  fi

  echo "[OK] 已检查并补齐: $file"
}

resolve_python

# 1) 按 --target 创建缺失的根目录规则文件
declare -a TARGET_FILES=()
case "$TARGET" in
  codex)  TARGET_FILES=("$REPO_DIR/AGENTS.md") ;;
  claude) TARGET_FILES=("$REPO_DIR/CLAUDE.md") ;;
  both)   TARGET_FILES=("$REPO_DIR/AGENTS.md" "$REPO_DIR/CLAUDE.md") ;;
esac

for f in "${TARGET_FILES[@]}"; do
  if [[ ! -f "$f" ]]; then
    create_rule_file "$f"
  fi
done

# 2) .gitattributes / .editorconfig
if [[ ! -f "$GITATTRIBUTES_FILE" ]]; then
  printf "%s\n" "$GITATTRIBUTES_CONTENT" > "$GITATTRIBUTES_FILE"
  echo "[OK] 已创建: $GITATTRIBUTES_FILE"
fi
if [[ ! -f "$EDITORCONFIG_FILE" ]]; then
  printf "%s\n" "$EDITORCONFIG_CONTENT" > "$EDITORCONFIG_FILE"
  echo "[OK] 已创建: $EDITORCONFIG_FILE"
fi

# 3) 同步根目录所有已存在的规则文件（AGENTS.md / CLAUDE.md）
for name in AGENTS.md CLAUDE.md; do
  sync_agents_file "$REPO_DIR/$name"
done

# 4) 同步子目录中所有已存在的 AGENTS.md / CLAUDE.md
while IFS= read -r extra_file; do
  sync_agents_file "$extra_file"
done < <(find "$REPO_DIR" -mindepth 2 \( -name AGENTS.md -o -name CLAUDE.md \) -type f | sort)
