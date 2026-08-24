---
schema_version: 1
template_version: 1
doc_id: "STYLE-DBSCRIPTS-20260824-01"
doc_type: style_regression
source_ids:
  - "REQ-DB-SCRIPTS-LAYOUT"
  - "CYCLE-01"
status: accepted
version: "v1.0"
current_slice: "CYCLE-01"
updated_at: "2026-08-24 20:28:46"
reader_level: business_general
writing_style: plain_chinese
appendix_policy: preserve_existing_or_one_terminal_appendix
---

# 6-review 风格回归：数据库脚本目录树 database/scripts 调整

结论：本轮核对 `package-structure-rules` 的规则文档、校验脚本和新增测试的写法与归位；影响：不代替业务正确性判断和发布放行；范围：`package-structure-rules` skill 的目录树迁移改动、`PROJECT_MEMORY.md` 镜像、新增测试与工程文档；非范围：业务运行时正确性、发布放行、存量项目迁移；变化：`database/sql/` 迁移为 `database/scripts/{sql,js,lua}/`，旧路径废弃；完成标准：STYLE: PASS；术语说明：风格回归是对规则文档、脚本和测试资产写法的检查；验证状态：真实测试通过后执行，文档机器校验、残留 Grep 与回读一致性均完成。

## 文档信息

| 字段 | 内容 |
| --- | --- |
| 关联任务 | `TASK-01` 至 `TASK-06` |
| 关联真实测试 | `TEST-01` 至 `TEST-05` |
| 检查时点 | 真实测试通过后 |

## 检查范围

本轮检查：

- `database/sql/` 旧路径是否在规则文档（SKILL.md、4 个 references）中彻底清除，仅保留废弃声明与禁止路径定义；
- `database/scripts/` 结构是否在机器事实源（placement-catalog.yaml）、校验脚本（placement_catalog.py）、人工目录树（project-layout-v2.md）、细化文档（database-layout.md）四处一致；
- 新增测试是否位于根 `test/` 镜像路径、使用 `*_test.py` 命名；
- 校验脚本 docstring 是否包含参数、返回与最近修改时间；
- 新增与修改文件是否 UTF-8、中文无乱码；
- 工程文档是否使用扁平 md 命名并符合白话摘要结构；
- `PROJECT_MEMORY.md` 机器索引区是否同步新口径。

### 范围外说明

不迁移存量项目文件、不修改知识库历史快照笔记、不改动其他兄弟 skill、不执行 Git 提交；`usage-recipes-go.md` 的 Go 标准库 `"database/sql/driver"` 引用不属于目录树口径，不在清理范围。

## 真实测试前置证据

新增测试 `python -X utf8 -m unittest test.package-structure-rules.database_scripts_layout_test -v` → `Ran 5 tests ... OK`；模块回归 `python -X utf8 -m unittest discover -s test/package-structure-rules -p "*_test.py"` 仅存 2 个既有 apifox 失败（改动前已存在，与本轮无关）；yaml 加载 `json.load` OK（entries: 106）；CLI `query --artifact database-sql --category ddl` 返回 `database/scripts/sql/ddl`。对应证据 `EVIDENCE-01` 至 `EVIDENCE-05`。

## 6-review 结论

STYLE: PASS

本轮未发现需要修复的风格问题。`database/sql` 旧路径已从规则文档清除（仅保留废弃声明与禁止路径定义），`database/scripts` 结构在事实源、脚本、目录树、细化文档四处一致，新增测试归位与命名正确，脚本 docstring 完整，文件编码 UTF-8，工程文档符合扁平 md 与白话摘要结构，项目记忆镜像已同步。

### 完成标准

风格回归完成标准为：旧路径清除、新结构四处一致、测试归位正确、改动最小、全部文件 UTF-8、文档通过机器校验。以上标准全部满足，判定 PASS。

## 检查清单

