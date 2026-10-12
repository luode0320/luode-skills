# 来源记录

### 2026-10-12 原生步骤清单可见性首轮裁决（已撤销）

> 历史裁决：本节中“同步失败时阻断领域执行”已由下方“用户澄清：显示验收不阻断任务执行”取代，不再作为当前规则。

- 来源：内部规则缺口回补；用户确认“用户明确要求原生步骤悬浮可见”必须作为验收条件。
- 本地现状：`SKILL.md` 已要求普通执行与 Goal 调用 `update_plan`，但允许 UI 通道缺失或失败后降级继续；这无法满足用户明确要求的原生清单可见性。
- 调整：在 `SKILL.md` 增加显式可见性例外，覆盖普通执行与 Goal；通道缺失或同步失败时阻断该目标的领域执行，且只允许完成本次授权的规则修复与只读诊断。`skill-hit-check-rules` 和 `autonomous-execution-rules` 增加指向 Owner 规则的例外路由。
- 适用边界：仅限用户明确将当前会话原生步骤清单可见列为完成条件的任务；普通任务继续使用原 `UI_SYNC_BLOCKED` 降级策略。
- 宿主特例：例外: Codex Desktop + 原生步骤任务悬浮窗是该宿主专属 UI 验收目标；WorkBuddy 继续使用其既有任务列表工具，本规则不声称所有宿主均没有 UI 通道。
- 环境依赖：无新增配置或依赖；沿用既有 Codex `update_plan` 通道。本线程工具缺少该入口的证据仅作为本次验收阻断，不写作已恢复事实。
- 同域扫描：检查 `task-plan-rehydration-rules`、`skill-hit-check-rules`、`autonomous-execution-rules`、`autonomous-execution-rules/references/continuation-and-pause.md`、`context-compression-rules` 与 `agent-runtime-recovery-rules/references/platform-capability-matrix.md`。保留一般降级规则，仅在 Owner、总控与执行入口加窄例外及引用；未复制投影 schema、Goal 生命周期或宿主恢复流程。
- 验证：三个受影响 Skill 的 `quick_validate.py` 通过；当前线程的原生清单尚未显示，故用户验收未通过、目标未完成。

### 2026-10-12 用户澄清：显示验收不阻断任务执行

- 来源：用户纠正前一版规则：“显示问题不能影响任务, 不显示也可以执行任务。”
- 裁决：前一条记录中“工具缺失或同步失败时阻断领域执行”的规则已撤销。清单实际显示仍是用户指定的验收条件，但只影响 UI 验收结论，不暂停领域任务。
- 当前行为：`update_plan` 缺失或同步失败时，若投影已持久化且会话归属明确，进入 `UI_SYNC_BLOCKED`、保留投影、继续执行并在后续检查点重试；不得谎称 UI 已显示。同步更新 `agents/openai.yaml`，清除“停止领域写入”的旧提示。投影持久化失败、会话归属不明或执行状态不明仍按原安全边界处理。
- 适用范围：Codex 原生清单显示验收；不把 Markdown、文件面板或浏览器视作原生 UI 验收证据。
- 验证：规则调整后重新运行三个受影响 Skill 的 `quick_validate.py` 与定向 `git diff --check`；当前线程尚无原生清单显示证据，因此显示验收仍待完成。

### 2026-10-12 Codex `update_plan` 默认关闭根因与配置恢复

