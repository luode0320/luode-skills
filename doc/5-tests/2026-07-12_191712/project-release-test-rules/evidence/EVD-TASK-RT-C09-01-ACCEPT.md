# EVD-TASK-RT-C09-01-ACCEPT

## 验收

- [x] 完整三方 fixture 返回 `status=PASS`，每个来源都有 path、sha256、loaded_at、source_type、status。
- [x] manifest/inventory/reusable 任一缺失返回 `missing_*`，聚合 `requires_refresh=true`。
- [x] 非法 YAML 返回 `BASELINE_INVALID`，非 local 路径返回 `NON_LOCAL_ASSET`。
- [x] strict pipeline 将契约同步失败写入报告并把 gate 置为 `BLOCKED`。
- [x] C08 local 回归通过，未改变默认非 strict 的既有执行和 baseline replay。

结论：TASK-RT-C09-01 完成，可进入 TASK-RT-C09-02；C09-02 的集合/hash 对账仍是后续门禁前置条件。
