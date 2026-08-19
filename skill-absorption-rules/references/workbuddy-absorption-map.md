# 吸收裁决表（workbuddy-absorption-map）

> 归属 owner：`skill-absorption-rules`。登记每次外部 skill 吸收的三态裁决结果，来源可回指。新吸收追加行，不覆盖旧记录。
>
> **防臃肿登记要求（2026-08-19 起）**：每次吸收除记录「合并/保留/拒绝」外，必须记录本次「整理去重」动作（合并了哪些重复段落、消除了哪些冗余引用、删除了哪些过时规则）与「净增体积变化」；无整理动作的写 `N/A + 理由`。只增不减的登记视为不合格。
>
> **同域扫描登记要求（2026-08-20 起）**：每次吸收必须在登记中新增「同域扫描结论」行——扫描范围（本次吸收触达的同域 skill 集合）、发现 X 处冗余（重复段落 / 门控层叠 / 散落产物）、清理 Y 处、PASS/FAIL；「整理去重」动作描述必须包含同域清理位置（哪个 skill、哪个段落、收敛到哪个权威）。缺同域扫描结论的吸收登记视为未完成。
>
> **内部更新通道登记（2026-08-20 起）**：本表同时登记「内部 skill 更新通道」的裁决式调整——来源列写"内部调整：<目标 skill>，<调整诉求>"，其余列（裁决 / 落点 / 整理去重 / 同域扫描结论 / 净增体积）要求与外部吸收完全一致，无外部源可删。

## 2026-08-19：java-story-develop__skillhub

