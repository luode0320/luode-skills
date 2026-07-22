---
name: bug-intake-rules
description: 当用户描述报错、异常行为、结果不符、线上问题、偶发问题、接口异常、页面异常、数据错误或性能异常时触发；当用户只有一句话 Bug、截图中的异常、现象不清或 Bug 信息缺少复现/环境/输入/日志/影响范围时，自动进入 `discovery-and-gap` 条件路由；当静态定位不足且需要状态不变量、诊断断言、快速失败、临时 debug 日志、关键分支日志、上下游输入输出日志或运行时观察时，自动进入 `runtime-diagnostics` 条件路由。负责建立统一 Bug 根目录，并作为 Bug 侦察、缺口与运行时诊断的唯一入口 owner；严格保留 local 配置、只读侦察、禁止污染生产代码、可回收临时诊断资产和证据归档边界。不要用它代替复现、最终静态根因定位、修复方案、回归风险或修复后验证。
---

# Bug 问题录入规则

只在把问题“说清楚、记完整、可继续定位”时使用这个 skill。
如果当前已经进入代码定位、断点调试或修复方案讨论，请转交 Bug 域后续 skill。

## Skill 作用与适用场景

- 把混乱的 Bug 描述整理成可定位的问题记录。
- 为当前 Bug 建立统一的 Bug 根目录记录入口。
- Bug 根目录落地时，流程图与时序图必须用 Mermaid 语法直接写入 `README.md` 正文，不另建独立 SVG 等图文件，与需求域"正文内嵌 Mermaid 图示"的约定保持一致。
- 明确异常现象、影响范围、环境条件、期望结果和实际结果。
- 补齐最基础的定位入口信息，避免一开始就凭感觉读代码。
- 区分“信息不足”与“已经可以进入定位”的状态。

## 自动触发信号

- 用户说“报错了”“不对”“有异常”“线上挂了”“偶发失败”。
- 页面行为、接口返回、数据状态或性能表现明显异常。
- 问题描述里混杂了主观判断、猜测结论和零散日志。
- 需要把问题统一整理成可复现、可定位的 Bug 入口。
- 需要先为后续 Bug 链路创建统一的 Bug 根目录，具体命名模板以 `artifact-storage-rules` 为准。

## 进入后先做什么

1. 先抽取异常现象，不要先猜根因。
2. 为当前 Bug 确认或创建统一的根目录，具体路径、目录名和入口文件统一遵循 `artifact-storage-rules`。
3. 同步按 `artifact-storage-rules` 约定在 `README.md` 正文内嵌 Mermaid 流程图与 Mermaid 时序图，不另建 `flow.svg`/`sequence.svg` 等独立图文件。
4. 再整理影响范围、出现环境、触发条件和出现频率。
5. 区分期望结果与实际结果。
6. 判断当前信息是否已经足够进入复现和定位。

## 默认执行流程

1. 默认先读 `references/bug-description-template.md`，按统一模板整理问题。
2. 如果需要检查哪些基础信息是必填，再读 `references/minimum-intake-fields.md`。
3. 如果需要判断某类描述是否合格，再读 `references/intake-examples.md` 对照正反例。
4. 输出标准化 Bug 描述和缺失信息清单；只有信息不足、仍需复现/定位或用户明确要求建议时，才输出必要后续动作。
5. 在基础信息不足时，优先转 `bug-intake-rules` 的 `discovery-and-gap` 条件路由主动侦察（看代码、查日志、只读连本地库比数据、读截图），能自己查到的不直接追问用户；侦察后仍解不开再进入 `discovery-and-gap` 条件路由的缺口阻断，不直接进入根因定位。

## 权责边界与不负责事项

- 只负责把问题入口整理清楚，不负责分析根因。
- 是否需要进入断言、临时日志或运行时观察，由本 owner 的 `runtime-diagnostics` 条件路由判断。
- 不负责形成修改建议，那属于 `bug-fix-proposal-rules`。
- 不把“用户的猜测原因”直接当成正式结论。

## 需要暂停并确认的条件

