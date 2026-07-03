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
PROJECT_MEMORY_FILE="$REPO_DIR/PROJECT_MEMORY.md"

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
- 把 `Plan Mode` 的默认计划外壳沉到仓库级规则里，保证所有计划型提问都会先触发 `implementation-planning-rules` 再回流前置域。
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
- 当前上下文处于 `Plan Mode` 时，必须把 `implementation-planning-rules` 作为第一层计划外壳先命中，再按需回流需求侦察、需求接入、缺口、边界、拆分或其他域；这条路由优先级高于普通计划型提问

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
- 本仓库默认处于 subagent 完全授权模式：用户已明确允许 agent 在任务可切分、写集不冲突、风险可控且环境支持时自动启动 subagent / delegation / parallel agent work；该项目级 standing authorization 视为满足工具显式授权条件。
- 进入分析、侦察、需求、Bug、审查、测试、文档或编码等实质执行前，主 agent 必须自主判断是否存在可由 subagent 并行推进的独立问题、证据来源、文件集、模块边界或职责边界；不得只依赖固定 skill 映射表。
- 只要判定为可并行或条件并行，且当前环境支持 subagent / multi-agent / thread 能力、当前轮授权或项目级完全授权成立、无明确禁止或写集冲突，必须优先真实启动子 agent 并行执行；不能只输出线程分配或并行建议。
- 项目分析、找 Bug、需求完善侦察、资料/日志/调用链证据收集等任务，即使没有固定并行 skill，也应优先尝试拆出只读 sidecar 子任务交给 subagent；主 agent 保留最终判断、归纳和冲突裁决职责。
- 单一根因、需求边界、接口契约、schema 或架构方向等需要统一裁决的主路径必须串行；其旁路证据收集、影响面盘点和资料检索可在边界清晰时条件并行。
- 若计划并行但真实子 agent 启动失败、环境不支持或被阻断，必须说明计划线程数、实际启动数、关闭/回收数和回退原因，不得把计划并行伪装成已并行。
- 需求阶段只允许围绕真实缺口一次推进一个关键问题；禁止把 agent 猜测写成待确认答案，禁止“先做了再补需求”，正式需求主文档未真实落盘前禁止进入实施规划与正式编码。
- 用户若在当前轮显式提出计划型问题（如“怎么做”“先给计划”“先出方案和步骤”“这个怎么改”），必须先命中计划规则；即使前置条件尚未齐备，也要输出受限计划 / 阻断计划，而不是表现成计划规则未触发。
- 当前运行环境若要求用 `<proposed_plan>` 或其他专用计划包裹输出，包裹层不改变项目内计划格式；计划正文仍必须遵守 `implementation-planning-rules` 与 `plan-structure-template.md` 的结构、字段和约束，不得退化成通用摘要式计划。
- 用户使用“开始实施 / 开始实现 / 开始执行 / 直接做 / 继续做完 / 按文档实现 / 按建议执行 / 按方案执行 / 就按你刚才说的做”等开工类指令时，不得视为无边界长文本执行授权；必须先确认已有执行计划，或当场给出本轮执行计划、任务完成条件、任务停止 / 结束条件和最大推进边界。缺少这些边界时，禁止直接进入实现 / 执行。
- 受限计划不得作为实施授权；用户即使明确采纳，agent 也只能先补齐缺失前置条件并将其升级为正式执行计划，未升级前禁止进入编码、改码、重构、测试实施或其他执行动作。
- 若当前轮只是采纳 agent 上一轮或更早轮次给出的建议、方案、修复路线或实施思路，也必须先把该建议收口成正式执行计划，才允许继续实现 / 执行；不得把聊天建议直接当成可执行计划。
- 实施规划阶段默认采用只读计划模式：禁止写代码、禁止边计划边试做；只允许读仓库、定依赖、列风险、拆任务、写实施文档。实施计划必须先写 agent 对当前问题的理解，至少交代问题 / 目标、本轮范围、非范围、当前优先闭环和关键假设 / 待确认点，再进入“依赖图 + 垂直切片”的最小闭环任务拆分；避免按前端 / 后端 / 数据库水平分层堆计划。单任务默认尽量控制在约 5 个文件以内，且每个最小任务都必须先完成自己的真实测试、审查、验收闭环后，才允许推进下一个任务。涉及代码生成、修改或重构的计划，必须显式写出真实测试入口、依赖环境、样本 / 数据来源和通过标准；`build`、`lint`、静态检查或人工阅读不算真实测试，免测只能写在纯文档、纯注释、纯排版、纯静态资源改名 / 搬运或不会影响运行结果的场景里；若计划涉及代码生成、修改或重构，“现状与落点”必须给出代码落点目录树，不能只写文件名或普通条目。
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

