# 运行时观察手段

## 用途

用于选择当前最合适的运行时诊断方式。

## 常见手段

- 断点与单步
  适合观察关键分支和状态变化顺序。
- 变量观察与调用栈
  适合确认异常状态是在哪里进入当前函数的。
- debug 日志
  适合定位偶发链路、上下游输入输出和关键条件命中。
- 断言检查
  适合快速暴露不变量被破坏的位置。

## 选择原则

- 先用最小侵入的方式。
- 先观察最关键的状态点，不做全链路无差别打印。
- 诊断手段要服务于当前假设，而不是“什么都加一点”。

## Heisenbug：调试工具附加即消失的 Bug

某些 Bug 在附加调试工具时消失（断点改变时序掩盖竞态、观察动作本身影响结果）：

- 改用日志 / 追踪（低侵入、不改时序）代替交互式 debugger。
- 语言支持时运行 race detector（Go `-race`、Python `asyncio` debug mode、Java/JVM 线程转储）。
- 明确记录「附加调试工具时是否改变行为」这一观察，本身就是诊断结论的一部分。

## 跨语言工具参考表

| 类别 | 工具 / 手段 |
|------|------------|
| 堆栈 | Python traceback、Java/JS stack trace、Go panic 输出、Rust backtrace |
| 日志 | Python `logging`、JS `console`、结构化 JSON 日志 |
| 调试器 | `pdb`/`ipdb`、Chrome DevTools、`gdb`/`lldb`、`dlv`（Go） |
| 性能 | `cProfile`、`py-spy`、Chrome Performance、`pprof`（Go） |
| 内存 | `tracemalloc`、Valgrind、Chrome Heap Snapshots |
| 并发 | thread dump、`asyncio` debug mode、Go `-race` |
