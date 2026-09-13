# 吸收裁决表

> 本文件记录 `reasoning-summary-structure-rules` 的 Skill 吸收历史。来源包括外部市场 Skill、内部调整、执行中 gap 回补。

| 日期 | 外部来源 | 外部精华（原子条目） | 本地现状 | 裁决 | 落点 | 整理去重（含同域清理） |
|---|---|---|---|---|---|---|
| 2026-09-05 | `markdown` Skillhub 市场 Skill | 空白行陷阱（列表前空行/嵌套列表4空格/纯空格行） | 无对应规则 | 合并 | `references/markdown-writing-rules.md` | 无（新文件，零存量冗余） |
| 2026-09-05 | 同上 | URL 括号/空格转义、引用式链接验证 | 无对应规则 | 合并 | 同上 | 同上 |
| 2026-09-05 | 同上 | 代码栅栏技巧（三重反引号内嵌、行内反引号含反引号）、语言提示 | 已有 Mermaid 语言标记规则，未覆盖通用场景 | 合并 | 同上 | 同上 |
| 2026-09-05 | 同上 | 表格细节（对齐冒号、管道符转义、空单元格、前空行） | 无对应规则 | 合并 | 同上 | 同上 |
| 2026-09-05 | 同上 | 转义字符清单（`\*` `\_` `\[` 等）、代码块内不转义、`&` 条件转义 | 无对应规则 | 合并 | 同上 | 同上 |
| 2026-09-05 | 同上 | 可移植性（扩展语法非通用、YAML frontmatter 边界） | 无对应规则 | 合并 | 同上 | 同上 |
| 2026-09-05 | 同上 | 行尾两空格 `<br>` 不可靠 | 本地红线禁止 HTML 标签 | 拒绝 | 不吸收 | 冲突：`<br>` 属于应避免的 HTML 标签 |
| 2026-09-05 | 同上 | 图片必须提供 alt text | 已有 `artifact-storage-rules` 非空 alt + IMG-* 资产 ID 规则 | 保留本地 | 不吸收 | 本地更强：含 IMG-* 资产 ID 要求 |
| 2026-09-05 | 同上 | HTML 标签在 GitHub 可用但许多渲染器不渲染 | 已有 AGENTS.md "统一使用 markdown，不依赖 HTML 渲染" 规则 | 保留本地 | 不吸收 | 本地规则更强，且覆盖全部输出场景 |
| 2026-09-08 | `mermaid-diagram`（lispking, v1.0.1） | Flowchart 语法详解（方向、形状、边、subgraph） | 本地无全面 Mermaid 语法参考 | 合并 | `references/mermaid-syntax-reference.md` | 无（新文件，零存量冗余） |
| 2026-09-08 | 同上 | Sequence 语法详解（participant、alt/opt/loop、autonumber、activate） | 同上 | 合并 | 同上 | 同上 |
| 2026-09-08 | 同上 | ER 语法详解（cardinality、PK/FK/UK、属性定义） | 同上 | 合并 | 同上 | 同上 |
| 2026-09-08 | 同上 | Class 语法详解（抽象类、继承、可见性） | 同上 | 合并 | 同上 | 同上 |
| 2026-09-08 | 同上 | State 语法详解（状态迁移、choice、composite） | 同上 | 合并 | 同上 | 同上 |
| 2026-09-08 | 同上 | Gantt 语法详解（dateFormat、section、状态、依赖） | 同上 | 合并 | 同上 | 同上 |
| 2026-09-08 | 同上 | Mindmap / Pie / Timeline / GitGraph 语法 | 同上 | 合并 | 同上 | 同上 |
| 2026-09-08 | 同上 | Common Pitfalls（特殊字符、`end` 关键字、未闭合块、mindmap 限制） | 本地降级自检 6 项未覆盖全部 | 合并 | 同上 | 同上 |
| 2026-09-08 | 同上 | Verification Script（check-mermaid.mjs, jsdom 真解析） | 本 skill 无真解析脚本 | 合并 | `scripts/check-mermaid.mjs`（从源目录复制） | 无（新文件，零存量冗余） |
| 2026-09-08 | 同上 | Diagram Type Selection（11 种对照表） | 本地各 skill 有语义匹配表 | 保留本地 | 不吸收 | 本地按问题语义匹配更强 |
| 2026-09-08 | 同上 | Styling & Readability（classDef、theme） | 本地有详细渲染可读性规则 | 保留本地 | 不吸收 | 本地更强（更具体、适应降级通道） |
| 2026-09-08 | 同上 | HTML Report 生成（mermaid.min.js 离线渲染） | 文档编写类 skill 使用 markdown 内嵌 Mermaid | 拒绝 | 不吸收 | 与 markdown 文档流程不兼容 |
| 2026-09-08 | 同上 | Workflow（提取→选型→写→验证→交付） | 各 skill 已有各自执行流程 | 保留本地 | 不吸收 | 分布式 skill 已覆盖，无需独立 workflow |