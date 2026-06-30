---
name: skill-hit-check-rules
description: 【强制总控】每轮用户新消息（含新会话第一条）都必须先做命中检查并在首条中间进度输出。凡涉及 Git 协作动作（含显式关键词与隐式语义，如“提交git/帮我提交/commit一下/推送代码/看下状态”），必须联动命中 git-collaboration-rules。凡处理本仓库任务，最低还必须联动命中 `parallel-task-dispatch-rules`。首条中间进度最小必填包含 `命中检查`、`命中技能`，若本轮命中 `parallel-task-dispatch-rules` 还必须追加 `并行技能`。
---

# Skill 命中检查规则（最小闭环版）

## -1.4 极简硬闸门（强制）
- 每轮首条中间进度只要求两行：
  - `命中检查:<通过/阻断>; Git规则:<通过/不适用/阻断>`
  - `命中技能:<skill1,skill2,...>`
- 若本轮存在 Git 意图，`Git规则` 不得为 `不适用`。
- 未输出上述两行即判定 `阻断`，禁止执行领域命令。

## -1.5 违规处理（强制）
- 若发生“先执行命令、后做命中检查”，立即停止后续命令并重启流程。
- 重启后仅需补齐两行命中输出，不再强制输出额外恢复提示文案。

## -1. 触发确认（强制）
- 每轮用户新消息都必须命中本 skill，且必须先执行命中检查，再执行任何领域动作。
- 若处理本仓库任务，必须同时命中 `parallel-task-dispatch-rules`。
- 若本轮任务存在多 skill 组合、并行拆分或规则收口风险，推荐同时命中 `skill-audit-rules`。
- 若本轮新增或修改任意 skill 资产（`SKILL.md`、`references`、`scripts`、`agents` 等），必须同时命中 `skill-compliance-gate-rules` 做收口闸门；详见「## 2.3 Skill 资产改动联动闸门」。
- 若用户消息包含任一 Git 意图（关键词或语义），必须同时命中 `git-collaboration-rules`。
- 若应命中未命中，判定 `阻断`，禁止继续执行对应领域命令。

## -1.0 新会话首轮保障（强制）
- 新会话第一条用户消息与普通轮次同等处理，不得因“缺少历史上下文”跳过本 skill。
- 无论是否已加载其他 skill，首条中间进度必须先输出“Skill 命中检查”，之后才能执行任何命令。
- 若首轮直接执行了领域命令（如 `git status`、`npm`、`go test`）而未先输出命中检查，判定为流程违规。

## -1.1 Git 意图识别（强制）
以下任一命中即视为 Git 意图，不要求用户必须出现单词 `git`：
- 显式关键词：`git`、`commit`、`push`、`pull`、`rebase`、`merge`、`cherry-pick`、`stash`、`status`、`diff`、`log`
- 中文动作词：`提交`、`推送`、`拉取`、`合并`、`变基`、`暂存`、`提交代码`、`提代码`
- 高频口语表达：`提交git`、`帮我提交`、`commit一下`、`给我推上去`、`看下git状态`、`看下改动`
- 语义等价表达：请求“把当前改动入库/提交到分支/同步到远端/查看当前提交记录”

未命中上述字面词但语义上等价时，仍必须判定为 Git 意图并联动命中 `git-collaboration-rules`。

## -1.1.1 Git 仅限当前轮次（新增，强制）
- Git 意图判定只基于“当前这轮用户消息”，不得引用、继承或延续历史轮次里出现过的 `提交git`、`commit一下`、`推送代码` 等表达。
- 若当前这轮用户消息未出现 Git 意图，即使之前某一轮已经说过“提交git”，本轮的 `Git规则` 也必须判定为 `不适用` 或 `阻断`，不得继续执行 Git 协作命令。
- 不得因为“上一轮已进入 Git 流程”“刚刚提交过一次”就默认本轮继续沿用 Git 协作授权。

## -1.2 Git 判定优先级（强制）
- 若同一消息同时命中多个领域，Git 判定优先级高于普通开发任务，必须先联动命中 `git-collaboration-rules`。
- 只要用户意图中包含“提交/推送/查看改动或状态/同步分支”等 Git 协作动作，不得以“需求过短”或“口语化表达”降级为普通对话。

