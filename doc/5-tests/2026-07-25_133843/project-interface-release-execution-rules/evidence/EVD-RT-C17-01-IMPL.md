# EVD-RT-C17-01-IMPL

## 结论

C17-01 已完成接口结果与消费者场景结果拆分。接口结果继续写入兼容的 `release-test-report.json`，并新增 `interface-results.json`；场景结果只接受 `scenario_results`，写入 `scenario-results.json`，不再把接口结果冒名写入场景报告。

## 实现范围

- `report.py` 新增真实场景步骤事件规范化，固定 `run_id/scenario_id/step_id/action/status/duration_ms/failure_type`。
- 新增 `consumer-coverage.json`、`protocol-capabilities.json`、`cleanup-report.json`、`dual-gate-diff.json` 和 `evidence-manifest.json`。
- 缺少真实场景输入时写入 `not_configured`，不伪造 runtime PASS。
- 覆盖和清理状态以真实场景结果派生，外部附加摘要不能覆盖失败或阻断。
- 产物参考清单已同步更新。

## 安全与兼容

请求、响应、捕获值和步骤输出沿用递归脱敏；证据清单只保存相对路径、SHA-256 和脱敏标志。旧报告字段和旧返回路径保留。
