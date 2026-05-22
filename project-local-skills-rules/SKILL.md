---
name: project-local-skills-rules
description: 当用户要求“分析项目”并明确希望总结该项目专属编码规则/实践为 skill，或要求沉淀项目私有 skill 清单时自动触发。负责把项目专属能力拆成多个独立 skill 并统一写入项目根目录 `skill/`，用于后续上下文预热和编码阶段优先命中；不要用它代替通用体系 skill 的执行，也不要代替 `artifact-storage-rules` 的全局路径裁决。
---

# 项目专属 Skill 沉淀规则

只在“把某个项目的专属规范沉淀成可复用 skill”时使用这个 skill。
目标是让项目内约定从口头经验变成可被自动读取和命中的 `skill/` 目录资产。

## Skill 作用与适用场景

- 当用户说“分析这个项目，并总结项目专属 skill”时，统一输出到项目根目录 `skill/`。
- 把项目经验拆成多个独立 skill，而不是写成一份超长总文档。
- 支持项目级规则沉淀场景，例如：
  - 代码风格与提交前检查
  - 静态属性枚举使用约定
  - 字符串与数字转换工具包用法
  - 时间转换工具包用法
  - 协程 / 并发包用法
  - HTTP 客户端与服务端包用法
  - 接口编写与契约约定
  - 数据库查询规范
  - Mongo / Redis / 北极星配置等中间件约定
- 让 `recent-context-bootstrap-rules` 可以从 `skill/` 快速读取项目私有规则。

## 自动触发信号

- 用户明确提出“分析项目并总结项目 skill”。
- 用户要求“给这个项目建立专属 skill”。
- 用户要求“把项目规则沉淀到 `/skill` 目录”。
- 用户提供多个项目实践点，要求整理为可复用规则集合。
- 新项目接入时需要先建立项目私有编码规范入口。

## 进入后先做什么

1. 先确认当前任务是“项目专属 skill 沉淀”，不是单次代码实现。
2. 默认先读 `../artifact-storage-rules/references/path-map.yaml`，确认 `skill/` 目录规则。
3. 扫描仓库中已有的项目约定来源：代码、文档、最近提交、现有工具封装。
4. 按主题把规则拆成多个小 skill（单一职责），避免大杂烩。
5. 每个子 skill 至少生成 `SKILL.md`，必要时补 `references/` 和 `agents/openai.yaml`。
6. 输出清单时明确：新增了哪些 skill、各自触发条件和核心职责。

## 默认执行流程

1. 默认先读 `references/scope-and-splitting.md`，确定拆分粒度。
2. 再读 `references/project-skill-template.md`，按统一模板产出每个子 skill。
3. 需要确定优先级时，再读 `references/priority-and-roadmap.md`。
4. 在项目根目录创建或更新 `skill/` 下的子 skill 目录。
5. 若发现与通用 skill 冲突，记录冲突点并转交 `skill-evolution-rules` 做体系侧回补。

## 权责边界与不负责事项

- 只负责“项目私有 skill 的沉淀与组织”，不直接替代需求、Bug、编码或测试主流程。
- 不负责修改系统级通用 skill 的规则正文（除非用户明确要求）。
- 不把项目专属经验直接写进全局 skill，避免污染其他项目。
- 不把多个无关主题硬塞进一个项目 skill。

## 需要暂停并确认的条件

- 项目规则证据不足，无法稳定归纳触发条件。
- 用户想要的是“立即实现功能”，而不是先沉淀 skill。
- 规则主题过多且边界重叠，短时间内无法合理拆分。
- 项目根目录已有历史 `skill/` 规范但结构冲突严重。

## 执行通过 / 驳回标准

- 通过：项目专属规则被拆成多个可命中的 skill，并落在项目根目录 `skill/`。
- 通过：每个 skill 都有清晰触发 description 和核心职责，不依赖口头补充。
- 驳回：只给抽象清单，不落地到 `skill/`。
- 驳回：把项目专属内容直接塞进全局 skill 导致跨项目污染。

## 执行结果归档要求

- 项目专属 skill 统一落地到项目根目录 `skill/`。
- 子 skill 建议结构：`skill/<topic>/SKILL.md`，按需补 `references/`、`agents/`。
- 输出结果至少包含：
  - 新增/更新的项目专属 skill 列表
  - 每个 skill 的触发说明和职责
  - 后续建议补齐的主题清单

## references 读取规则

- 默认先读 `references/scope-and-splitting.md`。
- 只有在实际新建子 skill 时，再读 `references/project-skill-template.md`。
- 只有在需要排优先级时，再读 `references/priority-and-roadmap.md`。
