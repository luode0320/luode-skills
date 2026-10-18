# 任务投影持久化与重建契约

## 托管区边界

`PROJECT_CURRENT.md` 只允许一个任务投影托管区；托管区内部是 v5 registry，可保存多个会话 projection 与可追溯隔离记录。同一会话也可并存多个独立计划；每项必须绑定受控字段 `session_id` 和唯一 `projection_id`，按计划身份更新，不同计划和会话写入不得互相覆盖：

````markdown
<!-- BEGIN TASK PLAN PROJECTION -->
```json
{
  "version": 5,
  "registry_schema": "task_plan_projection_registry",
  "registry_updated_at": "2026-07-25T00:00:00Z",
  "projections": [
    {
      "projection_id": "SESSION/<64 位 SHA-256>",
      "session_id": "<原始会话ID>",
      "projection_origin": "persisted",
      "synthesis_mode": "none",
      "state": "active",
      "plan_key": "REQ-RTP-001/CYCLE-RTP-01",
      "source_document": "doc/3-实施/example.md",
      "plan_fingerprint": "<64 位 SHA-256>",
      "updated_at": "2026-07-25T00:00:00Z",
      "steps": [
        {
          "id": "TASK-RTP-01",
          "step": "[TASK-RTP-01] 冻结恢复契约",
          "status": "in_progress"
        }
      ]
    }
  ]
}
```
<!-- END TASK PLAN PROJECTION -->
````

标记必须成对、顺序正确且只出现一次。零个区块时 `write`、`ensure-start` 或 Goal 创建可在文件末尾追加；已有一个区块时只替换区块本身。缺半边、重复、嵌套或逆序标记全部拒绝。registry 内 `projections` 可为空；空 registry 只能由当前会话按契约创建或迁移。

默认执行模式取得 `confirmed` 后，首次领域动作前必须先以 `ensure-start`（或正式投影等价的 `write`）持久化当前会话的活动投影；新任务应直接传入调用方按当前用户请求构造的任务专属投影，不能经过会退化为通用恢复清单的上下文合成路径。持久化成功结果必须直接包含同一会话的 `update_plan` payload，主 Agent 的下一动作固定为调用该工具。持久化与 UI 调用之间不得发生其它领域写操作。

## Schema 与兼容性

v5 registry 顶层字段必须且只能包含：

| 字段 | v1/v2/v3/v4 读取兼容 | v5 新写入规则 |
|---|---|---|
| `version` | 接受 `1`、`2`、`3` 单 projection 与 `4` registry | 所有成功写入统一输出 `5` |
| `registry_schema` | v1-v3 无此字段；v4 已有 | 固定为 `task_plan_projection_registry` |
| `registry_updated_at` | v1-v3 无此字段；v4 已有 | 带 UTC 时区的 ISO-8601 |
| `projections` | v1-v3 顶层 projection 在读取时包装为单项数组；v4 按兼容规则读取 | 数组；projection ID 与计划身份唯一，同一会话允许多个不同计划，不同会话可使用相同 `plan_key` |
| `quarantined_projections` | v1-v4 无此字段 | 最多 512 项，保留坏项的原始 JSON 与有限诊断字段，仍受全文字节上限约束 |

每个 v5 projection 的字段必须且只能包含：`projection_id`、`session_id`、`projection_origin`、`synthesis_mode`、`state`、`plan_key`、`source_document`、`plan_fingerprint`、`updated_at`、`steps`。`session_id` 非空且原样保存宿主会话 / 线程标识，仅允许出现在该字段。新写入的 canonical `projection_id` 固定为 `SESSION/<sha256>`：将下列对象按 UTF-8、`ensure_ascii=false`、键排序、紧凑分隔符序列化后计算 SHA-256，并加 `SESSION/` 前缀：

```json
{"session_id":"<session_id>","plan_key":"<plan_key>","source_document":"<source_document>","projection_origin":"<projection_origin>"}
```

