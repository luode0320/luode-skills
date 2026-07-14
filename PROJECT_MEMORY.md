# 项目长期记忆

## 白话文档与附录分层规则

- 需求、实施、审查、验收、Bug、测试、架构、交付和工作报告采用同一信息分层：H1 后单段正文固定说明结论、影响、范围、非范围、变化、完成标准、术语说明和验证状态；文件、命令、稳定 ID、追踪矩阵和证据分别进入执行附录或追踪附录。
- 审查或验收不适用时，必须说明原因和依据，但不构成任务阻断；只有需求明确要求该验证、当前必须完成且无可接受替代验证时，条件缺失才阻断。
- 新文档以 `reader_level: business_general`、`writing_style: plain_chinese`、`appendix_policy: preserve_existing_or_one_terminal_appendix` 和 `review_acceptance_gates` 启用机器门禁；24 个受管模板由 `plain-language-template-registry.yaml` 统一登记并逐项测试；未修改历史文档不批量迁移，在新建或后续修改时迁移。
- 审查、验收、功能验证、浏览器联调和第三方验证统一使用 `review-acceptance-gate-contract.md`：不适用不阻断，受限可继续但不能正式放行，明确必需且无替代验证才阻断。
- 来源：`artifact-delivery-gate-rules/references/plain-language-document-contract.md`、`artifact-delivery-gate-rules/references/review-acceptance-gate-contract.md`、`artifact-delivery-gate-rules/scripts/validate_engineering_docs.py`。
- 更新时间：2026-07-14。

## 任务阻断收口与恢复规则

- 真实阻断唯一使用 `artifact-delivery-gate-rules/references/task-blocker-closure-contract.md` 的 `BLK-*` 记录，至少包含任务状态、阻断阶段、依据与证据、已尝试动作与停止边界、影响、至多三步解决计划、恢复后重入点和去重键。
- 审查、验收、功能验证、Bug 验证、执行失败和运行时恢复只生产或校验阻断事实；`reasoning-summary-structure-rules` 是唯一面向用户渲染“任务阻断收口”的 owner，避免多处输出冲突计划。
- 仅 `blocked` 与 `manual_handoff` 触发任务阻断收口。`limited`、`not_applicable`、P2/P3、用户取消和预期负向测试不得生成 `BLK-*` 或写成任务已阻断。
- 阻断计划最多三步；每步必须包含责任方、前置条件、动作、完成判据和验证入口。恢复后从原测试、复审、重验或健康检查的重入点继续。
- 文档校验的正文 `N/A` 规则忽略 fenced code、示例与 Mermaid 内容，避免图中“不适用”分支被误判；正文声明仍必须给出原因或证据。
- 来源：`artifact-delivery-gate-rules/references/task-blocker-closure-contract.md`、`reasoning-summary-structure-rules/SKILL.md`、`artifact-delivery-gate-rules/scripts/validate_engineering_docs.py`。
- 更新时间：2026-07-14。

## Windows PowerShell 环境可靠性规则

- `windows-powershell-environment-rules` 的会话默认策略是 `RequiredOnly`：`ready` 和 `degraded` 可以继续，只有 `blocked`、`busy`、`failed`、`rollback_refused` 不能作为已准备好结论。
- 包恢复只接受 manifest 或调用方提供的精确 source/package ID；未知命令不搜索猜包。Git Bash 只能从 Git 安装根目录的 `bin\\bash.exe` 加 `MINGW|MSYS` 身份识别，WSL 原生命令仍交给 `windows-wsl-execution-rules`。
- profile 与 Terminal 的 Apply/Rollback 由事务、备份和 after hash 保护；WhatIf 不写用户状态，hash 漂移时必须拒绝覆盖。含中文的 PowerShell 5.1 脚本使用 UTF-8 BOM，避免被默认 ANSI 解码。
- 验证固定为临时目录 fixture：PowerShell 5.1 与 PowerShell 7 都要通过 TEST-PSENV-001 至 TEST-PSENV-009；不连接网络、不安装软件、不改真实用户配置。
- 来源：`windows-powershell-environment-rules/SKILL.md`、`references/runtime-state-contract.md`、`doc/7-验收/2026-07-13_230500_WindowsPowerShell环境可靠性升级_最终验收.md`。
- 更新时间：2026-07-13。

## 统一智能体运行期自恢复规则

- 稳定决策：`agent-runtime-recovery-rules` 是厂商无关的运行期恢复唯一 owner，覆盖 MCP、插件、浏览器会话、工具 transport 和智能体宿主；安装/注册仍由安装类 skill 负责，失败分类与案例生命周期仍由 `execution-failure-learning-rules` 负责。
- 稳定决策：恢复动作必须通过真实 adapter capability 准入，能力等级为 L0 观测、L1 探针、L2 重连、L3 重载、L4 受控重启、L5 检查点恢复与任务续接；无 L5 lifecycle API 时不得宣称任务自动续接。
- 稳定决策：运行期恢复固定使用单飞锁、一次不变复验、每层最多一次动作、默认 600 秒冷却、幂等性分类和脱敏 checkpoint；非幂等或幂等性未知的写操作只允许查询状态并转人工交接。
- 稳定决策：当前仓库只提供标准库状态原语 `agent-runtime-recovery-rules/scripts/recovery_state.py` 与 local 契约测试；真实平台插件重载、宿主重启和 L5 resume 由外部 adapter 提供，不能由规则猜测或伪造。
- 来源：`agent-runtime-recovery-rules/SKILL.md`、`references/adapter-contract.schema.json`、`doc/2-需求/2026-07-12_210000_统一智能体运行期自恢复规则.md`。
- 更新时间：2026-07-12。

## 通用上线测试引擎

- 稳定决策：`project-release-test-rules/scripts/release_test_engine/` 是协议中立内核，统一 IR 版本为 `2.0`；未知技术栈必须输出 `PENDING/UNSUPPORTED_ADAPTER`，不得伪报通过。
- 稳定决策：所有运行连接只来自 `local` 配置；普通业务写接口允许执行，DROP/TRUNCATE/破坏性 ALTER、源码/基础设施删除等极端操作由安全 denylist 阻断。
- 稳定决策：接口级结果固定为 `PASS`、`EXPECTED_FAIL`、`FAIL`、`PENDING`、`BLOCKED`；P0 入口任意非 `PASS` 阻断项目放行，项目门禁输出 `PASS`/`FAIL`/`PARTIAL`。
- 稳定决策：兼容入口为 `generate_release_test_plan.py doctor/run`，旧资产命令保留回退路径；项目专属字段只能写入项目基线/adapter，通用规则不得硬编码业务实体。
- 稳定决策：发现注册表覆盖 HTTP、CLI、GraphQL、gRPC、WebSocket、SOAP、JSON-RPC、消息、调度和事件；只有存在真实 local runner 的协议才允许 `PASS`，其余协议必须输出结构化 `PENDING`。
- 稳定决策：报告明细的 request/response 固定为脱敏 JSON 字符串，`responses.json` 保留脱敏对象；基线以 append-only 事件和 v2 原子投影为事实源。

## 核心记忆

### 仓库定位
- 别名: skill 仓库, 团队研发协作规则仓库
- 类型: 项目事实
- 定义: 本仓库用于沉淀面向团队研发协作的 Skill、references、脚本和入口文档，目标是让 AI 在需求、Bug、编码、审查、测试、交付流程中按任务内容自动命中规则。
- 来源: `README.md`、`项目设计.md`
- 适用范围: 全仓库
- 更新时间: 2026-06-27
- 状态: 启用

### 根目录主入口
- 别名: 仓库入口文档
- 类型: 文档入口
- 定义: 仓库根目录长期主入口文档包括 `README.md`、`编码skill.md`、`字典.md`、`项目设计.md`、`PROJECT_MEMORY.md`、`PROJECT_STYLE.md`。
- 来源: 根目录真实文件结构
- 适用范围: 全仓库
- 更新时间: 2026-06-27
- 状态: 启用

### 研发产物目录正式口径
- 别名: doc 顶层目录规则
- 类型: 目录规则
- 定义: 正式研发产物目录统一收口到 `doc/` 下；当前正式活动子目录按流程顺序编号为 `doc/1-架构/`、`doc/2-需求/`、`doc/3-实施/`、`doc/4-bugs/`、`doc/5-tests/`、`doc/6-审查/`、`doc/7-验收/`。
- 来源: `artifact-storage-rules/references/path-map.yaml`
- 适用范围: 文档归档与规则引用
- 更新时间: 2026-06-28
- 状态: 启用

### 活动文档命名前缀
- 别名: 来源对象标识, 实施需求标识, 审查时分秒, Bug 进入实施验收
- 类型: 命名规则
- 定义: 需求、实施、Bug、测试、审查、验收等活动产物统一使用 `YYYY-MM-DD_HHmmss` 时间前缀。实施、审查、验收这类下游文档必须在时间后保留来源对象标识，来源可以是需求也可以是 Bug；来源对象标识不重复前置时间戳，优先使用来源中文主干或短 ID，必要时加 `需求-` 或 `Bug-` 类型前缀。典型格式为 `YYYY-MM-DD_HHmmss_<项目或来源集合标识>_需求与实施计划全量顺序实施方案.md`、`YYYY-MM-DD_HHmmss_<来源对象标识>_实施周期NN_周期说明.md`、`YYYY-MM-DD_HHmmss_<来源对象标识>_<审查中文主题>.md`、`YYYY-MM-DD_HHmmss_<来源对象标识>_最终验收.md`；禁止只写 `时间_阶段_说明.md`、`YYYY-MM-DD_主题.md` 或缺少来源标识的 `YYYY-MM-DD_HHmmss_主题.md`。
- 来源: `artifact-storage-rules/references/path-map.yaml`、`artifact-storage-rules/references/naming-templates.md`
- 适用范围: 需求域、实施域、Bug 域、测试域、审查域、验收域
- 更新时间: 2026-06-29
- 状态: 启用

### 架构专题文档规则
- 别名: architecture-doc-rules, 架构文档目录
- 类型: 文档规则
- 定义: `architecture-doc-rules` 专门负责 `doc/1-架构/` 下的长期架构专题文档。四个有序中文主入口固定为 `1-总架构.md`、`2-目录树.md`、`3-模块职责.md`、`4-主要业务链路.md`；业务链路从序号 `5` 开始，同一链路保留原编号更新，新增独立链路取当前最大业务链路编号加一并回写索引，历史编号不复用、不重排。其他长期专题使用 `附录-<架构中文主题>.md`，不占用业务链路编号。根目录 `项目设计.md` 继续保持项目级总览入口。
- 来源: `architecture-doc-rules/SKILL.md`、`artifact-storage-rules/references/path-map.yaml`
- 适用范围: 架构域、项目设计域
- 更新时间: 2026-06-28
- 状态: 启用

### 需求主动侦察链路
- 别名: 老板式 idea 转需求, idea 侦察, 需求 discovery
- 类型: 流程规则
- 定义: 当用户只提出一句话 idea、粗略想法或老板式方向时，优先由 `requirement-discovery-rules` 主动侦察当前项目代码、文档、数据库线索、上下游服务、第三方调用、关联项目、GitHub、相关网站、官方 API 文档和用户补充路径或 URL，形成有证据来源的需求设计；外部资料默认遵循“官方文档/官网/自有仓库与站点优先，公共 GitHub 与社区资料只作补充”的优先级。已验证可复用的资料位置、数据库、URL、项目路径和侦察经验必须继续通过 `project-memory-rules` 回写长期记忆。
- 来源: 对话确认、`requirement-discovery-rules`
- 适用范围: 需求域
- 更新时间: 2026-06-28
- 状态: 启用

### 需求域第一入口
- 别名: 需求 skill 顺序, 需求前置入口
- 类型: 流程规则
- 定义: 当前对外统一流程为 `Idea/Discovery -> Intake -> 条件闸门 -> 验收标准 -> 实施 -> 测试 -> 审查 -> 最终验收`。其中需求域主流程收口到 `Idea/Discovery -> Intake`，条件步骤为 `Gap / Boundary / Splitting / Change`；`acceptance-criteria-rules` 负责前置验收标准，`implementation-planning-rules` 负责独立实施域，`final-acceptance-rules` 负责后置最终验收。内部默认仍以 `requirement-discovery-rules` 为第一入口；`requirement-intake-rules` 负责在 discovery 初稿后立即创建需求主文档，`requirement-gap-rules` 只处理主动侦察后仍无法补齐的关键缺口。需求阶段只允许读仓库、读资料、整理文档；不允许把 agent 猜测写成需求答案，也不允许“先做了再补需求”。需求主文档未真实落盘前，禁止进入实施规划与正式编码。需求、验收标准和实施计划完成后仍不得自动开工，必须等用户明确“开始实施/开始执行”后才能进入正式编码。
- 来源: `requirement-discovery-rules/references/requirement-domain-routing.md`、`编码skill.md`
- 适用范围: 需求域
- 更新时间: 2026-06-30
- 状态: 启用

### 需求临时缺口文档规则
- 别名: gap 临时文档, 缺口阻断文档
- 类型: 流程规则
- 定义: `requirement-gap-rules` 只处理 discovery 之后仍无法补齐的关键缺口；gap 阶段允许在 `doc/2-需求/` 下创建一份临时缺口文档，记录已侦察证据、待确认问题和阻断结论。用户确认并补齐后，必须先把稳定结论回填主需求文档，再删除临时缺口文档；未确认前不得删除，也不得继续进入验收标准、实施或最终验收。

### 双层验收规则
- 别名: 前置验收 + 最终验收, 验收双层机制, Bug 验收
- 类型: 流程规则
- 定义: 验收统一归入“验收”大类，分为前置 `验收标准` 与后置 `最终验收` 两层，来源对象可以是需求也可以是 Bug。前置验收标准由 `acceptance-criteria-rules` 生成并落到 `doc/7-验收/YYYY-MM-DD_HHmmss_<来源对象标识>_验收标准.md`；后置最终验收由 `final-acceptance-rules` 生成并落到 `doc/7-验收/YYYY-MM-DD_HHmmss_<来源对象标识>_最终验收.md`。测试和审查未完成时，最终验收必须阻断。
- 来源: `artifact-storage-rules/references/path-map.yaml`、`acceptance-criteria-rules`、`final-acceptance-rules`
- 适用范围: 验收域
- 更新时间: 2026-06-27
- 状态: 启用

