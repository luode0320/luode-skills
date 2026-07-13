# 恢复状态机与执行边界

## 状态和事件

| 状态 | 进入条件 | 允许动作 | 成功出口 | 失败出口 |
| --- | --- | --- | --- | --- |
| `healthy` | 探针与最小调用通过 | 正常工作 | `suspected` 由故障事件触发 | N/A |
| `suspected` | timeout、EOF、reset、不可达 | 一次探针、一次不变复验 | `healthy` | `diagnosed` |
| `diagnosed` | 已分类且 owner 为本 skill | capability 协商、作用域检查 | `recovering` | `manual_handoff` |
| `recovering` | 选定一个未尝试的恢复层 | reconnect/reload/restart | `reconnected`/`reloaded`/`restarted` | `blocked` |
| `reconnected` | L2 成功 | `wait_ready`、能力探测 | `verified` | `blocked` |
| `reloaded` | L3 成功 | `wait_ready`、能力探测 | `verified` | `blocked` |
| `restarted` | L4 成功且进程指纹可信 | `wait_ready`、能力探测 | `verified` | `blocked` |
| `verified` | 恢复后健康调用通过 | L5 resume 或人工交接 | `resumed` | `manual_handoff` |
| `resumed` | checkpoint、token 和原成功标准均通过 | 继续原任务 | `healthy` | `manual_handoff` |
| `manual_handoff` | 非幂等、无 resume、上下文不可恢复 | 输出原因和交接信息 | 终态 | N/A |
| `blocked` | 越权、预算耗尽、探针失败或安全条件不满足 | 只保留证据 | 终态 | N/A |

## 事件分类

- `transport_timeout`、`transport_disconnect`、`protocol_unavailable`：先 `suspected`，不直接重启。
- `component_unhealthy`：必须有组件级 capability 才能进入 `recovering`。
- `host_unhealthy`：只允许宿主 adapter 声明的 L4/L5；禁止猜测宿主进程。
- `resume_context_missing`、`checkpoint_invalid`：直接 `manual_handoff` 或 `blocked`，不得重放。

## 单飞、预算和冷却

`lock_key` 由平台、组件和作用域稳定生成。获取单飞锁失败时等待当前 `recovery_id` 的终态；不得启动第二个动作。默认预算如下：探针 1 次、不变复验 1 次、L2/L3/L4 各 1 次、`wait_ready` 2 次，每次等待超时后即终止当前层。成功或终态失败后设置 600 秒冷却；冷却内新故障复用结果并转人工交接。

预算计数必须原子递增，进程崩溃后可由 TTL 清理未完成锁。任何 adapter 只允许缩小预算、延长等待并说明原因，不得突破全局上限。

## 恢复后验证

恢复动作返回成功不等于恢复完成。必须依次验证：组件可达、协议版本/能力、最小只读健康调用、组件/会话指纹。L5 额外验证 checkpoint TTL、resume token、工作区/任务指纹和原成功标准。任一失败即进入 `blocked` 或 `manual_handoff`。

## 不可逆动作保护

非幂等调用在故障发生后可能已在远端生效；自动重放会造成重复写入。因此只能执行只读状态查询，携带原操作摘要和幂等键供人工判断。恢复规则不得替业务层声明未知操作为幂等。

## 终态阻断交接

`blocked` 与 `manual_handoff` 都是任务不能继续安全推进的终态。恢复引擎必须在终态结果中输出唯一 `BLK-runtime-*` 事实，字段遵循 `../../artifact-delivery-gate-rules/references/task-blocker-closure-contract.md`：状态、运行时恢复阶段、脱敏原因和 recovery/component 证据、已尝试层级与停止边界、影响、人工或上层 agent 的恢复计划、最小健康检查重入点，以及“原因码 + 组件 ID”去重键。

`healthy` 与 `resumed` 不输出阻断事实。没有 adapter、权限、可靠幂等性或恢复后健康检查时，恢复计划必须停在人工交接，不得重放操作或声称已经续接任务。
