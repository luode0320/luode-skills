# EVD-RT-C18-01-IMPL

## 结论

C18-01 已完成旧资产和 CLI 兼容迁移。旧列表式 `scenario-results.json` 可读取但会标记 `deprecated`，每条旧接口结果降为 `PENDING/LEGACY_INTERFACE_RESULT`；新增 `external-migrate` 输出独立迁移文件，不覆盖输入。

## 兼容边界

旧 `run`、`doctor` 和 `release-run` 入口继续保留；新版报告对象和旧列表形状都能被兼容层识别。旧资产不能绕过 verified 场景生命周期或场景门禁。
