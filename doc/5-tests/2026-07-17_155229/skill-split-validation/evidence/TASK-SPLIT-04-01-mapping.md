# TASK-SPLIT-04-01 原子化映射证据

- 测试：`TEST-SPLIT-013`（`python -X utf8 validate_skill_split.py --mode mapping --mapping mapping/release-test-rules.yaml`）。
- 映射产物：`doc/5-tests/2026-07-17_155229/skill-split-validation/mapping/release-test-rules.yaml`，32 条 `R-RT-001`~`R-RT-032` 规则 + 5 条 `shared_resources`，共 37 条目，`owner`/`migration_action` 覆盖率 100%。
- 基线指纹（只读核对，未改动）：
  - `project-release-test-rules/SKILL.md`：21,732B，MD5 `44dd4de1b4d987b47c01f5b2a18328ee`。
  - `agents/openai.yaml`：1,530B，MD5 `26aa13803638b72879b154ef10292f4c`。
  - 14 个 `references/*.md`：合计 78,907B（agent-response-judgement.md 9,978B / baseline-asset-rules.md 4,418B / bootstrap-workflow.md 2,567B / dependency-graph-rules.md 3,199B / execution-gate.md 6,356B / existing-test-skill-integration.md 4,201B / interface-inventory-schema.md 7,117B / inventory-reconcile-rules.md 2,077B / openapi-inventory-sync-rules.md 5,465B / output-artifacts.md 2,229B / report-format.md 12,368B / reusable-script-toolbox.md 5,609B / test-data-construction-rules.md 9,499B / test-selection-policy.md 3,759B），逐文件 MD5 见 Get-ChildItem -Recurse | Get-FileHash 命令留痕（本轮命令行输出，未落盘为独立文件）。
  - `scripts/generate_release_test_plan.py`：73,338B，MD5 `ada2daf8d41bcc8a64a40866a4e2d9dd`（兼容入口）。
  - `scripts/release_test_engine/`：25 个模块（含 9 个 `adapters/*` 协议适配器），总计约 220KB，逐文件 MD5 已核对但不迁移。
- 拆分结论：`group_a = project-interface-baseline-rules`（接口事实基线、双索引、参数来源、依赖图，只消费 engine 输出，不持有 engine 代码）；`group_b = project-interface-release-execution-rules`（engine 唯一行为 owner：runner/report/gate/judge/adapter，测试资产归档，最终放行结论）。
- 关键决策：`scripts/release_test_engine/` 与 `scripts/generate_release_test_plan.py` 本轮判定为 `shared_resources`，`owner=group_b`，`migration_action=reference_only`，即引擎实现保持原路径不迁移，两个新 skill 都不复制 Python 实现，避免同一段代码被两组同时声明为主实现；baseline skill 只在 references 里定义其消费的输出文件 schema。此决策直接对应实施总览关于 engine shared IR/schema 的主 owner 为 execution skill、baseline 只消费的既定边界。
- 命令与结果：`python -X utf8 validate_skill_split.py --mode mapping --mapping mapping/release-test-rules.yaml` 退出码 0，输出 [通过] mapping：原子化映射 37 条目全部有 owner 与 migration_action，覆盖率 100%。
- 结论：PASS。旧 skill 文件保持冻结基线，未做任何改动。