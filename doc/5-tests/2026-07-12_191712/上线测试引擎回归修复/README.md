# 上线测试引擎回归修复

本轮归档 `TASK-RT-R01`、`TASK-RT-R02`、`TASK-RT-R03` 的 R1 回归证据。所有执行均使用 local 配置语义、回环 fixture 或纯内存 mock；没有读取或连接 test、staging、pre、release、production 配置。

## R1 任务闭环

| 任务 | 实现落点 | 真实测试 | 结果 | 验收证据 |
| --- | --- | --- | --- | --- |
| `TASK-RT-R01` | `discovery.py::discover_project` 将 gRPC 去重写入 `_GRPC.finditer` 循环 | `python -X utf8 -m unittest discover -s doc/5-tests/2026-07-12_191712/project-release-test-rules/tests -p "test_discovery_regression.py" -v` | `1/1 PASS` | `EVD-TASK-RT-R01-001` |
| `TASK-RT-R02` | `runner.py::_rpc_http` 强制 local provenance，保留 `auth.py::resolve_auth` 脱敏 | `python -X utf8 -m unittest discover -s doc/5-tests/2026-07-12_180240/project-release-test-rules/tests -p "test_protocol_adapters.py" -v` | `4/4 PASS` | `EVD-TASK-RT-R02-001` |
| `TASK-RT-R03` | `generate_release_test_plan.py` 仅委派显式 `compat_*`，完整转发 `run` 参数 | `python -X utf8 -m unittest discover -s doc/5-tests/2026-07-12_180240/project-release-test-rules/tests/cli_compat -p "test_cli_contract.py" -v` | `8/8 PASS` | `EVD-TASK-RT-R03-001` |

## 真实测试与断言

### `EVD-TASK-RT-R01-001`

- 样本：普通 `.java` 文件含 `@KafkaListener`，`.proto` 无 gRPC service；使用临时目录并在测试退出时删除。
- 断言：无 gRPC match 不抛 `UnboundLocalError`，不伪造 gRPC 入口，消息监听器结果保留。
- 失败预期：异常、协议错配或入口数量漂移均为 FAIL。
- 审查：修改仅位于 `discovery.py` 循环缩进和本轮回归测试；无 adapter 契约、生产项目或环境配置变更。
- 验收：PASS。

### `EVD-TASK-RT-R02-001`

- 样本：`graphql_endpoint=https://prod.example` 的未证明来源、显式 `local_config`、显式 `config_environment=local`、local auth 引用和缺失 auth 引用。
- 断言：远程 URL 在 `urlopen` 前返回 `BLOCKED/LOCAL_CONFIG_PROVENANCE_INVALID` 且 `urlopen.assert_not_called()`；local endpoint 才进入 transport；auth 原值不进入结果。
- 失败预期：任何远程连接、错误码降级为 `LOCAL_SERVICE_UNAVAILABLE`、secret 明文均为 FAIL。
- 清理/回滚：不启动外部服务；mock/临时端口由测试释放；回滚范围仅 `_rpc_http` 与协议测试断言。
- 审查：显式 `production/test/staging` marker 无论 endpoint 名称均先阻断；缺省 marker 不把任意 URL 当作 local。
- 验收：PASS；GraphQL/RPC/JSON-RPC/SOAP 共用 RPC provenance 边界，协议测试 `4/4 PASS`。

### `EVD-TASK-RT-R03-001`

- 样本：compat handler 存在/不存在、engine 不可导入、`run --baseline-root` 及 config/inventory/plan/modules/adapters 等参数。
- 断言：旧命令不调用完整 `run_pipeline`；显式 compat handler 可观察 `compat_command` 且无 `func`；run 参数不静默丢弃；engine/dry-run 不支持时返回结构化 `PENDING`。
- 失败预期：旧输出契约丢失、调用列表为空、参数丢失或误发请求均为 FAIL。
- 清理/回滚：仅临时 mock 与 argv；无业务脚本改动，保留旧 handler 回退。
- 审查：`_invoke_engine` 仅向支持的签名传参，`**kwargs` handler 保留兼容字段；未改变旧十命令原实现。
- 验收：PASS；CLI contract `8/8 PASS`，全量引擎测试 `27/27 PASS`。

## 汇总门槛

- R1 三任务顺序 `R01 -> R02 -> R03` 已完成，未发现 P0/P1、安全或非 local 阻断。
- 语法检查：`python -X utf8 -m py_compile` 覆盖 `discovery.py`、`runner.py`、兼容入口和新增测试，PASS。
- 工作树未执行 Git commit/push；本 README 与测试资产均保留为未提交交付证据。

## C02 内核复验记录

`TASK-RT-C02-01` 沿用本轮既有 local 临时目录测试资产，目标为 IR/schema、事件追加、锁、原子替换和 replay。真实命令：

`python -X utf8 -m unittest doc/5-tests/2026-07-12_180240/project-release-test-rules/tests/test_core_engine.py -v`

结果 `7/7 PASS`。覆盖合法 IR round-trip、未知协议与缺 required field、非法事件不落盘、事件 replay、projector 异常保持旧 baseline、安全操作阻断与 local-only。实现审查未发现 P1；C02 验收证据为 `EVD-TASK-RT-C02-001`，可进入 C03。

## C03-C08 窄闭环证据索引

