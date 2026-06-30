# 上线接口测试产物清单

本文件定义 `project-release-test-rules` 执行后必须产出的正式测试资产。

## 中文说明目录
- `README.md`
  - 测试范围
  - 扫描与对账摘要
  - 必测/可选测/跳过接口统计
  - 门禁结论
  - 阻断原因与风险项

## ASCII 镜像目录
- `release-test-plan.yaml`
- `interface-test-results.md`
- `inventory-reconcile.yaml`
- `artifacts/raw-request/<接口标识>.json`
- `artifacts/raw-response/<接口标识>.json`
- `artifacts/masked-response/<接口标识>.json`
- `artifacts/logs/execute.log`
- `scripts/` 下的测试脚本或调用样本

## 产物要求
- 请求参数和简要响应必须为 JSON 字符串。
- 完整响应必须落盘，不能只保留在主报告中。
- 对账结果必须作为独立产物留存，便于追溯本轮新增、删除和漂移。
- 若某接口未执行，必须在结果中记录未执行原因，不能静默省略。
