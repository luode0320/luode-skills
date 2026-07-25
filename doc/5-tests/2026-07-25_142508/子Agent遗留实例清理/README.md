# 子 Agent 遗留实例清理测试证据

## 结论

本测试任务验证 `parallel-task-dispatch-rules` 的进入前预检、批次回收、终局扫描、真实关闭双重判定、下一批门禁和数量对账。平台没有真实关闭工具时，测试只允许产生未关闭告警，不把 `interrupt_agent` 或完成通知伪报为关闭。

## 真实测试资产

- 标准库契约测试：`parallel-task-dispatch-rules/tests/test_subagent_lifecycle_contract.py`
- 执行命令：`/usr/local/python3.14/bin/python3 -X utf8 parallel-task-dispatch-rules/tests/test_subagent_lifecycle_contract.py`
- 环境：local；不连接数据库、缓存、消息队列或 HTTP/RPC 上游。

## 覆盖范围

| 场景 | 断言 |
| --- | --- |
| 仍需执行的运行实例 | 保留实例，不计未关闭 |
| 已终态实例 | 真实关闭成功且复查不活跃后才计入关闭 |
| 运行实例回收 | 必须先停止再关闭 |
| 中断通知 | `interrupt_agent` 不计关闭 |
| 关闭成功但复查仍活跃 | 不计关闭并阻止下一批 |
| 关闭工具失败或不可用 | 只告警，阻止下一批 |
| 重复扫描 | 按 `agent_id` 去重，结果幂等 |
| 根 Agent / 其他会话 | 不扫描、不关闭 |
| 混合失败/取消/中断/放弃终态 | 可独立关闭，关闭数不要求等于完成数 |

## 证据

- 2026-07-25：11 项生命周期契约测试通过。
- 目标文件 UTF-8 回读通过，目标范围 `git diff --check` 通过。
- 当前平台真实枚举：`/root/audit_subagent_cleanup` 已完成但仍可见；平台未提供真实关闭能力，因此最终对账必须保留 `未关闭数=1` 和告警。