- 根因：OpenAI Codex CLI 0.152.0 发布说明明确把计划工具改为默认关闭；合并 PR #41744 记录默认值为 `false`，并明确可通过 `tools.update_plan.enabled = true` 注册该工具。
- 本机证据：用户级与当前项目级 `config.toml` 均未显式设置 `tools.update_plan.enabled`；用户级配置已追加 `[tools.update_plan]` 与 `enabled = true`，并用 TOML 解析器回读确认。用户级 `codex` 命令与桌面内置运行时为不同入口，不以全局 CLI 版本替代桌面当前工具注册证据。
- 当前验收：本轮工具清单仍未暴露 `update_plan`，当前线程原生清单仍无实际显示证据；配置成功不等于活动会话已加载或 UI 已恢复。目标保持进行中，显示未恢复期间继续领域任务。
- 官方依据：[Codex 0.152.0 发布说明](https://github.com/openai/codex/releases/tag/rust-v0.152.0) 与[启用 `update_plan` 配置的合并 PR #41744](https://github.com/openai/codex/pull/41744)。

### 2026-10-12 Desktop 重启后恢复同会话清单

- 来源：用户重启 Codex Desktop 后明确要求继续；恢复时发现 Goal 状态仍为 `blocked`，用户已明确显示故障不得暂停任务。
- 本地事实：重启后的桌面进程于 17:07 启动；本回合工具清单重新注册 `update_plan`。当前 `session_id` 的 Goal projection 校验通过，随后同会话 `update_plan` 调用成功返回。
- 新增规则：重启后继续时重新检查本回合工具注册和当前会话投影；工具可用且投影校验通过即同步。此前若只因 UI 同步失败留下 `blocked`，不把该 UI 状态当成领域任务阻断；用户明确继续后继续工作，不调用不支持的 Goal 状态恢复操作。
- 验收边界：本次核实工具重新注册和 `update_plan` 调用成功；没有直接屏幕截图，因此不把工具回执伪装成独立视觉证据。原生显示验收仍以当前线程 UI 实际显示为准。
- 环境依赖：无新增；沿用已有用户级 Codex 配置和当前会话 `update_plan` 通道。
- 同域去重：重启分支仅由本 Skill 负责；通用 UI 失败降级、投影 schema 和 Goal 生命周期沿用已有唯一权威段落，不重复定义。

### 2026-10-12 Desktop 重启后恢复同会话清单

- 来源：本次用户在重启 Codex Desktop 后要求继续；恢复过程中发现 Goal 状态仍是 `blocked`，但用户明确说明 UI 显示故障不得暂停任务。
- 本地事实：重启后的桌面进程启动时间为 17:07；本回合重新注册了 `update_plan`。当前 `session_id` 的 Goal projection 校验通过，随后对同一会话调用 `update_plan` 成功返回。
- 新增规则：重启后的继续回合重新检查运行时工具注册和当前会话投影；工具已注册且投影有效时立即同步。若先前仅因 UI 同步失败留下 `blocked` 状态，不把该 UI 状态误作领域阻断；遵循用户本轮继续意图，不调用工具不支持的 Goal 恢复状态操作。UI 通道仍不可用时保留投影并继续领域任务。
- 验收边界：本次确认了工具重新注册和 `update_plan` 调用成功；未取得当前屏幕截图，因此不把命令面板或工具返回描述为独立的屏幕视觉证据。原生显示验收仍以当前线程实际 UI 为准。
- 环境依赖：无新增；沿用当前用户级 Codex 配置和 `update_plan` 通道，当前用户级 Skill 根为仓库正式目录联接。
- 同域扫描：新增内容仅处理 Desktop 重启后的同会话恢复和 UI-only `blocked` 误判；不复制通用 UI 失败降级、投影 schema 或 Goal 生命周期规则。

### 2026-10-12 Goal、普通会话与 Plan Mode 默认细粒度步骤

- 来源：用户明确偏好任务步骤“越多越好、越细越好”，不接受仅开始/执行/完成；步骤很多时可滚动查看，并要求 Goal、正常会话及 Plan 模式都默认展示。
- 裁决：合并到本 Skill 的统一步骤展示与粒度规则。正式任务计划优先；Plan Mode 用原生计划流程展示步骤，当前工具可用时同步 `update_plan`。显示工具缺失或同步失败只影响 UI 验收，不暂停领域任务。
- 实现承接：移除 20 项数量上限，保留 51,200 UTF-8 字节 registry 总限；Goal 无正式计划可接管时以十项细化安全步骤为通用基线，已确认具体工作项时继续细化；无唯一来源时使用八项恢复清单。每步必须可执行、可核验，不为凑数量制造微步骤。
- 能力依据：[官方 Codex prompting guide](https://developers.openai.com/cookbook/examples/gpt-5/codex_prompting_guide)、[Goals in Codex](https://developers.openai.com/cookbook/examples/codex/using_goals_in_codex)、[Run long-horizon tasks with Codex](https://developers.openai.com/blog/run-long-horizon-tasks-with-codex)。官方资料说明计划/Goal 能力边界，但不承诺所有宿主及模式都显示同一悬浮 UI；需按当前会话工具和实际 UI 分别核验。
- 环境依赖：无新增；Plan 原生输出和 `update_plan` 是可选宿主通道。
- 整理：改写 Goal 固定三步、恢复三步、投影最多 20 项及 Plan Mode 不显示的冲突规则；唯一 Owner 保留 schema 与落盘安全契约，其它 Skill 只提供模式入口和引用。

### 2026-10-12 Goal 清单兼容与任务专属细化

- 来源：用户进一步明确三种模式的任务步骤“越多越好、越细越好”，长清单可滚动查看。
- 裁决：十步仅作为 Goal 无任务专属工作项时的细化基线，不是上限；按已确认工作项生成的连续 `GOAL-##` 清单可扩展。细节只写脱敏步骤，不保存 Goal 原文。
- 兼容：旧版固定三步 Goal 读取时映射至新版 `GOAL-01`、`GOAL-05`、`GOAL-09`，其余补入默认步骤；保留完成状态，阻断状态清除进行中状态。读取迁移不写盘，后续正常写入持久化新版。
- 实现落点：`scripts/task_plan_projection.py` 的 Goal 校验/迁移、`write --input` 受控投影入口、`references/task-plan-projection-contract.md`、`agents/openai.yaml` 与对应测试。
- 验证边界：需覆盖旧三步 registry 可读、超过十步 Goal 可通过、错序 ID 拒绝和正式回归脚本；仍无当前桌面 UI 截图，不声称已验证悬浮窗视觉显示。

### 2026-10-12 初始步骤投影时序与可读文案

- 来源：用户反馈任务执行较久才出现投影，并指出 `[TASK-001]` 等内部编号无法说明具体工作；要求 Goal、普通会话和 Plan Mode 都展示任务步骤，步骤应细、说明应更充分。
- 本地证据：`ensure_start_projection` 会原子写入当前会话 projection 并返回 payload；CLI 已提供 `ensure-start`，但脚本不负责调用宿主 UI。旧入口仅规定“首次领域动作前”，继续恢复流程还允许在投影前派只读子代理收集材料。
- 裁决：这是入口时序与文案契约缺口，不是 registry 脚本缺少写入能力。由 `skill-hit-check-rules` 要求在最少规则命中及必要 `PROJECT_CURRENT.md` registry 读取后、领域侦察前持久化并立即同步暂定清单；由本 Skill 定义临时 `synthesized/fallback` 与正式 L1/L2 的先后和替换规则。Plan Mode 先输出可读原生计划，不写执行期 registry。
- 文案约束：所有模式每条可见步骤都要以中文写清动作、对象和可辨认的结果/检查点；编号只作辅助索引，缩写或内部术语首次出现需有上下文。保持步骤数量不设小上限，单步与 registry 安全限制不变。
- 失败边界：原生任务 UI 缺失或同步失败时记录 UI 未同步并继续领域任务；不得声称显示已验证。投影写入失败、会话来源冲突或执行状态不明仍按现有安全规则处理。
- L1/L2 协调：暂定启动清单不是正式 L2 计划；取得项目上下文后先建立正式 L1，再写正式 L2，明确失活暂定投影。恢复时若无当前会话投影，先显示绑定当前 session 的暂定恢复清单，再派只读代理采集候选来源。
- 同会话多任务边界：只在当前回合证据能确认投影与同一已确认任务来源对象一致时复用；新任务、来源不匹配、多候选或归属不确定时，禁止沿用旧清单或覆盖其它 registry 项，改为绑定当前来源的暂定投影；脚本拒绝歧义时遵守持久化安全闸门。
- 同会话多活动计划：新任务 `ensure-start` 输入需明确当前任务 `plan_key`；只把该任务返回的 payload 同步到单一宿主清单，保留其它 registry 投影，不按时间/数组顺序选择，也不声称原生清单同时展示多个计划。
- 宿主限制：浮窗像素宽度属于桌面宿主 UI；此规则仓库只规定步骤文案，不宣称修改或控制窗口宽度。
- 环境依赖：N/A，本次不增环境变量、配置、依赖或脚本；复用 `ensure-start` 及当前宿主任务列表通道。
- 同域去重：入口先投影由 `skill-hit-check-rules` 路由，具体步骤字段、恢复和 UI 降级由本 Skill 唯一承接；不复制正式 L1 文档结构、投影 schema 或 UI 宽度实现。
- 验证：两份 Skill 的 `quick_validate.py` 已通过；规则改动后的字典刷新、同域审查与最终校验待本轮收口完成。
