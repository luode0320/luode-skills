---
name: bug-runtime-debug-rules
description: 当仅靠静态分析不能稳定定位 Bug，且需要在运行过程中通过断点、单步执行、变量观察、调用栈观察、条件命中判断、debug 日志或运行时证据来缩小问题范围时触发。负责运行时诊断进入条件、观察方式、退出条件和证据回流；不要把它当成默认第一选择。
---

# Bug 运行时诊断规则

只在静态定位已经无法继续有效收敛时使用这个 skill。
如果当前仍能通过代码、日志、trace 和调用链继续静态定位，就不要过早进入运行时调试。

## Skill 作用与适用场景

- 在静态证据不足时，通过运行时观察缩小 Bug 范围。
- 统一断点、单步、变量观察、调用栈观察、条件命中、debug 日志和断言诊断的进入条件。
- 规定运行时诊断什么时候结束，产物如何回流到根因结论。
- 防止把运行时调试变成无边界试错。

## 自动触发信号

- 静态定位已经明确卡住，多个根因假设无法排除。
- 关键状态只能在运行时观察到。
- 需要通过断点、变量快照、条件日志或断言检查才能发现异常位置。
- 偶发问题、时序问题、状态污染问题无法只靠静态阅读确认。

## 进入后先做什么

1. 先记录静态定位做到哪一步、卡在什么地方。
2. 明确本次运行时诊断要验证哪个假设、观察哪个状态。
3. 选择最小必要的诊断手段，不一上来全都用。
4. 规划诊断结束条件，避免无限试错。

## 默认执行流程

1. 默认先读 `references/runtime-entry-conditions.md`，确认当前是否真的需要进入运行时诊断。
2. 再读 `../artifact-storage-rules/references/path-map.yaml` 与 `../artifact-storage-rules/references/update-policy.md`，确认 Bug 根目录、入口 `README.md` 和同一 Bug 持续复用同一根目录的策略。
3. 再读 `references/runtime-observation-methods.md`，选择断点、变量观察、debug 日志、断言等合适手段。
4. 如果需要判断何时结束或如何回流，再读 `references/runtime-exit-and-handoff.md`。
5. 输出本轮诊断目标、观察点、得到的运行时证据和下一步结论，并更新到当前 Bug 根目录下的 `README.md`。
6. 结束后要么回流到 `bug-root-cause-rules` 固化结论，要么直接进入 `bug-fix-proposal-rules`。

## 权责边界与不负责事项

- 只负责运行时诊断，不替代 `bug-root-cause-rules` 的静态定位职责。
- 不代替 `bug-debug-log-rules` 讨论长期日志策略；这里的 debug 日志仅用于诊断。
- 不直接给出修复方案，那属于 `bug-fix-proposal-rules`。
- 不把断点、日志和断言长期残留在交付代码中。

## 需要暂停并确认的条件

- 当前问题其实还能继续静态收敛，不值得进入运行时调试。
- 运行时诊断需要修改风险较高的环境或行为，但尚未确认。
- 诊断目标不清，无法说明这次要验证什么假设。
- 运行时证据采集已经开始失控，出现无目标的反复试错。

## 执行通过 / 驳回标准

- 通过：能说明为什么要进入运行时诊断、观察了什么、得到了什么证据、这些证据如何缩小了问题范围。
- 驳回：没有明确假设就盲目打断点、盲目加日志，或运行时调试结束后仍无法说清得到的证据。

## 执行结果归档要求

- 将运行时诊断目标、观察点、关键变量或日志证据、结束结论统一记录到 `artifact-storage-rules` 约定的当前 Bug 根目录中。
- 归档内容至少包含进入原因、采用手段、观察结果、收缩结论、后续流转，以及临时 debug 日志或断言代码是否已删除。
- Bug 根目录、入口 `README.md` 和同一 Bug 根目录复用策略统一遵循 `../artifact-storage-rules/references/path-map.yaml` 与 `../artifact-storage-rules/references/update-policy.md`。
- 如果本轮诊断同时使用了调试日志和断言，相关记录统一落在同一个 Bug 根目录中，不再分散到 `analysis/` 或其他目录。

## references 读取规则

- 默认先读 `references/runtime-entry-conditions.md`。
- 在定位当前 Bug 根目录、入口 `README.md` 或判断是否继续复用同一根目录时，先读 `../artifact-storage-rules/references/path-map.yaml` 与 `../artifact-storage-rules/references/update-policy.md`。
- 只有在选择诊断手段时，再读 `references/runtime-observation-methods.md`。
- 只有在判断结束条件和交接方式时，再读 `references/runtime-exit-and-handoff.md`。
