# 来源记录（source-notes）

> 归属 owner：`code-quality-rules`。登记本 skill 历次调整的来源与落点，与 `workbuddy-absorption-map.md` 配套。

## 2026-08-23：内部更新——删除纪律

- **调整类型**：内部更新通道。
- **调整诉求**：删除代码/功能必须彻底（remove 语义），禁止 xxxv2 备份版本，禁止记忆残留"禁止使用"描述。
- **触发场景**：用户在主会话提出 agent 把"删除"执行成"废弃"，留下 xxxv2 备份和记忆警示。
- **落点**：
  - 主定义：`code-quality-rules/references/code-removal-discipline.md`（新建）
  - 入口引用：`code-quality-rules/SKILL.md` 最小改动主线核心约束 + references 读取规则
  - 联动补充：`project-memory-rules/SKILL.md` 写入规则
- **裁决依据**：见 `../code-quality-rules/workbuddy-absorption-map.md` 2026-08-23 段落。
- **未落盘内容**：无。
- **外部源**：无（内部更新通道）。

## 2026-08-23：外部吸收——cd-debug（调试排错特工）

- **调整类型**：外部吸收通道。
- **外部源**：skillhub 市场 `cd-debug__skillhub`（调试排错特工 v1.0.0，作者 smart）。
- **调整诉求**：吸收「定位报错根因，给最小改动的修复方案」中的最小改动部分规则。
- **裁决结论**：7 条原子精华中 5 条保留本地（本地已更强）、2 条拒绝（触发体系冲突 + 商业形态）、0 条合并 → 无落盘改动；最小改动规则权威仍在 `minimal-change-general.md` / `minimal-change-boundaries.md` / `minimal-change-examples.md`，入口协调见 `bug-fix-proposal-rules`「与最小改动的协调」。
- **落点**：无（裁决登记于 `workbuddy-absorption-map.md` 2026-08-23 段落）。
- **未落盘内容**：全部未落盘——外部源无超出本地的规则细节。
- **外部源删除**：已删除用户级 + 工作区两份安装源（md5 一致）。

## 2026-09-11：内部更新——函数签名规则

- **调整类型**：内部更新通道。
- **调整诉求**：补齐“函数参数设计”缺口——参数顺序、数量控制、单参数与结构体参数取舍；口径采用用户裁决的“语义优先”（需可选/扩展字段必收结构体，同源参数 ≥3 也建议收）。
- **触发场景**：用户提出 AI 辅助开发的核心瓶颈已从逻辑正确性转向代码质量，其九维清单中“函数参数的定义顺序、数量，以及单参数与结构体参数的取舍”此前只有局部约定（`SKILL.md` 的 Go 函数签名风格约定 + `function-structure-rules.md` 一句“参数过多优先提炼结构体”），无通用规则。
- **落点**：
  - 主定义：`code-quality-rules/references/function-signature-rules.md`（新建，2469B）
  - 入口引用：`code-quality-rules/SKILL.md` 可读性主线 + references 读取规则
- **裁决依据**：见 `../code-quality-rules/workbuddy-absorption-map.md` 2026-09-11 段落。
- **未落盘内容**：无。
- **外部源**：无（内部更新通道）。

## 2026-09-11：内部更新——定义位置规则

- **调整类型**：内部更新通道。
- **调整诉求**：补齐“代码、变量的定义位置”缺口——局部变量、包级变量与常量、函数的定义位置；口径采用用户裁决的“函数开头集中”。
- **触发场景**：用户九维清单中“代码、变量的定义位置与命名方式”此前只有“声明形式”规则（`code-style-consistency-rules` 的 Go 局部变量声明风格约定：逐行 `var`、禁止 `var (...)` 分组），没有“定义在哪里”的口径。
- **落点**：
  - 主定义：`code-quality-rules/references/definition-placement-rules.md`（新建，2366B）
  - 入口引用：`code-quality-rules/SKILL.md` 可读性主线 + references 读取规则
- **裁决依据**：见 `../code-quality-rules/workbuddy-absorption-map.md` 2026-09-11 定义位置段落。
- **未落盘内容**：无。
- **外部源**：无（内部更新通道）。