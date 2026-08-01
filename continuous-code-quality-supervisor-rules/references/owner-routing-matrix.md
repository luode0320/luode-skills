# Owner 路由矩阵

本文件只保存 Owner 名称、触发条件、调用顺序和边界，不复制任何 Owner Skill 正文。实际检查前必须读取当前工作树中的 Owner `SKILL.md`；Owner 缺失或来源不可读时只能产生 `unclassified/limited` finding。

## 允许引用列表

### 基础编码 Owner

| 顺序 | Owner Skill | 触发条件 |
|---|---|---|
| 1 | `code-generation-style-rules` | 任意代码、脚本、测试支撑代码或配置型代码改动；只读取项目风格和局部样例并做改动后闸门 |
| 2 | `code-minimal-change-rules` | 任意新增或修改代码 |
| 3 | `code-readability-rules` | 任意业务、工具、服务、脚本代码改动 |
| 4 | `code-style-consistency-rules` | 任意代码、脚本、配置或测试代码改动 |
| 5 | `naming-rules` | 任意新增或修改代码；检查本轮新增/修改标识符及其上下文命名，不要求先证明发生显式重命名 |
| 6 | `comment-placement-granularity-rules` | 代码或注释变化，检查必要性、位置和颗粒度 |
| 7 | `comment-completion-gate-rules` | 代码或注释变化，检查改动位点和步骤说明 |
| 8 | `chinese-comment-rules` | 任意代码或注释变化；只检查改动位点现有或应补注释的中文表达，不要求先存在中文注释 |

### 结构、接口、数据与横切 Owner

| Owner Skill | 触发条件 | 调用顺序 |
|---|---|---|
| `package-structure-rules` | 目录、包、模块或启动入口变化 | 基础 Owner 后、业务专项前 |
| `common-util-rules` | 工具类、公共方法、公共组件、复用代码、同语义重复封装或 7 天冻结变化 | 结构 Owner 后；目录落点由 `package-structure-rules` 主判 |
| `api-endpoint-rules` | controller、router、handler、HTTP 方法或路由变化 | API 第 1 |
| `api-request-rules` | 请求参数、DTO、query/path/body 或校验变化 | API 第 2 |
| `api-response-rules` | 返回体、响应包装、分页、错误码或兼容字段变化 | API 第 3 |
| `api-swagger-rules` | HTTP API、Swagger 或 OpenAPI 代码变化 | API 第 4 |
| `database-schema-rules` | 数据库、表、字段、索引、约束或迁移变化 | 数据库第 1 |
| `database-query-rules` | SQL、Repository、DAO、Mapper、事务、锁或查询变化 | 数据库第 2 |
| `error-handling-rules` | 异常类、异常处理中间件、重试或错误映射变化 | 横切 Owner |
| `logging-trace-rules` | logger、日志、trace、span 或观测字段变化 | 横切 Owner |
| `time-util-rules` | 时间、日期、时区、时间窗、定时任务或调度变化 | 横切 Owner |

### 前端与语言专项 Owner

| Owner Skill | 触发条件 |
|---|---|
| `frontend-component-rules` | React/Vue 组件文件、组件拆分、props、emits、state、effect、computed、watch、hook、生命周期或组合边界变化 |
| `frontend-ui-visual-rules` | CSS/样式、布局、class/className、颜色、响应式、ARIA、a11y 或视觉交互语义变化；普通 hook/computed 不触发 |
| `golang-patterns` | `.go` 文件、Go 模块或 Go 惯用模式变化 |
| `vue-best-practices` | `.vue` 文件、Vue 组件或 Vue 组合逻辑变化 |
| `vue-router-best-practices` | Vue Router、路由守卫、路由参数或导航变化 |
| `vercel-react-best-practices` | React/Next.js 组件、数据获取、渲染或性能语义变化 |
| `windows-encoding-rules` | `.ps1` / `.bat` / `.cmd`、`.editorconfig` / `.gitattributes`、BOM、非 UTF-8、EOL、乱码、重定向或中文编码证据变化；普通 UTF-8 Markdown/YAML 不触发 |

### 条件 Owner

| Owner Skill | 条件 |
|---|---|
| `micro-business-architecture-rules` | 项目存在微业务标记，且本次改动涉及业务隔离、跨业务 import 或 contract 通信；普通业务逻辑改动不触发 |
| `test-program-rules` | 只在测试程序、fixture、mock、stub 改动时触发；只做结构静态检查，不执行测试 |

## 静态来源清单

- 监督流程必须按 `references/owner-static-source-map.json` 读取 Owner 的当前 `SKILL.md` 与直接 reference 文件；该清单只保存相对路径、glob 与消费方式，不复制规则正文。
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

本矩阵采用封闭世界白名单：允许引用列表中的 28 个 Owner 是监督流程唯一可调用集合；仓库当前或未来出现的其它所有 Skill 一律属于排除集合，即使未在下列分类中逐名列出，也不得由监督流程调用。下列名单用于说明已知高风险类别和审计追踪，不扩大白名单。

### 阶段审查、测试执行与 UI 主导

`code-style-consistency-rules`、`code-style-consistency-rules`、`git-collaboration-rules`、`code-change-finalization-gate-rules`、`test-strategy-rules`、`functional-validation-rules`、`test-regression-rules`、`browser-advanced-testing-rules`、`browser-session-automation-rules`、`project-interface-release-execution-rules`、`web-design-guidelines`、`frontend-design`。

### 需求、Bug、实施与验收

`requirement-boundary-rules`、`requirement-change-rules`、`requirement-intake-rules`、`requirement-splitting-rules`、`bug-fix-proposal-rules`、`bug-intake-rules`、`bug-reproduction-rules`、`bug-root-cause-rules`、`bug-validation-rules`、`implementation-planning-rules`、`implementation-planning-rules`、`delivery-summary-rules`。

### 交付、产物与 Git

`artifact-delivery-gate-rules`、`artifact-storage-rules`、`delivery-summary-rules`、`swag-openapi-maintainer-rules`、`git-collaboration-rules`。

### 运行时、分析与元流程

`code-context-resync-rules`、`codegraph-analysis-rules`、`project-local-skills-rules`、`project-style-rules`、`skill-hit-check-rules`、`skill-audit-rules`、`skill-execution-compliance-gate-rules`、`skill-evolution-rules`、`skill-creator`、`skill-installer`、`find-skills`、`autonomous-execution-rules`、`parallel-task-dispatch-rules`、`team-development-rules`、`execution-failure-learning-rules`、`mcp-installation-rules`、`plugin-installation-rules`。

### 项目分析、文档与专项工程流程

`project-interface-baseline-rules`、`architecture-doc-rules`、`project-design-doc-rules`、`project-timeline-rules`、`project-local-skills-rules`、`project-rule-file-bootstrap-rules`、`godot-project-bootstrap-rules`。`micro-business-architecture-rules` 仅按允许列表中的受控条件作为质量 Owner，不因此放开其它项目流程。

### 状态、记忆、宿主与环境准备

`task-plan-rehydration-rules`、`obsidian-knowledge-flow`、`project-memory-rules`、`thread-title-rules`、`context-compression-rules`、`agent-runtime-recovery-rules`、`project-rule-file-bootstrap-rules`、`recent-context-bootstrap-rules`、`history-recall-rules`、`authenticated-url-routing-rules`、`windows-powershell-environment-rules`、`windows-wsl-execution-rules`。

排除列表中的 Skill 仍可由主流程按其自身触发条件调用；本监督 Skill 永不把它们当作质量 Owner。
