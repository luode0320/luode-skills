# TASK-SPLIT-02-04/02-05 路由更新与删除前承接检查证据

- 测试：`TEST-SPLIT-008`（字典生成脚本重跑）、`TEST-SPLIT-009`（pre-delete 触发样例复验，命令与 `TEST-SPLIT-005` 完全相同）。
- 路由更新范围（仅本轮 5 处允许文件，均已核对 `git diff` 逐行确认无越界改动）：
  - `AGENTS.md`：2 处引用（Skill 命中强制规则、上下文压缩续做规则）改为 `project-rule-file-bootstrap-rules` + `project-memory-file-bootstrap-rules` 联动表述。
  - `CLAUDE.md`：同上 2 处，文案一致。
  - `README.md`：Skill 一览表 1 行 `project-agents-bootstrap` 拆为两行；`176`/`179` 行历史 changelog 记录保留不改（历史事实不回改）。
  - `编码skill.md`：总控层 skill 表 1 行拆为两行；`godot-project-bootstrap-rules` 行内联动引用同步指向 `project-rule-file-bootstrap-rules`。
  - `项目设计.md`：3 处（脚本清单说明、总控层代表模块表、6.2 节脚本说明）补充共用脚本与双 skill 归属说明，脚本路径本身不变（脚本未迁移）。
- 命令：`python -X utf8 skill-dictionary/generate_dictionary.py` → 退出码 0，输出 `implemented_total=85`、`planned_missing=0`、`seed_total=28`。
- 校验结果：
  - `skill-dictionary/data.js` 中 `project-rule-file-bootstrap-rules`、`project-memory-file-bootstrap-rules` 均为 `"status": "implemented"`、`"domain_label": "总控层"`。
  - `project-agents-bootstrap` 自动降级为 `"status": "seed"`、`"domain_label": "扩展种子"`（SKILL.md 文件本身未改动，MD5 与 TASK-02-01 记录一致，未被删除）。
  - `字典.md` 同步重新生成（37 处插入/31 处删除，对应上述路由变化）。
- 命令：`pwsh -File run_trigger_cases.ps1 -Phase pre-delete -CasesRoot cases\bootstrap` → 6 个 trigger 用例与 1 个 pre-delete 用例全部 `[通过]`，输出显式声明 `未删除或修改任何真实 skill 目录`。
- 命令：`python -X utf8 validate_skill_split.py --mode mapping --mapping doc/5-tests/2026-07-17_155229/skill-split-validation/mapping/bootstrap-rules.yaml` → 复验通过，55 条目 owner+migration_action 100% 覆盖。
- 结论：路由更新未触碰任何 `.gitattributes`/`.editorconfig`/其他项目历史 changelog；周期状态维持 `comparing`，未执行任何删除动作，等待用户对 `project-agents-bootstrap` 目录的后续处置决策。