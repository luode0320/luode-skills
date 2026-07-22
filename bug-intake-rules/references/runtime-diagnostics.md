# Bug 条件路由：runtime-diagnostics

> 归属 owner：`bug-intake-rules`。本文件只承接条件路由细则，不创建第二个自动触发入口。迁移后的规则、用户习惯、local 安全红线、授权边界、暂停/停止、清理、回滚和归档要求继续有效。

## 迁移保留规则：bug-assertion-diagnostic-rules

# Bug 断言诊断规则

只在已有明确怀疑点，需要用断言或诊断检查快速缩小 Bug 区间时使用这个 skill。
如果当前还不清楚要验证什么，请先转 `bug-intake-rules` 的 `runtime-diagnostics` 条件路由；如果要设计正式参数校验，请转交相邻业务校验或错误处理规则。

## Skill 作用与适用场景

- 用快速失败和不变量检查尽快暴露异常区间。
- 约束断言适合放在哪里、检查什么、持续多久。
- 将断言方案、失败结果和清理状态统一收口到同一个 Bug 根目录。
- 帮助区分状态污染、顺序错误、分支误走和数据不一致。
- 防止把诊断断言混成正式业务规则。

## 自动触发信号

- 怀疑某个状态在运行途中被意外改写或污染。
- 怀疑调用顺序、生命周期或并发顺序错乱。
- 需要快速确认某个不变量是不是被破坏。
- 普通日志不足以收缩问题发生区间。
- 需要将本轮断言记录与同一 Bug 的日志记录统一保存在一个 Bug 根目录下。

## 进入后先做什么

1. 先定义要验证的状态、不变量或顺序假设。
2. 为当前 Bug 确认统一的根目录，具体路径、目录名和入口文件统一遵循 `artifact-storage-rules`。
3. 选择最能缩小区间的断言位置，而不是到处都加。
4. 明确断言失败后需要记录什么上下文。
5. 提前决定断言在问题定位或修改完成后如何删除，并同步记录删除结论。

## 默认执行流程

1. 默认先读 `bug-intake-rules/references/runtime-diagnostics-bug-assertion-diagnostic-rules-assertion-entry-conditions.md`，先判断当前是否适合用断言诊断。
2. 再读 `../artifact-storage-rules/references/path-map.yaml` 与 `../artifact-storage-rules/references/update-policy.md`，确认 Bug 根目录、入口 `README.md` 和同一 Bug 持续复用同一根目录的策略。
3. 如需继续展开，再读 `bug-intake-rules/references/runtime-diagnostics-bug-assertion-diagnostic-rules-assertion-placement.md`，需要决定断言放置位置和粒度。
4. 需要对照边界或正反例时，再读 `bug-intake-rules/references/runtime-diagnostics-bug-assertion-diagnostic-rules-assertion-examples.md`，需要对照断言诊断样例。
5. 输出断言诊断方案、放置位置、Bug 根目录记录方案和失败后的处理口径，并更新到当前 Bug 根目录下的 `README.md`。
6. 断言结果应回流 `bug-intake-rules` 的 `runtime-diagnostics` 条件路由 或 `bug-root-cause-rules` 固化定位结论；诊断代码进入测试和交付前必须经过 `implementation-review-rules` 检查。

## 权责边界与不负责事项

- 只负责诊断性断言，不代替正式输入校验和业务校验。
- 不在高风险路径随意加入会改变业务行为的重断言。
- 不把所有怀疑点都写成断言，必须有明确假设。
- 诊断断言属于调试改动，问题定位或修改完成后必须删除。
- 如果后续确实需要正式保护逻辑，必须删除当前诊断断言，再按正式校验逻辑重新设计，不能直接保留当前断言。
- 不默认长期保留诊断断言。

## 需要暂停并确认的条件

- 断言目标不清，无法说明要验证什么不变量。
- 断言会显著改变业务流程或引发不可接受的副作用。
- 断言失败后缺少上下文，无法支撑定位。
- 团队打算把诊断断言直接作为正式规则上线，但没有重新审查。
- 当前 Bug 还没有建立统一的 Bug 根目录，导致断言记录和日志记录可能再次分散。

## 执行通过 / 驳回标准

