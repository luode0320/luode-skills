## 目录用法索引规则

- 稳定决策：package-structure-rules 是目录用法索引的唯一 Owner，通过 Catalog 条目的 related_skills、usage_recipes、package_alias、example_scope 字段关联专业 skill 和 recipe 示例。
- 稳定决策：guide 子命令按 --category、--technology、--language 查询目录用法，支持 category 别名映射（如 json -> serialization、log -> logging、convert/conversion、message/mq、scheduler/cron）。
- 稳定决策：Go recipe 示例统一存放在 package-structure-rules/references/usage-recipes-go.md，首批覆盖 convert、time、cache/redis、json、log、http；Java/Node/Python 后续按需扩展。
- 稳定决策：新增 recipe 时按流程更新 usage-recipes-go.md、Catalog 条目的 usage_recipes 字段、directory-usage-routing.md 索引表，并运行 guide 子命令验证。
- 来源：package-structure-rules/SKILL.md、package-structure-rules/references/placement-catalog.yaml、package-structure-rules/scripts/placement_catalog.py、package-structure-rules/references/directory-usage-routing.md、package-structure-rules/references/usage-recipes-go.md。
- 更新时间：2026-08-08。

# 项目长期记忆


## 计划输出完整性规则

- 稳定决策：`implementation-planning-rules` 的正式实施计划必须零决策完整落盘；plan-structure-template.md 禁止在最终输出时压缩或省略思考阶段已形成的任何落点、文件/符号、命令、断言、回滚和完成条件。
- 稳定决策：宿主外层包裹（如 `<proposed_plan>`）的简洁/3-5小节要求仅影响包裹层，不得删减计划正文中的任务字段、细节或零决策事项；仓库模板完整度优先于宿主简洁要求。
- 稳定决策：plan-output-gate.md 硬失败结构包含内容密度 hard-fail：最小任务缺少零决策字段（文件/符号、操作、禁止触碰、精确测试命令、断言、清理、回滚、完成条件、停止条件中任一项）或出现"见上文""后续再定""若干文件""TBD""TODO""实现时再看"等占位词时直接不合格。
- 稳定决策：正式实施计划的主章节仅包含章节标题、各任务缺少可执行具体字段内容即为无效计划；代码变更类计划必须给出代码落点目录树（text 代码块）。
- 来源：`implementation-planning-rules/references/plan-structure-template.md`、`plan-output-gate.md`、`plan-review-checklist.md`、`minimum-task-execution-contract.md`、`AGENTS.md`、`CLAUDE.md`、`doc/3-实施/2026-08-09_REQ-PLAN-DETAIL-COMPLETE-001/实施总览.md`。
- 更新时间：2026-08-09。


## 运行时 Mock 目录树规则

- 稳定决策：`package-structure-rules` 是 Go 运行时 Mock 目录与装配的唯一 Owner；根 `mock/` 按 `internal/` 相对路径镜像，`mock/assembly/` 是唯一装配桥，包名固定为 `assembly`。
- 稳定决策：入口必须按需配对 `main_mock.go`（`//go:build mock`）与 `main_real.go`（`//go:build !mock`），两份 selector 声明同名 `newXxx()`；`main.go` 只调用 selector，入口不得直接导入 Mock 实现包。
- 稳定决策：Mock 实现文件必须 `//go:build mock` 且包名 `mock_<源包名>`；Catalog 以 `required_build_tag`、`required_exclude_build_tag`、`mirror_source_root`、`forbidden_direct_imports` 和 `init_policy: forbidden` 固化机器约束，`guide --category runtime-mock --language go` 返回 10 条配方。
- 稳定决策：CLI 的 `check_runtime_mock_structure` 只读检查 selector 配对、构建标签、函数集合、镜像、包名和入口导入边界；违规退出码 2；adoption 不扩大既有 `test/` 遗留快照豁免。
- 来源：`package-structure-rules/references/runtime-mock-layout-go.md`、`placement-catalog.yaml`、`placement-catalog.schema.json`、`package-structure-rules/scripts/placement_catalog.py`、`test/package-structure-rules/runtime_mock_layout_test.py`、`doc/3-实施/2026-08-08_REQ-PSR-MOCK-UPGRADE_实施周期01_运行时Mock升级.md`。
- 更新时间：2026-08-08。

## Codex Desktop 任务投影断点恢复规则

- 稳定决策：`task-plan-rehydration-rules` 是 `PROJECT_CURRENT.md` 任务投影托管区的唯一 Owner，独占 v4 registry schema、计划指纹、敏感字段拒绝、51,200 字节闸门、同目录排他锁、原子写入、失活和 `update_plan` payload。
- 稳定决策：正式实施周期文档仍是真实计划源；常规任务投影只保存当前周期最多 20 个任务的 ID、悬浮文案和 `pending/in_progress/completed` 状态。`PROJECT_CURRENT.md` 托管区使用 v4 `projections[]` 注册表，按受控原始 `session_id` 隔离多个会话；Goal 投影固定为不含 Goal 原文的三步，允许 `blocked` 仅观察状态，但不保存 prompt、响应、凭据、Goal ID、业务数据或原始用户输入。
- 稳定决策：原始宿主会话 / 线程标识只允许保存于投影条目的 `session_id` 字段，其它位置仍拒绝 `thread_id` 等敏感字段；所有会改变投影或 Goal 状态的写入 API 与 CLI 都必须显式提供 `session_id`，不得静默写入伪造的 legacy 会话。
- 稳定决策：任务状态迁移固定先按 `session_id` 原子更新 `PROJECT_CURRENT.md`，再调用 `update_plan`；Desktop 重开或上下文恢复后的首次继续回合先按当前会话精确校验活动投影并重建 UI，进行中步骤必须先核验中断点。
- 稳定决策：默认执行回合取得 `confirmed` 后，任何任务首次领域动作前都必须为当前 `session_id` 持久化 `active` 或 `blocked` projection；持久化成功后的下一动作必须立即调用 `update_plan`，两者之间禁止领域写操作。`update_plan` 失败进入 `UI_SYNC_BLOCKED`，保留 projection 并禁止继续领域写入；`inactive` 不创建悬浮任务列表。
- 稳定决策：任务投影会话解析固定为显式 `--session-id` 优先、`CODEX_THREAD_ID` 回退；两者冲突、非法或同时缺失时失败关闭。`ensure-start` 和带 payload 的 `write` 是首次持久化入口，返回结果必须绑定当前 session 并携带可直接调用的 `update_plan` payload。
- 稳定决策：十分钟只作缺失 projection 的异常修复闸门。任务已真实执行但当前会话缺少活动或阻断 projection，且扣除 Plan Mode、等待用户、`blocked` 和 `manual_handoff` 后主动执行时间严格大于 600 秒时，才先调用只读 `probe-timeout`，随后补建并立即同步；不再把十分钟作为正常任务首次显示悬浮窗的入口。
- 稳定决策：`probe-timeout` 不创建锁文件、临时文件、projection 或 payload；`goal_check_required` 后只允许主 Agent 按 `get_goal -> 复用明确匹配 Goal 或 create_goal 一次 -> goal --event create -> update_plan` 执行，子 Agent 不得调用 Goal 或主悬浮窗工具。
- 稳定决策：活动 Goal 不匹配、工具不可用、创建失败或结果不明确时禁止重复创建，使用原 `ensure-timeout` 生成普通 `exact/fallback` 投影；创建结果不明确只允许一次 `get_goal` 复核，Goal 已成功但投影失败也不得再创建。
- 稳定决策：Goal 摘要来源为已确认实施计划摘要、当前确认目标或固定兜底文案，必须是单行中文、最多 80 个 Unicode 字符并脱敏，只传给 `create_goal`，不得写入项目文件、测试 fixture、工程文档、项目记忆或 Obsidian。
- 稳定决策：超时升级只在工具返回、阶段进度或回合结束前等可执行检查点运行，不承诺后台第 601 秒自动唤醒；计时起止与暂停秒数不进入 projection schema 或项目长期状态，计时上下文丢失后重新计时而不是推算。
- 稳定决策：Goal 创建优先保护活动 `persisted` 或 `synthesized/exact` 正式计划；`synthesized/fallback` 只是恢复兜底，必须让位于 Goal 固定三步。Goal blocked 清除进行中步骤但保留观察列表；Goal complete 先返回一次性全完成 `update_plan` payload，再将三步写为 `inactive`，失活后禁止重放。
- 稳定决策：UI 重建不恢复执行授权，也不等同于 `agent-runtime-recovery-rules` 的 L5 checkpoint/resume；完成投影写为 `inactive`，工具不可用时保留磁盘状态但不得声称悬浮窗已恢复。
- 来源：`task-plan-rehydration-rules/SKILL.md`、`task-plan-rehydration-rules/references/task-plan-projection-contract.md`、`doc/2-需求/2026-07-23_012302_CodexDesktop任务悬浮窗断点恢复.md`、`doc/3-实施/2026-07-25_163230_CodexDesktop任务悬浮窗断点恢复_实施周期05_超时自动升级.md`、`doc/3-实施/2026-07-25_203000_CodexDesktop任务悬浮窗断点恢复_实施周期06_Goal自动升级.md`、`doc/3-实施/2026-07-26_150000_CodexDesktop任务悬浮窗断点恢复_实施周期07_首次持久化即悬浮窗同步.md`、`doc/2-需求/2026-07-25_000001_Goal模式任务悬浮窗进度可视化.md`。
- 更新时间：2026-07-26。


## 会话交接与新任务接续规则

- 稳定决策：`session-handoff-rules` 是会话迁移唯一 Owner；命中“开新会话继续”“新会话中继续”“新会话继续”“会话太长”“归档旧会话”“迁移任务”“接续任务”“提取会话压缩信息”“唤起另一个会话”等语义时，先提取当前目标、范围、已完成、进行中、下一步、阻断、验证和关键决策，再生成脱敏交接包。
- 稳定决策：交接包使用 `codex-session-handoff` v1 JSON 契约，字段白名单、UTF-8、24,576 字节上限、`next_steps` 非空和敏感字段 / 绝对路径拒绝由 `session-handoff-rules/scripts/validate_handoff_packet.py` 校验；交接包不得保存 `session_id`、`thread_id`、prompt、完整日志或凭据。
- 稳定决策：新任务必须先用 `codex_app__list_projects` 精确匹配当前保存项目，再用 `codex_app__create_thread` 的同项目 `environment: local` 创建；创建返回真实 `threadId` 后才可调用 `codex_app__wait_threads`，`clientThreadId` 只能报告 setup pending，不得当作真实线程 ID。
- 稳定决策：新任务首轮必须重新命中 `skill-hit-check-rules`、读取项目四件套、按自身 `session_id` 校验或建立 projection，并核验进行中断点；交接不复制旧任务 UI 状态、执行授权或未知非幂等操作。
- 稳定决策：v1 归档策略固定为 `manual_only`。新任务 ready 后只提示用户人工归档旧任务，不自动调用 `codex_app__set_thread_archived`；创建失败、项目不确定或 setup pending 时不改变旧任务状态。
- 来源：`session-handoff-rules/SKILL.md`、`session-handoff-rules/references/handoff-packet-contract.md`、`session-handoff-rules/references/codex-thread-routing.md`、`session-handoff-rules/scripts/validate_handoff_packet.py`、本轮用户确认的触发词。
- 更新时间：2026-08-02。


## Plan Mode 决策选择框永久等待规则

- 稳定决策：Plan Mode 决策型 `request_user_input` 必须完全省略 `autoResolutionMs`；选择框未得到用户选择时保持 `WAITING_DECISION`，没有等待时间或重发次数上限，宿主空答案不代表取消、授权、默认选择或完成。
- 稳定决策：`answers:{}`、答案缺失、缺少预期问题 ID、`null`/空返回和宿主隐式超时的下一动作只能是立即串行重发同一未决选择框；重发保持问题 ID、选项、推荐标记和冻结文案，部分答案只保存并重发剩余问题，每次只保留一个活动选择框。
- 稳定决策：未决循环期间禁止冻结集合 `commentary`、`limited_plan`、`pending_summary`、`proposed_plan`、`final`、`summary`、`final_answer`、`task_complete`、`result_and_conclusion` 及中文“结果与结论”输出；也不得自动采用推荐项、创建 Goal、恢复任务投影或触发自动升级；总结消费方必须拒绝任何未决 `request_user_input` / `WAITING_DECISION`。
- 稳定决策：只有用户完成全部选择、明确授权“你来定/按推荐”、明确要求停止，或工具明确不可恢复且无法再次调用时才离开等待；工具故障仍保持未决并报告宿主阻断。上下文压缩或会话恢复必须保留问题身份、选项、已选答案和等待状态。
- 来源：`implementation-planning-rules/SKILL.md`、`implementation-planning-rules/references/plan-question-coverage.md`、`implementation-planning-rules/references/plan-output-gate.md`、`reasoning-summary-structure-rules/SKILL.md`、`doc/4-bugs/2026-07-26_040639_PlanMode选择框永久等待/README.md`、`doc/7-验收/2026-07-26_040639_BUG-PLAN-WAIT-20260726-001_验收标准.md`、`doc/5-tests/2026-07-26_040607/plan_mode_wait_loop/test_plan_mode_wait_loop.py`。
- 更新时间：2026-07-26。


## 六域 Skill 精简与自动触发保护规则

- 稳定决策：需求、实施、测试、Bug 与 `6-review` 风格回归精简时，用户习惯、自动触发、授权、安全、local、输出协议、暂停与停止边界均为保护语义；可以迁移位置，不得删除或弱化。独立业务审查与后置验收不再是活动域。
- 稳定决策：同生命周期收敛为单主入口加条件路由；主 Skill 保留触发摘要和职责边界，重复细则下沉 references。
- 稳定决策：退役旧 Skill 前必须具备 source-target mapping、trigger contract、protected semantic IDs、active consumers、physical asset owner、baseline hashes、rollback locator 与正负 post-delete 证据；缺任一项保持 `hold`。
- 稳定决策：`implementation-planning-rules` 保持 Plan Mode 唯一入口，只做正文去重和 references 化，不拆为竞争入口。
- 稳定决策：历史归档不批量回写旧名称；活跃资产必须完成引用切换。
- 来源：`doc/2-需求/2026-07-21_221037_六域Skill结构精简与自动触发保持.md`、`doc/7-验收/2026-07-21_221037_六域Skill结构精简与自动触发保持_验收标准.md`。
- 更新时间：2026-07-21。


## 白话文档与附录分层规则

- 需求、实施、Bug、测试、`6-review`、架构、交付和工作报告采用同一信息分层：H1 后单段正文固定说明结论、影响、范围、非范围、变化、完成标准、术语说明和验证状态；文件、命令、稳定 ID、追踪矩阵和证据分别进入执行附录或追踪附录。
- 新活动文档不再使用 `review_acceptance_gates`；完成条件写入实施计划，真实测试产生 `TEST` 证据，`6-review` 只产生 `STYLE: PASS/FIX_REQUIRED`。历史审查和验收文件保留该字段时只读兼容。
- 新文档以 `reader_level: business_general`、`writing_style: plain_chinese`、`appendix_policy: preserve_existing_or_one_terminal_appendix` 启用机器门禁；受管模板由 `plain-language-template-registry.yaml` 统一登记并逐项测试；未修改历史文档不批量迁移。
- 功能验证、浏览器联调和第三方验证按各自测试规则处理；后置审查和最终验收不再构成活动放行分支。

## 配置环境来源契约

- 稳定决策：`package-structure-rules` 的 loader 条目必须记录统一环境来源优先级 `-env > APP_ENV > ENV > local`；reference 正文、Catalog、Schema 和活动契约测试必须保持同一表达。该契约只描述配置 loader 的来源识别，不改变 embedded/YAML 秘密边界或真实项目迁移授权。
- 稳定决策：同一环境的配置加载优先使用 `embedded/`；对应 embedded 配置缺失时才回退到 `yaml/`。YAML 条目禁止秘密原值并标记为 `embedded_source_fallback`，embedded 条目允许源码私密值并标记为 `embedded_source_primary`；该安全模型不把源码私密值回显到 Agent 输出、日志、README、错误或测试报告。
- 来源：`F:\binance-wangge-go` CYCLE-11 环境来源识别实施周期、`package-structure-rules` Catalog/Schema/reference 改动和配置契约测试。
- 更新时间：2026-08-06。
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

- 稳定决策：`project-interface-release-execution-rules/scripts/release_test_engine/` 是协议中立内核，统一 IR 版本为 `2.0`；未知技术栈必须输出 `PENDING/UNSUPPORTED_ADAPTER`，不得伪报通过。
- 稳定决策：所有运行连接只来自 `local` 配置；普通业务写接口允许执行，DROP/TRUNCATE/破坏性 ALTER、源码/基础设施删除等极端操作由安全 denylist 阻断。
- 稳定决策：接口级结果固定为 `PASS`、`EXPECTED_FAIL`、`FAIL`、`PENDING`、`BLOCKED`；P0 入口任意非 `PASS` 阻断项目放行，项目门禁输出 `PASS`/`FAIL`/`PARTIAL`。
- 稳定决策：兼容入口为 `generate_release_test_plan.py doctor/run`，旧资产命令保留回退路径；项目专属字段只能写入项目基线/adapter，通用规则不得硬编码业务实体。
- 稳定决策：发现注册表覆盖 HTTP、CLI、GraphQL、gRPC、WebSocket、SOAP、JSON-RPC、消息、调度和事件；只有存在真实 local runner 的协议才允许 `PASS`，其余协议必须输出结构化 `PENDING`。
- 稳定决策：报告明细的 request/response 固定为脱敏 JSON 字符串，`responses.json` 保留脱敏对象；基线以 append-only 事件和 v2 原子投影为事实源。

## 核心记忆

### 仓库定位
- 别名: skill 仓库, 团队研发协作规则仓库
- 类型: 项目事实
- 定义: 本仓库用于沉淀面向团队研发协作的 Skill、references、脚本和入口文档，目标是让 AI 在需求、Bug、编码、实施计划、真实测试、`6-review` 和交付流程中按任务内容自动命中规则。
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
- 定义: 正式研发产物目录统一收口到 `doc/` 下；当前活动子目录按流程顺序编号为 `doc/1-架构/`、`doc/2-需求/`、`doc/3-实施/`、`doc/4-bugs/`、`doc/5-tests/`、`doc/6-review/`；`doc/6-审查/` 与 `doc/7-验收/` 仅作为历史只读归档。
- 来源: `artifact-storage-rules/references/path-map.yaml`
- 适用范围: 文档归档与规则引用
- 更新时间: 2026-06-28
- 状态: 启用

### 活动文档命名前缀
- 别名: 来源对象标识, 实施需求标识, 风格回归时分秒, Bug 进入实施计划
- 类型: 命名规则
- 定义: 需求、实施、Bug、测试和 6-review 活动产物统一使用 `YYYY-MM-DD_HHmmss` 时间前缀。实施与 6-review 等下游文档必须在时间后保留来源对象标识，来源可以是需求也可以是 Bug；历史审查/验收文件只读保留。禁止只写 `时间_阶段_说明.md`、`YYYY-MM-DD_主题.md` 或缺少来源标识的 `YYYY-MM-DD_HHmmss_主题.md`。
- 来源: `artifact-storage-rules/references/path-map.yaml`、`artifact-storage-rules/references/naming-templates.md`
- 适用范围: 需求域、实施域、Bug 域、测试域、6-review 风格回归域
- 更新时间: 2026-06-29
- 状态: 启用

