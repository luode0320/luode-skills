# 命中检查清单

## 检查顺序

1. 只基于当前轮用户消息和当前运行环境匹配所有 Skill 的 `description` 与条件路由。
2. 先输出固定命中字段，再执行任何领域动作。
3. 记录 Git、并行、知识库、Skill 资产、新会话自举与失败恢复的联动摘要。
4. 将执行权交给对应 Owner Skill；本清单不复制其具体执行步骤。

## 注释场景补充

- 用户请求“补充注释”“只改注释”等表达时，至少检查 `comment-rules`（语言表达 / 位置颗粒度 / 补齐闸门三分区）、`code-change-finalization-gate-rules`。
- 函数/方法改动、补丁位点和最终核对清单仍按注释类 Owner Skill 执行，不在命中入口重复定义字段。

## 图片输入场景补充

- 消息包含图片或截图输入时，必须检查并命中 `image-redbox-focus-rules`。
- 不得跳过红框聚焦判断直接进入图片对应的主域任务。

## 项目规则/记忆聚合指令场景补充

- 用户给出“更新md / 更新项目规则md / 更新规则md / 根据 skill 更新项目 md / 补充仓库级规则”等聚合指令，或表达同步、补齐仓库级规则文件与项目 md 的意图时，必须命中 `project-rule-file-bootstrap-rules`，并按其 `rule-bootstrap`（规则文件 `AGENTS.md` / `CLAUDE.md`、`.gitattributes`、`.editorconfig`）与 `memory-bootstrap`（`PROJECT_CURRENT.md` / `PROJECT_MEMORY.md` / `PROJECT_HISTORY.md` 骨架）两个条件路由同时验收，不得只完成一组文件就收口。
- 该聚合指令下 `PROJECT_STYLE.md` 联动 `project-style-rules`、四件套事实内容联动 `project-memory-rules`；具体路由、脚本入口和逐文件结果由上述 Owner 定义，本入口只负责不漏触发和三方联动确认。

## 项目记忆/风格跨项目候选场景补充

- 本轮 `project-memory-rules`/`project-style-rules` 写入条目时标记了 `bridge_candidate: true` 或 `跨项目候选: 是` 时，收口阶段的知识库判断不得停留在 `不适用`，至少需要按 `capture-retrieve-distill.md` 走一次沉淀判断（检索去重后决定是否创建/追加）。
- 具体标准、落点和去重仍由 `knowledge-flow` 的 `references/project-memory-sync.md` 定义，本清单只负责不漏判断信号，不复制其执行细节。

## 任务投影恢复场景补充

- 新会话、上下文恢复或当前消息包含任意“继续”或恢复意图时，首条命中列表必须包含 `task-plan-rehydration-rules`，不得等领域动作开始后再补命中。至少覆盖“继续”“接着做”“接着执行”“恢复任务”“恢复执行”“按原计划继续”“继续上次任务”“往下做”“继续刚才的工作”及同义自然语言表达；不能因为消息没有出现“任务”“计划”或只含一个短词就漏触发。
- 当前回合处于 Plan Mode 时，恢复 Owner 只作为候选命中并明确退出，不读取 `PROJECT_CURRENT.md`、不调用 `update_plan`，也不创建任务悬浮窗。Plan Mode 已结束后，首条字段输出再读取并校验 `PROJECT_CURRENT.md` 的单一 v4 registry 托管区；必须按当前 `session_id` 定位唯一 projection，且有效活动 projection 必须在领域动作前真实调用 `update_plan`，并说明进行中步骤先核验中断点。
- 若 registry 缺失或当前会话无匹配 projection，则先触发只读子代理收集 `candidate_source_documents`、`completed_step_hints`、`current_step_hint` 和 `conflicts`；主代理把这些证据与 `PROJECT_CURRENT` 普通正文传给 `synthesize`，并绑定当前 `session_id`。唯一来源且存在明确步骤提示时补建 `exact` 正式列表；其余情况统一生成当前会话的固定三步 `fallback` 安全恢复列表。
- 投影失活、损坏、过期、来源不匹配、多匹配或属于其它会话时不调用 `update_plan`，但必须输出明确校验结论，不能静默略过，也不能把其它会话 projection 错投到当前任务。
- “同一任务”需要当前回合可核验的来源证据和匹配的 `session_id`；仅工作目录相同、消息只有“继续”或存在项目级活动 projection 都不足以确认归属。来源不确定时仍须命中恢复 Owner，但必须明确阻断 UI 重建，不能把其它会话的 projection 当作当前任务恢复。

## Go 测试资产场景补充

- 本轮新增或修改任意 `*_test.go`，或涉及测试程序、mock、fixture、数据构造脚本时，必须检查并命中 `test-program-rules`（含《Go 测试编译路径（强制）》），并按适用性路由到 `test-strategy-rules` 的 test-asset-governance。
- 源码目录禁放、ASCII 镜像、白盒诉求降级、生产代码测试污染判定和测试资产落点由上述专职 Owner 定义；本入口只负责自动触发和联动，不复制其目录清单、扫描命令或整改步骤。

## 代码改动收口场景补充

- 本轮发生代码新增或修改并准备收口时，按 `deferred-gate-registry.md` 与首条 `闸门预告` **逐项复核已声明 vs 已执行**：至少 `comment-rules`、`code-style-consistency-rules` 的 `6-review`、`code-change-finalization-gate-rules`，并按 `reasoning-summary-structure-rules` 输出最终总结（Plan Mode 除外）。
- 具体注释字段、审查步骤、测试证据和 PASS / FAIL 由各 Owner 定义；`闸门预告` 登记过或注册表判定当前阶段必需的 gate 未执行时，先补执行再收口。

