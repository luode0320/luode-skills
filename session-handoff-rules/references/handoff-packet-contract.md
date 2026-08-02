# 交接包契约

交接包是传给新 Codex 任务的脱敏 JSON。它只描述“要继续什么”和“继续前要核验什么”，不承载宿主会话身份、凭据、完整日志或执行授权。文件默认使用 UTF-8，正文不超过 24,576 字节。

## 必填结构

顶层只允许以下字段：

| 字段 | 类型 | 约束 |
| --- | --- | --- |
| `schema_version` | string | 固定为 `1.0` |
| `packet_type` | string | 固定为 `codex-session-handoff` |
| `created_at` | string | UTC ISO-8601 时间 |
| `task_summary` | string | 一句话描述当前任务，不能含绝对路径或秘密 |
| `goal` | string | 当前任务的可验证目标 |
| `scope` | object | 只允许 `in_scope`、`out_of_scope` 两个字符串数组 |
| `completed` | array | 已由当前会话完成并有证据的事项，可为空 |
| `in_progress` | array | 当前正在处理的事项，可为空；未知中断点必须写明 |
| `next_steps` | array | 必须至少有一项，按执行顺序排列 |
| `blocked` | array | 阻断、等待或未决事项，可为空 |
| `validation` | array | 已执行验证及结果，可为空；静态检查不能写成运行成功 |
| `decisions` | array | 稳定决策和边界，可为空 |
| `continuation` | object | 只允许下文定义的四个字段 |

`continuation` 必须包含：

```json
{
  "project_alias": "当前保存项目的短名称",
  "environment": "local",
  "archive_policy": "manual_only",
  "new_session_prompt": "新任务首轮先命中检查并重新读取项目四件套，再核验交接包和中断点。"
}
```

`project_alias` 只能是短名称或仓库相对标识，不得写 `C:\...`、`/home/...`、UNC 路径或其它绝对路径。`environment` 固定为 `local`；`archive_policy` 固定为 `manual_only`。每个数组最多 40 项，每项最多 2,000 个 Unicode 字符；对象、数组和字符串不得包含 NUL 控制字符。

## 脱敏规则

- 拒绝敏感字段名：`api_key`、`access_token`、`refresh_token`、`password`、`secret`、`private_key`、`authorization`、`cookie`、`connection_string`、`credential`、`session_id`、`thread_id` 等及其大小写、连字符、空格变体。
- 拒绝看起来像秘密的值：`Bearer` 鉴权值、`sk-` / `rk-` 长密钥、JWT、私钥头、带账号密码的数据库 URL，以及 `password=...`、`token: ...` 等赋值片段。
- 不传原始用户 prompt、完整响应、完整日志、截图内容、绝对本机路径、外部服务地址或连接串。需要定位文件时只写仓库相对路径、模块名和符号名。
- 以“脱敏后无法确认”为准：宁可删掉一项并写“需在新任务中只读核验”，也不要把原始值带入新任务。

## 有效示例

```json
{
  "schema_version": "1.0",
  "packet_type": "codex-session-handoff",
  "created_at": "2026-08-02T08:00:00Z",
  "task_summary": "新增会话交接 skill 并完成本地契约测试",
  "goal": "让新 Codex 任务能够安全接续当前任务并保留明确的下一步",
  "scope": {
    "in_scope": ["skill 规则", "交接包校验", "Codex App 新任务路由"],
    "out_of_scope": ["自动归档旧任务", "Git 历史写入"]
  },
  "completed": ["完成触发词清单"],
  "in_progress": ["补齐交接包脚本；尚未执行真实测试"],
  "next_steps": [
    "创建并运行交接包契约测试",
    "刷新 skill 字典并检查触发词"
  ],
  "blocked": [],
  "validation": ["尚未运行测试，不能宣称通过"],
  "decisions": ["归档策略固定为 manual_only"],
  "continuation": {
    "project_alias": "skills",
    "environment": "local",
    "archive_policy": "manual_only",
    "new_session_prompt": "先重新命中检查、读取四件套并核验进行中断点。"
  }
}
```

## 校验入口

```text
python -X utf8 -B session-handoff-rules/scripts/validate_handoff_packet.py <packet.json>
```

退出码为 `0` 才允许调用 `codex_app__create_thread`。脚本只读取输入，不修改原文件；失败时输出字段级原因，不能用最终回复口头说明替代校验。
