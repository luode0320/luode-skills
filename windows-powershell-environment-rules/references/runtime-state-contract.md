# Windows PowerShell 环境运行状态契约

脚本统一返回 `ready`、`degraded`、`blocked`、`busy`、`failed`、`rolled_back` 或 `rollback_refused`。`ready` 和 `degraded` 的退出码都是 `0`，因为两者都允许当前调用继续；区别必须由 JSON 的 `status` 和 `issues` 读取。

## 状态规则

- `ready`：当前策略的必需和可选工具均满足。
- `degraded`：必需条件满足，仅可选工具、Terminal 或非当前 shell 可见性存在限制。
- `blocked`：PowerShell 7、UTF-8 或当前策略的明确必需条件无法满足。
- `busy`：另一个环境写操作正在持有状态锁。
- `failed`：状态、manifest 或事务发生不能安全继续的错误。

## 状态文件

- `session-marker.json`：缓存 SessionEnsure 的可继续结果；`complete=true` 可以表示 `ready` 或 `degraded`。
- `last-run.json`：最新运行的结构化结果。
- `runs/<run-id>/journal.json`：一次 Apply 或 Rollback 的不可覆盖证据。
- `discovered-tools.json`：只保存已验证的动态工具；没有精确安装来源的条目必须标为 `check_only`。
- `failure-cases.json`：只保存脱敏环境失败证据，不晋级长期 active 规则。

## 回滚边界

Terminal 或 profile 仅在当前文件 SHA-256 仍等于 Apply 后 hash 时恢复。安装的软件包永不自动卸载。
