# EVD-TASK-RT-C08-03-TEST

- 状态：PASS（产物结构）；完整上线放行：BLOCKED。
- 真实测试：旧轮 `27/27 PASS`，本轮 `16/16 PASS`；新增 C08 local artifact replay 为 `1/1 PASS`。
- 产物检查：中文 README、ASCII 报告、responses、dependency graph、scenario results、sync/reconcile、raw/masked response、resolved params、dependency trace 均存在。
- 报告契约检查：`dataPreview`、P0/P1/P2 风险统计、参数生命周期统计、同步元数据和 baseline projection summary 均有断言。
- 阻断：本次端口 fixture 未启动，报告门禁为 `PARTIAL`；该结果被保留，不改写为 PASS。