`synthesis_mode` 不属于 canonical 身份字段。为读取历史 v4 registry，校验器还接受仅当把同一对象增加 `synthesis_mode` 后计算出的 legacy `SESSION/<sha256>` 与记录完全相等时的旧 ID。canonical 或 legacy 两种算法之一精确匹配即为有效；只与 canonical 结果不同、但与 legacy 结果相等，不是身份损坏。`validate` 和恢复操作不得自动改写 legacy ID；新条目使用 canonical ID，已存在 legacy 条目的常规状态更新可保留其 ID。两种算法都不匹配时，将该条目视为身份损坏：原文件字节保持不变，拒绝针对它的 payload/UI 恢复，不猜测或修复身份。

`plan_fingerprint` 仅校验步骤 ID、顺序和文案，不证明会话或来源文档归属。所有恢复和写入必须同时校验该条的 `session_id`、`projection_id` 与 `plan_key`、`source_document`、`projection_origin` 身份。相同 `plan_key` 可以出现在不同 `session_id` 下；同一会话出现多条候选时，`validate`、`payload`、`deactivate` 等单投影读取或迁移必须显式提供 `--plan-key` 或 `--projection-id`，且选择结果唯一；如 `plan_key` 在同会话内有歧义，必须改用 `--projection-id`。选择器缺失或不唯一时失败关闭，不得按更新时间、数组顺序或活动状态猜测。

v5 活动 `projections[]` 中单条无效时，读取器按条目容错：把所有损坏或身份重复候选放入 `quarantined_projections`，保留原始 JSON、来源版本、原数组索引、原因码和可验证的 `affected_session_id`，其余身份明确的计划继续可读可写；已有隔离记录校验后原样保留。`validate_registry` 作为写入前的最终闸门仍保持严格，候选 registry 任一条目无效时拒绝落盘，原文件字节不变。读取 v4 registry 时，顶层字段、标记、JSON、版本和数组上限仍严格校验；同一会话允许多个不同计划，不能仅按 `session_id` 去重。待隔离原文包含凭据、prompt、token 等敏感字段时，拒绝转换并保持原文件字节不变。读取只在内存转换、不改文件；显式 `migrate` 或后续成功写入才持久化 v5。隔离项与目标会话及所选计划身份可能冲突，或证据不足以排除冲突时，仅阻止该目标计划恢复 / 改写；其它会话和身份明确无关的计划可继续。若隔离记录无法验证所属会话，则证据不足以证明它与任何会话无关，所有会话的恢复 / 改写均失败关闭。托管标记、registry JSON 解析、顶层字段 / schema / 版本 / 数组上限损坏或隔离记录本身无效时整体失败关闭，保持原文件字节不变；整体失败关闭只退出悬浮任务列表重建与投影改写，不取消领域工作自身的执行授权。

旧 v1-v3 projection 读取时必须绑定当前调用解析出的 `session_id` 后包装为 v5 registry；解析优先级固定为显式 `--session-id` > `CODEX_THREAD_ID` > WorkBuddy 宿主元数据（`CODEBUDDY_MCP_CONFIG` 的 `mcpServers.*.headers["X-WorkBuddy-Session-Id"]` 唯一值，或 `WORKBUDDY_SESSION_ID` 环境变量），多来源不一致、均缺失或非法时失败关闭，不得写入、恢复或迁移。任何成功 `write`、`ensure-start`、`deactivate`、Goal 生命周期或 `migrate` 都统一输出 v5。

每个步骤必须且只能包含 `id`、`step`、`status`。其中 `id` 非空且当前投影内唯一，`step` 非空且最多 256 个 Unicode 字符，`status` 只能为 `pending`、`in_progress` 或 `completed`。常规活动投影最多一个 `in_progress`；常规 `active` 必须有未完成步骤，`inactive` 仅允许空步骤或全部完成步骤。

`persisted` 必须保留非空 `plan_key` 和 `source_document`；`synthesized/exact` 必须使用稳定且非空的 `plan_key`（推荐 `SYNTH-EXACT/<stable-source-id>`）并保留 `source_document`；`synthesized/fallback` 必须使用 `SYNTH-FALLBACK/<UTC>` 形式的 `plan_key` 且 `source_document` 为空字符串。

读取 v1-v4 不会改写文件；只有显式 `migrate` 或下一次成功 `write`、`ensure-start`、`deactivate`、Goal 生命周期写入才持久化为 v5。v2/v3 单 projection 不允许在没有可解析 `session_id` 时被猜测归属，避免旧投影被错误解释或覆盖其它会话。

## Goal 安全投影

