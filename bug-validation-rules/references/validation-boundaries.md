# 验证边界

- 修复验证聚焦当前缺陷是否关闭；功能验证聚焦当前需求是否实现正确；回归验证聚焦旧能力是否被带坏，三者可以连续执行但不得混写职责。
- Bug 结论记录统一沉淀到 `doc/4-bugs/`；活动测试脚本、测试数据、mock 与 fixture 按 `test-strategy-rules` 的 `test-asset-governance` 条件路由归入根 `test/`，报告和证据放入 `doc/5-tests/<时间戳>/`。
