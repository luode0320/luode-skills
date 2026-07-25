# Bug 条件路由：runtime-diagnostics

> 归属 owner：`bug-intake-rules`。本文件仅在静态证据不足时决定是否进入受控运行时观察；它不是独立 Skill，也不定义长期日志策略。

## 进入条件

- 多个根因假设无法由静态阅读排除，或关键状态只能在运行时看到。
- 需要断点、调用栈、变量快照、条件日志或临时断言观察异常位置。
- 偶发、时序或状态污染问题，且已能说明待验证假设与观察目标。

## 路由与产物

1. 先阅读 [公共契约](bug-lifecycle-common-contract.md)：只使用 local 配置，诊断以只读为先，临时资产必须可清理并归档到同一 Bug 根目录。
2. 按 [进入条件](runtime-diagnostics-bug-runtime-debug-rules-runtime-entry-conditions.md) 明确假设、观察点与退出条件，再选择 [观察手段](runtime-diagnostics-bug-runtime-debug-rules-runtime-observation-methods.md)。
3. 临时断言遵循 [断言进入条件](runtime-diagnostics-bug-assertion-diagnostic-rules-assertion-entry-conditions.md) 与 [放置规则](runtime-diagnostics-bug-assertion-diagnostic-rules-assertion-placement.md)；临时日志遵循 [日志放置规则](runtime-diagnostics-bug-debug-log-rules-debug-log-placement.md) 与 [清理规则](runtime-diagnostics-bug-debug-log-rules-debug-log-cleanup.md)。
4. 按 [退出与交接](runtime-diagnostics-bug-runtime-debug-rules-runtime-exit-and-handoff.md) 记录观察证据、已缩小范围与清理结果，并回流 `bug-root-cause-rules` 或后续生命周期入口。

## 必须保持的边界

- 禁止非 local 连接、写数据、无假设的反复试错，以及将临时断点、日志或断言保留在业务交付代码中。
- 如果静态证据还能继续收敛，或无法定义观察目标，则不得进入本路由。
- 运行时观察只提供证据，不替代根因裁决、修复方案和关闭验证；旧能力回归由 `test-regression-rules` 判断，关闭由 `bug-validation-rules` 判断。
