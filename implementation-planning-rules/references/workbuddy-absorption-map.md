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
| BuiltinMarket「自然改写」(write v1.0.1，SkillHub 生态) | 编辑哲学五条（过度编辑=失败/作者声音赢/禁用词表是例子/少而强/规则不单调增长） | 本地白话契约只要求"短句和常用中文"，无编辑取舍哲学 | 合并 | `artifact-delivery-gate-rules/references/natural-writing-ai-taste-removal.md`（§0） |
| 同一来源 | AI 味 20 模式（段末重述/升华/对比/瓶颈转移/系统定义/挑战展望/同义词循环/虚假范围/免责声明残留…） | 本地 `humanizer-zh` 有 9 类泛用模式，无中文技术文模式库 | 合并 | 同上（§2） |
| 同一来源 | 翻译腔 4 套路（物理动词/形容词预判/抽象名词主语/未译英文混入） | 本地无 | 合并 | 同上（§3） |
| 同一来源 | 专家腔 10 条（不补实作细节/元叙事/二人称预测/announce 引子/章节编号前缀/学习路径不改教程） | 本地无；"不补实作细节"与工程文档不编造红线同向 | 合并 | 同上（§4） |
| 同一来源 | 用词去正式化 + 高频替换表（非常→很/例如→比如/综上所述→直接收尾/报告腔清单） | 本地无行文用词表 | 合并 | 同上（§5） |
| 同一来源 | 句式/标题/列表/引号括号分号规则（电报句/bold+句号/判断式标题/列表去 list 化/括号超 10 字改写） | 白话契约无行文层规则 | 合并 | 同上（§6-8） |
| 同一来源 | 长文结构模式（跨章节同义清单/表格旁复读/删段先确认信息量） | 白话契约有附录分层，无结构复读检查 | 合并 | 同上（§9） |
| 同一来源 | 对外发文专项（身份脱敏/不踩竞品/用户感受先于功能清单） | 本地 delivery-summary 是内部交付，无公开文案红线 | 合并 | 同上（§10） |
| 同一来源 | 标点门禁脚本（check_punctuation.py：全角/半角/中西空格/禁破折号，跳过代码块/URL） | 本地无自动标点检查 | 合并 | `artifact-delivery-gate-rules/scripts/check_punctuation.py` + `check-punctuation.sh` |
| 同一来源 | 白话契约第 2 节"短句和常用中文"模糊要求 → 替换为自然行文规则引用 | 本地旧契约不可执行 | 合并（改写） | `plain-language-document-contract.md` §2 + §6 自检扩 8 条 |
| 同一来源 | durable-context（记忆非授权/当前状态优先/redaction gate） | 本地 PROJECT_MEMORY/零决策模型已覆盖精神 | 保留本地 | 无新增 |
| 同一来源 | 推文五规则、社交文案模式、product localization review | 本地无社交/多语言产品文案场景，低频 | 拒绝 | 无 |
| 同一来源 | pre-flight 受众锁定、语言检测 | 本地工程文档受众由 `reader_level: business_general` 固定 | 保留本地 | 无 |
| `woohahahaaa/auto-rename-session-label`（ClawHub/SkillHub，OpenClaw hook，message:received） | 仅对尚无标题的会话自动生成标题（幂等门槛，不覆盖已有 label） | 本地"标题已准确则跳过"已有精神，但无"仅空/泛化标题才生成"显式门槛 | 合并 | `thread-title-rules/SKILL.md` 适配节 + workbuddy-host-contract.md |
| 同一来源 | 用该会话当前使用的模型生成标题 | 本地未指定生成模型 | 合并 | `thread-title-rules/SKILL.md` 标题生成规则第 8 条 |
| 同一来源 | 失败安全降级：截断首条用户消息保证有标题 | 本地失败即跳过、无降级 | 合并 | `thread-title-rules/references/workbuddy-host-contract.md` 失败降级节 |
| 同一来源 | 便携性：无硬编码路径，运行时解析 home/agentId/dist | 本地自举硬绑定 Codex 路径 | 合并 | `thread-title-rules/workbuddy/rename-session.py`（运行时解析 WORKBUDDY_CONFIG_DIR） |
| 同一来源 | 独立副作用：只写 label，不干预 prompts/tools/消息流 | 本地"只负责会话元数据命名"已有精神 | 合并 | 边界声明强化（SKILL.md 适配节） |
| 同一来源 | 写后核对验证（hooks list/info + sessions.json 人工核对） | 本地以"真实工具结果证明"但无回读校验 | 合并 | `rename-session.py` SELECT 回读 `verified:true` |
| 同一来源 | 失败诊断：label 恒为截断首条消息 = LLM 分支失败 | 本地无诊断指引 | 合并 | workbuddy-host-contract.md 失败路由表 |
| 同一来源 | `openclaw hooks enable` CLI 安装机制 | WorkBuddy 宿主无 openclaw CLI，引入宿主无关依赖 | 拒绝 | 无 |
| 同一来源 | 写 OpenClaw `sessions.json` label 字段 | 宿主错误（本地目标是 WorkBuddy） | 拒绝 | 无（替换为 workbuddy.db 适配） |
| `finia2na/auto-session-labels`（ClawHub 插件） | 会话须同时含用户消息+助手回复才生成（资格门槛） | 本地无显式资格门槛 | 合并 | `thread-title-rules/SKILL.md` 触发/跳过语义 |
| 同一来源 | 写入前原子重查当前 label，防止生成期间被手动修改 | 本地无并发保护 | 合并 | `rename-session.py --expect-old` + workbuddy-host-contract.md |
| 同一来源 | 空/泛化/不安全模型输出忽略 | 本地无 | 合并 | `thread-title-rules/SKILL.md` 标题生成规则第 8 条 |
| 同一来源 | maxLabelLength 60 字符 | 本地 8-24 字更严格 | 保留本地 | 无新增 |
| 同一来源 | maxTokens 32 默认值 | 与本地 24 字上限冲突且过低（外部自身 SKILL.md 亦注明 1024 更稳） | 拒绝 | 无 |
| 本地 `thread-title-rules` 根因修复 | 根因：Codex 宿主绑定（MCP `rename_current_thread` + `~/.codex/config.toml`）在 WorkBuddy 静默失效 → 新增 WorkBuddy 原生适配（`workbuddy.db` sessions.custom_title 用户改名槽，双宿主矩阵互斥路由）；title 字段为主进程独占自动摘要槽、agent 写入会被回写覆盖（实测），禁止作为改名目标 | 本地无 WorkBuddy 路径 | 修复升级 | `workbuddy/rename-session.py` + `references/workbuddy-host-contract.md` + SKILL.md 双宿主矩阵 |
| 本地 `thread-title-rules` 强项 | 中文 8-24 字、对象+动作/症状/阶段、稳定不频繁改名、跳过条件矩阵、工具与证据约束、Codex 自举 | 外部无此精细规则 | 保留本地 | 无新增 |