## -1.3 新会话首轮联动（强制）
- 若为新会话第一轮，必须同时命中 `project-agents-bootstrap`（不依赖用户意图）。
- 命中后需先执行仓库根目录规则文件检测（Codex 检查 `AGENTS.md`，Claude Code 检查 `CLAUDE.md`）：若缺失则先补齐，再继续主任务。
- 未联动 `project-agents-bootstrap` 或跳过规则文件检测，判定 `阻断`。
- 若首轮检测到根目录规则文件不存在，必须先创建完成；创建完成前一律禁止进入主任务（包括分析、读码、执行命令、修改代码）。
- 若出现”先做主任务、后补规则文件”的顺序，按严重流程违规处理：立即停止当前任务，回滚到首轮闸门重走。

## 0. 首条消息格式（强制）
每轮第一条中间进度必须以以下模板开头：
- `templates/hit-check-template.md`
- 模板必须按普通 Markdown 渲染：`**Skill 命中检查**` 标题独立一行，字段行整行使用单反引号包裹；不得放入代码围栏（三反引号 / 三波浪线）、缩进代码块或 HTML。
- 最小必填两行（可在模板基础上扩展，但不得缺失）：
  - `命中检查:<通过/阻断>; Git规则:<通过/不适用/阻断>`
  - `命中技能:<skill1,skill2,...>`

## 1. 最小流程
1. 判定命中 skill（基于用户本轮请求）
2. 首条输出两行命中信息
3. 若为新会话第一轮，先执行 `project-agents-bootstrap` 的规则文件检测（Codex → `AGENTS.md`，Claude Code → `CLAUDE.md`）
4. 若缺失则立即创建规则文件，创建完成前禁止进入主任务
5. 仅当规则文件已存在（原有或新建）后，才允许进入主任务执行

## 1.1 首条闸门（强制阻断）
若本轮命中任一 skill，但首条中间进度未按模板输出“Skill 命中检查”，则不得执行对应领域命令。
特别地：命中 `git-collaboration-rules` 时，未输出两行命中信息前，禁止执行任何 `git` 命令（`status` 与 `diff --cached --stat` 盘点命令除外）。

## 2. Git 联动闸门（强制）
若命中 `git-collaboration-rules`，则：
1. 本 skill 只校验 Git 场景是否正确联动 `git-collaboration-rules`，不定义具体提交步骤、证据清单或仓库脚本。
2. Git 提交、推送、状态盘点、证据输出和等价回退检查，以 `git-collaboration-rules` 的当前规则为准。
3. 不得在本 skill 中硬编码项目本地脚本路径；仓库是否存在提交前后 gate 脚本，由 Git 协作 skill 或项目级规则自行判定。

## 2.3 Skill 资产改动联动闸门（强制）
若本轮新增或修改任意 skill 资产（`SKILL.md`、`references/`、`scripts/`、`agents/` 等）：
1. 必须命中 `skill-compliance-gate-rules`，并在收口前给出 PASS / FAIL 结论；未给出不得宣称完成。
2. 若改动了 skill 的 `description` 或触发条件，必须追加命中 `skill-evolution-rules`。
3. 若涉及多个 skill、职责边界或规则收口风险，必须追加命中 `skill-audit-rules`。
4. 若改动了任一 skill 的 `description` 或新增 / 修改了 `##` 级标题，收口前必须重新运行 skill 字典生成脚本（`python skill-dictionary/generate_dictionary.py`），刷新 `data.js` 与 `字典.md`，禁止手改生成产物。
5. 以上联动未走完，不得进入最终收口。

## 3. 通过标准
- 首条中间进度与最终回复都含“Skill 命中检查”
- 仓库任务下已正确联动 `parallel-task-dispatch-rules`
- Git 场景下已正确联动 `git-collaboration-rules`
- 无“只命中未执行”
- 最终回复必须包含固定校验行：
  - `命中检查:通过`
  - Git 场景追加：`Git规则:通过`

## 4. 执行文件
- `templates/hit-check-template.md`
