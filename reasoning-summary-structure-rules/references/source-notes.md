# 来源记录

> 本文件记录 `reasoning-summary-structure-rules` 的所有调整来源，包括外部吸收与内部更新。

## 2026-09-16：待裁定事项建议、选项与默认最安全兜底闭环（内部更新）

- **来源类型**：内部更新（用户纠正与推进规则深化）
- **来源场景**：用户指出工程执行任务总结结论中列出需裁定的事项时（如 pairProbeConcurrency 是否单例共享、表重建方式），仅列出要裁定的事而没有给出建议与选项选择，属于半成品输出；用户进一步明确要求：必须引入「如果不做裁定，默认推进的最安全兜底方案」，彻底消除用户未明确选择或回复“继续”时的系统停滞与盲目冒进风险。
- **吸收/更新精华**：强制执行四要素闭环：① 裁定点与影响；② 推荐建议与理由（加粗倾向）；③ 选项选择（清晰 A/B 方案）；④ 默认最安全兜底方案（明确声明未做裁定时的安全推进方案，原则：防限流、防击穿、防破坏误删、最小影响面、保持系统稳定）。
- **落点文件**：`SKILL.md`（frontmatter description、适用场景、待裁定事项处理铁律、T2/T1输出要求、发送前强制自检、驳回标准）、`references/summary-structure-template.md`（T2 结果区与中断点待裁定事项标准结构及结构要求）、`references/conditional-sections-rules.md`（待裁定事项处理规则）、`references/output-examples.md`（真实违规反例剖析与标准改写正例）。
- **裁决表**：`references/workbuddy-absorption-map.md`
- **同域冗余扫描**：PASS（与 implementation-planning-rules、bug-fix-proposal-rules 等技能无重叠冲突）。

## 2026-09-15：优化「输出总结」Skill 规则（三段式极简结构与决策收敛）

- **来源类型**：内部更新（用户反馈）
- **来源场景**：总结长而臃肿，存在大量背景铺垫、代码/SQL排查流水账、反复论证问题。
- **吸收/更新精华**：工程执行任务与决策研判任务严格分流；简单建议走极简断言（≤ 3 行），复杂建议走强制三段式（决策点 -> 跨成员影响 -> 明确建议与选项）；确立反铺垫、反探查流水账、反重复论证三反铁律。
- **落点文件**：`SKILL.md`、`references/summary-structure-template.md`、`references/conditional-sections-rules.md`、`references/output-examples.md`。
- **裁决表**：`references/workbuddy-absorption-map.md`
- **同域冗余扫描**：PASS。

## 2026-09-08：吸收 mermaid-diagram（lispking, v1.0.1）

- **来源类型**：外部吸收（本地安装源）
- **来源名称**：`mermaid-diagram`（lispking）
- **本地路径**：`C:\Users\luode\.workbuddy\skills\mermaid-diagram\`
- **吸收精华**：Mermaid 各图表类型语法详解（Flowchart、Sequence、ER、Class、State、Gantt、Mindmap、Pie、Timeline、GitGraph）及常见陷阱、check-mermaid.mjs 真解析脚本
- **落点文件**：`references/mermaid-syntax-reference.md`、`scripts/check-mermaid.mjs`
- **裁决表**：`references/workbuddy-absorption-map.md`
- **拒绝条目**：Diagram Type Selection（本地语义匹配更强）、Styling（本地可读性规则更强）、HTML Report 生成（与 markdown 流程不兼容）、Workflow（分布式 skill 已覆盖）
- **源处理**：待用户确认后删除本地安装源
- **同域冗余扫描**：PASS（检查了 requirement-intake-rules、bug-intake-rules、implementation-planning-rules、artifact-delivery-gate-rules、artifact-storage-rules、delivery-summary-rules 等兄弟 skill，无交叉冗余）
- **环境依赖**：check-mermaid.mjs 依赖 jsdom（`npm install jsdom` 到 skill 根目录），已在脚本注释中说明

## 2026-09-05：吸收 Markdown Skillhub 市场 Skill

- **来源类型**：外部吸收（本地安装源）
- **来源名称**：`markdown` Skillhub 市场 Skill
- **本地路径**：`C:\Users\luode\.workbuddy\skills\markdown__skillhub\`
- **吸收精华**：通用 Markdown 语法陷阱（空白行、链接、代码栅栏、表格、转义、可移植性）
- **落点文件**：`references/markdown-writing-rules.md`
- **裁决表**：`references/workbuddy-absorption-map.md`
- **拒绝条目**：`<br>` 行尾空格规则（与本地 HTML 红线冲突）、图片 alt text 规则（本地已有更强）、HTML 渲染规则（本地已有更强）
- **源处理**：已删除本地安装源
- **同域冗余扫描**：PASS（无重复段落、无门控层叠、无散落产物、引用链完整）