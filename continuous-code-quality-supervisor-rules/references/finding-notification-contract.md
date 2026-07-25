# Finding 与通知契约

## Finding 必填字段

每条 finding 必须是结构化对象，至少包含：

| 字段 | 类型 | 约束 |
|---|---|---|
| `owner_skill` | 字符串 | 必须来自允许 Owner；缺失时为 `unclassified` |
| `rule_source` | 字符串 | 当前 Owner `SKILL.md` 或其 reference 的相对路径 |
| `file` | 字符串 | 受影响文件相对路径，不保存文件正文 |
| `evidence` | 字符串 | 一行、短摘要、可定位，不放代码正文或凭据 |
| `severity` | 枚举 | `P0`、`P1`、`P2`、`P3` |
| `fingerprint` | 字符串 | `owner + rule_source + file + evidence` 的稳定摘要 |
| `status` | 枚举 | `open`、`limited`、`resolved`、`suppressed` |

## 限制 finding

Owner 文件缺失、名称不一致或规则来源不可读时必须使用：

```json
{
  "owner_skill": "unclassified",
  "rule_source": "missing-owner",
  "file": "<relative-path>",
  "evidence": "Owner source unavailable; static quality check not performed",
  "severity": "P1",
  "fingerprint": "<stable-sha256>",
  "status": "limited"
}
```

这类记录只说明检查受限，不代表发现了业务质量问题，也不允许监督 Skill 自行补充规范。

## 去重规则

1. 指纹由 Owner、规则来源、相对文件位置和短证据摘要计算。
2. 同一指纹再次出现时更新 `last_seen`、扫描次数和最近状态，不追加第二条记录。
3. 证据变化或 Owner 来源变化时生成新指纹，不覆盖旧记录。
4. 状态文件只保存摘要、时间、次数和位置，不保存 diff、代码正文、Goal 原文或通知响应。

## 通知载荷

通知实际实施会话时只发送：扫描标识、finding 指纹、Owner、规则来源、文件位置、短证据、严重级别、当前状态和修复回执要求。通知不是自动修改授权，不得要求监督会话直接改代码。

## 通知状态

| 状态 | 含义 | 监督动作 |
|---|---|---|
| `pending` | 已写入 finding，尚未确认发送 | 下一周期允许重试 |
| `sent` | 宿主确认已发送 | 等待实施会话处理 |
| `acknowledged` | 实施会话已确认 | 下一周期重新观察 |
| `limited` | 通知能力不可验证 | 保留限制事实，不报成功 |

## 安全拒绝

发现 `prompt`、`response`、`token`、`password`、`secret`、`private_key`、`api_key` 等字段，或 evidence 包含多行代码正文时，拒绝写入并将监督状态置为 `blocked`。预期负向测试和用户取消不得生成任务阻断事实。
