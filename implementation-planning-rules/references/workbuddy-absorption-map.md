# WorkBuddy 官方市场规则吸收裁决表

> 本表是“需求、实施、Bug、测试”四域吸收官方精华的唯一裁决依据。吸收原则：只吸收本地缺失或本地更弱的规则；本地已更强时保留本地并记录裁决；不复制官方整套工作流、不新增同类 skill、不引入 `.codebuddy/specs/` 或 `--skip-tests`。

## 裁决结论总览

| 官方来源 | 官方精华 | 本地现状 | 裁决 | 落点 |
| --- | --- | --- | --- | --- |
| `softspark-ai-toolkit-grill-me`（LobeHub，v1.0.1） | 每个问题附推荐答案（供确认，不写成已确认结论） | 本地缺口追问只列待确认项、不提供推荐答案 | 合并 | `requirement-intake-rules/references/adversarial-gap-interview.md` |
| 同一来源 | 魔鬼代言人反方批评：对每个主要决策挑战假设、列失败方式 | 本地缺口路由与计划自审都偏“识别缺失/覆盖度”，无对抗姿态 | 合并 | `adversarial-gap-interview.md` + `implementation-planning-rules/references/plan-devils-advocate-review.md` |
| 同一来源 | 决策树依赖优先：先核心依赖、后细节分支 | 本地有建议确认顺序，但非显式依赖优先决策树 | 合并 | `adversarial-gap-interview.md` |
| 同一来源 | 一次只问一个问题 | 本地 `gap-routing` 已有一字不差的同义规则 | 保留本地 | 无新增 |
| 同一来源 | 能查代码就不问用户 | 本地 `initial-discovery` 完整路由更强 | 保留本地 | 无新增 |
| 同一来源 | 不满足模糊答案、直到共识 | 本地极致完整性标准与回填闸门更强 | 保留本地 | 无新增 |
| `requirements-driven-workflow/commands/requirements-pilot.md` | 需求 100 分质量门（功能清晰 30 / 技术具体 25 / 实现完整 25 / 业务上下文 20），达到 90 分才移交 | 本地需求接入有检查清单与缺口路由，但没有量化门禁 | 合并 | `requirement-intake-rules/references/workbuddy-quality-gate.md` |
| `clawhub.ai/kevindai/tapd`（OpenClaw，Python 标准库零依赖） | 工作流流转/状态映射/结束状态/工作项类型 | 本地 `tapd-openapi` 无工作流模块 | 合并 | `tapd-openapi/references/workflows.md` |
| 同一来源 | 发布计划（releases） | 本地无 | 合并 | `tapd-openapi/references/releases.md` |
| 同一来源 | 用户待办（users/todo） | 本地无 | 合并 | `tapd-openapi/references/todo.md` |
| 同一来源 | SCM 提交关键字（get_scm_copy_keywords） | 本地无 | 合并 | `tapd-openapi/references/scm-keywords.md` |
| 同一来源 | 企业微信通知（BOT_URL） | 本地无 | 合并 | `tapd-openapi/references/wecom-notify.md` |
| 同一来源 | 短 ID 转长 ID + `?s=mcp` + Basic Auth + 自定义字段前置 | 本地无显式规则 | 合并 | `tapd-openapi/references/id-conversion.md` + SKILL.md 关键规则 |
| 同一来源 | `tapd_client_stdlib.py` 纯标准库脚本 | 本地 curl 已零依赖，但无统一 Python 客户端 | 合并 | `tapd-openapi/scripts/tapd_client_stdlib.py` |
| 同一来源 | 需求/缺陷/任务/评论/迭代/用例/Wiki/工时/附件 CRUD | 本地 `tapd-openapi` 全覆盖且更强（评论转 HTML、环境预检、失败处理） | 保留本地 | 无新增 |
| 同一来源 | 外部整套脚本工作流、OpenClaw 配置形态（`~/.openclaw/openclaw.json`） | 本地用 `TAPD_TOKEN` + curl 体系 | 不吸收 | 无 |
| `skillmd.ai/tdd`（SkillMD，Kent Beck / Feathers / Fowler + Ousterhout 反方） | 红→绿→重构测试先行节奏（无失败测试不写生产代码、一次一个行为） | 本地测试域只有"实现→真实测试→6-review"后置闭环，无测试先行节奏 | 合并 | `implementation-planning-rules/references/tdd-workflow.md` |
| 同一来源 | 三个 TDD pattern（从断言开始/三角测量/直接实现） | 本地无 | 合并 | 同上 |
| 同一来源 | 使用/跳过时机（探索性 spike、紧急 hotfix、纯 UI、一次性脚本跳过） | 本地无显式时机表 | 合并 | 同上 |
| 同一来源 | Ousterhout 反方（探索性/架构性工作先设计，防战术编程） | 本地无平衡机制 | 合并 | 同上 |
| 同一来源 | 测试隔离红线、根 `test/` ASCII 镜像、真实运行验证 | 本地 `test-strategy-rules` / `test-program-rules` / `functional-validation-rules` 全覆盖且更强 | 保留本地 | 无新增 |
| 同一来源 | TDD 免除收口测试、单测替代功能验证 | 本地 P0：真实测试与 6-review 不可免除 | 不吸收 | 无 |
| `codebuddy-plugins-official/godot-mcp`（anengyuki/Godot-mcp，MIT，市场缓存只读） | 三场景分流（make/new/modify + 环境探测 4 标志） | 本地 `godot-project-bootstrap-rules` 只做项目自举，无编辑器操作方法论 | 合并 | `godot-project-bootstrap-rules/references/godot-mcp-operations.md` |
| 同一来源 | 工作区目录契约（active-game.json + godot-editor 平铺） | 本地无 | 合并 | 同上 |
| 同一来源 | build_godot_scene 声明式场景构建（一次传完整树） | 本地无 | 合并 | 同上 |
| 同一来源 | Godot 4 路径与类型约定（res://、Vector2/Color 数组、弧度） | 本地无 | 合并 | 同上 |
| 同一来源 | 部署 5 步 + Debug 三工具（get_debug_errors/get_script_errors/get_editor_output） | 本地无 | 合并 | 同上 |
| 同一来源 | 项目自举、MCP 注册、图像配置模板 | 本地 `godot-project-bootstrap-rules` 主文件已覆盖 | 保留本地 | 无新增 |
| 同一来源 | MCP server / addons GDScript 插件本体 | 属于安装资产，由 `mcp-installation-rules` 处理，不复制进规则体系 | 不吸收 | 无 |
| 外部「任务拆解 / 任务拆解规划」skill（SkillHub 生态） | 检查重复任务 / 依赖环 / 无人负责事项 / 顺序冲突 | 本地有隐式依赖顺序，但无显式任务表体检清单 | 合并 | `implementation-planning-rules/references/plan-review-checklist.md`（任务表体检节） |
| 同一来源 | 不直接承诺工期、不凭空指定负责人或精确排期 | 本地 source-notes 已去掉时间分箱，精神一致但未显式成规则 | 合并 | `implementation-planning-rules/SKILL.md`（显式规则） |
| 同一来源 | 有验收标准、可独立验证、可并行的小任务 + 依赖顺序与检查点 | 本地 `task-granularity-and-order.md` 完全同义且更强（含正反例、坏味道、最小闭环） | 保留本地 | 无新增 |
| 同一来源 | 预计工时估算 | 本地刻意去掉时间分箱（source-notes 明确） | 不吸收 | 无 |
| 同一来源 | 单一责任人分配、Markdown 任务表 + CSV/JSON 导出 | 本地零决策执行模型 + 落盘文档体系，形态冲突 | 不吸收 | 无 |
| 外部「API测试自动化专家版 / API接口测试管理器 / 测试用例生成器」（SkillHub 生态） | 从 OpenAPI/spec 系统化生成测试用例（正向/异常/边界三类 + schema 驱动数据构造 + 认证/分页/依赖场景） | 本地 `apifox` 有 test-case 命令操作细节，但无"测什么、怎么设计用例"的方法论 | 合并 | `apifox-cli__skillhub/modules/test-case-generation.md` |
| 同一来源 | 180 陷阱知识库（请求构造/断言/数据状态/鉴权/接口定义/环境执行） | 本地 apifox 无陷阱库，测试失败排查靠经验 | 合并 | `apifox-cli__skillhub/modules/testing-pitfalls.md` |
| 同一来源 | 测试点分析、契约测试、性能测试方法论 | 本地无显式测试点分析；契约/性能映射为 apifox runner + 断言 | 合并 | `test-case-generation.md`（映射到 apifox 能力） |
| 同一来源 | apifox 命令操作细节（categoryId/处理器/断言字段/导入导出质量指标） | 本地 `modules/test-case.md` / `test-automation.md` / `import-export.md` 已覆盖 | 保留本地 | 无新增 |
| 同一来源 | Web UI 查看编辑、按项目分组管理 | apifox 客户端自带 | 不吸收 | 无 |
| 本地 `project-interface-release-execution-rules`（同源 skill 精华回收到 apifox） | P0/P1/P2 风险分级 + 必测/可选/跳过范围选择 | apifox skill 无范围选择策略 | 合并 | `apifox-cli__skillhub/modules/test-selection-policy.md` |
| 同一来源 | 8 级参数来源优先级（可复用/上游/数据库/缓存/OpenAPI 示例/fixture/规则/不存在数据） | apifox skill 无数据构造方法论 | 合并 | `apifox-cli__skillhub/modules/test-data-and-judgement.md` |
| 同一来源 | 响应判定（通过/不通过/待确认 + 阻断分类 BLOCKED_BY_DEPENDENCY 等） | apifox skill 无判定规则 | 合并 | 同上 |
| 同一来源 | `release_test_engine` 多协议执行引擎（HTTP/SSE/WebSocket/GraphQL/gRPC/SOAP） | apifox CLI 自带 runner 执行能力 | 保留本地（不迁移引擎代码） | 无 |
| 同一来源 | 上线门禁报告、双轨对账、场景契约等重流程 | 属于上线门禁域，与 apifox 场景形态不同 | 不吸收 | 无 |
| 同一文件 | 实施前先只读扫描代码库，形成上下文报告后再进入需求确认 | 本地实施规划有目录树与落点契约，但没有显式“先探索、总结发现、批准后编码” | 合并 | `implementation-planning-rules/references/pre-implementation-code-exploration.md` |
| 同一文件 | 需求达到 90 分后必须停下等用户显式批准再实施 | 本地已有需求稳定后移交实施规划，但批准闸门不显式 | 合并 | 需求质量门参考与实施规划规则 |
| `feature-dev/commands/feature-dev.md` | 深入理解代码库、识别未定义细节、设计后再实现 | 本地实施规划已覆盖零决策、落点与周期，但“先探索再设计”不显式 | 合并 | `pre-implementation-code-exploration.md` |
| `feature-dev/agents/code-architect.md` | 从最小改动、干净架构、务实平衡三个角度设计方案 | 本地已有多方案收敛与推荐路线要求 | 保留本地 | 无新增 |
| `requirements-driven-workflow/agents/requirements-review.md` | 代码审查按功能、集成、质量、性能评分 | 本地已有 `6-review` 风格回归与实施规划自审 | 保留本地 | 无新增 |
| `requirements-driven-workflow/agents/requirements-testing.md` | 风险导向测试：关键路径优先、真实场景、错误处理与集成验证 | 本地测试策略已有优先级模型与测试隔离红线 | 合并 | `test-strategy-rules/references/risk-based-test-conclusion.md` |
| `requirements-driven-workflow/commands/requirements-pilot.md` | `--skip-tests` 可跳过测试 | 本地 P0：测试不能跳过 | 不吸收 | 无 |
| 同一文件 | `.codebuddy/specs/` 目录落盘整套工作流 | 本地已用 `doc/` 与 skill references 统一管理 | 不吸收 | 无 |
| 同一文件 | `requirements-pilot` 阶段问答链与子代理链 | 本地已有实施规划、测试、审查分工 | 不吸收 | 无 |
| `feature-dev/commands/feature-dev.md` | Feature Dev 阶段问答链（发现、探索、澄清、架构、实现、审查、总结） | 本地四域 skill 已覆盖对应职责，不复制整套流程 | 不吸收 | 无 |
| `requirements-driven-workflow/agents/requirements-generate.md` | 技术规格直接映射文件、函数、接口、配置与验证 | 本地实施总览/周期已要求文件/符号落点与真实测试 | 保留本地 | 无 |

