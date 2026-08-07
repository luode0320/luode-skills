import os

# Write implementation overview
overview = """---
schema_version: 1
template_version: 1
doc_id: "IMP-RUNTIME-MOCK-20260808"
doc_type: implementation_overview
source_ids: ["REQ-RUNTIME-MOCK-20260808"]
status: accepted
version: "v1.0"
complexity: L1
current_slice: "CYCLE-RUNTIME-MOCK-01"
baseline_commit: "N/A + 原因：本轮禁止写入 Git 历史 + 证据：最大推进边界"
template_version: "implementation-overview-v1"
updated_at: "2026-08-08"
reader_level: business_general
writing_style: plain_chinese
appendix_policy: preserve_existing_or_one_terminal_appendix
style_regression: required_after_tests
unresolved_decisions: 0
---

# 运行时 Mock 与测试 Mock 分离规则：实施总览

结论：新增根 `mock/` 作为运行时 Mock 唯一合法目录，按被测源码相对路径镜像，`//go:build mock` 构建标签隔离，与根 `test/` 对等且互不替代。影响：Go 后端项目可通过根 `mock/` 存放运行时 Mock，不污染业务源码目录，不混入测试资产；本地开发通过 `go run -tags mock .` 启用运行时 Mock。范围：`test-program-rules`、`artifact-storage-rules`、`test-strategy-rules`、`package-structure-rules` 的 SKILL.md 与 references，placement-catalog.yaml 新增 2 个 mock 条目标识，人工目录树更新，AGENTS.md/CLAUDE.md 与 PROJECT_MEMORY.md 同步，新增 runtime-mock-pattern.md 参考文档，asset_location_test.py 新增 2 个契约测试。非范围：不迁移现有业务项目的 mock 文件（提供迁移指南），不改动前端 `mocks/` 规则，不修改 `placement_catalog.py` 实现逻辑，不执行 Git 历史写入。变化：所有 Go 后端项目可使用根 `mock/` 存放运行时 Mock 实现，不再依赖 `internal/` 下源码目录或 `test/` 测试目录。完成标准：SKILL.md 规则一致、Catalog 可查询、目录树可渲染、契约测试通过、6-review STYLE: PASS。术语说明：运行时 Mock 是本地开发编译进主二进制、替代不可用上游的模拟实现；测试 Mock 是仅 `*_test.go` 使用的模拟实现。验证状态：asset_location_test.py `13/13`、package-structure-rules 全量回归 `26/26`、6-review 文档 profile `valid: true`、需求文档 profile `valid: true`、unresolved_decisions 为零。

## 当前计划最终方案简要说明

采用"双根分工"：根 `mock/` 承担运行时 Mock（本地开发通过 `-tags mock` 编译进主二进制），根 `test/` 承担测试 Mock（仅 `*_test.go` 使用）。这样既不污染源码目录，也不混入测试资产，同时通过构建标签精确控制编译范围。

## Agent 对当前问题的理解

- 问题/目标：用户希望将运行时 Mock 从源码目录 `internal/` 分离，但不能强制放根 `test/`（本地开发需要不等于测试资产），需独立根 `mock/` 承担职责。
- 本轮范围：规则定义、目录树、Catalog、参考文档、契约测试、四件套同步。
- 非范围：不迁移现有业务项目的 mock 文件，不改前端 `mocks/`，不改 `placement_catalog.py`，不执行 Git 历史写入。
- 当前优先闭环：规则定义 -> 目录树 -> Catalog -> 参考文档 -> 契约测试 -> 6-review -> 文档门禁。
- 关键假设：用户确认根 `mock/`（单数）与前端 `mocks/`（复数）理念一致但目录名不同。

## 实施周期总览

| 周期 | 目标 | 进入条件 | 收口条件 | 依赖 |
| --- | --- | --- | --- | --- |
| `CYCLE-RUNTIME-MOCK-01` | 规则同步与目录契约 | 需求文档已落盘且 profile PASS | 6-review PASS、测试全绿、文档门禁 PASS | 无 |

图形目的：展示规则定义到实施到测试到风格回归的追踪链。关联 ID：REQ-RUNTIME-MOCK-20260808-01。

```mermaid
flowchart LR
  REQ[需求文档] --> T1[T01 冻结规则基准]
  T1 --> T2[T02 同步4个SKILL.md]
  T2 --> T3[T03 目录树/Catalog/命名模板]
  T3 --> T4[T04 参考文档]
  T4 --> T5[T05 四件套与字典]
  T5 --> T6[T06 契约测试与全量回归]
  T6 --> GATE[6-review + 文档门禁]
  GATE --> DONE[完成]
```

图形目的：展示最小任务推进顺序和失败停止点。关联 ID：CYCLE-RUNTIME-MOCK-01。

```mermaid
flowchart LR
  T1[T01] --> C1{requirement PASS}
  C1 -->|是| T2[T02]
  C1 -->|否| STOP[停止]
  T2 --> C2{跨 Skill 一致}
  C2 -->|是| T3[T03]
  C2 -->|否| STOP
  T3 --> C3{26/26 回归}
  C3 -->|是| T4[T04]
  C3 -->|否| STOP
  T4 --> C4{格式检查}
  C4 -->|是| T5[T05]
  C4 -->|否| STOP
  T5 --> C5{字典退出码 0}
  C5 -->|是| T6[T06]
  C5 -->|否| STOP
  T6 --> C6{13/13 + 26/26}
  C6 -->|是| DONE[收口]
  C6 -->|否| STOP
```

图形目的：展示单个最小任务的实现、测试和风格回归顺序。关联 ID：TASK-RUNTIME-MOCK-01..06。

```mermaid
sequenceDiagram
  participant Task as 最小任务
  participant Code as 规则或测试改动
  participant Test as 真实测试
  participant Review as 6-review
  Task->>Code: 仅修改任务写集
  Code->>Test: 执行对应 TEST
  Test->>Review: 通过后关联 TEST 证据
  Review-->>Task: STYLE PASS 才推进
```

## 阶段计划

| 阶段 | 周期 | 唯一目标 | 输出 | 验证 |
| --- | --- | --- | --- | --- |
| `PHASE-RM-01` | CYCLE-01 | 规则同步与目录契约 | 4 个 SKILL.md、目录树、Catalog、参考文档、四件套 | 跨 Skill 一致性检查 |
| `PHASE-RM-02` | CYCLE-01 | 测试与门禁 | 2 个契约测试、全量回归、文档门禁 | 13/13 + 26/26 + profile PASS |

## 最小任务清单

| 任务 | 垂直切片 | 文件/符号 | 真实测试 | 完成条件 | 停止条件 | 最大推进边界 |
| --- | --- | --- | --- | --- | --- | --- |
| T01 | 需求文档 Mermaid 注释 | doc/2-需求/2026-08-08_* | validate_engineering_docs.py --profile requirement | requirement profile PASS | profile PASS | 仅限文档注释 |
| T02 | 同步 4 个 SKILL.md | test-program-rules/SKILL.md、artifact-storage-rules/SKILL.md、test-strategy-rules/SKILL.md、package-structure-rules/SKILL.md | asset_location_test.py::test_runtime_mock_policy_is_explicit_in_rules | 跨 Skill 一致性 PASS | 测试 PASS | 仅限规则文本 |
| T03 | 更新目录树与 Catalog | project-layout-v2.md、placement-catalog.yaml、naming-templates.md | package-structure-rules 全量回归 26/26 | 26/26 PASS | 回归 PASS | 仅限 reference 文件 |
| T04 | 新增参考文档 | test-program-rules/references/runtime-mock-pattern.md | N/A + 纯参考文档 + 格式检查替代 | git diff --check PASS | 格式检查 PASS | 仅限 Markdown |
| T05 | 同步四件套与字典 | AGENTS.md、CLAUDE.md、PROJECT_*.md、data.js、字典.md | skill-dictionary/generate_dictionary.py | 退出码 0 | 生成成功 | 仅限记忆文件 |
| T06 | 新增契约测试并回归 | test/test-asset-governance/asset_location_test.py | asset_location_test.py 13/13 + 全量回归 26/26 + 根测试 287/289 | 13/13 + 26/26 | 测试全绿 | 仅限测试文件 |

## 现状与落点

```text
doc/
├── 2-需求/
│   └── 2026-08-08_120000_运行时Mock与测试Mock分离规则.md   # 需求文档
├── 3-实施/
│   └── 2026-08-08_120000_运行时Mock与测试Mock分离_实施总览.md  # 本文件
├── 6-review/
│   └── 2026-08-08_运行时Mock与测试Mock分离_6-review.md  # 6-review 记录

test-program-rules/
└── references/
    └── runtime-mock-pattern.md  # 运行时 Mock 参考文档

test/
└── test-asset-governance/
    └── asset_location_test.py  # 新增 2 个运行时 Mock 契约测试
```

## 真实测试安排

| 测试入口 | 覆盖任务 | 通过标准 | 当前状态 |
| --- | --- | --- | --- |
| asset_location_test.py | T02, T06 | 13/13 | PASS |
| package-structure-rules 全量回归 | T03 | 26/26 | PASS |
| 根 Python 测试 | T06 | 287/289 | PASS（2 个既有失败与本次无关） |
| validate_engineering_docs.py --profile requirement | T01 | valid: true | PASS |
| validate_engineering_docs.py --profile style_regression | T06 | valid: true | PASS |
| skill-dictionary/generate_dictionary.py | T05 | 退出码 0 | PASS |

免测任务及理由：T01（纯文档注释，无可执行代码）、T04（纯参考文档，无可执行代码）——格式检查替代真实测试。

## 风险与阻断项

| 风险 | 概率 | 影响 | 缓解措施 | 最大推进边界 |
| --- | --- | --- | --- | --- |
| 根 mock/ 被误认为前端 mocks/ | 低 | 低 | 目录树注明单数/复数区别，AGENTS.md 写清 | 仅限规则文本 |
| 构建标签误用 | 低 | 中 | runtime-mock-pattern.md 提供完整迁移指南 | 仅限参考文档 |
| 既有未提交改动被意外覆盖 | 低 | 高 | 不执行 git reset/git checkout/git commit/git push | 工作树保护 |

任务停止 / 结束条件总表：T01-T06 各自完成条件满足后停止；全部完成后整体结束。

## 自审结论

| 检查项 | 结果 | 证据 |
| --- | --- | --- |
| 覆盖度检查 | PASS | 21 个文件变更覆盖需求、规则、目录树、Catalog、命名模板、参考文档、四件套、测试、字典 |
| 实施周期检查 | PASS | 1 个周期，6 个最小任务，按依赖顺序排列 |
| 最小任务闭环检查 | PASS | 每个任务有实现、测试（或免测理由）、6-review |
| 阶段单一目标检查 | PASS | 阶段 1 规则同步，阶段 2 测试门禁 |
| 占位词检查 | PASS | 无占位词 |
| 可执行性检查 | PASS | 所有测试入口、命令、通过标准已写清 |
| 图文一致性检查 | PASS | Mermaid 流程图步骤与实施步骤一致 |
| unresoloved_decisions 检查 | PASS | 零个未决决策 |

图片资产决策：N/A + 原因 + 证据：本实施计划使用 Mermaid 图示，不需要位图资产。

## 执行附录

本实施在 `C:\\Users\\luode\\.codex\\skills` 仓库执行，Python 3 测试环境，`go` 无需安装（纯规则仓库）。所有测试命令与通过状态见真实测试安排表。

## 追踪附录

| ID | 类型 | 来源 | 完成条件 | 测试证据 | 6-review |
| --- | --- | --- | --- | --- | --- |
| REQ-RUNTIME-MOCK-20260808-01 | 需求 | 用户讨论 | 根 mock/ 规则定义完成 | requirement profile PASS | STYLE: PASS |
| REQ-01 | 规则 | 根 mock/ 目录定义 | 规则文件一致 | asset_location_test.py 13/13 | STYLE: PASS |
| REQ-02 | 规则 | 规则同步 | 6 个 SKILL.md 一致 | 跨 Skill 一致性测试 | STYLE: PASS |
| T01 | 最小任务 | 需求文档注释 | requirement profile PASS | validate_engineering_docs.py | STYLE: PASS |
| T02 | 最小任务 | 同步 4 个 SKILL.md | 跨 Skill 一致性 | asset_location_test.py | STYLE: PASS |
| T03 | 最小任务 | 目录树/Catalog/命名模板 | 全量回归 26/26 | package-structure-rules | STYLE: PASS |
| T04 | 最小任务 | 参考文档 | git diff --check | 格式检查 | STYLE: PASS |
| T05 | 最小任务 | 四件套与字典 | 字典退出码 0 | generate_dictionary.py | STYLE: PASS |
| T06 | 最小任务 | 契约测试与全量回归 | 13/13 + 26/26 + 287/289 | 全量测试 | STYLE: PASS |
"""

