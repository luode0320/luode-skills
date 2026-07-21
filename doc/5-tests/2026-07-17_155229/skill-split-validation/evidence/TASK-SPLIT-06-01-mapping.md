# TASK-SPLIT-06-01 原子化映射证据

- 测试：`TEST-SPLIT-021`（`python -X utf8 validate_skill_split.py --mode mapping --mapping mapping/2d-asset-rules.yaml`）。
- 映射产物：`doc/5-tests/2026-07-17_155229/skill-split-validation/mapping/2d-asset-rules.yaml`，29 条 `R-2D-001`~`R-2D-029`（对应 SKILL.md 各章节）+ 15 条 `RES-2D-001`~`RES-2D-015`（13 个 references + 3 个 scripts）+ 2 条 `shared_resources`（`asset-modes.md` 与 `agents/openai.yaml`），共 46 条目，`owner`/`migration_action` 覆盖率 100%。
- 基线指纹（只读核对，未改动）：`2d-asset-design/SKILL.md`：29,096B，MD5 `FB4E06AC8891F17FAB00CAE5D6462FE3`（超过 24,000B hard_warning）；13 个 `references/*.md`；3 个 `scripts/*.py`；1 个 `agents/openai.yaml`。
- 基线文档修正说明：实施周期 06 计划文档的"已核实文件和符号"只列出 6 个设计 refs + 6 个生产 refs 共 12 个，未提及 `references/asset-modes.md`；实测磁盘共 13 个 references。本轮判定 `asset-modes.md` 为计划文档遗漏项，归入 `shared_duplicate`（设计阶段"识别资产任务"与生产阶段"后处理锚点默认值"均需要），记录修正说明，不视为映射缺口。
- 拆分结论：`group_design = game-asset-design-gate-rules`（19 条 R-2D，6 个 RES-2D，覆盖设计确认、原创性、玩法可读性、商业级审稿闸门、项目风格一致性、素材 brief、参考筛选）；`group_production = game-asset-production-handoff-rules`（20 条 R-2D，9 个 RES-2D，覆盖 Godot 交付、真实生成、后处理、角色动画/地图/prop pack 生产、3 个脚本）；6 条 split_rewrite（description、"作用"、"自动触发范围"、"输出模式"、"资源"引用表、`agents/openai.yaml`）；1 条 shared_duplicate（`asset-modes.md`）。
- 关键判定：`## 地图、瓦片、场景道具` 一节文字里的商业级质量标准与设计组 `art-direction-quality-gate.md` 概念呼应，但其权威引用落点是生产组的 `map-strategies.md`/`layered-map-contract.md`/`prop-pack-contract.md` 三份文件，故整段判定 `group_production`，不拆分成设计/生产两半，避免同一小节被两组各改一半导致语义割裂。`references/image-generation-workflow.md` 虽然在"核心原则 1"里被设计阶段提及，但其内容是真实 imagegen 调用的 brief 格式与 generate/edit 判定规范，权威落点是生产组实际生成执行环节，故归 `group_production`，与实施周期 06 计划文档的基线分组一致。
- 命令与结果：`python -X utf8 validate_skill_split.py --mode mapping --mapping mapping/2d-asset-rules.yaml` → 退出码 0，`[通过] mapping：原子化映射 46 条目全部有 owner 与 migration_action，覆盖率 100%`。
- 结论：PASS。旧 skill 文件保持冻结基线，未做任何改动。
