## 目录用法索引规则

- 稳定决策：package-structure-rules 是目录用法索引的唯一 Owner，通过 Catalog 条目的 related_skills、usage_recipes、package_alias、example_scope 字段关联专业 skill 和 recipe 示例。
- 稳定决策：guide 子命令按 --category、--technology、--language 查询目录用法，支持 category 别名映射（如 json -> serialization、log -> logging、convert/conversion、message/mq、scheduler/cron）。
- 稳定决策：Go recipe 示例统一存放在 package-structure-rules/references/usage-recipes-go.md，首批覆盖 convert、time、cache/redis、json、log、http；Java/Node/Python 后续按需扩展。
- 稳定决策：新增 recipe 时按流程更新 usage-recipes-go.md、Catalog 条目的 usage_recipes 字段、directory-usage-routing.md 索引表，并运行 guide 子命令验证。
- 来源：package-structure-rules/SKILL.md、package-structure-rules/references/placement-catalog.yaml、package-structure-rules/scripts/placement_catalog.py、package-structure-rules/references/directory-usage-routing.md、package-structure-rules/references/usage-recipes-go.md。
- 更新时间：2026-08-08。

# 项目长期记忆

## 凭据持久化与输出脱敏

- 稳定决策：真实凭据原值可有意持久化于代码、配置、普通维护文档和对应 Git 提交；日志、错误、测试报告与证据、终端输出、Agent 回复、会话交接和自动知识摘要不得回显原值。
- 稳定决策：配置 Catalog 的 YAML 与 embedded 条目均使用 `allow_plain_secret`；`source_policy`、Schema、CLI 参数和返回结构不因该决策改变。
## Decimal 目录规则

- 稳定决策：`utils/decimal/` 是 Decimal 高精度数值类型封装唯一目录，Catalog ID `backend.utils.decimal`，Go 包别名 `decimalUtil`。
- 稳定决策：Decimal 能力覆盖 sql.Scanner、driver.Valuer、ToFloat64、String、Add/Sub/Mul/Div、Cmp/Equals、IsZero/IsPositive/IsNegative、Abs/Round/Max/Min 与四个构造函数（NewDecimalFromFloat64、NewDecimalFromString、NewDecimalFromInt64、NewDecimalFromDecimal）。
- 稳定决策：关联 skill 为 `common-util-rules`、`database-query-rules`、`database-schema-rules`，recipe 索引为 `usage-recipes-go.md#decimal`。
- 来源：`package-structure-rules/references/placement-catalog.yaml`、`package-structure-rules/references/usage-recipes-go.md`、`package-structure-rules/references/backend-util-layout.md`、`package-structure-rules/references/directory-usage-routing.md`、`package-structure-rules/references/project-layout-v2.md`。
- 更新时间：2026-08-09。


## 计划输出完整性规则

- 稳定决策：`implementation-planning-rules` 的正式实施计划必须零决策完整落盘；plan-structure-template.md 禁止在最终输出时压缩或省略思考阶段已形成的任何落点、文件/符号、命令、断言、回滚和完成条件。
- 稳定决策：宿主外层包裹（如 `<proposed_plan>`）的简洁/3-5小节要求仅影响包裹层，不得删减计划正文中的任务字段、细节或零决策事项；仓库模板完整度优先于宿主简洁要求。
- 稳定决策：plan-output-gate.md 硬失败结构包含内容密度 hard-fail：最小任务缺少零决策字段（文件/符号、操作、禁止触碰、精确测试命令、断言、清理、回滚、完成条件、停止条件中任一项）或出现"见上文""后续再定""若干文件""TBD""TODO""实现时再看"等占位词时直接不合格。
- 稳定决策：正式实施计划的主章节仅包含章节标题、各任务缺少可执行具体字段内容即为无效计划；代码变更类计划必须给出代码落点目录树（text 代码块）。
- 稳定决策：正式计划必须跨会话自包含：冻结主项目地址、仓库类型、代码基线、新会话接手第一步、当前周期/任务、local 环境入口和中断点核验顺序；计划不得依赖思考过程、悬浮窗或隐含工作目录。
- 稳定决策：引用其他项目代码必须逐项提供 `EXT-*`、可复现地址、版本/提交、项目根相对路径、文件/符号、用途、许可证/复制边界、可达性失败停止条件和验证回指；无外部引用必须写 `N/A + 原因 + 证据`。
- 来源：`implementation-planning-rules/references/plan-structure-template.md`、`plan-output-gate.md`、`plan-review-checklist.md`、`minimum-task-execution-contract.md`、`implementation-overview-template.md`、`implementation-cycle-template.md`、`plan-entry-checklist.md`、`cross-session-plan-execution-contract.md`、`agents/openai.yaml`、`AGENTS.md`、`CLAUDE.md`、`test/implementation-planning-rules/plan_output_contract_test.py`、`doc/3-实施/2026-08-09_190217_REQ-PLAN-DETAIL-COMPLETE-002_实施总览.md`。
- 更新时间：2026-08-09。


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
- 稳定决策：Goal 摘要来源为已确认实施计划摘要、当前确认目标或固定兜底文案，必须是单行中文、最多 80 个 Unicode 字符并脱敏，只传给 `create_goal`，不得写入项目文件、测试 fixture、工程文档、项目记忆或知识库。
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
- 稳定决策：`config/embedded/` 与 `config/yaml/` 是二选一互斥的配置模式，一个项目只能选择其中一种，不可并存，推荐优先使用 `config/embedded/`。YAML 条目标记为 `yaml_mutually_exclusive`，embedded 条目标记为 `embedded_mutually_exclusive`；两种模式都允许有意持久化真实密钥、密码、token、私钥原值，但 Agent 输出、日志、README、错误和测试报告不得泄露原值。该模型取代旧的“embedded 主来源、YAML 回退并存”口径。
- 来源：`package-structure-rules/references/configuration-layout.md`、`package-structure-rules` Catalog/Schema 改动和配置契约测试。
- 更新时间：2026-08-13。
- 来源：`artifact-delivery-gate-rules/references/plain-language-document-contract.md`、`artifact-delivery-gate-rules/references/review-acceptance-gate-contract.md`、`artifact-delivery-gate-rules/scripts/validate_engineering_docs.py`。
- 更新时间：2026-07-14。

## WorkBuddy 官方市场规则吸收整理补充

