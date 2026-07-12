# EVD-TASK-ARR-03-TEST

## 真实测试

- `test_agent_runtime_recovery.py`：`9/9 OK`。
- 覆盖敏感字段、额外业务字段、`scope_hash`、TTL 过期、损坏 JSON、单飞锁和 `resumed -> healthy`。
- 所有临时文件位于 `TemporaryDirectory`，测试后清理完成。
