---
name: project-local-skills-rules
description: 项目级 skill 自动沉淀与项目专属规则管理。任务收口时，若本轮涉及项目仓库写操作（代码/文档/配置修改）且产生可复用经验——如 5+ 次 tool call 的非平凡任务、踩坑后找到解法、用户纠正了方法、发现可复用多步骤 workflow——自动评估是否值得沉淀；用户明确要求"分析项目/总结项目专属 skill/沉淀项目规则"时同样触发。负责查重后以 project-项目名-主题-rules 命名写入项目根目录 skills/（luode-skills 仓库以仓库根为 skill 资产库），由项目级 AGENTS.md/CLAUDE.md 显式引用命中，不依赖任何工具专属路径；不代替 knowledge-flow 知识库笔记沉淀与 skill-absorption-rules 内部演进。
---

# 项目专属 Skill 沉淀规则

把项目写操作中产生的可复用经验沉淀成可被自动读取和命中的项目级 skill，目标是让项目内约定从口头经验变成 `project-<项目slug>-<topic>-rules/` 目录资产。

## Skill 作用与适用场景

- **通道 A（自动评估）**：任务收口时，本轮涉及项目仓库写操作且产生可复用经验 → 自动评估是否沉淀。
- **通道 B（主动点名）**：用户说"分析这个项目，并总结项目专属 skill"、"沉淀项目规则"、"给这个项目建立专属 skill" → 直接执行沉淀。
- **通道 C（阈值自动吸收）**：`memory-usage-tracking-rules` 判定项目记忆条目达到吸收阈值（`usage_count ≥ 3` 且跨 ≥ 2 个日期且 `absorbed_to` 为空）时，自动执行吸收为项目 skill，不设人工确认闸门。执行序列与回滚兜底见 `memory-usage-tracking-rules/references/absorption-trigger.md`。
- 支持的项目级规则沉淀场景：
  - 代码风格与提交前检查
  - 静态属性枚举使用约定
  - 字符串与数字转换工具包用法
  - 时间转换工具包用法
  - 协程 / 并发包用法
  - HTTP 客户端与服务端包用法
  - 接口编写与契约约定
  - 数据库查询规范
  - Mongo / Redis / 北极星配置等中间件约定