BODY_THREAD_TITLE=$(cat <<'EOF'
- 当当前 Codex / Claude / agent 会话进入明确需求、Bug、实施、审查、测试、提交或其他可命名任务，且会话标题为空泛、过时、泛称或不匹配当前任务时，必须自动命中 `thread-title-rules`。
- `thread-title-rules` 负责生成 8-24 字中文简要标题，并按平台能力矩阵调用当前环境真实线程重命名工具更新当前会话标题；Codex 环境优先使用真实 `set_thread_title` 工具，Claude Code 仅在存在真实改名工具时执行，Claude Desktop 默认视为无真实自动改名工具并显式跳过。
- 会话重命名不等待用户显式要求；但任务主题尚未稳定、标题已准确、工具不可用、无法可靠确定当前会话 ID 或用户明确禁止时必须跳过，并说明原因。
- `CLAUDE.md` 仅用于 Claude Code 仓库规则自举，不等同于 Claude Desktop 已具备自动会话改名能力。
- 标题采用“任务对象 + 动作 / 症状 / 阶段”的中文简要写法，避免只写“提交 git”“开始实施”“继续做”“修复 bug”“更新文档”等泛化动作标题。
- 禁止用正文伪造工具调用、raw directive 或猜测结果来宣称已经改名；所有标题变更必须来自真实工具返回。
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
- 所有代码、文档、配置、脚本、测试资产和生成类文本文件，新增或修改时默认使用 UTF-8 编码；禁止使用 GBK、ANSI、系统默认编码或编辑器默认编码落盘。
- 在 Windows、Linux、WSL、容器和远程服务器上写文件时都必须保持 UTF-8 口径一致；不得因为当前终端、区域设置或系统语言不同而切换编码。
- 通过命令行写文件时必须显式指定 UTF-8：PowerShell 使用 `Set-Content -Encoding UTF8`、`Add-Content -Encoding UTF8`、`Out-File -Encoding utf8`，Python / Node / Go 等脚本必须显式声明 UTF-8 读写参数或确保运行时强制 UTF-8。
- 禁止用未确认编码的 `>`、`>>`、默认 `Out-File`、默认 `Set-Content` 或其他依赖 shell 默认编码的方式写入中文、代码、Markdown、JSON、YAML、脚本和规则文件。
- 写入后必须回读关键文件并检查 `git diff`，确认中文未乱码、编码未漂移、换行未被意外批量转换。
- 仓库应提交 `.editorconfig` 与 `.gitattributes` 固定 `charset = utf-8`、基础换行和二进制文件规则；若发现文件被 GBK / ANSI 写入，必须先转回 UTF-8 再继续后续改动。
EOF
)

BODY_MIN_CHANGE=$(cat <<'EOF'
- 注释补充不改变业务逻辑。
EOF
)

BODY_LOCAL_ONLY_CONNECTION=$(cat <<'EOF'
- 需求侦察、Bug 复现 / 定位 / 运行时调试、功能验证、回归测试、上线接口测试、浏览器联调、启动前后端服务或执行任何测试脚本时，所有数据库、缓存、消息队列、HTTP/RPC 上游、前端 / 后端服务连接都只能使用 `local` 本地环境。
- 本地环境只允许来自 `config_local*`、`.env.local`、`.env.development`、本机开发容器、`localhost` / `127.0.0.1` / 本机端口等本地开发配置；`test`、`prod`、`production`、`staging`、`pre`、`release` 等非 local 环境一律禁止连接。
- 即使用户提供了 test / prod 连接串、账号、接口地址或临时授权，也不得由 agent 直接连接或调用；必须记录为环境阻断，并要求改用 local 本地数据库和本地服务。
- 若 local 配置缺失、local 数据不足或本地服务未启动，只能初始化 / 启动 / 查询 local 环境；不得回退到 test / prod 数据库、缓存、消息队列、外部服务或线上接口补证据。
- 需要写入数据时仅允许写入 local 环境，并且必须有清理或回滚方案；Bug 侦察类只读链路仍保持只读，禁止自行增删改数据。
EOF
)