### 实施开工授权与自动推进
- 别名: 开始实施确认, 开工授权, 最小任务自动推进, 长文本执行边界
- 类型: 流程规则
- 定义: 来源对象文档（需求或 Bug）、前置验收标准和实施总览/实施周期即使都已完成，也不构成自动开工授权；必须由用户在当前任务中明确说“开始实施”“开始实现”“开始执行”“直接做”“继续做完”或“按文档实现”，且当前任务已有执行计划、任务完成条件、任务停止 / 结束条件、最大推进边界和验证点，才允许从实施文档切入正式编码。实施规划阶段默认采用只读计划模式：禁止写代码、禁止边计划边试做，只允许读仓库、定依赖、列风险、拆任务、写实施文档。新项目、项目初期或多来源对象存在多份需求 / 实施文档时，必须先在 `doc/3-实施/` 维护“需求与实施计划全量顺序实施方案”，把需求主文档、验收标准、实施总览、实施周期和周期内最小任务按总顺序串起来，再进入单来源对象实施总览。计划正文开头必须先写“当前计划最终方案的简要说明”，用 1-3 句先交代推荐方案、主落点和为什么这么做；随后再写 agent 对当前问题的理解，至少交代问题 / 目标、本轮范围、非范围、当前优先闭环和关键假设 / 待确认点，再进入实施周期与最小任务拆分。实施周期是项目第一期、第二期、第三期等大进度单位和顺序边界，必须写清周期顺序、期次定位、进入条件、收口条件和周期内最小任务顺序；真正执行单元是当前周期内的最小任务，并优先按“依赖图 + 垂直切片”组织，避免按前端 / 后端 / 数据库水平分层堆计划。单任务尽量单次专注完成，默认控制在约 5 个文件以内；明显超过则继续拆分。凡是代码生成、修改或重构类任务，都必须显式计划真实测试，写清入口、环境、样本 / 数据来源和通过标准，`build`、`lint`、静态检查不算真实测试；只有纯文档、纯注释、纯排版、纯静态资源改名 / 搬运或不会影响运行结果的场景才允许免测；若计划涉及代码生成、修改或重构，“现状与落点”必须给出代码落点目录树，不能只写文件名或普通条目。若用户在当前轮显式提出“怎么做 / 先给计划 / 先出方案 / 先列步骤 / 这个怎么改”这类计划型问题，也必须先命中实施规划规则；若前置条件未齐，则输出受限计划 / 阻断计划，而不是不触发。若运行环境要求用 `<proposed_plan>` 等专用计划包裹输出，包裹层只负责渲染 / 协议，不能覆盖项目内计划结构；正文仍必须遵守 `implementation-planning-rules` 与模板字段，并在输出前执行 `implementation-planning-rules/references/plan-output-gate.md` 的字段矩阵。Plan Mode 计划正文若以 `Summary`、`Key Changes`、`Public Interfaces`、`Test Plan`、`Assumptions` 等通用工程计划小节作为主结构，或缺少当前计划最终方案简要说明、agent 理解、范围、非范围、当前优先闭环、关键假设、实施周期、阶段计划、最小任务、真实测试、完成条件、停止 / 结束条件、最大推进边界等核心字段，直接判定为无效计划，必须按模板重写，不得解释为简化版计划。受限计划不得作为实施授权；用户即使明确采纳，agent 也只能先补齐缺失前置条件并将其升级为正式执行计划，未升级前禁止进入编码、改码、重构、测试实施或其他执行动作。若用户给出开工类指令但没有计划或任务停止 / 结束条件，必须先补本轮受限计划并停在计划收口处，不得直接实现或进入长文本无限执行。开工后按 `autonomous-execution-rules` 默认遵循“当前实施周期内最小任务A实现 -> 最小任务A真实测试 -> 最小任务A审查 -> 最小任务A验收 -> 最小任务B…… -> 当前实施周期收口 -> 下一实施周期”的自动串行闭环；每个最小任务都必须先完成自己的真实测试、审查、验收，才允许进入下一个任务；禁止先连续实现多个最小任务后统一测试、统一审查或统一验收。
- 来源: `autonomous-execution-rules`、`implementation-planning-rules`、`team-development-rules/references/routing-rules.md`
- 适用范围: 实施域、测试域、审查域、验收域
- 更新时间: 2026-07-05
- 状态: 启用

### 代码生成风格入口链路
- 别名: 代码风格契约, 生成代码前风格总控, PROJECT_STYLE 应用入口
- 类型: 流程规则
- 定义: 新增、修改或重构任意代码、脚本、测试支撑代码或配置型代码前，必须先由 `code-generation-style-rules` 读取用户本轮要求、目标文件 / 同目录样例、根目录 `PROJECT_STYLE.md` 和已命中的编码类 skill，形成本轮代码风格契约；后续实现必须按契约落地。`project-style-rules` 继续只维护 `PROJECT_STYLE.md` 长期风格记忆，`code-style-consistency-rules` 基于本轮契约检查局部一致性。
- 来源: 对话确认、`code-generation-style-rules/SKILL.md`、`project-agents-bootstrap/SKILL.md`
- 适用范围: 编码基线域、仓库级规则自举、代码生成与修改
- 更新时间: 2026-07-05
- 状态: 启用

### 简单检查职责就地表达规则
- 别名: 小函数内联, 避免过度职责拆分, 简单检查不强拆函数
- 类型: 代码可读性规则
- 定义: 职责清晰不等于每个职责都拆成独立函数。极短的局部检查、判空、匹配器取用、scope/flag 选择等逻辑，如果只有一个调用点、无副作用、无复杂分支、无独立测试价值，优先留在当前函数内，并用步骤注释或局部注释补清业务含义；只有复用、稳定业务术语、复杂规则、副作用或独立测试需求成立时才拆函数。
- 来源: 对话确认、`code-readability-rules/SKILL.md`、`code-readability-rules/references/function-structure-rules.md`
- 适用范围: 函数拆分、局部检查、guard 分支、简单匹配逻辑、注释补充
- 更新时间: 2026-07-09
- 状态: 启用

### 工具落点分流规则
- 别名: util 归位, common/util 归位, util 与 common/util 区分
- 类型: 包结构/复用规则
- 定义: `util` 仅存放与当前项目无关、脱离项目上下文仍成立的通用工具；`common/util` 仅存放可复用但依赖当前项目文件、路径、配置、命名约定或目录结构的工具。引用项目文件或项目约定的复用工具不要放进独立 `util`。
- 来源: 对话确认、`common-util-rules`、`package-structure-rules`
- 适用范围: 通用工具、公共函数、复用代码、包归位
- 更新时间: 2026-07-08
- 状态: 启用

### 通用结束信号
- 别名: 结束即停, 不扩散下一步, 停止建议, 三类合法后续
- 类型: 流程规则
- 定义: 当用户明确表达“结束”“停止”“到此为止”“不要继续”“不要下一步建议”“不要扩散”等结束指令，或不存在三类合法后续时，该指令对 Codex、Claude Code、浏览器 agent、子 agent 或其他长文本 agent 通用；agent 必须停止自动继续、工具执行和扩散性后续建议，只保留必要的最小收口结论。最终收口只允许三类合法后续：原执行计划内未完成必需项、阻断项、用户显式要求的建议/backlog。可选优化、额外整理、未来迭代、体验提升、文档再润色等内容，若不属于原计划必需项，不得作为默认后续内容输出。无下一步时强制不输出“下一步状态”“下一步建议”“等待用户新指令”“无需继续动作”等占位文案，避免循环 loop 会话误触发。Codex goal 仅是运行时状态收口机制的一种特例；若当前环境存在 goal / plan / task 等显式状态机制，且已满足完成或阻断条件，必须按真实机制完成状态收口。
- 来源: `autonomous-execution-rules`、`reasoning-summary-structure-rules`、`skill-compliance-gate-rules`、`AGENTS.md`
- 适用范围: 多 agent 收口、最终总结、连续执行、skill 合规闸门
- 更新时间: 2026-06-29
- 状态: 启用