活动 Goal 在没有正式实施计划可接管时，默认使用至少十项的细化安全清单；存在已确认的任务工作项时，应按任务内容继续拆细，允许超过默认十项。步骤覆盖适用的目标与验收标准、范围约束、上下文核查、工作项拆分、分项执行、验证、风险检查、进度证据和收口；只保存脱敏后的步骤标题，不写入 Goal 原文。所有模式均不设步骤数量小上限，仍受单步最多 256 个 Unicode 字符和托管区总大小 51,200 UTF-8 字节约束。

```json
{
  "version": 5,
  "registry_schema": "task_plan_projection_registry",
  "registry_updated_at": "2026-07-25T00:00:00Z",
  "projections": [{
  "projection_id": "session:<session-id>:GOAL-ACTIVE",
  "session_id": "<原始会话ID>",
  "projection_origin": "goal",
  "synthesis_mode": "goal_default",
  "state": "active",
  "plan_key": "GOAL/ACTIVE",
  "source_document": "",
  "plan_fingerprint": "<按有序步骤 ID 和文案计算的 SHA-256>",
  "updated_at": "2026-07-25T00:00:00Z",
  "steps": [
    {"id": "GOAL-01", "step": "[GOAL-01] 梳理已确认目标与完成标准", "status": "in_progress"},
    {"id": "GOAL-02", "step": "[GOAL-02] 确认范围、约束和明确不做事项", "status": "pending"},
    {"id": "GOAL-03", "step": "[GOAL-03] 检查现有上下文、文件和事实来源", "status": "pending"},
    {"id": "GOAL-04", "step": "[GOAL-04] 拆出具体工作项并确认依赖顺序", "status": "pending"},
    {"id": "GOAL-05", "step": "[GOAL-05] 执行当前最小可验证工作项", "status": "pending"},
    {"id": "GOAL-06", "step": "[GOAL-06] 对照完成标准验证本阶段结果", "status": "pending"},
    {"id": "GOAL-07", "step": "[GOAL-07] 检查边界、异常和回归风险", "status": "pending"},
    {"id": "GOAL-08", "step": "[GOAL-08] 更新细化步骤状态和完成证据", "status": "pending"},
    {"id": "GOAL-09", "step": "[GOAL-09] 完成剩余必要工作并复核验收项", "status": "pending"},
    {"id": "GOAL-10", "step": "[GOAL-10] 清理临时产物并完成最终收口", "status": "pending"}
  ]
  }]
}
```

新建 Goal 在没有可用任务专属工作项时，使用上述十步作为细化基线；有任务专属拆分时允许追加步骤。步骤 ID 必须从 `GOAL-01` 起连续编号，顺序与文案前缀 `[GOAL-##]` 必须对应，状态规则如下：

| 场景 | 状态与模式 | 步骤与 payload |
|---|---|---|
| 创建、活动、恢复 | `active + goal_default` | 至少十步的细化默认清单或经过脱敏的任务专属细化清单，最多一个进行中；生成 payload |
| Goal 阻断 | `blocked + goal_blocked` | 已完成步骤保留，未完成步骤均为 `pending`，不得有进行中；生成仅观察用途的 payload |
| Goal 完成 | `inactive + goal_default` | 十步全部完成；返回一次性完成收口 payload，失活后不得再次生成活动 payload |
| Goal 创建遇到 fallback | 既有 `synthesized/fallback` | fallback 只是恢复兜底，替换为 Goal 细化默认清单 |
| 正式计划接管 | 既有 `persisted` 或 `synthesized/exact` | `create` 返回 `preserved_formal`；正式计划优先且保持独立，不写入 Goal 标识；若同一会话存在多条活动正式计划，返回空 projection/payload，不按数组顺序选择 |
| 已接管后的 Goal 生命周期 | `preserved_formal` | `restore`、`blocked`、`complete` 都返回无副作用的 `preserved_formal`；不得失活、改写或刷新真实正式计划 |

读取旧版固定三步 Goal 时，将旧 `GOAL-01` 映射到新 `GOAL-01`，旧 `GOAL-02` 映射到新 `GOAL-05`，旧 `GOAL-03` 映射到新 `GOAL-09`，保留可迁移状态并为其它步骤补 `pending`；旧投影若已失活则新版全部置为 `completed`，阻断状态不得残留 `in_progress`。该转换只在内存读取中发生，后续成功写入时统一持久化新版清单。

