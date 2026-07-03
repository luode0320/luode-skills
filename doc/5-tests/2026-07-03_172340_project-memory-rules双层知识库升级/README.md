# project-memory-rules 双层知识库升级验证记录

## 1. 测试目标

验证 `project-memory-rules` 与 `project-agents-bootstrap` 升级后，是否已经在当前仓库内真实形成“单文件双区”的长期记忆能力。

## 2. 验证范围

1. `PROJECT_MEMORY.md` 是否仍为唯一长期记忆主文件
2. `PROJECT_MEMORY.md` 是否已补齐 `## 机器索引区`
3. `project-memory-rules` 是否已经切换到“机器索引区优先、正文同步”口径
4. `project-agents-bootstrap/scripts/bootstrap_agents.sh` 是否能真实补齐双区骨架
5. skill 字典是否已刷新
6. 是否已完成最小迁移演练

## 3. 执行记录

### 3.1 脚本语法检查

- 命令: `bash -lc "bash -n project-agents-bootstrap/scripts/bootstrap_agents.sh"`
- 结果: 通过

### 3.2 自举脚本真实执行

- 命令: `bash -lc "./project-agents-bootstrap/scripts/bootstrap_agents.sh --repo . --target codex"`
- 关键结果:
  - 脚本输出 `已追加机器索引区: PROJECT_MEMORY.md`
  - 脚本完成根目录 `AGENTS.md` / `CLAUDE.md` 受管章节同步
  - 本仓库 `PROJECT_MEMORY.md` 已真实补齐双区结构

### 3.3 字典刷新

- 命令: `C:\Users\luode\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe skill-dictionary/generate_dictionary.py`
- 结果:
  - 生成 `skill-dictionary/data.js`
  - 生成 `字典.md`
  - 控制台输出 `implemented_total: 81`

## 4. 迁移演练样本

本轮从当前仓库现有 `PROJECT_MEMORY.md` 正文中选取 3 条长期记忆，迁入机器索引区：

| 样本 | 正文条目 | 机器实体 ID | 结果 |
| --- | --- | --- | --- |
| 样本 1 | URL 认证浏览器默认路由 | `rule.authenticated-url-routing` | 已迁入 |
| 样本 2 | doc 顶层混合命名 | `term.doc-top-level-mixed-naming` | 已迁入 |
| 样本 3 | 旧目录处理规则 | `rule.old-directory-cleanup` | 已迁入 |

补充结果：

- 已新增 4 条证据记录
- 已新增 3 条上下文记录
- 已新增 1 条关系记录
- 已补齐 `lifecycle.active` 与 `retrieval_hints`

## 5. 通过标准核对

| 检查项 | 结果 | 证据 |
| --- | --- | --- |
| 唯一长期记忆主文件仍是 `PROJECT_MEMORY.md` | 通过 | 根目录无 `PROJECT_MEMORY_INDEX.yaml`，且 `PROJECT_MEMORY.md` 已扩展为双区 |
| 底部 `## 机器索引区` 已存在 | 通过 | `PROJECT_MEMORY.md` 当前末尾已有 YAML 机器区 |
| memory skill 更新顺序已切到机器优先 | 通过 | `project-memory-rules/SKILL.md`、`agents/openai.yaml` |
| bootstrap 可补齐双区骨架 | 通过 | 脚本真实执行输出与 `PROJECT_MEMORY.md` diff |
| 字典已刷新 | 通过 | `skill-dictionary/data.js`、`字典.md` |
| 已完成最小真实迁移演练 | 通过 | 本文第 4 节与 `PROJECT_MEMORY.md` 机器区样本实体 |

## 6. 结论

本轮验证通过。当前仓库已完成：

1. 单文件双区结构落地
2. bootstrap 双区骨架补齐
3. 最小真实迁移演练
4. 字典刷新

仍未做的事情：

- 旧正文的全量实体化迁移尚未进行，本轮仅完成最小样本演练
- 外部向量库 / 图数据库接入仍不在本轮范围内
