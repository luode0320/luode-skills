# 来源记录

> 本文件记录 `reasoning-summary-structure-rules` 的所有调整来源，包括外部吸收与内部更新。

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