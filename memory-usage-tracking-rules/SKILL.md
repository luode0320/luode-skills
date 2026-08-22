---
name: memory-usage-tracking-rules
description: 记忆使用计数与高频条目自动吸收总入口（收口 gate），全局通用机制。当本轮实际引用项目记忆三文件 `PROJECT_MEMORY.md` / `PROJECT_STYLE.md` / `PROJECT_HISTORY.md` 的条目用于决策、输出、代码生成或被其他 skill 引用时，任务收口前必须命中本 skill 做计数回写与吸收候选扫描；当任一记忆条目的使用次数达到阈值（`usage_count ≥ 3` 且 `usage_days ≥ 2` 且 `absorbed_to` 为空）时，按本 skill 流程自动吸收为 `project-项目slug-主题-rules` 项目 skill 固定下来。会话启动全文读取不计入使用次数；机制适用于所有使用项目记忆四件套的项目（新项目由 bootstrap_agents.sh 自举时创建计数锚点，存量项目由收口闸门检测缺失锚点提示回补），不限于任何单一仓库。
---

# 记忆使用计数与高频条目自动吸收规则

## 核心目标

1. 给项目记忆三文件（`PROJECT_MEMORY.md` / `PROJECT_STYLE.md` / `PROJECT_HISTORY.md`）的条目增加"使用次数"统计，锚点统一采用**机器索引区模式**（文件底部固定标题 + yaml fenced block），把"高频"从定性信号变成可量化数据。
2. 使用次数达到阈值的高频条目，自动吸收为项目本地 skill（`project-<slug>-<topic>-rules`），让 `skill-absorption-rules` / `project-local-skills-rules` 的"场景高频、稳定、长期独立"判据获得量化输入。

三层链路：**计数锚点层**（三文件 schema）→ **计数回写层**（会话台账 + 收口闸门）→ **吸收沉淀层**（自动识别 → 查重 → 落盘 → 校验 → 登记）。

## 适用场景与自动触发信号

- 本轮实际引用（非启动读取）了 `PROJECT_MEMORY.md` / `PROJECT_STYLE.md` / `PROJECT_HISTORY.md` 中的条目，用于决策、输出、代码生成、命名、配置取值或被其他 skill 引用。
- 本轮窄读了 `PROJECT_HISTORY.md` 的某条历史事件并影响了当前任务。
- 任务收口前需要判定是否存在达到吸收阈值（`usage_count ≥ 3` 且 `usage_days ≥ 2` 且未吸收）的记忆条目。
- 用户显式说"统计记忆使用次数 / 看看哪些记忆条目标常用 / 把高频记忆吸收成 skill"。

**不触发**：会话启动按规则读取记忆文件全文（`父目录规则 -> PROJECT_CURRENT.md -> PROJECT_MEMORY.md`）不算"实际引用"，不计数。

## 计数锚点 schema（简版）

计数锚点统一在**文件底部**（与 `PROJECT_MEMORY.md` 既有"机器索引区必须位于底部"规则一致），详细字段与约束见 `references/usage-anchor-schema.md`。

### PROJECT_MEMORY.md — 扩展现有机器索引区

- 顶层新增 `usage_tracking:` 键（`version` 保持 1 向后兼容）：

```yaml
usage_tracking:
  schema_version: 1
  counted_files: [PROJECT_MEMORY.md, PROJECT_STYLE.md, PROJECT_HISTORY.md]
  policy_ref: memory-usage-tracking-rules/references/usage-tracking-policy.md
```

- `entities[]` 每实体追加 4 个**可选**字段（缺省 0/null，老实体不报错、无需全量迁移）：
  - `usage_count: <int>`（累计实际引用次数）
  - `usage_days: <int>`（累计引用天数，当天首次引用时 +1）
  - `last_used_at: <YYYY-MM-DD>`
  - `absorbed_to: <project-xxx-rules>`（非空即冻结计数，不再进候选）

