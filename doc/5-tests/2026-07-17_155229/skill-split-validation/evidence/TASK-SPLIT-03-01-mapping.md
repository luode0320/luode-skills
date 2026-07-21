# TASK-SPLIT-03-01 原子化映射证据

- 测试：`TEST-SPLIT-010`（`python -X utf8 validate_skill_split.py --mode mapping --mapping mapping/compliance-rules.yaml`）。
- 映射产物：`doc/5-tests/2026-07-17_155229/skill-split-validation/mapping/compliance-rules.yaml`，19 条 `R-COMP-001`~`R-COMP-019` 规则 + 4 条 `shared_resources`，共 23 条目，`owner`/`migration_action` 覆盖率 100%。
- 基线指纹（只读核对，未改动）：
  - `skill-compliance-gate-rules/SKILL.md`：19,211B，MD5 `16f5c34742279b64cae5de6daf8b1693`。
  - `agents/openai.yaml`：1,585B，MD5 `c63871136910cc346ba92df4f3971ffd`。
  - `references/applicability-and-gap-check.md`：3,393B，MD5 `36ce61fb03b935a75c614c3837066111`。
  - `references/next-step-suggestion-template.md`：3,084B，MD5 `8c8eec079543ee2df7d3dcaefb5950a1`。
- 拆分结论：`group_a = skill-execution-compliance-gate-rules`（其他已命中 skill 的执行完整性、`blocked/manual_handoff` 共享契约、Skill 执行证据、运行时状态真收口）；`group_b = code-change-finalization-gate-rules`（代码/测试改动的注释双 skill、implementation-review 收口、真实运行验证、router 提交前检查、用户手改保护）。
- 修正记录：初版映射把「Skill 执行证据确认」与「运行时状态收口确认」（默认执行流程第 16、17 项及进入清单第 13 项）误拆到 `group_b`，与「阻断判定与处理」通用两条（`R-COMP-010`/`R-COMP-012`，同概念）owner 不一致，构成潜在双写。复核后统一改为 `group_a` 承接，`R-COMP-004`/`R-COMP-005`/`R-COMP-006`/`R-COMP-007` 的 `section`/`source`/`note` 已同步更正，重跑 `TEST-SPLIT-010` 仍 23 条目 100% 覆盖。
- 命令与结果：`python -X utf8 validate_skill_split.py --mode mapping --mapping mapping/compliance-rules.yaml` → 退出码 0，`[通过] mapping：原子化映射 23 条目全部有 owner 与 migration_action，覆盖率 100%`。
- 结论：PASS。旧 skill 文件保持冻结基线，未做任何改动。