- 通过：能够说明断言验证什么、为什么放在这里、失败后会暴露什么信息；相关记录统一落在当前 Bug 根目录下；问题定位或修改完成后这些诊断断言已删除。
- 驳回：断言只是为了碰碰运气，没有清晰假设，没有统一 Bug 根目录记录，或断言本身引入额外混乱。

## 执行结果归档要求

- 将断言目标、位置、失败结果和删除结论统一记录到 `artifact-storage-rules` 约定的当前 Bug 根目录中。
- 当前 Bug 根目录必须包含 `README.md`，至少写明问题现象、验证假设、断言位置、失败摘要、定位结论和清理状态。
- Bug 根目录、入口 `README.md` 和同一 Bug 根目录复用策略统一遵循 `../artifact-storage-rules/references/path-map.yaml` 与 `../artifact-storage-rules/references/update-policy.md`。
- 如果同一 Bug 有多轮断言诊断和日志诊断，统一放在同一个 Bug 根目录下，不再分散记录到其他目录。
- 如果后续需要补正式保护逻辑，应在删除当前诊断断言后，另行按正式校验规则重新设计。

## references 读取规则

- 只要创建或修改 Bug 根目录 `README.md`，必须同时读取 `../artifact-delivery-gate-rules/references/plain-language-document-contract.md`，正文先写结论，技术细节保留在原有章节或附录。
- 如果本轮涉及审查、验收、功能验证、浏览器联调或第三方验证，必须同时读取 `../artifact-delivery-gate-rules/references/review-acceptance-gate-contract.md`，按适用性记录，不把不适用条件写成阻断。
- 默认先读 `bug-intake-rules/references/runtime-diagnostics-bug-assertion-diagnostic-rules-assertion-entry-conditions.md`。
- 在定位当前 Bug 根目录、入口 `README.md` 或判断是否继续复用同一根目录时，先读 `../artifact-storage-rules/references/path-map.yaml` 与 `../artifact-storage-rules/references/update-policy.md`。
- 只有在 规划断言位置和失败上下文 时，再读 `bug-intake-rules/references/runtime-diagnostics-bug-assertion-diagnostic-rules-assertion-placement.md`。
- 只有在 对照正反例或判断是否越界 时，再读 `bug-intake-rules/references/runtime-diagnostics-bug-assertion-diagnostic-rules-assertion-examples.md`。

## 迁移保留规则：bug-debug-log-rules

# Bug 调试日志规则

只在需要通过临时日志补充运行期证据，并且已有明确观察目标时使用这个 skill。
如果当前还没有明确观察目标，请先转 `bug-intake-rules` 的 `runtime-diagnostics` 条件路由；如果需要正式日志治理，请转交 `logging-trace-rules`。

## Skill 作用与适用场景

- 用最小可回收的临时日志补足运行期证据。
- 约束日志放在哪里、打什么、打到什么粒度就够。
- 强制临时日志沿用项目 logger，不允许 `fmt.Println`、`println`、`console.log` 等控制台打印。
- 将日志方案、观察结果和清理状态统一收口到同一个 Bug 根目录。
- 防止把诊断日志写成长期噪音或泄露敏感信息。
- 为后续清理和记录收口提供明确要求。

## 自动触发信号

- 需要观察关键变量、条件分支、上下游请求响应或时间线。
- 断点不方便或线上问题需要通过日志补证。
- 需要区分多个根因假设，但现有日志不足。
- 团队准备临时加打印，但尚未明确哪些日志是必须的。
- 需要将本轮日志记录与同一 Bug 的断言记录统一保存在一个 Bug 根目录下。

## 进入后先做什么

1. 先明确本轮日志要验证什么假设、观察哪个状态。
2. 为当前 Bug 确认统一的根目录，具体路径、目录名和入口文件统一遵循 `artifact-storage-rules`。
3. 确认临时日志调用方式沿用项目 `utils/log/` 封装，不走控制台打印。
4. 选择最靠近证据点的最小日志落位。
5. 控制日志粒度、输出量、敏感字段和生命周期。
6. 提前约定日志在问题定位或修改完成后如何删除，并同步记录删除结论。

## 默认执行流程