| 检查项 | 结论 | 依据 |
| --- | --- | --- |
| 旧路径清除 | PASS | 全仓库 Grep `database/sql` 仅剩：废弃声明（SKILL.md L31、database-layout.md L27、PROJECT_MEMORY.md L367）、禁止路径定义（placement-catalog.yaml L29）、Go 标准库引用（usage-recipes-go.md L324）、测试断言（database_scripts_layout_test.py）、迁移说明 docstring（placement_catalog.py L706）与归档文档 |
| 新结构四处一致 | PASS | placement-catalog.yaml（allowed_children 三层 + 7 entries）与 project-layout-v2.md（L125-152 目录树）、database-layout.md（17 行表格）、SKILL.md L31 表述一致 |
| 测试归位 | PASS | 新增 `test/package-structure-rules/database_scripts_layout_test.py`，根 `test/` 镜像、`*_test.py` 命名 |
| docstring 完整 | PASS | `check_database_script_path` 含参数、返回、最近修改时间（L706） |
| 最小改动 | PASS | 仅改 `package-structure-rules` 7 个文件 + PROJECT_MEMORY + 新增测试 + 归档文档，未新增 skill、未改兄弟 skill |
| 文件编码 | PASS | 新增与修改文件 UTF-8，中文无乱码 |
| 文档形态 | PASS | 实施总览/周期/6-review 使用扁平 md，通过 validate_engineering_docs.py 机器校验（error_codes 空） |
| 记忆镜像同步 | PASS | PROJECT_MEMORY.md L367 与 entity `rule.backend-database-storage-layout` definition 已同步新口径 |
| 未引入无关改动 | PASS | 未动 config 条目、skeletons、`test/` 其他测试；未执行 Git 提交 |

## 问题与修复

| 序号 | 问题 | 严重度 | 修复动作 | 状态 |
| --- | --- | --- | --- | --- |
| 无 | N/A + 原因 + 证据：九项风格检查全部一次通过；证据是上文检查清单中无任一 FIX_REQUIRED 项 | N/A | N/A | N/A |

图片资产决策：N/A + 原因 + 证据：本轮是规则文档、脚本与测试资产改动，没有 UI、截图、原型或位图需要视觉留证。

## 执行附录

### 关键改动

- `package-structure-rules/SKILL.md`（L31 核心边界第 7 条）
- `package-structure-rules/references/placement-catalog.yaml`（content_types / forbidden_paths / allowed_children / entries）
- `package-structure-rules/references/database-layout.md`（全表）
- `package-structure-rules/references/project-layout-v2.md`（L12 + L125-152）
- `package-structure-rules/references/lookup-and-reference-contract.md`（L31）
- `package-structure-rules/references/directory-usage-routing.md`（L64）
- `package-structure-rules/scripts/placement_catalog.py`（`check_database_script_path` 泛化、删 L750 硬编码）
- 仓库级：`PROJECT_MEMORY.md`（L367 + entity definition）
- 新增：`test/package-structure-rules/database_scripts_layout_test.py`、`doc/3-实施/2026-08-24_202846_*` 两份、本 6-review

### 验证命令

- 文档校验：`python -X utf8 artifact-delivery-gate-rules/scripts/validate_engineering_docs.py --profile implementation_overview --doc "doc/3-实施/2026-08-24_202846_数据库脚本目录树database-scripts调整_实施总览.md" --root D:\谷歌云盘\luode-skills`（error_codes 空）
- 周期校验：同上 `--profile implementation_cycle`（error_codes 空）
- 新增测试：`python -X utf8 -m unittest test.package-structure-rules.database_scripts_layout_test -v`（5/5 OK）
- 模块回归：`python -X utf8 -m unittest discover -s test/package-structure-rules -p "*_test.py"`（仅既有 apifox 失败）
- 全量回归：`python -X utf8 test/run_python_tests.py`（失败集合为既有环境项，无本轮相关新失败）

## 追踪附录

- 来源：`REQ-DB-SCRIPTS-LAYOUT`
- 周期：`CYCLE-01`
- 任务：`TASK-01` 至 `TASK-06`
- 测试：`TEST-01` 至 `TEST-05`
- 风格证据：`EVIDENCE-01` 至 `EVIDENCE-06`