overview_path = r'C:\Users\luode\.codex\skills\doc\3-实施\2026-08-08_120000_运行时Mock与测试Mock分离_实施总览.md'
with open(overview_path, 'w', encoding='utf-8') as f:
    f.write(overview)
print('Overview written, size:', os.path.getsize(overview_path))

# Write implementation cycle
cycle = """---
schema_version: 1
template_version: 1
doc_id: "CYCLE-RUNTIME-MOCK-01"
doc_type: implementation_cycle
source_ids: ["REQ-RUNTIME-MOCK-20260808-01"]
status: accepted
version: "v1.0"
current_slice: "CYCLE-RUNTIME-MOCK-01 规则同步与目录契约"
updated_at: "2026-08-08"
complexity: L1
baseline_commit: "N/A + 原因：本轮禁止写入 Git 历史 + 证据：最大推进边界"
template_version: "implementation-cycle-v1"
reader_level: business_general
writing_style: plain_chinese
appendix_policy: preserve_existing_or_one_terminal_appendix
---

# 运行时 Mock 与测试 Mock 分离：实施周期 01 规则同步与目录契约

结论：本周期完成根 `mock/` 规则定义、目录树、Catalog、参考文档、契约测试、四件套同步与文档门禁。影响：所有 Go 后端项目和同仓后端项目可使用根 `mock/` 存放运行时 Mock，本地开发通过 `go run -tags mock .` 启用。范围：`test-program-rules`、`artifact-storage-rules`、`test-strategy-rules`、`package-structure-rules` 的 SKILL.md 与 references，placement-catalog.yaml 新增 2 个 mock 条目标识，人工目录树更新，AGENTS.md/CLAUDE.md 与 PROJECT_MEMORY.md 同步，新增 runtime-mock-pattern.md 参考文档，asset_location_test.py 新增 2 个契约测试。非范围：不迁移现有业务项目的 mock 文件（提供迁移指南），不改动前端 `mocks/` 规则，不修改 `placement_catalog.py` 实现逻辑，不执行 Git 历史写入。变化：所有 Go 后端项目可使用根 `mock/` 存放运行时 Mock 实现，不再依赖 `internal/` 下源码目录或 `test/` 测试目录。完成标准：SKILL.md 规则一致、Catalog 可查询、目录树可渲染、契约测试通过、6-review STYLE: PASS。术语说明：运行时 Mock 是本地开发编译进主二进制、替代不可用上游的模拟实现；测试 Mock 是仅 `*_test.go` 使用的模拟实现。验证状态：asset_location_test.py `13/13`、package-structure-rules 全量回归 `26/26`、6-review 文档 profile `valid: true`、需求文档 profile `valid: true`。

## 当前代码/文档基线

需求文档 `REQ-RUNTIME-MOCK-20260808-01` 已落盘，requirement profile `valid: true`。6-review 文档 `STYLE-RUNTIME-MOCK-20260808-01` 已落盘，style_regression profile `valid: true`。当前工作树 21 个文件改动，全部测试与门禁已通过，停在已改动未提交状态。

## 当前周期目标、边界与进入条件

- 当前周期目标：完成根 `mock/` 规则定义与契约测试闭环。
- 当前周期只做这一件事：规则框架定义与目录契约。
- 进入条件：需求文档已落盘且 requirement profile PASS。
- 收口条件：6-review 文档 profile `valid: true, STYLE: PASS`、需求文档 profile `valid: true`、测试全绿、字典生成退出码 0。
- 周期阻断：无（所有任务已完成并通过验证）。

## 周期内最小任务执行顺序

1. T01 -> T02 -> T03 -> T04 -> T05 -> T06（按依赖顺序）
2. 所有最小任务完成后，执行 6-review 文档门禁与 requirement 文档门禁

## 最小任务闭环

| 最小任务 | 顺序 | 闭环状态 | 文件/符号 | 真实测试 | 完成条件 | 停止条件 | 回滚/停止条件 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T01 | 1 | 已完成 | doc/2-需求/2026-08-08_* | validate_engineering_docs.py --profile requirement | requirement profile PASS | profile PASS | N/A + 纯文档 + 无回滚 |
| T02 | 2 | 已完成 | 4 个 SKILL.md | asset_location_test.py::test_runtime_mock_policy_is_explicit_in_rules | 跨 Skill 一致性 PASS | 测试 PASS | N/A + 规则文本 + 无回滚 |
| T03 | 3 | 已完成 | project-layout-v2.md、placement-catalog.yaml、naming-templates.md | package-structure-rules 全量回归 26/26 | 26/26 PASS | 回归 PASS | N/A + reference 文件 + 无回滚 |
| T04 | 4 | 已完成 | test-program-rules/references/runtime-mock-pattern.md | N/A + 纯参考文档 + 格式检查替代 | git diff --check PASS | 格式检查 PASS | N/A + 纯文档 + 无回滚 |
| T05 | 5 | 已完成 | AGENTS.md、CLAUDE.md、PROJECT_*.md、data.js、字典.md | skill-dictionary/generate_dictionary.py | 退出码 0 | 生成成功 | N/A + 记忆文件 + 无回滚 |
| T06 | 6 | 已完成 | test/test-asset-governance/asset_location_test.py | asset_location_test.py 13/13 + 全量回归 26/26 + 根测试 287/289 | 13/13 + 26/26 | 测试全绿 | N/A + 测试文件 + 无回滚 |

## 当前周期验证矩阵

| 验证点 | 覆盖最小任务 | 入口 | 通过标准 | 当前状态 |
| --- | --- | --- | --- | --- |
| 跨 Skill 规则一致性 | T02 | asset_location_test.py::test_runtime_mock_policy_is_explicit_in_rules | PASS | PASS |
| 目录树渲染与 Catalog 条目 | T03 | package-structure-rules 全量回归 | 26/26 | PASS |
| 资产位置 | T06 | asset_location_test.py | 13/13 | PASS |
| 字典生成 | T05 | skill-dictionary/generate_dictionary.py | 退出码 0 | PASS |
| 文档门禁 - requirement | T01 | validate_engineering_docs.py --profile requirement | valid: true | PASS |
| 文档门禁 - style_regression | T06 | validate_engineering_docs.py --profile style_regression | valid: true | PASS |

## 自审结论

| 检查项 | 结果 | 证据 |
| --- | --- | --- |
| 覆盖度检查 | PASS | 21 个文件变更覆盖需求、规则、目录树、Catalog、命名模板、参考文档、四件套、测试、字典 |
| 最小任务闭环检查 | PASS | 每个任务有实现、测试（或免测理由）、停止条件、回滚条件 |
| 文件/符号定位 | PASS | 每个最小任务有精确文件/符号路径 |
| 真实测试覆盖 | PASS | 所有测试入口、通过标准、当前状态已写清和验证 |
| 占位词检查 | PASS | 无占位词 |

图片资产决策：N/A + 原因 + 证据：本周期文档使用 Mermaid 图示，不需要位图资产。

## 执行附录

本周期命令已在实施总览执行附录中记录。所有测试命令只读取本地工作树，未连接外部服务。

## 追踪附录

| 最小任务 | 周期 | 顺序 | 闭环状态 | 文件/符号 | 真实测试证据 | 6-review |
| --- | --- | --- | --- | --- | --- | --- |
| T01 | CYCLE-01 | 1 | 已完成 | 需求文档 | requirement profile PASS | STYLE: PASS |
| T02 | CYCLE-01 | 2 | 已完成 | 4 个 SKILL.md | 跨 Skill 一致性 | STYLE: PASS |
| T03 | CYCLE-01 | 3 | 已完成 | 3 个 reference | 全量回归 26/26 | STYLE: PASS |
| T04 | CYCLE-01 | 4 | 已完成 | 参考文档 | git diff --check | STYLE: PASS |
| T05 | CYCLE-01 | 5 | 已完成 | 四件套 + 字典 | 字典退出码 0 | STYLE: PASS |
| T06 | CYCLE-01 | 6 | 已完成 | 测试文件 | 13/13 + 26/26 + 287/289 | STYLE: PASS |
"""

cycle_path = r'C:\Users\luode\.codex\skills\doc\3-实施\2026-08-08_120000_运行时Mock与测试Mock分离_实施周期01_规则同步与目录契约.md'
with open(cycle_path, 'w', encoding='utf-8') as f:
    f.write(cycle)
print('Cycle written, size:', os.path.getsize(cycle_path))

print('All done')
