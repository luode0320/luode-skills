# Plan Mode 计划出口回归

本目录验证 `BUG-PLAN-OUTPUT-20260726-001` 的四类行为：计划出口唯一性、`WAITING_DECISION` 冻结、压缩恢复不生成总结，以及 Default Mode 的普通总结兼容性；同时接入既有永久等待状态模型，覆盖空答案、部分答案、单活动框和冻结输出。

运行命令：

`py.exe -3 -X utf8 -B doc/5-tests/2026-07-26_plan-output/test_plan_output_contract.py`

通过标准：本目录 6 个契约测试全部通过，并在测试入口内运行 `doc/5-tests/2026-07-26_040607/plan_mode_wait_loop/test_plan_mode_wait_loop.py` 的 10 项状态模型回归。

样本全部为脱敏消息，不包含原始凭证、token、Cookie、连接串或用户私密数据。
