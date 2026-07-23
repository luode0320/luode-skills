---
name: implementation-review-rules
description: 【强制自动触发】当功能代码已经完成、准备进入测试前验证时触发。作为唯一自动测试前实现闸门，统一检查 4 组内容：实现质量、格式清理、语法/类型/引用、目录归位/分层边界。负责检查实现是否符合可读性优先、单一职责、命名语义化、注释完整、错误处理明确、日志可追溯、依赖使用审慎、魔法值治理、冗余逻辑清理和编码规范等实现质量要求，并在功能不变前提下检查最近改动代码是否还存在可直接收口的表达层冗余；必须核验本轮改动是否完成 `comment-placement-granularity-rules` 与 `comment-completion-gate-rules` 的改动位点注释检查与补齐；必须完成基础格式、语法/类型/引用、目录归位与依赖方向的测试前收口；必须识别 500 行及以上且持续膨胀的文件并要求拆分或给出拆分方案；必须检查“可复用公共工具是否被重复封装”并拦截重复造轮子；必须检查“最近修改超过7天的高复用通用代码是否被直接修改旧行为”，命中时要求改为新增兼容路径；Go 场景下还需在实现自审阶段扫描 `doc/5-tests/` 外 `*_test.go` 禁放问题，以及本轮改动是否把业务实现直接落在 `internal/service/*.go` 根目录文件，是否把请求/响应/第三方结果结构体散落在 `internal/service` 实现文件，是否在函数/方法内使用 `var (...)` 分组声明局部变量，是否把多参数函数签名直接写成多行参数列表，是否把第三方 API 响应长期用 `map[string]any` + key 硬编码解析；若本轮改动涉及后端 HTTP API，还必须检查 Swagger/OpenAPI 是否同步更新；默认优先并行；不要用它代替功能验证规则。
---


# 实现自审规则

只在“代码已经写完，但还没进测试，需要先做一轮测试前实现收口”时使用这个 skill。
如果当前问题是功能是否正确，请转交测试域。

## Skill 作用与适用场景

- 保持功能代码、Bug 修复代码或重构代码完成后的唯一自动测试前实现闸门。
- 主入口只编排实现质量、格式清理、语法/类型/引用、目录归位/依赖方向四组检查，不在入口复制语言专项、命令或注释字段细则。
- 实现质量与语言专项由 `references/review-scope.md` 承接；格式、语法/引用、目录/依赖分别由对应 reference 承接。
- 注释链只核验 `comment-completion-gate-rules` 的 PASS/FAIL；该结果必须能证明已按其边界联动 `comment-placement-granularity-rules`，本入口不复述任何注释字段、编号或清单细则。
- 实现自审只证明“具备进入测试的最低条件”，不得替代 `functional-validation-rules` 或把静态检查表述为功能可用。

## 自动触发信号

- 功能代码、Bug 修复代码或重构代码刚完成，准备进入测试、联调或回归验证。
- 需要确认当前实现是否达到可交给测试域的最低质量，或正式代码评审前需要作者自审。
- Go 改动涉及测试落点、服务目录、请求/响应/第三方结果结构体、局部变量声明、多参数函数签名或第三方响应解析。
- 后端 HTTP API 已新增或修改，需要核验 Swagger/OpenAPI 同步状态。
- 改动代码尚未完成注释链 PASS/FAIL、500 行持续膨胀、公共工具复用、7 天高复用代码兼容性或基础格式收口检查。
- 默认优先评估并行；是否真实并行由 `parallel-task-dispatch-rules` 统一裁决。

## 进入后先做什么

