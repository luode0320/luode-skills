---
name: logging-trace-rules
description: 当新增或修改日志、logger、trace、span、审计日志、脱敏字段、排障字段、日志配置文件或链路透传逻辑时触发。负责统一日志与链路追踪规则，后端日志必须使用项目日志框架且不得使用控制台打印，并通过配置文件管理日志参数；业务日志默认必须使用中文表达，只有协议字段、固定 key、第三方固定原文等少数例外可以保留原文；日志初始化必须在 LoadConfig 之后且仅初始化一次，禁止空配置预初始化；不要用它代替错误处理、响应结构或长期监控告警策略。
---

# 日志与追踪规则

只在判断“该记什么日志、记录在哪个点、trace / span 怎么透传、不同日志类型怎么分层”时使用这个 skill。
如果当前问题是错误处理机制本身，请转交 `error-handling-rules`；如果当前问题是监控平台或告警体系，请单独处理，不在这个 skill 里扩张。

## Skill 作用与适用场景

- 统一业务日志、调试日志、审计日志的边界。
- 约束 trace / span 的透传与关键链路记录点。
- 明确日志字段、上下文信息和脱敏要求。
- 强制后端日志使用项目日志框架，不允许 `fmt.Println`、`println`、`console.log` 等控制台打印。
- Go 项目日志框架实现统一放在 `utils/log/`，业务代码统一调用该封装。
- 强制日志能力配置化，日志级别、文件路径、轮转参数等必须来自配置文件。
- 强制日志初始化顺序：必须先读取配置（LoadConfig），再初始化 logger。
- 强制日志只初始化一次，禁止重复初始化或多处初始化。
- 强制禁止空配置预初始化（例如 `Init(config.LogConfig{})`）。
- 强制日志调用排版规范：`Infof/Errorf/Warnf` 等格式化日志优先单行；若长度过长必须换行时，第一行只放日志模板字符串，下一行开始放参数，避免参数被拆成多段零碎换行。
- 日志排版的目标是“模板和参数分层清晰”，不是“强行按视觉等宽平均分块”；能一行写完就不要拆。
- 如果参数本身还很长，可以继续在参数行内换行，但必须保持同一参数列表连续，不要把参数拆成很多碎片，也不要把模板和参数交错换行。
- 防止把排障日志、业务日志和审计日志混成一套。
- 业务日志默认必须中文表达，只有协议字段、固定 key、第三方 SDK/API 固定字段名或第三方固定原文可以保留原样，不得把整条业务日志长期写成英文。
- 用户要求“补充日志 / 只补日志 / 日志完善”时，只处理当前 `git` 未提交的改动文件，未变动的历史文件不纳入本轮日志补齐范围。
- 业务日志开头必须使用 `[业务简要说明]` 前缀，例如 `[失败回调]`、`[tenantclient 下单]`，后面再跟具体上下文；简要说明必须能直接看出业务场景，不允许只写技术缩写。

## 自动触发信号

- 新增或修改 logger、日志字段、日志模板。
- 新增或修改日志初始化、日志配置项、日志目录或日志输出目标。
- 新增或修改的代码文件中已经存在日志调用时，即使本轮没有直接改动日志文本，也必须复核该文件内与改动上下文相关的日志是否符合中文表达、业务前缀和敏感信息规则。
- 新增或修改 `LoadConfig`、日志初始化入口、启动流程装配顺序。
- 新增或修改 trace-id、span-id、链路上下文透传。
- 新增或修改审计日志、排障日志、debug 日志。
- 用户要求“补充日志”“只补日志”“日志完善”。
- 不确定某条信息该记录成业务日志、调试日志还是审计日志。

## 进入后先做什么

1. 先判断当前记录点属于业务过程、调试排障还是审计留痕。
2. 确认当前服务使用的日志框架和项目封装（例如 Go 的 `go.uber.org/zap` + `utils/log/` 封装）。
3. 确认日志配置文件中已声明日志级别、路径、轮转和输出目标，禁止默认仅控制台输出。
4. 确认启动顺序为“先 LoadConfig，再 InitLogger”，且 logger 只初始化一次。
5. 确认不存在空配置预初始化（例如 `Init(config.LogConfig{})`）。
6. 再确认是否需要 trace / span 上下文。
7. 明确哪些字段必须记录，哪些字段需要脱敏。
8. 确定日志只记录必要上下文，不做无意义刷屏。
9. 按日志排版规范收口代码样式：能一行则一行；必须换行则“模板一行 + 参数下一行（必要时参数续行）”。
10. 如果本轮改动文件包含日志调用，先扫描这些文件中的日志文本，发现英文业务日志、无业务前缀、裸打敏感字段或控制台打印时，必须在当前文件范围内同步修正。
11. 如果本轮是补日志请求，必须逐一检查本轮所有改动位点的日志，不允许只改一部分最显眼的日志。
12. 如果是补日志请求，只收敛当前未提交的改动文件，未变动文件即使存在日志问题也不在本轮范围内。

## 默认执行流程

1. 默认先读 `references/backend-framework-and-config.md`，确认日志框架约束与配置项要求。
2. 再读 `references/log-types-and-fields.md`，判断日志类型和字段层次。
3. 如果涉及 trace / span 或链路透传，再读 `references/trace-propagation.md`。
4. 如果需要判断记录点和正反例，再读 `references/logging-examples.md`。
5. 输出日志框架方案、配置方案、初始化顺序方案（LoadConfig -> InitLogger，且仅一次）、日志类型、字段方案、trace 透传要求和不应记录的内容。
6. 如果当前只是临时诊断日志，提醒与 Bug 域调试日志区分，并明确后续是否保留。

