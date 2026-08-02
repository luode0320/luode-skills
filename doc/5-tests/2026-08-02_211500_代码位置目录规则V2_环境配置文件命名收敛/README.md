---
schema_version: 1
doc_id: "TEST-PSR-CONFIG-001"
doc_type: "test"
source_ids: ["REQ-PSR-CONFIG-ENV-001", "CYCLE-PSR-17-001"]
status: accepted
version: "v1.0"
current_slice: "TASK-17-02..04"
updated_at: "2026-08-02"
template_version: 1
reader_level: business_general
writing_style: plain_chinese
appendix_policy: preserve_existing_or_one_terminal_appendix
---

# 环境配置文件命名收敛测试说明

结论：本轮配置目录行为测试已通过，独立后端和同仓后端的环境配置目录、文件名、策略检查与 init 边界均符合冻结规则。影响：`package-structure-rules` 现在可以识别 `config_<env>` 文件契约；范围：Catalog 查询、目录渲染、strict/adoption/legacy、init 和既有入口回归；非范围：真实项目迁移、配置加载、秘密原值扫描和外部服务；变化：新增按环境拆分的 YAML/Go embedded 命名检查与不生成动态文件的初始化边界；完成标准：正负 fixture 结果、策略退出码、只读哈希和初始化无动态文件全部通过；术语说明：embedded 指源码内保存 YAML 字符串的配置文件；验证状态：配置行为测试和两组既有回归均已通过。

## 文档信息

| 字段 | 内容 |
|---|---|
| 关联需求 | `REQ-PSR-CONFIG-ENV-001` |
| 关联周期 | `CYCLE-PSR-17-001` |
| 当前任务 | `TASK-17-02..04` |
| 可执行测试代码 | `test/package-structure-rules/configuration_layout_test.py`、`entrypoint_layout_test.py`、`project_layout_contract_test.py` |
| 测试环境 | local 工作树、Windows Python、临时目录 |
| 证据边界 | 不使用数据库、缓存、消息队列、HTTP/RPC 上游或非 local 配置 |

## 完成标准

- 配置行为测试 `6/6 OK`，既有入口回归 `5/5 OK`，目录回归 `2/2 OK`。
- strict/adoption 的非法样本失败关闭，legacy 仅告警，三种策略检查前后哈希不变。
- init 创建静态配置目录但不生成任何动态环境配置文件。
- 测试资产只位于根 `test/` ASCII 镜像路径，临时 fixture 在测试结束后清理。

## 测试资产位置

正式可执行测试位于根 `test/` 的 ASCII 镜像路径：

- `test/package-structure-rules/configuration_layout_test.py`：本轮配置行为测试，6/6 通过。
- `test/package-structure-rules/entrypoint_layout_test.py`：CYCLE-15 入口回归，5/5 通过。
- `test/package-structure-rules/project_layout_contract_test.py`：CYCLE-16 目录回归，2/2 通过。

本说明、日志和报告属于研发证据，归档在当前 `doc/5-tests/` 时间戳目录；不在 `doc/5-tests/` 存放可执行测试代码。

## 真实测试命令与结果

| 测试 ID | 精确命令 | 样本与断言 | 实际结果 |
|---|---|---|---|
| `TEST-PSR-CONFIG-001` | `python -X utf8 -B test/package-structure-rules/configuration_layout_test.py -v` | 四个 config query、目录 render、标准/扩展环境、单文件、不配对、非法文件名、错误位置、Go 旧命名、三种策略、哈希和 init | `6/6 OK` |
| `TEST-PSR-CONFIG-002` | 同上 | `config_PROD.yaml`、`.json`、`config_test_yaml.go`、嵌套文件和错误配置根必须 strict 失败 | `通过` |
| `TEST-PSR-CONFIG-003` | 同上 | `.yml`、Java embedded 扩展名兼容、缺少环境文件或跨目录配对不失败 | `通过` |
| `TEST-PSR-CONFIG-004` | 同上 | strict/adoption 退出码 `2`，legacy 退出码 `0` 且 warnings 非空，检查前后哈希不变 | `通过` |
| `TEST-PSR-CONFIG-005` | 同上 | backend/fullstack init 创建配置目录但不生成 `config_*.yaml|yml|go` | `通过` |
| `TEST-PSR-CONFIG-006` | `python -X utf8 -B test/package-structure-rules/entrypoint_layout_test.py -v`；`python -X utf8 -B test/package-structure-rules/project_layout_contract_test.py -v` | CYCLE-15 入口和 CYCLE-16 活动 doc 目录不回归 | `5/5 OK`、`2/2 OK` |

## 环境与数据边界

- 仅使用 Windows 本地 Python、仓库内 Catalog/Schema/reference 和 `tempfile.TemporaryDirectory()` 临时目录。
- 不读取、不连接、不写入数据库、缓存、消息队列、HTTP/RPC 上游或 test/prod 配置。
- fixture 内容为最小 `sample: true`，不包含密码、token、私钥、连接串或其他秘密原值。
- 每个检查样本使用进程内临时目录，测试结束后由上下文管理器清理；未迁移真实项目。

## 失败预期、清理与回滚

- 预期负向样本必须返回 strict/adoption `2`，legacy `0` 并给出 warning；结果不符合即停止本周期收口。
- `check` 前后目录哈希必须一致；哈希变化即判定发生非授权写入并停止。
- `init` 只允许创建目录和既有静态根文件，不得创建任何环境配置文件；出现动态文件即停止。
- 回滚边界仅为 CYCLE-17 当前未提交增量；不使用 destructive Git 命令，不触碰 CYCLE-15/CYCLE-16 历史资产。

## 证据登记

| 任务 | IMPL | TEST | STYLE |
|---|---|---|---|
| `TASK-17-02` | `EVD-TASK-17-02-IMPL-01` | `EVD-TASK-17-02-TEST-01` | `EVD-TASK-17-02-STYLE-01` |
| `TASK-17-03` | `EVD-TASK-17-03-IMPL-01` | `EVD-TASK-17-03-TEST-01` | `EVD-TASK-17-03-STYLE-01` |
| `TASK-17-04` | `EVD-TASK-17-04-IMPL-01` | `EVD-TASK-17-04-TEST-01` | `EVD-TASK-17-04-STYLE-01` |

## 图片资产决策

图片资产决策：N/A + 原因：本轮只验证目录、文件名、CLI JSON 和临时 fixture，不涉及 UI 或视觉验收；证据：行为测试输出、目录哈希和本文测试矩阵已覆盖关系。
