# 执行失败持续学习与主动预防：前向行为验证

## 测试目的

验证 `execution-failure-learning-rules` 的 `prevent`、`recover`、`learn` 合同，覆盖验收标准 AC-001 至 AC-008。测试使用脱敏输入和本地仓库文件，不连接外部服务，不读写 test/prod 配置。

## 测试对象

- `execution-failure-learning-rules/SKILL.md`
- `execution-failure-learning-rules/references/classification-and-routing.md`
- `execution-failure-learning-rules/references/lifecycle-and-gates.md`
- `execution-failure-learning-rules/references/case-template.md`
- 首批 owner Skill 的路由与案例库路径

## 执行方式

```powershell
python -X utf8 doc/5-tests/2026-07-12_031353/execution_failure_learning_rules/forward_behavior_test.py
```

依赖：Python 3，标准库。测试脚本会输出每个验收场景的 `PASS` 日志和最终结论。

## 覆盖范围

| 场景 | 结果 |
| --- | --- |
| 已知 active 案例执行前预检 | PASS |
| 未知失败恢复后同输入、同成功标准复验 | PASS |
| 未授权 candidate 不晋级 active | PASS |
| 业务 Bug 不进入案例库 | PASS |
| 预期负向测试不触发学习晋级 | PASS |
| secret、私有路径脱敏 | PASS |
| 无 owner 转 `skill-evolution-rules` | PASS |
| active 与 candidate 冲突阻断复用 | PASS |

## 真实测试资产

- `doc/5-tests/2026-07-12_031353/execution_failure_learning_rules/forward_behavior_test.py`

## 验证结论

执行输出为 25 项断言全部 `PASS`，最终结论为 `forward behavior contract tests: PASS`。该测试验证的是 Skill 规则契约和路由行为，不替代真实图像 API、浏览器、MCP 或生产服务联调。