投影不得保存或由以下内容拼接步骤：Goal 原文、Goal ID、线程 ID、原始用户输入、prompt、response、业务数据或凭据。原始宿主会话 / 线程标识仅可保存在受控字段 `session_id`，不得出现在其它字段。递归拒绝的敏感字段包括 `objective`、`goal_objective`、`goal_id`、`goal_prompt`、`user_input`、`prompt`、`response`、`token`、`api_key`、`password`、`secret`、`private_key` 和 `business_data`；`thread_id` 仅作为 `session_id` 的输入语义允许，出现在其它字段时仍拒绝。未知字段同样拒绝。列表按内容需要逐步展开，不设任意小数量上限；每项文案仍不得超过 256 字符，整个 `PROJECT_CURRENT.md` 候选全文不得超过 51,200 UTF-8 字节，禁止截断或压成少量通用步骤。若投影写入只因全文超限被拒绝，必须转交 `project-memory-rules` 压缩普通历史正文并重新读取/校验后重试；容量问题不暂停领域任务，完整压缩协议见该 Skill 的 `PROJECT_CURRENT 超限压缩`。

## 指纹、大小与原子写入

`PROJECT_CURRENT.md` 是多个会话共享的单一文件。投影更新、最近会话快照更新及普通当前状态更新必须共用锁文件 `.PROJECT_CURRENT.md.lock`；锁路径基于目标文件所在目录和文件名，不得另造每个 Skill 私有的锁名。写入者须先获取锁，再读取最新全文和 registry，只修改本 Skill 拥有的正文区段或精确选中的投影条目，校验其余区段与投影未被覆盖后才写回。锁获取失败、锁内重读失败或源身份不符时必须保持原字节不变。`fsync` 与 `os.replace` 仅保证完整原子替换，不可替代锁内读改写协议；两个会话并发更新时，每个调用须串行重读最新 registry 并合并自己拥有的单条记录。

指纹只包含步骤 ID、顺序和文案，序列化固定使用 UTF-8、`ensure_ascii=false`、键排序和紧凑分隔符，再计算 SHA-256；`state`、`status`、`updated_at`、`plan_key` 和 `source_document` 不参与指纹。

读取文件时严格按 UTF-8 解码。写入前按候选全文 UTF-8 字节数检查，恰好 51,200 字节允许，51,201 字节拒绝，禁止截断。投影脚本本身只拒绝超限候选并保持原文件不变；由主 Agent 按 `project-memory-rules` 压缩普通历史正文，再重新读取最新文件并重试一次；并发写入再次造成超限时允许再执行一轮压缩/重试。两轮后仍无安全空间则不写入该 projection，但领域任务继续。写入必须在目标同目录创建 UTF-8 临时文件、`flush` 与 `fsync` 后使用 `os.replace` 原子替换；失败时清理临时文件且原文件字节保持不变。Windows 不支持目录 `fsync` 时只允许降级目录刷新，不得跳过文件 `fsync`。

## `update_plan` payload

活动 Goal 的 payload 使用“Goal 任务进度已恢复；进行中步骤必须先核验中断点”。阻断 Goal 的 payload 使用“Goal 当前已阻断；任务列表仅用于观察进度，不恢复执行授权”。常规 persisted/exact/fallback 投影保留各自既有说明。

脚本只生成 payload，不直接调用 UI 工具。主 Agent 固定按“成功持久化 -> 读取返回 payload -> 下一动作同步 UI”执行；两者之间禁止代码、文档、测试、委派等领域写操作。分级处理：会话归属冲突或不确定（多来源不一致、无匹配投影）、执行状态不明（进行中步骤无法核验）、UTF-8/registry 结构损坏及非容量类原子写失败按各自安全规则处理，禁止错投或重放未知写操作。若投影写入仅因全文超过 51,200 字节被拒绝，先调用 `project-memory-rules` 压缩普通历史正文并按容量契约重试；最多两轮后仍超限则保持原文件不变、投影不落盘但继续领域任务。UI 同步通道不可用（`update_plan` 缺失或调用失败）时也降级继续；只有磁盘投影已成功且会话归属明确时才可说已持久化，只有真实 `update_plan` 成功时才可说 UI 已同步。Plan Mode 不读写执行期 registry；默认通过原生计划流程展示细化步骤，若 `update_plan` 在当前会话可用可同步显示，UI 不可用不暂停计划形成。Goal 投影和 UI 重建均不构成执行授权。

