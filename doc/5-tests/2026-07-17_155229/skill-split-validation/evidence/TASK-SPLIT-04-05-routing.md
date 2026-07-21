# TASK-SPLIT-04-05 路由更新与删除前承接检查证据

- 测试：字典生成脚本重跑；`run_trigger_cases.ps1 -Phase pre-delete` 与 `-Phase post-delete`，`CasesRoot=cases/release-test`。
- 路由更新范围（`rg -n --fixed-strings "project-release-test-rules" --glob '!doc/**' ...` 复核，共 10 处活跃引用文件，按 `mapping/release-test-rules.yaml` 的 `group_a`（`project-interface-baseline-rules`，接口基线）/`group_b`（`project-interface-release-execution-rules`，测试执行）分组改写）：
  - `README.md`、`编码skill.md`：Skill 一览表各 1 行拆为两行；`编码skill.md` 内“7. 上线前项目级接口门禁”“测试域默认分流规则”“测试域内部顺序”三处描述改为分别指出基线扫描（baseline）与门禁执行（execution）两个环节的归属，不再单指一个旧 skill。
  - `functional-validation-rules/SKILL.md`：判定与门禁一节（`agent-response-judgement.md`/`execution-gate.md`/`report-format.md` 三处引用）改指向 `project-interface-release-execution-rules`（三份文件均已迁移到该 skill 的 references）。
  - `test-strategy-rules/SKILL.md`：写接口样本分布一节（`test-data-construction-rules.md` 引用与联动标题）改指向 `project-interface-release-execution-rules`（该文件已迁移到该 skill 的 references）。
  - `swag-openapi-maintainer-rules/SKILL.md`：双索引同步联动的 2 处改指向 `project-interface-baseline-rules`（双索引一致性是基线组职责）。
  - `artifact-delivery-gate-rules/references/plain-language-template-registry.yaml`：`TPL-PLAIN-TEST-005` 的 `path` 字段改指向 `project-interface-release-execution-rules/references/report-format.md`（该文件已迁移）。
  - `inventory.yaml`：4 处“发现证据”字段中的 `report-format.md` 路径引用改指向新路径（该文件已迁移）；第 27 行 `doc/5-tests/2026-07-12_180240/...` 属历史测试运行留痕，按惯例保留不改。
  - `PROJECT_MEMORY.md`：`上线接口测试门禁规则` 条目的“别名”补充两个新 skill 名，“来源”中 `SKILL.md`/`baseline-asset-rules.md` 改指向 `project-interface-baseline-rules`（已迁移）；第 42/99/972 行为脚本共享路径或候选矩阵历史记录，未迁移/历史事实，均保留不改。
  - `PROJECT_STYLE.md`：“来源”中 `reusable-script-toolbox.md` 改指向 `project-interface-release-execution-rules`（已迁移）；第 309/310 行脚本调用示例与说明中的 `scripts/generate_release_test_plan.py` 路径保持不变（引擎脚本本轮判定为 `shared_resources`/`reference_only`，未迁移，仍是 `project-interface-release-execution-rules` 的唯一行为实现，物理路径不变）。
- 命令与结果：`python -X utf8 skill-dictionary/generate_dictionary.py` → 退出码 0，`implemented_total=87`（较周期 03 后的 86 净增 1）、`planned_missing=0`、`seed_total=34`。
- 校验结果：
  - `project-interface-baseline-rules`、`project-interface-release-execution-rules` 均为 `"status": "implemented"`。
  - `project-release-test-rules` 自动降级为 `"status": "seed"`；`SKILL.md` MD5 `44dd4de1b4d987b47c01f5b2a18328ee` 与 `TASK-SPLIT-04-01` 基线一致，`scripts/generate_release_test_plan.py`、`scripts/release_test_engine/` 物理文件未被移动或删除。
  - `字典.md` 同步重新生成。
- 命令：`pwsh -NoProfile -File run_trigger_cases.ps1 -Phase pre-delete -CasesRoot cases/release-test` → 6 个 trigger 用例 + 1 个 pre-delete 快照全部 `[通过]`。
- 命令：`pwsh -NoProfile -File run_trigger_cases.ps1 -Phase post-delete -CasesRoot cases/release-test` → 6 个 trigger 用例 + 1 个 post-delete 快照全部 `[通过]`，输出显式声明 `未删除或修改任何真实 skill 目录`。
- 结论：路由更新未触碰任何 `.gitattributes`/`.editorconfig`/`doc/**` 历史文档；引擎脚本 `scripts/release_test_engine/` 与 `scripts/generate_release_test_plan.py` 按既定的 `shared_resources` 决策保留原路径，未迁移、未复制；周期状态维持 `comparing`，未执行任何删除动作，等待用户对 `project-release-test-rules` 目录的后续处置决策。
