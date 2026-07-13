---
name: code-generation-style-rules
description: 当新增、修改、重构任意代码、脚本、测试支撑代码或配置型代码前自动触发。负责在正式写代码前读取 `PROJECT_STYLE.md`、当前文件与同目录样例，把项目长期风格记忆和局部既有写法收敛成本轮“代码风格契约”，约束命名、结构、注释、日志、错误处理、复用、排版和禁用写法；写完后执行风格闸门，并在形成新的稳定团队偏好时联动 `project-style-rules` 回写 `PROJECT_STYLE.md`。不替代 `project-style-rules` 的记忆维护职责，也不替代 `code-minimal-change-rules`、`code-readability-rules`、`code-style-consistency-rules`、`naming-rules` 或注释类 skill 的专业检查。
---

# 代码生成风格规则

## 核心目标

在每次生成、修改或重构代码前，把分散在项目长期风格、当前文件、同目录样例和已命中编码类 skill 中的规则，收敛成本轮可执行的“代码风格契约”。后续实现、补丁和测试代码都必须按该契约落地。

## 自动触发信号

- 新增业务代码、工具代码、脚本代码、测试支撑代码或配置型代码。
- 修改已有函数、类、组件、脚本、测试或配置型代码。
- 重构代码结构、拆分函数、抽取工具、迁移目录或调整接口实现。
- 用户要求“按项目风格写”“保持我们的代码风格”“补充代码风格规则”。
- `PROJECT_STYLE.md`、当前文件风格和通用编码 skill 之间可能存在优先级冲突。

## 进入后先做什么

1. 先读取用户本轮要求，确认本轮确实涉及代码生成、修改或重构。
2. 读取目标文件最新内容；目标文件不存在时读取同目录或同模块的相邻样例。
3. 读取根目录 `PROJECT_STYLE.md`，只采用状态为启用且与当前语言、目录、任务相关的条目。
4. 加载全局用户风格反例库 `code-style-consistency-rules/references/user-style-feedback-library.md` 中状态为 active 的条目，作为本轮必须规避的用户禁用写法。
5. 识别本轮已经命中的编码类 skill，例如 `code-minimal-change-rules`、`code-readability-rules`、`code-style-consistency-rules`、`naming-rules`、注释类 skill、日志或错误处理类 skill。
6. 按 [style-priority.md](references/style-priority.md) 决定冲突优先级。
7. 产出本轮“代码风格契约”，把 active 反例并入契约的“禁用写法”，再开始写代码。

## 默认执行流程

1. 默认先读 [pre-coding-checklist.md](references/pre-coding-checklist.md)，确认编码前需要读取的风格来源，其中包含全局用户风格反例库。
2. 再读 [style-priority.md](references/style-priority.md)，处理用户要求、当前文件、同目录、`PROJECT_STYLE.md` 与通用规则的冲突。
3. 按 [style-contract-template.md](references/style-contract-template.md) 组织本轮代码风格契约。
4. 写代码时把契约作为当前轮实现约束，不把契约当成可选建议。
5. 写完后读 [post-change-style-gate.md](references/post-change-style-gate.md)，逐项核对是否满足契约；若本轮代码命中全局反例库中任一 active 反例，驳回并按其正例改写。
6. 若本轮形成新的稳定团队偏好，联动 `project-style-rules` 回写 `PROJECT_STYLE.md`；若只是一次性局部跟随，不回写长期风格。

## 风格契约内容

本轮代码风格契约至少覆盖：

- 命名：变量、函数、类、接口、字段、文件和测试命名。
- 结构：函数长度、分支组织、参数模型、目录归属、复用边界。
- 注释：是否需要中文注释、函数头、步骤编号、字段注释、补丁说明。
- 日志：日志等级、字段、模板、脱敏和上下文信息。
- 错误处理：返回值、异常映射、兜底、重试、降级和用户可见错误。
- 复用：项目内 helper / util / 已装依赖 / 标准库优先级。
- 排版：缩进、空行、换行、导入顺序、局部声明写法。
- 禁用写法：本轮明确不能引入的抽象、模板化写法、过度防御或风格跳变；以及全局用户风格反例库中所有 active 反例对应的写法。

## 与相邻 Skill 的边界

- `project-style-rules` 维护 `PROJECT_STYLE.md`，负责长期风格记忆的抽取、合并、废弃和回写；本 skill 负责在写代码前应用这些风格记忆。
- `code-style-consistency-rules` 检查本次改动是否与本轮风格契约和局部既有写法一致，并作为全局用户风格反例库的唯一 owner；本 skill 先生成契约，并在写码前加载该库 active 反例纳入禁用写法。
- `code-minimal-change-rules` 控制改动范围；本 skill 不允许借风格统一扩大无关 diff。
- `code-readability-rules` 检查结构清晰度；本 skill 只提前声明本轮应遵守的结构风格。
- `naming-rules` 检查命名语义；本 skill 只把项目命名偏好纳入契约。
- 注释类 skill 决定注释内容、位置和完整性；本 skill 只把注释风格要求列入契约。

## 需要暂停并确认的条件

- 用户本轮明确要求的风格与当前文件稳定风格冲突，且会影响可维护性或接口兼容。
- 当前文件与同目录样例存在两套明显冲突风格，无法判断应跟随哪一套。
- 要满足风格契约必须扩大到无关文件或批量格式化。
- `PROJECT_STYLE.md` 中存在过时、冲突或不适用于当前语言的条目，且缺少更高优先级依据。

## 执行通过 / 驳回标准

- 通过：写代码前已读取相关风格来源并形成本轮代码风格契约；改动后与契约、当前文件和同目录样例一致；新的稳定偏好已联动 `project-style-rules` 回写或明确无需回写。
- 驳回：直接开始写代码而未形成契约；把 `PROJECT_STYLE.md` 当成唯一来源忽略当前文件；把个人偏好、外部模板或一次性口头建议写成项目风格；借风格统一扩大无关改动。

## references 读取规则

- 默认先读 [pre-coding-checklist.md](references/pre-coding-checklist.md)。
- 存在风格冲突或优先级判断时，读 [style-priority.md](references/style-priority.md)。
- 需要输出或内部整理风格契约时，读 [style-contract-template.md](references/style-contract-template.md)。
- 改动完成准备收口时，读 [post-change-style-gate.md](references/post-change-style-gate.md)。
- 写码前加载用户禁用写法时，读 `code-style-consistency-rules/references/user-style-feedback-library.md` 的 active 条目。