1. 默认先读 `../logging-trace-rules/references/backend-framework-and-config.md`，确认日志框架和配置约束。
2. 再读 `bug-intake-rules/references/runtime-diagnostics-bug-debug-log-rules-debug-log-placement.md`，先判断日志应落在哪些关键证据点。
3. 再读 `../artifact-storage-rules/references/path-map.yaml` 与 `../artifact-storage-rules/references/update-policy.md`，确认 Bug 根目录、入口 `README.md` 和同一 Bug 持续复用同一根目录的策略。
4. 如需继续展开，再读 `bug-intake-rules/references/runtime-diagnostics-bug-debug-log-rules-debug-log-cleanup.md`，需要规划日志生命周期和回收方式。
5. 需要对照边界或正反例时，再读 `bug-intake-rules/references/runtime-diagnostics-bug-debug-log-rules-debug-log-examples.md`，需要对照日志诊断正反例。
6. 输出调试日志方案、落点说明、Bug 根目录记录方案和清理要求，并更新到当前 Bug 根目录下的 `README.md`。
7. 日志加完后继续回到 `bug-intake-rules` 的 `runtime-diagnostics` 条件路由 或 `bug-root-cause-rules` 使用证据定位；诊断完成后必须交给 `implementation-review-rules` 检查清理状态。

## 权责边界与不负责事项

- 只负责临时诊断日志，不替代正式日志和 trace 设计。
- 不在没有明确假设时大面积撒日志。
- 不输出敏感信息、全量大对象或高频无界日志。
- 不允许以控制台打印替代项目日志框架。
- 调试日志属于调试改动，问题定位或修改完成后必须删除。
- 如果后续确实需要正式观测点，必须重新按正式日志规则单独设计，不能直接保留当前调试日志。
- 不把临时日志直接留在交付代码中而不说明去留。

## 需要暂停并确认的条件

- 当前没有明确观察目标，日志只是为了“看看会不会发现什么”。
- 当前计划通过控制台打印临时排查，而不是走项目 logger。
- 准备输出敏感信息、账号标识或高风险数据。
- 日志落点过多、粒度过细，明显会制造噪音或性能风险。
- 诊断结束后没有清理方案。
- 当前 Bug 还没有建立统一的 Bug 根目录，导致日志记录和断言记录可能再次分散。

## 执行通过 / 驳回标准

- 通过：能够说明为什么要加这些日志、放在哪里、预计观察什么、如何控制风险；临时日志使用项目 logger 而非控制台打印；相关记录统一落在当前 Bug 根目录下；问题定位或修改完成后这些调试日志已删除。
- 驳回：为了图方便随手加打印或直接使用控制台打印，没有明确目标、没有清理计划、没有统一 Bug 根目录记录，或日志量和敏感性失控。

## 执行结果归档要求

- 将日志方案、落点、观察目标、观察结果和清理状态统一记录到 `artifact-storage-rules` 约定的当前 Bug 根目录中。
- 当前 Bug 根目录必须包含 `README.md`，至少写明问题现象、验证假设、日志位置、输出摘要、定位结论和清理状态。
- Bug 根目录、入口 `README.md` 和同一 Bug 根目录复用策略统一遵循 `../artifact-storage-rules/references/path-map.yaml` 与 `../artifact-storage-rules/references/update-policy.md`。
- 如果同一 Bug 有多轮日志诊断和断言诊断，统一放在同一个 Bug 根目录下，不再分散记录到其他目录。
- 如果后续需要补正式观测点，应在删除当前调试日志后，另行按正式日志规则重新设计。
- 进入最终回复前，必须联动 `artifact-delivery-gate-rules`，核对日志方案、观察结果和清理状态是否已经真实写入当前 Bug 根目录；未落盘不得判定调试日志工作完成。

## references 读取规则

- 只要创建或修改 Bug 根目录 `README.md`，必须同时读取 `../artifact-delivery-gate-rules/references/plain-language-document-contract.md`，正文先写结论，技术细节保留在原有章节或附录。
- 如果本轮涉及审查、验收、功能验证、浏览器联调或第三方验证，必须同时读取 `../artifact-delivery-gate-rules/references/review-acceptance-gate-contract.md`，按适用性记录，不把不适用条件写成阻断。
- 默认先读 `../logging-trace-rules/references/backend-framework-and-config.md`。
- 再读 `bug-intake-rules/references/runtime-diagnostics-bug-debug-log-rules-debug-log-placement.md`。
- 在定位当前 Bug 根目录、入口 `README.md` 或判断是否继续复用同一根目录时，先读 `../artifact-storage-rules/references/path-map.yaml` 与 `../artifact-storage-rules/references/update-policy.md`。
- 只有在 确定日志删除和回收记录 时，再读 `bug-intake-rules/references/runtime-diagnostics-bug-debug-log-rules-debug-log-cleanup.md`。
- 只有在 对照样例或判断日志是否过量 时，再读 `bug-intake-rules/references/runtime-diagnostics-bug-debug-log-rules-debug-log-examples.md`。

