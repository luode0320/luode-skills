# 实施周期 01：索引模型与引用重构

- 对应需求文档: `doc/2-需求/2026-07-03_162802_project-memory-rules双层知识库升级.md`
- 来源对象标识（需求或 Bug）: `project-memory-rules双层知识库升级`
- 对应实施总览: `doc/3-实施/2026-07-03_162802_project-memory-rules双层知识库升级_实施总览.md`
- 周期文档命名主干: `2026-07-03_162802_project-memory-rules双层知识库升级_实施周期01_索引模型与引用重构`
- 当前周期目标: 冻结 `PROJECT_MEMORY.md` 底部机器索引区的结构和单文件双区 references 体系
- 当前周期只做这一件事: 明确单文件内数据模型，不进入 skill 行为改写

## 当前周期最小任务清单

1. 定义 `memory-index-schema.md`
2. 新增实体类型与关系类型文档
3. 新增抽取流程、检索模式、冲突与失效规则文档

## 当前周期步骤顺序

1. 先确定 `PROJECT_MEMORY.md` 底部机器索引区的最小字段集: `version`、`entities`、`relations`、`evidence`、`contexts`、`lifecycle`、`retrieval_hints`、`extensions`。
2. 再确定实体类型、关系类型和状态集合。
3. 最后补齐 workflow / retrieval / conflict 三类流程性资料。

## 当前周期验证点

- 用 3 组样本事实验证 schema 是否足够表达:
  - 术语类事实
  - 规则类事实
  - 方法映射类事实
- 检查每份 reference 至少能支撑一个需求项。
- 检查是否仍保留“唯一长期记忆主文件”的兼容语义。

## 当前周期阻断项

- 若无法收敛 `PROJECT_MEMORY.md` 底部机器索引区的固定结构方案，则本周期阻断。
- 若状态集合无法覆盖“启用 / 失效 / 冲突 / 退役”场景，则本周期阻断。