- **来源**：LobeHub 安装包 `java-story-develop__skillhub`（工作区 `D:\谷歌云盘\luode-skills\java-story-develop__skillhub\`，用户级 `C:\Users\luode\.workbuddy\skills\java-story-develop__skillhub\`），版本以安装包 `_meta.json` 为准。
- **形态**：本地安装源吸收（先安装 → 分析吸收 → 删除源）。
- **拆解原子规则数**：14 条。

| # | 外部精华 | 本地现状 | 裁决 | 落点 / 理由 |
|---|---------|---------|------|------------|
| 1 | 环境探测：扫描 pom.xml/go.mod/package.json 探测运行时、Web 框架、ORM、业务框架、工具库、数据库、前端栈 | `project-memory-rules` 有四件套记忆但无环境探测清单机制 | 合并 | `project-memory-rules/references/environment-probe.md`（新建），含探测维度表 + 命令示例 + 记忆固化格式 |
| 2 | 记忆优先恢复环境，命中则跳过探测 | `project-memory-rules` 启动读 PROJECT_CURRENT/PROJECT_MEMORY | 保留本地 | 本地更强 |
| 3 | 环境记忆持久化格式（project-env-{projectName}） | `project-memory-rules` 机器索引区 | 合并 | 并入 environment-probe.md 的记忆固化格式 |
| 4 | 前端检测 + devMode 问询（FULLSTACK/BACKEND） | `package-structure-rules` 已能自动判断前后端同仓 | 拒绝 | 与本地「能自动判断就不问」习惯冲突 |
| 5 | SIMPLE/QUICK/FULL 三档分档路由 + 状态机 | `team-development-rules` 阶段路由、`requirement-splitting-rules` 复杂度拆分 | 合并 | `requirement-intake-rules/references/workload-mode-routing.md`（新建），与极致完整性标准调和 |
| 6 | context.json 状态机（currentPhase/phases/todos） | `task-plan-rehydration-rules` 投影 + AGENTS.md 追踪链 | 拒绝 | 机制形态不迁移，本地投影已覆盖 |
| 7 | 四轮小步迭代（骨架→填充→复盘→风险） | `artifact-delivery-gate-rules`（6-review）、`code-change-finalization-gate-rules` | 保留本地 | 本地更强 |
| 8 | 角色互搏（开发/产品双角色） | `adversarial-gap-interview.md` 已有对抗式缺口追问 | 合并 | `adversarial-gap-interview.md` 追加「设计阶段双角色自检」小节 |
| 9 | 异常恢复指引（6.1-6.5） | `agent-runtime-recovery-rules`、`session-handoff-rules`、`task-plan-rehydration-rules` | 保留本地 | 本地更强 |
| 10 | 11 条编码规范 | `code-generation-style-rules`、`code-readability-rules`、`error-handling-rules`、`logging-trace-rules`、`database-query-rules`、`naming-rules` 等十几条细分 | 保留本地 | 本地更细且 Go 生态适配 |
| 11 | 文档编号规则（1-Requirement/2-Analysis/3-Design） | `artifact-storage-rules`（doc/1-架构 2-需求 3-实施）+ 稳定 ID | 保留本地 | 本地更强 |
| 12 | TODO 分类规范（[临时]/[技债]/[外部依赖]/[逻辑补全]/[暂不明确]） | `task-blocker-closure-contract.md` 已有遗留项处理语义 | 拒绝 | 与本地闸门重叠，避免为吸收而吸收 |
| 13 | 核心变量命名（storyNameCN/ID/Branch） | `naming-rules`、`git-collaboration-rules` | 保留本地 | — |
| 14 | 子任务调度策略（并行分析/设计） | `parallel-task-dispatch-rules` | 保留本地 | 本地更强 |

- **落盘改动**：
  - 新增 `project-memory-rules/references/environment-probe.md`，并在 `project-memory-rules/SKILL.md` 适用场景追加引用。
  - 新增 `requirement-intake-rules/references/workload-mode-routing.md`，并在 `requirement-intake-rules/SKILL.md` References 追加引用。
  - 修改 `requirement-intake-rules/references/adversarial-gap-interview.md`，追加「设计阶段双角色自检」小节。
- **源清理**：吸收完成后删除本地安装 `java-story-develop__skillhub`（工作区 + 用户级两份）。
- **评分**：见对应 case study（`references/case-java-story-develop-absorption.md`，如需）。

## 2026-08-20：内部更新——需求 / 实施 / Bug 三域收敛去重

- **来源**：内部调整：三域 skill 体系（13 个 skill），调整诉求 = "整理一下需求、实施、bug 的 skill"（延续测试域收敛）。
- **形态**：内部更新通道（无外部源可删）。
- **拆解原子条目数**：13 个 skill 逐域盘点。

### 裁决与落点

| 域 | skill | 裁决 | 落点 / 理由 |
|---|---|---|---|
| 需求域 | intake / boundary / change / splitting | 保留现状 | 4 个 SKILL.md 均已"单一权威 + 引用"（shared-contract 76 行承载保护语义，各 SKILL.md 仅 1-2 句精简落地提示）；图片规则在 references 内为不同语境落地项（清单/检查/模板），非硬冗余 |
| 实施域 | delivery-gate | 调整合并 | step4 测试域细则（ASCII 镜像 / release-artifacts / apifox caseId）与 test-strategy 完全重复 → 收敛为引用 test-asset-governance + 《接口测试执行通道》 |
| 实施域 | implementation-planning | 保留现状 | 22 refs 主题区分度高（模板/门禁/契约/流程），按需加载是优点非膨胀；RULE-PMW / 跨会话契约红线不动 |
| 实施域 | storage / rehydration | 保留现状 | 职责独立，仅划界 |
| Bug 域 | intake 等 5 个 | 部分调整 | output-template 重命名规范化（→ bug-discovery-output-template.md）；11 个旧命名空间文件经全量复核为活跃路由资产（被 discovery-and-gap / runtime-diagnostics 引用），保留不删；五份 SKILL.md 已引用式（local 0 处展开复述），bug-lifecycle-common-contract 已为共享契约，C2-C5 保留现状 |

- **整理去重**：delivery-gate SKILL.md L62 测试域细则 → 引用 test-strategy（-约 80 字节展开）；Bug 模板重命名 + 注册表 TPL-PLAIN-BUG-002 path 同步 + discovery-and-gap.md L15 引用同步（消除旧命名空间文件名）。
- **同域扫描结论**：范围 = 需求域 4 + 实施域 4 + Bug 域 5（13 个 skill）；发现 = 探索初判 6 处冗余（需求图片规则 / 实施 refs 膨胀 / Bug 骨架同构等），实测后**3 处为误判**（已引用式 / 模块化设计 / 独立成文模板句），**1 处为误删**（Bug 旧命名文件实为活跃资产，已从 git 恢复 11 个 + 修复引用）；真实冗余 = delivery-gate 测试域细则 1 处 + 旧命名模板名 1 处；清理 2 处；**PASS**（引用链全量复核无死引用）。
- **净增体积**：-约 200 字节（收敛展开 + 重命名），无新增内容。
- **棘轮验证**：体积下降、UTF-8 全通过、全量回归无新增失败、引用链无断链——评分不降。

## 2026-08-20：内部更新——Skill 治理域盘点（保留现状）

- **来源**：内部调整：Skill 治理域（9 项），调整诉求 = "还有哪个域需要整理？→ 用户选 Skill 治理域"。
- **形态**：内部更新通道（只读盘点，无改动）。
- **裁决**：全部保留现状。
  - hit-check / audit / compliance-gate / reasoning-summary 四 gate：逐字重复检测 **0 处**；边界已通过"不替代/只负责/统一交给"声明划清（触发检查 / 过程中审计 / 收口闸门 / 总结渲染四阶段时序），合并会破坏触发机制，不整合即最好整理。
  - skill-dictionary：工具资产（generate_dictionary.py + data.js），被 authenticated-url-routing / code-style-consistency / doc 等广泛引用，非 skill 但移动破坏引用链 → 保留。
  - thread-title mcp/node_modules（23MB）：活跃 MCP server 依赖（SKILL.md 引用 bootstrap.mjs / rename_current_thread），删除破坏功能 → 保留；git 卫生（gitignore node_modules）另行处理。
  - evolution / split-preserve / absorption：职责清晰（gap 回补 / 体积拆分 / 外部引入），合并破坏各自触发 → 保留。
- **同域扫描结论**：范围 = 治理域 9 skill；发现 = 探索初判 4 处（门控层叠 3 遍 / dictionary 混入 / node_modules 垃圾 / 生命周期三 skill 归并），实测**全部为误判**（逻辑相似非逐字重复 / 工具资产 / 活跃依赖 / 职责独立）；真实冗余 0 处；清理 0 处；**PASS**。
- **净增体积**：0（只读盘点，零改动）。
- **棘轮验证**：未改动，无评分变化。

## 2026-08-20：内部更新——编码域盘点（保留现状）

- **来源**：内部调整：编码域（24 skill，~700KB），调整诉求 = "按优先级继续 → 编码域"。
- **形态**：内部更新通道（只读盘点，无改动）。
- **裁决**：全部保留现状。
  - 注释三件套（completion-gate / placement-granularity / chinese-comment）：逐字重复 0 处；三者为"补齐闸门 / 放置颗粒度 / 中文表达"三阶段视角，边界已通过"转交"声明划清；"5 行代码块步骤注释 / 结构体字段注释 / 补丁注释"虽在三件套内双写，但一处是"必须补"（闸门视角）、一处是"放哪"（放置视角），互补非冗余，合并会破坏 gate 强制触发语义。
  - 风格四件套（generation-style / minimal-change / readability / style-consistency）：逐字重复仅 1 处无害句（"不替代 style-consistency"）；四者为"写码前契约 / 范围控制 / 可读检查 / 一致性闸门"编码生命周期四阶段，generation-style 的"同时约束命名/结构/注释/日志/错误"是契约覆盖维度（写码前汇总声明），非越界执行，L58-65 边界节已划清。
  - api-* 四件套 / database-* 两件套：职责清晰（请求生命周期 / 结构-访问），保留。
  - 散落产物：无（各目录结构干净）；仓库根 inventory.yaml 是接口基线活跃资产（被 project-interface-baseline-rules 引用），保留。
- **同域扫描结论**：范围 = 编码域 24 skill；发现 = 探索初判 2 组（注释三件套可合一 / 风格四件套越界），实测**误判**（阶段/视角差异非逐字重复，边界已划清）；真实冗余 0 处；清理 0 处；**PASS**。
- **净增体积**：0（只读盘点，零改动）。
- **棘轮验证**：未改动，无评分变化。

## 2026-08-20：内部更新——Agent 运行域盘点（保留现状）

- **来源**：内部调整：Agent 运行域（11 skill，~568KB），调整诉求 = "按优先级继续 → Agent 运行域"。
- **形态**：内部更新通道（只读盘点，无改动）。
- **裁决**：全部保留现状。3 组候选触发重叠实测均为"触发源 / 时间窗 / 机制差异"，非硬冗余：
  1. session-handoff（用户主动换会话 / 归档）vs context-compression（系统被动压缩后的恢复）：触发源不同（用户发起 vs 系统事件）；compression 条件联动的是 recent-context-bootstrap 而非 handoff。
  2. autonomous（任务闭环推进，无 Goal 依赖）vs long-run-loop（Goal active / 显式 goal 意图驱动的长循环）：Goal 有无是关键差异。
  3. history-recall（用户主动问历史，深度回溯）vs recent-context-bootstrap（新会话启动引导，近 3 天）：双向"不要代替"声明已划清（recent 声明不代替 history 深度回忆，history 声明不代替 recent 近期引导）。
  - 逐字重复 0 处；8 个运行 skill 相互边界声明齐全（条件联动 / 不要代替 / 不替代执行授权）。
- **同域扫描结论**：范围 = 运行域 11 skill；发现 = 探索初判 3 组触发重叠，实测**误判**（触发源/时间窗/Goal 机制差异 + 边界声明已划清）；真实冗余 0 处；清理 0 处；**PASS**。
- **净增体积**：0（只读盘点，零改动）。
- **棘轮验证**：未改动，无评分变化。

## 2026-08-20：内部更新——项目记忆知识域盘点（保留现状，体系盘点收官）

- **来源**：内部调整：项目记忆知识域（8 skill，~444KB），调整诉求 = "顺手过一遍（体系盘点最后一个域）"。
- **形态**：内部更新通道（只读盘点，无改动）。
- **裁决**：全部保留现状。7 个 skill 产出物完全不同，职责天然清晰：
  - project-memory（四件套：状态/规则/历史）、project-style（PROJECT_STYLE.md 风格记忆）、project-local-skills（project-* 前缀项目级 skill 沉淀）、project-rule-file-bootstrap（新会话启动读取）、project-timeline（项目历程报告）、project-design-doc（项目设计.md 维护）、knowledge-flow（跨项目 Google Drive 知识库，明确与四件套分层）。
  - 逐字重复 0 处；边界声明齐全：style 不负责生成契约（归 code-generation-style）、local-skills 不代替 knowledge-flow、bootstrap 不替代 memory 事实抽取、timeline 不代替当前交付摘要、design-doc 不代替 recent-context-bootstrap/artifact-storage。
- **同域扫描结论**：范围 = 记忆知识域 8 skill；发现 = 探索初判"四件套 Owner 需划界"，实测**边界已划清**（产出物不同 + 双向声明）；真实冗余 0 处；清理 0 处；**PASS**。
- **净增体积**：0（只读盘点，零改动）。
- **棘轮验证**：未改动，无评分变化。

## 2026-08-20：内部更新——剩余 skill 全量扫描（4 组保留 + 4 个残留清理）

- **来源**：内部调整：8 域之外的剩余 skill 全量扫描，调整诉求 = "其他 skill 还需要整理吗？扫一遍"。
- **形态**：内部更新通道（扫描 + 少量清理）。
- **裁决**：
  - A 类自有规则 4 组候选重叠全部保留现状：浏览器三件套（本地自动化/高级观测/云端能力三层面，重复仅为 agent-browser 工具说明，独立可读需要，低价值不收敛）、安装组（MCP vs 插件，差异明确）、交付报告组（交付总结 vs 周期报告，差异明确）、Windows 组（编码 vs 环境，差异明确）。
  - 独立 A 类 8 个（git-collaboration / swag-openapi-maintainer / authenticated-url-routing / image-redbox-focus / godot-project-bootstrap / game-asset-* 等）职责清晰，保留。
  - B 类工具 skill 39 个（~4.75MB，含 skillhub + doc/pdf/spreadsheet 等）无卫生问题，无需整理。
- **清理（同域扫描发现）**：删除根目录 4 个 0 引用一次性脚本残留（_write_cycle.py / _write_cycle2.py / _write_docs.py / _bm_skillid_migration.json，均 git 跟踪、硬编码 8/8 文档路径，一次性产物）。index.html 保留（11 处引用）。
- **维持**：thread-title mcp/node_modules（活跃 MCP 依赖，gitignore 卫生另行处理）。
- **同域扫描结论**：范围 = 剩余全部 skill（17 A 类 + 39 B 类）；发现 = 4 组候选重叠 + 4 个残留；清理 4 个残留；真实冗余 0（A 类职责差异/低价值说明）；**PASS**。
- **净增体积**：-41KB（删除 4 个脚本）。
- **棘轮验证**：删除不影响任何引用（0 引用复核），评分不降。
