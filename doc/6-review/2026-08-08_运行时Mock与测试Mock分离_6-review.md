---
schema_version: 1
template_version: 1
doc_id: "STYLE-RUNTIME-MOCK-20260808-01"
doc_type: style_regression
source_ids: ["REQ-RUNTIME-MOCK-20260808"]
status: accepted
version: "v1.0"
current_slice: "TASK-RUNTIME-MOCK-01"
updated_at: "2026-08-08 12:00:00"
reader_level: business_general
writing_style: plain_chinese
appendix_policy: preserve_existing_or_one_terminal_appendix
---

# 6-review 风格回归：运行时 Mock 与测试 Mock 分离

结论：本轮新增根 `mock/` 作为运行时 Mock 唯一合法目录，与根 `test/` 对等，`//go:build mock` 构建标签保护；影响：运行时 Mock 与测试 Mock 职责分离，互不替代，本地开发通过 `go run -tags mock .` 启用；范围：`test-program-rules`、`artifact-storage-rules`、`test-strategy-rules`、`package-structure-rules` 的 SKILL.md 与 references，placement-catalog.yaml 新增 2 个 mock 条目标识，人工目录树更新，AGENTS.md/CLAUDE.md 与 PROJECT_MEMORY.md 同步，新增 runtime-mock-pattern.md 参考文档，asset_location_test.py 新增 2 个契约测试；非范围：不迁移现有业务项目的 mock 文件（提供迁移指南），不改动前端 `mocks/` 规则，不修改 `placement_catalog.py` 实现逻辑；变化：新增 1 个 reference 文件，修改 10 个规则/配置/记忆文件，新增 2 个测试用例，Catalog 新增 2 个条目标识；完成标准：`STYLE: PASS`；术语说明：运行时 Mock 是本地开发编译进主二进制、替代不可用上游的模拟实现；测试 Mock 是仅 `*_test.go` 使用的模拟实现；验证状态：asset_location_test.py `13/13`、package-structure-rules 全量回归 `26/26`、根 Python 测试 `287/289`（2 个既有失败与本次改动无关）、字典生成正常。

## 文档信息

| 字段 | 内容 |
| --- | --- |
| 关联任务 | `TASK-RUNTIME-MOCK-01` |
| 关联真实测试 | `TEST-RUNTIME-MOCK-001` |
| 检查时点 | 真实测试通过后 |

## 检查范围

- 检查 `test-program-rules`、`artifact-storage-rules`、`test-strategy-rules`、`package-structure-rules` 的 SKILL.md 及其直接 references。
- 检查 `placement-catalog.yaml`、`project-layout-v2.md`、`naming-templates.md` 的目录事实和命名模板。
- 检查 `AGENTS.md`、`CLAUDE.md`、`PROJECT_MEMORY.md` 的项目规则同步。
- 检查 `asset_location_test.py` 的运行时 Mock 契约测试。
- 检查 UTF-8、Markdown 层级、目录落点、尾随空白和 BOM。
- 范围外：不判断业务正确性、需求覆盖率、外部服务连通性或发布放行。

## 真实测试前置证据

- 资产位置测试：`python -X utf8 -m unittest discover -s test/test-asset-governance -p asset_location_test.py -v`，13 项通过（含 2 项新增运行时 Mock 测试）。
- 包结构测试：`python -X utf8 -m unittest discover -s test/package-structure-rules -p "*_test.py" -v`，26 项通过。
- 根测试：`python -X utf8 -B test/run_python_tests.py`，287/289 项通过（2 个既有失败为 `F:\luode-skills` 路径引用丢失，与本次改动无关）。
- 字典生成：`python -X utf8 skill-dictionary/generate_dictionary.py`，退出码 0，`implemented_total` 保持 69。

## 6-review 结论

- STYLE: PASS

## 检查清单

| 检查项 | 结果 | 证据 |
| --- | --- | --- |
| UTF-8、Markdown 结构、尾随空白 | PASS | `git diff --check` |
| 目录镜像和运行时 Mock 归位 | PASS | `test_runtime_mock_is_not_treated_as_scattered_test_asset` |
| 跨 Skill 规则一致性 | PASS | `test_runtime_mock_policy_is_explicit_in_rules` |
| 包结构目录事实 | PASS | package-structure-rules 全量回归 26/26 |
| 字典生成 | PASS | 退出码 0，`implemented_total` 不变 |

## 问题与修复

N/A + 原因 + 证据：本轮没有未修复的 `STYLE: FIX_REQUIRED` 项。

图片资产决策：N/A + 原因 + 证据：本风格回归只检查文本、路径和规则文件，不需要图片资产。

## 执行附录

所有命令只读取本地工作树或临时目录；未连接数据库、缓存、消息队列、HTTP/RPC 上游；未迁移或改写历史 `doc/5-tests/` 可执行资产；未执行 Git 历史写入。

## 追踪附录

`TASK-RUNTIME-MOCK-01` -> `test-program-rules/references/runtime-mock-pattern.md` / `test/test-asset-governance/asset_location_test.py` -> `TEST-RUNTIME-MOCK-001` -> `STYLE: PASS`。