## 首次持久化与会话解析

默认执行模式取得 `confirmed` 后，任何任务首次领域动作前都必须为当前会话持久化活动 projection；`active` 和 `blocked` projection 都必须有悬浮任务列表，`inactive` 不创建。入口固定为：

```text
ensure-start --project-current PROJECT_CURRENT.md --input projection_or_synthesis_context.json [--session-id <session-id>]
```

会话解析优先级固定为显式 `--session-id` > 宿主环境 `CODEX_THREAD_ID` > WorkBuddy 宿主元数据（`CODEBUDDY_MCP_CONFIG` 的 `mcpServers.*.headers["X-WorkBuddy-Session-Id"]` 唯一值，或 `WORKBUDDY_SESSION_ID` 环境变量）。多来源同时存在但不一致、任一值非法、或全部缺失时失败关闭且不得写文件；解析时禁止打印 `CODEBUDDY_MCP_CONFIG` 全文或其中的 token。成功结果必须同时返回绑定当前 session 的 projection 和可直接传给 UI 通道的 payload；正式 `write` 也必须返回同样的 payload。

## `probe-timeout` 与 Goal 优先超时升级

正常任务不得因“简单”而跳过首次投影；十分钟只作未显示步骤的异常补救闸门。已真实执行且主动时间严格超过 600 秒、当前会话尚未确认原生步骤清单同步成功时（没有活动 projection，或已有 projection 但 UI 同步失败/用户明确反馈未显示），才允许使用无写入资格探测入口：

```text
probe-timeout --project-current PROJECT_CURRENT.md --started-at <UTC-ISO-8601> --observed-at <UTC-ISO-8601> --paused-seconds <seconds> --session-id <session-id>
```

- `started_at` 是取得执行许可后第一个真实执行动作的 UTC 时间；`observed_at` 是当前检查点 UTC 时间；`paused_seconds` 是 Plan Mode、等待用户、`blocked` 和 `manual_handoff` 的累计暂停秒数，默认为 `0`。
- 主动执行秒数固定为 `observed_at - started_at - paused_seconds`。只有严格大于 600 秒才到期；599 秒、600 秒和暂停扣减后不超过 600 秒均返回 `action: not_due`。
- `probe-timeout` 只读取并校验 UTF-8 registry，不创建锁文件、临时文件、projection 或 payload。当前会话合法 `active` 返回 `already_active`；`blocked` 返回 `blocked_goal_preserved`；当前会话只有 `inactive` 或没有 projection 且到期时返回 `goal_check_required`。其它会话状态不得影响结果。`already_active` 仅代表磁盘状态，不代表 UI 显示成功；若 UI 未确认同步，恰有一条活动 projection 时调用 `ensure-timeout` 读取其现有 payload 后立即重试 `update_plan`，不创建 Goal、不替换投影。若当前会话有多条活动 projection，仅当正式计划或本回合首次同步返回值已明确证明目标身份时，使用只读 `payload --project-current PROJECT_CURRENT.md --session-id <session-id> --plan-key <plan-key>`（或 `--projection-id <projection-id>`）读取该条；身份不明或选择不唯一时禁止猜测、禁止刷新错误任务，继续领域任务并如实说明 UI 尚未同步。
- 非 UTC 时间、结束早于开始、负暂停、暂停大于墙钟时长、损坏 registry 或缺少 `session_id` 均返回非零，且目录和原文件没有副作用。

`goal_check_required` 后的宿主调用顺序固定为：

```text
probe-timeout -> get_goal -> 复用匹配活动 Goal 或 create_goal 一次 -> goal --event create -> update_plan
```

