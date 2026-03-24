---
name: team-development-rules
description: 按团队完整研发流程执行任务，涵盖中文优先协作、需求澄清、最小代码改动、编码规范、AGENTS.md 生成、Git 历史感知、测试、交付说明、方法时间戳安全检查和重复失败诊断。用于 Codex 在团队工程规则下生成、修改、调试、评审、测试或解释代码，或产出中文 AGENTS.md 及其他工程文档时触发。
---

# 团队研发规则

## 概览

在任何研发协作任务开始前，按这套规则统一沟通语言、澄清方式、代码实现、测试验证和交付说明。
根据任务类型按需读取对应参考文档，不要一次性加载所有细节。

## 执行流程

### 1. 建立上下文

- 技术沟通、需求讨论、代码评审、问题排查与交付说明默认使用中文。
- 若当前目录是 Git 仓库且具备读取历史的能力，至少读取当前分支最近一次提交记录，包括提交信息、修改文件和关键改动。
- 若用户要求生成 `AGENTS.md`，全文必须使用中文。

优先读取：

- `references/01-communication-and-clarification.md`
- `references/04-repo-and-delivery-rules.md`

### 2. 先澄清，再进入实现

- 在动手前先明确业务场景、输入输出、边界条件、技术栈和依赖约束。
- 若需求、BUG、边界、数据结构、接口契约或文档存在关键不明确项，立即暂停执行。
- 使用“待确认项 / 可选方案 / 推荐方案 / 确认后实施范围”的结构向用户确认。

必读：

- `references/01-communication-and-clarification.md`

### 3. 评估改动边界

- 优先复用已有组件、工具类、服务与项目约定。
- 优先新增代码来扩展功能，避免无必要的大范围重构。
- 若需要修改已有方法，先检查方法级注释中的“最近修改时间”。
- 当目标方法最近修改时间超过 7 天时，暂停修改，先给出修改必要性、风险评估、具体方案和验证方式，待用户确认后继续。

必读：

- `references/02-coding-and-change-rules.md`
- `references/05-method-change-guard.md`

### 4. 按规范实现

- 注释、文档和新增代码文件默认使用 UTF-8。
- 注释必须使用中文，重点解释“为什么这样做”；复杂代码块用 `1.`、`2.`、`3.` 标识步骤。
- 命名必须语义化；避免魔法值、硬编码配置、无意义缩写和明显冗余逻辑。
- 错误消息默认使用英文；日志优先使用中文，并体现模块、操作、对象或业务上下文。

必读：

- `references/02-coding-and-change-rules.md`

### 5. 完成后执行充分测试

- 完成需求开发后，必须执行完整且充分的测试。
- 若程序可以本地启动，优先执行端到端功能验证。
- 若程序暂时无法启动，构建贴合实际场景的测试用例、模拟数据和脚本，对核心逻辑做模拟执行验证。
- 所有测试资产统一存放在项目根目录 `test/` 下，并按 `yyyy-MM-DD HH:mm:ss + 需求中文简介` 创建子目录。

必读：

- `references/03-testing-and-validation.md`

### 6. 交付与复盘

- 交付说明必须包含改动原因、影响范围、风险点和验证方式。
- 如果逻辑不明确、需求存在缺口或规则冲突，必须先暂停并明确指出。
- 如果同一个问题连续尝试超过 5 次仍未解决，优先排查“修改的代码是否实际执行”或“当前实现架构是否不合适”。

优先读取：

- `references/03-testing-and-validation.md`
- `references/04-repo-and-delivery-rules.md`

## 参考文档选择

- 沟通、澄清、暂停确认：`references/01-communication-and-clarification.md`
- 编码规范、最小改动、注释、命名、错误与日志：`references/02-coding-and-change-rules.md`
- 测试执行、测试目录和验证要求：`references/03-testing-and-validation.md`
- Git、AGENTS.md、提交信息和交付说明：`references/04-repo-and-delivery-rules.md`
- 方法最近修改时间和 7 天保护规则：`references/05-method-change-guard.md`
