# 命中检查清单

## 检查顺序

1. 只基于当前轮用户消息和当前运行环境匹配所有 Skill 的 `description` 与条件路由。
2. 先输出固定命中字段，再执行任何领域动作。
3. 记录 Git、并行、Obsidian、Skill 资产、新会话自举与失败恢复的联动摘要。
4. 将执行权交给对应 Owner Skill；本清单不复制其具体执行步骤。

## 注释场景补充

- 用户请求“补充注释”“只改注释”等表达时，至少检查 `comment-placement-granularity-rules`、`comment-completion-gate-rules`、`chinese-comment-rules`、`code-change-finalization-gate-rules`。
- 函数/方法改动、补丁位点和最终核对清单仍按注释类 Owner Skill 执行，不在命中入口重复定义字段。

## 图片输入场景补充

- 消息包含图片或截图输入时，必须检查并命中 `image-redbox-focus-rules`。
- 不得跳过红框聚焦判断直接进入图片对应的主域任务。

## 任务投影恢复场景补充

- 新会话、上下文恢复或当前消息包含任意“继续”或恢复意图时，首条命中列表必须包含 `task-plan-rehydration-rules`，不得等领域动作开始后再补命中。至少覆盖“继续”“接着做”“接着执行”“恢复任务”“恢复执行”“按原计划继续”“继续上次任务”“往下做”“继续刚才的工作”及同义自然语言表达；不能因为消息没有出现“任务”“计划”或只含一个短词就漏触发。
- 当前回合处于 Plan Mode 时，恢复 Owner 只作为候选命中并明确退出，不读取 `PROJECT_CURRENT.md`、不调用 `update_plan`，也不创建任务悬浮窗。Plan Mode 已结束后，首条字段输出再读取并校验 `PROJECT_CURRENT.md` 的唯一任务投影托管区；有效活动投影必须在领域动作前真实调用 `update_plan`，并说明进行中步骤先核验中断点。
- 投影失活、损坏、过期、来源不匹配或属于其它任务时不调用 `update_plan`，但必须输出明确校验结论，不能静默略过，也不能把项目级活动投影错误投到无关任务。
- “同一任务”需要当前回合可核验的来源证据；仅工作目录相同、消息只有“继续”或存在项目级活动投影都不足以确认归属。来源不确定时仍须命中恢复 Owner，但必须明确阻断 UI 重建，不能把其它会话的投影当作当前任务恢复。

## Go 测试资产场景补充

- 本轮新增或修改任意 `*_test.go`，或涉及测试程序、mock、fixture、数据构造脚本时，必须检查并命中 `test-program-rules`（含《Go 测试编译路径（强制）》），并按适用性路由到 `test-strategy-rules` 的 test-asset-governance。
- 源码目录禁放、ASCII 镜像、白盒 seam 和测试资产落点由上述专职 Owner 定义；本入口只负责自动触发和联动，不复制其目录清单、扫描命令或整改步骤。

## 代码改动收口场景补充

- 本轮发生代码新增或修改并准备收口时，检查 `comment-placement-granularity-rules`、`comment-completion-gate-rules`、`implementation-review-rules`、`code-change-finalization-gate-rules`。
- 具体注释字段、审查步骤、测试证据和 PASS / FAIL 由各 Owner 定义；缺少任一必需 Owner 时先补执行再收口。

## 代码改动中段场景补充

- 本轮首次发生代码改动时，下一条中间进度复检注释与代码收口 Skill，不等待最终回复。
- 长链路出现阶段切换时再次复检；中段复检与最终复检不可相互替代。

## 判定原则

- 以触发条件为准，不以“任务简单”“已经知道怎么做”或“用户没点名”为由跳过。
- 可以多 Skill 同时命中；`skill-hit-check-rules` 是总控入口，不算业务 Owner。
- 仓库任务默认联动 `parallel-task-dispatch-rules`，由其统一判断串行、条件并行、真实启动、回收和回退；用户禁止或环境不支持时必须真实回退，不能伪报并行。
- 仓库任务执行 Obsidian 选择性判断：依赖历史知识或用户长期偏好时为 `检索`，形成可复用知识时为 `沉淀`，无价值时为 `不适用`，CLI 或 vault 不可用且影响动作时为 `阻断`。仅 `检索` 或 `沉淀` 联动 `obsidian-knowledge-flow`。
- Skill 资产新增或修改时联动 `skill-execution-compliance-gate-rules`；description 或触发条件变化追加 `skill-evolution-rules`；多 Skill、职责边界或收口风险追加 `skill-audit-rules`。
- 非预期执行失败联动 `execution-failure-learning-rules`；预期负向测试、用户取消、权限阻断和业务 Bug 分别交给其专属 Owner。

## Git 短指令场景补充

- Git 意图包括显式关键词 `git/commit/push/pull/rebase/merge/cherry-pick/stash/status/diff/log`，中文动作词“提交/推送/拉取/合并/变基/暂存”，以及“提交git/帮我提交/给我推上去/看下改动/同步到远端”等语义等价表达。
- Git 意图只认当前轮；历史轮次的提交或推送要求不得继承。
- 执行 Git 协作命中 `git-collaboration-rules`；提交级审查请求命中 `code-review-automation-rules`，二者不得混淆。
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
- 不得遗漏用户明确的停止、安全、授权、清理、回滚和输出协议。
