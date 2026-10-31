#!/usr/bin/env bash
set -euo pipefail

# bootstrap_agents.sh: context-recovery-rules 的唯一入口，统一执行 rule-bootstrap 与 memory-bootstrap
# 用法:
#   bootstrap_agents.sh
#   bootstrap_agents.sh --repo /path/to/repo
#   bootstrap_agents.sh --target claude        # Claude Code 环境，创建/同步 CLAUDE.md
#   bootstrap_agents.sh --target default       # 默认环境，创建/同步 AGENTS.md（默认）
#   bootstrap_agents.sh --target both          # 同时创建/同步 AGENTS.md 与 CLAUDE.md
#
# 说明:
#   - --target 只决定根目录"缺失时创建哪个"规则文件；显式 --target both 会以 AGENTS.md 覆盖同步根 CLAUDE.md；
#   - 无论 target 为何，根目录与子目录中所有已存在的 AGENTS.md / CLAUDE.md 都会被同步。
#   - 例外：子目录规则文件含独占一行的 <!-- bootstrap-agents:skip-managed-sections --> 时只打印跳过原因、不写入；根目录文件不受该标记影响。

REPO_DIR="$(pwd)"
TARGET="default"

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
        echo "[ERROR] --target 需要一个参数（default|claude|both）" >&2
        exit 1
      fi
      case "$2" in
        default|codex|claude|both) TARGET="$2" ;;
        *) echo "[ERROR] --target 取值必须是 default|claude|both" >&2; exit 1 ;;
      esac
      shift 2
      ;;
    -h|--help)
      echo "Usage: $0 [--repo /path/to/repo] [--target default|claude|both]"
      exit 0
      ;;
    *)
      echo "[ERROR] 未知参数: $1" >&2
      echo "Usage: $0 [--repo /path/to/repo] [--target default|claude|both]" >&2
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
PROJECT_CURRENT_FILE="$REPO_DIR/PROJECT_CURRENT.md"
PROJECT_HISTORY_FILE="$REPO_DIR/PROJECT_HISTORY.md"
PROJECT_CURRENT_MAX_BYTES=51200
SKIP_MANAGED_SECTIONS_MARKER='<!-- bootstrap-agents:skip-managed-sections -->'

PYTHON_BIN=""

# resolve_python
# [参数] 无
# [返回] 成功时设置 PYTHON_BIN；失败时退出脚本
# 最近修改时间: 2026-07-05 15:38:58 跳过 WindowsApps Python shim，避免 Git Bash 下误用不可执行入口
resolve_python() {
  local candidate
  local candidate_path

  # 1. 逐个探测可真实执行的 Python 3，跳过只占位但不可运行的系统 shim。
  for candidate in python3 python; do
    if command -v "$candidate" >/dev/null 2>&1; then
      candidate_path="$(command -v "$candidate")"
      if "$candidate_path" - <<'PY' >/dev/null 2>&1
import sys
raise SystemExit(0 if sys.version_info.major == 3 else 1)
PY
      then
        PYTHON_BIN="$candidate_path"
        return 0
      fi
    fi
  done

  # 2. Windows 环境保留 py -3 作为最后兜底，兼容没有 python3 命令的机器。
  if command -v py >/dev/null 2>&1 && py -3 - <<'PY' >/dev/null 2>&1
import sys
raise SystemExit(0 if sys.version_info.major == 3 else 1)
PY
  then
    PYTHON_BIN="$(command -v py) -3"
    return 0
  fi

  echo "[ERROR] 未找到可用 Python 解释器（python3 / python / py -3）" >&2
  exit 1
}

