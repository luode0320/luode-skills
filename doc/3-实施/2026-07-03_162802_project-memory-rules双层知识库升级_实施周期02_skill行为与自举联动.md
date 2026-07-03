# 实施周期 02：skill 行为与自举联动

- 对应需求文档: `doc/2-需求/2026-07-03_162802_project-memory-rules双层知识库升级.md`
- 来源对象标识（需求或 Bug）: `project-memory-rules双层知识库升级`
- 对应实施总览: `doc/3-实施/2026-07-03_162802_project-memory-rules双层知识库升级_实施总览.md`
- 周期文档命名主干: `2026-07-03_162802_project-memory-rules双层知识库升级_实施周期02_skill行为与自举联动`
- 当前周期目标: 让 `project-memory-rules` 与 `project-agents-bootstrap` 真正理解单文件双区记忆模型
- 当前周期只做这一件事: 改写 skill 行为、自举联动和默认提示词

## 当前周期最小任务清单

1. 改写 `project-memory-rules/SKILL.md`
2. 重写 `project-memory-template.md`
3. 更新 `agents/openai.yaml`
4. 补齐 `project-agents-bootstrap/SKILL.md` 与 `bootstrap_agents.sh`

## 当前周期步骤顺序

1. 先按周期 01 的 schema 改写 `project-memory-rules/SKILL.md`。
2. 再同步模板与默认 prompt。
3. 最后接入 bootstrap 编排逻辑，确保新会话和聚合 md 指令都覆盖 `PROJECT_MEMORY.md` 底部机器索引区。

## 当前周期验证点

- 用 3 个命中样本验证默认流程是否明确“机器索引区优先、正文同步”。
- 检查 prompt、skill、template 三者字段和顺序是否一致。
- 检查 bootstrap 规则是否仍把 `PROJECT_MEMORY.md` 作为唯一长期记忆主文件，而不是再创建第二个索引文件。

## 当前周期阻断项

- 若 `SKILL.md` 与 bootstrap 无法就单文件双区职责达成一致，则本周期阻断。
- 若更新 `description` 或 `##` 标题后无法完成字典刷新联动，则本周期阻断。
