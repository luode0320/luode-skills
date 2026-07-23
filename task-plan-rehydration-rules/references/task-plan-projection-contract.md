# 任务投影持久化与重建契约

## 托管区边界

`PROJECT_CURRENT.md` 最多存在一个任务投影托管区：

```markdown
<!-- BEGIN TASK PLAN PROJECTION -->
```json
{
  "version": 1,
  "state": "active",
  "plan_key": "REQ-RTP-001/CYCLE-RTP-01",
  "source_document": "doc/3-实施/example.md",
  "plan_fingerprint": "<64 位 SHA-256>",
  "updated_at": "2026-07-23T00:00:00Z",
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
```

标记必须成对、顺序正确且只出现一次。零个区块时 `write` 可在文件末尾追加；已有一个区块时只替换区块本身。缺半边、重复、嵌套或逆序标记全部拒绝。

## Schema

顶层字段必须且只能包含：

| 字段 | 约束 |
|---|---|
| `version` | 固定为整数 `1` |
| `state` | `active` 或 `inactive` |
| `plan_key` | 活动投影非空；空失活槽位允许空字符串 |
| `source_document` | 活动投影非空；空失活槽位允许空字符串 |
| `plan_fingerprint` | 非空步骤必须是根据步骤计算的 64 位小写 SHA-256 |
| `updated_at` | 带 UTC 时区的 ISO-8601，例如 `2026-07-23T00:00:00Z` |
| `steps` | 数组，最多 20 项 |

每个步骤必须且只能包含：

| 字段 | 约束 |
|---|---|
| `id` | 非空字符串，当前投影内唯一 |
| `step` | 非空字符串，最多 256 个 Unicode 字符 |
| `status` | `pending`、`in_progress` 或 `completed` |

最多一个步骤处于 `in_progress`。`active` 必须包含至少一个未完成步骤；`inactive` 只允许空步骤或全部完成步骤。

## 指纹

指纹只包含步骤 ID、顺序和文案：

```json
[
  {"id":"TASK-RTP-01","step":"[TASK-RTP-01] 冻结恢复契约"}
]
```

序列化固定使用 UTF-8、`ensure_ascii=false`、键排序和紧凑分隔符，再计算 SHA-256。`state`、`status`、`updated_at`、`plan_key` 和 `source_document` 不参与指纹。

## 失活槽位

新项目模板使用以下空槽位，表示没有可恢复任务：

```json
{
  "version": 1,
  "state": "inactive",
  "plan_key": "",
  "source_document": "",
  "plan_fingerprint": "",
  "updated_at": "1970-01-01T00:00:00Z",
  "steps": []
}
```

计划完成时允许保留已完成步骤和来源信息，只把 `state` 改为 `inactive` 并更新时间。任何失活投影都不得生成 `update_plan` payload。

## 敏感字段与大小

投影采用字段白名单并递归拒绝敏感键，包括 `prompt`、`response`、`token`、`api_key`、`password`、`secret`、`private_key`、`thread_id`、`user_input` 和 `business_data`。未知字段同样拒绝。

读取文件时严格按 UTF-8 解码。写入前按候选全文 UTF-8 字节数检查，恰好 51,200 字节允许，51,201 字节拒绝。禁止截断。

## 原子写入

1. 在目标文件同目录创建临时文件。
2. 以 UTF-8 和原正文换行风格写入候选全文。
3. `flush` 并 `fsync` 临时文件。
4. 关闭临时文件后使用 `os.replace` 原子替换。
5. 失败时清理临时文件，原文件保持不变。
6. Windows 不支持目录 `fsync` 时只允许降级目录刷新，不得跳过文件 `fsync`。

## `update_plan` payload

活动投影输出：

```json
{
  "explanation": "悬浮任务列表已从 PROJECT_CURRENT 重建；进行中步骤必须先核验中断点",
  "plan": [
    {
      "step": "[TASK-RTP-01] 冻结恢复契约",
      "status": "in_progress"
    }
  ]
}
```

脚本只生成 payload，不直接调用 UI 工具。Agent 必须真实调用 `update_plan` 后才能声称悬浮任务列表已重建。