- 稳定决策：吸收官方市场同类 skill 时以「整理补充」为原则，不是无限制累加，也不是整套复制。本地规则已经更完整的方向只做归纳；官方真正更优的少量动作才吸收进既有 skill 的 `references/`；不新建同类 skill，不复制官方工作流、问答链或目录结构。
- 稳定决策：需求域吸收官方 100 分质量门，落为 `requirement-intake-rules/references/workbuddy-quality-gate.md`；实施域吸收「编码前先探索代码库」，落为 `implementation-planning-rules/references/pre-implementation-code-exploration.md`；Bug 域吸收「修复前先分级风险并确认」，落为 `bug-fix-proposal-rules/references/fix-risk-grading-and-confirmation.md`；测试域吸收「风险分层后给出明确测试结论」，落为 `test-strategy-rules/references/risk-based-test-conclusion.md`。
- 来源：`implementation-planning-rules/references/workbuddy-absorption-map.md`、四个 skill 的 references、`doc/2-需求/2026-08-13_110000_WorkBuddy官方市场规则吸收整理补充.md`。
- 更新时间：2026-08-13。

## 任务阻断收口与恢复规则

- 真实阻断唯一使用 `artifact-delivery-gate-rules/references/task-blocker-closure-contract.md` 的 `BLK-*` 记录，至少包含任务状态、阻断阶段、依据与证据、已尝试动作与停止边界、影响、至多三步解决计划、恢复后重入点、去重键和必填字段“用户授权操作”。
- 稳定决策：真实阻断收口必须展示“用户授权操作”，用户只需回复“同意授权”即可授权执行最近一条、唯一有效、仍未解除的 `BLK-*` 记录列明的恢复动作，回复“暂不授权”保持阻断；授权后必须执行原恢复步骤并通过原验证入口，验证失败保持阻断；授权不构成跨任务、跨会话或未来任意写入的通用许可。
- 审查、验收、功能验证、Bug 验证、执行失败和运行时恢复只生产或校验阻断事实；`reasoning-summary-structure-rules` 是唯一面向用户渲染“任务阻断收口”的 owner，避免多处输出冲突计划。
- 仅 `blocked` 与 `manual_handoff` 触发任务阻断收口。`limited`、`not_applicable`、P2/P3、用户取消和预期负向测试不得生成 `BLK-*` 或写成任务已阻断。
- 阻断计划最多三步；每步必须包含责任方、前置条件、动作、完成判据和验证入口。恢复后从原测试、复审、重验或健康检查的重入点继续。
- 文档校验的正文 `N/A` 规则忽略 fenced code、示例与 Mermaid 内容，避免图中“不适用”分支被误判；正文声明仍必须给出原因或证据。
- 来源：`artifact-delivery-gate-rules/references/task-blocker-closure-contract.md`、`reasoning-summary-structure-rules/SKILL.md`、`artifact-delivery-gate-rules/scripts/validate_engineering_docs.py`、`doc/2-需求/2026-08-09_214745_REQ-BLK-AUTH-001_任务阻断授权操作提示.md`、`test/artifact-delivery-gate-rules/blocker_authorization_contract_test.py`。
- 更新时间：2026-08-09。

## Windows PowerShell 环境可靠性规则

- `windows-powershell-environment-rules` 的会话默认策略是 `RequiredOnly`：`ready` 和 `degraded` 可以继续，只有 `blocked`、`busy`、`failed`、`rollback_refused` 不能作为已准备好结论。
- 包恢复只接受 manifest 或调用方提供的精确 source/package ID；未知命令不搜索猜包。Git Bash 只能从 Git 安装根目录的 `bin\\bash.exe` 加 `MINGW|MSYS` 身份识别，WSL 原生命令不再由 `windows-wsl-execution-rules` 承接（该 skill 已删除，由 `wsl-windows-bridge` 提供 WSL↔Windows 工具桥）。
- profile 与 Terminal 的 Apply/Rollback 由事务、备份和 after hash 保护；WhatIf 不写用户状态，hash 漂移时必须拒绝覆盖。含中文的 PowerShell 5.1 脚本使用 UTF-8 BOM，避免被默认 ANSI 解码。
- 验证固定为临时目录 fixture：PowerShell 5.1 与 PowerShell 7 都要通过 TEST-PSENV-001 至 TEST-PSENV-009；不连接网络、不安装软件、不改真实用户配置。
- 稳定决策：任何一次调用 PowerShell 命令（不是进入交互式终端）都必须显式使用 `-NoProfile -ExecutionPolicy Bypass -Command`；5.1 回退路径还要先在命令体设置 `[Console]::OutputEncoding = [System.Text.Encoding]::UTF8`，7 路径继续优先 `pwsh -NoLogo -NoProfile -ExecutionPolicy Bypass -Command`。标准调用前缀唯一真源随 `windows-wsl-execution-rules` 删除而撤销，现以 `windows-encoding-rules/SKILL.md` 内联前缀为唯一真源，`windows-encoding-rules` 与 `windows-powershell-environment-rules` 只做交叉引用。
- 来源：`windows-powershell-environment-rules/SKILL.md`、`references/runtime-state-contract.md`、`windows-encoding-rules/SKILL.md`、`doc/2-需求/2026-08-14_223800_PowerShell控制继续优化.md`、`doc/3-实施/2026-08-14_223800_PowerShell控制继续优化_实施总览.md`、`doc/3-实施/2026-08-14_223800_PowerShell控制继续优化_实施周期01_标准调用前缀与三skill衔接.md`。
- 更新时间：2026-08-14。

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
- 定义: 根 `test/` 是唯一活动测试代码根，测试程序、mock、stub、fake、fixture、helper 与启动脚本按被测源码或 Skill 目录镜像存放；源码关联模拟程序必须与对应测试使用同一源码相对路径，只有跨源码复用的模拟能力才进入 `test/shared/`；Python 统一使用 `*_test.py`，模拟程序使用 `_mock`、`_stub` 或 `_fake` 后缀。`doc/5-tests/` 每轮只保存一份扁平测试主文档 `YYYY-MM-DD_HHmmss_<测试任务中文主题>.md`，日志、报告、截图与非可执行产物内联在正文；`doc/5-tests/基线/` 是唯一豁免子目录，上线接口测试机器产物落在 `test/release-artifacts/`。历史 `doc/5-tests/` 子目录及其中的可执行资产由指纹清单只读保护，首次修改、改名或新增时才迁至根 `test/`；Go 测试仅在根 `test/` 的 ASCII 外部黑盒包中运行，源码目录禁止 `*_test.go`。
- 来源: `artifact-storage-rules/references/path-map.yaml`、`test/shared/layout_policy.py`、`doc/3-实施/2026-08-01_191658_根test目录统一_实施总览.md`
- 适用范围: 新增测试、测试资产迁移、测试策略、测试程序、真实测试归档和 6-review 目录归位
- 更新时间: 2026-08-01
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