## 2026-08-23 吸收：dw-goal-breakdown（SkillHub 目标拆解）

- **来源**：`dw-goal-breakdown`（SkillHub 安装源，工作区 `D:\谷歌云盘\luode-skills\dw-goal-breakdown__skillhub\`，SKILL.md 读原文；v1.0.0，作者 Dream，MIT）
- **拆解原子条目**：5 条 → 合并 4 / 拒绝 1

| # | 外部精华 | 本地现状 | 裁决 | 落点 / 理由 |
|---|---------|---------|------|------------|
| 1 | 适用场景三件套：目标写成可衡量结果 / 拆月→周→日 / 标今日第一步 | 本地无自有目标拆解规则；long-run-loop-rules 只做执行循环 | 合并 | `implementation-planning-rules/references/goal-breakdown-seed.md`（新建，工程域入口）|
| 2 | 倒推法：澄清目标与 deadline → 拆 3 层动作 → 最小可行步 | 本地无同义规则 | 合并 | 方法本体单一权威在 `long-run-loop-rules/references/goal-breakdown-before-loop.md`；seed 引用式接入 |
| 3 | 首个最小可行步（默认 10 分钟内可启动） | 本地无 | 合并 | seed.md「最小步下沉」节：首个任务必须短时可启动 |
| 4 | 示例：转行做开发 → 季度学基础/月做项目/周刷题 + 今日选入门课 | 本地无 | 合并 | seed.md 示例节（改写为本地口径）|
| 5 | 源文件排版缺陷（逐字换行乱码、`示例: None` 占位） | 本地 skill 规范禁止乱码与空占位 | 拒绝 | 缺陷形态不吸收 |

- **落盘改动**：
  - 新增 `references/goal-breakdown-seed.md`（约 1.4KB，引用式）。
  - 修改 `SKILL.md`：自动触发信号补 1 条（模糊大目标计划型问题 → 轻量拆解入口）、references 读取规则补 1 条。
  - `references/source-notes.md` 追加来源记录。
- **整理去重**：方法步骤在 seed.md 与 before-loop.md 高度重复 → 收敛为「单一权威（before-loop）+ 引用式（seed）」，seed 已重写不重复定义步骤。
- **同域扫描结论**：范围 = implementation-planning-rules / long-run-loop-rules / requirement-splitting-rules / requirement-intake-rules / goal__skillhub / autonomous-execution-rules。关键词（倒推法/最小可行步/周→日/10 分钟可启动/拆解目标/大目标太小步）扫描：除本次两处新落盘文件外 0 命中；无门控层叠（long-run-loop 侧触发词已限定"目标模糊需先拆解再执行"）；无散落产物；引用链可达（seed → before-loop 跨 skill 相对路径正确）。**PASS**。
- **环境依赖**：N/A（规则纯文本，无环境变量/宿主配置/hook/依赖/路径引用）。
- **自检能力**：N/A（无环境依赖项）。
- **净增体积**：+约 1.4KB（seed.md）+ 约 0.3KB（SKILL.md 两行 + source-notes 一段）；引用式接入，不构成膨胀。
- **棘轮验证**：8 维评分 implementation-planning-rules 基线 85.0 → 吸收后 90.5（+5.5，主要提升：边界条件覆盖模糊目标 fallback、资源整合跨 skill 引用链）；新分严格高于基线，保留。评分方式：第三方视角（间隔一轮重新打分）。
- **删除源**：已删除工作区安装源 `dw-goal-breakdown__skillhub/`。

## 2026-08-23 吸收：conductor（Context-Driven Development，实施执行协议）

- **来源**：`conductor`（市场 `codebuddy-plugins-official/external_plugins/conductor`，本地只读缓存；Google Conductor 的 Claude Code 移植版，Apache-2.0；原文 = README + context-driven-development/track-management/workflow-patterns 三 SKILL + new-track/implement 两 command + conductor-validator）
- **拆解原子条目**：18 条 → 合并 8 / 保留本地 8 / 拒绝 2

| # | 外部精华 | 本地现状 | 裁决 | 落点 / 理由 |
|---|---------|---------|------|------------|
| 1 | Context→Spec&Plan→Implement 三阶段工作流 | REQ→AC→CYCLE→TASK + 上下文四件套更强 | 保留本地 | 无新增 |
| 2 | 上下文工件四文档（product/tech-stack/workflow/tracks） | PROJECT_CURRENT/MEMORY/HISTORY/STYLE 四件套等价 | 保留本地 | 形态映射已存在 |
| 3 | 实施前上下文校验（读→标过时→提议更新→确认） | `pre-implementation-code-exploration.md` 只覆盖代码库探索 | 合并 | `task-execution-protocol.md`「实施前上下文校验」节 |
| 4 | spec.md 模板（FR/NFR/AC/Scope/Risks） | requirement-structure-template + 极致完整性更强 | 保留本地 | 无新增 |
| 5 | plan.md 分阶段模板 | implementation-cycle-template 更强 | 保留本地 | 无新增 |
| 6 | 任务状态标记协议：`[ ]`/`[~]`/`[x]`/`[-]`/`[!]` 五态 | 无清单标记约定（仅单任务内部状态机） | 合并 | `task-execution-protocol.md`「状态标记」节 |
| 7 | 任务完成记录 commit SHA（plan 内可追溯） | 「绿后提交」无 plan 内 SHA 记录要求 | 合并 | 同上 |
| 8 | 阶段检查点机制（阶段完成→验证→checkpoint SHA；**去掉原版人工审批**） | 有最小任务闭环+6-review，无阶段级检查点协议 | 合并(适配) | 同上；放行走本地既有闸门，不引入人工等待 |
| 9 | 偏差标注格式（DEVIATION/Reason/Impact 三级 + 四类型分层） | requirement-change-rules 管需求层面，无执行期偏差标注格式 | 合并 | 同上（执行期偏差）；需求层面仍归 change-rules |
| 10 | 按工作单元语义回滚（周期/阶段/任务靠 plan 内 SHA 定位） | git-collaboration-rules 管 git 操作，无计划单元级回滚映射 | 合并 | 同上（git 红线仍归 git-collaboration-rules） |
| 11 | 任务规模量化指南（2-4 阶段/8-20 任务；>5 阶段或 >25 任务过大） | splitting 域无量化规模；本地单任务 ≤5 文件为文件粒度 | 合并 | 同上 |
| 12 | TDD 11 步核心节奏（RED→GREEN→REFACTOR） | `tdd-workflow.md` 已吸收且更强 | 保留本地 | 无新增 |
| 13 | git notes 附加任务摘要 | 无 git notes 用法 | 合并(轻量) | 同上「可选增强」1 句 |
| 14 | 覆盖率 80% 目标 | test-strategy-rules 管覆盖策略，不写死通用值 | 保留本地 | 无新增 |
| 15 | 错误恢复（测试失败回退/检查点拒绝/依赖阻塞） | error-handling-rules / bug-validation-rules 等价 | 保留本地 | 无新增（`[!]` 标记并入 #6） |
| 16 | 上下文反模式（Stale/Sprawl/Implicit/Hoarding/Over-Spec） | project-memory-rules 管记忆维护 | 保留本地 | 无新增 |
| 17 | plugin 命令形态（/setup /new-track /implement 等） | 本地是规则 skill 非 CLI 插件 | 拒绝 | 形态不匹配 |
| 18 | conductor/ 专属目录 + metadata.json 进度跟踪 | artifact-storage path-map + PROJECT_CURRENT.md 已有等价 | 拒绝 | 形态不匹配 |

- **落盘改动**：
  - 新增 `references/task-execution-protocol.md`（8643B：状态标记五态 + SHA 追踪 + 阶段检查点适配版 + 偏差标注 + 语义回滚 + 规模量化 + 实施前校验 + git notes）。
  - 修改 `SKILL.md`：references 读取规则补 1 条（+4/-1 行）。
  - `references/source-notes.md` 追加来源记录。
- **用户调整**：阶段检查点审批协议中的人工审批规则不吸收（本地零决策执行模型：强模型冻结决策、执行模型自动闭环），只保留「验证→记录→放行」机制，审批走本地既有闸门。
- **整理去重**：外部 4 文件约 20KB → 合并 8 项精华 → 新增 8643B；TDD 节奏已存在（tdd-workflow.md）不重复吸收。
- **同域扫描结论**：范围 = implementation-planning-rules / tdd-workflow（节奏互补）/ minimum-task-execution-contract（状态机互补）/ requirement-change（偏差分层）/ git-collaboration（git 机制边界）/ task-granularity-and-order（规模互补）。关键词（五态标记/checkpoint/DEVIATION/人工审批/语义回滚/规模阈值）扫描：除本次新落盘文件外 0 命中；无门控层叠；引用链可达。**PASS**。
- **环境依赖**：N/A（规则纯文本）。
- **净增体积**：+8643B（新 reference）+ 约 0.2KB（SKILL.md 登记）。
- **棘轮验证**：8 维评分 implementation-planning-rules 基线 63.3 → 吸收后 88.4（+25.1，主要提升：实测表现 3→9 四场景全部可直接执行、边界条件覆盖阻塞/跳过/规模阈值、检查点设计去掉人工审批适配零决策模型）；新分严格高于基线，保留。评分方式：独立子 agent 第三方视角。
- **删除源**：市场缓存为只读共享资产，不删除。