1. 冻结本轮实现目标、改动范围和用户手改基线；目标未收敛或上下文冲突时先停止审查并转对应 owner。
2. 读取 `references/review-scope.md`，检查最小改动、可读性、结构、命名、错误、日志、复用、文件膨胀、7 天兼容规则和语言专项。
3. 核验 `comment-completion-gate-rules` 的 PASS/FAIL 及其必要联动证据；FAIL 或无证据时不进入测试，本入口不重复检查注释字段细则。
4. 按需依次读取 `references/format-cleanup-checks.md`、`references/syntax-and-reference-checks.md`、`references/placement-and-dependency-checks.md`，完成四组测试前检查。
5. 涉及 HTTP API 时核验 `api-swagger-rules` 的同步结论；涉及用户手改冲突时核验 `code-context-resync-rules` 已完成且未回退用户内容。
6. 读取 `references/shared-evidence-and-specialized-contracts.md`，应用暂停、通过/驳回、归档、阻断和降级契约。
7. 输出受影响运行路径及其验证状态；没有真实运行证据时必须标记“仅静态验证”或“待真实运行验证”。

## 核心自审要求

- **实现质量与语言专项**：以 `references/review-scope.md` 为唯一细则来源，包含可读性、职责、命名、错误、日志、依赖、魔法值、冗余、500 行文件、公共工具复用、7 天兼容保护和 Go 专项。
- **分级口径**：硬阻断与默认自查以 `references/shared-evidence-and-specialized-contracts.md` 为唯一来源；默认自查项只有在实施计划冻结为放行项或用户本轮明确要求时才升级为硬阻断。
- **格式与清理**：以 `references/format-cleanup-checks.md` 为唯一细则来源。
- **语法、类型与引用**：以 `references/syntax-and-reference-checks.md` 为唯一细则来源；构建或静态检查失败不得进入测试。
- **目录、职责与依赖方向**：以 `references/placement-and-dependency-checks.md` 为唯一细则来源。
- **注释完成状态**：只消费 `comment-completion-gate-rules` 的 PASS/FAIL 和可追溯证据，不复制其字段、顺序、编号或清单定义。
- **真实验证降级**：实现自审不证明功能正确；只完成 build、lint、静态搜索或人工阅读时，结论必须保留静态验证边界。
- **用户手改保护**：发现磁盘内容与已读上下文不一致时，停止使用旧上下文，先执行 `code-context-resync-rules`，不得覆盖或回退用户手改。

## 默认执行流程

1. 确认触发阶段、改动范围和用户手改基线。
2. 按 review-scope → format → syntax/reference → placement/dependency 的顺序执行并收集证据。
3. 核验 comment-completion PASS/FAIL、Swagger/OpenAPI 适用状态和受影响运行路径。
4. 汇总通过项、驳回项、风险项与验证降级状态；任一必需组缺失时不得进入测试。
5. 需要范围边界或正反例时读取 `references/review-boundaries.md`、`references/review-examples.md`。
6. 按 `references/shared-evidence-and-specialized-contracts.md` 完成审查归档和阻断去重；P2/P3、`limited`、`not_applicable` 不升级为真实阻断。

## 权责边界与不负责事项

- 负责唯一测试前实现收口，不替代 formatter、lint、typecheck、构建或功能测试命令本身。
- 不负责需求裁决、功能正确性验证或最近改动范围之外的历史清理。
- 不代替语言、Swagger、注释、用户手改保护等 owner 定义细则；只消费其结论和证据。
- 不允许以赶进度为由放过重复造轮子、目录越层、500 行持续膨胀或 7 天高复用旧行为直接修改。

## 共享证据和专属契约

- 本入口仍是功能代码完成、测试前的唯一自动实现审查闸门；引用化不得削弱自动触发、阶段顺序、暂停、阻断、归档或真实验证降级。
- 开始收口、输出审查结论、归档证据或声明阻断前，必须读取 `references/shared-evidence-and-specialized-contracts.md`。
- 共享 reference 只提供证据与阶段契约；四组检查和专属 owner 结论仍必须真实执行。

## references 读取规则

- 默认先读 `references/shared-evidence-and-specialized-contracts.md` 与 `references/review-scope.md`。
- 按适用性读取格式、语法/引用、目录/依赖、边界和正反例 references；不得把“已引用”当成“已执行”。
