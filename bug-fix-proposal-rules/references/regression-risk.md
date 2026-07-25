# 高影响修复的回归风险路由

本 reference 归属 `bug-fix-proposal-rules#regression-risk`，仅在修复已定位且会影响公共方法、共享模块、接口、数据库、缓存、兼容性、异常语义或历史能力时阅读。

输出必须包含改动点、影响对象、风险等级、分级依据、高风险验证重点、已知风险与补救安排；风险识别不是回归测试，普通旧能力回归交给 `test-regression-rules`，关闭判定交给 `bug-validation-rules`。

依次读取：

1. `regression-risk/risk-dimensions.md`：识别风险维度。
2. `regression-risk/risk-ranking-and-scope.md`：完成分级与验证优先级。
3. `regression-risk/risk-examples.md`：需要校准高低风险判断时使用。