| 任务 | 真实测试入口 | 结果 | 证据 |
| --- | --- | --- | --- |
| `TASK-RT-C03-02` doctor execution matrix | `python -X utf8 -m unittest doc/5-tests/2026-07-12_191712/project-release-test-rules/tests/test_doctor_matrix.py -v` | `2/2 PASS` | `EVD-TASK-RT-C03-002` |
| `TASK-RT-C04-01` 参数位置 | `python -X utf8 -m unittest doc/5-tests/2026-07-12_191712/project-release-test-rules/tests/test_parameter_locations.py -v` | `2/2 PASS` | `EVD-TASK-RT-C04-001` |
| `TASK-RT-C04-02` local provider | `python -X utf8 -m unittest doc/5-tests/2026-07-12_191712/project-release-test-rules/tests/test_local_provider_resolution.py -v` | `2/2 PASS` | `EVD-TASK-RT-C04-002` |
| `TASK-RT-C05-01/02` 拓扑与失败传播 | `python -X utf8 -m unittest doc/5-tests/2026-07-12_180240/project-release-test-rules/tests/test_engine_extensions.py -v` | `5/5 PASS` | `EVD-TASK-RT-C05-001` |
| `TASK-RT-C06-01` HTTP/RPC/CLI local runtime | `python -X utf8 -m unittest doc/5-tests/2026-07-12_180240/project-release-test-rules/tests/test_local_e2e.py -v` | `3/3 PASS` | `EVD-TASK-RT-C06-001` |
| `TASK-RT-C06-02` 非 HTTP adapter 能力 | `python -X utf8 -m unittest doc/5-tests/2026-07-12_191712/project-release-test-rules/tests/test_runtime_matrix.py -v` | `4/4 PASS`（五类 local fixture；缺失/非法 fixture 明确 PENDING） | `EVD-TASK-RT-C06-002` |
| `TASK-RT-C07-01` 协议错误与 schema | `python -X utf8 -m unittest doc/5-tests/2026-07-12_191712/project-release-test-rules/tests/test_judge_protocols.py -v` | `2/2 PASS` | `EVD-TASK-RT-C07-001` |
| `TASK-RT-C07-02` 报告与基线投影 | local E2E 产物检查 | `PASS` | `EVD-TASK-RT-C07-002` |
| `TASK-RT-C08-01` v1->v2 迁移 | `python -X utf8 -m unittest doc/5-tests/2026-07-12_191712/project-release-test-rules/tests/test_migration_cli.py -v` | `2/2 PASS` | `EVD-TASK-RT-C08-001` |
| `TASK-RT-C08-02` 旧十命令/新入口兼容 | `python -X utf8 -m unittest doc/5-tests/2026-07-12_180240/project-release-test-rules/tests/cli_compat/test_cli_contract.py -v` | `8/8 PASS` | `EVD-TASK-RT-C08-002` |

说明：`TASK-RT-C08-03` 的最终 E2E、严格文档校验、skill compliance 和当前改动总审查仍属于最终收口门禁；在这些门禁完成前，不能输出“上线放行”。

## `EVD-TASK-RT-C06-002` runtime matrix 证据

- 实现落点：`project-release-test-rules/scripts/release_test_engine/adapters/__init__.py::fixture_capability/adapter_matrix_status`、`runner.py::_fixture`、`cli.py::run_doctor`。
- local fixture 契约：入口必须提供 `entrypoint.fixture_response`（兼容旧键 `fixture`），且显式声明 `status`；允许值为 `PASS`、`EXPECTED_FAIL`、`FAIL`、`PENDING`、`BLOCKED`。传输只能是 `fixture`、`in-process` 或 `in_process`，缺失/非法值不得默认 PASS。
- 真实测试：`python -X utf8 -m unittest doc/5-tests/2026-07-12_191712/project-release-test-rules/tests/test_runtime_matrix.py -v`，结果 `4/4 PASS`。
- 通过样本：gRPC、WebSocket、message、scheduler、event 各使用纯内存 local fixture，验证 `PASS` 与显式 `FAIL` 都能被 runner 保留，证据包含 `transport=fixture` 和 `execution_mode=in-process-fixture`。
- 阻断样本：无 fixture 为 `PENDING/UNSUPPORTED_ADAPTER`；缺少 `status` 为 `PENDING/FIXTURE_STATUS_MISSING`；非 in-process transport 为 `PENDING/FIXTURE_TRANSPORT_INVALID`；不会访问任何 HTTP/RPC 上游。
- 矩阵断言：doctor/adapter matrix 输出 `discovery_status`、`fixture_status`、`execution_status`、`execution_mode`、`runner`、逐入口状态和 pending 数；部分入口有 fixture 时输出 `fixture_status=partial`、`execution_status=partial`，不得聚合为 PASS。
- 兼容回归：旧协议测试 `python -X utf8 -m unittest doc/5-tests/2026-07-12_180240/project-release-test-rules/tests/test_protocol_adapters.py -v`，结果 `4/4 PASS`；当前时间戳目录全量测试 `python -X utf8 -m unittest discover -s doc/5-tests/2026-07-12_191712/project-release-test-rules/tests -p 'test_*.py' -v`，结果 `16/16 PASS`。
- 审查与边界：未修改 `report.py`；未启动 broker、scheduler、event bus 或远端服务；五类协议除显式 fixture 外仍保持 `PENDING/UNSUPPORTED_ADAPTER`，真实 runtime 依赖缺失不被伪造成 PASS。
