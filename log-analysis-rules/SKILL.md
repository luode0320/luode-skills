---
name: log-analysis-rules
description: 当用户要求查日志、读日志、日志分析、根据日志定位问题、按 request-id 反查请求链路、切换日志级别取证，或接口测试失败后需要服务端日志取证时触发。本 skill 是读日志侧唯一权威，负责日志文件定位、级别切换、请求全链路反查、日志过滤取证与调试窗口使用回收纪律；写日志归 logging-trace-rules，根因裁决归 bug-root-cause-rules，临时调试日志放置与清理归 bug-intake-rules 的 runtime-diagnostics。
---

# 日志读取与取证规则

只在判断"怎么取日志、怎么读日志、怎么按日志定位问题、调试窗口怎么用"时使用这个 skill。
如果当前问题是"怎么写日志"，请转交 `logging-trace-rules`；如果是错误处理机制本身，请转交 `error-handling-rules`；如果是临时调试日志的放置与清理，请转交 `bug-intake-rules` 的 runtime-diagnostics；如果是监控平台或告警体系，请单独处理，不在这个 skill 里扩张。

## Skill 作用与适用场景

- 定义日志文件路径约定与当日文件定位方法。
- 定义 DEBUG 级别切换与恢复纪律。
- 定义按 request-id / trace-id 反查一次请求全链路的方法。
- 定义日志取证过滤（时间窗、关键词、错误堆栈）。
- 定义调试窗口（前端 console、IDE 调试窗口、调试器输出）的使用与回收纪律。
- 作为"读日志"侧唯一权威：其它 skill 需要查日志取证时引用本 skill，不重复发明读日志步骤。
- 读日志动作只做"取、读、定位"，不做根因最终裁决；裁决归 `bug-root-cause-rules`。

## 自动触发信号

- 用户说"查日志""日志分析""根据日志定位""看服务端日志""看日志文件"。
- bug 定位进入日志取证环节，需要从日志文件取证据。
- apifox 等接口测试用例失败，响应体无法定位，需要服务端日志取证。
- 需要切换日志级别（如切 DEBUG）观察运行现场。
- 使用前端 console / IDE 调试窗口打印观察量。
- 需要对已有日志按时间窗、关键词、request-id 过滤并输出取证片段。

## 进入后先做什么

1. 判断日志来源：本地服务日志文件 / 调试窗口输出 / 远端服务日志。
2. 按 `references/log-file-location.md` 定位日志文件与当日文件，禁止凭记忆猜路径。
3. 若需要更细粒度观察，按 `references/log-level-switching.md` 切换 DEBUG 并记录切换事实与恢复计划。
4. 若存在关联标识（request-id / trace-id / 订单号），按 `references/request-id-traceback.md` 反查全链路。
5. 按 `references/log-fetch-and-filter.md` 用时间窗与关键词过滤取证。
6. 取证完成后按 `references/debug-window-discipline.md` 回收临时观测，恢复原日志级别。

## 默认执行流程

1. 默认先读 `references/log-file-location.md`，确认日志文件路径约定与当日文件。
2. 再读 `references/log-fetch-and-filter.md`，按过滤规则取证。
3. 需要全链路反查时，读 `references/request-id-traceback.md`。
4. 需要更细粒度级别时，读 `references/log-level-switching.md`。
5. 使用调试窗口时，读 `references/debug-window-discipline.md`。

## 权责边界与不负责事项

- 只负责"读日志、取证、定位"动作本身，不负责最终根因裁决（归 `bug-root-cause-rules`）。
- 不负责"怎么写日志"——格式、字段、框架、脱敏、trace 透传（归 `logging-trace-rules`）。
- 不负责临时调试日志的放置与清理（归 `bug-intake-rules` 的 runtime-diagnostics）。
- 不负责错误处理机制本身（归 `error-handling-rules`）。
- 不负责监控告警平台策略。

## 需要暂停并确认的条件

- 无法确定日志文件位置，或服务日志不可达。
- 需要长期提升日志级别（超过本次观测窗口）而未获用户确认。
- 日志中缺少可反查标识，无法按 request-id 拼接全链路。
- 取证涉及敏感字段脱敏，无法判断哪些可写入测试主文档。

## 执行通过 / 驳回标准

- 通过：日志文件定位正确；过滤条件明确可复现；取证片段带时间戳、文件路径与行号；临时观测已回收、日志级别已恢复。
- 驳回：凭猜测读日志；无过滤条件大海捞针；取证片段无来源标识；调试窗口打印残留未清理；DEBUG 级别切换后未恢复。

## references 读取规则

- 默认先读 `references/log-file-location.md`。
- 取证过滤读 `references/log-fetch-and-filter.md`。
- 全链路反查读 `references/request-id-traceback.md`。
- 级别切换读 `references/log-level-switching.md`。
- 调试窗口读 `references/debug-window-discipline.md`。
