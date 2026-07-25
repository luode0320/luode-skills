# 任务投影持久化与重建契约

## 托管区边界

`PROJECT_CURRENT.md` 只允许一个任务投影托管区；托管区内部是 v4 registry，可保存多个会话 projection。每个 projection 必须绑定受控字段 `session_id` 和唯一 `projection_id`，不同会话写入不得互相覆盖：

````markdown
<!-- BEGIN TASK PLAN PROJECTION -->
```json
{
  "version": 4,
  "registry_schema": "task_plan_projection_registry",
  "registry_updated_at": "2026-07-25T00:00:00Z",
  "projections": [
    {
      "projection_id": "session:<session-id>:<plan-key-hash>",
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

标记必须成对、顺序正确且只出现一次。零个区块时 `write` 或 Goal 创建可在文件末尾追加；已有一个区块时只替换区块本身。缺半边、重复、嵌套或逆序标记全部拒绝。registry 内 `projections` 可为空；空 registry 只能由当前会话按契约创建或迁移。

## Schema 与兼容性

v4 registry 顶层字段必须且只能包含：

| 字段 | v1/v2/v3 读取兼容 | v4 新写入规则 |
|---|---|---|
| `version` | 接受 `1`、`2`、`3` 单 projection | 所有成功写入统一输出 `4` |
| `registry_schema` | v1-v3 无此字段 | 固定为 `task_plan_projection_registry` |
| `registry_updated_at` | v1-v3 无此字段 | 带 UTC 时区的 ISO-8601 |
| `projections` | v1-v3 顶层 projection 在读取时包装为单项数组 | 数组；每项按 `session_id + projection_id` 唯一 |

每个 v4 projection 的字段必须且只能包含：`projection_id`、`session_id`、`projection_origin`、`synthesis_mode`、`state`、`plan_key`、`source_document`、`plan_fingerprint`、`updated_at`、`steps`。`session_id` 非空且原样保存宿主会话 / 线程标识，仅允许出现在该字段；`projection_id` 非空且在 registry 内唯一，推荐使用 `session:<session-id>:<plan-key-hash>`。

旧 v1-v3 projection 读取时必须绑定当前调用提供的 `session_id` 后包装为 v4 registry；没有 `session_id` 时仅允许读取明确 `inactive` 的单 projection，活动投影必须返回归属错误，不得写入、恢复或迁移。任何成功 `write`、`deactivate`、Goal 生命周期或 `migrate` 都统一输出 v4。

每个步骤必须且只能包含 `id`、`step`、`status`。其中 `id` 非空且当前投影内唯一，`step` 非空且最多 256 个 Unicode 字符，`status` 只能为 `pending`、`in_progress` 或 `completed`。常规活动投影最多一个 `in_progress`；常规 `active` 必须有未完成步骤，`inactive` 仅允许空步骤或全部完成步骤。

`persisted` 必须保留非空 `plan_key` 和 `source_document`；`synthesized/exact` 必须使用稳定且非空的 `plan_key`（推荐 `SYNTH-EXACT/<stable-source-id>`）并保留 `source_document`；`synthesized/fallback` 必须使用 `SYNTH-FALLBACK/<UTC>` 形式的 `plan_key` 且 `source_document` 为空字符串。

读取 v1/v2/v3 不会改写文件；只有下一次成功 `write`、`deactivate`、`migrate` 或 Goal 生命周期写入才升级为 v4。v2/v3 单 projection 不允许在没有 `session_id` 时被猜测归属，避免旧投影被错误解释或覆盖其它会话。

## Goal 安全投影

活动 Goal 在没有正式实施最小任务时，使用唯一的固定安全三步：

```json
{
  "version": 4,
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
  "plan_fingerprint": "<固定三步的 SHA-256>",
  "updated_at": "2026-07-25T00:00:00Z",
  "steps": [
    {"id": "GOAL-01", "step": "[GOAL-01] 确认当前闭环", "status": "in_progress"},
    {"id": "GOAL-02", "step": "[GOAL-02] 执行并更新进度", "status": "pending"},
    {"id": "GOAL-03", "step": "[GOAL-03] 验证并完成 Goal", "status": "pending"}
  ]
  }]
}
```

Goal 投影的 ID、顺序和文案必须与上述三步完全一致，只允许状态推进：

| 场景 | 状态与模式 | 步骤与 payload |
|---|---|---|
| 创建、活动、恢复 | `active + goal_default` | 固定三步，最多一个进行中；生成 payload |
| Goal 阻断 | `blocked + goal_blocked` | 已完成步骤保留，未完成步骤均为 `pending`，不得有进行中；生成仅观察用途的 payload |
| Goal 完成 | `inactive + goal_default` | 三步全部完成；payload 为 `null` |
| Goal 创建遇到 fallback | 既有 `synthesized/fallback` | fallback 只是恢复兜底，替换为 Goal 固定安全三步 |
| 正式计划接管 | 既有 `persisted` 或 `synthesized/exact` | `create` 返回 `preserved_formal`；正式计划优先且保持独立，不写入 Goal 标识 |
| 已接管后的 Goal 生命周期 | `preserved_formal` | `restore`、`blocked`、`complete` 都返回无副作用的 `preserved_formal`；不得失活、改写或刷新真实正式计划 |

投影不得保存或由以下内容拼接步骤：Goal 原文、Goal ID、线程 ID、原始用户输入、prompt、response、业务数据或凭据。原始宿主会话 / 线程标识仅可保存在受控字段 `session_id`，不得出现在其它字段。递归拒绝的敏感字段包括 `objective`、`goal_objective`、`goal_id`、`goal_prompt`、`user_input`、`prompt`、`response`、`token`、`api_key`、`password`、`secret`、`private_key` 和 `business_data`；`thread_id` 仅作为 `session_id` 的输入语义允许，出现在其它字段时仍拒绝。未知字段同样拒绝。

## 指纹、大小与原子写入

指纹只包含步骤 ID、顺序和文案，序列化固定使用 UTF-8、`ensure_ascii=false`、键排序和紧凑分隔符，再计算 SHA-256；`state`、`status`、`updated_at`、`plan_key` 和 `source_document` 不参与指纹。

读取文件时严格按 UTF-8 解码。写入前按候选全文 UTF-8 字节数检查，恰好 51,200 字节允许，51,201 字节拒绝，禁止截断。写入必须在目标同目录创建 UTF-8 临时文件、`flush` 与 `fsync` 后使用 `os.replace` 原子替换；失败时清理临时文件且原文件字节保持不变。Windows 不支持目录 `fsync` 时只允许降级目录刷新，不得跳过文件 `fsync`。

## `update_plan` payload

活动 Goal 的 payload 使用“Goal 任务进度已恢复；进行中步骤必须先核验中断点”。阻断 Goal 的 payload 使用“Goal 当前已阻断；任务列表仅用于观察进度，不恢复执行授权”。常规 persisted/exact/fallback 投影保留各自既有说明。

脚本只生成 payload，不直接调用 UI 工具。主 Agent 固定按“成功持久化 -> 读取返回 payload -> 调用 `update_plan`”执行，且只在默认执行回合调用；Plan Mode 不读取、写入或刷新投影。Goal 投影和 UI 重建均不构成执行授权。

## `probe-timeout` 与 Goal 优先超时升级

默认执行回合允许简单任务最初没有悬浮任务列表，但未完成任务不得无限期保持无 projection。无写入资格探测入口固定为：

```text
probe-timeout --project-current PROJECT_CURRENT.md --started-at <UTC-ISO-8601> --observed-at <UTC-ISO-8601> --paused-seconds <seconds> --session-id <session-id>
```

- `started_at` 是取得执行许可后第一个真实执行动作的 UTC 时间；`observed_at` 是当前检查点 UTC 时间；`paused_seconds` 是 Plan Mode、等待用户、`blocked` 和 `manual_handoff` 的累计暂停秒数，默认为 `0`。
- 主动执行秒数固定为 `observed_at - started_at - paused_seconds`。只有严格大于 600 秒才到期；599 秒、600 秒和暂停扣减后不超过 600 秒均返回 `action: not_due`。
- `probe-timeout` 只读取并校验 UTF-8 registry，不创建锁文件、临时文件、projection 或 payload。当前会话合法 `active` 返回 `already_active`；`blocked` 返回 `blocked_goal_preserved`；当前会话只有 `inactive` 或没有 projection 且到期时返回 `goal_check_required`。其它会话状态不得影响结果。
- 非 UTC 时间、结束早于开始、负暂停、暂停大于墙钟时长、损坏 registry 或缺少 `session_id` 均返回非零，且目录和原文件没有副作用。

`goal_check_required` 后的宿主调用顺序固定为：

```text
probe-timeout -> get_goal -> 复用匹配活动 Goal 或 create_goal 一次 -> goal --event create -> update_plan
```

- 只有主 Agent 能调用 Goal 和主悬浮窗工具。匹配活动 Goal 直接复用；无活动 Goal 使用脱敏摘要创建一次；不匹配或无法确认时禁止覆盖和二次创建。
- `create_goal` 结果不明确时仅允许一次 `get_goal` 复核，不允许无变化重试创建。Goal 创建成功但投影失败时不得再创建 Goal。
- 任务摘要来源为已确认计划摘要、已确认用户目标或固定兜底文案，必须单行中文且最多 80 个 Unicode 字符。禁止密钥、token、密码、连接串、完整路径、session ID、原始 prompt、原始日志和大段输入；无法可靠脱敏时使用“完成当前已确认的长任务并完成验证收口”。摘要只传给 `create_goal`，不得持久化。
- Goal 不可用、失败、不匹配或仍不明确时，调用原 `ensure-timeout` 作为降级入口。该入口继续按 `timeout` trigger 生成并原子写入 `exact/fallback` 普通投影，再返回 `escalated` 与 payload；其输入、返回和落盘兼容语义不变。
- Goal 投影或普通投影持久化成功后才调用 `update_plan`。UI 失败保留磁盘状态且不得宣称已刷新；后续检查点只恢复 UI。
- 计时事实只属于当前执行上下文，不新增 registry 字段，也不写入投影文案。该链路没有后台唤醒能力，只能在工具返回、阶段进度和回合结束前等可执行检查点调用。

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
| `create` | 无活动正式计划时原子写入安全三步；活动正式计划不覆盖 | `created` 或 `preserved_formal` | 活动 Goal 或正式计划 payload |
| `restore` | Goal 安全投影只读；活动正式计划不改写 | `restored` 或 `preserved_formal` | 仅活动 Goal payload；正式计划为 `null` |
| `blocked` | Goal 安全投影原子写入阻断状态并清除进行中步骤；正式计划无副作用 | `blocked` 或 `preserved_formal` | 阻断 Goal 观察 payload；正式计划为 `null` |
| `complete` | Goal 安全投影原子写入全部完成、失活状态；正式计划无副作用 | `completed` 或 `preserved_formal` | `null` |

`restore` 只能恢复活动 Goal 安全投影；阻断和失活 Goal 不恢复执行。`preserved_formal` 表示由于隐私边界没有 Goal 与正式计划的可持久化关联，Goal 生命周期不得替代正式计划自身的状态迁移。非法事件、错误状态迁移、损坏标记或 UTF-8 错误必须返回非零，并保持原文件不变。

## synthesize 输入输出

无投影补建仍使用（必须绑定当前会话）：

```text
synthesize --project-current PROJECT_CURRENT.md --input synthesis_context.json --session-id <session-id>
```

`synthesize` 处理 `continue` 和 `timeout` 两种触发下的正式计划 exact/fallback 补建；它不从 Goal 原文生成任务。输出仍包含 `mode`、绑定当前 `session_id` 的合法 projection、活动时的 `payload` 与最小证据。`exact` 仅在唯一来源文档、普通当前状态可指向唯一任务、存在明确步骤提示且无冲突时成立；其他情况统一生成当前会话的固定三步 `fallback` 安全恢复列表。其它会话 projection 不得被读取、覆盖或作为恢复候选。
