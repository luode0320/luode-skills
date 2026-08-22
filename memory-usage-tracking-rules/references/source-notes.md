# 来源记录（source-notes）

本文件登记 `memory-usage-tracking-rules` 的创建与调整来源，供追溯。吸收动作本身的裁决与落点登记在 `project-local-skills-rules` / `skill-absorption-rules` 各自的 `workbuddy-absorption-map.md` 与 `source-notes.md`，本文件只登记计数/吸收机制侧的来源。

## 创建记录

- 日期：2026-08-22
- 来源：内部升级（用户提出）
  - 需求：给 `PROJECT_MEMORY.md` / `PROJECT_STYLE.md` / `PROJECT_HISTORY.md` 记忆条目增加"使用次数"统计；后续把使用次数多的条目吸收为项目本地 skill 固定下来，让吸收规则获得量化输入。
  - 用户确认的决策：
    - 计数字段：参考 MEMORY 的机器索引区，三文件统一加机器索引区计数锚点。
    - 计数时机：仅实际引用时 +1（会话启动全文读取不计）。
    - 吸收触发：达阈值自动吸收（不设人工确认闸门）。
    - 落地范围：规则 + 模板 + 脚本。
- 关联资产：
  - 新 skill：`memory-usage-tracking-rules/`（SKILL.md + references × 4 + agents + scripts × 2）
  - 关联规则：`project-memory-rules`（usage_tracking 键）、`project-style-rules`（计数锚点区）、`project-rule-file-bootstrap-rules`（bootstrap 骨架）、`project-local-skills-rules`（通道 C）、`skill-absorption-rules`（自动吸收调和）
  - 注册表：`skill-hit-check-rules/references/deferred-gate-registry.md`
  - 仓库级：`AGENTS.md` 强制条款
  - 记忆文件：`PROJECT_MEMORY.md` / `PROJECT_STYLE.md` / `PROJECT_HISTORY.md` 计数锚点骨架

## 调整记录

- 2026-08-22：**修正生效范围表述**——机制为**全局通用**，适用于所有使用项目记忆四件套的项目，不限于 luode-skills 仓库（用户纠正：任何项目都要使用，不是单个项目）。同步修正：SKILL.md description / git 可回滚条款 / 吸收落点（`project-*` 为用户级全局 skill，对所有项目生效）、agents/openai.yaml、"仓库目录名"改为"项目目录名"。新项目由 bootstrap_agents.sh 自举时创建计数锚点，存量项目由收口闸门检测缺失锚点提示回补。
- 2026-08-22：**落点回归项目根 skills/**——用户纠正并 git 历史证实：`project-local-skills-rules` 初版（91357e8）落点就是**项目根 `skill/`**，2b0b251 吸收 skill-autosave 时被"路径适配 WorkBuddy 环境"改为用户级 `~/.workbuddy/skills/`；`artifact-storage-rules/references/path-map.yaml` 的 `project_local_skills` 一直是 `skill` 未改，两条规则长期矛盾。本次统一回归：落点为**项目根目录 `skills/`**（复数，用户拍板），命中由项目级 `AGENTS.md`/`CLAUDE.md` 显式引用；luode-skills 仓库特例直接落仓库根（仓库根即 skill 资产库）。同步修正：SKILL.md 查重命令与吸收落点、absorption-trigger.md 查重与落点、scan_absorption_candidates.py（docstring / existing_project_skills 主扫项目根 skills/ + 兼容用户级防重复 / dedup_hint）、project-local-skills-rules 全部落点、artifact-storage-rules（path-map `skill`→`skills` 两处 + SKILL.md/references）。
- 2026-08-22：**补齐规则 md 同步链路（bootstrap 受管章节）**——用户指出"计数+吸收规则要同步到规则 md 与同步脚本才能稳定触发"。核查发现 `bootstrap_agents.sh` 三处断点并修复：① `$BODY_SKILL_AUTO` 缺"### 记忆使用次数计数（强制）"子节（sync_section 对已存在 `##` 章节整体替换，luode-skills 跑 bootstrap 会把 AGENTS.md 手工子节删掉）；② `PROJECT_HISTORY_TEMPLATE` 缺 `## 计数锚点区`；③ `create_project_memory_file` 新建模板缺 `usage_tracking` 键（端到端测试抓到）。同步补齐 `CLAUDE.md` 计数条款与四件套模板 HISTORY 段标题统一。端到端验证：临时项目跑 bootstrap → AGENTS.md 含计数条款、HISTORY 含计数锚点区、MEMORY 含 usage_tracking，重跑幂等不重复。改动停在已改动未提交。
