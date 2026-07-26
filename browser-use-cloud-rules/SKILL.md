---
name: browser-use-cloud-rules
description: 当浏览器任务明确需要 Browser Use Cloud 的云端自主长链、托管并发、地域出口、托管代理、隐身浏览或服务商提供的合规验证码处理能力，或用户明确点名 Browser Use Cloud 时触发。作为 Browser Use Cloud 执行、安全、费用确认和 session 生命周期的唯一 Owner，负责检查 `BROWSER_USE_API_KEY`、Billing 余额、运行时 MCP 工具 schema 的硬费用上限、逐次 `run_session` / `send_task` 确认、默认无 profile/录制/保活，以及任务结束后的停止与费用回读。普通网页检索、真实 Chrome 登录态、应用内 Browser、DevTools 调试、本地 agent-browser、HAR/视觉 diff/trace 不使用本 Skill；不得用 Cloud 绕过权限、安全策略或真实浏览器连接失败。
---

# Browser Use Cloud 安全路由规则

## 目标与唯一 Owner 边界

- 只管理 Browser Use Cloud，不安装或调用本地开源 Browser Use。
- 浏览器总路由以 `../mcp-installation-rules/references/tool-priority.md` 为唯一矩阵；本 Skill 只接收已经判定为 Cloud 专属的任务。
- 费用确认只授权本次 Cloud 消费，不授权提交表单、购买、发布、发消息、创建账号或其它业务副作用。
- Cloud 不替换 Chrome Plugin、应用内 Browser、Chrome DevTools MCP、`browser-session-automation-rules` 或 `browser-advanced-testing-rules`。

## 触发后先做什么

1. 冻结任务摘要、目标域名、读写动作、业务副作用和预期完成条件。
2. 读取 [routing-and-safety.md](references/routing-and-safety.md)，复核 Cloud 正向条件、禁止替代场景和 MCP 配置边界。
3. 检查当前进程环境变量 `BROWSER_USE_API_KEY`，只报告存在或缺失，不读取其它凭据来源。
4. 从当前 Browser Use Cloud MCP 工具描述取得本次收费动作的真实 JSON schema：创建任务读取 `run_session`，追加任务读取 `send_task`；不得根据 REST 文档猜测 MCP 已支持同名参数。
5. 运行 `scripts/browser_use_cloud_preflight.py` 查询 Billing 并检查当前动作的可写 input schema。只有 `ready_for_confirmation` 可进入普通费用确认。

密钥缺失时固定输出：

> Browser Use Cloud 已命中，但本机未检测到 `BROWSER_USE_API_KEY`。请从 Browser Use Cloud 设置页取得 key，在本机用户环境变量中配置后重启 Codex；不要在聊天中粘贴 key。

## 预检命令

运行时把 MCP 暴露的 `run_session` schema 保存到本地临时 JSON 文件，只包含工具 schema，不包含请求、响应或凭据：

```bash
python -X utf8 -B browser-use-cloud-rules/scripts/browser_use_cloud_preflight.py \
  --action run_session \
  --schema-file <run-session-schema.json>
```

- 默认 Billing endpoint 为官方 `https://api.browser-use.com/api/v2/billing/account`。
- `--billing-url` 只允许上述官方 endpoint 或 loopback local mock；不得改到 test、staging、pre、release 或 production 业务服务。
- stdout 只允许脱敏 JSON；stderr、异常和测试 fixture 也不得包含 key、姓名、项目 ID 或订阅 ID。
- 状态只允许：`ready_for_confirmation`、`blocked_key_missing`、`blocked_auth`、`blocked_billing`、`blocked_no_credit`、`blocked_hard_cap_unavailable`。

## 硬费用上限与确认

- 运行时 schema 的可写 `inputSchema.properties.maxCostUsd` 明确为数值字段时，必须为本次动作设置用户确认的美元上限。不得从 output schema、描述、示例或推测别名判断硬上限存在。
- schema 没有硬上限时保持 `blocked_hard_cap_unavailable` 并默认取消。只有用户当次先明确接受“服务端无法强制本次硬预算”的风险，才允许继续到费用确认；该风险接受不能绕过密钥、认证、Billing 或余额阻断。
- 免费层、赠送额度或余额充足都不能跳过确认，也不得表述为“配置 key 后永久免费”。
- 使用宿主可用的阻塞确认能力，确认框不得自动超时或采用推荐项；宿主没有阻塞确认能力时停止并等待用户明确答复，不调用 Cloud。

每次 `run_session` 前展示并确认：

- 任务摘要、目标域名和业务副作用范围。
- 模型；未指定时写“服务商默认模型”。
- profile：默认不使用。
- 代理与地域：写明用户选择或服务商默认值。
- 录制：默认关闭。
- `keep_alive=false`。
- 当前免费层状态、脱敏余额和本次硬费用上限；无硬上限例外时明确标红风险。

每次 `send_task` 都必须用 `--action send_task` 和当前 `send_task` schema 重新执行预检及本节确认，不能复用 `run_session` 的硬上限结论、余额或授权，也不能复用上一次 `send_task` 的授权。默认 `keep_alive=false`；只有已有 session 曾经获得显式保活授权时才可能进入 `send_task`。

## 执行和 session 收口

1. 用户确认后才调用 `run_session` 或 `send_task`，并且只执行已展示的任务和参数。
2. 默认不传 `profile_id`，不上传 Cookie、localStorage、密码、本地 Chrome profile 或登录状态；默认关闭录制、计划任务、临时邮箱和与任务无关的内置扩展能力。
3. 成功、失败或用户取消后都调用 `get_session`。
4. 状态仍为 `created`、`idle` 或 `running` 时调用 `stop_session(strategy="session")` 销毁整个 sandbox；禁止使用只停止当前 task、让 session 留在 `idle` 的策略。
5. 停止后有限次回读 `get_session`；只有最终 `status="stopped"` 才算清理完成，仍为活跃状态或未知状态时失败关闭。
6. 最终必须读取非负有限的 `totalCostUsd`，并在返回可用时分别报告 `llmCostUsd`、`proxyCostUsd`、`browserCostUsd`；缺少总费用、费用非法或只有估算时不得声称费用已回读。

## 安全停止条件

- key 缺失、401/403、账户不存在、余额不明、响应损坏、超时或未知 Billing 字段。
- 余额为零或负数。
- 运行时 schema 无法取得、无法解析或没有硬费用上限，且用户未当次接受无硬上限风险。
- 用户没有完成本次确认，或确认内容与实际参数不一致。
- 任务需要上传用户登录态、绕过权限/安全策略、规避站点限制，或业务副作用未单独授权。
- 无法确认遗留 session 已停止，或无法读取最终实际费用。

## 验证

- 单元测试：`python -X utf8 -B -m unittest discover -s browser-use-cloud-rules/tests -p "test_*.py"`。
- Skill 校验：`python -X utf8 -B .system/skill-creator/scripts/quick_validate.py browser-use-cloud-rules`。
- 测试只能使用 loopback local mock 和哨兵 key，不调用真实 Browser Use Cloud，不消费额度；必须覆盖两种收费动作的独立 schema、output schema 误判、三类任务结果清理、`strategy="session"`、最终 stopped 状态和实际费用回读。
