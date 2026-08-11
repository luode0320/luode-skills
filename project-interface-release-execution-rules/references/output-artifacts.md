# 上线接口测试产物清单

本文件定义 `project-interface-release-execution-rules` 执行后必须产出的正式测试资产。

## 中文说明目录
- `README.md`
  - 测试范围
  - 扫描与对账摘要
  - 必测/可选测/跳过接口统计
  - 门禁结论
  - 阻断原因与风险项

## `doc/5-tests/` 中文主报告与机器产物根
- `release-test-plan.yaml`
- `interface-test-results.md`
- `interface-sync-report.yaml`
- `inventory-reconcile.yaml`
- `dependency-graph.json`
- `scenario-results.json`
- `interface-results.json`
- `consumer-coverage.json`
- `protocol-capabilities.json`
- `cleanup-report.json`
- `dual-gate-diff.json`
- `evidence-manifest.json`
- `.release-test-engine/shadow-evidence/<run_id>.json`（仅 shadow 硬切历史证据，路径相对项目根）
- `.release-test-engine/verification-evidence/<摘要>.json`（candidate 晋级证据，绑定正向、故障与清理运行）
- `artifacts/raw-request/<接口标识>.json`
- `artifacts/raw-response/<接口标识>.json`
- `artifacts/masked-response/<接口标识>.json`
- `artifacts/dependency-trace.json`
- `artifacts/dependency-trace/<接口标识>.json`
- `artifacts/resolved-params/<接口标识>.json`
- `artifacts/reusable-param-events.yaml`
- `artifacts/baseline-update-summary.yaml`
- `artifacts/logs/execute.log`

说明：上述时间戳目录只保存说明、响应、报告、日志、对账结果、截图和其他非可执行证据。可执行测试脚本、mock、stub、fake、fixture、helper、数据构造和调用样本不属于本目录。

## 根 `test/` 源码镜像

- `test/<被测源码目录镜像>/...`：源码关联的可执行接口测试脚本、mock、stub、fake、fixture、helper、数据构造和调用样本
- `test/shared/...`：仅跨源码复用的可执行测试辅助资产

测试资产不得写入业务源码目录、`doc/5-tests/` 或任意其他 `*/tests/` 目录。每轮中文主报告应通过路径或清单引用 `test/release-artifacts/YYYY-MM-DD_HHmmss_release-interface-test/` 的机器产物，以及根 `test/` 中实际执行的脚本和模拟程序。

## 产物要求
- 请求参数和简要响应必须为 JSON 字符串。
- 完整响应必须落盘，不能只保留在主报告中。
- 对账结果必须作为独立产物留存，便于追溯本轮新增、删除和漂移。
- 双索引同步结果必须作为独立产物留存，便于追溯当前代码、`swag/.swag-manifest.yaml` 与 `interface-inventory.yaml` 是否一致。
- shadow evidence 必须绑定文件 SHA-256，并能从场景目录全集和脱敏场景结果独立重算门禁；普通报告摘要不能替代该文件。
- 若某接口未执行，必须在结果中记录未执行原因，不能静默省略。
- 每个由 provider、local 数据、fixture 或规则解析出的参数都必须有依赖追踪产物。
- 每个新增、复验成功、失效、隔离或废弃的可复用参数都必须写入 `reusable-param-events.yaml`。
- 每轮测试结束后必须生成 `baseline-update-summary.yaml`，说明本轮对 `doc/5-tests/基线/` 的回写内容。
- `dependency-graph.json` 应从 `doc/5-tests/基线/dependency-graph.yaml` 派生，记录本轮实际执行顺序和阻断节点。

## 长期基线回写产物

每次测试结束后必须同步更新 `doc/5-tests/基线/`：

- `interface-inventory.yaml`
- `dependency-graph.yaml`
- `parameter-sources.yaml`
- `reusable-params.yaml`
- `scenario-catalog.yaml`
- `script-adapter.yaml`
- `execution-history.yaml`
- `baseline-change-log.md`
- `README.md`
