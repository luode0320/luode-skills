# project-memory-rules 双层知识库升级当前改动总审查

## 1. 审查范围

- `project-memory-rules/`
- `project-agents-bootstrap/`
- `PROJECT_MEMORY.md`
- `README.md`
- `skill-dictionary/data.js`
- `字典.md`
- `doc/7-验收/2026-07-03_170712_project-memory-rules双层知识库升级_验收标准.md`
- `doc/5-tests/2026-07-03_172340_project-memory-rules双层知识库升级/README.md`

## 2. 审查结论

- 审查结论: `通过`
- 是否允许进入提交阶段: `是`
- 是否存在阻断问题: `否`

## 3. 核心检查项

### 3.1 需求一致性

- 已与需求文档中的“单文件双区 + 不新增 `PROJECT_MEMORY_INDEX.yaml`”方向一致
- `project-memory-rules` 与 `project-agents-bootstrap` 的职责边界已分开：
  - 前者负责事实、实体、关系、证据和同步规则
  - 后者负责双区骨架检测、创建与幂等补齐

### 3.2 实现一致性

- `project-memory-rules/SKILL.md` 已改为机器索引区优先
- `project-memory-rules/agents/openai.yaml` 已同步新顺序
- `project-memory-rules/references/` 已补齐 schema、类型、流程、检索、冲突资料
- `project-agents-bootstrap/scripts/bootstrap_agents.sh` 已新增 `PROJECT_MEMORY.md` 双区骨架逻辑

### 3.3 风险检查

- 风险 1: bootstrap 误重写人工正文
  - 结果: 已规避，脚本仅在缺少 `## 机器索引区` 时追加或补最小 schema，不重写正文区
- 风险 2: 双区结构引入第二个主文件
  - 结果: 已规避，规则与脚本均明确禁止新增 `PROJECT_MEMORY_INDEX.yaml`
- 风险 3: 字典未刷新导致仓库说明与 skill 不一致
  - 结果: 已规避，已真实运行生成脚本

### 3.4 注释与可读性

- 新增脚本函数已补充职责注释
- 文档与规则文件均保持 UTF-8 中文内容

## 4. 验证证据

1. `bash -lc "bash -n project-agents-bootstrap/scripts/bootstrap_agents.sh"` 通过
2. `bash -lc "./project-agents-bootstrap/scripts/bootstrap_agents.sh --repo . --target codex"` 通过
3. `C:\Users\luode\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe skill-dictionary/generate_dictionary.py` 通过
4. `PROJECT_MEMORY.md` 已新增机器索引区并完成 3 条真实样本迁移
5. 独立验收文档与测试记录已落盘

## 5. 残余说明

- 本轮没有做 `PROJECT_MEMORY.md` 全量历史实体化迁移，只做了最小验证样本
- 工作区存在其他非本轮改动文件，未做回退；本审查仅覆盖本次升级涉及范围
