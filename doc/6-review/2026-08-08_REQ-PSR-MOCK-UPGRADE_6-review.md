---
schema_version: 1
template_version: 1
doc_id: "STYLE-PSR-MOCK-UPGRADE-20260808"
doc_type: style_regression
source_ids: ["REQ-PSR-MOCK-UPGRADE-001", "TEST-PSR-MOCK-UPGRADE-20260808"]
status: accepted
version: "v1.0"
current_slice: "completed"
updated_at: "2026-08-08"
reader_level: business_general
writing_style: plain_chinese
appendix_policy: preserve_existing_or_one_terminal_appendix
---

# 运行时 Mock 目录树 Skill 升级 6-review

结论：本轮已完成 Mock 规则改动的格式、编码、命名、目录归位、注释和可读性回归。影响：`mock/` 镜像、selector、assembly 和导入边界在规则资产中表达一致。范围：reference、Catalog、Schema、CLI、活动测试和测试证据。非范围：业务正确性、真实业务 Mock 行为、外部服务和发布放行。变化：新增 Go 运行时 Mock 专项契约和机器检查。完成标准：真实测试先通过且本记录为 `STYLE: PASS`。术语说明：STYLE 只表示格式、位置、写法和可读性回归结果。验证状态：已通过。

## 文档信息

| 字段 | 内容 |
|---|---|
| 关联测试 | `TEST-PSR-MOCK-UPGRADE-01..04` |
| 风格结果 | `STYLE: PASS` |
| 检查对象 | 规则正文、JSON Catalog/Schema、Python CLI 与契约测试、Markdown 测试证据 |

## 检查范围

- UTF-8、换行、尾随空白、JSON 可解析性和 Python 测试命名保持现有仓库口径。
- Mock 条目位于 `package-structure-rules/references/`，活动测试位于根 `test/package-structure-rules/`，测试证据位于 `doc/5-tests/`。
- `runtime-mock-layout-go.md` 与 Catalog 的 `mirror_source_root`、`required_build_tag`、`forbidden_direct_imports` 术语保持一致。
- 本轮新增 `check_runtime_mock_structure` 等 Python 函数，均具备 `[参数]`、`[返回]`、最近修改时间和本轮修改原因注释。
- N/A + 原因 + 证据：不判断业务逻辑、需求覆盖、接口运行或发布放行；真实测试证据见 `TEST-PSR-MOCK-UPGRADE-20260808`。

## 真实测试前置证据

| 测试 | 证据 |
|---|---|
| `TEST-PSR-MOCK-UPGRADE-01` | `EVD-TASK-1..4-TEST-01`：新增契约测试 5/5 |
| `TEST-PSR-MOCK-UPGRADE-02` | `EVD-TASK-2/3-TEST-01`：目录全量回归 36/36 |
| `TEST-PSR-MOCK-UPGRADE-03` | `EVD-TASK-4-TEST-01`：普通/mock 双构建通过 |
| `TEST-PSR-MOCK-UPGRADE-04` | `EVD-TASK-4-TEST-01`：字典与文档门禁 |

## 任务风格证据

| 任务 | IMPL | TEST | STYLE |
|---|---|---|---|
| `TASK-1` | `EVD-TASK-1-IMPL-01` | `EVD-TASK-1-TEST-01` | `EVD-TASK-1-STYLE-01` |
| `TASK-2` | `EVD-TASK-2-IMPL-01` | `EVD-TASK-2-TEST-01` | `EVD-TASK-2-STYLE-01` |
| `TASK-3` | `EVD-TASK-3-IMPL-01` | `EVD-TASK-3-TEST-01` | `EVD-TASK-3-STYLE-01` |
| `TASK-4` | `EVD-TASK-4-IMPL-01` | `EVD-TASK-4-TEST-01` | `EVD-TASK-4-STYLE-01` |

## 6-review 结论

STYLE: PASS

## 检查清单

| 检查项 | 结果 | 证据 |
|---|---|---|
| 格式、编码、换行和尾随空白 | PASS | `EVD-PSR-MOCK-UPGRADE-04` |
| 命名、写法、路径和目录归位 | PASS | `EVD-PSR-MOCK-UPGRADE-02` |
| 注释、可读性和规则术语一致性 | PASS | `EVD-PSR-MOCK-UPGRADE-01/04` |
| 测试资产未进入 `doc/5-tests/` | PASS | `EVD-PSR-MOCK-UPGRADE-02` |

## 问题与修复

- 已修复：strict 初版要求所有合法入口都配 selector，误伤未启用 Mock 的既有入口；现改为仅在 selector 存在或主入口已启用 Mock 时要求成对。
- 已修复：镜像检查初版要求同名源文件，误报 `mock/business/scalp/api/gateway_mock.go`；现改为校验源目录存在对应 Go 文件并读取源包名。
- 已修复：`guide --category runtime-mock` 初版漏过滤 artifact，返回全部 backend/fullstack 条目；现限定为 `artifact_kind=mock`。
- 已修复：复核发现 `SKILL.md` guide 示例代码围栏被退格符和孤立闭合标记破坏，已恢复为两个独立围栏。
- 已补齐：契约测试新增 `owner_skill` 统一、fullstack 不扩散和 Schema 必填字段断言，覆盖需求风险 1/2。
- 未发现需要新增生产逻辑、业务 Mock 实现或测试专用生产字段的问题。
- 若后续真实业务项目 Mock 行为与本规则不一致，应在业务项目按 local 配置验证，不得使用本记录替代运行验证。

图片资产决策：N/A + 原因：本风格回归只检查文本规则、目录和测试资产，不存在界面或视觉产物 + 证据：检查清单与 `EVD-PSR-MOCK-UPGRADE-01..04`。

## 追踪附录

| 来源/规则 | 测试 | 风格证据 |
|---|---|---|
| `REQ-PSR-MOCK-UPGRADE-001` 运行时 Mock 目录树升级 | `TEST-PSR-MOCK-UPGRADE-01` | `EVD-TASK-1..4-STYLE-01` |
| `mock/` 镜像、selector、assembly 与导入边界 | `TEST-PSR-MOCK-UPGRADE-01..03` | `EVD-TASK-2/3-STYLE-01` |
