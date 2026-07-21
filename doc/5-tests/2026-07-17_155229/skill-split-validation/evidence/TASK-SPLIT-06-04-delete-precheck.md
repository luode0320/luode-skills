# TASK-SPLIT-06-04 收尾（字典刷新/触发验证/路由预检）证据

- 字典刷新：`python -X utf8 skill-dictionary/generate_dictionary.py` 输出 `implemented_total=85`、`planned_missing=0`、`seed_total=36`；`game-asset-design-gate-rules` 与 `game-asset-production-handoff-rules` 均以"扩展种子"身份进入 `字典.md`（11.18、11.19）与 `skill-dictionary/data.js`（因未写入 `编码skill.md` 总规划表格，属预期降级行为，与 CYCLE-03/04/05 先例一致）；旧 `2d-asset-design` 在字典中保持"已实现"不变。
- 触发 fixture：`doc/5-tests/2026-07-17_155229/skill-split-validation/cases/2d-design/`（TASK-06-02 阶段已建好两阶段样本，本任务复用）：
  - `trigger_cases.json`：12 条（6 条 `pre-delete` + 6 条 `post-delete`），覆盖"设计闸门单独命中”“生产交接单独命中”“全流程两者都命中”“无关任务两者都不命中”“外部素材直接使用询问命中设计闸门”“已生成素材仅需后处理命中生产交接”六类场景，`post-delete` 场景额外要求 `2d-asset-design` 不得出现在命中列表。
  - `delete_cases.json`：2 条（`pre-delete` + `post-delete`），`old_skill=2d-asset-design`，`new_skills=[game-asset-design-gate-rules, game-asset-production-handoff-rules]`，`mapping_status=frozen`。
- `TEST-SPLIT-022`（复跑，两阶段）：
  - `run_trigger_cases.ps1 -Phase pre-delete -RepoRoot "D:\luode\luode-skills" -CasesRoot ".../cases/2d-design"` → `mode=pre-delete`，7 条样本（6 trigger + 1 delete）全部 `[通过]`，脚本输出 `[PASS]` 与 `[DONE] No real skill directory was deleted or modified`。
  - `run_trigger_cases.ps1 -Phase post-delete -RepoRoot "D:\luode\luode-skills" -CasesRoot ".../cases/2d-design"` → `mode=post-delete`，7 条样本（6 trigger + 1 delete）全部 `[通过]`，脚本同样输出 `[PASS]` 与 `[DONE]`。
- `mapping` 模式复验：`validate_skill_split.py --mode mapping --mapping mapping/2d-asset-rules.yaml` → 46 条目 owner/migration_action 覆盖率 100%，与 TASK-06-01 结论一致，未因新建两个 skill 目录而失效。
- 旧入口只读依赖扫描（`rg -l "2d-asset-design" --glob '!doc/5-tests/**' --glob '!2d-asset-design/**' --glob '!skill-dictionary/**' --glob '!字典.md' --glob '!game-asset-design-gate-rules/**' --glob '!game-asset-production-handoff-rules/**'`）命中 9 处，均只记录、不改写（本周期计划表无专门路由任务，与 CYCLE-03/04/05 先例一致）：
  - `agent-sprite-forge-design/SKILL.md`、`character-sprite-animation-production/SKILL.md`：共享根目录设计/生产联动 skill 对 `2d-asset-design` 的双向引用（与旧 `agent-browser` 拆分时的跨 skill 引用性质相同，本周期不改写，留待用户授权删除旧 skill 时统一处理）。
  - `doc/2-需求/`、`doc/3-实施/`（含实施总览、需求与实施计划全量顺序实施方案、周期01、周期06自身）、`doc/7-验收/`：本次拆分工程文档自身对旧 skill 名称的历史记录性引用，属预期，不改写。
  - `PROJECT_MEMORY.md`、`PROJECT_CURRENT.md`：项目记忆文件中的既有记录，本轮任务范围不含记忆文件改写，不改写。
- 最大推进边界确认：本任务只完成对照、字典刷新、触发验证与删除前只读扫描，**未执行任何旧 `2d-asset-design` 目录的删除或改写**，删除动作需等待用户明确授权。
- 结论：PASS。CYCLE-SPLIT-06 的 TASK-06-01~04 全部完成；下一步是更新实施总览（v1.5）并等待用户对 CYCLE-07/08 或删除授权的指示。
