# 项目长期记忆

## 核心记忆

### 仓库定位
- 别名: skill 仓库, 团队研发协作规则仓库
- 类型: 项目事实
- 定义: 本仓库用于沉淀面向团队研发协作的 Skill、references、脚本和入口文档，目标是让 AI 在需求、Bug、编码、审查、测试、交付流程中按任务内容自动命中规则。
- 来源: `README.md`、`项目设计.md`
- 适用范围: 全仓库
- 更新时间: 2026-06-27
- 状态: 启用

### 根目录主入口
- 别名: 仓库入口文档
- 类型: 文档入口
- 定义: 仓库根目录长期主入口文档包括 `README.md`、`编码skill.md`、`字典.md`、`项目设计.md`、`PROJECT_MEMORY.md`、`PROJECT_STYLE.md`。
- 来源: 根目录真实文件结构
- 适用范围: 全仓库
- 更新时间: 2026-06-27
- 状态: 启用

### 研发产物目录正式口径
- 别名: doc 顶层目录规则
- 类型: 目录规则
- 定义: 正式研发产物目录统一收口到 `doc/` 下；当前正式顶层子目录为 `doc/需求/`、`doc/架构/`、`doc/阶段/`、`doc/审查/`、`doc/bugs/`、`doc/tests/`。
- 来源: `artifact-storage-rules/references/path-map.yaml`
- 适用范围: 文档归档与规则引用
- 更新时间: 2026-06-27
- 状态: 启用

### 需求主动侦察链路
- 别名: 老板式 idea 转需求, idea 侦察, 需求 discovery
- 类型: 流程规则
- 定义: 当用户只提出一句话 idea、粗略想法或老板式方向时，优先由 `requirement-discovery-rules` 主动侦察当前项目代码、文档、数据库线索、上下游服务、第三方调用、用户补充路径或 URL，形成有证据来源的需求设计；已验证可复用的资料位置、数据库、URL、项目路径和侦察经验必须继续通过 `project-memory-rules` 回写长期记忆。
- 来源: 对话确认、`requirement-discovery-rules`
- 适用范围: 需求域
- 更新时间: 2026-06-27
- 状态: 启用

### 需求域第一入口
- 别名: 需求 skill 顺序, 需求前置入口
- 类型: 流程规则
- 定义: 需求域默认以 `requirement-discovery-rules` 为第一入口；`requirement-intake-rules` 负责把 discovery 或用户资料收口为需求主文档，`requirement-gap-rules` 只处理主动侦察后仍无法补齐的关键缺口。当前不把需求域 skill 合并成一个大 skill，而是通过 `requirement-discovery-rules/references/requirement-domain-routing.md` 维护相邻 skill 的顺序、让路和重叠边界。
- 来源: `requirement-discovery-rules/references/requirement-domain-routing.md`、`编码skill.md`
- 适用范围: 需求域
- 更新时间: 2026-06-27
- 状态: 启用

### 审查体系收口
- 别名: 审查链路
- 类型: 流程规则
- 定义: 默认审查链收口为 `implementation-review-rules`、`project-change-review-rules`、`skill-compliance-gate-rules`；其中 `code-review-automation-rules` 仅用于按当前分支提交范围做专项审查，不纳入默认自动审查链。
- 来源: `README.md`、`项目设计.md`
- 适用范围: 审查域
- 更新时间: 2026-06-27
- 状态: 启用

### 记忆与风格更新方式
- 别名: 长期规则回写方式
- 类型: 维护规则
- 定义: 当用户后续调整某个指标、命名、目录口径或风格偏好时，必须更新原有记忆或风格词条，不新增同义冲突条目，也不保留并行旧口径。
- 来源: 对话确认、`project-memory-rules`、`project-style-rules`
- 适用范围: 长期文档维护
- 更新时间: 2026-06-27
- 状态: 启用

## 术语表

### doc 顶层混合命名
- 别名: 中文语义优先命名
- 类型: 术语
- 定义: `doc/` 根目录保留英文，顶层子目录采用“中文语义优先 + 工程通用域保留英文”的混合方案：`需求`、`架构`、`阶段`、`审查`、`bugs`、`tests`。
- 来源: 对话确认、`artifact-storage-rules`
- 适用范围: 文档目录命名
- 更新时间: 2026-06-27
- 状态: 启用

## 业务约束

### 旧目录处理规则
- 别名: 不保留兼容层
- 类型: 迁移约束
- 定义: 当目录迁移完成且用户未要求保留兼容入口时，应删除旧目录、旧占位文件和旧跳转文档，不保留并行旧包或兼容壳。
- 来源: 对话确认、`artifact-storage-rules`
- 适用范围: 目录迁移与收口
- 更新时间: 2026-06-27
- 状态: 启用

## 变更记录

- 2026-06-27：初始化根目录长期记忆文档，补齐 doc 顶层目录口径、审查链收口和长期规则回写约束。
- 2026-06-27：新增需求主动侦察链路，明确老板式 idea 先由 agent 查项目、数据、代码、上下游和补充路径，再形成需求设计并回写可复用侦察线索。
- 2026-06-27：明确 `requirement-discovery-rules` 是需求域第一入口，现有需求 skill 暂不合并为大 skill，改为通过路由 reference 收敛职责重叠。
