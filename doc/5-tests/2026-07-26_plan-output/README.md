# Plan Mode 计划出口回归

本目录验证 `BUG-PLAN-OUTPUT-20260726-001` 的四类行为：计划出口唯一性、`WAITING_DECISION` 冻结、压缩恢复不生成总结，以及 Default Mode 的普通总结兼容性；同时接入既有永久等待状态模型，覆盖空答案、部分答案、单活动框和冻结输出。

运行命令：

`py.exe -3 -X utf8 -B test/implementation-planning-rules/plan_output_contract_test.py`

通过标准：活动测试入口 15 个契约测试全部通过，并在测试入口内运行 `doc/5-tests/2026-07-26_040607/plan_mode_wait_loop/test_plan_mode_wait_loop.py` 的 10 项状态模型回归。

样本全部为脱敏消息，不包含原始凭证、token、Cookie、连接串或用户私密数据。

历史可执行资产已于 2026-08-09 按根 `test/` 唯一活动测试代码根规则迁出：`test_plan_output_contract.py` 与 `fixtures/plan_output_cases.json` 现位于 `test/implementation-planning-rules/`，本目录只保留说明与证据。