## 迁移保留规则：bug-runtime-debug-rules

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
5. 若诊断需要启动服务、连接数据库 / 缓存 / 消息队列、调用 HTTP/RPC 上游或执行调试器，必须先确认全部连接目标来自 `test-strategy-rules` 的 local 本地配置；不得连接 test / prod / staging 等非 local 环境。

## 默认执行流程

1. 默认先读 `bug-intake-rules/references/runtime-diagnostics-bug-runtime-debug-rules-runtime-entry-conditions.md`，确认当前是否真的需要进入运行时诊断。
2. 再读 `../artifact-storage-rules/references/path-map.yaml` 与 `../artifact-storage-rules/references/update-policy.md`，确认 Bug 根目录、入口 `README.md` 和同一 Bug 持续复用同一根目录的策略。
3. 再读 `bug-intake-rules/references/runtime-diagnostics-bug-runtime-debug-rules-runtime-observation-methods.md`，选择断点、变量观察、debug 日志、断言等合适手段。
4. 如果需要判断何时结束或如何回流，再读 `bug-intake-rules/references/runtime-diagnostics-bug-runtime-debug-rules-runtime-exit-and-handoff.md`。
5. 输出本轮诊断目标、观察点、得到的运行时证据和下一步结论，并更新到当前 Bug 根目录下的 `README.md`。
6. 结束后要么回流到 `bug-root-cause-rules` 固化结论，要么直接进入 `bug-fix-proposal-rules`。

## 权责边界与不负责事项

- 只负责运行时诊断，不替代 `bug-root-cause-rules` 的静态定位职责。
- 不代替 `bug-intake-rules` 的 `runtime-diagnostics` 条件路由 讨论长期日志策略；这里的 debug 日志仅用于诊断。
- 不直接给出修复方案，那属于 `bug-fix-proposal-rules`。
- 不把断点、日志和断言长期残留在交付代码中。

## 需要暂停并确认的条件

- 当前问题其实还能继续静态收敛，不值得进入运行时调试。
- 运行时诊断需要修改风险较高的本地环境或行为，但尚未确认。
- 运行时诊断只能通过连接 test / prod / staging 数据库、缓存、消息队列、HTTP/RPC 上游或其他非 local 服务才能继续。
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
- 进入最终回复前，必须联动 `artifact-delivery-gate-rules`，核对运行时诊断目标、证据和结束结论是否已经真实写入当前 Bug 根目录；未落盘不得判定运行时诊断完成。

## references 读取规则

- 只要创建或修改 Bug 根目录 `README.md`，必须同时读取 `../artifact-delivery-gate-rules/references/plain-language-document-contract.md`，正文先写结论，技术细节保留在原有章节或附录。
- 如果本轮涉及审查、验收、功能验证、浏览器联调或第三方验证，必须同时读取 `../artifact-delivery-gate-rules/references/review-acceptance-gate-contract.md`，按适用性记录，不把不适用条件写成阻断。
- 默认先读 `bug-intake-rules/references/runtime-diagnostics-bug-runtime-debug-rules-runtime-entry-conditions.md`。
- 在定位当前 Bug 根目录、入口 `README.md` 或判断是否继续复用同一根目录时，先读 `../artifact-storage-rules/references/path-map.yaml` 与 `../artifact-storage-rules/references/update-policy.md`。
- 只有在选择诊断手段时，再读 `bug-intake-rules/references/runtime-diagnostics-bug-runtime-debug-rules-runtime-observation-methods.md`。
- 只有在判断结束条件和交接方式时，再读 `bug-intake-rules/references/runtime-diagnostics-bug-runtime-debug-rules-runtime-exit-and-handoff.md`。