### 普通 Markdown 输出规则
- 别名: text 代码块禁用, 自然语言不用代码围栏, 输出格式规则
- 类型: 输出规则
- 定义: 普通说明、方案、流程、总结、审查报告、线程拆分和状态回报必须使用普通 Markdown 段落、列表、表格或引用块；不得用 ` ```text `、无语言代码围栏、缩进代码块或 HTML 包裹整段自然语言输出。代码围栏只用于真实代码、命令、配置片段、日志片段、JSON/YAML 等需要等宽保真的内容。该规则由 `reasoning-summary-structure-rules` 负责收口检查，并由 `project-agents-bootstrap` 同步进 `AGENTS.md` / `CLAUDE.md` 的“输出格式规则”章节。
- 来源: 用户截图确认、`reasoning-summary-structure-rules`、`project-agents-bootstrap`、`PROJECT_STYLE.md`
- 适用范围: 最终回复、中间进度、审查报告、线程拆分、仓库规则文件模板
- 更新时间: 2026-06-30
- 状态: 启用

### Windows 执行路由与 PowerShell 保底
- 别名: Windows shell 主路由, PowerShell 专项兜底, windows-wsl-execution-rules 合并 powershell-windows
- 类型: 流程规则
- 定义: Windows 环境下的本地默认口径继续是“普通仓库命令优先 Git Bash / bash，执行类命令优先 `wsl.exe --cd` 进入 WSL，PowerShell 只用于 `.ps1`、Windows 专用 cmdlet、profile / 编码初始化或用户明确要求”；同时 `windows-wsl-execution-rules` 已吸收热门社区 skill `powershell-windows` 的高价值保底规则，进入 PowerShell 专项场景后必须额外遵守逻辑运算括号、ASCII-only、null check、`Join-Path`、`ConvertTo-Json -Depth` 和 UTF-8 重定向防护。
- 来源: 本轮对话确认、`windows-wsl-execution-rules/SKILL.md`、社区 skill `powershell-windows`
- 适用范围: Windows 执行环境、仓库命令路由、PowerShell 专项场景
- 更新时间: 2026-07-10
- 状态: 启用

### 并行执行闭环规则
- 别名: 并行识别必须真启动, 规划器加执行器, 子线程启动证据
- 类型: 流程规则
- 定义: `parallel-task-dispatch-rules` 只负责并行判定与线程拆分，不再允许单独停留在“识别出可并行”。本仓库默认处于 subagent 完全授权模式：用户已明确允许 agent 在任务可切分、写集不冲突、风险可控且环境支持时自动启动 subagent / delegation / parallel agent work；该项目级 standing authorization 视为满足工具显式授权条件。当并行判定为可并行或条件并行且无任务阻断时，必须继续联动 `subagent-dispatch-rules` 做真实启动判定并发起真实子线程 / 子代理执行，同时核对计划线程数、实际启动线程数与关闭/回收线程数。仅输出线程分配文案、`并行技能` 列表或口头启动说明，不视为真正并行已生效。并行识别不以固定 skill 映射为白名单；项目分析、找 Bug、需求完善侦察、资料/日志/调用链证据收集等任务，只要能拆成独立问题、独立证据来源、独立目录、独立模块或独立文件集，主 agent 必须优先形成只读 sidecar 子任务计划并在授权成立时真实委派。单一根因、需求边界、接口契约、schema 或架构方向等最终裁决仍由主 agent 串行负责。
- 来源: `parallel-task-dispatch-rules`、`parallel-task-dispatch-rules/references/task-classification.md`、`subagent-dispatch-rules`、`subagent-dispatch-rules/references/delegation-decision-matrix.md`
- 适用范围: 并行开发、并发审查、项目分析、需求侦察、Bug 分诊、sidecar 子任务分发
- 更新时间: 2026-06-30
- 状态: 启用

### 子 agent 启动计划脚本
- 别名: generate_subagent_plan, 批量委派计划, 中文任务名子 agent
- 类型: 工具规则
- 定义: `subagent-dispatch-rules` 在批量委派前优先运行 `subagent-dispatch-rules/scripts/generate_subagent_plan.py` 生成结构化启动计划。脚本只负责输出计划 JSON，不直接调用平台工具；真实启动仍由主 agent 读取计划后调用 subagent / multi-agent / thread 工具。脚本生成的 `agent_name` / `logical_agent_name` 默认使用“任务简要中文 + 线程标识”，用于主 agent 侧的中文逻辑命名与计划线程数核对；平台 UI 实际昵称仍以启动工具返回值为准。
- 来源: `subagent-dispatch-rules`
- 适用范围: 批量子任务委派、并行线程规划
- 更新时间: 2026-06-29
- 状态: 启用

### 子 agent 生命周期回收
- 别名: close_agent 回收, 子代理关闭, 已完成子线程释放
- 类型: 流程规则
- 定义: subagent 启动成功后，即使执行已完成，仍会继续占用并发槽位；主 agent 在结果回收并完成整合后，必须继续调用真实 `close_agent` / 等价关闭工具完成释放。`subagent-dispatch-rules` 的通过标准需要同时核对计划线程数、实际启动线程数与实际关闭线程数。
- 来源: `subagent-dispatch-rules`
- 适用范围: 所有真实子 agent / 并行代理执行场景
- 更新时间: 2026-06-29
- 状态: 启用

### 审查体系收口
- 别名: 审查链路
- 类型: 流程规则
- 定义: 默认审查链收口为 `implementation-review-rules`、`project-change-review-rules`、`artifact-delivery-gate-rules`、`skill-compliance-gate-rules`；实现自审与当前改动总审查在收口前必须真实落盘到 `doc/6-审查/`，不再允许仅在最终回复中口头保留通过结论。
- 来源: `README.md`、`项目设计.md`
- 适用范围: 审查域
- 更新时间: 2026-06-27
- 状态: 启用

### Git 提交基础审查与验收闸门
- 别名: 提交前审查检查, Git 基础验收, 提交不生成审查验收文档
- 类型: 流程规则
- 定义: 执行 `git commit` 前，必须直接对当前 staged 改动完成基础审查与基础验收：格式、注释、安全性、并发安全性、系统崩溃风险、边界条件和测试/功能验证适用性均须通过或明确“不适用 + 原因”。结论只写入 Git 提交证据；禁止仅因提交自动生成或要求 `doc/6-审查/`、`doc/7-验收/` 文档。只有用户显式发起总审查或正式最终验收，或非 Git 场景进入最终放行时，才执行对应 skill 的文档归档。
- 来源: 当前对话确认、`git-collaboration-rules/SKILL.md`、`project-change-review-rules/SKILL.md`、`final-acceptance-rules/SKILL.md`
- 适用范围: 提交流程、审查域
- 更新时间: 2026-07-13
- 状态: 启用

### README 改动日志时间戳格式
- 别名: README 日志格式, 提交日志时间戳
- 类型: 格式规则
- 定义: 根目录 `README.md` 改动日志每条记录格式固定为 `yyyy-MM-dd HH:mm:ss 提交标题`，时间戳使用当前北京时间；始终追加到改动日志末尾，不按时间回插旧位置。`pre_commit_gate.sh` 校验时剥除时间戳前缀后再与提交标题比较。
- 来源: `git-collaboration-rules/SKILL.md`、`branch-and-commit.md`
- 适用范围: 提交流程、README 维护
- 更新时间: 2026-07-01
- 状态: 启用

### Git 提交域隔离规则
- 别名: 提交域隔离, 需求实施测试Bug审查验收单独提交, 代码实现单独提交
- 类型: 流程规则
- 定义: `提交git` 允许拆成多次提交清空工作区，但每个 commit 默认只承载一个提交域。`doc/2-需求/`、`doc/3-实施/`、`doc/4-bugs/`、`doc/5-tests/`、`doc/6-审查/`、`doc/7-验收/` 六类流程产物各自单独提交；测试文件（至少 `doc/5-tests/**`、`*_test.*`、`*.spec.*`、`*.test.*`）归入测试提交；代码实现 / 运行配置单独提交，不与上述流程文档域或测试文件混提。根目录 `README.md` 改动日志可以跟随对应 commit 一起更新，但不单独构成提交域。
- 来源: 对话确认、`git-collaboration-rules/SKILL.md`、`git-collaboration-rules/scripts/pre_commit_gate.sh`
- 适用范围: 提交流程、需求域、实施域、Bug 域、测试域、审查域、验收域
- 更新时间: 2026-07-08
- 状态: 启用

### 文档落盘闸门
- 别名: 归档闸门, 收口前落盘检查
- 类型: 流程规则
- 定义: 需求、实施、验收、Bug、测试、审查任务在最终收口前必须联动 `artifact-delivery-gate-rules`，核对主文档、正文内嵌 Mermaid 图示（需求域、Bug 域统一不另建 SVG 等配套图文件）、README、需求与实施计划全量顺序实施方案、实施总览/实施周期、验收文档和证据路径是否已经真实落盘到 `doc/2-需求/`、`doc/3-实施/`、`doc/4-bugs/`、`doc/5-tests/`、`doc/6-审查/`、`doc/7-验收/`；实施域还必须核对新项目 / 多来源对象总顺序、周期顺序、期次定位、周期内最小任务顺序和已执行最小任务的实现 / 真实测试 / 审查 / 验收状态，未落盘或缺闭环状态不得判定任务完成。
- 来源: `artifact-delivery-gate-rules`、`README.md`
- 适用范围: 需求域、实施域、验收域、Bug 域、测试域、审查域
- 更新时间: 2026-07-05
- 状态: 启用

### 需求与实施文档极致完整性契约
- 别名: 零决策文档交接, 极致完整性, 普通模型执行契约, 文档质量 profile
- 类型: 文档质量规则
- 定义: 需求、验收标准、实施总览、实施周期和最小任务文档采用“结构完整、条件字段显式、决策冻结、图文一致、双向追踪、机器校验”的共同契约。所有条件字段必须填写，或使用 `N/A + 原因 + 证据`；普通模型不得自行补业务、技术、测试、回滚或停止决策。稳定追踪链固定为 `SRC -> DEC -> REQ/RULE -> AC -> CYCLE -> TASK -> 文件/符号 -> TEST -> EVIDENCE`。需求按复杂度 L1-L4 展开；L2 及以上按语义强制流程图、时序图及必要状态/数据/依赖图；实施总览、周期和任务卡分别承载整体决策、周期顺序和零决策执行动作。
- 来源: `requirement-intake-rules/references/extreme-completeness-standard.md`、`implementation-planning-rules/references/implementation-overview-template.md`、`implementation-planning-rules/references/implementation-cycle-template.md`、`implementation-planning-rules/references/minimum-task-execution-contract.md`、`artifact-delivery-gate-rules/references/document-handoff-contract.md`
- 适用范围: 需求域、验收域、实施域、交付闸门
- 更新时间: 2026-07-12
- 状态: 启用

### Windows PowerShell 环境准备与工具边界
- 别名: windows-powershell-environment-rules, PowerShell 7 默认入口, Windows CLI 工具清单
- 类型: 环境规则
- 定义: Windows 专项入口优先使用已验证的 PowerShell 7.6.3；Windows Terminal 用户级 `defaultProfile` 指向唯一受管 PowerShell 7 profile。PowerShell 5.1 保留为旧脚本兼容回退，不替换 `powershell.exe`，不修改 VS Code 默认终端或全局 Git 配置。Windows 侧通过固定 manifest 幂等准备并验证 `rg`、`fd`、`fzf`、`jq`、`yq`、`bat`、`eza`、`delta`、`just`、`sd`、`zoxide`、`wget2`、`aria2c`、`gsudo` 与 Git；7-Zip、tlrc 在当前非管理员环境下属于权限阻断。Windows 工具不等于 WSL 工具，WSL 进入项目后仍必须用 `command -v` 验证原生路径。
- 来源: `windows-powershell-environment-rules/SKILL.md`、`references/tool-manifest.yaml`、`references/safety-and-validation.md`、2026-07-12 真实 Audit/Apply/Rollback 与 WSL 路径复核
- 适用范围: Windows PowerShell 专项入口、Windows Terminal 用户设置、Windows CLI 工具安装与 WSL 隔离
- 更新时间: 2026-07-12
- 状态: 启用

### Markdown 图片资产闭环
- 别名: CHG-DOC-IMG-001, document_image_assets, Markdown 图片根目录
- 类型: 资产存储与交付门禁规则
- 定义: 所有需求、验收、实施和通用 Markdown 位图统一写入项目根 `doc/data/images/`；`doc/data/` 仅为文档数据容器，不提供直接图片入口。引用从当前 Markdown 位置计算 `/` 分隔相对路径，alt 必须非空且包含 `IMG-*`；图片决策为“需要”或 `N/A + 原因 + 证据`。真实生成必须经 `imagegen`，文件名遵循 `<document_stem>.<asset-slug>-v<number>.<ext>`；validator 校验路径、扩展名与签名、命名、九字段资产清单（用途、来源、版本、关联 ID、引用章节、敏感状态和版权状态）、决策、孤儿及 `doc/data/` 错位图片；Mermaid 仍负责流程、时序、状态、依赖和数据关系，图片不能替代 Mermaid。
- 来源: `artifact-storage-rules/references/path-map.yaml`、`artifact-delivery-gate-rules/references/document-quality-profiles.yaml`、`REQ-DOC-20260712-033322`
- 适用范围: 需求域、实施域、验收域、交付门禁
- 更新时间: 2026-07-12
- 状态: 启用

### 中间链路也受落盘闸门约束
- 别名: 中段归档闸门, 非主入口也要落盘
- 类型: 流程规则
- 定义: 文档落盘闸门不只约束需求入口、Bug 入口、测试总结和总审查入口；需求补齐/边界/拆分/变更、Bug 复现/根因/运行时诊断/修复建议/回归风险、测试策略/命名/程序/目录/散落资产治理等中间链路，只要已经形成应持久化结论，最终收口前同样必须联动 `artifact-delivery-gate-rules`。
- 来源: 本轮 skill 修订、`README.md`
- 适用范围: 需求域、Bug 域、测试域、审查域
- 更新时间: 2026-06-27
- 状态: 启用

### 提交级审查正式归档位置
- 别名: commit review 归档口径, 提交级专项审查出口
- 类型: 审查规则
- 定义: `code-review-automation-rules` 的正式长期输出已统一收口到 `doc/6-审查/`，文件名遵循 `artifact-storage-rules` 中央模板；不再写入项目根目录固定文件名 `code_review_result.md` 一类平行入口。
- 来源: `code-review-automation-rules`、`artifact-storage-rules/references/path-map.yaml`
- 适用范围: 审查域
- 更新时间: 2026-06-27
- 状态: 启用

### 记忆与风格更新方式
- 别名: 长期规则回写方式
- 类型: 维护规则
- 定义: 当用户后续调整某个指标、命名、目录口径或风格偏好时，必须更新原有记忆或风格词条，不新增同义冲突条目，也不保留并行旧口径。
- 来源: 对话确认、`project-memory-rules`、`project-style-rules`
- 适用范围: 长期文档维护
- 更新时间: 2026-06-27
- 状态: 启用

### Imagegen 错误案例持续演进
- 别名: imagegen, gpt-image-2 错误案例库, 生图失败经验回写
- 类型: Skill 维护规则
- 定义: 权威 `imagegen` skill 使用 `references/error-casebook.md` 保存已复现、已解决、已验证且已脱敏的生图错误；每次失败先分类并查找已有案例，解决后在获得 skill 维护授权时去重回写，未验证错误不得进入可执行案例，敏感凭据和用户私有内容不得落盘。
- 来源: `imagegen/SKILL.md`、`imagegen/references/error-casebook.md`、本轮验证结果
- 适用范围: gpt-image-2 CLI fallback、参数校验、透明背景、依赖/鉴权、限流与瞬态网络错误
- 更新时间: 2026-07-12
- 状态: 启用

### 执行失败持续学习与主动预防
- 别名: execution-failure-learning-rules, 执行失败案例演进, prevent recover learn
- 类型: Skill 维护规则
- 定义: 高风险工具调用前进入 `prevent` 预检，非预期失败进入 `recover` 分类、查库和同输入同成功标准复验，验证通过后才进入 `learn`。案例正文只归属于唯一 owner Skill；无维护授权保持 `candidate`，冲突标记 `conflicted`，业务 Bug、Skill 缺口和跨项目知识分别回流 `bug-*`、`skill-evolution-rules` 与 `obsidian-knowledge-flow`。
- 来源: `execution-failure-learning-rules/SKILL.md`、`references/classification-and-routing.md`、`references/lifecycle-and-gates.md`、本轮前向行为测试
- 适用范围: imagegen、Windows/WSL、浏览器、认证 URL、MCP/插件安装、Obsidian CLI 及后续注册的高风险执行域
- 更新时间: 2026-07-12
- 状态: 启用

### Windows / WSL 执行边界
- 别名: Windows 普通命令优先 bash, Git Bash 优先, 执行类动作才进 WSL
- 类型: 环境规则
- 定义: 当项目代码位于 WSL 文件系统内且 agent 运行在 Windows 时，搜索、读写文件、规则检查、普通 git 盘点等非执行动作默认优先使用 Git Bash / bash；PowerShell 不作为普通仓库命令入口，只在 `.ps1`、Windows 专用 cmdlet、PowerShell profile / 编码初始化或用户明确要求时使用。只有编译、运行、启动程序、测试、调试，以及会真实启动运行时的依赖安装，才通过 `wsl.exe --cd /home/<user>/<project> <command>` 进入 WSL。纯 Windows 项目，或当前任务本身不需要启动/执行程序时，不应误触发 WSL 执行规则。（另见 [[项目内文件引用路径]]：面向用户的文件路径格式判定与这里的“agent 运行位置”无关，即使 agent 直接跑在 WSL 内也要按用户查看环境转换路径，不要把这两条规则的适用条件混在一起读。）
- 来源: 用户本轮确认、`windows-wsl-execution-rules/SKILL.md`、`windows-encoding-rules/SKILL.md`、`AGENTS.md`
- 适用范围: Windows + WSL 协作开发、仓库级执行规则、命令模板
- 更新时间: 2026-07-06
- 状态: 启用

### 项目内文件引用路径
- 别名: 用户可访问路径, WSL 文件引用, UNC 路径展示
- 类型: 输出规则
- 定义: agent 回复中凡引用项目内文件，都必须使用用户当前客户端可打开的项目访问路径，而不是机械沿用执行环境路径。项目在 Windows 本地盘时使用 Windows 本地路径；项目在 WSL 文件系统且用户通过 Windows / Codex Desktop / Claude Desktop 访问时，项目内文件引用统一使用 `\\wsl.localhost\<distro>\home\<user>\<project>\...`；`/home/<user>/<project>` 只用于 WSL 内命令、`wsl.exe --cd` 参数、WSL shell 日志或必须保留原文的执行上下文。**判定依据只有“用户查看环境”，与 agent 自身运行在 WSL 还是 Windows 无关**：agent 直接跑在 WSL 内、执行不需要 `wsl.exe` 包裹时，这条规则依然生效，不能因为“自己就在 WSL 里”而顺手输出 `/home/...`。
- 来源: 用户确认、`windows-wsl-execution-rules/references/path-mapping.md`
- 适用范围: 最终回复、中间进度、审查报告、证据路径、截图说明、Markdown 链接和普通文本文件路径
- 更新时间: 2026-07-06
- 状态: 启用

### WSL 工具 PATH interop 误用排查
- 别名: rg permission denied, Windows 版工具误用, appendWindowsPath
- 类型: 环境规则
- 定义: WSL 默认在 `/etc/wsl.conf` 的 `[interop]` 段开启 `appendWindowsPath=true`，会把 Windows 的 `PATH` 追加到 WSL 的 `$PATH` 末尾；WSL 内未原生安装的命令行工具（如 `rg`）会 fallthrough 到 `/mnt/c/...` 下的 Windows 版 `.exe`，执行时可能因 DrvFs 挂载权限、只读标记或安全软件拦截报 `permission denied`。排查用 `command -v <tool>` 确认路径是否落在 `/mnt/` 下；修复优先在 WSL 内原生装该工具（如 `sudo apt install ripgrep`），不默认修改 `/etc/wsl.conf`。建议在新会话第一次于某 WSL 项目执行命令时，顺手做一次 `command -v` 一次性自检，提前发现缺失的原生包，而不是等报错再排查。
- 来源: 对话确认、`windows-wsl-execution-rules/references/tool-path-interop.md`
- 适用范围: WSL 执行环境、命令行工具排查
- 更新时间: 2026-07-06
- 状态: 启用

### 文件写入统一 UTF-8
- 别名: 跨平台 UTF-8 写入, 禁止 GBK/ANSI 落盘, 文件编码规则
- 类型: 环境规则
- 定义: 仓库所有代码、文档、配置、脚本、测试资产和生成类文本文件，新增或修改时默认使用 UTF-8 编码；Windows、Linux、WSL、容器和远程服务器上都必须保持同一口径，禁止用 GBK、ANSI、系统默认编码、编辑器默认编码或 shell 默认编码落盘。命令行写文件必须显式指定 UTF-8，写后回读关键文件并检查 `git diff`，确认中文未乱码、编码未漂移、换行未被意外批量转换。
- 来源: 用户本轮确认、`AGENTS.md`、`windows-encoding-rules/SKILL.md`、`windows-wsl-execution-rules/SKILL.md`
- 适用范围: 全仓库文件写入、规则文件自举、Windows / WSL / Linux 协作开发
- 更新时间: 2026-07-02
- 状态: 启用

### 会话自动重命名规则
- 别名: thread-title-rules, 会话标题自动更新, 任务中文简要
- 类型: 工作台规则
- 定义: 当前 Codex / Claude / agent 会话进入明确需求、Bug、实施、审查、测试、提交、规则更新，或用户提问后已经能稳定归纳出中文任务主题时，且标题为空泛、过时、泛称或不匹配当前任务时，必须自动命中 `thread-title-rules`；goal 创建、goal 恢复、上下文压缩续做、长任务阶段切换或执行阶段主题稳定时，也必须在过程中尽早判定是否改名，不等待最终总结。由 agent 生成 8-24 字中文简要标题，并按平台能力矩阵调用当前环境真实线程重命名工具更新当前会话标题。Codex 环境优先使用真实 `set_thread_title`；若当前工具列表尚未直接暴露 `set_thread_title` 或 `list_threads`，必须先通过 `tool_search` 发现线程工具，再按 `cwd`、最近更新时间和当前任务主题可靠识别当前会话后执行改名；只有完成工具发现后仍无真实工具时才可跳过。Claude Code 仅在存在真实改名工具时执行；Claude Desktop 默认视为无真实自动改名工具，必须显式跳过并说明原因。标题已准确、用户明确禁止或只是最小任务内部小步骤推进时跳过；禁止用正文伪造工具调用或猜测结果宣称已改名。
- 来源: 用户本轮确认、`thread-title-rules/SKILL.md`、`project-agents-bootstrap/SKILL.md`
- 适用范围: 会话管理、任务检索、总控层自动触发、仓库规则自举
- 更新时间: 2026-07-05
- 状态: 启用

### Obsidian 知识流选择性默认触发链
- 别名: obsidian-knowledge-flow, Obsidian 知识流, 选择性默认触发, 知识库检索沉淀
- 类型: 流程规则
- 定义: 项目启动先按“父目录平台规则 -> `PROJECT_CURRENT.md` -> `PROJECT_MEMORY.md`”读取项目本地四件套；`PROJECT_CURRENT.md` 覆盖维护当前状态且不超过 51,200 字节，`PROJECT_MEMORY.md` 只承载稳定规则与关键决策，`PROJECT_HISTORY.md` 只追加且普通启动不读。Obsidian 仍固定使用 `D:\obsidian_data` 及其 `知识库/` 工作区，仅当问题依赖跨项目历史、vault 知识或既有笔记时判定为 `检索` 并通过 CLI 检索 / 读取；仅当收口形成可复用知识时判定为 `沉淀` 并先通过 CLI 检索已有承接笔记。执行失败案例统一落到 `知识库/20-Knowledge/execution-failure-cases/<owner>/`，保留脱敏正反例、验证证据和追加式状态事件；只有 active 且 scope 精确匹配时自动复用。普通任务记录 `不适用`，CLI 或 vault 不可用时记录 `阻断`，不得直接文件读写 vault 作为 fallback；项目本地 Markdown 与 vault 链路不得混用。
- 来源: `AGENTS.md`、`CLAUDE.md`、`skill-hit-check-rules/SKILL.md`、`obsidian-knowledge-flow/SKILL.md`、`编码skill.md`
- 适用范围: 记忆域、命中检查、阶段收口、最终总结、Obsidian vault 知识检索与沉淀
- 更新时间: 2026-07-14
- 状态: 启用

### Obsidian Windows/WSL bridge 固定执行边界
- 别名: obsidian_cli_bridge, Windows/WSL CLI bridge, bridge-only vault
- 类型: 跨宿主执行规则
- 定义: Windows 与 WSL 的 Obsidian 检索、创建、追加、读取和 INDEX 更新统一经 `obsidian-knowledge-flow/scripts/obsidian_cli_bridge.py`，最终由 Windows 官方 CLI 操作唯一 vault 根 `D:\obsidian_data`；`知识库/` 只是 vault 内路径前缀，selector 必须按注册根动态唯一解析。WSL 仅通过 PowerShell interop，不安装原生 Linux CLI，不使用 vault 文件系统 fallback；写入必须 `verified=true` readback，应用恢复最多隐藏启动一次并有限重试。
- 来源: `obsidian-knowledge-flow/SKILL.md`、`cli-operations.md`、CYCLE-OBS-01/02 实机证据
- 适用范围: Windows/WSL 知识流、bridge transport、长正文分块与读回验证
- 更新时间: 2026-07-13
- 状态: 启用

### 项目四件套记忆闭环
- 别名: PROJECT_CURRENT, PROJECT_MEMORY, PROJECT_HISTORY, 项目本地记忆四件套
- 类型: 项目上下文规则
- 定义: 父目录 `AGENTS.md` / `CLAUDE.md` 只保存跨项目通用规则；项目根目录 `PROJECT_CURRENT.md` 保存当前任务交接信息并覆盖维护，`PROJECT_MEMORY.md` 保存稳定项目规则、关键决策和少量长期事实，`PROJECT_HISTORY.md` 只追加关键历史事件。新项目、新任务、新会话或上下文压缩恢复时，固定先读取父目录当前平台规则，再读取 current 和 memory；history 只在历史追问、状态不足或真实卡点时窄读。项目本地文件使用标准工具，Obsidian vault 仍只通过 CLI 选择性检索和沉淀。
- 来源: 用户本轮确认、`obsidian-knowledge-flow`、`project-memory-rules`、`project-agents-bootstrap`
- 适用范围: 项目启动、上下文交接、记忆更新、Obsidian 边界
- 更新时间: 2026-07-11
- 状态: 启用

### Git 协作联动 Obsidian 沉淀
- 别名: 提交前知识捕获, Git 收口沉淀, commit 联动 Obsidian
- 类型: 流程规则
- 定义: 当本仓库出现提交、推送、PR 收口或交付说明准备，且本轮形成可复用事实、决策、流程、定义、偏好、来源或调试经验时，优先命中 `obsidian-knowledge-flow` 做 `Obsidian:沉淀` 判定；沉淀只负责知识捕获，不构成 `git commit` / `git push` 授权。
- 来源: 对话确认、`git-collaboration-rules/SKILL.md`、`obsidian-knowledge-flow/SKILL.md`
- 适用范围: 提交流程、交付收口、Obsidian 记忆沉淀
- 更新时间: 2026-07-08
- 状态: 启用

### 本地连接调试测试红线
- 别名: 只连 local, 禁连 test/prod, 本地服务联调, local 数据库
- 类型: 环境安全规则
- 定义: 需求侦察、Bug 复现 / 定位 / 运行时调试、功能验证、回归测试、上线接口测试、浏览器联调、启动前后端服务或执行测试脚本时，所有数据库、缓存、消息队列、HTTP/RPC 上游、前端 / 后端服务连接都只能使用 local 本地环境。`test`、`prod`、`production`、`staging`、`pre`、`release` 等非 local 环境一律禁止连接；即使用户提供临时连接信息或授权，agent 也不得直接连接，只能记录为环境阻断并要求改用 local。本地配置缺失、local 数据不足或本地服务未启动时，只能补齐 local 环境或阻断，不得回退到 test / prod。
- 来源: 用户本轮确认、`AGENTS.md`、`test-strategy-rules/SKILL.md`、`project-agents-bootstrap/SKILL.md`、`project-agents-bootstrap/scripts/bootstrap_agents.sh`
- 适用范围: 需求域、Bug 域、测试域、运行时调试、浏览器联调、Windows / WSL 执行命令
- 更新时间: 2026-07-01
- 状态: 启用

### URL 认证浏览器默认路由
- 别名: authenticated-url-routing-rules, 已登录 Chrome 路由, URL 默认 Chrome Plugin
- 类型: 浏览器路由规则
- 定义: 当用户提供任意 URL、链接或网页地址，并要求打开、读取、分析、总结、截图、提取内容、排查页面、查看文档、理解网页、检查资料、访问在线文档或处理已在浏览器登录过的页面时，默认优先触发 `authenticated-url-routing-rules`，并优先使用 `chrome:control-chrome` 接管用户已登录的真实 Chrome profile，复用登录态、扩展、权限和已打开标签页。依赖真实 Chrome profile 的页面在 Chrome Plugin 不可用时停在连接/授权阻断，不得用 `agent-browser` 或其他浏览器绕过；明确为公开或 local 且不依赖用户 profile 的页面，才按统一路由选择 Chrome DevTools MCP 或 `agent-browser`。遇到登录页、权限页、验证码或人机验证时，不得用 `web`、搜索引擎、第三方转载或无登录态浏览器绕过权限。若 Chrome 已成功认领用户标签页但浏览器安全策略拒绝读取正文，必须停止绕过尝试，只报告 URL / 标题 / 认领状态和策略阻断事实，并将标签页保留为 handoff。后续执行中遇到并确认解决的 URL 认证、真实 Chrome 接管、登录态复用、权限页、正文读取策略或 handoff 问题，必须按“触发条件 -> 允许动作 -> 禁止动作 -> 收口证据”回写本 skill。
- 来源: 用户确认、`authenticated-url-routing-rules/SKILL.md`
- 适用范围: URL 分析、在线文档读取、浏览器权限页面、企业系统资料访问
- 更新时间: 2026-07-02
- 状态: 启用

## 术语表

### doc 顶层混合命名
- 别名: 中文语义优先命名
- 类型: 术语
- 定义: `doc/` 根目录保留英文，活动子目录采用“编号顺序 + 中文语义优先 + 工程通用域保留英文”的混合方案：`1-架构`、`2-需求`、`3-实施`、`4-bugs`、`5-tests`、`6-审查`、`7-验收`。
- 来源: 对话确认、`artifact-storage-rules`
- 适用范围: 文档目录命名
- 更新时间: 2026-06-28
- 状态: 启用

## 业务约束

### 旧目录处理规则
- 别名: 不保留兼容层
- 类型: 迁移约束
- 定义: 当目录迁移完成且用户未要求保留兼容入口时，应删除旧目录、旧占位文件和旧跳转文档，不保留并行旧包或兼容壳。
- 来源: 对话确认、`artifact-storage-rules`
- 适用范围: 目录迁移与收口
- 更新时间: 2026-06-27
- 状态: 启用

## 变更记录

- 2026-06-27：初始化根目录长期记忆文档，补齐 doc 顶层目录口径、审查链收口和长期规则回写约束。
- 2026-06-27：新增需求主动侦察链路，明确老板式 idea 先由 agent 查项目、数据、代码、上下游和补充路径，再形成需求设计并回写可复用侦察线索。
- 2026-06-27：明确 `requirement-discovery-rules` 是需求域第一入口，现有需求 skill 暂不合并为大 skill，改为通过路由 reference 收敛职责重叠。
- 2026-06-27：新增统一文档落盘闸门，明确需求、Bug、测试、审查收口前必须先核对正式文档已真实落盘；同时取消审查域“轻量通过可不落盘”的旧口径。
- 2026-06-27：补充“中间链路也必须过文档落盘闸门”的长期口径，并明确提交级专项审查正式归档到 `doc/6-审查/`，不再写项目根目录固定文件名。
- 2026-06-28：明确“需求/验收标准/实施计划完成不等于自动开工”，必须等用户明确“开始实施/开始执行”后才能进入编码；一旦开工，后续按实施周期自动串行推进实现、测试、审查与验收闭环。
- 2026-06-30：统一实施执行口径为“最小任务闭环优先于实施周期浏览”，并统一主执行链术语为“实现 -> 真实测试 -> 审查 -> 验收”。
- 2026-06-29：将实施执行粒度从“实施周期闭环”细化为“最小任务闭环”；实施周期继续作为文档管理容器，真正执行顺序改为每个最小任务依次完成实现、真实测试、审查、验收后再进入下一个最小任务。
- 2026-06-29：补充长文本执行边界；“开始实施/开始实现/开始执行/直接做/继续做完/按文档实现”等开工词必须有执行计划、任务完成条件、任务停止 / 结束条件和最大推进边界，缺少时先补受限计划并停在计划收口处，不得直接实现。
- 2026-06-29：新增并行执行闭环口径，明确 `parallel-task-dispatch-rules` 判定可并行后必须继续联动 `subagent-dispatch-rules` 做真实启动判定，不能只停留在文本规划；2026-06-30 补充工具授权优先级，真实启动需服从工具元数据。
- 2026-06-29：新增 `generate_subagent_plan.py` 启动计划脚本，明确批量委派先生成计划 JSON，再由主 agent 读取计划并真实启动；子 agent 名称默认使用任务简要中文。
- 2026-06-29：补充子 agent 生命周期口径，明确中文任务名属于主 agent 逻辑名，平台 UI 昵称由启动工具返回；结果收回后仍必须调用 `close_agent` 完成回收。
- 2026-06-30：扩展并行识别口径，明确并行不再依赖固定 skill 映射白名单；主 agent 在项目分析、找 Bug、需求完善侦察、证据收集等任务中必须自主识别可委派的只读 sidecar 子任务并优先尝试真实 subagent 并行。
- 2026-06-30：修正 subagent 自动启动口径，明确自动的是委派判定；真实启动必须服从当前工具元数据和授权策略。若工具要求用户显式授权，先检查当前轮授权与项目级完全授权；仅两者均不存在时，才回退本地执行并记录实际启动数为 0。
- 2026-06-30：根据用户确认启用 subagent 完全授权模式；项目级 standing authorization 视为满足工具显式授权条件，不再因缺少逐次 subagent 指令而回退本地执行。
- 2026-06-28：将正式活动文档目录迁移为 `doc/1-架构/` 到 `doc/7-验收/` 的编号顺序，并新增 `architecture-doc-rules` 承接长期架构专题文档。
- 2026-06-28：固定架构域四个中文主入口，补齐目录树、模块职责、主要业务链路示例，并明确单条业务链路的新增与更新策略。
- 2026-06-28：架构域文件改为固定顺序编号，基础入口占用 `1-4`，业务链路从 `5` 开始按最大编号加一，历史编号不复用、不重排。
- 2026-06-29：新增通用结束信号口径，明确“结束即停”不只适用于 Codex goal，也适用于 Claude Code、浏览器 agent、子 agent 等长文本收口场景。
- 2026-06-29：统一活动文档命名前缀为 `YYYY-MM-DD_HHmmss`，并要求实施、审查、验收等下游文档保留来源对象标识；来源可以是需求或 Bug，避免只看见阶段或审查主题而看不出来源对象。
- 2026-06-29：收紧无下一步收口口径，最终后续内容只允许原执行计划内未完成必需项、阻断项、用户显式要求的建议/backlog，其他可选优化不得默认输出。
- 2026-06-30：新增普通 Markdown 输出规则，明确自然语言结构化输出不得包进 ` ```text ` 等代码围栏，应使用 Markdown 段落、列表、表格或引用块。
- 2026-06-30：收紧需求阶段口径，明确“一次只推进一个关键问题”只允许基于真实缺口，不允许夹带 agent 猜测；需求主文档未真实落盘前，禁止进入实施规划与正式编码。
- 2026-06-30：收紧实施规划口径，明确计划阶段只读、最小任务优先按依赖图与垂直切片组织、单任务默认控制在约 5 个文件以内，且每个最小任务都必须先完成真实测试、审查、验收闭环后再进入下一个任务。
- 2026-07-01：历史上曾收紧为 PowerShell UTF-8 后承接普通命令；2026-07-02 已按新确认口径替换为 Windows 下普通仓库命令优先 Git Bash / bash，PowerShell 仅用于专项场景，执行类动作才进入 WSL。
- 2026-07-01：恢复 README 改动日志时间戳格式为 yyyy-MM-dd HH:mm:ss 提交标题；新增提交前审查闸门，pre_commit_gate.sh 校验 doc/6-审查/ 下审查文档的审查结论、是否允许提交、阻断问题；两个审查 skill 归档时统一写入判定字段。
- 2026-07-01：新增本地连接调试测试红线，明确需求、Bug、测试、运行时调试、启动联调和浏览器验证只能连接 local 本地数据库与本地服务，禁止连接 test / prod / staging 等非 local 环境。
- 2026-07-12：新增 `windows-powershell-environment-rules` 并完成 Windows PowerShell 7.6.3 默认入口、UTF-8 profile、Windows CLI 工具 manifest、Terminal JSONC 幂等/回滚和 WSL 原生工具隔离验证；7z/tlrc 因管理员权限保留阻断。
- 2026-07-01：补充计划型提问入口，明确用户只要显式索要“怎么做/先给计划/先出方案/先列步骤”，就必须先命中实施规划规则；若前置条件未齐，也要输出受限计划 / 阻断计划，而不是表现成计划规则未触发。
- 2026-07-01：补充受限计划授权边界，明确受限计划不得作为实施授权；即使用户明确采纳，也必须先补齐前置条件并升级为正式执行计划，未升级前禁止进入编码、改码、重构、测试实施或其他执行动作。
- 2026-07-03：补充 Plan Mode 包裹口径，明确运行环境若要求用 `<proposed_plan>` 等专用计划包裹输出，包裹层不改变项目内计划格式；计划正文仍必须遵守 `implementation-planning-rules` 与模板结构。
- 2026-07-04：补充 Plan Mode 硬失败口径，明确 `Summary / Key Changes / Public Interfaces / Test Plan / Assumptions` 等通用工程计划壳不能作为实施规划主结构，且计划输出前必须执行 `implementation-planning-rules/references/plan-output-gate.md` 字段矩阵；缺核心字段时必须按模板重写。
- 2026-07-05：明确实施周期是第一期 / 第二期 / 第三期等大进度与顺序边界，执行必须先按周期推进，周期内每个最小任务都完成“实现 -> 真实测试 -> 审查 -> 验收”后才进入下一任务 / 下一周期；文档落盘和最终验收需记录周期收口与最小任务闭环证据。
- 2026-07-13：完成 Obsidian Windows/WSL bridge-only 固定执行边界与 CYCLE-OBS-02 实机收口；唯一 vault 根为 `D:\obsidian_data`，WSL 通过 PowerShell interop，长正文和 append 必须以 CLI readback/hash 证明一致，未使用 vault 文件系统 fallback。
- 2026-07-05：新增新项目 / 多来源对象的“需求与实施计划全量顺序实施方案”口径，要求先用项目级总表串起需求、验收标准、实施总览、实施周期和周期内最小任务，再进入单来源对象执行。
- 2026-07-02：新增文件写入统一 UTF-8 口径，明确代码、文档、配置、脚本、测试资产和生成文本跨 Windows / WSL / Linux 默认 UTF-8，禁止 GBK / ANSI / 默认编码落盘，命令行写入后必须回读并检查 diff。
- 2026-07-02：新增会话自动重命名规则，明确任务主题稳定且标题泛化、过时或不匹配时自动命中 `thread-title-rules`，调用真实线程重命名工具改为 8-24 字中文简要；标题已准确、工具不可用或用户禁止时跳过。
- 2026-07-03：补充会话自动重命名平台能力矩阵，明确 Codex 优先用 `set_thread_title`，Claude Code 仅在存在真实改名工具时执行，Claude Desktop 默认显式跳过，`CLAUDE.md` 不等同于 Desktop 已具备自动改名能力。
- 2026-07-02：新增 URL 认证浏览器默认路由，明确用户提供 URL 时默认优先通过 Chrome Plugin 复用用户真实 Chrome 登录态，避免隔离浏览器或 `web` 丢失权限；补充 Chrome 安全策略拒绝正文读取时只报告阻断事实并 handoff，不做绕过；执行中已确认解决的问题必须继续回灌到 skill。
- 2026-07-12：收敛浏览器工具路由：用户真实 Chrome profile 只由 Chrome Plugin 接管；公开或 local 页面按 Chrome DevTools MCP 与 `agent-browser` 能力路由；`agent-browser` 保留为隔离 session、网络/HAR、视觉 diff、录制/trace、代理和多引擎等条件能力，不再作为前后端联调默认强制工具。
- 2026-07-02：补充项目内文件引用路径规则，明确 Windows 桌面访问 WSL 项目时，所有面向用户的项目内文件引用都用 `\\wsl.localhost\...`，`/home/...` 仅保留给 WSL 命令与日志上下文。
- 2026-07-02：更新上线接口测试门禁规则，新增项目基线资产库、参数依赖解析、可复用参数生命周期、失效持续更新和通用脚本复用优先口径。
- 2026-07-02：新增 Swag OpenAPI 全量维护规则，明确 `swag/` 为唯一正式输出目录，单接口完整 YAML、总 YAML 与 `.swag-manifest.yaml` 持续维护。
- 2026-07-02：补充上线测试与 Swag OpenAPI 双索引同步规则，明确 `swag/.swag-manifest.yaml` 与 `doc/5-tests/基线/interface-inventory.yaml` 理论上都不应缺失；任一缺失或三方接口集合不一致时，从当前代码刷新 swag 与测试基线两边。
- 2026-07-03：收紧 Swag OpenAPI 导入口径，明确单接口 YAML 导入 Apifox 时默认直入目标目录，不通过 `tags` 额外创建父目录；头部、请求参数、响应字段都必须有中文说明，源码注释不足时只允许受控推导。
- 2026-07-03：补充单接口 Swag 文件命名规则，默认采用“路径名 + 中文简要说明”格式；中文说明优先取显式 `summary`，缺失时允许受控推导，仍无法稳定得到时回退纯路径文件名并在 manifest 记录 `summary_source: unresolved`。
- 2026-07-03：补充单接口 Swag 中文简介清洗规则，明确文件名后缀必须去掉 `1.`、`11.`、`（1）`、`【1】` 等数字前缀和无业务意义特殊符号，只保留接口中文简介本体。
- 2026-07-03：收紧审查链注释门禁，明确只要本轮存在代码改动，`project-change-review-rules` 与 `implementation-review-rules` 都必须按注释双 skill 完整核验方法注释、字段/结构体字面量注释、步骤注释、`[参数]` / `[返回]`、最近修改时间和改动原因；任一缺失默认按审查失败处理，不得降级为建议项。
- 2026-07-03：补充会话自动重命名执行细节，明确 Codex 下若首屏未直接暴露 `set_thread_title` / `list_threads`，必须先通过 `tool_search` 发现线程工具，再识别当前会话并执行改名；未做工具发现不得直接记为“工具不可用”。
- 2026-07-05：会话自动重命名补充“阶段+提问”策略，要求用户提问、goal 创建 / 恢复、上下文压缩续做和长任务阶段切换时在过程中尽早判断标题，不等最终总结；标题已准确或仅小步骤推进时跳过。
- 2026-07-05：新增代码生成风格入口链路，明确新增、修改或重构代码前必须由 `code-generation-style-rules` 读取 `PROJECT_STYLE.md` 与局部样例，形成本轮代码风格契约。
- 2026-07-08：新增工具落点分流 util/common/util 规则，明确项目无关工具归 `util`，引用项目文件、路径、配置或约定的复用工具归 `common/util`。
- 2026-07-06：修正“项目内文件引用路径”规则的表述边界。用户反馈实际输出中仍出现 `/home/...` 裸路径，排查发现 `windows-wsl-execution-rules/SKILL.md`、`path-mapping.md`、`recommended-workflow.md`、`command-templates.md` 和本文件的“Windows / WSL 执行边界”词条，都把这条规则的表述挂在“agent 在 Windows”分支下；当 agent 实际直接运行在 WSL 内（情况一）时容易被误读为不适用。已改写为独立于 agent 运行位置的规则，并在“Windows / WSL 执行边界”词条中拆出交叉引用，避免两条规则的适用条件混读。
- 2026-07-06：新增“WSL 工具 PATH interop 误用排查”词条。用户反馈在 WSL 内执行命令时被解析成 Windows 打包的 `rg`，报 permission denied；补充根因（`appendWindowsPath` 导致 PATH fallthrough）、排查命令（`command -v`）、修复优先级（原生装包优先，不默认改 `/etc/wsl.conf`），并新增“新会话首次进入 WSL 项目时一次性自检”的建议（经用户确认，力度介于纯文档和自动化脚本之间）。
- 2026-07-08：新增 Git 协作联动 Obsidian 沉淀规则，明确提交 / 推送 / PR 收口形成可复用事实时先检索并沉淀，但沉淀不构成提交授权。

### 上线接口测试门禁规则
- 别名: project-release-test-rules, 上线测试门禁
- 类型: 测试域核心规则
- 定义: 上线前项目级全接口测试门禁，替代人工接口回归验证，输出上线准入结论。每个业务项目必须在 `doc/5-tests/基线/` 长期维护接口清单、参数来源、依赖图、可复用参数、场景目录、脚本适配、执行历史和变更日志；同时将 `swag/.swag-manifest.yaml` 与 `doc/5-tests/基线/interface-inventory.yaml` 作为当前代码接口事实的双索引，任一缺失、陈旧或接口集合不一致时，先刷新 swag 与测试基线两边。若目标接口参数无法直接确定，agent 必须按 `reusable_param -> upstream_api -> local_database -> local_cache -> openapi_example -> fixture -> rule` 解析，并把来源写入依赖追踪；已测试通过的参数可持续复用，但必须有 `candidate/reusable/stale/invalid/quarantined/retired` 生命周期、复验、失效归因和持续回写机制。已有通用脚本能力优先复用，缺能力时扩展 `project-release-test-rules/scripts/generate_release_test_plan.py` 的通用子命令，不为每次上线重复生成一次性脚本。
- 来源: `project-release-test-rules/SKILL.md`、`project-release-test-rules/references/baseline-asset-rules.md`、`project-release-test-rules/scripts/generate_release_test_plan.py`
- 适用范围: 全项目上线前接口测试、回归验证、上线准入判定
- 更新时间: 2026-07-02
- 状态: 启用

### Swag OpenAPI 全量维护规则
- 别名: swag-openapi-maintainer-rules, 更新 swag, OpenAPI YAML 资产
- 类型: API 文档资产规则
- 定义: 当用户要求生成、补齐、刷新、维护项目 swag，导出 Apifox / OpenAPI / Swagger YAML，或补齐上游/第三方出站接口文档时，触发 `swag-openapi-maintainer-rules`。自有接口继续从真实路由、controller、请求 DTO、响应 DTO、统一响应包装和鉴权中间件读取，维护根 `swag/` 的自有接口全量文档；上游接口从 client、请求构造、base URL 和响应消费代码读取，按 B1 独立落在 `swag/<vendor-slug>/`。上游 manifest 固定使用 `source_type: upstream`、`upstream`、`base_url`、`coverage: partial`、`source_client_file`、`source_symbols` 和 `discovery_confidence`；根 `openapi.yaml` 不聚合上游。每个接口仍使用可独立导入 Apifox 的完整 YAML、单接口无默认 tags、路径名加中文简要说明和中文字段描述；上游只记录本项目实际消费字段，官方资料只能离线受控补充，不能联网抓取或编造字段。根与上游清理按目录隔离，manifest 的 `file` 必须是裸文件名。自有接口若存在上线测试基线，刷新 swag 后继续同步或提示同步 `doc/5-tests/基线/interface-inventory.yaml`；上游子集不自动并入自有基线。
- 来源: `swag-openapi-maintainer-rules/SKILL.md`
- 适用范围: 自有 HTTP API 与主动调用的上游/第三方出站接口文档导出、Swagger/OpenAPI 资产维护、Apifox YAML 导入
- 更新时间: 2026-07-14
- 状态: 启用

## 需求与实施文档极致完备化规则

- 需求、验收、实施总览、实施周期和最小任务卡均采用 Markdown + YAML front matter；复杂度为 L2 及以上时，按语义提供 Mermaid 流程图和时序图，L3/L4 追加状态、数据、依赖或故障图。
- 高推理模型冻结业务、技术、测试、回滚、停止和异常决策；普通模型只能按 `REQ -> AC -> PLAN -> CYCLE -> TASK -> TEST -> EVIDENCE` 追踪链执行，不得补默认值或猜测未决决策。
- 每个最小任务必须唯一归属一个实施周期，并完成“实现/落盘 -> 真实测试或有证据的免测 -> 审查 -> 验收”闭环；缺少任一证据时不得把状态写为已完成。
- `artifact-delivery-gate-rules` 是文档质量唯一机器门禁；profile、严格追踪、N/A 理由、失效链接、Mermaid 语法和 UTF-8 检查失败时必须回开上游文档。
- 实施规划使用单来源实施总览和项目级全量顺序实施方案两层入口；周期状态、任务状态、项目当前状态、审查和最终验收必须同步，不能保留已被后续事实超越的旧入口状态。

## Windows PowerShell 环境自动迭代规则

- `windows-powershell-environment-rules` 的新会话入口是 `initialize_windows_powershell.ps1 -Mode SessionEnsure`；通过用户级 TTL marker 和原子锁避免重复准备，Apply journal 不完整时写 `complete=false`，不得伪造健康状态。
- Windows PowerShell 命令缺失统一经 `recover_windows_command.ps1` / `RecoverCommand` 路由；canonical manifest 或显式精确 `PackageId` 才能安装，未知命令不执行 `winget search` 猜包。
- 安装并真实版本探针验证成功的非 canonical 工具写入用户级 `discovered-tools.json`，仅 `verified=true` 且通过 ID/命令/source 白名单的记录在后续会话合并读取；canonical `tool-manifest.yaml` 不运行时修改。
- 失败摘要写入用户级 `failure-cases.json`，必须 UTF-8、原子替换、去重、限长、脱敏；PowerShell Windows owner 与 WSL 原生 shell/`127` owner 分离。
- 当前 runtime 不提供任意 agent shell 调用的全局失败拦截；自动恢复范围仅限显式 wrapper 或未来接入 runtime hook 的路径。

## 机器索引区

```yaml
version: 1
entities:
  - entity_id: rule.swag-upstream-openapi
    name: "上游与第三方出站接口文档规则"
    type: "API 文档资产规则"
    aliases:
      - swag-openapi-maintainer-rules
      - 上游接口文档
      - 第三方出站接口文档
      - swag/<vendor-slug>
    definition: "自有接口继续在根 swag/ 维护全量文档；本项目主动调用的外部第三方 API 与内部其他服务按 B1 独立落在 swag/<vendor-slug>/，每个子目录自带 openapi、manifest 和单接口 YAML。上游 manifest 固定使用 source_type: upstream、upstream、base_url、coverage: partial、source_client_file、source_symbols、discovery_confidence；只记录代码实际调用和消费字段，根与上游清理按目录隔离，file 必须是裸文件名。"
    scope: "swag-openapi-maintainer-rules 的出站调用发现、OpenAPI 生成、递归校验与 Apifox 导入"
    status: "active"
    evidence_ids:
      - evidence.skill.swag-openapi-maintainer
      - evidence.dialog.swag-upstream-openapi
    context_ids:
      - context.implementation-flow
    updated_at: 2026-07-14
  - entity_id: rule.imagegen-error-case-evolution
    name: "Imagegen 错误案例持续演进"
    type: "Skill 维护规则"
    aliases:
      - imagegen
      - gpt-image-2 错误案例库
      - 生图失败经验回写
    definition: "权威 imagegen skill 使用 references/error-casebook.md 保存已复现、已解决、已验证且已脱敏的生图错误；每次失败先分类并查找已有案例，解决后在获得 skill 维护授权时去重回写，未验证错误不得进入可执行案例，敏感凭据和用户私有内容不得落盘。"
    scope: "gpt-image-2 CLI fallback、参数校验、透明背景、依赖/鉴权、限流与瞬态网络错误"
    status: "active"
    evidence_ids:
      - evidence.skill.imagegen
      - evidence.dialog.imagegen-error-case-evolution
    context_ids:
      - context.imagegen-maintenance
    updated_at: 2026-07-12
  - entity_id: rule.execution-failure-learning
    name: "执行失败持续学习与主动预防"
    type: "Skill 维护规则"
    aliases:
      - execution-failure-learning-rules
      - 执行失败案例演进
      - prevent recover learn
    definition: "高风险工具调用前进入 prevent 预检，非预期失败进入 recover 分类、查库和同输入同成功标准复验，验证通过后才进入 learn。案例正文只归属于唯一 owner Skill；无维护授权保持 candidate，冲突标记 conflicted，业务 Bug、Skill 缺口和跨项目知识分别回流 bug-*、skill-evolution-rules 与 obsidian-knowledge-flow。"
    scope: "imagegen、Windows/WSL、浏览器、认证 URL、MCP/插件安装、Obsidian CLI 及后续注册的高风险执行域"
    status: "active"
    evidence_ids:
      - evidence.skill.execution-failure-learning
      - evidence.test.execution-failure-learning
    context_ids:
      - context.execution-failure-learning
    updated_at: 2026-07-12
  - entity_id: rule.task-blocker-closure
    name: "任务阻断收口与恢复"
    type: "流程规则"
    aliases:
      - BLK-* 阻断记录
      - 任务已阻断
      - 解决计划与重入点
    definition: "真实阻断只以共享 BLK-* 契约记录，生产者只提供结构化事实，reasoning-summary-structure-rules 唯一渲染用户可见收口。记录必须包含状态、阶段、证据、已尝试动作、停止边界、影响、至多三步恢复计划、重入点和去重键；limited、not_applicable、P2/P3、用户取消与预期负向测试不触发。"
    scope: "审查、验收、功能验证、Bug 验证、执行失败、运行时恢复、最终总结与文档门禁"
    status: "active"
    evidence_ids:
      - evidence.doc.task-blocker-closure
      - evidence.test.task-blocker-closure
    context_ids:
      - context.task-blocker-closure
    updated_at: 2026-07-14
  - entity_id: rule.authenticated-url-routing
    name: "URL 认证浏览器默认路由"
    type: "浏览器路由规则"
    aliases:
      - authenticated-url-routing-rules
      - 已登录 Chrome 路由
      - URL 默认 Chrome Plugin
    definition: "当用户提供 URL、网页地址或在线文档链接并要求读取、分析、截图或排查页面时，默认优先命中 `authenticated-url-routing-rules`，并优先通过 `chrome:control-chrome` 复用用户已登录的真实 Chrome profile；依赖真实 profile 的页面在 Chrome Plugin 不可用时停在连接/授权阻断，明确为公开或 local 且不依赖用户 profile 的页面才按统一路由选择 Chrome DevTools MCP 或 `agent-browser`。"
    scope: "URL 分析、在线文档读取、浏览器权限页面"
    status: "active"
    evidence_ids:
      - evidence.skill.authenticated-url-routing
    context_ids:
      - context.url-analysis
    updated_at: 2026-07-03
  - entity_id: rule.windows-powershell-environment
    name: "Windows PowerShell 环境准备与工具边界"
    type: "环境规则"
    aliases:
      - windows-powershell-environment-rules
      - PowerShell 7 默认入口
      - Windows CLI 工具清单
    definition: "Windows 专项入口优先使用 PowerShell 7.6.3；Windows Terminal 用户级 defaultProfile 指向唯一受管 PowerShell 7 profile；PowerShell 5.1 保留为旧脚本兼容回退。Windows 侧按固定 manifest 幂等安装并验证常用 CLI；7z/tlrc 在非管理员环境下保留权限阻断。Windows 工具不等于 WSL 工具，WSL 仍须用 command -v 验证原生路径。"
    scope: "Windows PowerShell 专项入口、Windows Terminal 用户设置、Windows CLI 工具安装与 WSL 隔离"
    status: "active"
    evidence_ids:
      - evidence.skill.windows-powershell-environment
      - evidence.test.windows-powershell-environment
    context_ids:
      - context.windows-powershell-environment
    updated_at: 2026-07-12
  - entity_id: rule.plain-language-document-layering
    name: "白话文档与附录分层"
    type: "文档交接规则"
    aliases:
      - 正文白话化
      - 执行附录
      - 追踪附录
    definition: "研发文档 H1 后单段正文固定说明结论、影响、范围、非范围、变化、完成标准、术语说明和验证状态；技术细节、命令、稳定 ID、追踪矩阵和证据分别放入执行附录或追踪附录。24 个受管模板由登记表统一覆盖，未修改历史文档不批量迁移。审查、验收、功能验证、浏览器联调和第三方验证统一使用三态门禁：not_applicable 有原因和依据但不阻断，limited 可继续准备但不能正式放行，applicable 只有在来源明确要求、当前必须完成且没有验证或替代验证时才阻断。"
    scope: "需求、实施、审查、验收、Bug、测试、架构、交付和工作报告"
    status: "active"
    evidence_ids:
      - evidence.skill.plain-language-document-contract
      - evidence.test.engineering-document-validator
    context_ids:
      - context.document-handoff
    updated_at: 2026-07-13
  - entity_id: term.doc-top-level-mixed-naming
    name: "doc 顶层混合命名"
    type: "术语"
    aliases:
      - 中文语义优先命名
    definition: "`doc/` 根目录保留英文，活动子目录采用“编号顺序 + 中文语义优先 + 工程通用域保留英文”的混合方案。"
    scope: "文档目录命名"
    status: "active"
    evidence_ids:
      - evidence.skill.artifact-storage
      - evidence.dialog.doc-layout
    context_ids:
      - context.doc-directory-naming
    updated_at: 2026-07-03
  - entity_id: rule.old-directory-cleanup
    name: "旧目录处理规则"
    type: "迁移约束"
    aliases:
      - 不保留兼容层
    definition: "当目录迁移完成且用户未要求保留兼容入口时，应删除旧目录、旧占位文件和旧跳转文档，不保留并行旧包或兼容壳。"
    scope: "目录迁移与收口"
    status: "active"
    evidence_ids:
      - evidence.skill.artifact-storage
      - evidence.dialog.old-directory-cleanup
    context_ids:
      - context.directory-migration
    updated_at: 2026-07-03
  - entity_id: rule.implementation-cycle-minimum-task
    name: "实施周期与最小任务闭环"
    type: "流程规则"
    aliases:
      - 周期最小任务闭环
      - 实施周期顺序
      - 最小任务全流程收口
    definition: "实施周期是项目第一期、第二期、第三期等大进度单位和顺序边界；执行必须先按周期推进，当前周期内每个最小任务都完成实现、真实测试、审查、验收后，才允许进入下一最小任务或下一周期。"
    scope: "实施规划、连续执行、文档落盘、最终验收"
    status: "active"
    evidence_ids:
      - evidence.skill.implementation-planning
      - evidence.skill.autonomous-execution
      - evidence.skill.final-acceptance
    context_ids:
      - context.implementation-flow
    updated_at: 2026-07-05
  - entity_id: rule.implementation-sequence-master-plan
    name: "需求与实施计划全量顺序实施方案"
    type: "流程规则"
    aliases:
      - 实施顺序总表
      - 全量顺序实施方案
      - 新项目实施总顺序
    definition: "新项目、项目初期或多来源对象存在多份需求 / 实施文档时，必须在 `doc/3-实施/` 维护项目级或来源集合级总顺序文档，串起需求主文档、验收标准、实施总览、实施周期和周期内最小任务；该文档只负责跨来源对象排序，不替代单来源对象实施总览。"
    scope: "实施规划、文档落盘、连续执行入口"
    status: "active"
    evidence_ids:
      - evidence.skill.implementation-planning
      - evidence.skill.artifact-storage
    context_ids:
      - context.implementation-flow
      - context.doc-directory-naming
    updated_at: 2026-07-05
  - entity_id: rule.code-generation-style-contract
    name: "代码生成风格入口链路"
    type: "流程规则"
    aliases:
      - code-generation-style-rules
      - 代码风格契约
      - 生成代码前风格总控
      - PROJECT_STYLE 应用入口
    definition: "新增、修改或重构任意代码、脚本、测试支撑代码或配置型代码前，必须先由 `code-generation-style-rules` 读取用户本轮要求、目标文件 / 同目录样例、根目录 `PROJECT_STYLE.md` 和已命中的编码类 skill，形成本轮代码风格契约；`project-style-rules` 只维护长期风格记忆，`code-style-consistency-rules` 基于契约检查局部一致性。"
    scope: "编码基线域、仓库级规则自举、代码生成与修改"
    status: "active"
    evidence_ids:
      - evidence.skill.code-generation-style
      - evidence.skill.project-agents-bootstrap
    context_ids:
      - context.code-generation-style
    updated_at: 2026-07-05
  - entity_id: rule.simple-check-inline-readability
    name: "简单检查职责就地表达"
    type: "代码可读性规则"
    aliases:
      - 小函数内联
      - 避免过度职责拆分
      - 简单检查不强拆函数
    definition: "职责清晰不等于每个职责都拆成独立函数。极短的局部检查、判空、匹配器取用、scope/flag 选择等逻辑，如果只有一个调用点、无副作用、无复杂分支、无独立测试价值，优先留在当前函数内，并用步骤注释或局部注释补清业务含义；只有复用、稳定业务术语、复杂规则、副作用或独立测试需求成立时才拆函数。"
    scope: "函数拆分、局部检查、guard 分支、简单匹配逻辑、注释补充"
    status: "active"
    evidence_ids:
      - evidence.skill.code-readability-rules
      - evidence.dialog.simple-check-inline
    context_ids:
      - context.code-generation-style
    updated_at: 2026-07-09
  - entity_id: rule.util-common-util-placement-split
    name: "util 与 common/util 工具分流"
    type: "包结构规则"
    aliases:
      - util 归位
      - common/util 归位
      - util 与 common/util 区分
    definition: "util 仅存放与当前项目无关、脱离项目上下文仍成立的通用工具；common/util 仅存放可复用但依赖当前项目文件、路径、配置、命名约定或目录结构的工具。引用项目文件或项目约定的复用工具不要放进独立 util。"
    scope: "通用工具、公共函数、复用代码、包归位"
    status: "active"
    evidence_ids:
      - evidence.skill.common-util-rules
      - evidence.skill.package-structure-rules
      - evidence.dialog.util-common-util-placement
    context_ids:
      - context.code-generation-style
    updated_at: 2026-07-08
  - entity_id: rule.thread-title-process-trigger
    name: "会话标题过程触发"
    type: "工作台规则"
    aliases:
      - thread-title-rules
      - 会话自动重命名
      - 阶段加提问改名
      - goal 中途改名
    definition: "当前会话收到明确提问、进入明确任务，或发生 goal 创建 / 恢复、上下文压缩续做、长任务阶段切换等可命名过程节点时，若能稳定归纳中文任务主题且当前标题为空泛、过时或不匹配，必须命中 `thread-title-rules` 并通过真实线程工具尽早改名；标题已准确、用户禁止或只是最小任务内部小步骤推进时跳过。"
    scope: "会话管理、goal 长任务、上下文续做、任务检索"
    status: "active"
    evidence_ids:
      - evidence.skill.thread-title
      - evidence.dialog.thread-title-process-trigger
    context_ids:
      - context.thread-title-management
    updated_at: 2026-07-05
  - entity_id: rule.obsidian-knowledge-flow-selective-default
    name: "Obsidian 知识流选择性默认触发链"
    type: "流程规则"
    aliases:
      - obsidian-knowledge-flow
      - Obsidian 知识流
      - 选择性默认触发
      - 知识库检索沉淀
    definition: "项目启动先按父目录平台规则 -> PROJECT_CURRENT.md -> PROJECT_MEMORY.md 读取本地上下文；current 覆盖维护且不超过 51,200 字节，memory 只承载稳定规则与关键决策，history 只追加且普通启动不读。Obsidian 固定使用 D:\\obsidian_data 及其 知识库/ 工作区，仅在跨项目历史或既有 vault 知识依赖时通过 CLI 检索 / 读取，仅在收口形成可复用知识时先检索再沉淀；普通任务不为形式调用 CLI，CLI / vault 不可用时阻断且不得直接读写 vault 文件。项目本地 Markdown 与 vault 链路不得混用。"
    scope: "记忆域、命中检查、阶段收口、最终总结、Obsidian vault 知识检索与沉淀"
    status: "active"
    evidence_ids:
      - evidence.skill.obsidian-knowledge-flow
      - evidence.skill.skill-hit-check
      - evidence.doc.repo-rules
      - evidence.doc.skill-plan
    context_ids:
      - context.obsidian-knowledge-flow
      - context.memory-domain
    updated_at: 2026-07-11
  - entity_id: rule.obsidian-windows-wsl-bridge-boundary
    name: "Obsidian Windows/WSL bridge 固定执行边界"
    type: "跨宿主执行规则"
    aliases:
      - obsidian_cli_bridge
      - Windows/WSL CLI bridge
      - bridge-only vault
    definition: "Windows 与 WSL 的 Obsidian 检索、创建、追加、读取和 INDEX 更新统一经 obsidian_cli_bridge.py，最终由 Windows 官方 CLI 操作唯一 vault 根 D:\\obsidian_data；知识库/ 只是 vault 内路径前缀，selector 按注册根动态唯一解析。WSL 仅通过 PowerShell interop，不安装原生 Linux CLI，不使用 vault 文件系统 fallback；写入必须 verified=true readback，应用恢复最多隐藏启动一次并有限重试。"
    scope: "Windows/WSL 知识流、bridge transport、长正文分块与读回验证"
    status: "active"
    evidence_ids:
      - evidence.skill.obsidian-knowledge-flow
      - evidence.doc.repo-rules
    context_ids:
      - context.obsidian-knowledge-flow
      - context.memory-domain
    updated_at: 2026-07-13
  - entity_id: rule.git-obsidian-capture-link
    name: "Git 协作联动 Obsidian 沉淀"
    type: "流程规则"
    aliases:
      - 提交前知识捕获
      - Git 收口沉淀
      - commit 联动 Obsidian
    definition: "当本仓库出现提交、推送、PR 收口或交付说明准备，且本轮形成可复用事实、决策、流程、定义、偏好、来源或调试经验时，优先命中 `obsidian-knowledge-flow` 做 `Obsidian:沉淀` 判定；沉淀只负责知识捕获，不构成 `git commit` / `git push` 授权。"
    scope: "提交流程、交付收口、Obsidian 记忆沉淀"
    status: "active"
    evidence_ids:
      - evidence.skill.obsidian-knowledge-flow
      - evidence.skill.git-collaboration
      - evidence.dialog.git-obsidian-capture-link
    context_ids:
      - context.obsidian-knowledge-flow
      - context.git-collaboration
      - context.memory-domain
    updated_at: 2026-07-08
  - entity_id: rule.git-commit-domain-split
    name: "Git 提交域隔离规则"
    type: "流程规则"
    aliases:
      - 提交域隔离
      - 需求实施测试Bug审查验收单独提交
      - 代码实现单独提交
    definition: "`提交git` 允许拆成多次提交清空工作区，但每个 commit 默认只承载一个提交域。`doc/2-需求/`、`doc/3-实施/`、`doc/4-bugs/`、`doc/5-tests/`、`doc/6-审查/`、`doc/7-验收/` 六类流程产物各自单独提交；测试文件（至少 `doc/5-tests/**`、`*_test.*`、`*.spec.*`、`*.test.*`）归入测试提交；代码实现 / 运行配置单独提交，不与上述流程文档域或测试文件混提。"
    scope: "提交流程、需求/实施/Bug/测试/审查/验收归档"
    status: "active"
    evidence_ids:
      - evidence.skill.git-collaboration
      - evidence.dialog.git-commit-domain-split
    context_ids:
      - context.git-collaboration
    updated_at: 2026-07-08
  - entity_id: rule.git-commit-review-acceptance-evidence
    name: "Git 提交基础审查与验收闸门"
    type: "流程规则"
    aliases:
      - 提交前审查检查
      - Git 基础验收
      - 提交不生成审查验收文档
    definition: "Git 提交必须直接对 staged 改动执行基础审查与基础验收，并在提交证据中记录格式、注释、安全性、并发安全性、系统崩溃风险、边界条件和测试/功能验证适用性；不得因提交自动创建或要求 `doc/6-审查/`、`doc/7-验收/`。显式总审查、正式最终验收和非 Git 正式放行仍按各自规则归档。"
    scope: "提交流程、基础审查、基础验收"
    status: "active"
    evidence_ids:
      - evidence.skill.git-collaboration
      - evidence.dialog.git-commit-no-review-acceptance-doc
    context_ids:
      - context.git-collaboration
    updated_at: 2026-07-14
relations:
  - relation_id: rel.old-directory-cleanup.depends-on.doc-top-level-mixed-naming
    type: "depends_on"
    from: "rule.old-directory-cleanup"
    to: "term.doc-top-level-mixed-naming"
    evidence_ids:
      - evidence.skill.artifact-storage
    status: "active"
  - relation_id: rel.git-obsidian-capture-link.depends-on.obsidian-knowledge-flow
    type: "depends_on"
    from: "rule.git-obsidian-capture-link"
    to: "rule.obsidian-knowledge-flow-selective-default"
    evidence_ids:
      - evidence.skill.obsidian-knowledge-flow
      - evidence.skill.git-collaboration
    status: "active"
evidence:
  - evidence_id: evidence.skill.swag-openapi-maintainer
    type: "skill"
    source: "swag-openapi-maintainer-rules/SKILL.md 与 references"
    path: "swag-openapi-maintainer-rules/SKILL.md"
    note: "上游出站接口触发、B1 子目录、manifest 元数据、递归校验和根/上游隔离规则来源"
  - evidence_id: evidence.dialog.swag-upstream-openapi
    type: "dialog"
    source: "2026-07-14 需求实施计划与离线验证"
    path: "doc/5-tests/2026-07-14_121425/第三方swag校验升级验证/README.md"
    note: "7 个离线正反例证明上游 scope、裸文件名守卫、单目录兼容和陌生目录 warning 可验证"
  - evidence_id: evidence.doc.task-blocker-closure
    type: "doc"
    source: "任务阻断收口共享契约"
    path: "artifact-delivery-gate-rules/references/task-blocker-closure-contract.md"
    note: "唯一 BLK-* 字段、生产者边界、最终渲染 owner 和非阻断排除规则来源"
  - evidence_id: evidence.test.task-blocker-closure
    type: "test"
    source: "本地任务阻断收口验证"
    path: "artifact-delivery-gate-rules/tests/test_validate_engineering_docs.py"
    note: "52 项文档门禁单元测试与运行时阻断事实测试证明状态边界和恢复事实可验证"
  - evidence_id: evidence.skill.imagegen
    type: "skill"
    source: "imagegen/SKILL.md"
    path: "imagegen/SKILL.md"
    note: "imagegen 错误案例分类、验证、授权回写、去重和敏感信息保护规则来源"
  - evidence_id: evidence.dialog.imagegen-error-case-evolution
    type: "dialog"
    source: "用户需求与本轮验证"
    note: "用户要求持续记录生图错误示例和解决方案，本轮以本地 dry-run/check 验证首批案例"
  - evidence_id: evidence.skill.execution-failure-learning
    type: "skill"
    source: "execution-failure-learning-rules/SKILL.md"
    path: "execution-failure-learning-rules/SKILL.md"
    note: "执行失败 prevent/recover/learn 路由、唯一 owner、脱敏、去重、冲突和授权门禁来源"
  - evidence_id: evidence.test.execution-failure-learning
    type: "test"
    source: "doc/5-tests/2026-07-12_031353/execution_failure_learning_rules/forward_behavior_test.py"
    path: "doc/5-tests/2026-07-12_031353/execution_failure_learning_rules/forward_behavior_test.py"
    note: "AC-001 至 AC-008 前向行为验证，25 项断言全部通过"
  - evidence_id: evidence.skill.authenticated-url-routing
    type: "skill"
    source: "authenticated-url-routing-rules/SKILL.md"
    path: "authenticated-url-routing-rules/SKILL.md"
    note: "URL 默认走真实 Chrome 登录态的技能定义来源"
  - evidence_id: evidence.skill.artifact-storage
    type: "skill"
    source: "artifact-storage-rules/SKILL.md"
    path: "artifact-storage-rules/SKILL.md"
    note: "文档目录与迁移收口规则来源"
  - evidence_id: evidence.dialog.doc-layout
    type: "dialog"
    source: "对话确认"
    note: "doc 顶层混合命名为仓库长期口径"
  - evidence_id: evidence.dialog.old-directory-cleanup
    type: "dialog"
    source: "对话确认"
    note: "旧目录迁移完成后不保留兼容层"
  - evidence_id: evidence.skill.implementation-planning
    type: "skill"
    source: "implementation-planning-rules/SKILL.md"
    path: "implementation-planning-rules/SKILL.md"
    note: "实施周期、最小任务清单和计划闸门来源"
  - evidence_id: evidence.skill.autonomous-execution
    type: "skill"
    source: "autonomous-execution-rules/SKILL.md"
    path: "autonomous-execution-rules/SKILL.md"
    note: "开始实施后的周期内最小任务连续执行来源"
  - evidence_id: evidence.skill.final-acceptance
    type: "skill"
    source: "final-acceptance-rules/SKILL.md"
    path: "final-acceptance-rules/SKILL.md"
    note: "最终验收核对周期收口与最小任务闭环证据来源"
  - evidence_id: evidence.skill.code-generation-style
    type: "skill"
    source: "code-generation-style-rules/SKILL.md"
    path: "code-generation-style-rules/SKILL.md"
    note: "代码生成前风格契约入口来源"
  - evidence_id: evidence.skill.project-agents-bootstrap
    type: "skill"
    source: "project-agents-bootstrap/SKILL.md"
    path: "project-agents-bootstrap/SKILL.md"
    note: "仓库级规则自举同步代码生成风格入口来源"
  - evidence_id: evidence.skill.code-readability-rules
    type: "skill"
    source: "code-readability-rules/SKILL.md"
    path: "code-readability-rules/SKILL.md"
    note: "函数结构、职责拆分颗粒度和过度小函数内联规则来源"
  - evidence_id: evidence.dialog.simple-check-inline
    type: "dialog"
    source: "对话确认"
    note: "用户通过 DID matcher 示例确认极短检查职责可留在当前函数内，用注释补清业务语义"
  - evidence_id: evidence.skill.common-util-rules
    type: "skill"
    source: "common-util-rules/SKILL.md"
    path: "common-util-rules/SKILL.md"
    note: "公共工具复用、存放位置和 util/common/util 分流规则来源"
  - evidence_id: evidence.skill.package-structure-rules
    type: "skill"
    source: "package-structure-rules/SKILL.md"
    path: "package-structure-rules/SKILL.md"
    note: "包结构、目录分层和子包归位规则来源"
  - evidence_id: evidence.dialog.util-common-util-placement
    type: "dialog"
    source: "对话确认"
    note: "当前对话确认 util 与 common/util 的分流口径"
  - evidence_id: evidence.skill.thread-title
    type: "skill"
    source: "thread-title-rules/SKILL.md"
    path: "thread-title-rules/SKILL.md"
    note: "会话标题过程触发与真实改名工具约束来源"
  - evidence_id: evidence.dialog.thread-title-process-trigger
    type: "dialog"
    source: "对话确认"
    note: "用户确认采用“阶段+提问”策略，要求提问、goal 创建 / 恢复和长任务阶段切换时在过程中尝试改名"
  - evidence_id: evidence.skill.obsidian-knowledge-flow
    type: "skill"
    source: "obsidian-knowledge-flow/SKILL.md"
    path: "obsidian-knowledge-flow/SKILL.md"
    note: "Obsidian 知识流选择性默认判断、CLI 检索、捕获和沉淀规则来源"
  - evidence_id: evidence.skill.git-collaboration
    type: "skill"
    source: "git-collaboration-rules/SKILL.md"
    path: "git-collaboration-rules/SKILL.md"
    note: "Git 协作与提交授权规则来源"
  - evidence_id: evidence.skill.skill-hit-check
    type: "skill"
    source: "skill-hit-check-rules/SKILL.md"
    path: "skill-hit-check-rules/SKILL.md"
    note: "首条命中检查输出 Obsidian 判断并联动 obsidian-knowledge-flow 的规则来源"
  - evidence_id: evidence.doc.repo-rules
    type: "doc"
    source: "AGENTS.md / CLAUDE.md"
    path: "AGENTS.md"
    note: "仓库级 Obsidian 选择性默认触发硬规则来源"
  - evidence_id: evidence.doc.skill-plan
    type: "doc"
    source: "编码skill.md"
    path: "编码skill.md"
    note: "主规划记忆域将 obsidian-knowledge-flow 纳入正式触发链的来源"
  - evidence_id: evidence.dialog.git-obsidian-capture-link
    type: "dialog"
    source: "对话确认"
    note: "用户要求将 Git 提交流程与 Obsidian 沉淀机制联动到项目规则中"
  - evidence_id: evidence.dialog.git-commit-domain-split
    type: "dialog"
    source: "对话确认"
    note: "用户要求需求、实施、测试、Bug、审查、验收与代码实现按提交域拆分，不再混在同一个 commit 里"
  - evidence_id: evidence.dialog.git-commit-no-review-acceptance-doc
    type: "dialog"
    source: "对话确认"
    note: "用户要求 Git 提交保留审查验收步骤，但不自动生成审查或验收文档"
contexts:
  - context_id: context.task-blocker-closure
    type: "task-scope"
    name: "任务阻断收口与恢复"
    note: "适用于真实 blocked 或 manual_handoff 的统一事实、解决计划和重入验证"
  - context_id: context.imagegen-maintenance
    type: "skill-maintenance"
    name: "Imagegen Skill 维护"
    note: "适用于生图调用错误的案例检索、排障验证、脱敏回写和版本演进"
  - context_id: context.execution-failure-learning
    type: "skill-maintenance"
    name: "执行失败持续学习"
    note: "适用于高风险调用的执行前预检、失败恢复、候选案例回写和 active 授权晋级"
  - context_id: context.url-analysis
    type: "task-scope"
    name: "URL 分析与在线文档读取"
    note: "适用于需要读取、分析或截图已登录页面的场景"
  - context_id: context.doc-directory-naming
    type: "repository-convention"
    name: "文档目录命名"
    note: "适用于 doc 顶层活动目录命名与归档"
  - context_id: context.directory-migration
    type: "repository-convention"
    name: "目录迁移与收口"
    note: "适用于目录迁移完成后的旧目录清理"
  - context_id: context.implementation-flow
    type: "task-scope"
    name: "实施规划与执行"
    note: "适用于实施周期、最小任务、连续执行、文档落盘和最终验收"
  - context_id: context.code-generation-style
    type: "task-scope"
    name: "代码生成风格契约"
    note: "适用于新增、修改、重构代码前的风格来源收敛和契约检查"
  - context_id: context.thread-title-management
    type: "workspace-convention"
    name: "会话标题管理"
    note: "适用于用户提问、goal 长任务、上下文续做和阶段切换时的会话标题更新"
  - context_id: context.obsidian-knowledge-flow
    type: "task-scope"
    name: "Obsidian 知识流"
    note: "适用于历史知识依赖、知识库检索、阶段收口沉淀和最终总结捕获判断"
  - context_id: context.git-collaboration
    type: "task-scope"
    name: "Git 协作与知识沉淀"
    note: "适用于提交、推送、PR 收口和交付说明准备时的知识捕获判断"
  - context_id: context.memory-domain
    type: "repository-convention"
    name: "记忆域"
    note: "适用于近期上下文、历史回忆、Obsidian 知识流和长期项目记忆"
lifecycle:
  active:
    - "rule.swag-upstream-openapi"
    - "rule.task-blocker-closure"
    - "rule.imagegen-error-case-evolution"
    - "rule.execution-failure-learning"
    - "rule.authenticated-url-routing"
    - "term.doc-top-level-mixed-naming"
    - "rule.old-directory-cleanup"
    - "rule.implementation-cycle-minimum-task"
    - "rule.implementation-sequence-master-plan"
    - "rule.code-generation-style-contract"
    - "rule.simple-check-inline-readability"
    - "rule.util-common-util-placement-split"
    - "rule.thread-title-process-trigger"
    - "rule.obsidian-knowledge-flow-selective-default"
    - "rule.git-obsidian-capture-link"
    - "rule.git-commit-domain-split"
    - "rule.git-commit-review-acceptance-evidence"
    - "rel.old-directory-cleanup.depends-on.doc-top-level-mixed-naming"
  deprecated: []
  stale: []
  conflicted: []
  retired: []
retrieval_hints:
  aliases:
    上游接口文档:
      - "rule.swag-upstream-openapi"
    第三方出站接口文档:
      - "rule.swag-upstream-openapi"
    swag/<vendor-slug>:
      - "rule.swag-upstream-openapi"
    source_type upstream:
      - "rule.swag-upstream-openapi"
    任务阻断收口:
      - "rule.task-blocker-closure"
    任务已阻断:
      - "rule.task-blocker-closure"
    BLK-*:
      - "rule.task-blocker-closure"
    imagegen:
      - "rule.imagegen-error-case-evolution"
    execution-failure-learning-rules:
      - "rule.execution-failure-learning"
    执行失败案例演进:
      - "rule.execution-failure-learning"
    prevent recover learn:
      - "rule.execution-failure-learning"
    gpt-image-2 错误案例库:
      - "rule.imagegen-error-case-evolution"
    生图失败经验回写:
      - "rule.imagegen-error-case-evolution"
    windows-powershell-environment-rules:
      - "rule.windows-powershell-environment"
    PowerShell 7 默认入口:
      - "rule.windows-powershell-environment"
    Windows CLI 工具清单:
      - "rule.windows-powershell-environment"
    authenticated-url-routing-rules:
      - "rule.authenticated-url-routing"
    已登录 Chrome 路由:
      - "rule.authenticated-url-routing"
    中文语义优先命名:
      - "term.doc-top-level-mixed-naming"
    不保留兼容层:
      - "rule.old-directory-cleanup"
    周期最小任务闭环:
      - "rule.implementation-cycle-minimum-task"
    实施周期顺序:
      - "rule.implementation-cycle-minimum-task"
    最小任务全流程收口:
      - "rule.implementation-cycle-minimum-task"
    需求与实施计划全量顺序实施方案:
      - "rule.implementation-sequence-master-plan"
    实施顺序总表:
      - "rule.implementation-sequence-master-plan"
    全量顺序实施方案:
      - "rule.implementation-sequence-master-plan"
    小函数内联:
      - "rule.simple-check-inline-readability"
    避免过度职责拆分:
      - "rule.simple-check-inline-readability"
    简单检查不强拆函数:
      - "rule.simple-check-inline-readability"
    职责拆分颗粒度:
      - "rule.simple-check-inline-readability"
    util 归位:
      - "rule.util-common-util-placement-split"
    common/util 归位:
      - "rule.util-common-util-placement-split"
    util 与 common/util 区分:
      - "rule.util-common-util-placement-split"
    项目无关工具:
      - "rule.util-common-util-placement-split"
    项目相关工具:
      - "rule.util-common-util-placement-split"
    code-generation-style-rules:
      - "rule.code-generation-style-contract"
    代码风格契约:
      - "rule.code-generation-style-contract"
    生成代码前风格总控:
      - "rule.code-generation-style-contract"
    thread-title-rules:
      - "rule.thread-title-process-trigger"
    会话自动重命名:
      - "rule.thread-title-process-trigger"
    阶段加提问改名:
      - "rule.thread-title-process-trigger"
    goal 中途改名:
      - "rule.thread-title-process-trigger"
    obsidian-knowledge-flow:
      - "rule.obsidian-knowledge-flow-selective-default"
    Obsidian 知识流:
      - "rule.obsidian-knowledge-flow-selective-default"
    选择性默认触发:
      - "rule.obsidian-knowledge-flow-selective-default"
    知识库检索沉淀:
      - "rule.obsidian-knowledge-flow-selective-default"
    Git 协作联动 Obsidian 沉淀:
      - "rule.git-obsidian-capture-link"
    提交前知识捕获:
      - "rule.git-obsidian-capture-link"
    Git 收口沉淀:
      - "rule.git-obsidian-capture-link"
    commit 联动 Obsidian:
      - "rule.git-obsidian-capture-link"
    提交域隔离:
      - "rule.git-commit-domain-split"
    需求实施测试Bug审查验收单独提交:
      - "rule.git-commit-domain-split"
    代码实现单独提交:
      - "rule.git-commit-domain-split"
  scopes:
    Imagegen Skill 维护:
      - "rule.imagegen-error-case-evolution"
    执行失败持续学习:
      - "rule.execution-failure-learning"
    高风险调用预检:
      - "rule.execution-failure-learning"
    Windows PowerShell 环境:
      - "rule.windows-powershell-environment"
    WSL 原生工具隔离:
      - "rule.windows-powershell-environment"
    candidate active 案例:
      - "rule.execution-failure-learning"
    gpt-image-2 CLI fallback:
      - "rule.imagegen-error-case-evolution"
    生图错误案例:
      - "rule.imagegen-error-case-evolution"
    URL 分析:
      - "rule.authenticated-url-routing"
    文档目录命名:
      - "term.doc-top-level-mixed-naming"
    目录迁移与收口:
      - "rule.old-directory-cleanup"
    实施规划:
      - "rule.implementation-cycle-minimum-task"
      - "rule.implementation-sequence-master-plan"
    连续执行:
      - "rule.implementation-cycle-minimum-task"
      - "rule.implementation-sequence-master-plan"
    编码基线域:
      - "rule.code-generation-style-contract"
    代码生成:
      - "rule.code-generation-style-contract"
    风格契约:
      - "rule.code-generation-style-contract"
    函数拆分:
      - "rule.simple-check-inline-readability"
    局部检查:
      - "rule.simple-check-inline-readability"
    可读性:
      - "rule.simple-check-inline-readability"
    工具落点分流:
      - "rule.util-common-util-placement-split"
    util / common/util:
      - "rule.util-common-util-placement-split"
    公共工具归位:
      - "rule.util-common-util-placement-split"
    会话标题管理:
      - "rule.thread-title-process-trigger"
    goal 长任务:
      - "rule.thread-title-process-trigger"
    记忆域:
      - "rule.obsidian-knowledge-flow-selective-default"
    Obsidian:
      - "rule.obsidian-knowledge-flow-selective-default"
    知识库检索:
      - "rule.obsidian-knowledge-flow-selective-default"
    阶段收口:
      - "rule.obsidian-knowledge-flow-selective-default"
    提交流程:
      - "rule.git-obsidian-capture-link"
      - "rule.git-commit-domain-split"
    交付收口:
      - "rule.git-obsidian-capture-link"
    Obsidian 记忆沉淀:
      - "rule.git-obsidian-capture-link"
    提交域隔离:
      - "rule.git-commit-domain-split"
  sources:
    execution-failure-learning-rules/SKILL.md:
      - "rule.execution-failure-learning"
    execution-failure-learning-rules/references/classification-and-routing.md:
      - "rule.execution-failure-learning"
    execution-failure-learning-rules/references/lifecycle-and-gates.md:
      - "rule.execution-failure-learning"
    execution-failure-learning-rules/references/case-template.md:
      - "rule.execution-failure-learning"
    windows-powershell-environment-rules/SKILL.md:
      - "rule.windows-powershell-environment"
    windows-powershell-environment-rules/references/tool-manifest.yaml:
      - "rule.windows-powershell-environment"
    windows-powershell-environment-rules/references/safety-and-validation.md:
      - "rule.windows-powershell-environment"
    windows-powershell-environment-rules/scripts/initialize_windows_powershell.ps1:
      - "rule.windows-powershell-environment"
    doc/5-tests/2026-07-12_031353/execution_failure_learning_rules/forward_behavior_test.py:
      - "rule.execution-failure-learning"
    imagegen/SKILL.md:
      - "rule.imagegen-error-case-evolution"
    imagegen/references/error-casebook.md:
      - "rule.imagegen-error-case-evolution"
    authenticated-url-routing-rules/SKILL.md:
      - "rule.authenticated-url-routing"
    artifact-storage-rules/SKILL.md:
      - "term.doc-top-level-mixed-naming"
      - "rule.old-directory-cleanup"
      - "rule.implementation-sequence-master-plan"
    implementation-planning-rules/SKILL.md:
      - "rule.implementation-cycle-minimum-task"
      - "rule.implementation-sequence-master-plan"
    autonomous-execution-rules/SKILL.md:
      - "rule.implementation-cycle-minimum-task"
    final-acceptance-rules/SKILL.md:
      - "rule.implementation-cycle-minimum-task"
    code-generation-style-rules/SKILL.md:
      - "rule.code-generation-style-contract"
    code-readability-rules/SKILL.md:
      - "rule.simple-check-inline-readability"
    code-readability-rules/references/function-structure-rules.md:
      - "rule.simple-check-inline-readability"
    common-util-rules/SKILL.md:
      - "rule.util-common-util-placement-split"
    package-structure-rules/SKILL.md:
      - "rule.util-common-util-placement-split"
    编码skill.md:
      - "rule.util-common-util-placement-split"
    project-agents-bootstrap/SKILL.md:
      - "rule.code-generation-style-contract"
      - "rule.thread-title-process-trigger"
    thread-title-rules/SKILL.md:
      - "rule.thread-title-process-trigger"
    obsidian-knowledge-flow/SKILL.md:
      - "rule.obsidian-knowledge-flow-selective-default"
    skill-hit-check-rules/SKILL.md:
      - "rule.obsidian-knowledge-flow-selective-default"
    AGENTS.md:
      - "rule.obsidian-knowledge-flow-selective-default"
      - "rule.git-obsidian-capture-link"
    CLAUDE.md:
      - "rule.obsidian-knowledge-flow-selective-default"
      - "rule.git-obsidian-capture-link"
    编码skill.md:
      - "rule.obsidian-knowledge-flow-selective-default"
      - "rule.git-obsidian-capture-link"
    git-collaboration-rules/SKILL.md:
      - "rule.git-obsidian-capture-link"
      - "rule.git-commit-domain-split"
    git-collaboration-rules/scripts/pre_commit_gate.sh:
      - "rule.git-commit-domain-split"
extensions:
  external_refs:
    - type: migration-sample
      note: "本轮仅迁移 3 条现有长期记忆作为单文件双区演练样本"
  retrieval_provider: ""
  vector_doc_id: ""
  graph_node_id: ""
```
