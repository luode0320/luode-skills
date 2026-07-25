# EVD-RT-C16-02-IMPL

- 完成 `scenario.cleanup` 白名单执行、脱敏报告和失败升级。
- 主流程 PASS/FAIL 后均执行清理；清理禁止嵌套 cleanup 和 state.probe。
- 清理失败保留步骤输出并把最终状态升级为 `BLOCKED/CLEANUP_FAILED`。
