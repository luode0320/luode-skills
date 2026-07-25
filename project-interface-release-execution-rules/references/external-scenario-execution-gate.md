# 外部消费者场景真实执行与双轨门禁

> 归属 owner：`project-interface-release-execution-rules`。本文件定义 HTTP/SSE/WebSocket/Socket.IO 的真实运行、报告和发布切换。

## 协议与真实运行

- HTTP 覆盖 JSON、form、multipart、下载头与内容摘要；SSE 覆盖订阅就绪、HTTP 触发、事件关联、断流和游标重连。
- 原生 WebSocket 必须使用 RFC 6455 真实连接，覆盖握手、鉴权、收发、顺序、重复、关闭和重连。
- Socket.IO 必须使用真实 namespace/event/ack 连接，不能用普通 WebSocket fixture 替代。
- 跨协议场景至少证明写入、实时事件和最终 HTTP 读回使用同一关联值。
- fixture PASS 只能作为测试支撑证据，不能冒充被测 runtime 的 PASS。

## 事件日志与状态

- 每个步骤日志固定包含 `run_id/scenario_id/step_id/action/status/duration_ms/failure_type`。
- 场景状态只允许 `PASS/FAIL/BLOCKED/PENDING`。
- 协议 runtime 缺失返回 PENDING；环境、安全、探针越权或清理失败返回 BLOCKED；确定性断言和传输错误返回 FAIL。
- 所有实时连接无论主流程结果如何都必须关闭。

## CLI 与退出码

- 增强入口固定为 `external-doctor/generate/validate/verify/run/migrate`。
- `release-run --gate-mode legacy|shadow|scenario` 是发布兼容入口，未显式指定时继续默认 `legacy`。
- `external-run` 未显式指定 `--gate-mode` 时固定默认 `scenario`；不得因复用旧 parser 而静默落入 legacy、跳过消费者场景。
- 退出码固定为 `0=PASS`、`1=场景断言 FAIL`、`2=CLI 或契约无效`、`3=环境或安全 BLOCKED`、`4=候选或覆盖缺口 PENDING`。
- doctor 未通过时不得进入项目发现、接口请求或实时协议连接。

## 报告与证据

- 接口结果与场景结果必须分开写入 `interface-results.json` 和 `scenario-results.json`。
- 附属资产固定为 `consumer-coverage.json`、`protocol-capabilities.json`、`cleanup-report.json`、`dual-gate-diff.json` 和 `evidence-manifest.json`。
- 证据清单只保存相对路径、SHA-256 和脱敏状态，不复制原始请求响应。
- 空场景输入必须报告 `not_configured`，不能报告 PASS。

## 场景硬门禁

- 场景门禁以 verified 目录的 P0/P1 场景全集为分母，不接受结果子集自报覆盖。
- missing、unexpected、duplicate、来源指纹不一致或目录为空均为覆盖阻断。
- 所选 P0/P1 任一 `FAIL/BLOCKED/PENDING` 或必需清理未 PASS 均禁止自动放行。
- P2 不影响自动门禁分母，但风险和结果必须可追踪。

## shadow 与硬切

- `shadow` 同时运行 legacy 与场景轨道；切换前 legacy 仍决定当前自动放行，差异必须分类并解释。
- 切换要求连续 3 次全量 local 运行：P0/P1 覆盖 100%、场景全部 PASS、清理 100%、无未解释差异、同一场景目录指纹。
- 三条历史必须具有唯一 `run_id`、可复核 `evidence_digest`，最后一条属于当前运行。
- 每条 shadow 历史还必须绑定项目根内 `.release-test-engine/shadow-evidence/<run_id>.json` 的相对路径和文件 SHA-256；纯内存自签摘要、绝对/越界路径、缺失文件或文件篡改均固定为 `BLOCKED/HISTORY_EVIDENCE_INVALID`。
- evidence 文件固定包含场景目录全集、脱敏场景结果、legacy 状态摘要、场景门禁和双轨差异；切换判断必须回读文件，重算目录指纹、P0/P1 场景门禁、cleanup 结果和未解释差异，再与历史摘要逐字段对账。
- 硬切后 `active_mode=scenario`，运行时禁止请求 legacy 或 shadow，不得自动回退旧门禁。