### Skill 体积治理统计基线
- 别名: Skill 体积预算, 规则文档体积基线, 默认文本包
- 类型: 统计口径
- 定义: 截至 2026-07-17，正式字典主规划包含 84 个 skill；仓库根目录实际存在 111 个带 `SKILL.md` 的目录，其中 27 个属于扩展种子，不纳入主规划拆分基线。默认文本包定义为单个 skill 的 `SKILL.md` 加 `references/` 下全部文本资源的原始字节数。预算等级固定为 `normal`、`review`、`split_candidate`、`hard_warning`：`normal` 不超过 `SKILL.md` 16,000 B、单 reference 最大 12,000 B、默认文本包 48,000 B；超过建议值进入 `review`，超过 SKILL.md 20,000 B、单 reference 16,000 B 或默认文本包 64,000 B 进入 `split_candidate`，SKILL.md 超过 24,000 B 进入 `hard_warning`。
- 来源: `doc/5-tests/2026-07-17_155229/skill-split-validation/skill-size-report.py`、`doc/5-tests/2026-07-17_155229/skill-split-validation/skill-size-report.json`、`字典.md`、`doc/2-需求/2026-07-16_114619_Skill体积治理与拆分.md`
- 适用范围: Skill 体积盘点、候选冻结和后续职责拆分复评
- 更新时间: 2026-07-17
- 状态: 启用

### Skill 体积候选冻结
- 别名: Skill 拆分候选矩阵, 候选顺序, 正式/扩展种子双层追踪
- 类型: 拆分决策
- 定义: `TASK-SPLIT-01-02` 将正式 84 个 skill 与扩展种子 27 个分层记录在 `candidate-matrix.yaml`；正式进入拆分的 4 项为 `project-agents-bootstrap`、`skill-compliance-gate-rules`、`project-release-test-rules`、`agent-browser`，每项均有两个独立职责组；`2d-asset-design` 作为 P1 扩展种子例外进入 CYCLE-SPLIT-06；MCP 进入 P2 候选设计，implementation-planning 进入条件复评，其余保持暂缓或不候选。
- 来源: `doc/5-tests/2026-07-17_155229/skill-split-validation/mapping/candidate-matrix.yaml`、`doc/3-实施/2026-07-16_114619_Skill体积治理与拆分_实施周期01_预算与候选冻结.md`、`doc/7-验收/2026-07-16_114619_Skill体积治理与拆分_验收标准.md`
- 适用范围: 后续 CYCLE-SPLIT-02 至 CYCLE-SPLIT-08 的候选进入、职责映射和测试入口选择
- 更新时间: 2026-07-17
- 状态: 启用

### Skill 拆分通用测试入口
- 别名: `TEST-SPLIT-003`, 五类拆分验证, pre/post-delete fixture
- 类型: 测试契约
- 定义: `TASK-SPLIT-01-03` 固化 `validate_skill_split.py` 的 `size`、`mapping`、`trigger`、`pre-delete`、`post-delete` 五类模式，并由 `run_trigger_cases.ps1` 通过 `-CasesRoot` 转发。报告和矩阵路径必须位于仓库根目录内，fixture 根必须位于当前测试时间戳目录内；越界必须非零失败，不删除真实 skill。
- 来源: `doc/5-tests/2026-07-17_155229/技能拆分验证/README.md`、`doc/3-实施/2026-07-16_114619_Skill体积治理与拆分_实施周期01_预算与候选冻结.md`
- 适用范围: CYCLE-SPLIT-02 至 CYCLE-SPLIT-08 的静态覆盖、触发、删除前后和路径边界验证
- 更新时间: 2026-07-17
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
- 定义: 当用户只提出一句话 idea、粗略想法或老板式方向时，优先由 `requirement-intake-rules` 的 `initial-discovery` 路由主动侦察当前项目代码、文档、数据库线索、上下游服务、第三方调用、关联项目、GitHub、相关网站、官方 API 文档和用户补充路径或 URL，形成有证据来源的需求设计；外部资料默认遵循“官方文档/官网/自有仓库与站点优先，公共 GitHub 与社区资料只作补充”的优先级。已验证可复用的资料位置、数据库、URL、项目路径和侦察经验必须继续通过 `project-memory-rules` 回写长期记忆。
- 来源: 对话确认、`requirement-intake-rules/references/initial-discovery-route.md`
- 适用范围: 需求域
- 更新时间: 2026-06-28
- 状态: 启用

### 需求域第一入口
- 别名: 需求 skill 顺序, 需求前置入口
- 类型: 流程规则
- 定义: 当前对外统一流程为 `Idea/Discovery -> Intake -> 条件闸门 -> 实施计划（含 AC 完成条件） -> 实现 -> 真实测试 -> 6-review -> 交付总结`。其中需求域主流程仍收口到 `Idea/Discovery -> Intake`，条件步骤为 `Gap / Boundary / Splitting / Change`；`implementation-planning-rules` 负责把完成条件、异常边界、停止条件和测试映射冻结在实施计划中。内部统一由 `requirement-intake-rules` 作为第一入口；粗略 idea 进入 `initial-discovery` 路由，主入口负责立即创建需求主文档，`requirement-intake-rules` 的 `gap-routing` 只处理主动侦察后仍无法补齐的关键缺口。需求阶段只允许读仓库、读资料、整理文档；不允许把 agent 猜测写成需求答案，也不允许“先做了再补需求”。需求主文档未真实落盘前，禁止进入实施规划与正式编码。实施计划完成后仍不得自动开工，必须等用户明确“开始实施/开始执行”后才能进入正式编码。
- 来源: `requirement-intake-rules/references/requirement-domain-shared-contract.md`、`编码skill.md`
- 适用范围: 需求域
- 更新时间: 2026-07-22
- 状态: 启用

### 需求临时缺口文档规则
- 别名: gap 临时文档, 缺口阻断文档
- 类型: 流程规则
- 定义: `requirement-intake-rules` 的 `gap-routing` 只处理 discovery 之后仍无法补齐的关键缺口；gap 阶段允许在 `doc/2-需求/` 下创建一份临时缺口文档，记录已侦察证据、待确认问题和阻断结论。用户确认并补齐后，必须先把稳定结论回填主需求文档，再删除临时缺口文档；未确认前不得删除，也不得继续进入实施计划。

### 实施计划完成条件规则
- 别名: AC 完成条件, 计划内验收口径, 真实测试映射
- 类型: 流程规则
- 定义: 完成标准不再单独生成验收 Skill 或验收文档；`AC-*` 继续写入实施总览、实施周期或任务卡，冻结成功条件、异常边界、范围外、停止条件、真实测试入口和证据映射。真实测试逐条引用 AC 并产生 `TEST` 证据，测试完成后由 `code-style-consistency-rules` 记录一次 `STYLE: PASS` 或 `STYLE: FIX_REQUIRED`。
- 来源: `implementation-planning-rules`、`artifact-delivery-gate-rules`、`code-style-consistency-rules`
- 适用范围: 实施域、测试域、6-review 风格回归
- 更新时间: 2026-08-01
- 状态: 启用

### 根测试代码与测试证据双根规则
- 别名: 根 test 目录, 测试资产镜像, doc/5-tests 证据根
- 类型: 测试资产目录规则
- 定义: 根 `test/` 是唯一活动测试代码根，测试程序、mock、stub、fake、fixture、helper 与启动脚本按被测源码或 Skill 目录镜像存放；源码关联模拟程序必须与对应测试使用同一源码相对路径，只有跨源码复用的模拟能力才进入 `test/shared/`；Python 统一使用 `*_test.py`，模拟程序使用 `_mock`、`_stub` 或 `_fake` 后缀。`doc/5-tests/<时间戳>/` 只保存 README、日志、报告、截图与非可执行产物。历史 `doc/5-tests/` 中的可执行资产由指纹清单只读保护，首次修改、改名或新增时才迁至根 `test/`；Go 测试仅在根 `test/` 的 ASCII 外部黑盒包中运行，源码目录禁止 `*_test.go`。
- 来源: `artifact-storage-rules/references/path-map.yaml`、`test/shared/layout_policy.py`、`doc/3-实施/2026-08-01_191658_根test目录统一_实施总览.md`
- 适用范围: 新增测试、测试资产迁移、测试策略、测试程序、真实测试归档和 6-review 目录归位
- 更新时间: 2026-08-01
- 状态: 启用


### 运行时 Mock 目录规则
- 别名: 运行时 Mock, 根 mock 目录, mock 构建标签
- 类型: 目录规则
- 定义: 根 `mock/` 是运行时 Mock 的唯一合法目录，与根 `test/` 对等，按被测源码相对路径镜像；文件必须以 `//go:build mock` 开头，包名约定 `mock_<源包名>`；运行时 Mock 编译进主二进制，替代不可用上游，与测试 Mock 职责分离、互不替代。`go run -tags mock .` 启用。
- 来源: `test-program-rules/references/runtime-mock-pattern.md`、`package-structure-rules/references/project-layout-v2.md`
- 适用范围: 后端运行时 Mock 落点、Go 构建标签、本地开发调试
- 更新时间: 2026-08-08
- 状态: 启用

### 实施开工授权与自动推进
- 别名: 开始实施确认, 开工授权, 最小任务自动推进, 长文本执行边界
- 类型: 流程规则
- 定义: 来源对象文档（需求或 Bug）和实施总览/实施周期即使都已完成，也不构成自动开工授权；必须由用户在当前任务中明确说“开始实施”“开始实现”“开始执行”“直接做”“继续做完”或“按文档实现”，且当前任务已有执行计划、AC 完成条件、任务停止 / 结束条件、最大推进边界和验证点，才允许从实施文档切入正式编码。实施规划阶段默认采用只读计划模式：禁止写代码、禁止边计划边试做，只允许读仓库、定依赖、列风险、拆任务、写实施文档。新项目、项目初期或多来源对象存在多份需求 / 实施文档时，必须先在 `doc/3-实施/` 维护“需求与实施计划全量顺序实施方案”，把需求主文档、实施总览、实施周期和周期内最小任务按总顺序串起来，再进入单来源对象实施总览。计划正文开头必须先写“当前计划最终方案的简要说明”，用 1-3 句先交代推荐方案、主落点和为什么这么做；随后再写 agent 对当前问题的理解，至少交代问题 / 目标、本轮范围、非范围、当前优先闭环和关键假设 / 待确认点，再进入实施周期与最小任务拆分。实施周期是项目第一期、第二期、第三期等大进度单位和顺序边界，必须写清周期顺序、期次定位、进入条件、收口条件和周期内最小任务顺序；真正执行单元是当前周期内的最小任务，并优先按“依赖图 + 垂直切片”组织，避免按前端 / 后端 / 数据库水平分层堆计划。单任务尽量单次专注完成，默认控制在约 5 个文件以内；明显超过则继续拆分。凡是代码生成、修改或重构类任务，都必须显式计划真实测试，写清入口、环境、样本 / 数据来源和通过标准，`build`、`lint`、静态检查不算真实测试；只有纯文档、纯注释、纯排版、纯静态资源改名 / 搬运或不会影响运行结果的场景才允许免测；若计划涉及代码生成、修改或重构，“现状与落点”必须给出代码落点目录树，不能只写文件名或普通条目。若用户在当前轮显式提出“怎么做 / 先给计划 / 先出方案 / 先列步骤 / 这个怎么改”这类计划型问题，也必须先命中实施规划规则；若前置条件未齐，则输出受限计划 / 阻断计划，而不是不触发。若运行环境要求用 `<proposed_plan>` 等专用计划包裹输出，包裹层只负责渲染 / 协议，不能覆盖项目内计划结构；正文仍必须遵守 `implementation-planning-rules` 与模板字段，并在输出前执行 `implementation-planning-rules/references/plan-output-gate.md` 的字段矩阵。Plan Mode 计划正文若以 `Summary`、`Key Changes`、`Public Interfaces`、`Test Plan`、`Assumptions` 等通用工程计划小节作为主结构，或缺少当前计划最终方案简要说明、agent 理解、范围、非范围、当前优先闭环、关键假设、实施周期、阶段计划、最小任务、真实测试、完成条件、停止 / 结束条件、最大推进边界等核心字段，直接判定为无效计划，必须按模板重写，不得解释为简化版计划。受限计划不得作为实施授权；用户即使明确采纳，agent 也只能先补齐缺失前置条件并将其升级为正式执行计划，未升级前禁止进入编码、改码、重构、测试实施或其他执行动作。若用户给出开工类指令但没有计划或任务停止 / 结束条件，必须先补本轮受限计划并停在计划收口处，不得直接实现或进入长文本无限执行。开工后按 `autonomous-execution-rules` 默认遵循“当前实施周期内最小任务A实现 -> 最小任务A真实测试 -> 最小任务A 6-review -> 最小任务B…… -> 当前实施周期收口 -> 下一实施周期”的自动串行闭环；每个最小任务都必须先完成自己的真实测试和 6-review，才允许进入下一个任务；禁止先连续实现多个最小任务后统一测试。
- 来源: `autonomous-execution-rules`、`implementation-planning-rules`、`team-development-rules/references/routing-rules.md`
- 适用范围: 实施域、测试域、6-review 风格回归域
- 更新时间: 2026-07-05
- 状态: 启用

### 代码生成风格入口链路
- 别名: 代码风格契约, 生成代码前风格总控, PROJECT_STYLE 应用入口
- 类型: 流程规则
- 定义: 新增、修改或重构任意代码、脚本、测试支撑代码或配置型代码前，必须先由 `code-generation-style-rules` 读取用户本轮要求、目标文件 / 同目录样例、根目录 `PROJECT_STYLE.md` 和已命中的编码类 skill，形成本轮代码风格契约；如果当前上下文已形成高度统一的局部风格，新增内容只做必要模板替换，不加入多余代码；如果实现已有接口，必须优先查找并参考既有接口实现，记录参考实现或无参考实现的降级依据；后续实现必须按契约落地。`project-style-rules` 继续只维护 `PROJECT_STYLE.md` 长期风格记忆，`code-style-consistency-rules` 基于本轮契约检查局部一致性。
- 来源: 对话确认、`code-generation-style-rules/SKILL.md`、`project-agents-bootstrap/SKILL.md`
- 适用范围: 编码基线域、仓库级规则自举、代码生成与修改
- 更新时间: 2026-07-15
- 状态: 启用

### 长代码块内步骤注释
- 别名: 代码块五行门槛, 长代码块步骤注释, 代码块内步骤注释
- 类型: 代码注释规则
- 定义: 函数/方法体、闭包体和连续控制流代码块按非空行计数（代码行和已有注释行均计入，空行不计），超过 5 行时必须在该代码块内部就近补顶层编号步骤注释；每个超长代码块独立判断，嵌套代码块不能只依赖外层编号，多个步骤按 `1.`、`2.`、`3.` 展开。
- 来源: 用户本轮需求、`comment-completion-gate-rules/SKILL.md`（补齐闸门主 Owner）、`comment-placement-granularity-rules/SKILL.md`（放置与颗粒度辅助 Owner）
- 适用范围: 代码注释、步骤注释、注释放置与颗粒度、代码审查
- 更新时间: 2026-07-16
- 状态: 启用

### 简单检查职责就地表达规则
- 别名: 小函数内联, 避免过度职责拆分, 简单检查不强拆函数
- 类型: 代码可读性规则
- 定义: 职责清晰不等于每个职责都拆成独立函数。极短的局部检查、判空、匹配器取用、scope/flag 选择等逻辑，如果只有一个调用点、无副作用、无复杂分支、无独立测试价值，优先留在当前函数内，并用步骤注释或局部注释补清业务含义；只有复用、稳定业务术语、复杂规则、副作用或独立测试需求成立时才拆函数。
- 来源: 对话确认、`code-readability-rules/SKILL.md`、`code-readability-rules/references/function-structure-rules.md`
- 适用范围: 函数拆分、局部检查、guard 分支、简单匹配逻辑、注释补充
- 更新时间: 2026-07-09
- 状态: 启用

### 后端工具落点分流规则
- 别名: 后端 utils 归位, common/util 归位, IP 工具包归位, utils 与 common/util 区分
- 类型: 包结构/复用规则
- 定义: 后端中可脱离项目独立复制的工具包与 SDK 仅放根 `utils/<package>/`；根 `utils/` 不得有直接文件且不得依赖项目其他包。请求 IP 提取、规范化、公私网判断和国家/地区归属查询适配固定在 `utils/ip/`，不承载代理信任、风控、业务黑白名单或业务地域策略。可引用项目其他包但不承载业务流程的高关联工具函数统一放独立后端根 `common/util/<function>.<ext>`，不得创建子目录；源码根 `util/` 为废弃位置，新代码不得进入。业务域私有辅助继续放 `business/<domain>/util/`；前端工具目录不受此规则影响。
- 来源: 对话确认、`common-util-rules`（公共资格与复用）、`package-structure-rules`（目录落点与依赖方向）
- 适用范围: 后端通用工具、SDK、高关联工具函数、业务域私有辅助归位
- 更新时间: 2026-08-04
- 状态: 启用

### 微业务跨域 JSON RPC 规则
- 别名: 业务域 rpc, 微业务 JSON 通信, 目标域 rpc 公开入口
- 类型: 包结构/业务隔离规则
- 定义: 业务域仅在真实存在跨域调用时创建 `business/<domain>/rpc/`。调用方只能精确导入目标域 `rpc/` 的公开函数，输入和输出均为 JSON 字符串；目标域在自身 `rpc/` 内解析、校验、调用私有层并返回 `Response{code,status,message,data}` JSON。不得导入目标域的 `api/`、`service/`、`entity/`、`base/`、`constant/`、`init/`、`crontask/` 或 `util/`，也不得跨域传递异常、实体、仓储模型或可变业务状态。
- 来源: 对话确认、`package-structure-rules`、`micro-business-architecture-rules`
- 适用范围: 后端微业务目录、跨业务调用、CodeGraph 导入审查、JSON 响应边界
- 更新时间: 2026-07-28
- 状态: 启用

### 通用结束信号
- 别名: 结束即停, 不扩散下一步, 停止建议, 三类合法后续
- 类型: 流程规则
- 定义: 当用户明确表达“结束”“停止”“到此为止”“不要继续”“不要下一步建议”“不要扩散”等结束指令，或不存在三类合法后续时，该指令对 Codex、Claude Code、浏览器 agent、子 agent 或其他长文本 agent 通用；agent 必须停止自动继续、工具执行和扩散性后续建议，只保留必要的最小收口结论。最终收口只允许三类合法后续：原执行计划内未完成必需项、阻断项、用户显式要求的建议/backlog。可选优化、额外整理、未来迭代、体验提升、文档再润色等内容，若不属于原计划必需项，不得作为默认后续内容输出。无下一步时强制不输出“下一步状态”“下一步建议”“等待用户新指令”“无需继续动作”等占位文案，避免循环 loop 会话误触发。Codex goal 仅是运行时状态收口机制的一种特例；若当前环境存在 goal / plan / task 等显式状态机制，且已满足完成或阻断条件，必须按真实机制完成状态收口。
- 来源: `autonomous-execution-rules`、`reasoning-summary-structure-rules`、`skill-execution-compliance-gate-rules`、`AGENTS.md`
- 适用范围: 多 agent 收口、最终总结、连续执行、skill 合规闸门
- 更新时间: 2026-06-29
- 状态: 启用