- 规则变更的完整历史以 git 提交历史为准；关键事件追加到 `PROJECT_HISTORY.md`（保留最近 20 条）；当前生效口径以对应 skill 的 `SKILL.md` 与 `AGENTS.md` 为事实源。
- 本小节只保留最近 10 条尚未沉降到上述三处的过渡性记录，超出即删除，不做无限堆积。历史上本节曾堆积 75 条日期流水共 19KB，违反本文件「只保存稳定规则、关键决策和少量长期事实」的职责定义，且因缺少上限而持续增长；2026-08-12 已清空，逐条核对其当前口径均已被 skill 文件或 `AGENTS.md` 承接。
- 2026-08-12：变更记录清空并加保留上限；跨项目通用判据迁往知识库，本文件只留本仓库落地口径与指针。


## Skill 体积治理与职责拆分

- 稳定统计口径：正式字典主规划有 84 个 skill，磁盘有 111 个带 `SKILL.md` 的目录，其中 27 个属于扩展种子，不纳入正式预算基线；默认文本包按 `SKILL.md` 与直接 references 文本字节数统计。
- 稳定测试契约：通用入口覆盖 `size`、`mapping`、`trigger`、`pre-delete`、`post-delete` 五类模式；报告和矩阵路径不得越出仓库根目录，fixture 根不得越出当天测试时间戳目录；越界必须非零失败且不得删除真实 skill。
- 当前状态：2026-07-17 已完成周期 01 的三个最小任务；2026-08-01 起闭环口径统一为“实施计划完成条件 -> 实现 -> 真实测试 -> 6-review”。周期 01 已收口，周期 02 尚未进入，真实 skill、字典和 Git 历史保持未修改。
- 证据来源：需求、验收、实施总览、实施周期 01、测试 README、当前改动审查报告和 `validate_skill_split.py` 的本地验证结果。
- 知识库沉淀：`20-Knowledge/codex-skills/skill-体积治理与职责拆分计划.md`，并已更新 `INDEX.md` 导航入口。
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
- 稳定决策：独立后端配置唯一根为 `config/`，前后端同仓的后端配置唯一根为 `backend/config/`；`config/yaml/` 与 `config/embedded/` 是二选一互斥的配置模式，一个项目只能选择其中一种，不可并存，推荐优先使用 embedded。常见多环境 YAML 使用 `yaml/config_local.yaml`、`yaml/config_test.yaml`、`yaml/config_prod.yaml`，Go 源码内嵌配置格式名必须后置，使用 `embedded/config_local_yaml.go`、`embedded/config_test_yaml.go`、`embedded/config_prod_yaml.go`；环境集合可扩展，不要求所有环境齐全。格式名后置的原因是 `config_test.go` 会被 Go 当成测试文件并排除出 `go build`，因此 `embedded/config_<env>.go` 属于非法旧命名；环境名同样不得以 `_yaml` 结尾。外部 YAML 不参与编译，保持 `config_<env>.yaml`，不加 `_yaml` 后缀。文件名契约只对 `.go` 强制，其他语言的 embedded 仍只校验源码扩展名；`check` 只读，`init` 不生成动态环境配置文件。YAML 与 embedded 都允许有意持久化真实密钥、密码、token、私钥原值，但 Agent 输出、日志、README、错误和测试报告不得泄露原值。config/ 根允许直接存放 `load.<ext>`（配置加载与解析入口）与 `model.<ext>`（配置结构定义）两个源码文件，条件提交且 `init` 不创建；`config/yaml/` 与 `config/embedded/` 只存放配置数据。
- 稳定决策：fullstack、backend、frontend 三类项目统一使用项目根 `test/` 作为活动测试代码唯一入口；独立后端使用根 `test/`，不建立 `backend/test/`；前后端同仓也不建立 `backend/test/` 或 `frontend/test/`。Catalog 的测试目录 Owner 为 `test-strategy-rules`，`doc/5-tests/` 只保存测试说明和非可执行证据，不能替代根 `test/`。
- 稳定决策：前后端同仓、独立后端、独立前端三类项目根都必须直接保存并提交 `Dockerfile`。Catalog 以 `project-governance/dockerfile` 的必需文件条目建模，`init` 自动创建空文件位置；`strict` 只读拒绝缺失或被目录占用，`adoption` 保持旧项目渐进采纳，不强制补迁移文件。
- 稳定决策：业务域直连源码根 `<source-root>/<domain>/`，去掉 `business/` 中间层；业务相关逻辑完全通过版本目录 `<v?>`（`v1` 起，命名 `v[0-9]+`）隔离，`router/`、`controller/`、`entity/`、`service/` 下沉到版本目录内（`service/` 必建），`api/`、`base/`、`constant/`、`util/`、`crontask/` 为跨版本通用业务逻辑。域级初始化入口为单文件 `init.<ext>`（`<ext>` 为语言扩展名），全量注册本域所有版本路由并以 `/v1`、`/v2` 前缀区分、多版本并存对外，旧版本不因新版本诞生而下线、也不冻结。目录树用 `<source-root>` 占位符多语言统一（Go=`internal/`、Java=`src/main/java/<包>`、Node=`src/`、Python=`src/<包>`），不单为 Go 定 `internal/` 树。
- 稳定决策：完全移除 `rpc/` 跨业务公开入口；业务域之间禁止直接 import 对方任何目录（无 rpc 例外），跨域共享结构仅走根 `common/` 与 `global/` 非业务运行引用。机器事实源 `placement-catalog.yaml` 的 `router`/`controller` 已改版本级条目（含 `<source-root>`/`<domain>`/`<v?>` 占位符与 `requires_domain`）、`business-rpc` 条目已删除；`micro_business.py` 提供 `scaffold <域>`（建版本骨架 + 单文件 `init.go`）、`check`（校验域间禁止直连）、`check --detect-new`（候选新项目三态判定）。
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