## 权责边界与不负责事项

- 只负责日志与链路追踪规则，不代替 `error-handling-rules` 设计异常处理路径。
- 不代替监控、告警、报表平台设计。
- 不允许后端以控制台打印替代正式日志框架。
- 不允许在多个模块重复初始化 logger。
- 不允许在配置加载前用空配置预初始化 logger。
- 不把所有调试打印都合理化成正式业务日志。
- 不把审计日志、业务日志和 debug 日志混成同一个字段集。
- 不允许把一条 `Infof/Errorf/Warnf` 的参数无限拆成多段视觉噪音换行，导致日志代码可读性明显下降。
- 不允许把业务日志长期写成英文模板；只有协议字段、固定 key、第三方固定原文等少数例外可以保留原样。
- 不允许把未变动的历史文件纳入本轮补日志范围；补日志只能收敛到当前 `git` 未提交的改动文件。
- 不允许业务日志没有 `[业务简要说明]` 前缀，也不允许前缀只有技术缩写而看不出业务场景。

## 需要暂停并确认的条件

- 日志内容包含敏感信息、隐私信息或高风险字段。
- trace 透传会影响上下游约定或旧链路兼容。
- 审计日志是否必须保留还不明确。
- 当前计划新增大量日志，但无法说明用途和记录点价值。
- 当前日志方案无法说明配置来源，或日志仍只输出到控制台。
- 当前无法确认日志初始化顺序（LoadConfig 与 InitLogger）或初始化次数。

## 执行通过 / 驳回标准

- 通过：能明确日志框架、配置来源、初始化顺序（LoadConfig 后初始化且仅一次）、日志类型、关键字段、记录点、trace 透传方式和脱敏边界；业务日志默认中文表达，仅少数协议字段/固定 key/第三方原文保留例外；业务日志统一以 `[业务简要说明]` 前缀开头；本轮改动文件内与改动上下文相关的既有日志已复核；本轮补日志请求时，当前未提交改动文件的日志都已检查完毕，未变动文件未被纳入。
- 驳回：使用控制台打印替代正式 logger、缺少配置化管理、配置加载前初始化 logger、重复初始化、使用空配置预初始化、日志类型混乱、字段随意、trace 断链、敏感信息裸打、业务日志长期英文化，或把临时 debug 日志当成长期正式日志，或改动文件内明显相关的既有英文业务日志未复核，或补日志请求只改了一部分日志位点，或把未变动的历史文件纳入本轮补日志范围，或业务日志缺少 `[业务简要说明]` 前缀。

## 日志排版规范（新增）

适用范围：`Infof`、`Warnf`、`Errorf` 及同类格式化日志调用。

规则：
- 能一行写完日志模板与参数时，优先单行。
- 如果一行过长必须换行，必须采用“日志模板单独一行，参数从下一行开始”的两段式。
- 参数过长时可以继续换行，但保持同一参数列表连续，不要把模板和参数反复交错换行。
- 只要模板还能保留在首行，就不要把模板和第一个参数一起挪到下一行。

推荐示例（短日志，单行）：

```go
applog.Infof("确认订单跳过，order_id=%s 原因=终态成功", order.OrderID)
```

推荐示例（长日志，两段式）：

```go
applog.Errorf("确认订单里程碑状态写入失败，order_id=%s from=%d(%s) to=%d(%s) err=%v",
	order.OrderID, order.OrderStatus, orderStatusText(order.OrderStatus), constant.OrderStatusChainConfirmedSuccess,
	orderStatusText(constant.OrderStatusChainConfirmedSuccess), err)
```

推荐示例（较短的两段式调用）：

```go
applog.Infof("SEND阶段开始，order_id=%s status=%d(%s) retry_count=%d tx_hash_len=%d",
	order.OrderID, order.OrderStatus, orderStatusText(order.OrderStatus), order.RetryCount, len(strings.TrimSpace(order.TxHash)))
```

反例（不推荐，过度拆分导致阅读成本高）：

```go
applog.Errorf(
	"确认订单里程碑状态写入失败，order_id=%s from=%d(%s) to=%d(%s) err=%v",
	order.OrderID,
	order.OrderStatus,
	orderStatusText(order.OrderStatus),
	constant.OrderStatusChainConfirmedSuccess,
	orderStatusText(constant.OrderStatusChainConfirmedSuccess),
	err,
)
```

反例（不推荐，模板与参数反复交错拆分）：

```go
applog.Errorf(
	"确认订单里程碑状态写入失败，order_id=%s from=%d(%s) to=%d(%s) err=%v",
	order.OrderID, order.OrderStatus,
	orderStatusText(order.OrderStatus), constant.OrderStatusChainConfirmedSuccess,
	orderStatusText(constant.OrderStatusChainConfirmedSuccess), err,
)
```

## 执行结果归档要求

- 如果本次定义了日志字段规范、trace 透传方案或审计边界，将结论记录到 `analysis/` 或 `review/`。
- 归档内容至少包含日志类型、关键字段、透传方案、脱敏说明和兼容影响。
- 如果只是沿用既有清晰模式且无争议，可以不单独归档。

## references 读取规则

- 默认先读 `references/backend-framework-and-config.md`。
- 再读 `references/log-types-and-fields.md`。
- 只有在处理 trace / span 时，再读 `references/trace-propagation.md`。
- 只有在对照正反例或记录点时，再读 `references/logging-examples.md`。
