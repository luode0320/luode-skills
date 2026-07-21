# TASK-SPLIT-06-05 路由更新与删除前承接检查证据

- 测试：字典生成脚本重跑；`run_trigger_cases.ps1 -Phase pre-delete` 与 `-Phase post-delete`，`CasesRoot=cases/2d-design`。
- 路由更新范围（`rg -n --fixed-strings "2d-asset-design" --glob '!doc/**' ...` 复核，共 2 处活跃引用文件，按 `mapping/2d-asset-rules.yaml` 的 `group_design`（`game-asset-design-gate-rules`，设计确认闸门）/`group_production`（`game-asset-production-handoff-rules`，生产实现与交付）分组改写）：
  - `character-sprite-animation-production/SKILL.md`：`## 与 2d-asset-design 的关系` 标题与正文 2 处描述改指向 `game-asset-production-handoff-rules`（正式素材生产总流程、角色动作/sprite sheet 生产联动均属于生产交接组职责）。
  - `agent-sprite-forge-design/SKILL.md`：`## 和 2d-asset-design 的关系` 标题与正文 2 处描述改指向 `game-asset-production-handoff-rules`（确认后继续生产/后处理/Godot 交付、命中正式素材任务的联动触发均属于生产交接组职责）。
  - `PROJECT_MEMORY.md`（第 99/972 行）、`PROJECT_CURRENT.md`（第 17 行）：均为 `TASK-SPLIT-01-02` 候选矩阵历史决策记录（`2d-asset-design` 作为 P1 扩展种子例外进入 `CYCLE-SPLIT-06`），按 `TASK-SPLIT-06-04` 删除前检查已记录的范围排除结论，本轮路由任务同样不改写。
- 命令与结果：`python -X utf8 skill-dictionary/generate_dictionary.py` → 退出码 0，`implemented_total=88`（与周期 05 后一致，未变化）、`planned_missing=0`、`seed_total=33`（与周期 05 后一致，未变化）。
- 校验结果：
  - `2d-asset-design`、`game-asset-design-gate-rules`、`game-asset-production-handoff-rules` 三者的 `status` 均为 `"seed"`、`status_label` 均为 `"扩展种子"`：这是预期结果而非缺陷——`2d-asset-design` 本身在 `TASK-SPLIT-01-02` 候选矩阵中就是 P1 扩展种子例外，从未被纳入 `编码skill.md` 的正式 84 个 skill 主规划域表（`rg` 核实 `编码skill.md` 中不存在 `2d-asset-design`/`game-asset-design-gate-rules`/`game-asset-production-handoff-rules` 任一条目），因此本轮拆分不涉及 `implemented_total` 净增，这与 `CYCLE-SPLIT-02`~`05`（4 项正式候选，各自净增 1）的字典口径差异属于既定设计，非本轮路由遗漏。
  - `2d-asset-design/SKILL.md` MD5 `fb4e06ac8891f17fab00cae5d6462fe3` 与 `TASK-SPLIT-06-01` 基线一致，`references/`、`scripts/`、`agents/` 目录内容未被移动或删除。
  - `字典.md` 同步重新生成。
- 命令：`pwsh -NoProfile -File run_trigger_cases.ps1 -Phase pre-delete -CasesRoot cases/2d-design` → 6 个 trigger 用例 + 1 个 pre-delete 快照全部 `[通过]`。
- 命令：`pwsh -NoProfile -File run_trigger_cases.ps1 -Phase post-delete -CasesRoot cases/2d-design` → 6 个 trigger 用例 + 1 个 post-delete 快照全部 `[通过]`，输出显式声明 `未删除或修改任何真实 skill 目录`。
- 结论：路由更新未触碰任何 `.gitattributes`/`.editorconfig`/`doc/**` 历史文档；`PROJECT_MEMORY.md`/`PROJECT_CURRENT.md` 中的候选矩阵历史决策记录延续 `TASK-SPLIT-06-04` 已确认的范围排除，未回改；周期状态维持 `comparing`，未执行任何删除动作，等待用户对 `2d-asset-design` 目录的后续处置决策。
