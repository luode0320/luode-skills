# 实现自审的共享证据与专属契约

## 用途

本文件是 `CYCLE-SS-05` 的条件路由落点：将该 owner 的共享证据、暂停、结论、归档与阻断细则从入口文件下沉到可按需读取的 reference。自动触发入口、触发 aliases、阶段职责、用户习惯、授权、安全、停止边界、输出和证据归档均保持有效；不得因下沉而省略任何原有检查。

## 使用顺序

1. 先由同目录 `SKILL.md` 依据原自动触发条件确认本 owner 的专属阶段。
2. 在读取证据、作出结论、归档或处理阻断前读取本文件。
3. 按本文件中的原有 references 路由读取细节；专属阶段职责仍以 `SKILL.md` 为准。
4. `code-review-automation-rules` 仍是提交级专责审查入口，不得因本文件的通用证据契约被合并、删除或替代。

## 保护语义

- 保留自动触发与原 `description`、trigger aliases；没有命中本 owner 的专属条件时不得误触发。
- 保留用户习惯、授权与停止边界、local 环境安全、输出协议、证据归档、回滚/重验和任务阻断规则。
- 本文件是 owner 内的引用化去重，不是删除 owner、合并阶段职责或用模型默认能力替代规则。

## 代码质量 Owner 结果消费契约

实现自审不再保存代码质量细则的第二份正文。遇到可读性、命名、注释、目录、公共工具、Go 风格、接口、数据库、错误处理、日志、时间或前端静态质量问题时，只消费对应 Owner 的 PASS/FAIL、finding、证据位置和阻断级别。完整规则来源必须回到唯一 Owner：

- 基础编码：`code-generation-style-rules`、`code-minimal-change-rules`、`code-readability-rules`、`code-style-consistency-rules`、`naming-rules`。
- 注释质量：`comment-placement-granularity-rules`、`comment-completion-gate-rules`、`chinese-comment-rules`。
- 结构与复用：目录、二级子目录、依赖方向和 500 行拆分消费 `package-structure-rules`；公共资格、复用检索、防重复封装和 7 天冻结消费 `common-util-rules`。
- 位点专项：接口、数据库、错误、日志、时间、前端、Go、Vue、React、Windows 编码、微业务和测试程序消费其各自 Owner 结果。

## 需要暂停并确认的条件

- 任一已命中 Owner 给出 P0/P1 finding，且修复会改变需求边界、接口契约、数据结构、目录边界或兼容策略。
- `package-structure-rules` 判断目录/依赖方向需要跨模块迁移，超出本轮最小改动范围。
- `common-util-rules` 命中 7 天冻结或已存在可复用实现，但替换调用路径、兼容方案或旧行为保留策略尚未确认。
- 注释、命名、结构或可读性 finding 已严重到需要回到编码阶段重做，而不是在审查阶段局部补丁。
- 本轮涉及后端 HTTP API、数据库 schema/query、前端路由或跨业务 contract，但对应 Owner 的来源或结果为 `limited`，继续审查只能猜测规则。

## 执行通过 / 驳回标准

- 通过：实现目标达成；已命中的代码质量 Owner 均有可追溯结果；P0/P1 finding 已修复或有明确不适用依据；P2/P3 finding 不影响当前放行边界且已记录为改进项；目录、公共工具、注释、接口、数据库和语言专项没有未处理的硬阻断。
- 驳回：存在未处理的 P0/P1 Owner finding；存在 `limited` Owner 但该 Owner 对当前放行判断必需；或实现自审自行复制/改写 Owner 规则正文并据此绕过唯一 Owner 结果。
- 降级项：通用可读性、命名、局部风格、轻量日志表达、P2/P3 注释颗粒度等问题，只有在实施计划或用户本轮明确冻结为放行条件时才作为硬阻断；否则记录为改进项并回到对应 Owner。

## 执行结果归档要求

- 将自审结论、驳回项和回改建议记录到 `doc/6-审查/`。
- 实现自审文件名必须使用 `YYYY-MM-DD_HHmmss_<来源对象标识>_<审查中文主题>.md`；来源对象标识可以来自需求或 Bug，禁止使用 `YYYY-MM-DD_<审查中文主题>.md` 或缺少来源标识的 `YYYY-MM-DD_HHmmss_<审查中文主题>.md`。
- 归档内容至少包含检查范围、通过项、未通过项和受影响运行路径清单；仅当存在未通过项、阻断风险或用户明确要求建议时，补写必要后续动作。
- 无论是否为轻量实现、是否存在争议、是否全部通过，只要本轮已执行实现自审，就必须完成审查文档落盘；禁止仅在最终回复中口头保留通过结论而不写入 `doc/6-审查/`。
- 进入最终回复前，必须联动 `artifact-delivery-gate-rules` 核对本轮审查文档是否已经真实落到 `doc/6-审查/`，未落盘不得判定实现自审完成。
- 审查文档必须包含统一判定字段：`审查结论: 通过/阻断`、`审查范围: <文件列表或等价范围说明>`、`是否允许提交: 是/否`、`阻断问题: <P0/P1 摘要，没有则写无>`；字段缺失不得判定自审完成。
- 审查结论为“阻断”时，必须读取并在同一审查文档写入 `../artifact-delivery-gate-rules/references/task-blocker-closure-contract.md` 的完整“任务阻断收口”；解决计划需包含回改责任方、完成判据和复审入口。若同根因已有 `BLK-*`，引用该记录而不重复编写计划。

## references 读取规则

- 默认先读 `references/review-scope.md`。
- 只有在判断与相邻审查 skill 的边界时，再读 `references/review-boundaries.md`。
- 只有在需要检查基础格式与清理项时，再读 `references/format-cleanup-checks.md`。
- 只有在需要检查语法、类型、引用与构建风险时，再读 `references/syntax-and-reference-checks.md`。
- 只有在需要检查目录归位、职责对位与依赖方向时，再读 `references/placement-and-dependency-checks.md`。
- 只有在需要正反例时，再读 `references/review-examples.md`。
- 输出实现审查文档前，必须读取 `../artifact-delivery-gate-rules/references/plain-language-document-contract.md`；正文先说明是否可继续，检查清单、文件位置和证据进入附录。
- 涉及审查适用性、第三方响应或专项环境时，必须同时读取 `../artifact-delivery-gate-rules/references/review-acceptance-gate-contract.md`，按门禁记录区分可继续、受限交接和正式放行。
- 审查结论为“阻断”时，必须读取 `../artifact-delivery-gate-rules/references/task-blocker-closure-contract.md`，不得以 P2/P3、`limited` 或 `not_applicable` 误建 `BLK-*` 记录。
