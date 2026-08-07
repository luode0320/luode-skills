---
schema_version: 1
doc_id: "STYLE-HIST-RETAIN-20-001"
doc_type: "style_regression"
source_ids: ["USER-APPROVED-PLAN/PROJECT_HISTORY-RETAIN-20"]
status: accepted
version: "v1.0"
current_slice: "TASK-HIST-01..07"
updated_at: "2026-08-05"
template_version: "style-regression-v1"
reader_level: business_general
writing_style: plain_chinese
appendix_policy: preserve_existing_or_one_terminal_appendix
---

# PROJECT_HISTORY.md 保留最近 20 条事件 6-review 风格回归

结论：本次风格回归为 `STYLE: PASS`，本轮九个改动文件的格式、UTF-8、注释、位置、可读性与复用均符合仓库口径。影响：确认本次改动没有引入无关差异、注释缺口或编码漂移，可以交给用户决定是否提交。范围：本轮实际改动的文件，逐项检查格式、UTF-8、注释、目录归位、日志、可读性、复用、残留与编码。非范围：业务正确性、需求覆盖、发布放行判断，以及未被本轮改动的文件。变化：`PROJECT_HISTORY.md` 由 148 条裁剪为 20 条并按日期倒序，头部说明更新；规则与记忆文件 HISTORY 口径统一为“追加并只保留最近 20 条”；bootstrap 模板与四件套模板同步新口径；`PROJECT_MEMORY.md` 人类区与机器索引区更新并追加变更记录。完成标准：十类检查项全部无 P0 与 P1 问题，且 TC-1 至 TC-5 的真实验证都在风格回归之前通过。术语说明：`STYLE: PASS` 指风格回归通过；`P0` 与 `P1` 指必须修复的阻断级与高优先级问题。验证状态：已通过，无待修问题。

## 文档信息

| 项目 | 内容 |
|---|---|
| 所属来源 | `USER-APPROVED-PLAN/PROJECT_HISTORY-RETAIN-20` |
| 覆盖任务 | `TASK-HIST-01` 至 `TASK-HIST-07` |
| 执行时点 | TC-1 至 TC-5 真实验证通过之后，逐项执行 |
| 关联真实测试 | `TEST-TC-1`、`TEST-TC-2`、`TEST-TC-3`、`TEST-TC-4`、`TEST-TC-5` |
| 实现证据 | `EVIDENCE-TASK-HIST-01` 至 `EVIDENCE-TASK-HIST-07` |
| 测试证据 | `EVIDENCE-TEST-TC-1` 至 `EVIDENCE-TEST-TC-5` |
| 风格证据 | `EVIDENCE-STYLE-HIST-01` |

## 图片资产决策

图片资产决策：N/A + 原因：本次风格回归只检查文本文件与脚本模板文本的格式、注释与位置，不包含界面、截图或视觉验收对象 + 证据：`doc/data/images/` 下无本任务图片引用。

## 检查范围

| 序号 | 文件 | 归属任务 | 改动性质 |
|---|---|---|---|
| 1 | `PROJECT_HISTORY.md` | `TASK-HIST-01` | 头部说明更新 + 148 条裁剪为 20 条并补日期、倒序 |
| 2 | `project-memory-rules/SKILL.md` | `TASK-HIST-02` | 写入规则新增“历史事件保留窗口”小节 |
| 3 | `project-rule-file-bootstrap-rules/SKILL.md` | `TASK-HIST-03` | memory-bootstrap 职责表 HISTORY 行同步 |
| 4 | `project-rule-file-bootstrap-rules/scripts/bootstrap_agents.sh` | `TASK-HIST-03` | 两处模板文本（heredoc 行 + PROJECT_HISTORY_TEMPLATE）同步 |
| 5 | `project-rule-file-bootstrap-rules/references/项目记忆模板/四件套模板.md` | `TASK-HIST-03` | 标题与头部说明同步 |
| 6 | `AGENTS.md` / `CLAUDE.md` | `TASK-HIST-04` | 四件套段落 HISTORY 行同步 |
| 7 | `PROJECT_MEMORY.md` | `TASK-HIST-05` | 人类区与机器索引区 HISTORY 描述更新、更新时间刷新、变更记录追加 |
| 8 | `PROJECT_CURRENT.md` | `TASK-HIST-01` | 运行时投影托管区写入（task-plan-rehydration-rules 工具产物） |
| 9 | `skill-dictionary/data.js` | `TASK-HIST-06` | 字典生成脚本刷新（时间戳 + repo_root 修正，无内容漂移） |

范围外说明：`doc/5-tests/2026-07-13_174233/init-tmp/AGENTS.md`、`CLAUDE.md` 与 `vercel-react-best-practices/AGENTS.md` 在 bootstrap 幂等验证中被脚本同步，随后已恢复为 HEAD 内容，未纳入本次改动范围。

