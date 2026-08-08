---
schema_version: 1
doc_id: "TEST-PSR-MOCK-UPGRADE-20260808"
doc_type: test
source_ids: ["REQ-PSR-MOCK-UPGRADE-001", "CYCLE-PSR-MOCK-UPGRADE-001"]
status: accepted
version: "v1.0"
current_slice: "runtime-mock-layout"
updated_at: "2026-08-08"
reader_level: business_general
writing_style: plain_chinese
appendix_policy: preserve_existing_or_one_terminal_appendix
---

# 运行时 Mock 目录树 Skill 升级真实测试

结论：本轮已验证 Go 运行时 Mock 的目录、selector、assembly、镜像、包名和导入边界可被 Catalog 查询并被 CLI 只读检查。影响：所有按本规则组织 Go 后端和前后端同仓后端的项目，以及执行目录检查的自动化入口。范围：`package-structure-rules` 的 reference、Catalog、Schema、CLI 与活动测试。非范围：真实业务 Mock 行为、testnet/live 连接和非 local 环境。变化：新增 `runtime_mock_layout_test.py` 5 个契约测试。完成标准：新增测试全部通过，既有目录回归保持全绿，真实项目双构建通过，字典与文档门禁通过。术语说明：`selector` 指入口选择文件，`assembly` 指 Mock 装配桥接包。验证状态：已通过。

## 文档信息

| 字段 | 内容 |
|---|---|
| 关联任务 | `TASK-1` 至 `TASK-4` |
| 测试环境 | local 工作树、Windows Python、临时目录、本地 Go 1.26 + vendor |
| 可执行测试 | `test/package-structure-rules/runtime_mock_layout_test.py` |
| 证据边界 | 仅记录脱敏命令和结果，不记录任何秘密原值 |

## 测试矩阵

| TEST | 入口 | 断言 | 失败预期 |
|---|---|---|---|
| `TEST-PSR-MOCK-UPGRADE-01` | 新测试文件 | 5/5 通过：Catalog 唯一、guide 配方、owner_skill 统一、fullstack 不扩散、strict 正例、8 类反例、adoption 分流、reference 一致性 | 任一分类不唯一、正例误报或反例漏报即失败 |
| `TEST-PSR-MOCK-UPGRADE-02` | `test/package-structure-rules` 全量回归 | 36/36 通过（31 既有 + 5 新增） | 任一既有行为回退即失败 |
| `TEST-PSR-MOCK-UPGRADE-03` | 真实项目双构建 | `go build -mod=vendor .` 与 `go build -tags mock -mod=vendor .` 均退出码 0 | 任一构建失败即失败 |
| `TEST-PSR-MOCK-UPGRADE-04` | 字典与文档门禁 | 字典退出码 0，`implemented_total` 69；requirement/implementation_cycle 文档 profile PASS | 任一机器校验失败即失败 |

## 真实测试命令

```powershell
python -X utf8 -m unittest test/package-structure-rules/runtime_mock_layout_test.py -v
python -X utf8 -m unittest discover -s test/package-structure-rules -p "*_test.py" -q
python -X utf8 package-structure-rules/scripts/placement_catalog.py check --root F:\binance-wangge-go --project-kind backend --language go --policy adoption --adoption-manifest doc/1-架构/3-目录规则收敛清单.yaml
go build -mod=vendor .
go build -tags mock -mod=vendor .
python -X utf8 skill-dictionary/generate_dictionary.py
python -X utf8 -B artifact-delivery-gate-rules/scripts/validate_engineering_docs.py --profile requirement --doc doc/2-需求/2026-08-08_REQ-PSR-MOCK-UPGRADE-001_运行时Mock目录树Skill升级.md --root F:\luode-skills
python -X utf8 -B artifact-delivery-gate-rules/scripts/validate_engineering_docs.py --profile implementation_cycle --doc doc/3-实施/2026-08-08_REQ-PSR-MOCK-UPGRADE_实施周期01_运行时Mock升级.md --root F:\luode-skills
python -X utf8 -B artifact-delivery-gate-rules/scripts/validate_engineering_docs.py --profile test --doc doc/5-tests/2026-08-08_REQ-PSR-MOCK-UPGRADE/README.md --root F:\luode-skills --strict
python -X utf8 -B artifact-delivery-gate-rules/scripts/validate_engineering_docs.py --profile style_regression --doc doc/6-review/2026-08-08_REQ-PSR-MOCK-UPGRADE_6-review.md --root F:\luode-skills --strict
```

## 本轮实测结果

| TEST | 状态 | 证据 |
|---|---|---|
| `TEST-PSR-MOCK-UPGRADE-01` | 新增测试 5/5 通过 | `EVD-TASK-1..4-TEST-01` |
| `TEST-PSR-MOCK-UPGRADE-02` | 全量回归 36/36 通过 | `EVD-TASK-2-TEST-01`、`EVD-TASK-3-TEST-01` |
| `TEST-PSR-MOCK-UPGRADE-03` | 普通/mock 双构建均通过 | `EVD-TASK-4-TEST-01` |
| `TEST-PSR-MOCK-UPGRADE-04` | 字典退出码 0，文档 profile PASS | `EVD-TASK-4-TEST-01` |

## 任务证据台账

| 任务 | IMPL | TEST | STYLE |
|---|---|---|---|
| `TASK-1` | `EVD-TASK-1-IMPL-01` | `EVD-TASK-1-TEST-01` | `EVD-TASK-1-STYLE-01` |
| `TASK-2` | `EVD-TASK-2-IMPL-01` | `EVD-TASK-2-TEST-01` | `EVD-TASK-2-STYLE-01` |
| `TASK-3` | `EVD-TASK-3-IMPL-01` | `EVD-TASK-3-TEST-01` | `EVD-TASK-3-STYLE-01` |
| `TASK-4` | `EVD-TASK-4-IMPL-01` | `EVD-TASK-4-TEST-01` | `EVD-TASK-4-STYLE-01` |

## 验证结论

四项测试均达到完成标准；未发现 Mock 目录、selector、assembly、导入边界或既有 strict/adoption 行为回归。真实项目 adoption 检查报告两个测试 Mock 文件不在既有 `test/` 遗留快照，属既有快照与新加测试文件的不一致，按计划不扩大豁免并记录阻断证据。

## 测试边界

- 本轮只使用 local 工作树、临时目录和本地 Go vendor 构建，不连接数据库、缓存、消息队列、HTTP/RPC 上游或 test/prod 环境。
- 技能仓库根目录直接执行 strict 不作为本轮证据：该根目录缺少业务项目必需 `Dockerfile`；临时 fixture 的 strict/adoption 断言已由新测试覆盖。
- 本轮不写入任何 API key、token、密码、私钥、连接串或其它秘密原值。
- 图片资产决策：N/A + 原因：本任务只验证文本规则、Catalog、Schema、CLI 和测试脚本，无界面或视觉产物 + 证据：上述测试矩阵。

## 追踪附录

| 规则变化 | TEST | 风格证据 |
|---|---|---|
| `mock/` 镜像、selector、assembly、包名与导入边界 | `TEST-PSR-MOCK-UPGRADE-01/02` | `EVD-TASK-1..4-STYLE-01` |
| 普通/mock 构建隔离 | `TEST-PSR-MOCK-UPGRADE-03` | `EVD-TASK-4-STYLE-01` |
| 目录树、Catalog、CLI 与字典一致 | `TEST-PSR-MOCK-UPGRADE-04` | `EVD-TASK-4-STYLE-01` |
