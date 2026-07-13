# 实施总览模板：零决策交接版

> 本模板用于 `implementation_overview`。它负责冻结整体技术决策、周期顺序和追踪关系；普通模型执行时必须进入具体周期的最小任务卡，不得从总览自行推导实现细节。

## 白话正文与附录

文档先在 H1 后用一段普通中文说清推荐方案、业务影响、范围、周期目标和完成结果，再保留当前文档原有标题、层级和顺序。文件树、任务表、命令和证据继续放在原有技术章节或已有附录；只有没有合适位置时才在末尾增加唯一的 `附录`。同时补齐 `reader_level`、`writing_style`、`appendix_policy: preserve_existing_or_one_terminal_appendix` 和 `review_acceptance_gates` 元数据。

## 文档信息

```yaml
schema_version: 1
doc_id: "IMP-OVERVIEW-YYYYMMDD-001"
doc_type: implementation_overview
source_ids: ["REQ-...", "AC-..."]
status: draft
version: v1.0
complexity: L1|L2|L3|L4
current_slice: "SLICE-..."
baseline_commit: "commit-or-N/A-with-reason"
template_version: "implementation-overview-v1"
updated_at: "YYYY-MM-DD HH:mm:ss"
reader_level: business_general
writing_style: plain_chinese
appendix_policy: preserve_existing_or_one_terminal_appendix
review_acceptance_gates: []
```

## 当前计划最终方案简要说明

用 1-3 句冻结推荐方案、主落点和选择原因；不得只写“按需求实现”。

## Agent 对当前问题的理解

- 问题 / 目标：
- 本轮范围：
- 非范围：
- 当前优先闭环：
- 关键假设 / 待确认点：
- `unresolved_decisions`：无，或逐项列 `DEC-*`、等级、阻断原因和升级路径。

## 图片资产决策与实施边界

- 图片资产决策：`需要` 或 `N/A + 原因 + 证据`。`需要` 时列出必需场景（UI/原型、截图证据、视觉对比、真实产物、空间布局、外观基线或 Mermaid 无法准确表达的内容）；`N/A` 时说明为何 Mermaid、表格或文字已经足够。
- Mermaid 边界：流程、时序、状态、依赖和数据关系必须继续使用 Mermaid，图片不得替代既有 Mermaid 门禁；图片只能补充无法准确表达的视觉内容。
- 生成契约：真实生成调用 `imagegen`，目标路径显式为项目根 `doc/data/images/<document_stem>.<asset-slug>-v<number>.<ext>`；失败即阻断，不得使用程序绘图、占位图或 Base64 冒充。
- 格式契约：PNG 用于 UI、截图、文字密集图和信息图；JPEG 用于照片；WebP 只有在目标渲染器兼容性已验证并记录证据后才能使用；扩展名必须与文件签名一致。
- 引用契约：Markdown 仅使用从当前文档位置计算的 `/` 分隔相对路径，例如 `![IMG-OVERVIEW-001 登录状态对比](../data/images/<document-stem>.login-state-v1.png)`；禁止绝对路径、反斜杠、`file://`、远程热链、HTML `<img>`、越界路径及 `doc/data/<file>` 旧路径。

## 图片资产清单

| 图片 ID | 用途 / 生成输入 | 来源 | 相对路径 | 版本 | 关联 REQ/RULE / AC / CYCLE / TASK | 引用章节 | 敏感状态 | 版权状态 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `IMG-*` |  | `imagegen` / 用户提供 / N/A | `../data/images/<document-stem>.<asset-slug>-v<number>.<ext>` | `v1` |  |  | `无敏感信息/需脱敏` | `已确认/待确认`

## 已冻结决策与方案比较

| ID | 决策问题 | 候选方案 | 选定方案 | 排除原因 | 影响面 | 回滚 | 证据 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `DEC-*` |  |  |  |  |  | `ROLLBACK-*` | `SRC-*` |

## 系统边界与现状基线

必须列出已核实的目录、模块、依赖版本、关键符号、接口和提交基线。涉及代码时附代码落点目录树：

```text
repo/
├── path/to/module/       # 已存在模块；列出职责和关键符号
└── path/to/new_file      # 新增文件；列出唯一用途
```

## 实施周期总览

| 顺序 | 周期 ID | 期次定位 | 单一周期目标 | 进入条件 | 收口条件 | 依赖 | 文档 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `CYCLE-01` | 第一期 |  |  |  |  | `./..._实施周期01_...md` |

周期必须按 `01 -> 02 -> ...` 顺序推进；前一周期没有实现、真实测试、审查、验收四项闭环，不得进入下一周期。

```mermaid
flowchart LR
  C01["CYCLE-01 第一期"] --> G01{"收口条件满足?"}
  G01 -->|是| C02["CYCLE-02 第二期"]
  G01 -->|否| STOP["⛔ 停止并回流阻断项"]
```

图形目的：说明周期门禁和不可跳期规则。关联 ID：`CYCLE-01`、`CYCLE-02`。

## 阶段计划

每个阶段只承载一个目标，必须写输入、动作、输出、验证门槛和归属周期。阶段不是可替代最小任务的执行单位。

| 阶段 | 周期 | 唯一目标 | 输入 | 输出 | 验证门槛 |
| --- | --- | --- | --- | --- | --- |
| `PHASE-01` | `CYCLE-01` |  |  |  |  |

## 最小任务清单与追踪矩阵

| 周期内顺序 | 任务 ID | 垂直切片目标 | 预计文件数 | 文件/符号契约 | 真实测试 | 完成条件 | 停止条件 |
| --- | --- | --- | ---: | --- | --- | --- | --- |
| 1 | `TASK-01` |  |  | `minimum-task-execution-contract.md` | `TEST-01` |  |  |

每个 `TASK-*` 只能归属一个 `CYCLE-*`，默认不超过 5 个文件；超出时必须拆分或记录不可拆分的证据。任务必须逐个完成“实现 -> 真实测试 -> 审查 -> 验收”。

| 来源/验收 | 周期 | 任务 | 文件/符号 | 测试 | 证据 | 状态 |
| --- | --- | --- | --- | --- | --- | --- |
| `REQ-*` / `AC-*` | `CYCLE-01` | `TASK-01` | `path:Symbol` | `TEST-01` | `EVIDENCE-*` |  |

## 真实测试安排

每个行为变更任务必须写独立测试入口、local 环境、样本/fixture、断言、失败预期、清理方式和证据位置。`build`、`lint`、静态检查、人工阅读不算真实测试。

| 测试 ID | 任务 | 命令/入口 | local 环境 | 样本 | 断言 | 失败预期 | 清理 | 证据 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `TEST-01` | `TASK-01` |  |  |  |  |  |  | `EVIDENCE-*` |

## 风险、阻断、回滚与最大推进边界

| ID | 风险/阻断 | 触发证据 | 当前措施 | 恢复路径 | 禁止动作 |
| --- | --- | --- | --- | --- | --- |
| `GAP-01` / `ROLLBACK-01` |  |  |  |  |  |

- 任务完成条件：
- 任务停止 / 结束条件：
- 当前 agent 最大推进边界：
- 是否已获得用户开始实施授权：`是/否`（计划本身不构成授权）。

## 自审结论

- 零决策交接：
- 文件/符号落点：
- 需求/验收/任务/测试覆盖率：
- 周期顺序与闭环：
- 图形语义与 Mermaid 解析：
- 占位词和 N/A 证据：
- 用户确认状态：