- 只有主 Agent 能调用 Goal 和主悬浮窗工具。匹配活动 Goal 直接复用；无活动 Goal 使用脱敏摘要创建一次；不匹配或无法确认时禁止覆盖和二次创建。
- `create_goal` 结果不明确时仅允许一次 `get_goal` 复核，不允许无变化重试创建。Goal 创建成功但投影失败时不得再创建 Goal。
- 任务摘要来源为已确认计划摘要、已确认用户目标或固定兜底文案，必须单行中文且最多 80 个 Unicode 字符。禁止密钥、token、密码、连接串、完整路径、session ID、原始 prompt、原始日志和大段输入；无法可靠脱敏时使用“完成当前已确认的长任务并完成验证收口”。摘要只传给 `create_goal`，不得持久化。
- Goal 不可用、失败、不匹配或仍不明确时，调用原 `ensure-timeout` 作为降级入口。该入口继续按 `timeout` trigger 生成并原子写入 `exact/fallback` 普通投影，再返回 `escalated` 与 payload；其输入、返回和落盘兼容语义不变。
- Goal 投影或普通投影持久化成功后才同步 UI。仅 UI 同步通道不可用时降级继续：保留磁盘投影、继续领域执行、后续检查点只恢复 UI；不得宣称已刷新或伪造同步成功。
- 计时事实只属于当前执行上下文，不新增 registry 字段，也不写入投影文案。该链路没有后台唤醒能力；长工具调用返回后的第一个可执行检查点必须立即处理已超过 600 秒且未确认显示的清单，不得再等下一阶段或回合结束。

## Goal CLI 生命周期

```text
goal --project-current PROJECT_CURRENT.md --event create --session-id <session-id>
goal --project-current PROJECT_CURRENT.md --event restore --session-id <session-id>
goal --project-current PROJECT_CURRENT.md --event blocked --session-id <session-id>
goal --project-current PROJECT_CURRENT.md --event complete --session-id <session-id>
```

所有成功结果均为 `{ "ok", "action", "projection", "payload" }`：

| 事件 | 磁盘行为 | action | payload |
|---|---|---|---|
| `create` | 无活动正式计划时原子写入细化安全清单；活动正式计划不覆盖 | `created` 或 `preserved_formal` | 活动 Goal；唯一正式计划可返回 projection/payload，多条正式计划时 projection/payload 为 `null` |
| `restore` | Goal 安全投影只读；活动正式计划不改写 | `restored` 或 `preserved_formal` | 仅活动 Goal payload；正式计划为 `null` |
| `blocked` | Goal 安全投影原子写入阻断状态并清除进行中步骤；正式计划无副作用 | `blocked` 或 `preserved_formal` | 阻断 Goal 观察 payload；正式计划为 `null` |
| `complete` | Goal 安全投影先生成一次性完成收口 payload，再原子写入全部完成、失活状态；正式计划无副作用 | `completed` 或 `preserved_formal` | 完成收口 payload 或 `preserved_formal` 的 `null` |

`restore` 只能恢复活动 Goal 安全投影；阻断和失活 Goal 不恢复执行。`preserved_formal` 表示由于隐私边界没有 Goal 与正式计划的可持久化关联，Goal 生命周期不得替代正式计划自身的状态迁移。非法事件、错误状态迁移、损坏标记或 UTF-8 错误必须返回非零，并保持原文件不变。

## synthesize 输入输出

无投影补建仍使用（必须绑定当前会话）：

```text
synthesize --project-current PROJECT_CURRENT.md --input synthesis_context.json --session-id <session-id>
```

`synthesize` 处理 `start`、`continue` 和 `timeout` 三种触发下的正式计划 exact/fallback 补建；它不从 Goal 原文生成任务。上下文在 1–96 字符范围内提供脱敏 `task_summary`；只要能从当前请求、已确认项目目标或来源文档识别任务，就必须提供，不能因字段可选而漏传。摘要不得包含原始 prompt、Goal 原文、凭据或业务数据。输出仍包含 `mode`、绑定当前 `session_id` 的合法 projection、活动时的 `payload` 与最小证据。`exact` 仅在唯一来源文档、普通当前状态可指向唯一任务、存在明确步骤提示且无冲突时成立；其他情况生成 `fallback`：若有 `task_summary`，每条恢复步骤都必须带有该任务摘要；若没有可信来源可以安全识别任务，首步必须明确说明具体任务尚未识别，清单只用于核验会话目标和来源。新任务启动不走该通用恢复 fallback；应使用 `ensure-start` 直接接收的任务专属投影。其它会话 projection 不得被读取、覆盖或作为恢复候选。
