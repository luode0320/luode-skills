# Owner 路由矩阵

本文件只定义监督生命周期的消费边界。静态 Owner 名称、触发条件、顺序、来源映射和路径安全规则由 [共享静态 Owner 路由契约](../../code-style-consistency-rules/references/static-owner-routing-contract.md) 唯一拥有；实际检查前仍必须读取当前工作树中的 Owner `SKILL.md`。Owner 缺失或来源不可读时只能产生 `unclassified/limited` finding。

## 共享静态路由消费

- 监督流程从 `code-style-consistency-rules/scripts/static_owner_router.py` 读取完整 Owner 集合；不得在本目录复制 Owner 常量、条件路由或来源映射。
- 来源映射固定为 `code-style-consistency-rules/references/static-owner-source-map.json`。
- 本 Skill 保留 Goal 双条件、扫描、finding 指纹、脱敏、`limited` 降级与通知；不拥有静态路由正文。
- `6-review` 只从同一共享路由中消费风格子集；监督可消费完整静态 Owner 集合，二者不能互相替代。

## 静态来源安全边界

- 共享来源映射只保存相对路径、glob 与消费方式，不复制规则正文。
- `source_paths`、`source_globs` 只能指向对应 Owner 目录内的 `.md` 规则来源；绝对路径、`..`、跨 Owner 路径、空 glob、声明文件缺失、非 UTF-8 或 frontmatter 名称不一致，都必须生成 `unclassified/limited` finding。
- 下一次扫描必须重新读取 source map 与磁盘文件，不允许使用监督 Skill 内嵌副本或旧摘要。
- `agents/openai.yaml`、`AGENTS.md`、`CLAUDE.md`、生成字典和历史文档不是静态质量正文来源，除非未来明确写入 source map 并通过安全测试。

## 冲突与优先级

1. 先执行基础编码 Owner。
2. 目录和公共复用 Owner 先于接口、数据和语言专项。
3. API 固定为 endpoint -> request -> response -> swagger。
4. 数据库固定为 schema -> query。
5. 横切 Owner 在主位点 Owner 之后叠加，不替代主位点 Owner。
6. 多个语言/框架条件可以并行命中；同一 Owner 只保留一次。
7. 无法确定唯一 Owner 时标记 `unclassified/limited`，不得自创规则。

## Owner 内部转交截断

- 本矩阵只消费允许 Owner 中可直接用于当前 diff 的静态代码质量条款。Owner 正文若要求转交、联动或让位给本矩阵排除的 Skill，监督流程必须在转交前停止，只记录该静态检查的适用结果，不继续调用被排除 Skill。
- `test-program-rules` 只消费测试程序、fixture、mock、stub 的结构、隔离、命名和可维护性条款；其对 `test-strategy-rules`、`artifact-storage-rules` 或测试执行入口的转交在监督上下文中不执行。
- `frontend-component-rules` 与 `frontend-ui-visual-rules` 只消费当前前端 diff 可判断的组件结构、视觉、交互和可访问性静态条款；其对 `frontend-design` 的让位或设计生成流程在监督上下文中不执行。
- `code-generation-style-rules` 只消费项目风格、局部样例和改动后风格闸门；不执行写码前授权或长期风格回写。

## 永不调用的排除列表

共享静态路由契约定义监督可读取的完整 Owner 集合；本文件下列名单只记录监督永不调用的阶段、运行时和动态执行类 Skill，不复制该集合，也不扩大共享白名单。

### 阶段审查、测试执行与 UI 主导

`git-collaboration-rules`、`code-change-finalization-gate-rules`、`test-strategy-rules`、`functional-validation-rules`、`test-regression-rules`、`browser-advanced-testing-rules`、`browser-session-automation-rules`、`web-design-guidelines`、`frontend-design`。

### 需求、Bug、实施与验收

`requirement-boundary-rules`、`requirement-change-rules`、`requirement-intake-rules`、`requirement-splitting-rules`、`bug-fix-proposal-rules`、`bug-intake-rules`、`bug-reproduction-rules`、`bug-root-cause-rules`、`bug-validation-rules`、`implementation-planning-rules`、`implementation-planning-rules`、`delivery-summary-rules`。

### 交付、产物与 Git

`artifact-delivery-gate-rules`、`artifact-storage-rules`、`delivery-summary-rules`、`swag-openapi-maintainer-rules`、`git-collaboration-rules`。

### 运行时、分析与元流程

`code-context-resync-rules`、`codegraph-analysis-rules`、`project-local-skills-rules`、`project-style-rules`、`skill-hit-check-rules`、`skill-audit-rules`、`skill-execution-compliance-gate-rules`、`skill-evolution-rules`、`skill-creator`、`skill-installer`、`find-skills`、`autonomous-execution-rules`、`parallel-task-dispatch-rules`、`team-development-rules`、`execution-failure-learning-rules`、`mcp-installation-rules`、`plugin-installation-rules`。

### 项目分析、文档与专项工程流程

`project-interface-baseline-rules`、`architecture-doc-rules`、`project-design-doc-rules`、`project-timeline-rules`、`project-local-skills-rules`、`project-rule-file-bootstrap-rules`、`godot-project-bootstrap-rules`。`micro-business-architecture-rules` 仅按允许列表中的受控条件作为质量 Owner，不因此放开其它项目流程。

### 状态、记忆、宿主与环境准备

`task-plan-rehydration-rules`、`knowledge-flow`、`project-memory-rules`、`thread-title-rules`、`context-compression-rules`、`agent-runtime-recovery-rules`、`project-rule-file-bootstrap-rules`、`recent-context-bootstrap-rules`、`history-recall-rules`、`authenticated-url-routing-rules`、`windows-powershell-environment-rules`、`wsl-windows-bridge`。

排除列表中的 Skill 仍可由主流程按其自身触发条件调用；本监督 Skill 永不把它们当作质量 Owner。
