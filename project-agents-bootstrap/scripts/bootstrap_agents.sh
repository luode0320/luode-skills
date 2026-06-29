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

### 项目长期上下文文档自动加载（强制）

- 会话开始（含新会话首轮、上下文压缩续做后）必须检测项目根目录四个长期上下文文档：`AGENTS.md`、`CLAUDE.md`、`PROJECT_MEMORY.md`、`PROJECT_STYLE.md`。
- 存在即读取并加载为当前上下文；缺失即按各自主文档模板创建；其后随对话与代码变化持续维护，不是只建一次。
- `PROJECT_MEMORY.md` 记忆对象：指标、参数、表字段、缓存键、变量、公式、方法映射、别名等反复出现且需长期复用的事实（联动 `project-memory-rules`）。
- `PROJECT_STYLE.md` 记忆对象：方法、注释、错误处理、日志、接口等代码写法样例（联动 `project-style-rules`）。
- 来源优先级：当前项目代码 > 最近对话 > 已有文档 > 旧记忆 / 旧风格；来源冲突时以高优先级为准。
- 缺失则按各自 `references` 主文档模板创建；只写明确事实，合并去重，刷新「更新时间」，并在「变更记录」补写变更原因。
- 单一主文档原则：每类长期上下文只维护一份根目录主文档，不产生衍生文件。
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
- 处理本仓库任务时，必须先命中并加载至少五个基础 skill。
- 最低要求：至少命中 `skill-hit-check-rules`、`parallel-task-dispatch-rules`、`reasoning-summary-structure-rules`、`project-memory-rules`、`project-style-rules`。
- 若本轮涉及创建、补齐或更新仓库级规则文件，默认额外启用 `project-agents-bootstrap` 进行自举补齐；该规则同样适用于其他项目仓库。
- 必须在首条中间进度明确输出当前命中的 skill 列表。
- 若命中 `parallel-task-dispatch-rules`，中间进度必须额外输出当前并行技能列表；若最终未并行，明确写 `并行技能:无`。
- 进入分析、侦察、需求、Bug、审查、测试、文档或编码等实质执行前，主 agent 必须自主判断是否存在可由 subagent 并行推进的独立问题、证据来源、文件集、模块边界或职责边界；不得只依赖固定 skill 映射表。
- 只要判定为可并行或条件并行，且当前环境支持 subagent / multi-agent / thread 能力、无明确禁止或写集冲突，必须优先真实启动子 agent 并行执行；不能只输出线程分配或并行建议。
- 项目分析、找 Bug、需求完善侦察、资料/日志/调用链证据收集等任务，即使没有固定并行 skill，也应优先尝试拆出只读 sidecar 子任务交给 subagent；主 agent 保留最终判断、归纳和冲突裁决职责。
- 单一根因、需求边界、接口契约、schema 或架构方向等需要统一裁决的主路径必须串行；其旁路证据收集、影响面盘点和资料检索可在边界清晰时条件并行。
- 若计划并行但真实子 agent 启动失败、环境不支持或被阻断，必须说明计划线程数、实际启动数、关闭/回收数和回退原因，不得把计划并行伪装成已并行。
- 用户使用“开始实施 / 开始实现 / 开始执行 / 直接做 / 继续做完 / 按文档实现”等开工类指令时，不得视为无边界长文本执行授权；必须先确认已有执行计划，或当场给出本轮执行计划、完成定义、停止条件和最大推进边界。缺少计划或停止条件时，禁止直接进入实现 / 执行。
- 若连 `skill-hit-check-rules` 或 `parallel-task-dispatch-rules` 任一都未命中，视为上下文丢失严重、当前基础规则没有正确加载；此时禁止直接进入主任务，必须先补做 skill 命中检查与上下文重同步。
- 若本轮任务存在多 skill 组合、并行拆分或规则收口风险，默认应额外启用 `skill-audit-rules` 进行只读审计。
- 自动审查白名单只保留 `implementation-review-rules` 与最终收口前的 `project-change-review-rules`。
- `project-change-review-rules` 同时支持两类触发：用户明确要求审查当前改动，或本轮存在代码改动且准备最终收口。
- `code-review-automation-rules` 仅用于当前分支提交级审查，不纳入默认自动审查链。
- 若本轮新增或修改任意 skill 资产（`SKILL.md`、`references`、`scripts`、`agents` 等），必须命中 `skill-compliance-gate-rules` 并在收口前给出 PASS / FAIL 结论；改动 `description` 或触发条件追加 `skill-evolution-rules`，涉及多 skill / 职责边界 / 规则收口风险追加 `skill-audit-rules`；改动 `description` 或新增 / 修改 `##` 级标题后，收口前必须重跑 skill 字典生成脚本刷新 `data.js` 与 `字典.md`；上述联动未走完不得收口。
- 任何 agent 收到用户明确结束指令（如“结束”“停止”“到此为止”“不要继续”“不要下一步建议”“不要扩散”）时，必须立即停止自动继续和扩散性输出，只允许给出必要的最小收口结论。
- 若命中 `autonomous-execution-rules`，自动继续只允许用于“完成原始用户目标仍必需的动作”；不得把“进一步优化 / 可继续整理 / 总结里的下一步建议 / 未来迭代建议”自动升级成新的执行目标。
- 当原始用户目标已经完成或用户已给出明确结束指令，且不存在完成原始目标仍必需的动作时，必须停止连续执行并直接结束；不得输出“下一步状态”“下一步建议”“等待用户新指令”“无需继续动作”等任何可能触发循环 loop 的占位区块或扩散性文案，除非用户明确要求后续建议。
- 若当前运行环境存在 goal / plan / task 等显式状态收口机制，且原始用户目标已经完成或已满足该机制的阻断条件，必须在最终收口前真实执行对应收口动作；只写完成文案不算真正结束运行时状态。Codex goal 仅是其中一种特例。
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