- 落点统一为**项目根目录 `skills/`**（如 `D:\某项目\skills\project-<slug>-<topic>-rules\`），跨工具通用；luode-skills 仓库特例：仓库根即 skill 资产库，`project-*` 直接落仓库根与既有 skill 平级。
- 命中方式：由项目级规则文件（`AGENTS.md` / `CLAUDE.md`）显式声明引用 `skills/` 目录，AI 按声明扫描命中；不依赖任何工具专属路径（如 `~/.workbuddy/skills/`）。

## 自动触发信号

- 任务收口时：本轮有项目写操作（代码/文档/配置/测试改动）且满足沉淀条件（见 `references/auto-trigger-and-evaluation.md`）。
- 用户明确要求"分析项目并总结项目 skill"、"把项目规则沉淀到 skill"、"给项目建立专属 skill"。
- 用户提供多个项目实践点，要求整理为可复用规则集合。
- 新项目接入时需要先建立项目私有编码规范入口。
- `memory-usage-tracking-rules` 的候选扫描输出命中吸收阈值的记忆条目（通道 C 自动吸收）。

## 进入后先做什么

1. 先确认当前是"项目专属 skill 沉淀"，不是单次代码实现；对照 `references/auto-trigger-and-evaluation.md` 的价值评估门槛，不满足则不沉淀。
2. 按 `references/dedup-and-update.md` 查重：`ls <项目根>/skills/ | grep '^project-'`（luode-skills 仓库用 `ls . | grep '^project-'`），比较 name + description 是否覆盖同一场景。
3. 扫描仓库中已有的项目约定来源：本轮改动的代码、文档、报错与解法、用户纠正点。
4. 按主题拆成多个小 skill（单一职责），避免大杂烩；命名 `project-<项目slug>-<topic>-rules`。
5. 每个子 skill 至少生成 `SKILL.md`，必要时补 `references/` 和 `agents/openai.yaml`（推荐用 `.system/skill-creator/scripts/init_skill.py` 创建）。
6. 输出清单时明确：新增/更新了哪些 skill、各自触发条件和核心职责。

## 默认执行流程

1. 默认先读 `references/scope-and-splitting.md`，确定拆分粒度。
2. 再读 `references/project-skill-template.md`，按统一模板产出每个子 skill（含踩坑经验与可直接复制的命令）。
3. 需要确定优先级时，再读 `references/priority-and-roadmap.md`。
4. 创建/更新落点：项目根 `skills/project-<slug>-<topic>-rules/`（luode-skills 仓库直接落仓库根）；创建用 skill-creator 的 `init_skill.py`（`<luode-skills 仓库>/.system/skill-creator/scripts/init_skill.py`，`--path` 指向项目根 `skills/`），更新直接改 SKILL.md；改后跑 `quick_validate.py` 校验。
5. 若发现与通用 skill 冲突，记录冲突点并转交 `skill-absorption-rules` 做体系侧回补。

## 权责边界与不负责事项

- 只负责"项目私有 skill 的沉淀与组织"，不直接替代需求、Bug、编码或测试主流程。
- 不负责修改系统级通用 skill 的规则正文（除非用户明确要求）。
- 不把项目专属经验直接写进全局 skill（无项目前缀），避免污染其他项目。
- 不把多个无关主题硬塞进一个项目 skill。
- 不代替 `knowledge-flow` 的知识库笔记沉淀（笔记 vs skill 资产分开）。
- 不负责已有 skill 执行中暴露 gap 的体系侧演进（那是 `skill-absorption-rules`）。

## 需要暂停并确认的条件

- 项目规则证据不足，无法稳定归纳触发条件。
- 用户想要的是"立即实现功能"，而不是先沉淀 skill。
- 规则主题过多且边界重叠，短时间内无法合理拆分。
- 查重发现与已有 skill 高度重叠，无法判断该补哪个。
- 通道 C（阈值自动吸收）例外：不设人工确认闸门，但查重无法判断归属、或新 skill 结构校验失败时，必须暂停并转人工。

## 执行通过 / 驳回标准

- 通过：项目专属规则被拆成多个可命中的 skill，并落在项目根 `skills/project-<slug>-<topic>-rules/`（luode-skills 仓库为仓库根）。
- 通过：每个 skill 都有清晰触发 description 和核心职责，不依赖口头补充。
- 通过：吸收经验包含踩坑记录与可直接复制的命令。
- 驳回：只给抽象清单，不落地到 skill 目录。
- 驳回：把项目专属内容直接塞进无项目前缀的全局 skill 导致跨项目污染。

## 执行结果归档要求

- 项目专属 skill 统一落地到项目根 `skills/project-<项目slug>-<topic>-rules/`（luode-skills 仓库为仓库根）。
- 子 skill 结构：`SKILL.md` + 按需 `references/`、`agents/`。
- 输出结果至少包含：
  - 新增/更新的项目专属 skill 列表
  - 每个 skill 的触发说明和职责
  - 后续建议补齐的主题清单
- 在 `references/source-notes.md` 登记本次创建/更新动作。

## references 读取规则

- 判断是否触发沉淀、评估价值时读 `references/auto-trigger-and-evaluation.md`。
- 决定落点、执行查重与创建/更新时读 `references/dedup-and-update.md`。
- 确定拆分粒度时读 `references/scope-and-splitting.md`。
- 实际新建子 skill 时读 `references/project-skill-template.md`。
- 需要排优先级时读 `references/priority-and-roadmap.md`。
- 吸收登记与来源回溯时读 `references/workbuddy-absorption-map.md`、`references/source-notes.md`。
