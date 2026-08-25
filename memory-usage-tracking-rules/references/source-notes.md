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
- 2026-08-25：**规则 md 同步链路第二轮：从「有没有写」到「读不读得出来」**——内部调整通道，来源是某存量项目首次启用计数锚点时暴露的真实缺陷（该项目 `PROJECT_MEMORY.md` 机器索引区 yaml **长期整块解析失败**，16 个实体一个读不到，而扫描仍返回 `candidates: []` 且退出码 0）。上一轮（8/22）修的是"章节/键有没有被写进去"，本轮修的是"写出来的内容是否合法、读取侧是否会静默、存量项目怎么回补"。7 条裁决全部合并落盘：
  - **① 三处模板半截**：`bootstrap_agents.sh` 的 `PROJECT_MEMORY_MACHINE_SECTION`、`create_project_memory_file` 内嵌模板、补齐兜底 `required_blocks` 写出的 `usage_tracking.counted_files` **都只有 1 项、都无 `policy_ref`**，与 `usage-anchor-schema.md` 定义不符——即每个自举出来的项目都是半截的。三处补全。
  - **② 字段数漂移**：`project-memory-rules/SKILL.md` 写"3 个计数字段"漏 `usage_days`，而吸收阈值"跨 ≥2 日期"正依赖它（缺失时 `None < min_days` 直接跳过，引用再多也不进候选）。校准为 4 个并加说明。
  - **③ 静默降级**：`usage_ledger_validate.py` / `scan_absorption_candidates.py` 的 `except yaml.YAMLError: return {}` 让"解析失败"与"无数据"不可区分。改为抛 `AnchorParseError` + 退出码 2，错误信息指向健康检查脚本。
  - **④ 判据升级**：`project-rule-file-bootstrap-rules` 的「Schema 变更强制检查」兜底判据原为 `grep -c`（文本在即算过），卡不住本轮这类缺陷。新增第 3 条「解析器判据」——必须 `check_memory_anchors.py` `ok=true` 且 summary 数量符合预期。
  - **⑤ 存量回补缺口**：补齐路径只做加法、`needle not in block` 判据把半截块一路判为"已满足"，存量项目永远修不好。脚本侧新增「键在但内容不全」`[WARN]`；SKILL.md 新增第 5 条「存量项目回补」；`memory-usage-tracking-rules` 新增「存量项目锚点回补（强制）」小节（含完成判据与"回补本身不计数"）。
  - **⑥⑦ 新增校验载体**：新增 `scripts/check_memory_anchors.py`（只读，C1 yaml 可解析性 / C2 非法裸标量 / C3 schema 一致性 / C4 锚点条目一一对应 / C5 锚点区位于底部，`--list-missing` 出回补清单），并挂进 `project-rule-file-bootstrap-rules` 统一执行步骤 4.1（**每次 memory-bootstrap 都跑，不限于 schema 变更轮**）与本 skill 计数回写的两级前置校验。`usage-anchor-schema.md` 新增第 0 节「写入约束：中文技术内容的 yaml 裸标量」（保留符首字符 / 值内 `: ` 与 ` #` / 已加引号不重复处理）。
  - **验证**：新脚本对正常项目 `ok=true`（16/26/20）；两个缺陷 fixture 负向验证覆盖 C1~C5 并给出确切文件行号；坏样本下两个读取脚本均退出码 2 不再静默；真实自举三路径（新建 → counted_files 3 项 + policy_ref、幂等重跑不重复、半截块出 `[WARN]`）全通过；三脚本对正常项目回归与基线一致（16/26/20、默认候选 0、降阈值 62）。
  - **净增与整理**：净增 1 个脚本 + 若干条款；整理动作——删除 2 处 `except: return {}` 静默降级（减法），把 `counted_files` 的 4 份字面副本从"各自维护"收敛为"schema 为权威 + 脚本校验三处副本"，不新增第 5 份。
  - **同域冗余扫描**：范围 `memory-usage-tracking-rules` / `project-rule-file-bootstrap-rules` / `project-memory-rules` / `project-style-rules`；发现 0 处重复段落（C1~C5 在 schema 是定义、在 bootstrap 是分流动作，非重复）、0 处门控层叠（回写前校验 vs 自举后检查场景不同）、0 处散落产物（fixture 已清理）、引用链 18 处指向一致无断链。**PASS**。
  - 改动停在已改动未提交。
- 2026-08-22：**补齐规则 md 同步链路（bootstrap 受管章节）**——用户指出"计数+吸收规则要同步到规则 md 与同步脚本才能稳定触发"。核查发现 `bootstrap_agents.sh` 三处断点并修复：① `$BODY_SKILL_AUTO` 缺"### 记忆使用次数计数（强制）"子节（sync_section 对已存在 `##` 章节整体替换，luode-skills 跑 bootstrap 会把 AGENTS.md 手工子节删掉）；② `PROJECT_HISTORY_TEMPLATE` 缺 `## 计数锚点区`；③ `create_project_memory_file` 新建模板缺 `usage_tracking` 键（端到端测试抓到）。同步补齐 `CLAUDE.md` 计数条款与四件套模板 HISTORY 段标题统一。端到端验证：临时项目跑 bootstrap → AGENTS.md 含计数条款、HISTORY 含计数锚点区、MEMORY 含 usage_tracking，重跑幂等不重复。改动停在已改动未提交。
