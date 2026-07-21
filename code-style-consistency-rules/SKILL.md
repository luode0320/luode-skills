---
name: code-style-consistency-rules
description: 当新增或修改任意代码文件、脚本文件、配置型代码或测试代码时触发；当用户以文字或截图指出某写法不对、这个风格不对、不能这么写、这样写不行时也必须触发。负责跟随项目现有写法，并在本轮已触发 `code-generation-style-rules` 时依据其产出的代码风格契约检查局部一致性，避免局部风格跳变和个人偏好入侵；同时作为全局用户风格反例库的唯一 owner，把用户否定的写法规范化为反例、把用户期望的写法记为正例，经用户确认后写入 `references/user-style-feedback-library.md` 全局永久生效，供写码前加载规避；不要用它代替最小改动、可读性、注释规范、代码归位规则或代码生成风格契约入口。
---

# 代码风格一致性规则

只在判断“这次改动有没有跟着项目现有写法走”时使用这个 skill。
如果当前争议是范围控制、结构可读性、注释内容或包结构，请交给对应的小 skill。

## Skill 作用与适用场景

- 保持同一项目、同一目录、同一模块下的写法一致。
- 基于 `code-generation-style-rules` 产出的本轮代码风格契约做一致性检查；若契约缺失，应先回到编码前风格入口补齐。
- 避免在局部改动中带入个人偏好的风格跳变。
- 跟随项目已有的缩进、空行、组织方式和常见表达习惯。
- 降低团队在审查和维护时的认知切换成本。
- 即使在做代码简化，也不引入外部模板式“优雅写法”或与项目现状割裂的表达。

## Go 路由风格约定

- `internal/router` 中统一使用单行注册格式：`group.POST("/path", controller.Method)`。
- 参数间保留 `gofmt` 标准空格，不做手写去空格风格。
- 路由说明注释放在调用上一行，避免 inline 注释导致调用被拆成多行。
- 同一函数步骤中存在多条连续路由注册时，统一使用代码块 `{ ... }` 包裹注册语句，强化步骤边界与可读性。

## Go 局部变量声明风格约定

- 函数或方法内部需要预声明变量时，禁止使用 `var (...)` 分组声明。
- 局部变量应逐行单独声明，例如 `var order *model.AdminTenantOrder`、`var err error`。
- 本约定只约束函数/方法内局部变量声明，不强制改动包级 `var (...)` 历史写法。

## Go 函数签名风格约定

- 函数或方法签名默认使用单行参数声明，不使用“每个参数一行”的多行签名写法。
- 若参数数量或语义复杂度过高导致单行可读性明显下降，优先定义参数结构体（如 `HandleStageFailureParams`）并传入该结构体。
- 避免把“参数过多”问题直接转化为多行参数列表；应通过收敛参数模型提升可读性。

## Go 代码排版补充约定

- 多参数函数调用与格式化日志调用都优先保持单行。
- 只有在单行明显过长时才换行，且换行目标要保持语义边界清楚。
- 多参数函数调用若必须换行，优先按“函数名一行、参数下一行”的方式收口；参数本身再换行时应按参数分隔符续行，可按语义分组，不要求每个参数单独一行。
- 格式化日志调用若必须换行，遵循“日志模板一行、参数下一行”的两段式写法；参数可按语义分组续行，不要求每个参数单独换行。
- 参数列表若必须继续换行，优先在参数分隔处续行，避免把同一条调用拆成多段交错块。
- 只要模板还能保留在首行，就不要把模板和第一个参数一起推到下一行。
- 反例：把 `applog.Errorf(...)`、函数调用参数、或者函数签名拆成多层碎片换行，只会增加阅读成本，不视为更优雅的风格。

## Go 编码规则清单

- 字符串去除首尾空格不是默认防御动作；只有业务规则明确要求输入归一化、外部数据已知存在首尾脏空格、或比较 / 判空 / 入库前必须统一口径时，才使用 `strings.TrimSpace`。
- 禁止在没有明确必要性的情况下，对 `item.ID`、`order.TxHash` 等字段随手包裹 `strings.TrimSpace(...)`；这类多余操作会隐藏真实数据形态，也会增加无意义的代码噪音。
- Go 常量和枚举禁止使用 `iota`，必须显式写出每个常量值；可视化和长期维护优先于少写几行代码。
- 后续团队补充 Go 编码约定时，优先追加到 `references/go-coding-rules.md` 的清单中，保持“一条规则一条 bullet”的格式。

推荐示例：

```go
applog.Infof("SEND阶段开始，order_id=%s status=%d(%s) retry_count=%d tx_hash_len=%d",
	order.OrderID, order.OrderStatus, orderStatusText(order.OrderStatus), order.RetryCount, len(strings.TrimSpace(order.TxHash)))
```

推荐示例（需要换行时）：

```go
applog.Errorf("上游接口请求失败，order_id=%s stage=%s endpoint=%s timeout_ms=%d latency_ms=%d err=%v",
	orderID, stage, resolved.URL,
	timeout.Milliseconds(), time.Since(startAt).Milliseconds(), err,
)
```

