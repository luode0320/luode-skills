---
schema_version: 1
template_version: 1
doc_id: "STYLE-CACHETASK-20260827-01"
doc_type: style_regression
source_ids:
  - "SRC-cachetask-20260827"
status: accepted
version: "v1.0"
current_slice: "CACHETASK-01"
updated_at: "2026-08-27 14:45:00"
reader_level: business_general
writing_style: plain_chinese
appendix_policy: preserve_existing_or_one_terminal_appendix
---

# 6-review 风格回归：cachetask 缓存重建任务目录加入目录树

结论：本轮仅核对规则文档、脚本落点和测试资产的写法与归位；影响：不代替业务正确性判断和发布放行；范围：`package-structure-rules`（目录树、语言 reference、SKILL.md、placement_catalog.py）、`work-report-summary-rules/scripts/generate_git_report.py`、`configuration_layout_test.py` 测试基线、字典刷新与收口证据；非范围：业务运行时正确性、发布放行、其他兄弟 skill；变化：后端根级新增 `cachetask/` 缓存重建任务目录（缓存过期驱动异步重建，SWR 模式），与 `crontask/`（时间驱动）、`async/`（消息驱动）并列，并同步 adoption 根级目录白名单与工作汇报目录分类映射；完成标准：STYLE: PASS；术语说明：风格回归是对代码、规则文档和测试资产写法的检查；验证状态：本次相关真实测试通过后执行，字典刷新与项目记忆同步完成。

## 文档信息

| 字段 | 内容 |
| --- | --- |
| 关联任务 | cachetask 目录树吸收（内部更新通道） |
| 关联真实测试 | adoption/strict 双策略 check、package-structure-rules 45 项测试 |
| 检查时点 | 真实测试通过后 |

## 检查范围

本轮检查：

- `cachetask/` 目录条目与用途说明在目录树、SKILL.md、语言 reference、adoption 白名单四处一致；
- 三类根级任务入口（`crontask/`/`cachetask/`/`async/`）触发机制表述不重复、边界清晰；
- 新增与修改文件是否 UTF-8、中文是否无乱码；
- 字典刷新是否可重复，`PROJECT_MEMORY.md` 人类区与机器索引区是否同步；
- 知识库笔记回读一致且索引检查通过。

### 范围外说明

不迁移历史 `doc/3-实施/` 文档、不执行 Git 提交、不改动其他兄弟 skill；`utils/cache/`（Redis/Mongo 缓存读写适配）是独立概念，不属本次新增范围。

## 真实测试前置证据

`placement_catalog.py check --policy adoption`（含 `cachetask/coin_price/refresh.go` 的临时后端项目）exit 0；`check --policy strict` 同样 exit 0；package-structure-rules 45 项测试全通过（含顺手修复的 apifox 环境断言基线）；字典刷新 `generate_dictionary.py` 退出码 0；知识库 `knowledge_index.py check` 退出码 0、254 链接 0 死链。

## 6-review 结论

STYLE: PASS

本轮未发现需要修复的风格问题。`cachetask/` 目录条目与三类任务入口边界在目录树、SKILL.md、三个语言 reference、adoption 白名单四处一致，用途说明与 `utils/cache/` 技术适配边界显式区分；工作汇报目录映射补 `cachetask` 与既有 `crontask` 同表同格式；apifox 环境断言基线顺手修复；文件编码与字典刷新符合仓库既有约定。

### 完成标准

风格回归完成标准为：cachetask 目录语义四处一致、三类任务入口边界清晰、改动最小、全部文件 UTF-8、字典刷新成功、知识库索引检查通过。以上标准全部满足，判定 PASS。

## 检查清单