## 代码改动中段场景补充

- 本轮首次发生代码改动时，下一条中间进度按 `deferred-gate-registry.md` 把新触发的代码域延迟 gate（注释 gate、实现自审、最终收口 gate 等）补进 `闸门预告` 并复检，不等待最终回复（`闸门预告` 是预测，此处按真实改动对账修正）。
- 长链路出现阶段切换时再次复检；中段复检与最终复检不可相互替代。

## 外部 Skill 吸收场景补充

- 用户表达"吸收/借鉴/融合/采纳 某个 skill 的精华到我们的 skill""这个 skill 能不能吸收""把 XX skill 的思路用起来""优化我们的 skill 让它更强大""把外部精华沉淀成规则"等意图时，必须命中 `skill-absorption-rules`，按"获取原文 -> 三态裁决 -> 落点简化 -> 8维评分棘轮验证 -> 登记"闭环执行。
- 提供外部 skill 的 URL / GitHub / 市场页面 / SKILL.md 原文时，先由 `skill-absorption-rules` 抓取并拆解；本入口不复制其裁决步骤。
- 与 `skill-absorption-rules`（内部 gap 演进）、`skill-audit-rules`（多 skill 职责审计）按职责边界联动；外部种子场景由 `skill-absorption-rules` 总承接。

## 判定原则

- 以触发条件为准，不以“任务简单”“已经知道怎么做”或“用户没点名”为由跳过。
- 可以多 Skill 同时命中；`skill-hit-check-rules` 是总控入口，不算业务 Owner。
- 仓库任务默认联动 `parallel-task-dispatch-rules`，由其统一判断串行、条件并行、真实启动、回收和回退；用户禁止或环境不支持时必须真实回退，不能伪报并行。
- 非 Plan Mode 的仓库实质任务按 `deferred-gate-registry.md` + 当前任务类型，在首条 `闸门预告` 字段登记本轮将适用的延迟触发 gate（`reasoning-summary-structure-rules` 恒为成员），强制项列入 `命中技能`。`闸门预告` 是预测：中段按真实改动对账修正，收口按其逐项复核声明与执行是否一致。Plan Mode 下延迟 gate 判定 `NOT_APPLICABLE`、`reasoning-summary-structure-rules` 不得命中，`闸门预告` 置 `不适用(Plan Mode)`。
- 仓库任务执行知识库选择性判断：依赖历史知识或用户长期偏好时为 `检索`，形成可复用知识时为 `沉淀`，无价值时为 `不适用`，知识库目录不存在或不可读、路径不合法、写入后回读不一致且影响动作时为 `阻断`。仅 `检索` 或 `沉淀` 联动 `knowledge-flow`。所有知识库读写必须限定在知识库根目录内操作，写入后回读校验。
- Skill 资产新增或修改时联动 `skill-execution-compliance-gate-rules`；description 或触发条件变化追加 `skill-absorption-rules`；多 Skill、职责边界或收口风险追加 `skill-audit-rules`。
- 非预期执行失败联动 `execution-failure-learning-rules`；预期负向测试、用户取消、权限阻断和业务 Bug 分别交给其专属 Owner。

## Git 短指令场景补充

- Git 意图包括显式关键词 `git/commit/push/pull/rebase/merge/cherry-pick/stash/status/diff/log`，中文动作词“提交/推送/拉取/合并/变基/暂存”，以及“提交git/帮我提交/给我推上去/看下改动/同步到远端”等语义等价表达。
- Git 意图只认当前轮；历史轮次的提交或推送要求不得继承。
- 执行 Git 协作命中 `git-collaboration-rules`；本轮不再存在独立提交级审查 Skill，提交动作仍只处理 Git 边界。
- 不得要求用户额外补“测试已完成”后才触发 Git 路由，也不得由本入口直接实施提交步骤。

## 自主执行场景补充

- 多步骤任务存在完成原始目标仍必需且可直接执行的下一步时，检查 `autonomous-execution-rules`。
- 用户明确暂停、停止或结束时，停止自动继续和扩散输出；不得把建议项升级成新目标。

## 子代理分发场景补充

- 子代理判断统一归入 `parallel-task-dispatch-rules`；本入口只报告 `并行技能` 和联动结果。
- 共享写集、统一裁决主路径或上下文重复读取成本过高时保持串行。
- 若计划并行但未真实启动，必须报告回退原因，不能把计划数当作实际启动数。

## 漏触发防护

- 不确定时可标记候选命中并继续核验，不得跳过命中检查。
- 不得把“只命中名称”当作已执行；必须完成 Owner Skill 的必要动作。
- 不得在代码已改动后直到最终回复才首次补声明注释或收口 Skill。
- 不得整轮实质任务到最终回复才首次意识到应命中任何延迟触发 gate（`reasoning-summary-structure-rules`、注释 gate、`6-review`、最终收口 gate、合规 gate 等）；非 Plan Mode 时首条命中检查即须按 `deferred-gate-registry.md` 登记 `闸门预告`，收口逐项复核声明与执行是否一致。
- 不得遗漏用户明确的停止、安全、授权、清理、回滚和输出协议。