## 真实测试前置证据

风格回归在真实测试通过之后执行，不代替真实测试。

| 任务 | 真实测试 | 结果 | 证据 |
|---|---|---|---|
| `TASK-HIST-01` | `TEST-TC-1`：裁剪结果断言（20 条、日期严格倒序、首条 08-05、UTF-8 回读 + `git diff --check`） | 通过 | `EVIDENCE-TEST-TC-1` |
| `TASK-HIST-06` | `TEST-TC-2`：临时副本模拟追加 1 条新事件后自动裁剪为 20 条且新事件置顶 | 通过 | `EVIDENCE-TEST-TC-2` |
| `TASK-HIST-06` | `TEST-TC-3`：七个文件 HISTORY 口径均含“最近 20 条”且语义一致 | 通过 | `EVIDENCE-TEST-TC-3` |
| `TASK-HIST-06` | `TEST-TC-4`：运行 `bootstrap_agents.sh` 幂等，不覆盖 `PROJECT_HISTORY.md` 与 AGENTS 新口径 | 通过 | `EVIDENCE-TEST-TC-4` |
| `TASK-HIST-06` | `TEST-TC-5`：skill 字典重跑无内容漂移；`doc/6-review` 归档通过 style_regression profile 校验 | 通过 | `EVIDENCE-TEST-TC-5` |

完整命令与输出见本轮执行证据（裁剪脚本副本断言、`git diff --check`、字典生成脚本退出码、bootstrap 幂等前后 hash 对比）。

## 检查清单

| 检查项 | 结论 | 依据 |
|---|---|---|
| 格式与排版 | 通过 | 事件条目统一 `- YYYY-MM-DD：` 前缀；Markdown 未混入 HTML；规则小节沿用文件既有列表结构 |
| 注释完整性 | 通过 | 本轮无新增或修改函数/方法（bootstrap 仅模板文本行替换），函数位点 0 个；无结构体字面量位点 |
| 中文表达 | 通过 | 新增与修改说明均为简体中文，`STYLE`、`P0`、`P1`、`repo_root` 等技术符号保留原文 |
| 代码位置与目录归位 | 通过 | 改动均落在既有规则/记忆文件内；`doc/6-review/` 归档按时间戳与来源标识命名；无新增测试资产 |
| 日志与输出 | 通过 | 未新增打印或调试输出；验证脚本仅在临时副本运行后已删除 |
| 可读性 | 通过 | 20 条事件按日期倒序、同日保持原顺序；头部说明与新小节一次说清保留窗口 |
| 复用与最小改动 | 通过 | 裁剪逻辑统一实现并先在临时副本验证；规则口径同步未扩大无关段落 |
| 本轮残留 | 通过 | `.codex-tmp/` 临时目录已删除；bootstrap 幂等验证产生的子目录文件已恢复为 HEAD |
| 编码与换行 | 通过 | 全部改动文件 UTF-8 严格回读成功；`git diff --check` 退出码 0；无 NUL 字节 |
| 无关差异 | 通过 | 差异统计与计划文件清单逐项对应；bootstrap 运行额外改动的三个子目录文件已还原 |

## 问题与修复

| 编号 | 级别 | 问题 | 处理 |
|---|---|---|---|
| `STYLE-HIST-001` | P2 | bootstrap 幂等验证运行后，脚本将根 `AGENTS.md` / `CLAUDE.md` 中模板外的两行（根 `test/` 唯一活动测试代码根、probe-timeout 投影规则）删除，并同步了三个子目录文件 | 已恢复根文件两行与三个子目录文件为 HEAD 内容，工作树只保留计划内改动；脚本模板漂移作为范围外发现记录 |

## 范围外发现

以下问题在本轮检查中被发现，但不属于本周期范围，未修改：

| 项目 | 现象 | 判定 |
|---|---|---|
| `project-rule-file-bootstrap-rules/scripts/bootstrap_agents.sh` | 受管章节模板与根 `AGENTS.md` 存在内容漂移：模板缺失“根 `test/` 唯一活动测试代码根”与“probe-timeout 投影规则”两行，运行同步会删除模板外内容 | 既有问题，不在本轮计划范围；已恢复本轮受影响文件，未改脚本模板 |

## 6-review 结论

`STYLE: PASS`

| 项目 | 结论 |
|---|---|
| 风格结论 | `STYLE: PASS`，无 P0、无 P1；一个 P2（bootstrap 运行副作用）已在本轮处理 |
| 边界声明 | 本结论只覆盖代码风格、格式、位置、注释、日志、可读性与复用，不判断业务正确性、需求覆盖或发布放行 |
| 完成标准 | 检查清单十项全部通过，且 TC-1 至 TC-5 真实验证都在风格回归之前通过 |
| 后续动作 | 无。改动停在已改动未提交状态，是否提交由用户决定 |