| 检查项 | 结论 | 依据 |
| --- | --- | --- |
| cachetask 语义四处一致 | PASS | `project-layout-v2.md`、`SKILL.md`、三个语言 reference、`placement_catalog.py` 白名单均含 `cachetask/` |
| 三类任务入口边界 | PASS | 目录树正文显式区分触发机制：时间驱动/缓存过期驱动/消息驱动 |
| 与 utils/cache 边界 | PASS | 目录树正文与知识库笔记均声明 cachetask 只承载重建逻辑、不重复实现缓存读写 |
| 最小改动 | PASS | 仅改 package-structure-rules 6 文件 + work-report 1 脚本 + 1 测试基线 + 字典，未新增 skill、未迁移历史文档 |
| 文件编码 | PASS | 新增与修改文件 UTF-8，中文无乱码 |
| 字典刷新 | PASS | `generate_dictionary.py` 退出码 0，data.js 已含"缓存任务" |
| 知识库沉淀 | PASS | 新笔记回读 2850 字节一致，`knowledge_index.py check` 0 死链 |
| 未引入无关改动 | PASS | 未新增 skill、未执行 Git 提交 |

## 问题与修复

| 序号 | 问题 | 严重度 | 修复动作 | 状态 |
| --- | --- | --- | --- | --- |
| 1 | 全量测试 2 处失败：`configuration_layout_test` 断言 `standard_environments` 仍为 `["local","test","prod"]`，而 catalog 已含 `apifox`（2026-08-21 引入的标准环境扩展） | 低（既有基线漂移，与本轮改动无关） | 断言同步为含 `apifox`，docstring 修改时间更新 | 已修复 |
| 2 | 全量测试另有 12 失败/13 错误 | 低（既有环境性问题：缺 Go 工具链、git 环境、台账断言等；失败测试文件与本轮改动无交集，package-structure-rules 45 项全通过） | 不属本轮范围，收口报告说明 | 保留 |

图片资产决策：N/A + 原因 + 证据：本轮是规则文档、脚本与测试资产改动，没有 UI、截图、原型或位图需要视觉留证。

## 执行附录

### 关键改动

- `package-structure-rules/references/project-layout-v2.md`：后端目录树加 `cachetask/` 条目 + 三类根级任务入口正文说明
- `package-structure-rules/references/{structure-general,node-python-module-layout,java-layer-layout}.md`：根级目录列表加 `cachetask/`
- `package-structure-rules/SKILL.md`：description 加"缓存任务"、核心边界第 2 条根级唯一位置加 `cachetask/`
- `package-structure-rules/scripts/placement_catalog.py`：`ADOPTION_V2_SOURCE_ROOTS["backend"]` 加 `cachetask`
- `work-report-summary-rules/scripts/generate_git_report.py`：`MODULE_LABELS` 加 `"cachetask": "缓存任务"`
- `test/package-structure-rules/configuration_layout_test.py`：`standard_environments` 断言同步 apifox（基线修复）
- 仓库级：`skill-dictionary/data.js`、`字典.md`（字典重跑）、`PROJECT_MEMORY.md`、`package-structure-rules/workbuddy-absorption-map.md`、`package-structure-rules/references/source-notes.md`
- 知识库：新建 `20-Knowledge/工程实践/cachetask缓存重建任务目录.md`，五件套笔记补双向关联

### 验证命令

- adoption：`python -B package-structure-rules/scripts/placement_catalog.py check --root <tmp> --project-kind backend --language go --policy adoption --adoption-manifest doc/1-架构/3-目录规则收敛清单.yaml` → exit 0
- strict：同上但 `--policy strict` → exit 0
- 回归：`python -B -m unittest discover -s test/package-structure-rules -p "*_test.py"` → 45 tests OK
- 字典：`python -B skill-dictionary/generate_dictionary.py` → exit 0
- 知识库：`python -B knowledge-flow/scripts/knowledge_index.py check` → exit 0

## 追踪附录

- 来源：`SRC-cachetask-20260827`（用户会话）
- 落点：`package-structure-rules`（workbuddy-absorption-map.md / source-notes.md）
- 知识库：`KNOW-20260827-cachetask-root-entry`（关联 `KNOW-20260826-cache-five-pieces`）
- 风格证据：`EVD-CACHETASK-20260827-STYLE`（本 6-review）