### 普通 Markdown 输出规则
- 别名: text 代码块禁用, 自然语言不用代码围栏, 输出格式规则
- 类型: 输出规则
- 定义: 普通说明、方案、流程、总结、审查报告、线程拆分和状态回报必须使用普通 Markdown 段落、列表、表格或引用块；不得用 ` ```text `、无语言代码围栏、缩进代码块或 HTML 包裹整段自然语言输出。代码围栏只用于真实代码、命令、配置片段、日志片段、JSON/YAML 等需要等宽保真的内容。最终总结在存在流程、依赖、状态、执行链、跨角色交互或量化结果时，优先在执行证据前输出 1 张、必要时最多 2 张 Mermaid 图形；每张图前写图形目的和关联 ID，图形只表达真实事实并与正文术语一致，简单单点任务不强制造图。该规则由 `reasoning-summary-structure-rules` 负责收口检查，并由 `project-rule-file-bootstrap-rules` 同步进 `AGENTS.md` / `CLAUDE.md` 的“输出格式规则”章节。
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
- 定义: `parallel-task-dispatch-rules` 是并行分类与子代理生命周期的唯一 Owner，不允许停留在“识别出可并行”。本仓库默认处于 subagent 完全授权模式，但系统规则、工具元数据和用户当前轮禁止优先；统一状态机在任务可切分、写集不冲突、风险可控且环境支持时完成真实启动、主路径继续、结果回收和关闭，并核对计划线程数、实际启动数、完成数与关闭数。仅输出线程分配文案、`并行技能` 列表或口头启动说明，不视为真正并行。并行识别不以固定 skill 映射为白名单；项目分析、找 Bug、需求完善侦察、资料/日志/调用链证据收集等任务，只要能拆成独立问题或证据源且不重复读取大段上下文，应优先形成 sidecar 计划并在授权成立时真实委派。单一根因、需求边界、接口契约、schema 或架构方向等最终裁决仍由主 agent 串行负责。
- 来源: `parallel-task-dispatch-rules`、`parallel-task-dispatch-rules/references/task-classification.md`、`parallel-task-dispatch-rules/references/delegation-decision-matrix.md`
- 适用范围: 并行开发、并发审查、项目分析、需求侦察、Bug 分诊、sidecar 子任务分发
- 更新时间: 2026-06-30
- 状态: 启用

### 子 agent 启动计划脚本
- 别名: generate_subagent_plan, 批量委派计划, 中文任务名子 agent
- 类型: 工具规则
- 定义: `parallel-task-dispatch-rules` 在批量委派前按需运行 `parallel-task-dispatch-rules/scripts/generate_subagent_plan.py` 生成结构化启动计划。脚本只负责输出计划 JSON，不直接调用平台工具；真实启动仍由主 agent 读取计划后调用 subagent / multi-agent / thread 工具。脚本生成的 `agent_name` / `logical_agent_name` 默认使用“任务简要中文 + 线程标识”，用于主 agent 侧的中文逻辑命名与计划线程数核对；平台 UI 实际昵称仍以启动工具返回值为准。
- 来源: `parallel-task-dispatch-rules`
- 适用范围: 批量子任务委派、并行线程规划
- 更新时间: 2026-06-29
- 状态: 启用

### 子 agent 生命周期与终局对账
- 别名: close_agent 回收, 子代理关闭, 已完成子线程释放, 终局扫描, 未关闭告警
- 类型: 流程规则
- 定义: `parallel-task-dispatch-rules` 对当前会话全部非根 agent 执行进入前预检、批次回收和最终回复前终局扫描。完成、失败、取消、中断和放弃均不等于关闭；只有真实关闭或平台契约明确的等价资源释放成功且关闭后重新枚举不再活跃，才计入关闭数。平台没有真实关闭能力时只记录未关闭告警并禁止下一批，不得伪报全部关闭。统一对账保留计划线程数、实际启动数、完成数、关闭数，并新增终态数、终局扫描数、仍活跃数、未关闭数和告警原因。
- 来源: `parallel-task-dispatch-rules`
- 适用范围: 所有真实子 agent / 并行代理执行场景
- 更新时间: 2026-07-25
- 状态: 启用

### 6-review 风格回归收口
- 别名: 风格回归链路, 6-review
- 类型: 流程规则
- 定义: 活动质量回归只保留测试后的 `code-style-consistency-rules` `6-review`；检查格式、命名、注释、日志、可读性、目录归位和局部习惯，输出 `STYLE: PASS` 或 `STYLE: FIX_REQUIRED`。不判断业务正确性、需求覆盖或发布放行，结果记录到 `doc/6-review/`。
- 来源: `README.md`、`项目设计.md`、`code-style-consistency-rules`
- 适用范围: 6-review 风格回归、交付收口
- 更新时间: 2026-08-01
- 状态: 启用

### 共享静态 Owner 路由与可选监控消费者
- 别名: 共享 Owner 路由, 静态来源映射, 监控代码消费者
- 类型: Skill 治理规则
- 定义: `code-style-consistency-rules/scripts/static_owner_router.py` 与 `references/static-owner-source-map.json` 是共享静态 Owner 路由的唯一 Owner。测试后的 `6-review` 从该路由选择风格子集；`continuous-code-quality-supervisor-rules` 仅在 Goal active 且用户明确要求“监控代码”时条件式消费完整路由，继续负责扫描、脱敏、finding 指纹、去重和通知。监督器不得复制 Owner 常量、条件路由或来源映射，且不构成 `6-review` Gate。
- 来源: `code-style-consistency-rules/scripts/static_owner_router.py`、`code-style-consistency-rules/references/static-owner-routing-contract.md`、`continuous-code-quality-supervisor-rules/SKILL.md`
- 适用范围: `6-review` 风格回归、条件式持续代码监控、共享路由维护
- 更新时间: 2026-08-01
- 状态: 启用

### Git 提交基础质量闸门
- 别名: 提交前质量检查, Git 基础质量核查, 提交不生成活动流程文档
- 类型: 流程规则
- 定义: 执行 `git commit` 前，必须直接对当前 staged 改动完成基础质量核查：格式、注释、安全性、并发安全性、系统崩溃风险、边界条件和测试/功能验证适用性均须通过或明确“不适用 + 原因”。结论只写入 Git 提交证据；不因提交自动生成活动审查/验收文档。活动风格结果统一由 `6-review` 记录。
- 来源: 当前对话确认、`git-collaboration-rules/SKILL.md`、`code-style-consistency-rules`
- 适用范围: 提交流程、6-review 风格回归
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
- 别名: 提交域隔离, 同一任务文档合并提交, docs/test/实现分离
- 类型: 流程规则
- 定义: `提交git` 允许拆成多次提交清空工作区，但每个 commit 默认只承载一个提交域。同一任务的需求、实施、Bug、测试说明、6-review、验收和项目状态同步文件统一归入一笔 `docs` 提交；`doc/5-tests/**` 只保存说明、日志、报告、截图和非可执行证据。根 `test/**`、`*_test.*`、`*.spec.*`、`*.test.*` 等可执行测试独立归入 `test` 提交；代码实现 / 运行配置独立归入 `feat` 或 `fix` 提交，不与 `docs` 或 `test` 混提。历史 `doc/6-审查/`、`doc/7-验收/` 只读兼容，根目录 `README.md` 改动日志可以跟随对应 commit 一起更新，但不单独构成提交域。
- 来源: 对话确认、`git-collaboration-rules/SKILL.md`、`git-collaboration-rules/scripts/pre_commit_gate.sh`
- 适用范围: 提交流程、需求域、实施域、Bug 域、测试域、6-review 风格回归
- 更新时间: 2026-08-02
- 状态: 启用

### 文档落盘闸门
- 别名: 归档闸门, 收口前落盘检查
- 类型: 流程规则
- 定义: 需求、实施、Bug、测试和 6-review 任务在最终收口前必须联动 `artifact-delivery-gate-rules`，核对主文档、正文内嵌 Mermaid 图示、README、需求与实施计划全量顺序实施方案、实施总览/实施周期、6-review 文档和证据路径是否已经真实落盘到 `doc/2-需求/`、`doc/3-实施/`、`doc/4-bugs/`、`doc/5-tests/`、`doc/6-review/`；实施域还必须核对新项目 / 多来源对象总顺序、周期顺序、期次定位、周期内最小任务顺序和已执行最小任务的实现 / 真实测试 / 6-review 状态，未落盘或缺闭环状态不得判定任务完成。
- 来源: `artifact-delivery-gate-rules`、`README.md`
- 适用范围: 需求域、实施域、Bug 域、测试域、6-review 风格回归
- 更新时间: 2026-07-05
- 状态: 启用

### 需求与实施文档极致完整性契约
- 别名: 零决策文档交接, 极致完整性, 普通模型执行契约, 文档质量 profile
- 类型: 文档质量规则
- 定义: 需求、实施总览、实施周期和最小任务文档采用“结构完整、条件字段显式、决策冻结、图文一致、双向追踪、机器校验”的共同契约。所有条件字段必须填写，或使用 `N/A + 原因 + 证据`；实施计划持有 AC 完成条件、异常边界、停止条件和测试映射。普通模型不得自行补业务、技术、测试、回滚或停止决策。稳定追踪链固定为 `SRC -> DEC -> REQ/RULE -> AC -> CYCLE -> TASK -> 文件/符号 -> TEST -> EVIDENCE`。需求按复杂度 L1-L4 展开；L2 及以上按语义强制流程图、时序图及必要状态/数据/依赖图；实施总览、周期和任务卡分别承载整体决策、周期顺序和零决策执行动作。
- 来源: `requirement-intake-rules/references/extreme-completeness-standard.md`、`implementation-planning-rules/references/implementation-overview-template.md`、`implementation-planning-rules/references/implementation-cycle-template.md`、`implementation-planning-rules/references/minimum-task-execution-contract.md`、`artifact-delivery-gate-rules/references/document-handoff-contract.md`
- 适用范围: 需求域、实施域、交付闸门
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

### 历史审查与验收归档边界
- 别名: 历史只读归档
- 类型: 文档边界
- 定义: `doc/6-审查/` 与 `doc/7-验收/` 的既有文件原文只读保留，历史链接可继续读取；活动流程不再新增、更新或依赖这些目录。
- 来源: `artifact-storage-rules`、`code-style-consistency-rules`
- 适用范围: 历史资料、6-review 活动边界
- 更新时间: 2026-08-01
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
- 定义: 当前 Codex / Claude / agent 会话进入明确需求、Bug、实施、审查、测试、提交、规则更新，或用户提问后已经能稳定归纳出中文任务主题时，且标题为空泛、过时、泛称或不匹配当前任务时，必须自动命中 `thread-title-rules`；goal 创建、goal 恢复、上下文压缩续做、长任务阶段切换或执行阶段主题稳定时，也必须在过程中尽早判定是否改名，不等待最终总结。由 agent 生成 8-24 字中文简要标题，并按真实工具能力更新当前会话标题。Codex App 优先调用只接收 `title` 的统一 MCP 工具 `rename_current_thread`，由工具从可信 MCP 元数据识别当前任务；首次 `INVALID_TITLE` 只允许修正后重试 MCP 一次且第二次失败直接跳过，MCP 未暴露或首次调用的其他失败时，仅在真实存在可直接作用于当前会话的 `set_thread_title` 时回退一次，MCP 成功后不得重复调用。禁止通过 `list_threads`、`cwd`、最近更新时间、preview 或标题相似度猜测当前会话。其他宿主只按真实工具发现结果执行，不按模型名称推断能力；标题已准确、用户明确禁止、主题不稳定或只是最小任务内部小步骤推进时跳过，禁止伪造工具调用或猜测结果宣称成功。
- 来源: 用户本轮确认、`thread-title-rules/SKILL.md`、`thread-title-rules/references/rename-tool-contract.md`
- 适用范围: Codex App 会话管理、任务检索、总控层自动触发、模型无关工具路由
- 更新时间: 2026-07-22
- 状态: 启用

### Obsidian 知识流选择性默认触发链
- 别名: obsidian-knowledge-flow, Obsidian 知识流, 选择性默认触发, 知识库检索沉淀
- 类型: 流程规则
- 定义: 项目启动先按“父目录平台规则 -> `PROJECT_CURRENT.md` -> `PROJECT_MEMORY.md`”读取项目本地四件套；`PROJECT_CURRENT.md` 覆盖维护当前状态且不超过 51,200 字节，`PROJECT_MEMORY.md` 只承载稳定规则与关键决策，`PROJECT_HISTORY.md` 追加关键事件并只保留最近 20 条（自动裁剪、按日期倒序）且普通启动不读。Obsidian 仍固定使用 `D:\obsidian_data` 及其 `知识库/` 工作区，仅当问题依赖跨项目历史、vault 知识或既有笔记时判定为 `检索` 并通过 CLI 检索 / 读取；仅当收口形成可复用知识时判定为 `沉淀` 并先通过 CLI 检索已有承接笔记。执行失败案例统一落到 `知识库/20-Knowledge/execution-failure-cases/<owner>/`，保留脱敏正反例、验证证据和追加式状态事件；只有 active 且 scope 精确匹配时自动复用。普通任务记录 `不适用`，CLI 或 vault 不可用时记录 `阻断`，不得直接文件读写 vault 作为 fallback；项目本地 Markdown 与 vault 链路不得混用。
- 来源: `AGENTS.md`、`CLAUDE.md`、`skill-hit-check-rules/SKILL.md`、`obsidian-knowledge-flow/SKILL.md`、`编码skill.md`
- 适用范围: 记忆域、命中检查、阶段收口、最终总结、Obsidian vault 知识检索与沉淀
- 更新时间: 2026-08-05
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
- 定义: 父目录 `AGENTS.md` / `CLAUDE.md` 只保存跨项目通用规则；项目根目录 `PROJECT_CURRENT.md` 保存当前任务交接信息并覆盖维护，`PROJECT_MEMORY.md` 保存稳定项目规则、关键决策和少量长期事实，`PROJECT_HISTORY.md` 追加关键历史事件并只保留最近 20 条（自动裁剪、按日期倒序）。新项目、新任务、新会话或上下文压缩恢复时，固定先读取父目录当前平台规则，再读取 current 和 memory；history 只在历史追问、状态不足或真实卡点时窄读。项目本地文件使用标准工具，Obsidian vault 仍只通过 CLI 选择性检索和沉淀。
- 来源: 用户本轮确认、`obsidian-knowledge-flow`、`project-memory-rules`、`project-agents-bootstrap`
- 适用范围: 项目启动、上下文交接、记忆更新、Obsidian 边界
- 更新时间: 2026-08-05
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
- 定义: 当用户提供任意 URL、链接或网页地址，并要求打开、读取、分析、总结、截图、提取内容、排查页面、查看文档、理解网页、检查资料、访问在线文档或处理已在浏览器登录过的页面时，默认优先触发 `authenticated-url-routing-rules`，并优先使用 `chrome:control-chrome` 接管用户已登录的真实 Chrome profile，复用登录态、扩展、权限和已打开标签页。依赖真实 Chrome profile 的页面在 Chrome Plugin 不可用时停在连接/授权阻断，不得用本地自动化或 Browser Use Cloud 绕过；明确为公开或 local 且不依赖用户 profile 的页面，才按统一矩阵选择 Chrome DevTools MCP、`browser-session-automation-rules` 或高级验证 Skill。只有云端自主长链、托管并发、地域出口、托管代理、隐身、合规验证码等 Cloud 专属需求，或用户明确点名 Browser Use Cloud 时，才转交 `browser-use-cloud-rules`。遇到登录页、权限页、验证码、人机验证或正文安全策略阻断时，不得用 Cloud、搜索结果、第三方转载或其它浏览器绕过权限。
- 来源: 用户确认、`authenticated-url-routing-rules/SKILL.md`
- 适用范围: URL 分析、在线文档读取、浏览器权限页面、企业系统资料访问
- 更新时间: 2026-07-26
- 状态: 启用

### Browser Use Cloud 收费与安全路由
- 别名: browser-use-cloud-rules, BROWSER_USE_API_KEY, Cloud 浏览器
- 类型: 浏览器路由规则
- 定义: Browser Use Cloud 只用于云端自主长链、托管并发、地域出口、托管代理、隐身或服务商提供且站点允许的合规验证码处理，不接本地开源 Browser Use，也不替换 Chrome Plugin、应用内 Browser、Chrome DevTools MCP 或本地 agent-browser。每次 `run_session`、`send_task` 前都只从本机 `BROWSER_USE_API_KEY` 检查凭据存在性，查询 Billing，验证当前动作的可写 `inputSchema.properties.maxCostUsd`，展示任务、profile、代理、地域、录制、`keep_alive=false`、余额和费用上限，并取得当次明确确认；免费层也不能跳过。无硬费用上限默认停止。完成、失败或取消后读取 session，活跃时固定 `stop_session(strategy="session")`，只有最终 `status="stopped"` 且 `totalCostUsd` 为非负有限值才算收口。
- 来源: `browser-use-cloud-rules/SKILL.md`、`mcp-installation-rules/references/tool-priority.md`、`doc/7-验收/2026-07-26_063000_REQ-BU-20260726-001_验收标准.md`
- 适用范围: Browser Use Cloud 路由、收费动作、密钥提醒、session 生命周期
- 更新时间: 2026-07-26
- 状态: 启用

### 结果与结论适中详细度契约
- 别名: reasoning-summary-structure-rules, 结果区 3–5 句, 适中详细结论
- 类型: 最终总结输出规则
- 定义: `reasoning-summary-structure-rules` 的结果区默认用 3 个简短句子依次回答本次解决的问题、采用的方法以及结果/验证状态；复杂、受限或存在关键边界时，只有在事实需要时扩展到第 4–5 句说明范围边界、残留卡点或验证限制。不得用“已完成”等空泛状态词替代核心信息，也不得复制命令、完整测试清单、逐文件改动或执行流水账；该契约不改变既有总结章节顺序、图形化条件、`WAITING_DECISION` 阻断和任务阻断收口 Owner。
- 来源: `reasoning-summary-structure-rules/SKILL.md`、`reasoning-summary-structure-rules/references/conditional-sections-rules.md`、`reasoning-summary-structure-rules/references/output-examples.md`、`doc/7-验收/2026-07-26_162000_REQ-SUMMARY-DETAIL-001_最终验收.md`
- 适用范围: 最终回复、审查/验收收口、复杂度与边界驱动的结果区详细度
- 更新时间: 2026-07-26
- 状态: 启用


- 构造/装配：`mock/` 下的包可正常导入 `internal/...`；但 module 根（如 `main.go`）不能直接导入 `mock/internal/...`，必须通过 `mock/assembly` 装配层转发，否则 Go internal 可见性规则拒绝编译。
- 工厂模式：推荐 `main_real.go`（`//go:build !mock`，生产实现）+ `main_mock.go`（`//go:build mock`，调用 `mock/assembly`）双文件装配；多工厂场景使用 `internal/factory/` 统一装配。
- 真实项目 F:\binance-wangge-go 已迁移：`internal/business/scalp/api/mock_gateway.go` 保留测试 Mock（`MockGateway`、`NewMockGateway`），运行时 Mock 迁至 `mock/internal/business/scalp/api/gateway_mock.go`（包名 `mock_api`），`main_real.go`/`main_mock.go` 双文件工厂，`.vscode/launch.json` 新增 mock 调试模式。
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
- 2026-06-27：曾将独立 Discovery Skill 设为需求域第一入口；当前稳定口径已迁移为 `requirement-intake-rules#initial-discovery`，四个需求 Owner 保持独立，通过条件路由与 reference 收敛职责重叠。
- 2026-06-27：新增统一文档落盘闸门，明确需求、Bug、测试、审查收口前必须先核对正式文档已真实落盘；同时取消审查域“轻量通过可不落盘”的旧口径。
- 2026-06-27：补充“中间链路也必须过文档落盘闸门”的长期口径，并明确提交级专项审查正式归档到 `doc/6-审查/`，不再写项目根目录固定文件名。
- 2026-06-28：明确“需求/验收标准/实施计划完成不等于自动开工”，必须等用户明确“开始实施/开始执行”后才能进入编码；一旦开工，后续按实施周期自动串行推进实现、测试、审查与验收闭环。
- 2026-06-30：统一实施执行口径为“最小任务闭环优先于实施周期浏览”；2026-08-01 起主执行链更新为“实施计划完成条件 -> 实现 -> 真实测试 -> 6-review”。
- 2026-06-29：将实施执行粒度从“实施周期闭环”细化为“最小任务闭环”；实施周期继续作为文档管理容器，当前执行顺序为每个最小任务依次满足实施计划完成条件、实现、真实测试和 6-review 后再进入下一个最小任务。
- 2026-06-29：补充长文本执行边界；“开始实施/开始实现/开始执行/直接做/继续做完/按文档实现”等开工词必须有执行计划、任务完成条件、任务停止 / 结束条件和最大推进边界，缺少时先补受限计划并停在计划收口处，不得直接实现。
- 2026-06-29：建立并行规划与真实启动闭环；2026-06-30 补充工具授权优先级；2026-07-22 收敛为 `parallel-task-dispatch-rules` 单一状态机，统一分类、授权、启动、观测、回收与关闭，不能只停留在文本规划。
- 2026-06-29：新增 `generate_subagent_plan.py` 启动计划脚本，明确批量委派先生成计划 JSON，再由主 agent 读取计划并真实启动；子 agent 名称默认使用任务简要中文。
- 2026-06-29：补充子 agent 生命周期口径，明确中文任务名属于主 agent 逻辑名，平台 UI 昵称由启动工具返回；结果收回后仍必须调用 `close_agent` 完成回收。
- 2026-06-30：扩展并行识别口径，明确并行不再依赖固定 skill 映射白名单；主 agent 在项目分析、找 Bug、需求完善侦察、证据收集等任务中必须自主识别可委派的只读 sidecar 子任务并优先尝试真实 subagent 并行。
- 2026-06-30：修正 subagent 自动启动口径，明确自动的是委派判定；真实启动必须服从当前工具元数据和授权策略。若工具要求用户显式授权，先检查当前轮授权与项目级完全授权；仅两者均不存在时，才回退本地执行并记录实际启动数为 0。
- 2026-06-30：根据用户确认启用 subagent 完全授权模式；项目级 standing authorization 视为满足工具显式授权条件，不再因缺少逐次 subagent 指令而回退本地执行。
- 2026-07-25：补充子 agent 三段生命周期扫描、关闭后复查和数量对账规则；`interrupt_agent`、完成通知和停止采样不计关闭，平台无真实关闭工具时仅告警并阻止下一批。
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
- 2026-07-05：明确实施周期是第一期 / 第二期 / 第三期等大进度与顺序边界；2026-08-01 起，周期内每个最小任务都满足“实施计划完成条件 -> 实现 -> 真实测试 -> 6-review”后才进入下一任务 / 下一周期，文档落盘记录周期收口与最小任务闭环证据。
- 2026-07-13：完成 Obsidian Windows/WSL bridge-only 固定执行边界与 CYCLE-OBS-02 实机收口；唯一 vault 根为 `D:\obsidian_data`，WSL 通过 PowerShell interop，长正文和 append 必须以 CLI readback/hash 证明一致，未使用 vault 文件系统 fallback。
- 2026-07-05：新增新项目 / 多来源对象的“需求与实施计划全量顺序实施方案”口径，要求先用项目级总表串起需求、验收标准、实施总览、实施周期和周期内最小任务，再进入单来源对象执行。
- 2026-07-02：新增文件写入统一 UTF-8 口径，明确代码、文档、配置、脚本、测试资产和生成文本跨 Windows / WSL / Linux 默认 UTF-8，禁止 GBK / ANSI / 默认编码落盘，命令行写入后必须回读并检查 diff。
- 2026-07-02：新增会话自动重命名规则，明确任务主题稳定且标题泛化、过时或不匹配时自动命中 `thread-title-rules`，调用真实线程重命名工具改为 8-24 字中文简要；标题已准确、工具不可用或用户禁止时跳过。
- 2026-07-03：补充会话自动重命名平台能力矩阵，明确 Codex 优先用 `set_thread_title`，Claude Code 仅在存在真实改名工具时执行，Claude Desktop 默认显式跳过，`CLAUDE.md` 不等同于 Desktop 已具备自动改名能力。
- 2026-07-02：新增 URL 认证浏览器默认路由，明确用户提供 URL 时默认优先通过 Chrome Plugin 复用用户真实 Chrome 登录态，避免隔离浏览器或 `web` 丢失权限；补充 Chrome 安全策略拒绝正文读取时只报告阻断事实并 handoff，不做绕过；执行中已确认解决的问题必须继续回灌到 skill。
- 2026-07-12：收敛浏览器工具路由：用户真实 Chrome profile 只由 Chrome Plugin 接管；公开或 local 页面按 Chrome DevTools MCP 与 `agent-browser` 能力路由；`agent-browser` 保留为隔离 session、网络/HAR、视觉 diff、录制/trace、代理和多引擎等条件能力，不再作为前后端联调默认强制工具。
- 2026-07-26：新增 Browser Use Cloud 条件路由，只接云端自主长链、托管并发、地域出口、托管代理、隐身或合规验证码专属场景；逐次收费动作执行 key、Billing、硬费用上限和人工确认，结束后销毁遗留 session 并回读实际费用，免费层也不例外。
- 2026-07-26：完成 `REQ-SUMMARY-DETAIL-001` 结果与结论详细度切片；简单任务结果区固定 3 句，复杂、受限或有关键边界时按事实扩展至 4–5 句，始终覆盖问题、方法和结果/验证状态，禁止空泛状态词和流水账；专项回归 9/9、Skill 校验、工程文档 strict、审查与最终验收通过，未执行 Git 历史写入。
- 2026-07-02：补充项目内文件引用路径规则，明确 Windows 桌面访问 WSL 项目时，所有面向用户的项目内文件引用都用 `\\wsl.localhost\...`，`/home/...` 仅保留给 WSL 命令与日志上下文。
- 2026-07-02：更新上线接口测试门禁规则，新增项目基线资产库、参数依赖解析、可复用参数生命周期、失效持续更新和通用脚本复用优先口径。
- 2026-07-02：新增 Swag OpenAPI 全量维护规则，明确 `swag/` 为唯一正式输出目录，单接口完整 YAML、总 YAML 与 `.swag-manifest.yaml` 持续维护。
- 2026-07-02：补充上线测试与 Swag OpenAPI 双索引同步规则，明确 `swag/.swag-manifest.yaml` 与 `doc/5-tests/基线/interface-inventory.yaml` 理论上都不应缺失；任一缺失或三方接口集合不一致时，从当前代码刷新 swag 与测试基线两边。
- 2026-07-03：收紧 Swag OpenAPI 导入口径，明确单接口 YAML 导入 Apifox 时默认直入目标目录，不通过 `tags` 额外创建父目录；头部、请求参数、响应字段都必须有中文说明，源码注释不足时只允许受控推导。
- 2026-07-03：补充单接口 Swag 文件命名规则，默认采用“路径名 + 中文简要说明”格式；中文说明优先取显式 `summary`，缺失时允许受控推导，仍无法稳定得到时回退纯路径文件名并在 manifest 记录 `summary_source: unresolved`。
- 2026-07-03：补充单接口 Swag 中文简介清洗规则，明确文件名后缀必须去掉 `1.`、`11.`、`（1）`、`【1】` 等数字前缀和无业务意义特殊符号，只保留接口中文简介本体。
- 2026-08-01：历史审查链退役，注释、格式和目录归位改由测试后的 `6-review` 风格回归核对；缺失统一输出 `STYLE: FIX_REQUIRED`。
- 2026-07-03：补充会话自动重命名执行细节，明确 Codex 下若首屏未直接暴露 `set_thread_title` / `list_threads`，必须先通过 `tool_search` 发现线程工具，再识别当前会话并执行改名；未做工具发现不得直接记为“工具不可用”。
- 2026-07-05：会话自动重命名补充“阶段+提问”策略，要求用户提问、goal 创建 / 恢复、上下文压缩续做和长任务阶段切换时在过程中尽早判断标题，不等最终总结；标题已准确或仅小步骤推进时跳过。
- 2026-07-05：新增代码生成风格入口链路，明确新增、修改或重构代码前必须由 `code-generation-style-rules` 读取 `PROJECT_STYLE.md` 与局部样例，形成本轮代码风格契约。
- 2026-07-16：按用户要求升级注释双 skill，明确超过 5 行有效代码的函数/方法体、闭包体和连续控制流代码块必须在块内就近补顶层步骤注释，嵌套超长代码块单独判断。
- 2026-07-17：完成 Skill 体积治理与职责拆分周期 01。确认 84/111/27 统计口径、冻结候选矩阵并完成五类通用测试入口；当前改动总审查通过，TASK-SPLIT-01-03 验收通过，周期 01 收口但不进入周期 02，真实 skill、字典和 Git 历史保持未修改。
- 2026-07-08：新增工具落点分流 util/common/util 规则，明确项目无关工具归 `util`，引用项目文件、路径、配置或约定的复用工具归 `common/util`。
- 2026-07-06：修正“项目内文件引用路径”规则的表述边界。用户反馈实际输出中仍出现 `/home/...` 裸路径，排查发现 `windows-wsl-execution-rules/SKILL.md`、`path-mapping.md`、`recommended-workflow.md`、`command-templates.md` 和本文件的“Windows / WSL 执行边界”词条，都把这条规则的表述挂在“agent 在 Windows”分支下；当 agent 实际直接运行在 WSL 内（情况一）时容易被误读为不适用。已改写为独立于 agent 运行位置的规则，并在“Windows / WSL 执行边界”词条中拆出交叉引用，避免两条规则的适用条件混读。
- 2026-07-06：新增“WSL 工具 PATH interop 误用排查”词条。用户反馈在 WSL 内执行命令时被解析成 Windows 打包的 `rg`，报 permission denied；补充根因（`appendWindowsPath` 导致 PATH fallthrough）、排查命令（`command -v`）、修复优先级（原生装包优先，不默认改 `/etc/wsl.conf`），并新增“新会话首次进入 WSL 项目时一次性自检”的建议（经用户确认，力度介于纯文档和自动化脚本之间）。
- 2026-07-08：新增 Git 协作联动 Obsidian 沉淀规则，明确提交 / 推送 / PR 收口形成可复用事实时先检索并沉淀，但沉淀不构成提交授权。
- 2026-08-05：`PROJECT_HISTORY.md` 由“只追加”改为“追加并只保留最近 20 条”（按日期倒序、新事件置顶、追加后自动裁剪、被裁事件不归档）；同步 `project-memory-rules`、bootstrap 资产、`AGENTS.md` / `CLAUDE.md` 与机器索引口径。

### 上线接口测试门禁规则
- 别名: project-release-test-rules（历史名，已拆分）, project-interface-baseline-rules, project-interface-release-execution-rules, 上线测试门禁
- 类型: 测试域核心规则
- 定义: 上线前项目级全接口测试门禁，替代人工接口回归验证，输出上线准入结论。每个业务项目必须在 `doc/5-tests/基线/` 长期维护接口清单、参数来源、依赖图、可复用参数、场景目录、脚本适配、执行历史和变更日志；同时将 `swag/.swag-manifest.yaml` 与 `doc/5-tests/基线/interface-inventory.yaml` 作为当前代码接口事实的双索引，任一缺失、陈旧或接口集合不一致时，先刷新 swag 与测试基线两边。若目标接口参数无法直接确定，agent 必须按 `reusable_param -> upstream_api -> local_database -> local_cache -> openapi_example -> fixture -> rule` 解析，并把来源写入依赖追踪；已测试通过的参数可持续复用，但必须有 `candidate/reusable/stale/invalid/quarantined/retired` 生命周期、复验、失效归因和持续回写机制。已有通用脚本能力优先复用，缺能力时扩展 `project-interface-release-execution-rules/scripts/generate_release_test_plan.py` 的通用子命令，不为每次上线重复生成一次性脚本。
- 来源: `project-interface-baseline-rules/SKILL.md`、`project-interface-baseline-rules/references/baseline-asset-rules.md`、`project-release-test-rules/scripts/generate_release_test_plan.py`
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

## Skill 体积治理与职责拆分

- 稳定统计口径：正式字典主规划有 84 个 skill，磁盘有 111 个带 `SKILL.md` 的目录，其中 27 个属于扩展种子，不纳入正式预算基线；默认文本包按 `SKILL.md` 与直接 references 文本字节数统计。
- 稳定测试契约：通用入口覆盖 `size`、`mapping`、`trigger`、`pre-delete`、`post-delete` 五类模式；报告和矩阵路径不得越出仓库根目录，fixture 根不得越出当天测试时间戳目录；越界必须非零失败且不得删除真实 skill。
- 当前状态：2026-07-17 已完成周期 01 的三个最小任务；2026-08-01 起闭环口径统一为“实施计划完成条件 -> 实现 -> 真实测试 -> 6-review”。周期 01 已收口，周期 02 尚未进入，真实 skill、字典和 Git 历史保持未修改。
- 证据来源：需求、验收、实施总览、实施周期 01、测试 README、当前改动审查报告和 `validate_skill_split.py` 的本地验证结果。
- Obsidian 沉淀：`知识库/20-Knowledge/codex-skills/skill-体积治理与职责拆分计划.md`，并已通过 bridge 更新 `知识库/INDEX.md` 导航入口。
- 更新时间：2026-07-17。

## 需求与实施文档极致完备化规则

- 需求、验收、实施总览、实施周期和最小任务卡均采用 Markdown + YAML front matter；复杂度为 L2 及以上时，按语义提供 Mermaid 流程图和时序图，L3/L4 追加状态、数据、依赖或故障图。
- 高推理模型冻结业务、技术、测试、回滚、停止和异常决策；普通模型只能按 `REQ -> AC -> PLAN -> CYCLE -> TASK -> TEST -> EVIDENCE` 追踪链执行，不得补默认值或猜测未决决策。
- 每个最小任务必须唯一归属一个实施周期，并完成“实施计划完成条件 -> 实现/落盘 -> 真实测试或有证据的免测 -> 6-review”闭环；缺少任一证据时不得把状态写为已完成。
- `artifact-delivery-gate-rules` 是文档质量唯一机器门禁；profile、严格追踪、N/A 理由、失效链接、Mermaid 语法和 UTF-8 检查失败时必须回开上游文档。
- 实施规划使用单来源实施总览和项目级全量顺序实施方案两层入口；周期状态、任务状态、项目当前状态、真实测试和 6-review 状态必须同步，不能保留已被后续事实超越的旧入口状态。

## Windows PowerShell 环境自动迭代规则

- `windows-powershell-environment-rules` 的新会话入口是 `initialize_windows_powershell.ps1 -Mode SessionEnsure`；通过用户级 TTL marker 和原子锁避免重复准备，Apply journal 不完整时写 `complete=false`，不得伪造健康状态。
- Windows PowerShell 命令缺失统一经 `recover_windows_command.ps1` / `RecoverCommand` 路由；canonical manifest 或显式精确 `PackageId` 才能安装，未知命令不执行 `winget search` 猜包。
- 安装并真实版本探针验证成功的非 canonical 工具写入用户级 `discovered-tools.json`，仅 `verified=true` 且通过 ID/命令/source 白名单的记录在后续会话合并读取；canonical `tool-manifest.yaml` 不运行时修改。
- 失败摘要写入用户级 `failure-cases.json`，必须 UTF-8、原子替换、去重、限长、脱敏；PowerShell Windows owner 与 WSL 原生 shell/`127` owner 分离。
- 当前 runtime 不提供任意 agent shell 调用的全局失败拦截；自动恢复范围仅限显式 wrapper 或未来接入 runtime hook 的路径。

- 2026-07-21：六域 Skill 精简采用“单主入口 + 条件路由”；需求 discovery 已迁移到 `requirement-intake-rules` 的 `initial-discovery`，自动触发、local 安全、证据、记忆回写、输出和停止边界保持不变。

## 总控层单向路由与合并规则

- 稳定决策：`skill-hit-check-rules` 是每轮唯一首入口；它只确认联动，不复制 Git、失败恢复、并行或 Skill 资产 Owner 的执行细则。
- 稳定决策：`parallel-task-dispatch-rules` 是并行分类与子代理生命周期的唯一 Owner，一次状态机完成串行/条件并行/可并行判定、上下文成本、互斥写集、系统能力与授权、真实启动、主路径继续、结果回收、关闭和回退；计划、启动、完成、关闭数量必须可核对。
- 稳定决策：`project-rule-file-bootstrap-rules` 是项目自举唯一 Owner，内部保留 `rule-bootstrap` 与 `memory-bootstrap`；规则文件非受管内容、UTF-8、`PROJECT_CURRENT.md` 51,200 字节、机器索引和 `PROJECT_HISTORY.md` 追加后只保留最近 20 条（自动裁剪）均为保护语义。
- 稳定决策：压缩恢复先执行共享 `context-recovery-contract`；只有 `recent_context_state=missing` 才条件调用 `recent-context-bootstrap-rules`，新会话预热、压缩恢复和明确历史回忆三个入口保持独立。
- 稳定决策：注释细则由注释 Owner 定义，上层审查和收口只消费 PASS/FAIL、缺口与证据；执行合规和代码收口只产生状态，不重复定义最终 Markdown；`reasoning-summary-structure-rules` 唯一渲染阻断、合法后续和无下一步收口。
- 稳定决策：退役总控 Skill 前必须有 protected semantic mapping、trigger fixtures、active consumer 清零、physical asset owner、baseline tree、rollback locator、生命周期证据和 post-delete PASS；失败候选保持 HOLD，不为目标数量强删。
- 来源：`doc/2-需求/2026-07-22_223221_总控层Skill精简合并与单向路由.md`、`doc/5-tests/2026-07-22_223221/control-plane-streamlining/`。
- 更新时间：2026-07-22。

## 代码位置目录规则 V2

- 稳定决策：`package-structure-rules` 是三类项目的代码位置、查找与引用唯一 Owner；人工目录树、JSON 兼容 YAML Catalog、CLI 和相邻 Skill 必须保持一致。
- 稳定决策：后端项目无关、可独立复制的技术工具、SDK 和服务注册发现统一位于项目根 `utils/<package>/`；`utils/` 仅允许工具包子目录且不得直接存放文件，服务发现只允许 `utils/discovery/polaris/`、`utils/discovery/nacos/`，不得使用 `infrastructure/`、根 `util/`、`utils/graphql/`、`utils/asyncapi/`、`utils/avro/` 或 `utils/api/http/`。需要引用项目其他包但不承载业务流程的高关联工具统一位于独立后端 `common/util/`，直接存放当前语言文件且禁止子目录；源码根 `util/` 为废弃位置。
- 稳定决策：前后端同仓、独立后端和独立前端项目根都直接保存 `AGENTS.md`、`CLAUDE.md`、`PROJECT_CURRENT.md`、`PROJECT_MEMORY.md`、`PROJECT_HISTORY.md`；`PROJECT_STYLE.md` 是条件文件。`AGENTS.md` 与 `CLAUDE.md` 正文必须一致，分别供 Codex 与 Claude Code 读取。Catalog 将六项建模为 `.md` 文件节点，`init` 只创建五个必需文件位置，且仅在显式启用时创建 `PROJECT_STYLE.md`，不负责或覆盖各 Owner 的文件正文；strict 仅只读拒绝双文件正文漂移。
- 稳定决策：`database/connection/` 是关系型数据库、Redis、Mongo 等数据存储服务的连接、连接池与客户端初始化入口；`database/model/` 只允许 `db/`、`redis/`、`mongo/` 子目录。`database/migration/` 是自动迁移生产源码，字段和索引均按 CRUD 分类；独立 SQL 仅在 `database/sql/ddl/`、`database/sql/index/` 与 `database/sql/field/{create,update,delete}/`，每个 SQL 叶子目录只直接保存 `.sql` 文件，且与迁移源码严格隔离。
- 稳定决策：后端项目根不建立 `data/`、`data/business/`、`data/project/` 或 `data/seed/`；Catalog 将根 `data` 作为禁止路径，query、init 与 strict 必须失败关闭。该限制不影响前端 `src/data/`、业务域数据或 `doc/data/`。
- 稳定决策：旧项目不自动迁移。每个独立项目以 `doc/1-架构/3-目录规则收敛清单.yaml` 人工登记 `adopted_paths` 与 `legacy_source_roots`；已采纳 V2 目录可按 Catalog 扩展，遗留快照只允许维护已登记的源码文件和目录。新业务、新模块与可独立演进逻辑必须使用 V2 唯一位置，`check --policy adoption` 全程只读且不得成为绕过禁止路径的通道。
- 稳定决策：独立后端的默认二进制入口固定为根 `main.<ext>`，仅当存在额外 binary 时使用 `cmd/<binary>/main.<ext>`；前后端同仓的后端对应固定为 `backend/main.<ext>` 与 `backend/cmd/<binary>/main.<ext>`。根 `cmd/main.<ext>`、同仓根 `main.<ext>`、同仓根 `cmd/` 和 `backend/cmd/main.<ext>` 都是非法入口；Catalog 以动态 pattern 建模，`init` 显式启用时必须失败关闭且不得创建占位路径。
- 稳定决策：独立后端配置唯一根为 `config/`，前后端同仓的后端配置唯一根为 `backend/config/`；两者均按需使用 `yaml/` 与 `embedded/` 子目录。常见多环境 YAML 使用 `yaml/config_local.yaml`、`yaml/config_test.yaml`、`yaml/config_prod.yaml`，Go 源码内嵌配置格式名必须后置，使用 `embedded/config_local_yaml.go`、`embedded/config_test_yaml.go`、`embedded/config_prod_yaml.go`；环境集合可扩展，不要求所有环境齐全，也不要求 YAML 与 embedded 成对出现。格式名后置的原因是 `config_test.go` 会被 Go 当成测试文件并排除出 `go build`，因此 `embedded/config_<env>.go` 属于非法旧命名；环境名同样不得以 `_yaml` 结尾。外部 YAML 不参与编译，保持 `config_<env>.yaml`，不加 `_yaml` 后缀。文件名契约只对 `.go` 强制，其他语言的 embedded 仍只校验源码扩展名；`check` 只读，`init` 不生成动态环境配置文件。YAML 继续禁止秘密原值；backend/fullstack 的 embedded 源码允许直接包含 API key、密钥、密码等私密值，源码为主且默认不依赖环境变量，但 Agent 输出、日志、README、错误和测试报告不得泄露原值。config/ 根允许直接存放 `load.<ext>`（配置加载与解析入口）与 `model.<ext>`（配置结构定义）两个源码文件，条件提交且 `init` 不创建；`config/yaml/` 与 `config/embedded/` 只存放配置数据。
- 稳定决策：fullstack、backend、frontend 三类项目统一使用项目根 `test/` 作为活动测试代码唯一入口；独立后端使用根 `test/`，不建立 `backend/test/`；前后端同仓也不建立 `backend/test/` 或 `frontend/test/`。Catalog 的测试目录 Owner 为 `test-strategy-rules`，`doc/5-tests/` 只保存测试说明和非可执行证据，不能替代根 `test/`。
- 稳定决策：前后端同仓、独立后端、独立前端三类项目根都必须直接保存并提交 `Dockerfile`。Catalog 以 `project-governance/dockerfile` 的必需文件条目建模，`init` 自动创建空文件位置；`strict` 只读拒绝缺失或被目录占用，`adoption` 保持旧项目渐进采纳，不强制补迁移文件。
- 来源：`package-structure-rules/SKILL.md`、`package-structure-rules/references/project-layout-v2.md`、`package-structure-rules/references/placement-catalog.yaml`。
- 更新时间：2026-08-05。

## 非 Plan Mode 最小计划分级规则

- 稳定决策：计划任何时候都需要，只是确认方式不同——Plan Mode 下先出计划、等用户明确确认后再执行；非 Plan Mode 下先出最小计划、默认直接执行，不必逐条等待确认。
- 稳定决策：`implementation-planning-rules` 新增 `minimum-plan-grading` 条件路由，按改动量把非 Plan Mode 任务分三级：微小（预计 1 个文件、数行以内、无分支）沿用 Karpathy 硬闸门隐性收敛，不强制可见计划；中等（预计 2-5 个文件，或存在分支/方案选择、影响面不完全确定）编码前必须先输出一段对话内可见的最小计划（改动目标、方案、影响范围、验证方式），输出后默认直接执行；重量级（命中原有多文件/多模块/多接口触发条件，或 Plan Mode）沿用完整实施总览/实施周期/Plan Mode 流程。
- 稳定决策：Bug 域的同等分级义务固定交给 `bug-fix-proposal-rules` 及其 `references/confirm-before-coding.md`，`minimum-plan-grading` 不重复接管，避免同一次修复被两套分级规则同时套用。
- 稳定决策：中等分级的最小计划默认不必写入 `artifact-storage-rules` 的正式实施文档；若执行中发现改动量超出预期（触达文件明显超过 5 个或触及公共模块），必须停下重新评估分级并按需升级为重量级。
- 来源：对话确认、`implementation-planning-rules/SKILL.md`、`implementation-planning-rules/references/minimum-plan-grading.md`、`bug-fix-proposal-rules/references/confirm-before-coding.md`。
- 更新时间：2026-07-29。

## 三类项目 doc 目录收敛规则

- 稳定决策：fullstack、backend、frontend 的活动研发目录统一为 `doc/1-架构/`、`doc/2-需求/`、`doc/3-实施/`、`doc/4-bugs/`、`doc/5-tests/`、`doc/6-review/`；条件图片与截图统一放 `doc/data/images/`。
- 稳定决策：`doc/6-审查/`、`doc/7-验收/` 只作为历史只读归档，不再进入人工活动骨架、Catalog skeleton 或新初始化结果。
- 稳定决策：独立前端不建立根 `data/business/<domain>/`、`data/project/` 原始静态数据树；源码域 `src/modules/<domain>/data/` 和 `doc/data/images/` 不受影响。
- 稳定决策：后端独立项目的 `doc/` 必须展开完整活动子树，注释使用“后端”；同仓目录使用工作区语义；`6-review` 说明为“测试后的风格回归记录”。
- 来源：`package-structure-rules/references/project-layout-v2.md`、`package-structure-rules/references/placement-catalog.yaml`、`doc/2-需求/2026-07-28_014412_代码位置目录规则V2.md`、`doc/3-实施/2026-08-02_192314_REQ-PSR-DOC-LAYOUT-001_实施周期16_三类项目doc目录收敛.md`。
- 更新时间：2026-08-02。

## 总结知识引用清单规则

- 稳定决策：`reasoning-summary-structure-rules` 的最终总结新增条件小节 `## 📚 知识引用`，用「本轮引用」三列表与「本轮沉淀」四列表承载 Obsidian 事实；原先分散在「方案与根因」和「结果与结论」的两处单行摘要口径已作废。
- 稳定决策：无真实阻断时末尾顺序按引用台账分流——台账非空由知识引用收尾、改动点紧邻其前；台账为空由改动点收尾；真实阻断时两者都在阻断收口之前。
- 稳定决策：`obsidian-knowledge-flow` 每次 `read`、`create`、`append` 返回 `verified=true` 后必须立即登记引用台账（笔记名、所在目录、本轮用途、`status`、操作、readback 六字段）；台账是会话内事实，不写入 vault、不落盘项目文件。
- 稳定决策：只有真实 `read` 成功的笔记可进引用表，`search` 命中未读取的一律不得入表；引用小节每一行都必须能回指一次返回成功的 bridge 调用。
- 稳定决策：笔记名一律取自发起 bridge 调用时所用 path 的文件名部分，禁止使用 CLI 回显文本——官方 CLI 在 Windows 下回显中文会乱码。
- 事实更新：固定 vault `D:\obsidian_data` 已注册可用，`doctor`、`read` 与 `create` 均返回 `verified=true`；此前记录的 `Obsidian:阻断` 结论已过期。
- 来源：`reasoning-summary-structure-rules/SKILL.md`、`references/summary-structure-template.md`、`references/conditional-sections-rules.md`、`obsidian-knowledge-flow/references/capture-retrieve-distill.md`、`doc/2-需求/2026-08-04_总结知识引用清单_Obsidian引用可视化.md`、`doc/3-实施/2026-08-04_总结知识引用清单_实施周期21_Obsidian引用可视化.md`。
- 更新时间：2026-08-04。

## 知识库可迭代更新规则

- 稳定决策：Obsidian 知识库从只增量补充改为可迭代更新。写入前必须显式判定 `补充` / `矛盾未裁决` / `取代` 三态之一；判为取代必须在同一轮内处置旧笔记，只写新笔记不处置旧笔记是禁止行为。
- 稳定决策：取代按旧笔记剩余价值分三档——仍有历史参考价值改 `status: superseded` 并标 `superseded_by`；完全失效且反向链接为 0 改 `status: archived` 后 `move` 到 `知识库/90-Archive/`；内容错误或有害 `delete` 进回收站并在新笔记记录旧错误说法。
- 稳定决策：三档处置前必须先查 `backlinks`，引用数不为 0 时不得 `move` 或 `delete`，只能降级为标记取代；接替关系必须双向写入 `supersedes` 与 `superseded_by`，只写一侧视为治理未闭环。
- 稳定决策：`superseded` 与 `archived` 状态的笔记不得作为当前事实，检索命中时顺着 `superseded_by` 跳到接替笔记；执行失败案例笔记不适用三档处置，仍只能 `append` 追加状态事件，bridge 层直接拒绝对该目录的 `move` 与 `delete`。
- 稳定决策：三档处置由 agent 自动执行（`delete` 进回收站可恢复），但每次 `property-set`、`move`、`delete` 都必须在最终总结的知识引用小节如实登记。
- 稳定决策：bridge 白名单从 8 个扩到 16 个，新增 `property-read`、`properties`、`property-set`、`move`、`delete`、`backlinks`、`files`、`orphans`；八个新命令全部使用 `path=`，`delete` 固定进回收站不透传 `permanent`，`move` 的目标目录必须已存在。
- 关键事实：官方 CLI 在 stdout 被重定向时输出的是正确 UTF-8 字节；此前"CLI 回显中文乱码"的判断是错误归因，真实根因是 bridge 自身 stdout 沿用系统 locale，已在 `main()` 用 `reconfigure(encoding="utf-8")` 根因修复。
- 关键事实：存在性探测必须用严格模式，因为 `properties` 对不存在的文件以退出码零返回 `Error:` 载荷。
- 关键事实：读取笔记元信息优先用 `properties --json`，比解析 `read` 全文更省更稳；部分笔记没有 frontmatter，会返回 `No frontmatter found.`，拿不到状态字段。
- 来源：`obsidian-knowledge-flow/references/conflict-staleness.md`、`references/capture-retrieve-distill.md`、`references/note-schema.md`、`scripts/obsidian_cli_bridge.py`、`scripts/audit_vault_knowledge.py`、`doc/2-需求/2026-08-05_知识库可迭代更新_冲突取代与废弃治理.md`。
- 更新时间：2026-08-05。

## PROJECT_MEMORY / PROJECT_STYLE 到 Obsidian 的选择性沉淀桥接规则

- 稳定决策：`PROJECT_MEMORY.md`/`PROJECT_STYLE.md` 与 Obsidian vault 的"本地上下文 vs 跨项目知识库"边界不变；新增的是一条"单条可复用事实"选择性桥梁，不是整份文件同步或镜像备份，核心标准定义在 `obsidian-knowledge-flow/references/project-memory-bridge.md`。
- 稳定决策：判断是否跨项目可复用采用两层分工——初判层由 `project-memory-rules`/`project-style-rules` 在写入条目的同一步骤完成，标准是"通用性删除测试"（去掉项目名、具体表名/字段名、具体服务名等专属信息后条目是否仍然成立）叠加类型白名单、适用范围显式标注为通用、状态为启用四条，全部满足才追加可选字段 `bridge_candidate: true` / `跨项目候选: 是`；这一步不调用 bridge，不产生 vault 副作用。
- 稳定决策：复核与落地层由 `obsidian-knowledge-flow` 在既有"总结阶段捕获流程"（会话总结、阶段收口或最终回复前）完成，把候选条目作为新增信息来源纳入既有扫描，套用既有排除规则二次核验后，选择性沉淀到 `知识库/20-Knowledge/project-rules/`（来自 project-memory-rules）或 `知识库/20-Knowledge/code-style/`（来自 project-style-rules）；不新增 Obsidian 四态之外的第五种状态，只是"沉淀"分支下的新增信息来源。
- 稳定决策：去重固定为"先 `search`、命中则 `append`、未命中才 `create`"，vault 侧笔记只保留脱敏后的通用表述与 `source_refs` 来源引用，不摘录项目原文；`skill-hit-check-rules` 的命中清单同步补充识别信号，避免候选标记被漏判为"不适用"。
- 来源：`obsidian-knowledge-flow/references/project-memory-bridge.md`、`obsidian-knowledge-flow/SKILL.md`、`obsidian-knowledge-flow/references/capture-retrieve-distill.md`、`obsidian-knowledge-flow/references/vault-layout.md`、`project-memory-rules/SKILL.md`、`project-memory-rules/references/project-knowledge-source-contract.md`、`project-style-rules/SKILL.md`、`skill-hit-check-rules/references/hit-checklist.md`、用户在 Plan Mode 确认的方案（`C:\Users\luode\.claude\plans\project-memory-md-project-style-md-obsi-fancy-wand.md`）。
- 更新时间：2026-08-05。

## 代码风格规则生效层级规则

- 稳定决策：一条代码风格规则写进 `code-style-consistency-rules/SKILL.md` 正文并不等于生效；能否拦住代码生成取决于它是否落在**写码前**会被加载的入口。四个落点的实际效力分层为：`references/user-style-feedback-library.md`（`code-generation-style-rules` 写码前强制加载 active 条目，最强）> `references/go-coding-rules.md`（Go 改动默认补读）> `SKILL.md` 正文（skill 加载后、写码后一致性检查，弱）> `references/consistency-examples.md`（「只有在对照正反例时」才读，拦不住生成）。
- 稳定决策：往 `code-style-consistency-rules` 增补风格约束时，必须先问「这条会在写码前被读到吗」。只写 SKILL.md 正文和正反例文件等于把规则放在事后复盘层；跨项目通用偏好一律走 `style-feedback-workflow.md` 的 candidate→用户确认→active 流程写入全局反例库，项目专属一次性约定才走 `PROJECT_STYLE.md`（边界依据 `project-style-rules/SKILL.md:51`）。
- 证据：2026-08-06 实测，「Go 函数内禁止 `var (...)` 分组声明」原本已存在于 `SKILL.md:40-44` 与 `consistency-examples.md` 正例 4 / 反例 5，模型仍写出分组声明；根因即两个写码前加载入口均缺该规则。修复后新增 `STYLE-CASE-GO-003` active 条目与 `go-coding-rules.md` bullet，并补齐「行尾中文注释按列对齐」这一层原表述未覆盖的约束。
- 来源：`code-style-consistency-rules/references/user-style-feedback-library.md`、`code-style-consistency-rules/references/go-coding-rules.md`、`code-style-consistency-rules/references/style-feedback-workflow.md`、`code-generation-style-rules/references/pre-coding-checklist.md`、用户在 Plan Mode 确认的方案（`C:\Users\luode\.claude\plans\var-bestgap-int64-typed-narwhal.md`）。
- 更新时间：2026-08-06。

## 机器索引区

```yaml
version: 1
entities:
  - entity_id: rule.obsidian-iterative-knowledge-governance
    name: "知识库可迭代更新与分级处置"
    type: "知识库治理规则"
    aliases:
      - 三档处置
      - 知识库迭代更新
      - superseded_by 接替关系
      - 知识库巡检
    definition: "写入 Obsidian 知识库前必须显式判定补充、矛盾未裁决或取代三态之一；判为取代须在同一轮内按剩余价值分三档处置旧笔记：有历史参考价值改 status=superseded 并标 superseded_by，完全失效且 backlinks 为 0 改 status=archived 后 move 到 知识库/90-Archive/，内容错误或有害 delete 进回收站。三档前必须先查 backlinks，引用不为 0 只能标记取代；接替关系双向写入 supersedes 与 superseded_by，superseded_by 非空时 status 不得为 active。superseded 与 archived 不作当前事实，检索时顺 superseded_by 跳到接替笔记。执行失败案例笔记不适用三档处置，bridge 拒绝对该目录 move/delete。三档由 agent 自动执行但必须在总结的知识引用小节登记。bridge 白名单扩到 16 个命令，八个新命令均用 path=，delete 不透传 permanent，move 目标目录须已存在。已积压冲突用只读脚本 audit_vault_knowledge.py 出候选，脚本零写入。"
    scope: "Obsidian 知识库写入、检索、冲突处置与积压巡检"
    status: "active"
    evidence_ids:
      - evidence.obsidian-iterative-knowledge-governance
    context_ids:
      - context.obsidian-knowledge-flow
    updated_at: 2026-08-05
  - entity_id: rule.summary-knowledge-citation-section
    name: "总结知识引用小节与引用台账"
    type: "总结结构与知识库规则"
    aliases:
      - 知识引用小节
      - 引用台账
      - Obsidian 引用清单
    definition: "最终总结在无真实阻断时按引用台账分流收尾：台账非空输出 ## 知识引用 作为最后一节，用「本轮引用」三列表（序号、笔记、本轮用途）与「本轮沉淀」四列表（序号、笔记、操作、readback）承载，改动点紧邻其前；台账为空整节省略且由改动点收尾。obsidian-knowledge-flow 每次 read/create/append 返回 verified=true 后立即登记六字段台账；只有真实 read 成功的笔记可入引用表，search 命中未读取的不得入表；笔记名取自本地发起的 path 文件名，禁用 CLI 回显文本；笔记 status 为 stale/deprecated/retired/conflicted 时在用途列标注。"
    scope: "最终总结渲染、Obsidian 检索与沉淀登记、总结条件字段判定与驳回标准"
    status: "active"
    evidence_ids:
      - evidence.summary-knowledge-citation-section
    context_ids:
      - context.obsidian-knowledge-flow
    updated_at: 2026-08-04
  - entity_id: rule.root-test-code-and-evidence-layout
    name: "根测试代码与测试证据双根规则"
    type: "测试资产目录规则"
    aliases:
      - 根 test 目录
      - 测试资产镜像
      - doc/5-tests 证据根
    definition: "根 test/ 是唯一活动测试代码根，测试程序、mock、stub、fake、fixture、helper 和启动脚本按被测目录镜像；源码关联模拟程序与对应测试使用同一源码相对路径，跨源码复用模拟能力才进入 test/shared/；Python 文件使用 *_test.py，模拟程序使用 _mock、_stub 或 _fake 后缀。doc/5-tests/ 仅保存时间戳 README 和非可执行证据；历史可执行资产由指纹清单保护，首次修改才迁移。Go 测试使用根 test/ 的 ASCII 外部黑盒包，源码目录禁止 *_test.go。"
    scope: "新增测试、活动测试迁移、真实测试归档、测试策略和 6-review 目录归位"
    status: "active"
    evidence_ids:
      - evidence.root-test-code-and-evidence-layout
    context_ids:
      - context.test-asset-governance
    updated_at: 2026-08-01
  - entity_id: rule.runtime-mock-location
    name: "运行时 Mock 目录规则"
    type: "目录规则"
    aliases:
      - 根 mock 目录
      - 运行时 Mock
      - mock 构建标签
      - selector 配对
      - runtime-mock 目录树
    definition: "根 mock/ 是运行时 Mock 的唯一合法目录，与根 test/ 对等，按 internal/ 相对路径镜像；入口按需配对 main_mock.go（//go:build mock）与 main_real.go（//go:build !mock），两份 selector 声明同名 newXxx()；mock/assembly/ 是唯一装配桥且包名固定 assembly，Mock 实现包名 mock_<源包名>；目录检查只读，adoption 不扩大既有 test/ 遗留快照豁免。"
    scope: "后端运行时 Mock 落点、Go 构建标签、入口 selector、assembly 装配、Catalog 查询与 CLI 只读检查"
    status: "active"
    updated_at: 2026-08-08
  - entity_id: rule.package-structure-three-project-test-root
    name: "三类项目根测试目录落点"
    type: "包结构目录规则"
    aliases:
      - 三类项目根 test
      - 独立后端根 test
      - fullstack backend frontend test
    definition: "fullstack、backend、frontend 三类项目都把活动测试代码放在项目根 test/。独立后端不建立 backend/test/；前后端同仓不建立 backend/test/ 或 frontend/test/。Catalog 以 test-strategy-rules 为 Owner 建模唯一测试目录，doc/5-tests/ 只保存说明和非可执行证据。"
    scope: "package-structure-rules 的人工目录树、Catalog、query、render、init 和根测试契约"
    status: "active"
    evidence_ids:
      - evidence.package-structure-three-project-test-root
    context_ids:
      - context.test-asset-governance
    updated_at: 2026-08-02
  - entity_id: rule.shared-static-owner-routing
    name: "共享静态 Owner 路由与可选监控消费者"
    type: "Skill 治理规则"
    aliases:
      - 共享 Owner 路由
      - static_owner_router
      - 监控代码消费者
    definition: "code-style-consistency-rules 是静态 Owner 路由与来源映射的唯一 Owner；测试后的 6-review 消费风格子集。continuous-code-quality-supervisor-rules 仅在 Goal active 且用户明确要求监控代码时条件式消费完整集合，保留扫描、脱敏、finding 指纹、去重和通知，不得复制路由常量、条件或来源映射，也不是测试后的 Gate。"
    scope: "6-review 风格回归、条件式持续代码监控、共享静态路由维护"
    status: "active"
    evidence_ids:
      - evidence.shared-static-owner-routing
    context_ids:
      - context.implementation-flow
    updated_at: 2026-08-01
  - entity_id: rule.control-plane-single-direction-routing
    name: "总控层单向路由与合并规则"
    type: "Skill 治理规则"
    aliases:
      - 总控层精简
      - 并行与子代理统一 Owner
      - 项目自举双条件路由
    definition: "每轮由 skill-hit-check-rules 唯一进入；并行分类与子代理生命周期统一归 parallel-task-dispatch-rules，生命周期必须执行进入前预检、批次回收和最终回复前终局扫描，只有真实关闭并复查不活跃才计关闭，未关闭实例阻止下一批；项目规则和记忆骨架自举统一归 project-rule-file-bootstrap-rules 的 rule-bootstrap/memory-bootstrap；压缩恢复只在近期事实缺失时条件调用 recent-context-bootstrap-rules；最终 Markdown 由 reasoning-summary-structure-rules 唯一渲染。退役候选必须完成保护语义、触发正负样本、消费者、资产、回滚和 post-delete 门禁。"
    scope: "总控入口、上下文恢复、项目自举、并行委派、执行收口和最终总结"
    status: "active"
    evidence_ids:
      - evidence.control-plane-streamlining
      - evidence.control-plane-post-delete
    context_ids:
      - context.skill-governance
    updated_at: 2026-07-25
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
    definition: "当用户提供 URL、网页地址或在线文档链接并要求读取、分析、截图或排查页面时，默认优先命中 `authenticated-url-routing-rules`，并优先通过 `chrome:control-chrome` 复用用户已登录的真实 Chrome profile；依赖真实 profile 的页面在 Chrome Plugin 不可用时停在连接/授权阻断，不得用本地自动化或 Browser Use Cloud 绕过；只有 Cloud 专属需求或用户明确点名时才转交 `browser-use-cloud-rules`。"
    scope: "URL 分析、在线文档读取、浏览器权限页面"
    status: "active"
    evidence_ids:
      - evidence.skill.authenticated-url-routing
    context_ids:
      - context.url-analysis
    updated_at: 2026-07-26
  - entity_id: rule.browser-use-cloud-safety
    name: "Browser Use Cloud 收费与安全路由"
    type: "浏览器路由规则"
    aliases:
      - browser-use-cloud-rules
      - BROWSER_USE_API_KEY
      - Cloud 浏览器
    definition: "Browser Use Cloud 只用于 Cloud 专属能力，不接本地 Browser Use，也不替换现有浏览器路由。每次 run_session/send_task 前检查本机 key、Billing、当前动作可写 maxCostUsd 并取得当次确认；免费层也确认，无硬上限默认停止。任务结束后用 strategy=session 停止遗留 session，只有 stopped 且实际总费用合法才收口。"
    scope: "Browser Use Cloud 路由、收费动作、密钥提醒、session 生命周期"
    status: "active"
    evidence_ids:
      - evidence.skill.browser-use-cloud
      - evidence.accept.browser-use-cloud-20260726
    context_ids:
      - context.url-analysis
    updated_at: 2026-07-26
  - entity_id: rule.reasoning-summary-detail
    name: "结果与结论适中详细度契约"
    type: "最终总结输出规则"
    aliases:
      - reasoning-summary-structure-rules
      - 结果区 3–5 句
      - 适中详细结论
    definition: "最终结果区默认使用 3 个简短句子回答解决的问题、采用的方法和结果/验证状态；复杂、受限或存在关键边界时按事实扩展到第 4–5 句，仅补充必要范围边界、残留卡点或验证限制。禁止用空泛状态词替代核心信息，也禁止复制命令、完整测试清单、逐文件改动或执行流水账；不改变既有总结顺序、图形化条件、WAITING_DECISION 阻断或任务阻断收口 Owner。"
    scope: "最终回复、审查验收收口、结果区详细度和结论可复核性"
    status: "active"
    evidence_ids:
      - evidence.skill.reasoning-summary-detail
      - evidence.test.reasoning-summary-detail
      - evidence.accept.reasoning-summary-detail-20260726
    context_ids:
      - context.final-summary
    updated_at: 2026-07-26
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
    definition: "实施周期是项目第一期、第二期、第三期等大进度单位和顺序边界；执行必须先按周期推进，当前周期内每个最小任务都完成实施计划中的完成条件、实现、真实测试和测试后的 6-review 风格回归后，才允许进入下一最小任务或下一周期。"
    scope: "实施规划、连续执行、文档落盘、真实测试、6-review 风格回归"
    status: "active"
    evidence_ids:
      - evidence.skill.implementation-planning
      - evidence.skill.autonomous-execution
      - evidence.skill.artifact-storage
    context_ids:
      - context.implementation-flow
    updated_at: 2026-08-01
  - entity_id: rule.implementation-sequence-master-plan
    name: "需求与实施计划全量顺序实施方案"
    type: "流程规则"
    aliases:
      - 实施顺序总表
      - 全量顺序实施方案
      - 新项目实施总顺序
    definition: "新项目、项目初期或多来源对象存在多份需求 / 实施文档时，必须在 `doc/3-实施/` 维护项目级或来源集合级总顺序文档，串起需求主文档、实施计划内的 AC 完成条件、实施总览、实施周期和周期内最小任务；该文档只负责跨来源对象排序，不替代单来源对象实施总览。"
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
    definition: "新增、修改或重构任意代码、脚本、测试支撑代码或配置型代码前，必须先由 `code-generation-style-rules` 读取用户本轮要求、目标文件 / 同目录样例、根目录 `PROJECT_STYLE.md` 和已命中的编码类 skill，形成本轮代码风格契约；高度统一的局部上下文只允许必要模板替换，不得加入多余代码；实现已有接口时必须优先参考既有接口实现并记录参考或降级依据；`project-style-rules` 只维护长期风格记忆，`code-style-consistency-rules` 基于契约检查局部一致性。"
    scope: "编码基线域、仓库级规则自举、代码生成与修改"
    status: "active"
    evidence_ids:
      - evidence.skill.code-generation-style
      - evidence.skill.project-agents-bootstrap
    context_ids:
      - context.code-generation-style
    updated_at: 2026-07-15
  - entity_id: rule.comment-block-step-annotation
    name: "长代码块内步骤注释"
    type: "代码注释规则"
    aliases:
      - comment-completion-gate-rules
      - comment-placement-granularity-rules
      - 代码块五行门槛
      - 长代码块步骤注释
      - 代码块内步骤注释
    definition: "函数/方法体、闭包体和连续控制流代码块按非空有效代码行计数，超过5行时必须在块内就近补顶层编号步骤注释；每个超长代码块独立判断，嵌套代码块不能只依赖外层编号。"
    scope: "代码注释、步骤注释、注释放置与颗粒度、代码审查"
    status: "active"
    evidence_ids:
      - evidence.skill.comment-completion
      - evidence.skill.comment-placement
      - evidence.dialog.comment-block-step-annotation
    context_ids:
      - context.code-generation-style
    updated_at: 2026-07-16
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
  - entity_id: rule.backend-utils-common-util-placement
    name: "后端 utils 与 common/util 工具分流"
    type: "包结构规则"
    aliases:
      - 后端 utils 归位
      - common/util 归位
      - IP 工具包归位
      - utils 与 common/util 区分
    definition: "可独立复制的后端工具包与 SDK 位于根 utils/<package>/，根 utils 不得直接存放文件且不得依赖项目其他包；IP 提取、规范化、公私网判断和国家/地区归属查询适配固定于 utils/ip/，不承载代理信任或业务策略；可引用项目其他包的高关联工具函数直接位于独立后端 common/util/<function>.<ext>，不得创建子目录。源码根 util 为废弃位置，业务域 util 保留为域私有辅助能力。"
    scope: "后端通用工具、SDK、高关联工具函数、业务域私有辅助归位"
    status: "active"
    evidence_ids:
      - evidence.skill.common-util-rules
      - evidence.skill.package-structure-rules
      - evidence.dialog.backend-utils-common-util-placement
    context_ids:
      - context.code-generation-style
    updated_at: 2026-08-04
  - entity_id: rule.backend-root-governance-files
    name: "后端根治理文件位置"
    type: "项目治理目录规则"
    aliases:
      - 后端根 AGENTS
      - 后端根 CLAUDE
      - 项目四件套根位置
      - 后端 PROJECT_STYLE
    definition: "后端项目根直接保存 AGENTS.md、CLAUDE.md、PROJECT_CURRENT.md、PROJECT_MEMORY.md、PROJECT_HISTORY.md；PROJECT_STYLE.md 仅在有长期风格时创建。AGENTS.md 与 CLAUDE.md 正文必须一致。Catalog 将六项登记为 Markdown 文件节点；init 只创建五个必需文件位置，条件风格文件必须显式启用，strict 只读拒绝双规则文件正文漂移，正文仍由各自 Owner 维护。"
    scope: "后端项目骨架、Catalog 查询、目录树渲染和 init 初始化"
    status: "active"
    evidence_ids:
      - evidence.skill.package-structure-rules
      - evidence.dialog.backend-root-governance-files
    context_ids:
      - context.code-generation-style
    updated_at: 2026-07-29
  - entity_id: rule.backend-database-storage-layout
    name: "后端数据存储目录分层"
    type: "包结构与数据存储规则"
    aliases:
      - 数据存储 connection
      - database model 分类
      - 独立字段 SQL
      - database 连字符查询
    definition: "database/connection 承载关系型数据库、Redis、Mongo 等数据存储服务的连接、连接池与客户端初始化；database/model 只能使用 db、redis、mongo 子目录；自动迁移源码留在 database/migration 的字段和索引 CRUD 分类；独立 SQL 只进入 database/sql/ddl、database/sql/index、database/sql/field/create、update、delete，叶子目录只能直接保存 .sql 文件。公开 database 连字符 artifact 查询兼容 Catalog 的内部下划线字段。"
    scope: "后端目录树、Catalog 查询、初始化、strict 检查与独立 SQL 边界"
    status: "active"
    evidence_ids:
      - evidence.skill.package-structure-rules
      - evidence.dialog.backend-database-storage-layout
    context_ids:
      - context.code-generation-style
    updated_at: 2026-07-31
  - entity_id: rule.backend-root-data-forbidden
    name: "后端根 data 禁止路径"
    type: "包结构禁止规则"
    aliases:
      - 后端根 data 删除
      - backend data forbidden
      - data/business data/project data/seed
    definition: "后端项目根不建立 data、data/business、data/project 或 data/seed。Catalog 将 data 作为禁止路径，query、init 与 strict 必须失败关闭；该规则不影响前端 src/data、业务域数据或 doc/data。"
    scope: "后端目录树、Catalog 查询、初始化、strict 检查与旧项目 adoption 边界"
    status: "active"
    evidence_ids:
      - evidence.skill.package-structure-rules
      - evidence.dialog.backend-root-data-deletion
    context_ids:
      - context.code-generation-style
    updated_at: 2026-07-31
  - entity_id: rule.project-dual-platform-rule-files
    name: "三类项目双平台协作规则文件"
    type: "项目治理目录规则"
    aliases:
      - AGENTS 与 CLAUDE 一致
      - Codex 与 Claude Code 规则文件
      - 双平台项目根规则
    definition: "前后端同仓、独立后端和独立前端项目根都必须提交 AGENTS.md 与 CLAUDE.md，两个文件正文必须一致，分别供 Codex 与 Claude Code 读取。Catalog 对每种项目类型提供唯一文件节点；init 只创建空文件位置，strict 只读比对已同时存在的正文，bootstrap_agents.sh --target both 以 AGENTS.md 同步 CLAUDE.md。"
    scope: "三类项目目录树、Catalog 查询、初始化、严格检查和项目规则自举"
    status: "active"
    evidence_ids:
      - evidence.skill.package-structure-rules
      - evidence.dialog.project-dual-platform-rule-files
    context_ids:
      - context.code-generation-style
    updated_at: 2026-07-29
  - entity_id: rule.micro-business-json-rpc-boundary
    name: "微业务跨域 JSON RPC 边界"
    type: "包结构与业务隔离规则"
    aliases:
      - 业务域 rpc
      - 微业务 JSON 通信
      - 目标域 rpc 公开入口
    definition: "业务域按需创建 business/<domain>/rpc。调用方只可精确导入目标域 rpc 的公开函数，输入和输出均为 JSON 字符串；目标域在自身 rpc 内完成解析、校验、私有服务调用和 Response{code,status,message,data} 序列化。目标域 api、service、entity、base、constant、init、crontask、util 等均为私有层，不得跨域导入。"
    scope: "后端微业务目录、跨业务调用、CodeGraph 导入审查、JSON 响应边界"
    status: "active"
    evidence_ids:
      - evidence.skill.package-structure-rules
      - evidence.skill.micro-business-architecture-rules
      - evidence.dialog.micro-business-json-rpc-boundary
    context_ids:
      - context.code-generation-style
    updated_at: 2026-07-28
  - entity_id: rule.legacy-project-directory-adoption
    name: "旧项目目录规则渐进采纳"
    type: "包结构兼容规则"
    aliases:
      - 旧项目渐进采纳
      - 收敛清单
      - adoption 检查
      - legacy_source_roots
    definition: "旧项目不自动迁移。人工维护 doc/1-架构/3-目录规则收敛清单.yaml：adopted_paths 只能精确登记已存在的 V2 Catalog 路径并继续遵守其约束；legacy_source_roots 只快照已存在的源码目录和文件，允许维护但禁止新增。新业务、新模块和独立新逻辑必须进入 V2 唯一位置；adoption 检查全程只读。"
    scope: "旧项目目录兼容、V2 原地采纳、遗留源码维护边界与 CLI 检查"
    status: "active"
    evidence_ids:
      - evidence.skill.package-structure-rules
      - evidence.doc.psr-v2-adoption
      - evidence.dialog.legacy-project-directory-adoption
    context_ids:
      - context.code-generation-style
    updated_at: 2026-07-29
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
    definition: "项目启动先按父目录平台规则 -> PROJECT_CURRENT.md -> PROJECT_MEMORY.md 读取本地上下文；current 覆盖维护且不超过 51,200 字节，memory 只承载稳定规则与关键决策，history 追加关键事件并只保留最近 20 条（自动裁剪、按日期倒序）且普通启动不读。Obsidian 固定使用 D:\\obsidian_data 及其 知识库/ 工作区，仅在跨项目历史或既有 vault 知识依赖时通过 CLI 检索 / 读取，仅在收口形成可复用知识时先检索再沉淀；普通任务不为形式调用 CLI，CLI / vault 不可用时阻断且不得直接读写 vault 文件。项目本地 Markdown 与 vault 链路不得混用。"
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
      - 同一任务文档合并提交
      - docs/test/实现分离
    definition: "`提交git` 允许拆成多次提交清空工作区，但每个 commit 默认只承载一个提交域。同一任务的需求、实施、Bug、测试说明、6-review、验收和项目状态同步文件统一归入一笔 `docs` 提交；`doc/5-tests/**` 只保存说明、日志、报告、截图和非可执行证据。根 `test/**`、`*_test.*`、`*.spec.*`、`*.test.*` 等可执行测试独立归入 `test` 提交；代码实现 / 运行配置独立归入 `feat` 或 `fix` 提交，不与 `docs` 或 `test` 混提。历史 `doc/6-审查/`、`doc/7-验收/` 只读兼容，不因新流程创建。"
    scope: "提交流程、需求/实施/Bug/测试/6-review 归档"
    status: "active"
    evidence_ids:
      - evidence.skill.git-collaboration
      - evidence.dialog.git-commit-domain-split
    context_ids:
      - context.git-collaboration
    updated_at: 2026-08-02
  - entity_id: rule.git-commit-review-acceptance-evidence
    name: "Git 提交基础质量闸门"
    type: "流程规则"
    aliases:
      - 提交前质量检查
      - Git 基础质量
      - 提交不生成审查验收文档
    definition: "Git 提交必须直接对 staged 改动执行基础质量核查，并在提交证据中记录格式、注释、安全性、并发安全性、系统崩溃风险、边界条件和测试/功能验证适用性；不得因提交自动创建或要求 `doc/6-审查/`、`doc/7-验收/`。活动代码改动的风格结论只由真实测试后的 `doc/6-review/` 记录，业务正确性由真实测试负责。"
    scope: "提交流程、基础质量、6-review 风格回归"
    status: "active"
    evidence_ids:
      - evidence.skill.git-collaboration
      - evidence.dialog.git-commit-no-review-acceptance-doc
    context_ids:
      - context.git-collaboration
    updated_at: 2026-08-01
  - entity_id: fact.skill-size-baseline-20260717
    name: "Skill 体积治理统计基线"
    type: "统计口径"
    aliases:
      - Skill 体积预算
      - 84 个正式 skill
      - 默认文本包
      - 扩展种子排除
    definition: "正式字典主规划统计 84 个 skill；根目录实际 111 个带 SKILL.md 的目录中有 27 个扩展种子，不纳入主规划拆分基线。默认文本包为 SKILL.md 与 references 全部文本资源的原始字节总数；预算等级按 16,000/20,000/24,000 B、12,000/16,000 B 和 48,000/64,000 B 阈值分为 normal、review、split_candidate、hard_warning。"
    scope: "全仓 skill 体积盘点、候选冻结和职责拆分复评"
    status: "active"
    evidence_ids:
      - evidence.test.skill-size-report-20260717
      - evidence.doc.skill-size-plan-20260717
    context_ids:
      - context.implementation-flow
    updated_at: 2026-07-17
  - entity_id: fact.skill-split-candidate-matrix-20260717
    name: "Skill 体积候选矩阵"
    type: "拆分决策"
    aliases:
      - Skill 拆分候选矩阵
      - 候选顺序
      - 正式/扩展种子双层追踪
    definition: "TASK-SPLIT-01-02 将 84 个正式 skill 与 27 个扩展种子分层记录；正式 enter_split 为 project-agents-bootstrap、skill-compliance-gate-rules、project-release-test-rules、agent-browser，各自具备两个独立职责组；2d-asset-design 为 P1 扩展种子例外；mcp-installation-rules 为 P2 candidate_design；implementation-planning-rules 为 gated_reassessment。"
    scope: "CYCLE-SPLIT-02 至 CYCLE-SPLIT-08 的候选进入、职责映射和测试入口选择"
    status: "active"
    evidence_ids:
      - evidence.test.skill-candidate-matrix-20260717
      - evidence.doc.skill-split-plan-20260717
    context_ids:
      - context.implementation-flow
    updated_at: 2026-07-17
  - entity_id: fact.skill-split-validation-entry-20260717
    name: "Skill 拆分通用测试入口"
    type: "测试契约"
    aliases:
      - TEST-SPLIT-003
      - 五类拆分验证
      - pre/post-delete fixture
    definition: "TASK-SPLIT-01-03 固化 validate_skill_split.py 的 size、mapping、trigger、pre-delete、post-delete 五类模式，并由 run_trigger_cases.ps1 通过 -CasesRoot 转发；报告和矩阵路径必须位于仓库根目录内，fixture 根必须位于当前测试时间戳目录内，越界必须非零失败且不得删除真实 skill。"
    scope: "CYCLE-SPLIT-02 至 CYCLE-SPLIT-08 的静态覆盖、触发、删除前后和路径边界验证"
    status: "active"
    evidence_ids:
      - evidence.test.skill-split-validation-entry-20260717
      - evidence.doc.skill-split-entry-plan-20260717
      - evidence.review.skill-split-current-diff-20260717
      - evidence.accept.skill-split-task-01-03-20260717
      - evidence.doc.skill-split-cycle-01-close-20260717
      - evidence.obsidian.skill-split-plan-20260717
    context_ids:
      - context.implementation-flow
    updated_at: 2026-07-17
  - entity_id: fact.skill-split-cycle-01-closure-20260717
    name: "Skill 拆分周期 01 收口状态"
    type: "周期状态"
    aliases:
      - 周期 01 收口
      - TASK-SPLIT-01-03 验收完成
      - 周期 02 未进入
    definition: "周期 01 的三个最小任务均完成实现、真实测试、审查和验收；通用测试入口只验证离线 fixture 契约，不代表真实 skill 已拆分，周期 02 保持未进入。"
    scope: "Skill 体积治理与职责拆分实施周期"
    status: "active"
    evidence_ids:
      - evidence.review.skill-split-current-diff-20260717
      - evidence.accept.skill-split-task-01-03-20260717
      - evidence.doc.skill-split-cycle-01-close-20260717
      - evidence.obsidian.skill-split-plan-20260717
    context_ids:
      - context.implementation-flow
    updated_at: 2026-07-17
  - entity_id: rule.task-plan-rehydration
    name: "Codex Desktop 任务投影断点恢复"
    type: "运行时恢复规则"
    aliases:
      - 任务投影
      - 悬浮任务列表恢复
      - task-plan-rehydration-rules
      - PROJECT_CURRENT 任务投影
      - 缺失投影十分钟异常修复
      - ensure-timeout
      - ensure-start
      - UI_SYNC_BLOCKED
    definition: "task-plan-rehydration-rules 独占 PROJECT_CURRENT v4 registry 托管区的 schema、指纹、session_id 归属、排他锁、原子写入、失活和 update_plan payload；默认执行取得 confirmed 后，任何任务首次领域动作前必须为当前 session 持久化 active/blocked projection，持久化后的下一动作立即调用 update_plan，失败进入 UI_SYNC_BLOCKED 并禁止继续领域写入。会话解析按显式 --session-id 优先、CODEX_THREAD_ID 回退，冲突或缺失失败关闭。十分钟只作为缺失 projection 的异常修复闸门；计时不持久化，也不承诺后台唤醒。"
    scope: "Codex Desktop 默认执行回合、首次任务可见性、Goal 生命周期、上下文恢复、宿主重开后的首次继续回合和缺失投影十分钟异常修复"
    status: "active"
    evidence_ids:
      - evidence.skill.task-plan-rehydration
      - evidence.doc.task-plan-rehydration-requirement
      - evidence.doc.task-plan-timeout-cycle
      - evidence.doc.task-plan-first-persist-cycle
    context_ids:
      - context.task-plan-rehydration
    updated_at: 2026-07-25
  - entity_id: rule.session-handoff
    name: "会话交接与新任务接续"
    type: "会话迁移规则"
    aliases:
      - 开新会话继续
      - 新会话中继续
      - 新会话继续
      - 会话太长
      - 归档旧会话
      - 迁移任务
      - 接续任务
      - 提取会话压缩信息
      - 唤起另一个会话
      - session-handoff-rules
    definition: "session-handoff-rules 负责提取当前会话和项目可核验的目标、范围、完成项、进行中断点、下一步、阻断、验证和关键决策，生成 UTF-8 脱敏交接包，并在同一保存项目的 local 环境创建新任务；v1 只提示人工归档旧任务，不自动改变旧任务状态。"
    scope: "Codex 会话压缩交接、新任务接续、交接包脱敏与校验、同项目 local 任务创建和 setup pending 边界"
    status: "active"
    evidence_ids:
      - evidence.skill.session-handoff
      - evidence.test.session-handoff
      - evidence.review.session-handoff
      - evidence.dialog.session-handoff-triggers
    context_ids:
      - context.session-handoff
      - context.memory-domain
    updated_at: 2026-08-02
  - entity_id: rule.plan-mode-decision-wait-loop
    name: "Plan Mode 决策选择框永久等待"
    type: "交互状态规则"
    aliases:
      - Plan Mode 永久等待
      - 空答案循环重发
      - WAITING_DECISION
      - SUMMARY-GATE-PMW-001
    definition: "Plan Mode 决策型 request_user_input 完全省略 autoResolutionMs；空答案、缺失答案、缺少预期问题 ID、null/空返回和宿主隐式超时均保持 WAITING_DECISION，并在旧调用返回后立即串行重发同一未决选择框。重发无次数或时间上限，部分答案只重发剩余问题且始终单活动框；未决期间禁止 commentary、limited_plan、pending_summary、proposed_plan、final、summary、final_answer、task_complete、result_and_conclusion、中文结果与结论、默认选择、Goal 和任务投影恢复。只有完整选择、明确代选、明确停止或明确不可恢复工具故障才离开等待。"
    scope: "Plan Mode 决策提问、宿主空答案消费、部分答案保存、总结输出闸门和上下文恢复"
    status: "active"
    evidence_ids:
      - evidence.skill.implementation-planning-plan-wait
      - evidence.skill.reasoning-summary-plan-wait
      - evidence.test.plan-mode-wait-loop
      - evidence.doc.bug-plan-wait
      - evidence.doc.acceptance-plan-wait
    context_ids:
      - context.plan-mode-wait-loop
      - context.implementation-flow
    updated_at: 2026-07-26
relations:
  - relation_id: rel.root-test-code-and-evidence-layout.owned-by.artifact-storage
    type: "owned_by"
    from: "rule.root-test-code-and-evidence-layout"
    to: "artifact-storage-rules"
    evidence_ids:
      - evidence.root-test-code-and-evidence-layout
    status: "active"
  - relation_id: rel.shared-static-owner-routing.consumed-by.continuous-supervisor
    type: "consumed_by"
    from: "rule.shared-static-owner-routing"
    to: "continuous-code-quality-supervisor-rules"
    evidence_ids:
      - evidence.shared-static-owner-routing
    status: "active"
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
  - relation_id: rel.session-handoff.depends-on.task-plan-rehydration
    type: "depends_on"
    from: "rule.session-handoff"
    to: "rule.task-plan-rehydration"
    evidence_ids:
      - evidence.skill.session-handoff
      - evidence.skill.task-plan-rehydration
    status: "active"
evidence:
  - evidence_id: evidence.root-test-code-and-evidence-layout
    type: "test"
    source: "根 test 目录统一实施与真实测试"
    path: "doc/5-tests/2026-08-01_191658_根test目录统一/README.md"
    note: "七组活动测试迁移至根 test/；治理测试 9/9、全量 Python 测试 187/187、Go 临时黑盒模块和严格文档 profile 均通过，历史 doc/5-tests 可执行资产指纹未变化。"
  - evidence_id: evidence.package-structure-three-project-test-root
    type: "test"
    source: "代码位置目录规则 V2 CYCLE-18 三类项目根 test 目录统一"
    path: "doc/5-tests/2026-08-02_235000_三类项目根test目录统一/README.md"
    note: "三类 Catalog、人工目录树、query、render 和 init 的根 test 契约测试 4/4 通过；入口回归 5/5、配置回归 7/7、根 Python 测试 212/212、文档 profile 和 Skill 校验通过。"
  - evidence_id: evidence.shared-static-owner-routing
    type: "skill"
    source: "6-review 共享静态 Owner 路由"
    path: "code-style-consistency-rules/scripts/static_owner_router.py"
    note: "唯一静态 Owner 路由和来源映射；持续监控仅条件式消费，7 项路由单测、17 项监控单测与专项脚本均通过。"
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
    path: "test/artifact-delivery-gate-rules/validate_engineering_docs_test.py"
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
  - evidence_id: evidence.skill.browser-use-cloud
    type: "skill"
    source: "browser-use-cloud-rules/SKILL.md"
    path: "browser-use-cloud-rules/SKILL.md"
    note: "Browser Use Cloud 专属路由、费用预检和 session 收口来源"
  - evidence_id: evidence.accept.browser-use-cloud-20260726
    type: "acceptance"
    source: "REQ-BU-20260726-001 最终验收"
    path: "doc/7-验收/2026-07-26_063000_REQ-BU-20260726-001_最终验收.md"
    note: "记录 Cloud 专属路由、逐次收费确认、本地回归和禁止真实收费测试的正式验收证据。"
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
  - evidence_id: evidence.skill.implementation-planning-plan-wait
    type: "skill"
    source: "Plan Mode 永久等待规则改动"
    path: "implementation-planning-rules/SKILL.md"
    note: "RULE-PMW-001..004、空答案串行重发、部分答案保留、无上限和单活动选择框契约来源"
  - evidence_id: evidence.skill.reasoning-summary-plan-wait
    type: "skill"
    source: "Plan Mode 总结消费方闸门改动"
    path: "reasoning-summary-structure-rules/SKILL.md"
    note: "SUMMARY-GATE-PMW-001 拒绝未决选择的总结、final_answer 和 task_complete 来源"
  - evidence_id: evidence.skill.reasoning-summary-detail
    type: "skill"
    source: "结果与结论详细度规则改动"
    path: "reasoning-summary-structure-rules/SKILL.md"
    note: "结果区 3 句核心、复杂边界 4–5 句上限、问题方法结果/验证覆盖和流水账拒绝契约来源"
  - evidence_id: evidence.test.reasoning-summary-detail
    type: "test"
    source: "结果与结论适中详细度专项回归"
    path: "doc/5-tests/2026-07-26_153733/reasoning-summary-structure-rules/test_result_conclusion_detail.py"
    note: "9 项本地正负样例验证句数、核心信息、复杂边界、重复流水账和 WAITING_DECISION 兼容"
  - evidence_id: evidence.accept.reasoning-summary-detail-20260726
    type: "acceptance"
    source: "REQ-SUMMARY-DETAIL-001 最终验收"
    path: "doc/7-验收/2026-07-26_162000_REQ-SUMMARY-DETAIL-001_最终验收.md"
    note: "记录 3–5 句结果区契约、七项验收标准、9/9 回归、审查结论和真实模型/UI 非范围边界"
  - evidence_id: evidence.test.plan-mode-wait-loop
    type: "test"
    source: "Plan Mode 永久等待专项行为回归"
    path: "doc/5-tests/2026-07-26_040607/plan_mode_wait_loop/test_plan_mode_wait_loop.py"
    note: "10 个本地标准库用例覆盖无超时字段、2/10/100 次空答案、部分答案、延迟选择、授权、停止、故障、历史负例和总结闸门"
  - evidence_id: evidence.doc.bug-plan-wait
    type: "bug"
    source: "BUG-PLAN-WAIT-20260726-001"
    path: "doc/4-bugs/2026-07-26_040639_PlanMode选择框永久等待/README.md"
    note: "原会话空答案后输出总结的时间线、影响范围、状态契约和停止边界"
  - evidence_id: evidence.doc.acceptance-plan-wait
    type: "acceptance"
    source: "BUG-PLAN-WAIT-20260726-001 验收标准"
    path: "doc/7-验收/2026-07-26_040639_BUG-PLAN-WAIT-20260726-001_验收标准.md"
    note: "AC-PMW-001..007、真实 Desktop 两个以上空答案周期和 LIMITED 口径来源"
  - evidence_id: evidence.skill.autonomous-execution
    type: "skill"
    source: "autonomous-execution-rules/SKILL.md"
    path: "autonomous-execution-rules/SKILL.md"
    note: "开始实施后的周期内最小任务连续执行来源"
  - evidence_id: evidence.skill.style-regression
    type: "skill"
    source: "code-style-consistency-rules/SKILL.md"
    path: "code-style-consistency-rules/SKILL.md"
    note: "测试后的唯一 6-review 风格回归入口"
  - evidence_id: evidence.skill.code-generation-style
    type: "skill"
    source: "code-generation-style-rules/SKILL.md"
    path: "code-generation-style-rules/SKILL.md"
    note: "代码生成前风格契约入口来源"
  - evidence_id: evidence.skill.comment-completion
    type: "skill"
    source: "comment-completion-gate-rules/SKILL.md"
    path: "comment-completion-gate-rules/SKILL.md"
    note: "改动位点注释补齐、步骤编号和代码块长度门槛来源"
  - evidence_id: evidence.skill.comment-placement
    type: "skill"
    source: "comment-placement-granularity-rules/SKILL.md"
    path: "comment-placement-granularity-rules/SKILL.md"
    note: "代码块内步骤注释落点与颗粒度来源"
  - evidence_id: evidence.dialog.comment-block-step-annotation
    type: "dialog"
    source: "用户本轮需求"
    note: "用户要求代码块超过5行时必须进行代码块内步骤注释"
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
    note: "公共工具资格、复用检索、防重复封装和冻结策略来源；目录落点由 package-structure-rules 承接"
  - evidence_id: evidence.skill.package-structure-rules
    type: "skill"
    source: "package-structure-rules/SKILL.md"
    path: "package-structure-rules/SKILL.md"
    note: "包结构、目录分层和子包归位规则来源"
  - evidence_id: evidence.dialog.backend-utils-common-util-placement
    type: "dialog"
    source: "对话确认"
    note: "当前对话确认后端根 utils 与源码根 util 的分流口径"
  - evidence_id: evidence.dialog.backend-database-storage-layout
    type: "dialog"
    source: "对话确认"
    note: "当前对话确认数据存储连接、模型分类、字段 SQL 叶子目录和公开查询兼容口径"
  - evidence_id: evidence.dialog.backend-root-governance-files
    type: "dialog"
    source: "对话确认"
    note: "当前对话确认后端项目根的四个必需治理文件和条件 PROJECT_STYLE 文件"
  - evidence_id: evidence.dialog.project-dual-platform-rule-files
    type: "dialog"
    source: "对话确认"
    note: "用户确认前后端同仓、独立后端和独立前端项目根均应成对保存正文一致的 AGENTS.md 与 CLAUDE.md。"
  - evidence_id: evidence.skill.micro-business-architecture-rules
    type: "skill"
    source: "micro-business-architecture-rules/SKILL.md"
    path: "micro-business-architecture-rules/SKILL.md"
    note: "微业务横向隔离、目标域 rpc 精确导入与 CodeGraph 审查来源"
  - evidence_id: evidence.dialog.micro-business-json-rpc-boundary
    type: "dialog"
    source: "对话确认"
    note: "当前对话冻结业务域 rpc 的 JSON 输入输出和私有层跨域导入禁令"
  - evidence_id: evidence.doc.psr-v2-adoption
    type: "doc"
    source: "代码位置目录规则 V2 旧项目渐进采纳需求"
    path: "doc/2-需求/2026-07-28_014412_代码位置目录规则V2.md"
    note: "冻结收敛清单、adoption 只读检查、遗留快照维护边界和本地验收。"
  - evidence_id: evidence.dialog.legacy-project-directory-adoption
    type: "dialog"
    source: "对话确认"
    note: "当前对话确认旧项目可人工登记相似目录沿用，新业务和独立新逻辑逐步采用 V2。"
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
    note: "用户确认同一任务的需求、实施、Bug、测试说明、6-review、验收和项目状态同步合并为 docs 提交，测试与实现仍独立"
  - evidence_id: evidence.dialog.git-commit-no-review-acceptance-doc
    type: "dialog"
    source: "对话确认"
    note: "用户要求 Git 提交保留审查验收步骤，但不自动生成审查或验收文档"
  - evidence_id: evidence.test.skill-size-report-20260717
    type: "test"
    source: "TASK-SPLIT-01-01 真实统计与验收"
    path: "doc/5-tests/2026-07-17_155229/skill-split-validation/skill-size-report.json"
    note: "报告证明正式注册 skill 84 个、磁盘目录 111 个、排除扩展种子 27 个，并记录各 skill 的字节数与预算等级。"
  - evidence_id: evidence.doc.skill-size-plan-20260717
    type: "doc"
    source: "Skill 体积治理与职责拆分需求及周期 01 文档"
    path: "doc/3-实施/2026-07-16_114619_Skill体积治理与拆分_实施周期01_预算与候选冻结.md"
    note: "需求、验收、实施总览、周期和任务证据统一冻结体积阈值、统计口径、ASCII 测试路径与四项闭环。"
  - evidence_id: evidence.test.skill-split-validation-entry-20260717
    type: "test"
    source: "TASK-SPLIT-01-03 通用测试入口真实验证"
    path: "doc/5-tests/2026-07-17_155229/skill-split-validation/validate_skill_split.py"
    note: "Python/PowerShell help、all、pre-delete、post-delete、py_compile 和仓库/fixture 路径越界负向测试通过；正向退出码为 0，越界按预期非零。"
  - evidence_id: evidence.doc.skill-split-entry-plan-20260717
    type: "doc"
    source: "TASK-SPLIT-01-03 测试入口计划与验收同步"
    path: "doc/3-实施/2026-07-16_114619_Skill体积治理与拆分_实施周期01_预算与候选冻结.md"
    note: "周期、需求、验收、总览、全量顺序方案、README 和 PROJECT_CURRENT 已同步当前入口、边界、失败预期和证据槽位。"
  - evidence_id: evidence.review.skill-split-current-diff-20260717
    type: "review"
    source: "TASK-SPLIT-01-03 当前改动总审查"
    path: "doc/6-审查/2026-07-17_181312_REQ-SKILL-SPLIT-20260716_通用测试入口当前改动审查.md"
    note: "审查确认通用入口、fixture 路由、路径边界和停止边界无 P0/P1，结论为通过。"
  - evidence_id: evidence.accept.skill-split-task-01-03-20260717
    type: "acceptance"
    source: "TASK-SPLIT-01-03 任务验收"
    path: "doc/3-实施/2026-07-16_114619_Skill体积治理与拆分_实施周期01_预算与候选冻结.md"
    note: "TEST-SPLIT-003、工程文档 profile、UTF-8 和真实 skill/字典未修改边界均通过；仅表示测试入口任务完成。"
  - evidence_id: evidence.doc.skill-split-cycle-01-close-20260717
    type: "doc"
    source: "Skill 体积治理与职责拆分周期 01 收口同步"
    path: "doc/3-实施/2026-07-16_114619_Skill体积治理与拆分_实施周期01_预算与候选冻结.md"
    note: "周期文档、测试 README、需求/验收/实施门禁和 PROJECT_CURRENT 已同步完成状态，周期 02 保持未进入。"
  - evidence_id: evidence.obsidian.skill-split-plan-20260717
    type: "knowledge"
    source: "Obsidian 知识流阶段收口沉淀"
    path: "知识库/20-Knowledge/codex-skills/skill-体积治理与职责拆分计划.md"
    note: "通过固定 vault bridge create/readback 沉淀统计口径、候选顺序、五类验证契约和当前周期状态，并通过 bridge append/readback 更新 INDEX。"
  - evidence_id: evidence.skill.task-plan-rehydration
    type: "skill"
    source: "任务投影断点恢复唯一 Owner 与机器契约"
    path: "task-plan-rehydration-rules/SKILL.md"
    note: "定义 v4 多会话 registry、首次继续按 session_id 精确触发、十分钟超时升级、状态同步顺序、UI 与执行授权边界、失活和工具不可用语义。"
  - evidence_id: evidence.doc.task-plan-rehydration-requirement
    type: "doc"
    source: "Codex Desktop 任务悬浮窗断点恢复需求与实施文档"
    path: "doc/2-需求/2026-07-23_012302_CodexDesktop任务悬浮窗断点恢复.md"
    note: "冻结任务投影字段、恢复时机、安全边界、验收标准和五周期实施顺序。"
  - evidence_id: evidence.doc.task-plan-timeout-cycle
    type: "doc"
    source: "Codex Desktop 任务悬浮窗十分钟超时升级实施周期"
    path: "doc/3-实施/2026-07-25_163230_CodexDesktop任务悬浮窗断点恢复_实施周期05_超时自动升级.md"
    note: "冻结严格大于 600 秒、四类暂停、exact/fallback、无后台唤醒和 57 项回归证据。"
  - evidence_id: evidence.doc.task-plan-first-persist-cycle
    type: "doc"
    source: "Codex Desktop 任务悬浮窗首次持久化与立即刷新实施周期"
    path: "doc/3-实施/2026-07-26_150000_BUG-RTP-20260726-001_首次持久化与立即刷新_实施周期07.md"
    note: "冻结 confirmed 后首次持久化、下一动作 update_plan、会话解析、UI_SYNC_BLOCKED 和十分钟异常修复边界。"
  - evidence_id: evidence.skill.session-handoff
    type: "skill"
    source: "session-handoff-rules/SKILL.md"
    path: "session-handoff-rules/SKILL.md"
    note: "会话交接触发词、事实抽取、脱敏、同项目 local 创建、等待和 manual_only 归档边界来源。"
  - evidence_id: evidence.test.session-handoff
    type: "test"
    source: "会话交接包契约测试"
    path: "test/session-handoff-rules/validate_handoff_packet_test.py"
    note: "覆盖有效交接包、next_steps 非空、敏感字段拒绝和字节上限；本地四项断言通过。"
  - evidence_id: evidence.review.session-handoff
    type: "review"
    source: "会话交接 skill 6-review"
    path: "doc/6-review/2026-08-02_033000_会话交接skill_6-review.md"
    note: "记录 UTF-8、目录归位、命名、注释和脚本可读性风格回归结论。"
  - evidence_id: evidence.dialog.session-handoff-triggers
    type: "dialog"
    source: "本轮用户确认的会话交接触发词"
    note: "冻结开新会话继续、新会话中继续、新会话继续、会话太长、归档旧会话、迁移任务、接续任务、提取会话压缩信息和唤起另一个会话。"
contexts:
  - context_id: context.test-asset-governance
    type: "repository-convention"
    name: "测试资产双根治理"
    note: "适用于根 test/ 镜像、源码关联 mock/stub/fake、doc/5-tests/ 证据、历史可执行资产按需迁移、Python 命名和 Go 黑盒路径"
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
  - context_id: context.session-handoff
    type: "task-scope"
    name: "会话交接与新任务接续"
    note: "适用于提取当前会话压缩信息、生成脱敏交接包、同项目 local 创建新任务和人工归档旧任务"
  - context_id: context.task-plan-rehydration
    type: "task-scope"
    name: "任务悬浮窗断点恢复"
    note: "适用于 confirmed 后首次任务投影持久化、立即刷新悬浮列表、Desktop 重开后的首次继续回合、上下文恢复、进行中步骤核验和缺失投影十分钟异常修复"
  - context_id: context.plan-mode-wait-loop
    type: "task-scope"
    name: "Plan Mode 决策永久等待"
    note: "适用于决策选择框空答案串行重发、部分答案合并、单活动框、无限等待和未决总结闸门"
  - context_id: context.final-summary
    type: "task-scope"
    name: "最终总结结果区"
    note: "适用于结果区问题、方法、结果/验证状态的 3 句核心契约，以及复杂、受限或有关键边界时的 4–5 句受控扩展"
lifecycle:
  active:
    - "rule.shared-static-owner-routing"
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
    - "rule.backend-utils-common-util-placement"
    - "rule.backend-database-storage-layout"
    - "rule.backend-root-data-forbidden"
    - "rule.micro-business-json-rpc-boundary"
    - "rule.legacy-project-directory-adoption"
    - "rule.runtime-mock-location"
    - "rule.thread-title-process-trigger"
    - "rule.obsidian-knowledge-flow-selective-default"
    - "rule.obsidian-iterative-knowledge-governance"
    - "rule.git-obsidian-capture-link"
    - "rule.git-commit-domain-split"
    - "rule.git-commit-review-acceptance-evidence"
    - "rule.task-plan-rehydration"
    - "rule.session-handoff"
    - "rule.plan-mode-decision-wait-loop"
    - "rule.reasoning-summary-detail"
    - "rel.old-directory-cleanup.depends-on.doc-top-level-mixed-naming"
  deprecated: []
  stale: []
  conflicted: []
  retired: []
retrieval_hints:
  aliases:
    开新会话继续:
      - "rule.session-handoff"
    新会话中继续:
      - "rule.session-handoff"
    新会话继续:
      - "rule.session-handoff"
    会话太长:
      - "rule.session-handoff"
    归档旧会话:
      - "rule.session-handoff"
    迁移任务:
      - "rule.session-handoff"
    接续任务:
      - "rule.session-handoff"
    提取会话压缩信息:
      - "rule.session-handoff"
    唤起另一个会话:
      - "rule.session-handoff"
    会话交接:
      - "rule.session-handoff"
    交接包:
      - "rule.session-handoff"
    新任务接续:
      - "rule.session-handoff"
    任务投影:
      - "rule.task-plan-rehydration"
    悬浮任务列表恢复:
      - "rule.task-plan-rehydration"
    Desktop 继续任务:
      - "rule.task-plan-rehydration"
    update_plan 重建:
      - "rule.task-plan-rehydration"
    简单任务十分钟升级:
      - "rule.task-plan-rehydration"
    首次持久化立即刷新:
      - "rule.task-plan-rehydration"
    ensure-start:
      - "rule.task-plan-rehydration"
    UI_SYNC_BLOCKED:
      - "rule.task-plan-rehydration"
    ensure-timeout:
      - "rule.task-plan-rehydration"
    Plan Mode 永久等待:
      - "rule.plan-mode-decision-wait-loop"
    空答案循环重发:
      - "rule.plan-mode-decision-wait-loop"
    WAITING_DECISION:
      - "rule.plan-mode-decision-wait-loop"
    SUMMARY-GATE-PMW-001:
      - "rule.plan-mode-decision-wait-loop"
    结果与结论详细度:
      - "rule.reasoning-summary-detail"
    结果区 3–5 句:
      - "rule.reasoning-summary-detail"
    适中详细结论:
      - "rule.reasoning-summary-detail"
    简单任务 3 句:
      - "rule.reasoning-summary-detail"
    复杂任务 4–5 句:
      - "rule.reasoning-summary-detail"
    Skill 体积预算:
      - "fact.skill-size-baseline-20260717"
    84 个正式 skill:
      - "fact.skill-size-baseline-20260717"
    默认文本包:
      - "fact.skill-size-baseline-20260717"
    扩展种子排除:
      - "fact.skill-size-baseline-20260717"
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
    后端 utils 归位:
      - "rule.backend-utils-common-util-placement"
    common/util 归位:
      - "rule.backend-utils-common-util-placement"
    utils 与 common/util 区分:
      - "rule.backend-utils-common-util-placement"
    项目无关工具包:
      - "rule.backend-utils-common-util-placement"
    项目高关联工具函数:
      - "rule.backend-utils-common-util-placement"
    业务域 rpc:
      - "rule.micro-business-json-rpc-boundary"
    微业务 JSON 通信:
      - "rule.micro-business-json-rpc-boundary"
    目标域 rpc 公开入口:
      - "rule.micro-business-json-rpc-boundary"
    旧项目渐进采纳:
      - "rule.legacy-project-directory-adoption"
    收敛清单:
      - "rule.legacy-project-directory-adoption"
    adoption 检查:
      - "rule.legacy-project-directory-adoption"
    code-generation-style-rules:
      - "rule.code-generation-style-contract"
    代码风格契约:
      - "rule.code-generation-style-contract"
    生成代码前风格总控:
      - "rule.code-generation-style-contract"
    代码块五行门槛:
      - "rule.comment-block-step-annotation"
    长代码块步骤注释:
      - "rule.comment-block-step-annotation"
    代码块内步骤注释:
      - "rule.comment-block-step-annotation"
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
    同一任务文档合并提交:
      - "rule.git-commit-domain-split"
    代码实现单独提交:
      - "rule.git-commit-domain-split"
  scopes:
    会话交接:
      - "rule.session-handoff"
    新任务接续:
      - "rule.session-handoff"
    交接包脱敏:
      - "rule.session-handoff"
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
    最终总结:
      - "rule.reasoning-summary-detail"
    结果区详细度:
      - "rule.reasoning-summary-detail"
    结论可复核性:
      - "rule.reasoning-summary-detail"
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
    代码注释:
      - "rule.comment-block-step-annotation"
    注释放置颗粒度:
      - "rule.comment-block-step-annotation"
    函数拆分:
      - "rule.simple-check-inline-readability"
    局部检查:
      - "rule.simple-check-inline-readability"
    可读性:
      - "rule.simple-check-inline-readability"
    后端工具落点分流:
      - "rule.backend-utils-common-util-placement"
    后端数据存储目录:
      - "rule.backend-database-storage-layout"
    后端根 data 禁止路径:
      - "rule.backend-root-data-forbidden"
    独立字段 SQL:
      - "rule.backend-database-storage-layout"
    utils / common/util:
      - "rule.backend-utils-common-util-placement"
    后端公共工具归位:
      - "rule.backend-utils-common-util-placement"
    微业务隔离:
      - "rule.micro-business-json-rpc-boundary"
    跨业务调用:
      - "rule.micro-business-json-rpc-boundary"
    旧项目目录兼容:
      - "rule.legacy-project-directory-adoption"
    遗留源码维护:
      - "rule.legacy-project-directory-adoption"
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
    同一任务文档合并提交:
      - "rule.git-commit-domain-split"
    可执行测试独立提交:
      - "rule.git-commit-domain-split"
  sources:
    session-handoff-rules/SKILL.md:
      - "rule.session-handoff"
    session-handoff-rules/references/handoff-packet-contract.md:
      - "rule.session-handoff"
    session-handoff-rules/references/codex-thread-routing.md:
      - "rule.session-handoff"
    session-handoff-rules/scripts/validate_handoff_packet.py:
      - "rule.session-handoff"
    test/session-handoff-rules/validate_handoff_packet_test.py:
      - "rule.session-handoff"
    doc/6-review/2026-08-02_033000_会话交接skill_6-review.md:
      - "rule.session-handoff"
    编码skill.md:
      - "rule.session-handoff"
    字典.md:
      - "rule.session-handoff"
    skill-dictionary/data.js:
      - "rule.session-handoff"
    task-plan-rehydration-rules/SKILL.md:
      - "rule.task-plan-rehydration"
    task-plan-rehydration-rules/references/task-plan-projection-contract.md:
      - "rule.task-plan-rehydration"
    task-plan-rehydration-rules/scripts/task_plan_projection.py:
      - "rule.task-plan-rehydration"
    doc/2-需求/2026-07-23_012302_CodexDesktop任务悬浮窗断点恢复.md:
      - "rule.task-plan-rehydration"
    doc/3-实施/2026-07-25_163230_CodexDesktop任务悬浮窗断点恢复_实施周期05_超时自动升级.md:
      - "rule.task-plan-rehydration"
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
      - "rule.plan-mode-decision-wait-loop"
    implementation-planning-rules/references/plan-question-coverage.md:
      - "rule.plan-mode-decision-wait-loop"
    implementation-planning-rules/references/plan-output-gate.md:
      - "rule.plan-mode-decision-wait-loop"
    reasoning-summary-structure-rules/SKILL.md:
      - "rule.plan-mode-decision-wait-loop"
      - "rule.reasoning-summary-detail"
    reasoning-summary-structure-rules/references/conditional-sections-rules.md:
      - "rule.reasoning-summary-detail"
    reasoning-summary-structure-rules/references/output-examples.md:
      - "rule.reasoning-summary-detail"
    doc/5-tests/2026-07-26_153733/reasoning-summary-structure-rules/test_result_conclusion_detail.py:
      - "rule.reasoning-summary-detail"
    doc/7-验收/2026-07-26_162000_REQ-SUMMARY-DETAIL-001_最终验收.md:
      - "rule.reasoning-summary-detail"
    doc/4-bugs/2026-07-26_040639_PlanMode选择框永久等待/README.md:
      - "rule.plan-mode-decision-wait-loop"
    doc/7-验收/2026-07-26_040639_BUG-PLAN-WAIT-20260726-001_验收标准.md:
      - "rule.plan-mode-decision-wait-loop"
    doc/5-tests/2026-07-26_040607/plan_mode_wait_loop/test_plan_mode_wait_loop.py:
      - "rule.plan-mode-decision-wait-loop"
    autonomous-execution-rules/SKILL.md:
      - "rule.implementation-cycle-minimum-task"
    code-style-consistency-rules/SKILL.md:
      - "rule.implementation-cycle-minimum-task"
      - "rule.style-regression"
    code-generation-style-rules/SKILL.md:
      - "rule.code-generation-style-contract"
    comment-completion-gate-rules/SKILL.md:
      - "rule.comment-block-step-annotation"
    comment-completion-gate-rules/references/comment-step-numbering-gate.md:
      - "rule.comment-block-step-annotation"
    comment-placement-granularity-rules/SKILL.md:
      - "rule.comment-block-step-annotation"
    comment-placement-granularity-rules/references/comment-placement.md:
      - "rule.comment-block-step-annotation"
    code-readability-rules/SKILL.md:
      - "rule.simple-check-inline-readability"
    code-readability-rules/references/function-structure-rules.md:
      - "rule.simple-check-inline-readability"
    common-util-rules/SKILL.md:
      - "rule.backend-utils-common-util-placement"
    package-structure-rules/SKILL.md:
      - "rule.backend-utils-common-util-placement"
      - "rule.micro-business-json-rpc-boundary"
      - "rule.legacy-project-directory-adoption"
    doc/2-需求/2026-07-28_014412_代码位置目录规则V2.md:
      - "rule.legacy-project-directory-adoption"
    micro-business-architecture-rules/SKILL.md:
      - "rule.micro-business-json-rpc-boundary"
    编码skill.md:
      - "rule.backend-utils-common-util-placement"
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
    artifact-storage-rules/references/naming-templates.md:
      - "rule.runtime-mock-location"
    test-program-rules/SKILL.md:
      - "rule.runtime-mock-location"
    test-program-rules/references/runtime-mock-pattern.md:
      - "rule.runtime-mock-location"
    test-strategy-rules/SKILL.md:
      - "rule.runtime-mock-location"
    test-strategy-rules/references/test-asset-governance.md:
      - "rule.runtime-mock-location"
    package-structure-rules/SKILL.md:
      - "rule.runtime-mock-location"
    package-structure-rules/references/project-layout-v2.md:
      - "rule.runtime-mock-location"
    package-structure-rules/references/placement-catalog.yaml:
      - "rule.runtime-mock-location"
    package-structure-rules/references/runtime-mock-layout-go.md:
      - "rule.runtime-mock-location"
    package-structure-rules/scripts/placement_catalog.py:
      - "rule.runtime-mock-location"
    test/package-structure-rules/runtime_mock_layout_test.py:
      - "rule.runtime-mock-location"
    AGENTS.md:
      - "rule.runtime-mock-location"
    CLAUDE.md:
      - "rule.runtime-mock-location"

extensions:
  external_refs:
    - type: migration-sample
      note: "本轮仅迁移 3 条现有长期记忆作为单文件双区演练样本"
  retrieval_provider: ""
  vector_doc_id: ""
  graph_node_id: ""
```