BODY_REUSE_FIRST=$(cat <<'EOF'
- 编写代码前，必须先检索是否已有可复用的开源库、npm 包或项目内工具类，优先复用而非从零实现。
- 优先级：项目内已有工具类 / 公共方法 > 成熟开源库（npm / GitHub）> 自行实现。
- 禁止在已有成熟第三方库覆盖该能力时重复造轮子；引入新依赖前须确认许可证兼容、维护活跃且无已知安全问题。
- 若确实需要自行实现，必须在代码注释或 PR 说明中写明为何不使用现有库 / 工具类。
- 检索范围应覆盖项目 `utils`、`common`、`helpers` 等公共目录，以及 `package.json` / `go.mod` 等依赖声明文件。
EOF
)

BODY_MINIMAL_LADDER=$(cat <<'EOF'
- 写代码前按以下顺序逐级判断,停在前一级能成立的就停,不往下跳级:
  1. 需要存在吗?纯推测性需求 → 不写,用一行说明为何跳过(YAGNI)
  2. 代码库已有?已有的 helper / util / 类型 / 模式 → 复用,不重写;改前先搜 `utils` / `common` / `helpers` 及依赖声明文件
  3. 标准库能做?→ 用标准库,不引入第三方
  4. 平台原生特性能覆盖?→ 用原生(如浏览器 `<input type="date">`、CSS 原生能力、DB 约束替代应用层校验),不装库
  5. 已装依赖能解?→ 用它,不加新依赖
  6. 能写成一行?→ 写一行
  7. 都不行: 才写最小可工作代码
- 阶梯在理解问题后才运行,不替代阅读:先读任务和涉及的代码、追完真实流程,再爬阶梯;两级行得通就取更高一级,第一个能用的解就是对的
- Bug 修复走根因不走症状:改前 grep 所有调用方,在共享函数加一处 guard 比每调用方加一处 guard 更小 diff,且不留下兄弟调用方仍然坏掉
- 不写未请求的抽象:没有第二实现的接口、单一产品的工厂、永不改的配置值,都不提前建
- 故意简化处标记 `deferral:` 注释,写明天花板和升级路径,例如 `// deferral: 全局锁, 吞吐量不够时改每账户锁`; 没有升级路径的标记为会被静默忽略的风险
- 与「变更最小化」「依赖与工具复用优先规则」的边界:本阶梯管写什么(方案选择),「变更最小化」管改多少(diff 范围),「依赖与工具复用优先规则」是本阶梯第 2、5 级的具体执行细节;三者互补不冲突
- 不可砍的红线:信任边界的输入校验、防数据丢失的错误处理、安全措施、无障碍基础、硬件校准旋钮、用户显式要求的内容;简化只针对冗余抽象和重复造轮,不针对安全检查
- 非平凡逻辑(分支 / 循环 / 解析 / 金额或安全路径)落地时留一个最小可运行自检(assert 或一个测试文件),平凡一行不需要
- 用户坚持要完整版 → 照建,不再争论
EOF
)