## 吸收后必须保持的边界

- 不新增 Skill 目录，不复制官方插件目录。
- 不引入 `.codebuddy/specs/`、`--skip-tests`、`requirements-pilot` 或 Feature Dev 阶段问答链作为正式入口。
- 本地四类 skill 仍是唯一 Owner；官方精华只作为 references 或正文补充。
- 所有吸收内容必须能回指官方只读路径与本地原规则，避免“为吸收而吸收”。

## 证据与校验

- 官方只读路径：`C:\Users\luode\.workbuddy\plugins\marketplaces\codebuddy-plugins-official\plugins\requirements-driven-workflow\...`、`...\feature-dev\...`。
- 本表与四份新增 reference、四个 `SKILL.md` references 区段保持一致；任一不一致即阻断收口。
| `skillmd.ai/skills/test-cases`（SkillMD，MIT，作者 cexll）+ 用户描述增强版 | 从 PRD/用户故事/验收标准/功能拆分文档提取需求生成用例（需求驱动非实现驱动） | 本地 `apifox/modules/test-case-generation.md` 只有接口定义驱动，无需求文档输入源 | 合并 | `apifox-cli__skillhub/modules/test-case-from-requirement.md` |
| 同一来源 | 需求完整性五维预检（业务规则/角色权限/状态/边界/异常处理），缺必填主动询问 | 本地有需求追问文化（adversarial-gap-interview）但无"用例生成前完整性检查"显式步骤 | 合并 | 同上 |
| 同一来源 | 四类场景覆盖（功能/边界/错误/状态转换，含无效转换矩阵） | 本地有正/异/边界三类 + 状态测试点，状态转换全矩阵不显式 | 合并 | 同上 |
| 同一来源 | 12 字段用例模板（ID/标题/需求链接/优先级/类型/前置条件/测试数据/步骤/预期结果/后置条件/自动化建议/依据） | 本地 `test-case.md` 有 apifox 字段、generation 有断言模板，无需求驱动用例字段规范 | 合并 | 同上 |
| 同一来源 | 需求追溯矩阵 RTM（需求↔用例↔覆盖状态，双向追溯） | 本地无 RTM 输出模板 | 合并 | 同上 |
| 同一来源 | 按风险选择测试设计方法（等价类/边界值/决策表/状态转换/场景法） | 本地有 P0/P1/P2 接口分级，无"按风险选设计方法"表 | 合并 | 同上 |
| 同一来源 | 优先级赋值（核心流程/数据完整性/安全/收入→High） | 本地 `test-selection-policy.md` P0/P1/P2 更细（接口域） | 保留本地 | 无新增 |
| 同一来源 | 好/差用例判据、7 陷阱、10 项质量清单 | 本地 `testing-pitfalls.md` 180 陷阱更强 | 保留本地 | 无新增 |
| 同一来源 | 红线：不编造规则、不声称已执行/完整覆盖 | 本地 `functional-validation-rules` + `test-data-and-judgement` 伪通过检查更强 | 保留本地 | 无新增 |
| 同一来源 | 输出 MD/CSV/Excel/JSON、输出到 `tests/<name>-test-cases.md` | apifox 导入导出 + `doc/5-tests/` 测试主文档体系已覆盖且更强 | 保留本地 | 无新增 |
