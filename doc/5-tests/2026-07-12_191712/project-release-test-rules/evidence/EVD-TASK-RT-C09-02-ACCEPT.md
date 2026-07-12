# EVD-TASK-RT-C09-02-ACCEPT

## 验收

- [x] 三方完整一致时 `synced=true`、`status=PASS`。
- [x] 任一单边集合、重复 interface_id 或 schema hash 不一致时 `status=BLOCKED`。
- [x] schema 漂移输出旧/新 hash 证据，并将关联 reusable sample 标记为 `stale/schema_changed`。
- [x] 兼容 CLI 输出 `interface-sync-report.yaml`，不改 manifest/inventory/reusable 源文件。
- [x] C09-01 与历史 C08 回归保持通过，当天全量测试 `26/26 PASS`。

结论：`TASK-RT-C09-02` 完成，可进入 `TASK-RT-C10-01`；上线放行仍受 C10-C12 约束。