### PROJECT_STYLE.md / PROJECT_HISTORY.md — 新增计数锚点区

- 文件底部新增固定标题 `## 计数锚点区`（与 MEMORY 的"机器索引区"语义区分：本区只承载计数，不含实体/关系/证据全索引）。
- yaml 块，锚点 key 用条目标题（`### 标题`，稳定可回指）：

```yaml
version: 1
anchors:
  - title: 中文优先表达
    usage_count: 0
    usage_days: 0
    last_used_at: null
    absorbed_to: null
```

- HISTORY 锚点 key 用事件条目 `- YYYY-MM-DD：` 后的核心主题短语（约前 12 字符，可前缀匹配）。
- 条目标题被重写时同步更新锚点 title；缺失锚点由收口闸门提示回补。
- **HISTORY 裁剪一致性**：被裁剪事件的计数随事件一起删除（不保留 retired）——HISTORY 只保留最近 20 条窗口，被裁剪即失去候选价值；审计留痕写当日日志。HISTORY 计数仅作主题热度**弱信号**，吸收候选以 MEMORY/STYLE 为主。

## 计数回写规则

- **谁 +1**：仅"实际引用时"——条目被检索后用于决策、输出、代码生成、被其他 skill 引用时 +1；HISTORY 窄读计入；**会话启动全文读取不计**。
- **收集**：会话内维护内存台账 `usage_log: [{file, anchor, reason}]`，不即时写盘，按 `(file, anchor)` 去重（同会话同条目只 +1）。
- **回写时机**：任务收口时由本 skill（已注册为延迟 gate）统一执行，不即时写盘。非 Plan Mode 实质任务轮恒为 `闸门预告` 成员。
- **前置校验（防虚报）**：回写前跑 `scripts/usage_ledger_validate.py`，每条 claim 锚点必须真实存在于文件且可定位，输出 `{ok, valid_claims, invalid_claims}`；`ok=false` 阻断回写，先修正台账再回写。
- **机器/人类区同步**：计数只写机器区/计数锚点区，**人类区不展示计数**（控体积）；吸收后人类区条目状态标记"已沉淀"。
- **与更新时间不联动**：`更新时间` = 内容修订时间，`last_used_at` = 最近引用时间，语义分离。
- 回写动作由 AI 编辑记忆文件（脚本只读校验，AI 写盘），三文件结构不同、回写含状态标记，不脚本化写盘。

## 吸收触发与自动吸收流程

### 阈值

`usage_count ≥ 3` 且 `usage_days ≥ 2`（引用分布在 ≥ 2 个不同日期），且 `absorbed_to` 为空。3 次过滤偶然引用，跨 2 日期排除单日凑数，与 `project-local-skills-rules` 既有"5+ tool call"沉淀门槛同量级。

### 执行序列（收口时自动执行）

| 步骤 | 动作 | 执行者 |
|---|---|---|
| 1 | 跑 `scripts/scan_absorption_candidates.py` 出候选清单（只读） | 脚本自动 |
| 2 | 查重：`ls <项目根>/skills/ \| grep '^project-'`（luode-skills 仓库用 `ls . \| grep '^project-'`）+ 与通用 skill 对照；已覆盖则更新不新建 | AI 按 `project-local-skills-rules/references/dedup-and-update.md` |
| 3 | 用 `.system/skill-creator/scripts/init_skill.py` 生成 `project-<slug>-<topic>-rules/` 骨架，按 `project-skill-template.md` 填充 | 脚本自动 + AI 填充 |
| 4 | 回写原条目标记 `absorbed_to` + 人类区状态"已沉淀" | AI 按规则 |
| 5 | `quick_validate.py` 校验 + 同域冗余扫描（复用 `skill-absorption-rules` 第 5 步四项检查） | 脚本自动 |
| 6 | 登记 `workbuddy-absorption-map.md` / `references/source-notes.md` / `.workbuddy/memory/当日日志` | AI 按规则 |
| 7 | 收口总结列出改动文件清单（diff 锚点）；**不自动 git commit**（遵守 AGENTS.md 严禁自动提交） | 规则强制 |