BODY_OUTPUT_FORMAT=$(cat <<'EOF'
- AI 输出统一使用 markdown，不依赖 HTML 渲染：HTML 标签在 Claude Desktop、纯 CLI、Codex 等大量 agent 环境不渲染，会退化成原文噪声，并破坏对输出的机器解析。
- 视觉层级与区分靠 markdown 语义结构（`#` / `##` 标题、`---` 分隔线、表格、`>` 引用块、徽章 emoji），不靠绝对字号。
- 字号由各 agent 渲染端（客户端主题 / 字体 / 缩放）决定，内容层不强行控制；需要更大字号时调客户端，不在输出里塞 HTML。
- 普通说明、方案、流程、总结、审查报告、线程拆分和状态回报必须使用普通 Markdown 段落、列表、表格或引用块；不得用 ` ```text `、无语言代码围栏、缩进代码块或 HTML 包裹整段自然语言输出。
- 代码围栏只用于真实代码、命令、配置片段、日志片段、JSON/YAML 等需要等宽保真的内容；若只是为了展示可读结构，应改用 Markdown 列表或表格。
EOF
)

BODY_WINDOWS_WSL=$(cat <<'EOF'
> 详细规则与命令模板见 `windows-wsl-execution-rules` 与 `windows-encoding-rules` skill。本节为写入规则文件的最小约束摘要。Windows 下普通仓库命令优先使用 Git Bash / bash；PowerShell 不作为普通仓库命令入口，只在 `.ps1`、Windows 专用 cmdlet、PowerShell profile / 编码初始化或用户明确要求时使用。代码位于 WSL 文件系统内且当前动作属于编译、运行、启动程序、测试、调试等执行类命令时，才优先进入 WSL；普通搜索、读写文件、规则检查、普通 git 盘点默认留在 Git Bash / bash。

**先看 agent 在哪运行：**

- **agent 在 WSL（推荐）**：直接 `cd /home/<user>/<project>` 执行执行类命令，普通命令也可直接在当前 shell 完成，无需任何包裹。
- **agent 在 Windows（如 Claude Desktop GUI）**：
  - 普通仓库命令优先使用 Git Bash / bash；PowerShell 只用于 `.ps1`、Windows 专用 cmdlet、PowerShell profile / 编码初始化或用户明确要求的场景
  - 看代码、改代码、搜索、规则检查、普通 git：经 `\\wsl.localhost\<distro>\home\<user>\<project>` 或 Git Bash / bash 可访问的等价路径访问 WSL 文件
  - 编译、运行、启动程序、测试、调试，以及会真实启动运行时的依赖安装：`wsl.exe --cd /home/<user>/<project> <command>`

**为什么只有执行类动作在 WSL：** 只有 WSL 进程能正常联网，且运行产物面向 Linux；普通读写、搜索、规则检查不依赖 WSL 运行时，强行切换反而容易引入路径或权限问题。

**命令格式：** 执行类命令用 `wsl.exe --cd /home/<user>/<project> <command>`（默认发行版省略 `-d`；多发行版时用 `wsl.exe -l -v` 查名后加 `-d <发行版名>`）。普通命令不要为了统一口径强制套这层。代码在 WSL 时不再使用 `/mnt/<drive>`；纯 Windows 项目或本轮不执行程序时，不要误触发本规则。

**用户可访问文件引用：** 回复用户时，凡引用项目内文件都按用户当前环境可打开的路径输出。项目在 WSL 且用户从 Windows 桌面访问时，Markdown 链接、普通文本路径、审查证据路径、截图说明和最终总结中的项目内文件路径都使用 `\\wsl.localhost\<distro>\home\<user>\<project>\...`；只有命令参数、WSL shell 上下文和日志原文保留 `/home/<user>/<project>`。

**编码约束：**

- 仓库提交 `.gitattributes` 与 `.editorconfig`，固定 UTF-8 和换行策略；任何读写文件操作都继续遵守“文件编码与写入规则”
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

PROJECT_MEMORY_MACHINE_SECTION=$(cat <<'EOF'
## 机器索引区

```yaml
version: 1
entities: []
relations: []
evidence: []
contexts: []
lifecycle:
  active: []
  deprecated: []
  stale: []
  conflicted: []
  retired: []
retrieval_hints:
  aliases: {}
  scopes: {}
  sources: {}
extensions:
  external_refs: []
  retrieval_provider: ""
  vector_doc_id: ""
  graph_node_id: ""
```
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

# 创建最小可用的 PROJECT_MEMORY.md 双区骨架；仅负责主文件与机器索引区占位，不写业务事实。
create_project_memory_file() {
  local file="$1"
  cat > "$file" <<'EOF'
# 项目记忆

## 核心记忆

- 待补充

## 变更记录

- 2026-07-03: 由 `project-agents-bootstrap` 初始化双区骨架

## 机器索引区

```yaml
version: 1
entities: []
relations: []
evidence: []
contexts: []
lifecycle:
  active: []
  deprecated: []
  stale: []
  conflicted: []
  retired: []
retrieval_hints:
  aliases: {}
  scopes: {}
  sources: {}
extensions:
  external_refs: []
  retrieval_provider: ""
  vector_doc_id: ""
  graph_node_id: ""
```
EOF
  echo "[OK] 已创建: $file"
}

# 同步 PROJECT_MEMORY.md 的结构骨架；若已有正文，只补底部受管机器索引区，不重写人工内容。
sync_project_memory_file() {
  local file="$1"

  if [[ ! -f "$file" ]]; then
    create_project_memory_file "$file"
    return 0
  fi

  # 只补双区骨架，不重写人类正文区；事实抽取与正文归并仍交给 project-memory-rules。
  $PYTHON_BIN - "$file" "$PROJECT_MEMORY_MACHINE_SECTION" <<'PY'
from pathlib import Path
import sys

path = Path(sys.argv[1])
machine_section = sys.argv[2].rstrip("\n")
text = path.read_text(encoding="utf-8")

if "## 机器索引区" not in text:
    if not text.endswith("\n"):
        text += "\n"
    text += "\n" + machine_section + "\n"
    path.write_text(text, encoding="utf-8")
    print(f"[INFO] 已追加机器索引区: {path}")
    raise SystemExit(0)

marker = "## 机器索引区"
start = text.index(marker)
fence_start = text.find("```yaml", start)
if fence_start == -1:
    insert_at = start + len(marker)
    text = text[:insert_at] + "\n\n```yaml\nversion: 1\nentities: []\nrelations: []\nevidence: []\ncontexts: []\nlifecycle:\n  active: []\n  deprecated: []\n  stale: []\n  conflicted: []\n  retired: []\nretrieval_hints:\n  aliases: {}\n  scopes: {}\n  sources: {}\nextensions:\n  external_refs: []\n  retrieval_provider: \"\"\n  vector_doc_id: \"\"\n  graph_node_id: \"\"\n```\n" + text[insert_at:]
    path.write_text(text, encoding="utf-8")
    print(f"[INFO] 已补齐机器索引区 yaml 骨架: {path}")
    raise SystemExit(0)

fence_end = text.find("```", fence_start + len("```yaml"))
if fence_end == -1:
    raise SystemExit("[ERROR] `## 机器索引区` 后缺少闭合 ```，无法安全补齐")

block = text[fence_start:fence_end]
required_blocks = [
    ("version:", "version: 1\n"),
    ("entities:", "entities: []\n"),
    ("relations:", "relations: []\n"),
    ("evidence:", "evidence: []\n"),
    ("contexts:", "contexts: []\n"),
    ("lifecycle:", "lifecycle:\n  active: []\n  deprecated: []\n  stale: []\n  conflicted: []\n  retired: []\n"),
    ("retrieval_hints:", "retrieval_hints:\n  aliases: {}\n  scopes: {}\n  sources: {}\n"),
    ("extensions:", "extensions:\n  external_refs: []\n  retrieval_provider: \"\"\n  vector_doc_id: \"\"\n  graph_node_id: \"\"\n"),
]

missing = []
for needle, snippet in required_blocks:
    if needle not in block:
        missing.append(snippet)

if missing:
    insert_at = fence_end
    prefix = ""
    if not block.endswith("\n"):
        prefix = "\n"
    text = text[:insert_at] + prefix + "".join(missing) + text[insert_at:]
    path.write_text(text, encoding="utf-8")
    print(f"[INFO] 已补齐机器索引区最小 schema: {path}")
else:
    print(f"[INFO] 机器索引区已存在且满足最小骨架: {path}")
PY
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
  sync_section "$file" "会话动态重命名规则" "$BODY_THREAD_TITLE"
  sync_section "$file" "注释任务强制流程" "$BODY_COMMENT_TASK"
  sync_section "$file" "上下文压缩续做规则" "$BODY_CONTEXT_COMPRESS"
  sync_section "$file" "文件编码与写入规则" "$BODY_CHINESE_ENC"
  sync_section "$file" "变更最小化" "$BODY_MIN_CHANGE"
  sync_section "$file" "本地连接调试测试红线（最高优先级，强制）" "$BODY_LOCAL_ONLY_CONNECTION"
  sync_section "$file" "依赖与工具复用优先规则" "$BODY_REUSE_FIRST"
  sync_section "$file" "最小实现优先级阶梯" "$BODY_MINIMAL_LADDER"
  sync_section "$file" "输出格式规则" "$BODY_OUTPUT_FORMAT"
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

# 3) 确保 PROJECT_MEMORY.md 至少具备单文件双区骨架
sync_project_memory_file "$PROJECT_MEMORY_FILE"

# 4) 同步根目录所有已存在的规则文件（AGENTS.md / CLAUDE.md）
for name in AGENTS.md CLAUDE.md; do
  sync_agents_file "$REPO_DIR/$name"
done

# 5) 同步子目录中所有已存在的 AGENTS.md / CLAUDE.md
while IFS= read -r extra_file; do
  sync_agents_file "$extra_file"
done < <(find "$REPO_DIR" -mindepth 2 \( -name AGENTS.md -o -name CLAUDE.md \) -type f | sort)