- 连异常现象本身都描述不清。
- 连期望结果和实际结果都无法区分。
- 连出现环境、影响范围或触发条件都完全未知。
- 问题描述里只有结论，没有现象和证据。

## 执行通过 / 驳回标准

- 通过：能够形成结构化问题描述，至少说明现象、范围、环境、期望、实际和缺失项。
- 驳回：仍停留在“感觉有问题”“大概不对”“应该是这里坏了”这类无法接力的描述层。

## 执行结果归档要求

- 将标准化后的 Bug 入口信息统一记录到 `artifact-storage-rules` 约定的当前 Bug 根目录中。
- 当前 Bug 根目录必须包含 `README.md`，至少写明现象、影响范围、环境条件、期望结果、实际结果和缺失项；仅当仍未达到可复现/可定位条件时，补写必要后续动作。
- 当前 Bug 根目录的 `README.md` 正文必须同时包含 Mermaid 流程图与 Mermaid 时序图；缺任一图视为 Bug 入口记录不完整。
- 如果只是轻量问题且后续马上进入复现，可以简化记录，但仍应继续沿用同一个 Bug 根目录。
- 进入最终回复前，必须联动 `artifact-delivery-gate-rules` 核对当前 Bug 根目录、`README.md` 及其正文内嵌的 Mermaid 流程图与时序图是否已经真实落盘；未落盘不得判定 Bug 入口记录完成。

## 条件路由：discovery-and-gap

当用户仅给出一句话 Bug、截图中的异常、现象不清，或缺少复现条件、环境、输入、日志、影响范围和时间线时，唯一进入 `bug-intake-rules` 的 `discovery-and-gap` 路由。先主动查看代码、调用链、已有日志/trace、配置和截图；如需数据对比，只能使用 local 配置做只读查询，禁止增删改，无法自行取得的关键信息才一次推进一个真实问题向用户确认。

读取 `references/discovery-and-gap.md` 及其命名空间资源，形成证据、根因候选、缺口分级、Bug 根目录记录和明确 handoff；该路由不直接替代复现、根因定位或修复建议。

自动触发别名：`一句话 Bug`、`截图中的异常`、`现象不清`、`缺少复现条件`、`缺少环境信息`、`缺少输入数据`。

## 条件路由：runtime-diagnostics

当静态定位不足、需要观察状态变化、时序、输入输出、调用栈或关键分支时，唯一进入 `bug-intake-rules` 的 `runtime-diagnostics` 路由。路由选择最小必要的诊断断言、可回收临时 debug 日志或运行时观察；全部连接只能来自 local 配置，临时诊断资产必须记录、清理并回流到当前 Bug 根目录。

读取 `references/runtime-diagnostics.md` 及其命名空间资源，明确进入条件、观察假设、退出条件、收缩结论与后续流转；不得把临时断言、临时日志或断点残留为正式业务逻辑。

自动触发别名：`状态不变量`、`诊断断言`、`快速失败`、`临时 debug 日志`、`关键分支日志`、`上下游输入输出日志`、`断点调试`、`单步观察`、`调用栈观察`。

## references 读取规则

- 默认先读 `references/bug-description-template.md`；命中 `discovery-and-gap` 或 `runtime-diagnostics` 时追加读取对应条件路由 reference。
- 在决定 Bug 根目录、入口文件和同 Bug 复用策略时，先读 `../artifact-storage-rules/references/path-map.yaml` 与 `../artifact-storage-rules/references/update-policy.md`。
- 只有在检查基础字段是否齐全时，再读 `references/minimum-intake-fields.md`。
- 只有在对照好坏描述样例时，再读 `references/intake-examples.md`。
- 输出 Bug 入口文档前，必须读取 `../artifact-delivery-gate-rules/references/plain-language-document-contract.md`；正文先写现象、影响和期望，环境、日志、复现数据和证据进入附录。
- 若 Bug 需要审查、验收、浏览器联调或第三方验证，必须同时读取 `../artifact-delivery-gate-rules/references/review-acceptance-gate-contract.md`。