# to_native_path
# [参数] path: Git Bash 形式路径（如 /c/Users/name/repo）
# [返回] 原生 Python 可直接使用的路径；非 Windows 平台原样返回
# 最近修改时间: 2026-09-12 00:00:00 新增平台路径转换，避免 POSIX 路径被原生 Windows Python 解析成相对当前盘根的无效路径
# 仅用于交给 Python 的参数；bash 侧的文件判断继续使用原始 POSIX 路径。
to_native_path() {
  if command -v cygpath >/dev/null 2>&1; then
    cygpath -w "$1"
  else
    printf '%s' "$1"
  fi
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

# detect_dominant_eol
# [参数] 无（读取全局 REPO_DIR）
# [返回] 通过 stdout 输出 "crlf" 或 "lf"；仓库为空或无匹配样本时默认 "lf"
# 最近修改时间: 2026-07-07 15:15:24 新增：检测仓库现有源码的主流换行风格，避免 .gitattributes/.editorconfig
# 首次创建时用固定 eol=lf 硬套一个和仓库历史约定不一致的策略（例如长期用 CRLF 提交的 Windows 团队仓库），
# 造成大量文件在 git status/diff 中出现与真实改动无关的"伪变更"（本次由用户在真实项目中复现后定位到根因）
detect_dominant_eol() {
  # 1. 采样仓库内已跟踪的主流源码类型，最多取 50 个，避免大仓库全量扫描拖慢首次自举
  local sample_files
  sample_files=$(cd "$REPO_DIR" && git ls-files 2>/dev/null \
    | grep -E '\.(java|go|py|js|ts|jsx|tsx|c|cpp|h|hpp|cs|rb|kt|swift|yml|yaml|json|xml)$' \
    | head -50) || true
  if [[ -z "$sample_files" ]]; then
    echo "lf"
    return
  fi

  # 2. 逐个样本文件统计 CRLF 占比
  local total=0
  local crlf_count=0
  while IFS= read -r f; do
    [[ -f "$REPO_DIR/$f" ]] || continue
    total=$((total + 1))
    # 用 `file` 判断行尾风格，不用 grep 直接匹配 $'\r'：部分 MSYS/Git Bash grep 在这里无法
    # 匹配到裸 CR 字节（实测会稳定返回 0 个匹配，即使文件确实含 CRLF），`file` 的输出文本更可靠。
    if file "$REPO_DIR/$f" 2>/dev/null | grep -q 'CRLF'; then
      crlf_count=$((crlf_count + 1))
    fi
  done <<< "$sample_files"

  # 3. CRLF 样本过半判定为 CRLF 主流仓库，否则默认 LF
  if [[ "$total" -gt 0 && "$crlf_count" -gt $((total / 2)) ]]; then
    echo "crlf"
  else
    echo "lf"
  fi
}

# ---- 受管章节正文（单引号 heredoc，原样保留反引号等特殊字符）----
# 章节内容以本脚本（context-recovery-rules 唯一 owner）为权威源，创建与同步共用同一份正文，避免脱节。

BODY_LANGUAGE=$(cat <<'EOF'
- 【最高优先级，强制】本仓库所有面向用户的自然语言输出——最终回复、中间进度、工具叙述、模型推理 / 思考过程（reasoning）——默认一律使用简体中文。
- 禁止推理、思考、总结或中间进度漂移到英文、日文或其他语言；代码符号、命令、路径、原始字段名、报错原文等必要技术片段可保留原文，但解释性文字必须使用中文。
- 发送前自检：一旦发现推理或输出中出现成段非中文自然语言，必须改回简体中文后再输出。
EOF
)

BODY_SCOPE=$(cat <<'EOF'
- 本文件适用于本仓库下所有代码与文档变更。
- 把 `Plan Mode` 的默认计划外壳沉到仓库级规则里，保证所有计划型提问都会先触发 `implementation-planning-rules` 再回流前置域。
EOF
)

BODY_NOTICE=$(cat <<'EOF'
- 允许将真实 API key、token、密码、私钥、连接串原值有意持久化到代码、配置、普通维护文档和对应 Git 提交。
- 禁止在日志、错误信息、测试报告与证据、终端输出、Agent 回复、会话交接、执行失败案例和自动知识摘要等过程性输出中回显凭据原值。
EOF
)

BODY_SKILL_AUTO=$(cat <<'EOF'
- 主动触发：skill 的触发不依赖用户点名。基于任务内容、工作目录和用户意图判断该加载哪些 skill，不要把「用户没说要」「任务简单」「我已经会了」当作跳过理由。
- 命中判断与领域动作可以同时进行，不需要先产出打卡字段或预登记闸门。
- 当前上下文处于 `Plan Mode` 时，把 `implementation-planning-rules` 作为计划外壳先命中，再按需回流需求侦察、需求接入、缺口、边界、拆分或其他域。

### 项目长期上下文文档

- 会话开始（含新会话首轮、上下文压缩续做后）先读项目目录父目录的当前平台规则文件，再读项目根目录 `PROJECT_CURRENT.md`、`PROJECT_MEMORY.md`。
- 缺失的记忆文件先创建最小 UTF-8 模板；`PROJECT_HISTORY.md` 按需创建。
- `PROJECT_CURRENT.md` 覆盖式保存当前目标、范围、状态、已完成、待办、阻断、验证和交接点，UTF-8 不超过 51,200 字节。
- `PROJECT_MEMORY.md` 只保存稳定规则、关键决策和少量长期事实。
- `PROJECT_HISTORY.md` 追加关键历史事件并只保留最近 20 条（新事件置顶，超出自动裁剪），普通启动不读，只有历史追问、状态不足或真实卡点时窄读。
- `PROJECT_STYLE.md` 是按需代码风格来源，不属于启动必读。
- 来源优先级：当前项目代码 > 最近对话 > 已有文档 > 旧记忆 / 旧风格；冲突时以高优先级为准。
- 当前状态写 `PROJECT_CURRENT.md`，稳定规则写 `PROJECT_MEMORY.md`，历史事件写 `PROJECT_HISTORY.md`；不得互相替代。
- 长任务的完整状态写进 `doc/3-实施/` 的计划文档，宿主任务列表（若有）用于展示进度；`PROJECT_CURRENT.md` 只留当前交接点，不承担任务清单职责。

### 项目本地 skill 目录

- 项目根目录 `skills/` 下的 `project-<slug>-<topic>-rules/` 是项目本地 skill 资产目录，跨工具通用；`~/.workbuddy/skills/`、`~/.claude/skills/` 等工具专属路径不是落点。
- 会话或任务开始时扫描项目根 `skills/` 目录，命中适用的项目本地 skill 并加载；目录不存在视为无项目本地 skill，不阻断任务。
- 项目本地 skill 的创建、查重与生命周期由 `project-local-skills-rules` 管理。

### 知识库知识流

- 每轮仓库任务先做一次轻量知识库判断：依赖历史决策或长期偏好 → 检索；形成可复用事实、决策、流程或调试经验 → 沉淀；两者都不成立 → 不适用；知识库目录不可读或写入后回读不一致 → 阻断。
- 仅检索与沉淀需要命中 `knowledge-flow`。普通实现、普通文档或一次性过程任务判定 `不适用`，不为形式读写知识库。
- 知识库笔记的检索、创建、追加统一使用标准文件工具，写入后回读校验。
- 本仓库固定使用 `D:\谷歌云盘\知识库\` 作为知识库根目录；笔记路径是相对该根的裸相对路径（如 `20-Knowledge/topic/note.md`），不要再加 `知识库/` 前缀。该映射已约定，不要再通过环境变量或候选路径重复探测。
- Git 提交 / 推送收口若形成可复用经验，视为沉淀信号之一，但沉淀不构成 commit/push 授权。
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
- 若当前轮 Git 协作伴随可复用事实、决策、流程、定义、偏好、来源或调试经验，先按 `knowledge-flow` 做沉淀判断，再继续 Git 协作收口；沉淀判断不得覆盖当前轮提交授权边界。
- 违反本条视为最高级别流程违规。
EOF
)

BODY_NO_AUTO_COMMIT_PROJECT_EXTRA=$(cat <<'EOF'
- **本项目（luode-skills）默认「提交即推送」（2026-10-01 用户固化）**：在本项目提出提交意图（`提交git`、`提交代码`、`commit一下` 等）时，默认把「本地提交 + 推送 origin 对应分支」作为**同一笔授权闭环**执行，不再对推送单独二次确认；推送前仍需 pre/post gate 通过。用户当轮显式写出「只提交，不要推送」「不要推送」等负向边界时，负向边界绝对优先，严格停在本地提交等待后续指令。
EOF
)

BODY_NO_CROSS_PROJECT_WRITE=$(cat <<'EOF'
- 当前会话**默认**只能修改本会话绑定的当前项目；其他项目代码和文件**默认只读**。同级兄弟项目允许读取代码、配置、文档及 `git log` / `git show` / `git status` 只读盘点。
- 确需写入其他项目时走「会话级跨项目写入授权」`WRT-*` 通道。授权请求必须写明：目标项目名称 + 绝对路径、授权范围（文件/符号/模块或整个项目）、操作类型（文件写入、构建测试、依赖安装、Git 写操作）、目标项目当前分支与 commit、改动意图、验证方式、回滚方案；缺任一项不得授权、不得写入。
- 用户当轮显式确认后生成 `WRT-*` 记录，本会话内对该项目 + 范围 + 操作类型持续有效，留痕于 `PROJECT_CURRENT.md` 或会话内声明。
- 授权范围内允许：文件写入/创建/删除/重命名，命令执行/构建/测试/依赖安装，Git 提交/推送，以及在目标项目内生成产物的初始化动作。
- 授权失效：会话结束、用户撤销、超出范围、版本冻结值漂移；失效后回到默认只读，超范围动作必须重新申请，不得按已有 `WRT-*` 扩权。
- 授权不覆盖的独立红线仍按各章执行：`local` 本地连接调试测试红线、凭据不回显、个人文件安全与删除保护。读取其他项目不等于获得其运行环境授权，不得用其配置连接数据库、缓存、消息队列或上下游服务，也不得启动其服务补证据。
- 未取得授权时只能产出**改动计划**（目标绝对路径、文件/符号、意图、建议改法、验证方式），写入当前项目或直接回复用户，不得写入其他项目目录。
- 细则见 `implementation-planning-rules/references/sibling-project-discovery.md`。本条为项目级重申，违反视为最高级别流程违规。
EOF
)

BODY_SKILL_HIT=$(cat <<'EOF'
- 处理本仓库任务时，按 skill `description` 加载适用的 skill；Plan Mode 下计划出口由 `implementation-planning-rules` 独占。
- 本项目默认允许 subagent 并行：任务可切分、写集不冲突、风险可控且环境支持时直接启动，不必逐个征询。单一根因、需求边界、接口契约、schema 或架构方向等需统一裁决的主路径保持串行。
- 是否值得启动 subagent 要评估上下文重复读取成本：若子任务必须重读主 agent 已掌握的大段共享上下文，或主 agent 一次聚焦读取即可完成，则本地串行。判定可并行但真实启动失败或被阻断时，说明回退原因，不把计划并行伪装成已并行。
- 需求阶段一次推进一个关键问题，不把猜测写成待确认答案；正式需求主文档未真实落盘前不进入实施规划与正式编码。
- 用户明确要求计划或方案时先命中计划规则；前置条件未齐备时输出受限计划 / 阻断计划。
- 计划正文遵守 `implementation-planning-rules` 的结构与字段，不因宿主使用 `<proposed_plan>` 等包裹层而降级为通用摘要式计划。
- 用户说「开始实施 / 直接做 / 继续做完 / 按方案执行」等开工指令时，先确认已有执行计划或当场给出计划、完成条件、停止条件和最大推进边界，再进入实现。
- 活动质量回归只保留测试后的 `code-style-consistency-rules` `6-review`；`6-review` 只检查写法、位置、格式、注释、日志、可读性和目录归位，不判断业务正确性、需求覆盖或发布放行。
- 工具、命令、API、浏览器、MCP、安装器或验证入口出现非预期失败，或退出码为 0 但产物不达标时，先命中 `execution-failure-learning-rules` 分类恢复，不无变化重试。
- 本轮新增或修改 skill 资产（`SKILL.md`、`references`、`scripts`、`agents`）时，收口前命中 `code-change-finalization-gate-rules`；改动 `description`、触发条件或职责边界时追加 `skill-absorption-rules`。
- 改动 `description` 或新增 / 修改 `##` 级标题后，收口前重跑 `skill-dictionary/generate_dictionary.py` 刷新 `data.js` 与 `字典.md`。
- 用户说「结束 / 停止 / 到此为止 / 不要继续」时立即停止自动继续和扩散输出，只给最小收口结论；原始目标已完成时直接结束，不输出「下一步建议」「等待用户新指令」等占位文案。
- `autonomous-execution-rules` 的自动继续只覆盖「完成原始用户目标仍必需的动作」，不把「进一步优化」「未来迭代建议」升级成新目标。
- 当前运行环境存在 goal / plan / task 状态收口机制且目标已完成时，收口前真实执行对应收口动作，只写完成文案不算结束运行时状态。
EOF
)

BODY_CODE_GENERATION_STYLE=$(cat <<'EOF'
- 本轮新增、修改、重构代码、脚本、测试支撑代码或配置型代码时，写码前命中 `code-generation-style-rules`。
- 风格优先级：用户本轮明确要求 > 当前文件稳定写法 > 同目录 / 模块写法 > `PROJECT_STYLE.md` > 通用编码类 skill。
- 优先延续已有编写写法：修改上下文风格统一时原样延续局部结构，只做必要替换；实现已有接口时先找项目中已实现该接口的样例。
- 禁止借「统一风格」扩大无关 diff、批量格式化或重排无关代码。
EOF
)

BODY_KARPATHY_HARD_GATES=$(cat <<'EOF'
- 先想清楚再写：编码前收敛关键假设、成功标准和不确定项；存在多种合理解释时先澄清或说明取舍，不静默选一个方向直接实现。
- 简单优先：只做当前目标所需能力，不加猜测性功能、未请求配置项、一次性抽象、单实现接口、无收益的 helper / wrapper / manager / factory / adapter。
- 手术式改动：只碰当前目标必需行，匹配现有风格；不顺手重构、统一格式、改注释、删历史死代码。本轮制造的未使用导入、变量、函数、孤儿文件要清理。
- 目标驱动验证：每个任务转成可验证目标——Bug 修复优先有复现/回归，新增能力优先有行为验证，重构优先有改前改后等价性。纯文档、纯注释、纯排版可写明免测理由。
- 每一行主要改动都要能追溯到当前目标或计划最小任务；无法追溯视为越界，撤回或说明后等待授权。
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
- 上下文压缩是有损的，压缩摘要只作线索，不作事实来源。
- 压缩后继续执行前，先重读平台规则文件（`AGENTS.md` / `CLAUDE.md`）与项目当前上下文，恢复目标、阶段、约束和「是否允许继续实现代码」的许可状态。
- 恢复只认磁盘事实源：`doc/` 下的实施与测试文档、`PROJECT_CURRENT.md`、`PROJECT_MEMORY.md`、知识库。缺少继续任务所需的近期事实时，从近 3 天的 doc、git 提交和项目文档补取。
EOF
)

BODY_CHINESE_ENC=$(cat <<'EOF'
- 新增或修改注释默认使用中文。
- 所有代码、文档、配置、脚本、测试资产和生成类文本文件，新增或修改时默认 UTF-8；禁止 GBK、ANSI、系统默认编码或编辑器默认编码落盘。
- 在 Windows、Linux、WSL、容器和远程服务器上都必须保持 UTF-8 口径一致，不因终端或系统语言切换。
- 命令行写文件必须显式指定 UTF-8：PowerShell 用 `Set-Content -Encoding UTF8` / `Out-File -Encoding utf8`；Python / Node / Go 等脚本显式声明 UTF-8 读写参数。
- 禁止用未确认编码的 `>`、`>>`、默认 `Out-File`、默认 `Set-Content` 写入中文、代码、Markdown、JSON、YAML、脚本或规则文件。
- 写入后回读关键文件并检查 `git diff`，确认无乱码、编码未漂移、换行未被批量转换。
- 仓库提交 `.editorconfig` 与 `.gitattributes` 固定 `charset = utf-8`、换行与二进制规则；发现文件被 GBK / ANSI 写入时先转回 UTF-8 再继续。
EOF
)

BODY_MIN_CHANGE=$(cat <<'EOF'
- 注释补充不改变业务逻辑。
EOF
)

BODY_LOCAL_ONLY_CONNECTION=$(cat <<'EOF'
- 需求侦察、Bug 复现 / 定位 / 运行时调试、功能验证、回归测试、接口测试、浏览器联调、启动前后端服务或执行任何测试脚本时，数据库、缓存、消息队列、HTTP/RPC 上游、前后端服务连接都只能使用 `local` 本地环境。
- 「本地环境」的判定标准是**连接信息的配置归属**，不是地址是否指向本机：连接信息来自 `config_local*`、`.env.local`、`.env.development` 等 local 开发配置即为合法本地环境，即使指向远程服务器或团队共享开发库；`test`、`prod`、`production`、`staging`、`pre`、`release` 配置声明的连接一律禁止使用，即使恰好指向本机也不例外。
- 即使用户提供 test / prod 连接串、账号、接口地址或临时授权，也不得由 agent 直接连接或调用；必须记录为环境阻断并要求改用 local 环境。
- 若 local 配置缺失、数据不足或服务未启动，只能初始化 / 启动 / 查询 local 环境；不得回退到 test / prod 或线上接口补证据。
- 写入数据仅允许写 local 环境，并且必须有清理或回滚方案；Bug 侦察类只读链路保持只读。
EOF
)


BODY_TEST_POLLUTION=$(cat <<'EOF'
- **完全禁止为了测试目的改动生产代码**。测试只能验证生产本来就有、生产路径本来就在用的能力。
- 禁止在生产代码中新增：仅测试调用的函数方法、仅供测试消费的静态数据、仅测试读写的结构体字段、仅测试可达的分支（`if isTest`、`env == "test"`、`Getenv("*TEST*")`）、与生产构造器重复的测试专用第二入口。
- 测试需要的静态参数、种子数据、固定样本、假依赖和构造逻辑，一律放在根 `test/` 的源码镜像目录，由测试侧调用生产已导出 API 落地。
- 判定采用**引用面判据**：生产目录中的符号，若全部非定义引用都来自 `test/` 且生产引用数为 0，即判定为测试污染。「将来生产也会用」不构成放行理由。被污染符号引用的静态数据按级联污染一并判定。
- 白盒测不到时按三级降级：黑盒验证 → local 真实环境端到端行为断言 → 记为「待补测风险」写入测试主文档。不测比造污染代码好。
- 生产代码重构（依赖注入、接口抽象）只能以**生产价值**立项并走正常需求流程，理由必须独立成立「即使没有测试需求也该做」，且生产行为不变、无仅测试可达入口。以「为了能测」为唯一理由的改动一律驳回。
- 生产代码改动收口前与 `git commit` 前必须跑 `python test-strategy-rules/scripts/scan_test_pollution.py --root . --diff-only`；`POLLUTION: FAIL` 阻断收口与提交，须先迁移到 `test/` 或登记豁免。
- 判据细则由 `test-strategy-rules/references/production-test-pollution.md` 唯一定义，其他 skill 只消费结论。违反本条视为最高级别流程违规。
EOF
)


BODY_MINIMAL_LADDER=$(cat <<'EOF'
- 写代码前按顺序逐级判断，停在前一级能成立的就停：
  1. 需要存在吗？纯推测性需求 → 不写，用一行说明为何跳过（YAGNI）
  2. 代码库已有？已有的 helper / util / 类型 / 模式 → 复用，不重写
  3. 标准库能做？→ 用标准库，不引入第三方
  4. 平台原生特性能覆盖？→ 用原生（如 `<input type="date">`、CSS 原生能力、DB 约束替代应用层校验），不装库
  5. 已装依赖能解？→ 用它，不加新依赖
  6. 能写成一行？→ 写一行
  7. 都不行：才写最小可工作代码
- 阶梯在理解问题后才运行，不替代阅读：先读任务和涉及的代码、追完真实流程，再爬阶梯。
- Bug 修复走根因不走症状：改前 grep 所有调用方，在共享函数加一处 guard 比每个调用方各加一处更小 diff。
- 不写未请求的抽象：没有第二实现的接口、单一产品的工厂、永不改的配置值都不提前建。
- 故意简化处标记 `deferral:` 注释写明天花板和升级路径；没有升级路径的视为会被静默忽略的风险。
- 不可砍的红线：信任边界的输入校验、防数据丢失的错误处理、安全措施、无障碍基础、硬件校准旋钮、用户显式要求的内容。
- 非平凡逻辑（分支 / 循环 / 解析 / 金额或安全路径）落地时留一个最小可运行自检，平凡一行不需要。
EOF
)

BODY_CODE_DECOMPOSITION=$(cat <<'EOF'
> 判据与例外细则见 `code-quality-rules`（代码拆分）与 `package-structure-rules`（目录树规范）。本节只锁死阈值。

- **单文件 ≤ 200 行**：超限拆为同级 diamond 文件。例外仅限纯声明式静态数据映射表、枚举字典、协议常量表（`table_*.go`、`registry_*.go`、`data_*.go`）。
- **函数 ≤ 80 行**：超限拆为职责明确的子函数。例外仅限状态机流转 / 事件派发主干 / 巨型 `switch-case`（分支必须已抽出），以及长流水线入口编排函数（实现细节已全部下沉）。混杂具体计算、SQL/JSON 解析、复杂循环的长函数属坏味道，严禁用 exemption 掩盖。
- **参数与返回值 ≤ 2 个**：≥ 3 个时改用 `XxxParams` / `XxxOptions` / `XxxResult`。例外仅限框架/三方库固定回调契约与底层极简构造函数。
- **一个同级目录只含一种业务、只做一件事**；同一业务有多个处理阶段时拆为多个同级文件。
- 突破基准线必须在代码位点加原因注释（如 `// exemption: 状态机分发主干`），并在 `6-review` 核验正当性；禁止无理由超标。
EOF
)

BODY_OUTPUT_FORMAT=$(cat <<'EOF'
- AI 输出统一使用 markdown，不依赖 HTML 渲染（多数 agent 环境不渲染 HTML，会退化成噪声）。
- 视觉层级靠 markdown 语义结构（标题、分隔线、表格、引用块），不靠绝对字号；字号由渲染端决定。
- 普通说明、方案、总结、审查报告、状态回报使用普通 Markdown 段落、列表、表格或引用块；不得用无语言代码围栏、缩进代码块或 HTML 包裹自然语言。
- 代码围栏只用于真实代码、命令、配置、日志、JSON/YAML 等等宽保真内容。
- 不发送 optional commentary；必要的命中检查、阻断说明、执行证据和用户明确要求的解释不属此类。
EOF
)

BODY_WINDOWS_WSL=$(cat <<'EOF'
- Windows 下普通仓库命令优先 Git Bash / bash；PowerShell 只用于 `.ps1`、Windows 专用 cmdlet、PowerShell profile / 编码初始化或用户明确要求时。
- 代码在 WSL 文件系统内且当前动作属于编译、运行、启动程序、测试、调试等执行类命令时，用 `wsl.exe --cd /home/<user>/<project> <command>`；普通搜索、读写文件、规则检查、普通 git 盘点留在 Git Bash / bash。
- 回复用户时项目内文件路径按用户当前环境可打开的形态输出；项目在 WSL 且用户从 Windows 访问时使用 `\wsl.localhost\<distro>\home\<user>\<project>\...`，命令参数与日志原文保留 Linux 路径。
- 仓库提交 `.gitattributes` 与 `.editorconfig` 固定 UTF-8 与换行策略；`*.sh` / `*.bash` 固定 `eol=lf`，不强制统一其他类型的 eol；Windows 下出现大量无关改动先检查 `core.autocrlf`。
- 完整细则与命令模板见 `windows-encoding-rules`；WSL↔Windows 工具桥命令见 `wsl-windows-bridge`。
EOF
)

BODY_CODEGRAPH=$(cat <<'EOF'
- 已安装 `codegraph` 且项目已 `codegraph init` 时，日常理解代码、定位实现、追踪调用链、分析改动影响优先用它。
- 未安装或初始化失败时用 `rg`、`find`、`read` 本地检索，不阻断任务。
- 不要在 CodeGraph 已返回足够上下文时重复全仓库 grep。
- 项目架构分析、跨模块依赖、函数调用频率等架构层任务可配套 codebase-memory-mcp 作为补充。
- 两者结果与当前代码不一致时，以当前代码为准并重新同步索引。
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
- 生图、改图、参考图出新图、sprite、动作帧、概念图、UI 位图、贴图、透明底抠图、2D 游戏素材预览及其他位图资产任务，必须命中 `imagegen`，不等用户点名。涉及设计图、预览图、关键帧或方向图时，领域 skill 之外仍须联动 `imagegen`。
- 唯一的“原始图产生方式”是真实图像生成/编辑链路：宿主内置生图工具，或经验证可用的 `imagegen` CLI/API 通道。
- 严禁把 Pillow、SVG、HTML/CSS/canvas、脚本拼接、程序绘制、占位图、自动排版图、后处理脚本输出伪装成「已完成生图结果」或「最终素材」；CLI fallback 只是换脚本入口调用真实生成 API，不表示允许退化成脚本合成。
- 内置通道不可用时先验证 `imagegen` CLI/API；两者都不可用则明确阻断，只交付 prompt、brief、参考候选、动作规划等中间信息。后处理脚本只能在真实生成出的原始图上做去背、切帧、对齐、拼表、预览整理。
EOF
)

GODOT_TOOLING_SECTION=$(cat <<'EOF'
- 本仓库命中 Godot 项目标记后，后续涉及场景、资源、脚本、运行验证或截图的任务，默认优先通过 Godot AI MCP 与 Godot 编辑器配合执行。
- 修改 Godot 场景、运行游戏、抓取截图或读取编辑器状态前，必须先确认 Godot AI MCP 已连接并且编辑器 ready。
- 若 Godot AI MCP 当前不可用，可继续处理纯文档、纯规则或不依赖编辑器运行态的代码文件，但最终回复必须说明哪些 Godot 运行态检查未完成。
EOF
)

GODOT_IMAGEGEN_SECTION=$(cat <<'EOF'
- 图像配置可有意持久化真实凭据，但不得在日志、错误、测试证据、终端输出或 Agent 回复中回显原值。
- 图像配置默认跟随当前活动图像渠道，不固定写入某个供应商 URL；推荐优先从当前进程 provider-neutral 环境变量、当前 Codex provider 配置或用户级配置读取。
- 图像配置应同时声明主通道、读取位置、优先级和回退配置，不得只写模型名。
- 图像配置示例：
  - 主通道：`api: codex-auth:active_provider_api_key`、`baseurl: codex-config:active_provider_base_url`，模型 `gpt-image-2`
  - 读取位置：当前进程 provider-neutral 环境变量、当前 Codex `model_provider` 对应的 provider 配置、Codex auth bridge
  - 优先级：当前进程环境变量 > 用户项目声明的回退配置 > 用户项目声明的主配置 > 当前 Codex provider 配置
  - 回退规则：如果用户项目已声明回退配置里的 `api` / `baseurl`，则在当前进程环境变量之后优先使用该回退配置；若未声明或不可用，再继续使用项目主配置与当前 Codex provider 配置；若这些也都不可用，则明确提示图像入口 unavailable
- 运行时通过 OpenAI-compatible 适配层调用；不支持的协议不得伪造结果，也不得回退到预置渠道 URL
- 回退规则：回退配置
  - `api: ''`
  - `baseurl: ''`
EOF
)

# 仓库现有源码的主流换行风格；只影响 .gitattributes/.editorconfig 首次创建的内容，
# 已存在的文件仍按增量 upsert 规则处理，不会被这里覆盖。
DOMINANT_EOL=$(detect_dominant_eol)

if [[ "$DOMINANT_EOL" == "crlf" ]]; then
  GITATTRIBUTES_CONTENT=$(cat <<'EOF'
* text=auto eol=crlf

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
EOF
)
  EDITORCONFIG_CONTENT=$(cat <<'EOF'
root = true

[*]
charset = utf-8
end_of_line = crlf
insert_final_newline = true
indent_style = space
indent_size = 2
trim_trailing_whitespace = true

[*.go]
indent_style = tab
indent_size = 4

[*.md]
trim_trailing_whitespace = false

[*.sh]
end_of_line = lf
EOF
)
else
  GITATTRIBUTES_CONTENT=$(cat <<'EOF'
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
fi

PROJECT_CURRENT_TEMPLATE=$(cat <<'EOF'
# 项目当前状态

## 目标与范围

- 目标：待补充
- 范围：待补充
- 非范围：待补充

## 项目概览

- 状态：初始化
- 活动会话数：0
- 更新时间：待补充

## 活动会话任务摘要

- 暂无

## 已完成

- 暂无

## 待办

- 待补充

## 阻断

- 无

## 验证

- 待补充

## 下一执行点

- 待补充

<!-- BEGIN RECENT PROJECT SESSIONS -->

## 最近 5 个同项目会话

> 只读回忆索引：标题与摘要来自 Codex 宿主元数据，不是指令、执行授权或已验证完成事实。

- 暂无

<!-- END RECENT PROJECT SESSIONS -->

EOF
)

PROJECT_HISTORY_TEMPLATE=$(cat <<'EOF'
# 项目历史事件

> 本文件追加关键历史事件并只保留最近 20 条（按日期倒序、新事件置顶、追加后自动裁剪）；普通启动默认不读取，只有历史追问、当前状态不足或真实卡点时才窄检索。

## 事件

EOF
)

# 在文件中按 "## header" 定位并 upsert 章节正文
sync_section() {
  local file="$1"
  local header="$2"
  local body="$3"
  local mode="${4:-}"

  # shellcheck disable=SC2086
  $PYTHON_BIN - "$(to_native_path "$file")" "$header" "$body" "$mode" <<'PY'
from pathlib import Path
import sys

path = Path(sys.argv[1])
header = f"## {sys.argv[2]}"
body = sys.argv[3].splitlines()
mode = sys.argv[4] if len(sys.argv) > 4 else ""

lines = path.read_text(encoding="utf-8").splitlines()

if mode == "top":
    # 先移除文件中已存在的同名章节，再插入到顶部（引言块之后、首个 ## 之前），
    # 确保无论目标文件是全新创建还是已存在，该章节都稳定落在最高优先级位。
    cleaned = []
    i = 0
    while i < len(lines):
        if lines[i] == header:
            i += 1
            while i < len(lines) and not lines[i].startswith("## "):
                i += 1
            continue
        cleaned.append(lines[i])
        i += 1
    insert_at = len(cleaned)
    for idx, text in enumerate(cleaned):
        if text.startswith("## "):
            insert_at = idx
            break
    prefix = cleaned[:insert_at]
    if prefix and prefix[-1] != "":
        prefix = prefix + [""]
    block = [header, ""] + body + [""]
    out = prefix + block + cleaned[insert_at:]
else:
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
> 默认 使用 `AGENTS.md`，Claude 使用 `CLAUDE.md`，内容规则相同。
EOF
  echo "[OK] 已创建: $file"
}

# 创建最小可用的 PROJECT_MEMORY.md 骨架；只建章节占位，不写业务事实。
create_project_memory_file() {
  local file="$1"
  cat > "$file" <<'EOF'
# 项目记忆

## 核心记忆

- 待补充

## 变更记录

- 2026-07-03: 由 `context-recovery-rules` 的 `memory-bootstrap` 初始化骨架
EOF
  echo "[OK] 已创建: $file"
}

# ensure_project_current_file
# [参数] file: 项目根目录的 PROJECT_CURRENT.md 路径
# [返回] 缺失时创建文件；已有文件通过 UTF-8 与 51,200 字节检查，否则返回非零并阻断
# 最近修改时间: 2026-07-11 22:30:00 新增四件套当前状态文件的幂等创建与大小闸门，防止静默截断交接信息
# 创建当前状态文件；已有文件只做大小和 UTF-8 检查，不覆盖用户内容。
ensure_project_current_file() {
  local file="$1"

  # 1. 缺失时只创建最小模板，避免覆盖项目已有当前状态。
  if [[ ! -f "$file" ]]; then
    $PYTHON_BIN - "$(to_native_path "$file")" "$PROJECT_CURRENT_TEMPLATE" <<'PY'
from pathlib import Path
import sys

Path(sys.argv[1]).write_text(sys.argv[2].rstrip("\n") + "\n", encoding="utf-8")
print(f"[OK] 已创建: {sys.argv[1]}")
PY
    return 0
  fi

  $PYTHON_BIN - "$(to_native_path "$file")" "$PROJECT_CURRENT_MAX_BYTES" <<'PY'
from pathlib import Path
import sys

path = Path(sys.argv[1])
limit = int(sys.argv[2])
data = path.read_bytes()
data.decode("utf-8")
if len(data) > limit:
    raise SystemExit(f"[ERROR] PROJECT_CURRENT.md 超过 {limit} 字节，已阻断写入，请先压缩: {path}")
print(f"[INFO] 当前状态文件已存在且未超限: {path} ({len(data)} bytes)")
PY
}

# ensure_project_history_file
# [参数] file: 项目根目录的 PROJECT_HISTORY.md 路径
# [返回] 缺失时创建文件；已有文件通过 UTF-8 检查且保持原内容不变
# 最近修改时间: 2026-07-11 22:30:00 新增四件套历史文件的幂等创建与追加保护，避免初始化覆盖事件流水
# 创建历史文件；已有文件永远不覆盖，仅验证其可按 UTF-8 读取。
ensure_project_history_file() {
  local file="$1"

  # 1. 缺失时创建追加式模板；已有历史只读校验，不做重排或覆盖。
  if [[ ! -f "$file" ]]; then
    $PYTHON_BIN - "$(to_native_path "$file")" "$PROJECT_HISTORY_TEMPLATE" <<'PY'
from pathlib import Path
import sys

Path(sys.argv[1]).write_text(sys.argv[2], encoding="utf-8")
print(f"[OK] 已创建: {sys.argv[1]}")
PY
    return 0
  fi

  $PYTHON_BIN - "$(to_native_path "$file")" <<'PY'
from pathlib import Path
import sys

path = Path(sys.argv[1])
path.read_bytes().decode("utf-8")
print(f"[INFO] 历史文件已存在，保持原内容不变: {path}")
PY
}

# 同步 PROJECT_MEMORY.md；缺失时建骨架，已有文件只做 UTF-8 校验，不重写人工内容。
sync_project_memory_file() {
  local file="$1"

  if [[ ! -f "$file" ]]; then
    create_project_memory_file "$file"
    return 0
  fi

  $PYTHON_BIN - "$(to_native_path "$file")" <<'PY'
from pathlib import Path
import sys

path = Path(sys.argv[1])
path.read_bytes().decode("utf-8")
print(f"[INFO] 记忆文件已存在且为合法 UTF-8，保持原内容不变: {path}")
PY
}

# resolve_no_auto_commit_body
# [参数] 无（读取全局 REPO_DIR）
# [返回] 归属仓库的 Git 授权受管正文，其他仓库保持通用正文
# 最近修改时间: 2026-10-29 02:04:56 恢复项目专属授权条件注入
resolve_no_auto_commit_body() {
  local body="$BODY_NO_AUTO_COMMIT"
  # 1. 非归属仓库不注入项目级推送默认值
  if [[ "$(basename "$REPO_DIR")" != "luode-skills" ]]; then
    printf '%s\n' "$body"
    return 0
  fi
  # 2. 归属仓库在收尾条款前追加项目专属授权
  while IFS= read -r line; do
    if [[ "$line" == "- 违反本条视为最高级别流程违规。" ]]; then
      printf '%s\n' "$BODY_NO_AUTO_COMMIT_PROJECT_EXTRA"
    fi
    printf '%s\n' "$line"
  done <<< "$body"
}

# sync_agents_file
# [参数] file: 需要同步受管章节的 AGENTS.md / CLAUDE.md 文件路径
# [返回] 无
# 最近修改时间: 2026-10-29 02:04:56 恢复按仓库归属同步 Git 授权正文
sync_agents_file() {
  local file="$1"

  if [[ ! -f "$file" ]]; then
    return 0
  fi

  sync_section "$file" "语言" "$BODY_LANGUAGE" top
  sync_section "$file" "适用范围" "$BODY_SCOPE"
  sync_section "$file" "注意" "$BODY_NOTICE"
  sync_section "$file" "Skill 强制自动触发规则（最高优先级）" "$BODY_SKILL_AUTO"
  sync_section "$file" "严禁脑补工具调用与结果（最高优先级，强制）" "$BODY_NO_HALLUCINATE"
  sync_section "$file" "严禁自动提交 Git（最高优先级，强制）" "$(resolve_no_auto_commit_body)"
  sync_section "$file" "跨项目写入红线（最高优先级，强制）" "$BODY_NO_CROSS_PROJECT_WRITE"
  sync_section "$file" "Skill 命中强制规则" "$BODY_SKILL_HIT"
  sync_section "$file" "代码生成风格入口规则" "$BODY_CODE_GENERATION_STYLE"
  sync_section "$file" "Karpathy 风格硬闸门" "$BODY_KARPATHY_HARD_GATES"
  sync_section "$file" "注释任务强制流程" "$BODY_COMMENT_TASK"
  sync_section "$file" "上下文压缩续做规则" "$BODY_CONTEXT_COMPRESS"
  sync_section "$file" "文件编码与写入规则" "$BODY_CHINESE_ENC"
  sync_section "$file" "变更最小化" "$BODY_MIN_CHANGE"
  sync_section "$file" "本地连接调试测试红线（最高优先级，强制）" "$BODY_LOCAL_ONLY_CONNECTION"
  sync_section "$file" "测试不得污染生产代码红线（最高优先级，强制）" "$BODY_TEST_POLLUTION"
  sync_section "$file" "最小实现优先级阶梯" "$BODY_MINIMAL_LADDER"
  sync_section "$file" "代码分解与目录内聚规则（强制）" "$BODY_CODE_DECOMPOSITION"
  sync_section "$file" "输出格式规则" "$BODY_OUTPUT_FORMAT"
  sync_section "$file" "Windows / WSL 执行规则" "$BODY_WINDOWS_WSL"
  sync_section "$file" "CodeGraph 与代码检索" "$BODY_CODEGRAPH"
  sync_section "$file" "插件检测安装规则" "$BODY_PLUGIN"
  sync_section "$file" "图像生成强制规则" "$BODY_IMAGEGEN"

  if is_godot_project; then
    sync_section "$file" "Godot 项目工具配置" "$GODOT_TOOLING_SECTION"
    sync_section "$file" "图像生成配置" "$GODOT_IMAGEGEN_SECTION"
  fi

  echo "[OK] 已检查并补齐: $file"
}

# has_skip_marker
# 判断规则文件是否含独占一行的跳过标记（允许首尾空白与 CRLF 行尾）
# [参数] file: 子目录中的 AGENTS.md / CLAUDE.md 文件路径
# [返回] 含跳过标记时退出码为 0，否则非 0
# 最近修改时间: 2026-10-08 11:04:29 新增, 识别子目录精简规则文件的跳过标记
has_skip_marker() {
  local file="$1"
  grep -qE "^[[:space:]]*${SKIP_MANAGED_SECTIONS_MARKER}[[:space:]]*$" "$file"
}

resolve_python
# Windows 上 Python 的 stdout 默认编码常落到系统 ANSI 代码页（如中文系统的 GBK/cp936），
# 而脚本内嵌 Python 块用 encoding="utf-8" 读写文件、却用默认编码 print() 状态信息，
# 会导致中文 [INFO]/[ERROR] 提示在终端里乱码（实测复现）；强制 UTF-8 让文件与输出编码口径一致。
export PYTHONIOENCODING=utf-8

# 1) 按 --target 创建缺失的根目录规则文件
declare -a TARGET_FILES=()
case "$TARGET" in
  default) TARGET_FILES=("$REPO_DIR/AGENTS.md") ;;
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

# 3) 确保项目记忆四件套存在且职责边界可执行
ensure_project_current_file "$PROJECT_CURRENT_FILE"
ensure_project_history_file "$PROJECT_HISTORY_FILE"
sync_project_memory_file "$PROJECT_MEMORY_FILE"

# 4) 同步根目录所有已存在的规则文件（AGENTS.md / CLAUDE.md）
for name in AGENTS.md CLAUDE.md; do
  sync_agents_file "$REPO_DIR/$name"
done

# 5) 显式要求双平台规则时，AGENTS.md 是唯一正文源，避免默认平台与 Claude Code 读取不同规则。
if [[ "$TARGET" == "both" ]] && ! cmp -s "$REPO_DIR/AGENTS.md" "$REPO_DIR/CLAUDE.md"; then
  cp "$REPO_DIR/AGENTS.md" "$REPO_DIR/CLAUDE.md"
  echo "[INFO] 已以 AGENTS.md 同步根 CLAUDE.md"
fi

# 6) 同步子目录中所有已存在的 AGENTS.md / CLAUDE.md
while IFS= read -r extra_file; do
  # 1. 含跳过标记的刻意精简规则文件只提示原因，不写入
  if has_skip_marker "$extra_file"; then
    echo "[INFO] 已跳过: ${extra_file}（原因: 含跳过标记 ${SKIP_MANAGED_SECTIONS_MARKER}，声明为刻意精简的独立规则文件，不同步受管章节）"
    continue
  fi
  # 2. 其余子目录规则文件照常同步受管章节
  sync_agents_file "$extra_file"
done < <(find "$REPO_DIR" -mindepth 2 \( -name AGENTS.md -o -name CLAUDE.md \) -type f | sort)