- 稳定决策：`reasoning-summary-structure-rules` 的最终总结新增条件小节 `## 📚 知识引用`，用「本轮引用」三列表与「本轮沉淀」四列表承载知识库事实；原先分散在「方案与根因」和「结果与结论」的两处单行摘要口径已作废。
- 稳定决策：无真实阻断时末尾顺序按引用台账分流——台账非空由知识引用收尾、改动点紧邻其前；台账为空由改动点收尾；真实阻断时两者都在阻断收口之前。
- 稳定决策：`knowledge-flow` 每次读取、创建、追加笔记成功后必须立即登记引用台账（笔记名、所在目录、本轮用途、`status`、操作、回读结果六字段）；台账是会话内事实，不写入知识库、不落盘项目文件。
- 稳定决策：只有真实读取成功的笔记可进引用表，检索命中未读取的一律不得入表；引用小节每一行都必须能回指一次成功返回的文件读/写调用。
- 稳定决策：笔记名一律取自读写笔记时所用相对路径的文件名部分。（原附带的「禁止使用 CLI 回显文本，因官方 CLI 回显中文乱码」理由已于 2026-08-12 随 CLI 链路废除而失效）
- 事实更新：知识库根目录已迁至 `D:\谷歌云盘\知识库\`，读写均通过标准文件工具直接完成，不再依赖任何 CLI 前置注册。
- 来源：`reasoning-summary-structure-rules/SKILL.md`、`references/summary-structure-template.md`、`references/conditional-sections-rules.md`、`knowledge-flow/references/capture-retrieve-distill.md`、`doc/2-需求/2026-08-04_总结知识引用清单_Obsidian引用可视化.md`、`doc/3-实施/2026-08-04_总结知识引用清单_实施周期21_Obsidian引用可视化.md`。
- 更新时间：2026-08-04。

## 知识库可迭代更新规则

- 稳定决策：知识库从只增量补充改为可迭代更新。写入前必须显式判定 `补充` / `矛盾未裁决` / `取代` 三态之一；判为取代必须在同一轮内处置旧笔记，只写新笔记不处置旧笔记是禁止行为。
- 稳定决策：取代按旧笔记剩余价值分三档——仍有历史参考价值改 `status: superseded` 并标 `superseded_by`；完全失效且反向链接为 0 改 `status: archived` 后移动到 `90-Archive/`；内容错误或有害 `delete` 进回收站并在新笔记记录旧错误说法。
- 稳定决策：三档处置前必须先用 Grep 扫 `[[笔记名]]` 统计反向链接，引用数不为 0 时不得移动或删除，只能降级为标记取代；接替关系必须双向写入 `supersedes` 与 `superseded_by`，只写一侧视为治理未闭环。
- 稳定决策：`superseded` 与 `archived` 状态的笔记不得作为当前事实，检索命中时顺着 `superseded_by` 跳到接替笔记；执行失败案例笔记不适用三档处置，仍只能追加状态事件，禁止对该目录做移动与删除。
- 稳定决策：三档处置由 agent 自动执行，但每次改属性、移动、删除都必须在最终总结的知识引用小节如实登记。
- 已取代（2026-08-12）：原 bridge 16 命令白名单（`property-read`/`properties`/`property-set`/`move`/`delete`/`backlinks`/`files`/`orphans` 等）随 CLI 链路整体废除，改由标准文件工具完成；frontmatter 属性用 YAML 解析读写，反向链接与孤儿笔记用 Grep 扫 `[[wikilink]]` 统计。
- 已取代（2026-08-12）：CLI stdout 编码归因与 bridge `reconfigure(encoding="utf-8")` 修复随 bridge 脚本删除而失效；当前所有笔记读写显式指定 UTF-8。
- 已取代（2026-08-12）：`properties` 严格模式探测口径随 CLI 废除失效；文件存在性直接由文件系统判断。
- 关键事实：读取笔记元信息直接解析文件头部的 YAML frontmatter；部分笔记没有 frontmatter，取不到状态字段时按无状态处理。
- 来源：`knowledge-flow/references/conflict-staleness.md`、`references/capture-retrieve-distill.md`、`references/note-schema.md`、`scripts/audit_vault_knowledge.py`、`doc/2-需求/2026-08-05_知识库可迭代更新_冲突取代与废弃治理.md`。
- 更新时间：2026-08-05。

## PROJECT_MEMORY / PROJECT_STYLE 到知识库的选择性沉淀规则

- 稳定决策：`PROJECT_MEMORY.md`/`PROJECT_STYLE.md` 与知识库的"本地上下文 vs 跨项目知识库"边界不变；新增的是一条"单条可复用事实"选择性通道，不是整份文件同步或镜像备份，核心标准定义在 `knowledge-flow/references/project-memory-sync.md`。
- 稳定决策：判断是否跨项目可复用采用两层分工——初判层由 `project-memory-rules`/`project-style-rules` 在写入条目的同一步骤完成，标准是"通用性删除测试"（去掉项目名、具体表名/字段名、具体服务名等专属信息后条目是否仍然成立）叠加类型白名单、适用范围显式标注为通用、状态为启用四条，全部满足才追加可选字段 `bridge_candidate: true` / `跨项目候选: 是`；这一步不写入知识库，不产生知识库副作用。
- 稳定决策：复核与落地层由 `knowledge-flow` 在既有"总结阶段捕获流程"（会话总结、阶段收口或最终回复前）完成，把候选条目作为新增信息来源纳入既有扫描，套用既有排除规则二次核验后，选择性沉淀到 `20-Knowledge/project-rules/`（来自 project-memory-rules）或 `20-Knowledge/code-style/`（来自 project-style-rules）；不新增知识库四态之外的第五种状态，只是"沉淀"分支下的新增信息来源。
- 稳定决策：去重固定为"先检索、命中则追加、未命中才新建"，知识库侧笔记只保留脱敏后的通用表述与 `source_refs` 来源引用，不摘录项目原文；`skill-hit-check-rules` 的命中清单同步补充识别信号，避免候选标记被漏判为"不适用"。
- 来源：`knowledge-flow/references/project-memory-sync.md`、`knowledge-flow/SKILL.md`、`knowledge-flow/references/capture-retrieve-distill.md`、`knowledge-flow/references/knowledge-layout.md`、`project-memory-rules/SKILL.md`、`project-memory-rules/references/project-knowledge-source-contract.md`、`project-style-rules/SKILL.md`、`skill-hit-check-rules/references/hit-checklist.md`、用户在 Plan Mode 确认的方案（`C:\Users\luode\.claude\plans\project-memory-md-project-style-md-obsi-fancy-wand.md`）。
- 更新时间：2026-08-05。

## 知识库承载体迁移与路径前缀规则

- 稳定决策：知识库承载体从 Obsidian vault `D:\obsidian_data` 迁移到 Google Drive 同步目录 `D:\谷歌云盘\知识库\`，多端同步交给 Google Drive 客户端。选择这条路线的原因是 Obsidian 的同步不如谷歌云硬盘方便，且知识库退化成普通 Markdown 文件夹后不再依赖 Obsidian 应用运行。
- 稳定决策：CLI 桥接层整体废除。`obsidian_cli_bridge.py`、`obsidian_cli_windows.ps1`、`distill_vault.py` 已删除，所有笔记的检索、读取、创建、追加、移动、删除统一改用标准文件工具，写入后回读校验取代原 `verified=true` 判据。原「不得用 `rg`/`Get-Content`/`Set-Content` 冒充 vault 操作」这条禁令方向已完全反转——文件工具现在是唯一正确通道。
- 稳定决策：笔记路径基准是**相对知识库根的裸相对路径**（如 `20-Knowledge/topic/note.md`），**禁止再加 `知识库/` 前缀**。根目录本身已经是 `知识库`，前缀叠加会生成嵌套目录 `D:\谷歌云盘\知识库\知识库\`。这正是 2026-08-12 发现嵌套目录的根因，且该错误约定在 Obsidian 时代就已存在（原 `D:\obsidian_data\知识库\知识库\` 同样是它的产物）。知识库现有 `INDEX.md` 的 wikilink 一直用的就是裸相对路径，是正确写法的既有证据。
- 稳定决策：`obsidian-knowledge-flow` skill 更名 `knowledge-flow`；每轮首条中间进度的状态字段由 `Obsidian:<检索/沉淀/不适用/阻断>` 改为 `知识库:<检索/沉淀/不适用/阻断>`。四态语义保留，只有 `阻断` 判据改为「知识库目录不存在或不可读 / 路径不合法 / 写入后回读不一致」。
- 关键事实：知识库内容治理同步完成——嵌套层 1 篇实质笔记合并回 `20-Knowledge/研发流程/`，4 篇已作废 Obsidian CLI 笔记与 Obsidian 默认欢迎页删除，2 处散落文件归位到标准布局，`INDEX.md` 死链与过期措辞清理，笔记总数 65→59，全库 wikilink 无新增死链。blog-data 系列笔记里的 "Obsidian vault" 是源 vault 的真实来源事实，按历史事实保留不改。
- 来源：`knowledge-flow/SKILL.md`、`knowledge-flow/references/file-operations.md`、`knowledge-flow/references/knowledge-layout.md`、`AGENTS.md`、`CLAUDE.md`、`project-rule-file-bootstrap-rules/scripts/bootstrap_agents.sh`、用户在 Plan Mode 确认的方案（`C:\Users\luode\.claude\plans\d-mellow-hippo.md`）。
- 更新时间：2026-08-12。

## 知识库检索准召与主题收敛规则

- 跨项目判据见知识库笔记 `知识库检索失效的三种模式与修法`（手写导航覆盖率必然衰减、分类目录自由生长会散落同一主题、纯结构化索引会漏检正文、索引新鲜度要自动处理）。
- 本仓库落地：检索第一跳固定为 `python knowledge-flow/scripts/knowledge_index.py query --keyword "<词>"`，覆盖全库，按六类结构化字段加正文匹配并返回命中原因；索引 `_index.json` 是可再生成物，过期自动重建。
- 本仓库落地：`20-Knowledge` 固定 7 个中文主题（项目、代码规则、工程实践、研发流程、AI协作、数据清洗、开发环境）加 3 个契约固定落点（`execution-failure-cases`、`project-rules`、`code-style`，保留英文因被其它 skill 硬编码引用）；有常驻断言锁定「实际目录 ⊆ 声明清单」。
- 本仓库落地：笔记路径一律为相对知识库根的裸相对路径，禁止带 `知识库/` 前缀（会生成嵌套目录）。
- 更新时间：2026-08-12（判据已迁知识库，此处只留本仓库落地口径）。


## 知识库沉淀触发与契约强制规则

- 跨项目判据见知识库笔记 `知识库沉淀失效的三种模式与修法`（触发条件不能是主观描述、契约要有机器强制、下游机制零使用往往是上游输入不可信、BOM 会让头部判定静默失效等）。
- 本仓库落地：沉淀触发硬信号清单在 `knowledge-flow/references/capture-retrieve-distill.md` 的「沉淀触发硬信号」；判断依据写进状态字段（如 `知识库:沉淀（命中信号2 推翻旧归因）`），只要求写明依据、不要求每轮必须有沉淀。
- 本仓库落地：头部合规入口是 `python knowledge-flow/scripts/knowledge_index.py check`，校验活动区必填六字段与状态枚举，不合规返回非零退出码可当闸门；`90-Archive/` 按只读归档豁免。
- 本仓库落地：冲突候选归组条件为「(同主题 且 共享标签 ≥2) 或 标题相似度 ≥ 0.72」，下限常量 `MIN_SHARED_TAGS` 有断言锁定；标题相似度是跨主题例外通道。
- 更新时间：2026-08-12（判据已迁知识库，此处只留本仓库落地口径）。


## 代码风格规则生效层级规则

- 跨项目判据见知识库笔记 `规则与共用定义的落点决定其有效性`（规则要落在动作前会被读取的入口才生效，四层落点效力分层）。
- 本仓库落地：写码前强制加载入口是 `code-style-consistency-rules/references/user-style-feedback-library.md` 的 active 条目；Go 改动默认补读 `references/go-coding-rules.md`。只写 `SKILL.md` 正文或 `consistency-examples.md` 等于放在事后复盘层，拦不住生成。
- 本仓库分流：跨项目通用偏好走 `style-feedback-workflow.md` 的 candidate→用户确认→active 流程写入全局反例库；项目专属一次性约定才走 `PROJECT_STYLE.md`（边界依据 `project-style-rules/SKILL.md:51`）。
- 更新时间：2026-08-12（判据已迁知识库，此处只留本仓库落地口径）。


## 机器索引区

```yaml
version: 1
entities:
  - entity_id: rule.knowledge-iterative-governance
    name: "知识库可迭代更新与分级处置"
    type: "知识库治理规则"
    aliases:
      - 三档处置
      - 知识库迭代更新
      - superseded_by 接替关系
      - 知识库巡检
    definition: "写入知识库前必须显式判定补充、矛盾未裁决或取代三态之一；判为取代须在同一轮内按剩余价值分三档处置旧笔记：有历史参考价值改 status=superseded 并标 superseded_by，完全失效且反向链接为 0 改 status=archived 后移动到 90-Archive/，内容错误或有害则删除。三档前必须先用 Grep 扫 [[笔记名]] 统计反向链接，引用不为 0 只能标记取代；接替关系双向写入 supersedes 与 superseded_by，superseded_by 非空时 status 不得为 active。superseded 与 archived 不作当前事实，检索时顺 superseded_by 跳到接替笔记。执行失败案例笔记不适用三档处置，禁止对该目录做移动与删除。三档由 agent 自动执行但必须在总结的知识引用小节登记。已积压冲突用只读脚本 audit_vault_knowledge.py 出候选，脚本零写入。2026-08-12 起承载体为 D:\\谷歌云盘\\知识库\\，读写改用标准文件工具，原 bridge 16 命令白名单已废除。"
    scope: "知识库写入、检索、冲突处置与积压巡检"
    status: "active"
    evidence_ids:
      - evidence.knowledge-iterative-governance
    context_ids:
      - context.knowledge-flow
    updated_at: 2026-08-12
  - entity_id: rule.summary-knowledge-citation-section
    name: "总结知识引用小节与引用台账"
    type: "总结结构与知识库规则"
    aliases:
      - 知识引用小节
      - 引用台账
      - 知识库引用清单
    definition: "最终总结在无真实阻断时按引用台账分流收尾：台账非空输出 ## 知识引用 作为最后一节，用「本轮引用」三列表（序号、笔记、本轮用途）与「本轮沉淀」四列表（序号、笔记、操作、readback）承载，改动点紧邻其前；台账为空整节省略且由改动点收尾。knowledge-flow 每次读取/创建/追加笔记成功后立即登记六字段台账；只有真实读取成功的笔记可入引用表，检索命中未读取的不得入表；笔记名取自读写笔记时所用相对路径的文件名部分；笔记 status 为 stale/deprecated/retired/conflicted 时在用途列标注。"
    scope: "最终总结渲染、知识库检索与沉淀登记、总结条件字段判定与驳回标准"
    status: "active"
    evidence_ids:
      - evidence.summary-knowledge-citation-section
    context_ids:
      - context.knowledge-flow
    updated_at: 2026-08-12
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
    name: "运行时 Mock 目录规则"
    type: "目录规则"
    aliases:
      - 根 mock 目录
      - 运行时 Mock
      - mock 构建标签
      - selector 配对
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
    definition: "高风险工具调用前进入 prevent 预检，非预期失败进入 recover 分类、查库和同输入同成功标准复验，验证通过后才进入 learn。案例正文只归属于唯一 owner Skill；无维护授权保持 candidate，冲突标记 conflicted，业务 Bug、Skill 缺口和跨项目知识分别回流 bug-*、skill-evolution-rules 与 knowledge-flow。"
    scope: "imagegen、Windows/WSL、浏览器、认证 URL、MCP/插件安装、知识库文件读写及后续注册的高风险执行域"
    status: "active"
    evidence_ids:
      - evidence.skill.execution-failure-learning
      - evidence.test.execution-failure-learning
    context_ids:
      - context.execution-failure-learning
    updated_at: 2026-08-12
  - entity_id: rule.task-blocker-closure
    name: "任务阻断收口与恢复"
    type: "流程规则"
    aliases:
      - BLK-* 阻断记录
      - 任务已阻断
      - 解决计划与重入点
      - 同意授权
      - 暂不授权
    definition: "真实阻断只以共享 BLK-* 契约记录，生产者只提供结构化事实，reasoning-summary-structure-rules 唯一渲染用户可见收口。记录必须包含状态、阶段、证据、已尝试动作、停止边界、影响、至多三步恢复计划、重入点、去重键和必填字段'用户授权操作'；用户回复'同意授权'可授权最近一条唯一有效未解除记录的恢复动作，'暂不授权'保持阻断，授权后走原验证入口且失败保持阻断；limited、not_applicable、P2/P3、用户取消与预期负向测试不触发。"
    scope: "审查、验收、功能验证、Bug 验证、执行失败、运行时恢复、最终总结与文档门禁"
    status: "active"
    evidence_ids:
      - evidence.doc.task-blocker-closure
      - evidence.test.task-blocker-closure
    context_ids:
      - context.task-blocker-closure
    updated_at: 2026-08-09
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
  - entity_id: rule.micro-business-domain-isolation
    name: "微业务业务域隔离与版本目录"
    type: "包结构与业务隔离规则"
    aliases:
      - 业务域隔离
      - 版本目录
      - 域间禁止直连
      - 业务域直连源码根
    definition: "业务域直连源码根 <source-root>/<domain>/，业务相关逻辑完全通过版本目录 <v?>（v1、v2…）隔离，其余为跨版本通用业务逻辑；域级入口为单文件 init.<ext>，全量注册本域所有版本路由并以 /v1、/v2 前缀区分、多版本并存对外。业务域之间禁止直接 import 对方任何目录（无 rpc 例外），跨域共享结构仅走根 common/ 与 global/ 非业务运行引用。"
    scope: "后端微业务目录、跨业务导入隔离、版本目录语义、CodeGraph 导入审查"
    status: "active"
    evidence_ids:
      - evidence.skill.package-structure-rules
      - evidence.skill.micro-business-architecture-rules
      - evidence.dialog.micro-business-domain-isolation
    context_ids:
      - context.code-generation-style
    updated_at: 2026-08-18
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
  - entity_id: rule.knowledge-flow-selective-default
    name: "知识库知识流选择性默认触发链"
    type: "流程规则"
    aliases:
      - knowledge-flow
      - 知识库知识流
      - 选择性默认触发
      - 知识库检索沉淀
    definition: "项目启动先按父目录平台规则 -> PROJECT_CURRENT.md -> PROJECT_MEMORY.md 读取本地上下文；current 覆盖维护且不超过 51,200 字节，memory 只承载稳定规则与关键决策，history 追加关键事件并只保留最近 20 条（自动裁剪、按日期倒序）且普通启动不读。知识库固定使用 D:\\谷歌云盘\\知识库\\，笔记路径为相对该根的裸相对路径且禁止再加 知识库/ 前缀，仅在跨项目历史或既有知识库内容依赖时通过标准文件工具检索 / 读取，仅在收口形成可复用知识时先检索再沉淀；普通任务不为形式读写知识库，目录不可达 / 路径不合法 / 写入后回读不一致时阻断。项目本地 Markdown 与知识库落点不得混用。"
    scope: "记忆域、命中检查、阶段收口、最终总结、知识库检索与沉淀"
    status: "active"
    evidence_ids:
      - evidence.skill.knowledge-flow
      - evidence.skill.skill-hit-check
      - evidence.doc.repo-rules
      - evidence.doc.skill-plan
    context_ids:
      - context.knowledge-flow
      - context.memory-domain
    updated_at: 2026-08-12
  - entity_id: rule.legacy-windows-wsl-bridge-boundary
    name: "知识库 Windows/WSL bridge 固定执行边界（已取代）"
    type: "跨宿主执行规则"
    aliases:
      - obsidian_cli_bridge
      - Windows/WSL CLI bridge
      - bridge-only vault
    definition: "【2026-08-12 整体取代，仅作历史脉络保留】原口径：Windows 与 WSL 的 Obsidian 检索、创建、追加、读取和 INDEX 更新统一经 obsidian_cli_bridge.py，最终由 Windows 官方 CLI 操作唯一 vault 根 D:\\obsidian_data，WSL 仅通过 PowerShell interop，写入必须 verified=true readback。该 bridge 与 PowerShell 适配器脚本已删除，跨宿主 transport、selector 解析、应用恢复与分块读回等约束一并作废；现由 knowledge-flow 用标准文件工具直接读写 D:\\谷歌云盘\\知识库\\，写后回读校验取代 readback。"
    scope: "（历史）Windows/WSL 知识流、bridge transport、长正文分块与读回验证"
    status: "superseded"
    evidence_ids:
      - evidence.skill.knowledge-flow
      - evidence.doc.repo-rules
    context_ids:
      - context.knowledge-flow
      - context.memory-domain
    superseded_by:
      - rule.knowledge-base-migration-path-prefix
    updated_at: 2026-08-12
  - entity_id: rule.git-knowledge-capture-link
    name: "Git 协作联动知识库沉淀"
    type: "流程规则"
    aliases:
      - 提交前知识捕获
      - Git 收口沉淀
      - commit 联动知识库
    definition: "当本仓库出现提交、推送、PR 收口或交付说明准备，且本轮形成可复用事实、决策、流程、定义、偏好、来源或调试经验时，优先命中 `knowledge-flow` 做 `知识库:沉淀` 判定；沉淀只负责知识捕获，不构成 `git commit` / `git push` 授权。"
    scope: "提交流程、交付收口、知识库记忆沉淀"
    status: "active"
    evidence_ids:
      - evidence.skill.knowledge-flow
      - evidence.skill.git-collaboration
      - evidence.dialog.git-knowledge-capture-link
    context_ids:
      - context.knowledge-flow
      - context.git-collaboration
      - context.memory-domain
    updated_at: 2026-08-12
  - entity_id: rule.knowledge-base-migration-path-prefix
    name: "知识库承载体迁移与裸相对路径基准"
    type: "知识库治理规则"
    aliases:
      - 谷歌云盘知识库
      - 裸相对路径
      - 禁止知识库前缀
      - 嵌套知识库目录
    definition: "知识库承载体从 Obsidian vault D:\\obsidian_data 迁移到 Google Drive 同步目录 D:\\谷歌云盘\\知识库\\，多端同步交给 Google Drive 客户端。CLI 桥接层整体废除，obsidian_cli_bridge.py / obsidian_cli_windows.ps1 / distill_vault.py 已删除，所有笔记读写改用标准文件工具，写入后回读校验取代原 verified=true 判据，原「不得用文件系统操作冒充 vault 操作」禁令方向已完全反转。笔记路径基准是相对知识库根的裸相对路径（如 20-Knowledge/topic/note.md），禁止再加 知识库/ 前缀——根本身已经是 知识库，前缀叠加会生成嵌套目录 D:\\谷歌云盘\\知识库\\知识库\\，该错误约定在 Obsidian 时代即已存在。skill 由旧命名更名 knowledge-flow；每轮状态字段由 Obsidian:<...> 改为 知识库:<...>，四态语义保留，阻断判据改为目录不可达 / 路径不合法 / 写入后回读不一致。"
    scope: "知识库根目录、笔记路径基准、读写通道、状态字段命名与 skill 命名"
    status: "active"
    supersedes:
      - rule.legacy-windows-wsl-bridge-boundary
    evidence_ids:
      - evidence.skill.knowledge-flow
      - evidence.doc.repo-rules
    context_ids:
      - context.knowledge-flow
      - context.memory-domain
    updated_at: 2026-08-12
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
      - evidence.knowledge.skill-split-plan-20260717
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
      - evidence.knowledge.skill-split-plan-20260717
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
  - entity_id: rule.workbuddy-market-skill-absorption
    name: "WorkBuddy 官方市场 skill 吸收整理补充"
    type: "Skill 治理规则"
    aliases:
      - WorkBuddy 规则吸收
      - skill 吸收裁决
      - 需求实施 Bug 测试四域吸收
    definition: "吸收官方市场同类 skill 时以整理补充为原则，不是无限制累加或整套复制；本地规则已更完整的方向只做归纳，官方真正更优的少量动作才吸收进既有 skill 的 references/；不新建同类 skill。四域落点：需求域 100 分质量门、实施域编码前代码库探索、Bug 域修复前风险分级与确认、测试域风险分层明确结论。对应 SKILL.md 只补 references 引用，不扩触发条件。"
    scope: "WorkBuddy 官方市场同类 skill 对照、需求域、实施域、Bug 域、测试域规则吸收与整理"
    status: "active"
    evidence_ids:
      - evidence.doc.workbuddy-absorption-map
      - evidence.test.workbuddy-absorption
    context_ids:
      - context.implementation-flow
    updated_at: 2026-08-13
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
  - relation_id: rel.git-knowledge-capture-link.depends-on.knowledge-flow
    type: "depends_on"
    from: "rule.git-knowledge-capture-link"
    to: "rule.knowledge-flow-selective-default"
    evidence_ids:
      - evidence.skill.knowledge-flow
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
    note: "唯一 BLK-* 字段（含必填'用户授权操作'）、生产者边界、最终渲染 owner 和非阻断排除规则来源"
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
    note: "微业务横向隔离、业务域之间禁止直连与 CodeGraph 审查来源"
  - evidence_id: evidence.dialog.micro-business-domain-isolation
    type: "dialog"
    source: "对话确认"
    note: "当前对话冻结业务域之间禁止直接 import（无 rpc 例外）与版本目录隔离语义"
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
  - evidence_id: evidence.skill.knowledge-flow
    type: "skill"
    source: "knowledge-flow/SKILL.md"
    path: "knowledge-flow/SKILL.md"
    note: "知识库知识流选择性默认判断、CLI 检索、捕获和沉淀规则来源"
  - evidence_id: evidence.skill.git-collaboration
    type: "skill"
    source: "git-collaboration-rules/SKILL.md"
    path: "git-collaboration-rules/SKILL.md"
    note: "Git 协作与提交授权规则来源"
  - evidence_id: evidence.skill.skill-hit-check
    type: "skill"
    source: "skill-hit-check-rules/SKILL.md"
    path: "skill-hit-check-rules/SKILL.md"
    note: "首条命中检查输出 知识库判断并联动 knowledge-flow 的规则来源"
  - evidence_id: evidence.doc.repo-rules
    type: "doc"
    source: "AGENTS.md / CLAUDE.md"
    path: "AGENTS.md"
    note: "仓库级知识库选择性默认触发硬规则来源"
  - evidence_id: evidence.doc.skill-plan
    type: "doc"
    source: "编码skill.md"
    path: "编码skill.md"
    note: "主规划记忆域将 knowledge-flow 纳入正式触发链的来源"
  - evidence_id: evidence.dialog.git-knowledge-capture-link
    type: "dialog"
    source: "对话确认"
    note: "用户要求将 Git 提交流程与知识库沉淀机制联动到项目规则中"
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
  - evidence_id: evidence.knowledge.skill-split-plan-20260717
    type: "knowledge"
    source: "知识库知识流阶段收口沉淀"
    path: "20-Knowledge/codex-skills/skill-体积治理与职责拆分计划.md"
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
  - context_id: context.knowledge-flow
    type: "task-scope"
    name: "知识库知识流"
    note: "适用于历史知识依赖、知识库检索、阶段收口沉淀和最终总结捕获判断"
  - context_id: context.git-collaboration
    type: "task-scope"
    name: "Git 协作与知识沉淀"
    note: "适用于提交、推送、PR 收口和交付说明准备时的知识捕获判断"
  - context_id: context.memory-domain
    type: "repository-convention"
    name: "记忆域"
    note: "适用于近期上下文、历史回忆、知识库知识流和长期项目记忆"
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
    - "rule.micro-business-domain-isolation"
    - "rule.legacy-project-directory-adoption"
    - "rule.thread-title-process-trigger"
    - "rule.knowledge-flow-selective-default"
    - "rule.knowledge-iterative-governance"
    - "rule.git-knowledge-capture-link"
    - "rule.git-commit-domain-split"
    - "rule.git-commit-review-acceptance-evidence"
    - "rule.task-plan-rehydration"
    - "rule.session-handoff"
    - "rule.plan-mode-decision-wait-loop"
    - "rule.reasoning-summary-detail"
    - "rule.workbuddy-market-skill-absorption"
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
    同意授权:
      - "rule.task-blocker-closure"
    暂不授权:
      - "rule.task-blocker-closure"
    任务阻断授权:
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
    业务域隔离:
      - "rule.micro-business-domain-isolation"
    版本目录:
      - "rule.micro-business-domain-isolation"
    域间禁止直连:
      - "rule.micro-business-domain-isolation"
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
    knowledge-flow:
      - "rule.knowledge-flow-selective-default"
    知识库知识流:
      - "rule.knowledge-flow-selective-default"
    选择性默认触发:
      - "rule.knowledge-flow-selective-default"
    知识库检索沉淀:
      - "rule.knowledge-flow-selective-default"
    Git 协作联动知识库沉淀:
      - "rule.git-knowledge-capture-link"
    提交前知识捕获:
      - "rule.git-knowledge-capture-link"
    Git 收口沉淀:
      - "rule.git-knowledge-capture-link"
    commit 联动知识库:
      - "rule.git-knowledge-capture-link"
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
      - "rule.micro-business-domain-isolation"
    跨业务调用:
      - "rule.micro-business-domain-isolation"
    旧项目目录兼容:
      - "rule.legacy-project-directory-adoption"
    遗留源码维护:
      - "rule.legacy-project-directory-adoption"
    会话标题管理:
      - "rule.thread-title-process-trigger"
    goal 长任务:
      - "rule.thread-title-process-trigger"
    知识库记忆域:
      - "rule.knowledge-flow-selective-default"
    知识库:
      - "rule.knowledge-flow-selective-default"
    知识库检索:
      - "rule.knowledge-flow-selective-default"
    阶段收口:
      - "rule.knowledge-flow-selective-default"
    提交流程:
      - "rule.git-knowledge-capture-link"
      - "rule.git-commit-domain-split"
    交付收口:
      - "rule.git-knowledge-capture-link"
    知识库记忆沉淀:
      - "rule.git-knowledge-capture-link"
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
      - "rule.micro-business-domain-isolation"
      - "rule.legacy-project-directory-adoption"
    doc/2-需求/2026-07-28_014412_代码位置目录规则V2.md:
      - "rule.legacy-project-directory-adoption"
    micro-business-architecture-rules/SKILL.md:
      - "rule.micro-business-domain-isolation"
    编码skill.md:
      - "rule.backend-utils-common-util-placement"
    project-agents-bootstrap/SKILL.md:
      - "rule.code-generation-style-contract"
      - "rule.thread-title-process-trigger"
    thread-title-rules/SKILL.md:
      - "rule.thread-title-process-trigger"
    knowledge-flow/SKILL.md:
      - "rule.knowledge-flow-selective-default"
    skill-hit-check-rules/SKILL.md:
      - "rule.knowledge-flow-selective-default"
    AGENTS.md:
      - "rule.knowledge-flow-selective-default"
      - "rule.git-knowledge-capture-link"
    CLAUDE.md:
      - "rule.knowledge-flow-selective-default"
      - "rule.git-knowledge-capture-link"
    编码skill.md:
      - "rule.knowledge-flow-selective-default"
      - "rule.git-knowledge-capture-link"
    git-collaboration-rules/SKILL.md:
      - "rule.git-knowledge-capture-link"
      - "rule.git-commit-domain-split"
    git-collaboration-rules/scripts/pre_commit_gate.sh:
      - "rule.git-commit-domain-split"
    artifact-storage-rules/references/naming-templates.md:
    test-program-rules/SKILL.md:
    test-strategy-rules/SKILL.md:
    test-strategy-rules/references/test-asset-governance.md:
    package-structure-rules/SKILL.md:
    package-structure-rules/references/project-layout-v2.md:
    package-structure-rules/references/placement-catalog.yaml:
    package-structure-rules/scripts/placement_catalog.py:
    AGENTS.md:
    CLAUDE.md:

extensions:
  external_refs:
    - type: migration-sample
      note: "本轮仅迁移 3 条现有长期记忆作为单文件双区演练样本"
  retrieval_provider: ""
  vector_doc_id: ""
  graph_node_id: ""
```
