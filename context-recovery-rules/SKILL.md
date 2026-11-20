---
name: context-recovery-rules
description: 会话上下文准备与恢复的唯一 owner。`rule-bootstrap` / `memory-bootstrap` 路由：新会话第一轮默认触发，`AGENTS.md`、`CLAUDE.md`、`.gitattributes`、`.editorconfig` 或项目记忆四件套（`PROJECT_CURRENT.md`、`PROJECT_MEMORY.md`、`PROJECT_HISTORY.md`，`PROJECT_STYLE.md` 按需）任一缺失或受管章节未同步时幂等补齐，保留用户手写内容。`recent-context-bootstrap` 路由：新会话或上下文压缩后如需近期事实，从近 3 天 `doc/`、git 提交与项目文档补取。同时拥有规则文件与记忆文件的生成脚本。不负责代码风格记忆（归 `project-style-rules`）或跨项目知识沉淀（归 `knowledge-flow`）。
---

# 上下文准备与恢复

## 有损前提（最高优先级）

上下文压缩有损且时机不可预测；未落盘的计划、状态、决策、偏差和证据在压缩后一律视为已丢失。

- 磁盘是唯一可靠记忆：按执行顺序命名的任务计划文档、`doc/` 工程文档、项目记忆文件、知识库。会话上下文、聊天输出、思考过程、宿主 UI 任务列表都不是事实源。
- 写入纪律先于恢复纪律：每个状态变更点先写盘（节奏见 `../autonomous-execution-rules/references/state-persistence-and-task-granularity.md`），压缩恢复只是最后防线。
- 恢复只认磁盘：压缩摘要只作线索，数值、路径、命令、结论必须回读文件确认后才可引用，禁止凭记忆续做。

## 路由一：自举（`rule-bootstrap` / `memory-bootstrap`）

唯一入口 `scripts/bootstrap_agents.sh [--repo PATH] [--target default|claude|both]`，幂等创建或同步规则文件与记忆骨架，保护非受管内容。

- 规则文件按当前 AI 选择：Codex 用 `AGENTS.md`，Claude Code 用 `CLAUDE.md`；`--target both` 以 `AGENTS.md` 为唯一正文源。受管章节缺失时追加、已存在时原位更新，确切文字以脚本内 heredoc 为唯一权威源（索引 `references/规则文件模板/agents-md-sections-index.md`）。
- 子目录规则文件含独占一行 `<!-- bootstrap-agents:skip-managed-sections -->` 时跳过；根目录始终同步。`.gitattributes` / `.editorconfig` 缺失时创建最小版本，已存在不覆盖。
- 记忆文件只管存在性、结构与 UTF-8；容量上限与事实抽取归 `project-memory-rules`，风格归 `project-style-rules`。
- 必须真实执行脚本并逐文件输出新建 / 更新 / 跳过及原因；脚本失败、部分完成、覆盖非受管内容、`PROJECT_CURRENT.md` 超限均阻断。
- Godot 项目额外核对 `Godot 项目工具配置` 与 `图像生成配置`；凭据允许写入项目代码/配置/维护文档，禁止在过程性输出中回显原值。未装 `codegraph` 时安装并 `codegraph init`，失败回退不阻塞。

## 路由二：压缩恢复（`recovery`）

只在压缩已经发生后触发。按 `references/context-recovery-contract.md` 的固定顺序执行：重读规则文件 → `PROJECT_CURRENT.md` → `PROJECT_MEMORY.md`（`PROJECT_HISTORY.md` 默认不读）→ 恢复阶段、主域 Owner、必命中 skill、写集与最大推进边界 → 恢复编码许可（`confirmed` / `not-confirmed` / `unknown`，非 `confirmed` 禁止编码）→ 判定近期事实三态。

- 只有 `recent_context_state=missing` 才条件调用路由三；`sufficient` 直接继续，`uncertain` 先核验现有来源，不得把「发生压缩」等同于「必须预热」。恢复偏移按磁盘任务计划文档的状态字段与「下一动作」指针确认，文档缺失先补建落盘再继续。
- 存在未完成必需项时必须继续执行或输出显式中断点（已完成 + 剩余 + 下一动作 + 重入入口）。
- `Plan Mode` 不持久化执行期活动 projection，默认通过原生计划流程展示细化步骤；恢复期间禁止生成总结型收尾，恢复后继续由 `implementation-planning-rules` 生成原计划。
- 恢复完成后立即交还主域；用户明确停止时只形成最小收口。恢复中确认的事实由主域写回对应载体。细节见 `references/compression-playbook.md`、`references/trigger-signals.md`、`references/recovery-boundary.md`。

## 路由三：近期预热（`warmup`）

新会话缺少近期事实、或被路由二以 `missing` 调用时触发；扫描限近 3 天，按需读 skill frontmatter 建最小索引，`项目设计.md` 只作弱参考。输出来源、补齐项、仍缺项与交接点后立即让路，不因预热恢复或扩大任何授权。细节见 `references/bootstrap-sources.md`、`references/warmup-boundary.md`、`references/warmup-output-format.md`。