### 与"人在回路 / 棘轮"的调和

- **自动执行 + git 可回滚**：当前项目若为 git 仓库（如 luode-skills），吸收写盘后可随时 `git diff` 审计、`git checkout` 回退；非 git 项目以改动文件清单 + 当日日志留痕代替。收口总结强制列改动文件清单作 diff 锚点。
- **棘轮保留为机器可验证**：以三条件 PASS/FAIL 替代人工确认——`quick_validate.py` PASS + 同域冗余扫描 PASS + `absorbed_to` 指针可达；任一 FAIL 自动回滚本次吸收。
- **事后审计点**：当日日志追加"自动吸收记录"（候选、diff 摘要、校验结论），用户事后可审可回滚。

### 防重复吸收 / 防膨胀

阈值够硬；吸收后 `absorbed_to` 非空即冻结计数、后续引用走 skill；查重硬约束（通用规则不得沉淀为 `project-*`）；每次吸收复用 `skill-absorption-rules` 的"吸收即整理"（同主题可合并则合并，只增不减视为不合格）。

## 权责边界与不负责事项

- 只负责"记忆条目计数 + 高频条目吸收为项目 skill"的闭环，不替代 `project-memory-rules`（记忆维护）、`project-style-rules`（风格维护）的主流程。
- 计数/吸收是 **skill 资产**；`knowledge-flow` 的知识库笔记沉淀、`PROJECT_MEMORY.md` 的 `bridge_candidate` 字段不参与计数与吸收。
- 不自动执行 git commit / push / PR（AGENTS.md 严禁自动提交，收口停在"已改动未提交"）。
- 不修改其他项目的文件（跨项目写入红线：其他项目一律只读）。
- 吸收落点 `project-*` 统一为**项目根目录 `skills/`**（如 `D:\某项目\skills\project-<slug>-<topic>-rules\`），luode-skills 仓库特例直接落仓库根（仓库根即 skill 资产库）；命中由项目级 `AGENTS.md` / `CLAUDE.md` 显式声明引用，不依赖任何工具专属路径。

## 需要暂停并确认的条件

- 候选条目证据不足，无法稳定归纳 skill 的触发条件与职责边界。
- 查重发现与既有 skill 高度重叠，无法判断该补哪个。
- 计数台账中存在无法回溯到真实引用行为的 claim（必须先修正再继续）。
- 吸收会牵动多个 skill 或与现有 skill 职责大面积重叠。

## 执行通过 / 驳回标准

- 通过：计数回写前 `usage_ledger_validate.py` 输出 `ok=true`；吸收候选经查重、落盘、`quick_validate.py` PASS、同域冗余扫描 PASS；`absorbed_to` 指针可达；登记 `source-notes.md` 与当日日志；收口总结列出改动文件清单且不自动提交。
- 驳回：未过前置校验就回写计数（虚报）；达阈值候选未执行吸收而静默跳过；吸收后未跑校验/同域扫描；吸收导致 skill 库膨胀（无整理去重证据）；跨项目写入或自动提交。

## references 读取规则

- 定义计数锚点 schema 与字段约束时读 `references/usage-anchor-schema.md`。
- 定义回写时机、台账格式、防虚报规则时读 `references/usage-tracking-policy.md`。
- 判定吸收阈值与执行序列时读 `references/absorption-trigger.md`。
- 登记吸收来源与落点时读 `references/source-notes.md`（吸收动作由 `project-local-skills-rules` / `skill-absorption-rules` 承接，本文件只登记计数侧来源）。
- 校验脚本契约以 `scripts/usage_ledger_validate.py` 与 `scripts/scan_absorption_candidates.py` 的 CLI docstring 为准。
