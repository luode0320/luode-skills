# Bug 条件路由：discovery-and-gap

> 归属 owner：`bug-intake-rules`。本文件仅在 intake 完成现象标准化后，决定“信息缺口是否能先通过只读侦察补齐”；它不是独立 Skill，也不重复公共安全规则。

## 进入条件

- 用户只提供一句现象、截图、少量报错或日志，尚不足以组织稳定复现。
- 怀疑代码逻辑或数据状态异常，但可从代码、现有日志、trace、配置或 local 只读数据中主动补证。
- 在向用户追问前，先判断缺失信息是否能由主动侦察取得。

## 路由与产物

1. 先阅读 [公共契约](bug-lifecycle-common-contract.md)，确认只使用 local 配置、只读侦察、同一份 Bug 主文档归档与停止边界。
2. 按 [侦察清单](discovery-and-gap-bug-discovery-rules-discovery-checklist.md) 收集可验证事实；数据证据按 [只读取证规则](discovery-and-gap-bug-discovery-rules-evidence-and-db-readonly.md) 执行。
3. 用 [领域路由](discovery-and-gap-bug-discovery-rules-bug-domain-routing.md) 决定交给复现、根因、运行时诊断或用户补充；输出采用 [结论模板](bug-discovery-output-template.md)。
4. 只有主动侦察后仍缺少不可替代信息时，才使用 [缺口信号](discovery-and-gap-bug-gap-rules-blocking-signals.md) 和 [缺口清单](discovery-and-gap-bug-gap-rules-gap-checklist.md) 向用户提出最小问题。

## 必须保持的边界

- 证据不足时写为假设，不得把截图、可疑代码或数据猜测当作根因。
- 禁止连接 test、staging、pre、release、prod 或 production 配置；禁止写数据、无目标调试或以修复名义掩盖证据缺口。
- 静态证据不足且必须观察运行时状态时，转入 `runtime-diagnostics`；正式复现、根因裁决、修复建议和关闭验证分别留给其生命周期入口。
- 旧能力是否回归由 `test-regression-rules` 判断；修复是否可关闭由 `bug-validation-rules` 判断。
