# 统一智能体运行期自恢复规则测试

## 测试目标

验证 `agent-runtime-recovery-rules` 是否形成平台无关的恢复协议，并确认 MCP/插件安装规则已经把运行期故障路由给统一 owner。

## 环境与边界

- 环境：local 文件 fixture；Python 3 标准库；不启动外部服务。
- 数据：规则文件、adapter schema、失败路由和案例库。
- 禁止：连接 test/prod、调用真实 MCP、重启宿主、修改安装配置。

## 执行命令

```powershell
python -X utf8 doc/5-tests/2026-07-12_203429/agent-runtime-recovery-rules/test_agent_runtime_recovery.py
```

## 通过标准

- 统一 skill、schema、状态机、能力矩阵和案例库均存在且为 UTF-8 可读文件。
- schema 声明 `L0` 到 `L5`、`probe/reconnect/reload/restart/resume` 和脱敏检查点字段。
- 统一 owner 明确禁止非幂等自动重放、未授权进程操作和无 capability 的重启。
- 失败路由包含 `mcp_runtime_transport`、`plugin_runtime_unhealthy`、`agent_host_unhealthy`，且安装 skill 仍保留 provisioning 职责。

## 清理与回滚

本测试为只读静态契约测试，无临时服务、数据库或持久化运行状态；失败时仅修正规则资产，回滚以本轮文件 diff 为边界。
