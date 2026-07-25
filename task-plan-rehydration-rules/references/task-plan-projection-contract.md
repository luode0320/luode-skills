# 任务投影持久化与重建契约

## 托管区边界

`PROJECT_CURRENT.md` 最多存在一个任务投影托管区：

````markdown
<!-- BEGIN TASK PLAN PROJECTION -->
```json
{
  "version": 3,
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
```
<!-- END TASK PLAN PROJECTION -->
````

标记必须成对、顺序正确且只出现一次。零个区块时 `write` 或 Goal 创建可在文件末尾追加；已有一个区块时只替换区块本身。缺半边、重复、嵌套或逆序标记全部拒绝。

## Schema 与兼容性

顶层字段必须且只能包含：

| 字段 | v1/v2 读取兼容 | v3 新写入规则 |
|---|---|---|
| `version` | 接受 `1`、`2` | 所有成功写入统一输出 `3` |
| `projection_origin` | v1 隐式为 `persisted`；v2 为 `persisted` 或 `synthesized` | 额外允许 `goal` |
| `synthesis_mode` | v1 隐式为 `none`；v2 为 `none`、`exact` 或 `fallback` | 额外允许 `goal_default`、`goal_blocked` |
| `state` | `active` 或 `inactive` | 额外允许 `blocked`，但仅限 Goal 投影 |
| `plan_key` | 活动投影非空；空失活槽位允许空字符串 | Goal 固定为 `GOAL/ACTIVE` |
| `source_document` | persisted/exact 活动投影非空；fallback 为空 | Goal 固定为空字符串 |
| `plan_fingerprint` | 非空步骤必须为步骤 ID、顺序和文案的 64 位小写 SHA-256 | 规则不变 |
| `updated_at` | 带 UTC 时区的 ISO-8601 | 规则不变 |
| `steps` | 数组，最多 20 项 | Goal 固定安全三步 |

每个步骤必须且只能包含 `id`、`step`、`status`。其中 `id` 非空且当前投影内唯一，`step` 非空且最多 256 个 Unicode 字符，`status` 只能为 `pending`、`in_progress` 或 `completed`。常规活动投影最多一个 `in_progress`；常规 `active` 必须有未完成步骤，`inactive` 仅允许空步骤或全部完成步骤。

`persisted` 必须保留非空 `plan_key` 和 `source_document`；`synthesized/exact` 必须使用稳定且非空的 `plan_key`（推荐 `SYNTH-EXACT/<stable-source-id>`）并保留 `source_document`；`synthesized/fallback` 必须使用 `SYNTH-FALLBACK/<UTC>` 形式的 `plan_key` 且 `source_document` 为空字符串。

读取 v1/v2 不会改写文件；只有下一次成功 `write`、`deactivate` 或 Goal 生命周期写入才升级为 v3。v2 不允许 `goal`、`goal_default`、`goal_blocked` 或 `blocked`，避免旧投影被错误解释。

## Goal 安全投影

活动 Goal 在没有正式实施最小任务时，使用唯一的固定安全三步：

```json
{
  "version": 3,
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

投影不得保存或由以下内容拼接步骤：Goal 原文、Goal ID、线程 ID、原始用户输入、prompt、response、业务数据或凭据。递归拒绝的敏感字段包括 `objective`、`goal_objective`、`goal_id`、`goal_prompt`、`thread_id`、`user_input`、`prompt`、`response`、`token`、`api_key`、`password`、`secret`、`private_key` 和 `business_data`。未知字段同样拒绝。

## 指纹、大小与原子写入

指纹只包含步骤 ID、顺序和文案，序列化固定使用 UTF-8、`ensure_ascii=false`、键排序和紧凑分隔符，再计算 SHA-256；`state`、`status`、`updated_at`、`plan_key` 和 `source_document` 不参与指纹。

读取文件时严格按 UTF-8 解码。写入前按候选全文 UTF-8 字节数检查，恰好 51,200 字节允许，51,201 字节拒绝，禁止截断。写入必须在目标同目录创建 UTF-8 临时文件、`flush` 与 `fsync` 后使用 `os.replace` 原子替换；失败时清理临时文件且原文件字节保持不变。Windows 不支持目录 `fsync` 时只允许降级目录刷新，不得跳过文件 `fsync`。

## `update_plan` payload

活动 Goal 的 payload 使用“Goal 任务进度已恢复；进行中步骤必须先核验中断点”。阻断 Goal 的 payload 使用“Goal 当前已阻断；任务列表仅用于观察进度，不恢复执行授权”。常规 persisted/exact/fallback 投影保留各自既有说明。

脚本只生成 payload，不直接调用 UI 工具。主 Agent 固定按“成功持久化 -> 读取返回 payload -> 调用 `update_plan`”执行，且只在默认执行回合调用；Plan Mode 不读取、写入或刷新投影。Goal 投影和 UI 重建均不构成执行授权。

## Goal CLI 生命周期

```text
goal --project-current PROJECT_CURRENT.md --event create
goal --project-current PROJECT_CURRENT.md --event restore
goal --project-current PROJECT_CURRENT.md --event blocked
goal --project-current PROJECT_CURRENT.md --event complete
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

无投影补建仍使用：

```text
synthesize --project-current PROJECT_CURRENT.md --input synthesis_context.json
```

`synthesize` 只处理“继续”场景的正式计划 exact/fallback 补建；它不从 Goal 原文生成任务。输出仍包含 `mode`、合法投影、活动时的 `payload` 与最小证据。`exact` 仅在唯一来源文档、普通当前状态可指向唯一任务、存在明确步骤提示且无冲突时成立；其他情况统一输出固定三步 `fallback` 安全恢复列表。