反例：

```go
applog.Errorf(
	"上游接口请求失败，order_id=%s stage=%s endpoint=%s timeout_ms=%d latency_ms=%d err=%v",
	orderID,
	stage,
	resolved.URL,
	timeout.Milliseconds(),
	time.Since(startAt).Milliseconds(),
	err,
)
```

## 用户风格反馈捕获与学习

只在用户以文字或截图指出“某写法不对 / 这个风格不对 / 不能这么写 / 这样写不行”时使用本节；本 skill 是全局用户风格反例库的唯一 owner。

- 触发信号：文字信号包含“不能这么写、这个风格不对、这个写法不对、这样写不行、别这样写、以后不要这么写”等语义；截图信号由 `image-redbox-focus-rules` 聚焦红框后路由到本节，读图理解沿用模型原生多模态能力，本节不做 OCR。
- 处理流程按 `references/style-feedback-workflow.md` 执行：定位被否定写法 → 提取正例（用户未给出则追问，不凭空生成）→ 生成 `语言|场景|反例签名` 去重键 → 组装 candidate 回显 → 用户确认后写入 `references/user-style-feedback-library.md` 的 active 条目 → 去重合并。
- 生效时机：candidate 只在当轮回显不落盘，仅 active 落盘并跨项目、跨会话永久生效（确认后生效）。
- 去重：命中同一去重键只更新出现次数与确认时间，不新增正文条目。
- 作用域边界：全局通用偏好写入本库；项目专属一次性约定仍走 `PROJECT_STYLE.md` 与 `project-style-rules`。
- 收口联动：本次写入若改动本 skill 的 `description` 或 `##` 标题，收口前重跑 `python skill-dictionary/generate_dictionary.py`，并走 `skill-execution-compliance-gate-rules`。

## 自动触发信号

- 新增代码文件。
- 用户以文字或截图指出某写法不对、风格不对、不能这么写、这样写不行。
- 修改已有文件中的实现风格。
- 补充同目录下的新函数、新方法或新测试。
- 调整局部写法时需要判断是否与项目现有风格冲突。

## 进入后先做什么

1. 若本轮涉及代码生成、修改或重构，先确认 `code-generation-style-rules` 已形成本轮代码风格契约。
2. 再观察当前目录和相邻文件的既有写法。
3. 识别本项目已经稳定存在的风格约定。
4. 区分“项目既有风格”与“个人理想风格”。
5. 在当前必要改动范围内跟随已有写法和本轮契约，而不是强推新风格。

## 默认执行流程

1. 先读取 `references/style-baseline.md`，明确风格一致性的基本原则。
2. 如果需要判断应该跟随哪个局部风格，再读取 `references/local-convention-detection.md`。
3. 如果需要判断某种写法是不是风格跳变，再读取 `references/consistency-examples.md`。
4. Go 代码改动还需读取 `references/go-coding-rules.md`，确认是否命中团队显式编码约定。
5. 优先跟随当前模块、当前目录、当前语言在仓库内的既有写法。
6. 如果仓库内存在明显冲突风格，暂停并确认应跟随哪一侧，而不是现场自定标准。

## 权责边界与不负责事项

- 只负责风格一致性，不替代 `code-generation-style-rules` 生成编码前风格契约，也不替代 `code-minimal-change-rules` 控制改动范围。
- 不替代 `code-readability-rules` 处理结构清晰度。
- 不替代注释类 skill 决定注释语言、颗粒度和写法。
- 不主动发起全仓统一格式化或大面积风格清理。

## 需要暂停并确认的条件

- 同一项目存在两套明显冲突的既有风格，无法判断该跟随哪一套。
- 为了保持一致必须扩大到大范围无关改动。
- 用户明确要求引入新风格，但仓库中没有对应先例。
- 当前目录的历史风格本身质量很差，继续跟随会明显降低可维护性。

## 执行通过 / 驳回标准

- 通过：当前改动与项目现有写法一致，没有引入新的局部风格跳变。
- 驳回：把个人偏好、外部模板风格或新的局部规则带进现有项目，导致同层代码出现明显割裂感。

## 执行结果归档要求

- 如果仓库内存在冲突风格并做了跟随选择，将结论记录到 `analysis/` 或 `doc/6-审查/`。
- 归档内容至少包含跟随依据、冲突位置和暂定处理结论。
- 如果本次只是常规跟随现有风格且无争议，可以不单独归档。

## references 读取规则

- 默认先读 `references/style-baseline.md`。
- 只有在判断应跟随哪个局部风格时，再读 `references/local-convention-detection.md`。
- 只有在对照正反例时，再读 `references/consistency-examples.md`。
- Go 代码改动默认补读 `references/go-coding-rules.md`。
- 处理用户风格反馈（文字或截图否定某写法）时，先读 `references/style-feedback-workflow.md` 走捕获学习流程。
- 组装或写入一条反例条目时，读 `references/style-case-template.md` 对齐字段与去重键。
- 写码前需要规避用户已确认反例时，加载 `references/user-style-feedback-library.md` 的 active 条目。
