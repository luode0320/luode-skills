# TASK-SPLIT-03-02 双入口建立证据

- 测试：`TEST-SPLIT-011`（`pwsh -NoProfile -File run_trigger_cases.ps1 -Phase pre-delete -CasesRoot cases\compliance`）。
- 新增文件：
  - `skill-execution-compliance-gate-rules/SKILL.md`（11,075B，< 16,000B 常规预算）、`agents/openai.yaml`（1,515B）、`references/applicability-and-gap-check.md`（3,393B，原文整份迁移，字节数与旧 skill 一致）。
  - `code-change-finalization-gate-rules/SKILL.md`（13,596B，< 16,000B 常规预算）、`agents/openai.yaml`（1,655B）、`references/next-step-suggestion-template.md`（3,084B，原文整份迁移，字节数与旧 skill 一致）。
- 边界核对：
  - 两个新 skill 的 `description` 与「权责边界与不负责事项」均各自声明“不重复检查对方职责”，互不依赖。
  - `reasoning-summary-structure-rules` 唯一阻断渲染 owner 边界在两个新 skill 的「输出要求（简化版）」中各自重述，未新增渲染逻辑。
  - frontmatter 经 `yaml.safe_load` 解析通过（`name`/`description` 字段完整）。
- 触发样本：`doc/5-tests/2026-07-17_155229/skill-split-validation/cases/compliance/trigger_cases.json` 新增 6 条 `pre-delete` 样本，覆盖「仅执行合规」「仅代码收口」「二者同时命中」「二者均不命中（其他 skill）」「运行时状态收口场景」「补注释场景」；`delete_cases.json` 新增 1 条 `pre-delete` 快照（`old_skill_present=true`、`new_skills_present=true`、`mapping_status=frozen`）。
- 命令与结果：`pwsh -NoProfile -File run_trigger_cases.ps1 -Phase pre-delete -CasesRoot cases\compliance` → 6 个 trigger 用例 + 1 个 pre-delete 快照全部 `[通过]`，输出显式声明未删除或修改任何真实 skill 目录。
- 结论：PASS。两个新 skill 命中边界唯一、无双写，`skill-compliance-gate-rules` 保持冻结未删除。