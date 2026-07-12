# EVD-TASK-RT-C09-02-TEST

## 真实测试

命令：`python -X utf8 -m unittest doc/5-tests/2026-07-12_191712/project-release-test-rules/tests/test_contract_reconcile.py -v`

结果：`6/6 PASS`，覆盖：

- 三方完全一致并生成 report；
- manifest 单边新增接口；
- schema hash 漂移；
- reusable 参数 stale projection；
- 重复 interface_id；
- 全资产缺失；
- 兼容 CLI 子进程入口和 UTF-8 输出。

全量回归：当天测试目录 `26/26 PASS`。
