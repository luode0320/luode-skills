# TASK-SPLIT-03-03 删除前验证与引用扫描证据

- 测试：`TEST-SPLIT-012`（`python -X utf8 skill-dictionary/generate_dictionary.py`；再执行 `pwsh -NoProfile -File run_trigger_cases.ps1 -Phase post-delete -CasesRoot cases\compliance`）。
- 字典刷新命令与结果：`python -X utf8 skill-dictionary/generate_dictionary.py` → 退出码 0，输出 `implemented_total=85`、`planned_missing=0`、`seed_total=30`。
  - `skill-dictionary/data.js` 中 `skill-compliance-gate-rules` 仍为 `"status": "implemented"`、`"domain_label": "总控层"`（未改动 `编码skill.md` 源，旧入口按契约保持冻结主入口地位）。
  - `skill-execution-compliance-gate-rules`、`code-change-finalization-gate-rules` 均自动进入 `"status": "seed"`、`"domain_label": "扩展种子"`（SKILL.md 已存在但尚未写入 `编码skill.md` 总规划表，属预期的“新入口已就绪、路由未切换”中间态）。
  - `字典.md` 已同步重新生成。
- 触发样本补齐：`trigger_cases.json` 新增 6 条 `post-delete` 样本（`COMP-TRIGGER-POST-001`~`006`，与 `pre-delete` 样本一一对应，额外将 `skill-compliance-gate-rules` 列入 `forbidden`，模拟旧入口已下线后的路由）；`delete_cases.json` 新增 1 条 `post-delete` 快照（`old_skill_present=false`）。
- 命令与结果：
  - `pwsh -NoProfile -File run_trigger_cases.ps1 -Phase pre-delete -CasesRoot cases\compliance` → 复验仍全部 `[通过]`（回归确认新增 post-delete 样本未破坏既有 pre-delete 用例）。
  - `pwsh -NoProfile -File run_trigger_cases.ps1 -Phase post-delete -CasesRoot cases\compliance` → 6 个 trigger 用例 + 1 个 post-delete 快照全部 `[通过]`，输出显式声明未删除或修改任何真实 skill 目录。

## 旧入口依赖扫描（只读，`rg -l "skill-compliance-gate-rules"`）

- 仓库级路由/字典源（本任务允许文件范围外，未改动，需在未来专门的路由任务中处理，参照 `CYCLE-SPLIT-02` 的 `TASK-SPLIT-02-04` 模式）：`AGENTS.md`、`CLAUDE.md`、`README.md`、`编码skill.md`、`项目设计.md`、`字典.md`、`skill-dictionary/data.js`。
- 其他 skill 的活跃协作引用（同样只读记录，未改动，均以“不替代/联动 skill-compliance-gate-rules”的方式表述，需在路由任务中改指向新入口或改为同时联动两个新入口）：
  - `skill-hit-check-rules/SKILL.md`（2 处，含收口联动清单）
  - `skill-audit-rules/SKILL.md`
  - `project-change-review-rules/SKILL.md`
  - `reasoning-summary-structure-rules/SKILL.md`
  - `frontend-design/SKILL.md`
  - `code-style-consistency-rules/SKILL.md`
  - `thread-title-rules/SKILL.md`
  - `autonomous-execution-rules/SKILL.md`
  - `parallel-task-dispatch-rules/references/existing-skill-mapping.md`
  - `vercel-react-best-practices/AGENTS.md`
- 历史记录类引用（`doc/2-需求/`、`doc/3-实施/`、`doc/6-审查/`、`doc/5-tests/` 下的既有审查/需求/实施/测试文档），均为已归档历史事实，按项目惯例不回改历史记录。
- `project-agents-bootstrap/SKILL.md`、`scripts/bootstrap_agents.sh` 引用属于 `CYCLE-SPLIT-02` 遗留的同类冻结引用，不属本周期处理范围。
- 结论：旧入口 `skill-compliance-gate-rules` 目前仍被至少 10 处活跃 skill 协作引用与 7 处仓库级路由/字典源引用，删除前必须先有专门的路由更新任务（对齐 `CYCLE-SPLIT-02` 的 `TASK-SPLIT-02-04` 范式）改写这些引用指向两个新 skill，本任务契约允许文件不含这些路由文件，故本轮不改写，只记录扫描结果。

## 收口结论

- `TEST-SPLIT-010`/`011`/`012` 全部 PASS；旧 skill 全程冻结未改动（MD5 与 `TASK-SPLIT-03-01` 记录一致）；两个新 skill 均已建立且命中边界唯一；字典刷新显示新入口处于“已就绪、扩展种子”中间态，旧入口仍是唯一正式入口。
- `CYCLE-SPLIT-03` 状态维持 `comparing`，未执行任何真实删除动作，未触碰旧入口内容或仓库级路由文件；等待用户对路由切换与旧 skill 后续处置做出决策。