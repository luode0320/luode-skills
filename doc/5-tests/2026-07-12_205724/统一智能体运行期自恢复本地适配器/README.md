# 统一智能体运行期自恢复本地适配器测试

## 测试目的

在不连接 MCP、插件、宿主或任何外部服务的前提下，用进程内 `local adapter fixture` 驱动现有 `recovery_state.py` 与 `RecoveryEngine`，验证能力声明、恢复动作边界、单飞锁、幂等性安全、检查点 TTL/损坏拒绝，以及 L5 续接成功和缺少 L5 时的降级结论。

## 测试对象与资产

- 规则对象：`agent-runtime-recovery-rules/SKILL.md`
- 契约对象：`agent-runtime-recovery-rules/references/adapter-contract.schema.json`
- 状态原语：`agent-runtime-recovery-rules/scripts/recovery_state.py`
- 检查点校验：`recovery_state.read_checkpoint`
- 恢复编排器：`agent-runtime-recovery-rules/scripts/recovery_engine.py::RecoveryEngine`
- 真实测试入口：`../agent-runtime-recovery-rules/test_recovery_engine_fixture.py`
- 本 README 所在中文说明目录只保留本文件；fixture 与 unittest 均在同一时间戳根目录的 ASCII 目录中。

## 执行前置条件

- Python 3 标准库可用；测试脚本通过 `importlib` 加载仓库内状态原语。
- 仅使用进程内对象和系统临时目录；不读取 `.env`、`config_test*` 或其他外部连接配置。
- 不启动端口、不调用 MCP、不重载插件、不重启宿主、不写入业务数据。

## 执行方式

```powershell
python -X utf8 doc/5-tests/2026-07-12_205724/agent-runtime-recovery-rules/test_recovery_engine_fixture.py
```

可选语法检查（不能替代上面的真实测试）：

```powershell
python -X utf8 -m py_compile agent-runtime-recovery-rules/scripts/recovery_state.py agent-runtime-recovery-rules/scripts/recovery_engine.py doc/5-tests/2026-07-12_205724/agent-runtime-recovery-rules/test_recovery_engine_fixture.py
```

## 覆盖范围与断言

| 场景 | local fixture 输入 | 关键断言 |
| --- | --- | --- |
| L0 | `local-observer` | 状态原语流程只探针并 `manual_handoff`；`RecoveryEngine` 因能力等级不足返回 `blocked/probe_capability_missing` |
| L2 | `local-transport` | 仅 `reconnect -> wait_ready`，不调用 `reload` 或 `restart` |
| L3 | `local-plugin` | 仅 `reload -> wait_ready`，不调用 `restart` |
| L4 | `local-host` | 仅 `restart -> wait_ready`，恢复后不宣称任务续接 |
| single-flight | 同一检查点先后 claim 两个 recovery id | 第二个 claim 在锁 TTL 内抛出 `RuntimeError`，释放后可重新 claim |
| non-idempotent | L2 组件标记 `non_idempotent` | 不执行 reconnect/reload/restart，直接 `manual_handoff` |
| 缺少 L5 | L4 组件要求 `resume` | 状态原语要求续接时为 `blocked`；`RecoveryEngine` 工具恢复后为 `manual_handoff`，均不调用不存在的 `resume` |
| L5 成功 | `local-l5`，原成功标准已验证 | `checkpoint -> resume` 后进入 `resumed` |
| L5 未验证 | `local-l5`，原成功标准未验证 | 不得宣称续接，进入 `manual_handoff` |
| 过期检查点 | `ttl_seconds=1` 后读取/claim | 两个入口均抛出 `checkpoint_expired` |
| 损坏检查点 | 非 JSON 内容 | 读取/claim 均抛出 `checkpoint_invalid` |
| scope 越权 | `local-transport` 使用其他组件 scope | `blocked/component_scope_mismatch`，不调用 adapter |
| local-only | 所有 scope 和 entrypoint | 仅 `local` provenance 和 local fixture 引用，拒绝 test/prod/staging 等环境片段 |

引擎入口测试直接构造 `RecoveryRequest` 并调用 `RecoveryEngine.recover`，覆盖 L2/L3/L4、L0 未声明可操作能力、`non_idempotent`、缺少 L5 resume hook、L5 成功/未验证和单飞检查点；同时保留状态原语层测试，避免只通过静态文本断言。

## 清理、回滚与停止条件

- 每个用例使用 `TemporaryDirectory`，检查点、锁和动作日志在用例结束时自动清理。
- 测试不修改生产规则、安装配置、MCP 配置或业务数据；回滚边界仅为本轮新增测试资产。
- 任一断言失败、出现未声明动作、出现非 local 引用或临时目录无法清理时，测试轮次判定为失败并停止，不切换到外部环境。

## 验证结论

已通过：`python -X utf8 doc/5-tests/2026-07-12_205724/agent-runtime-recovery-rules/test_recovery_engine_fixture.py`，退出码 `0`，共 `19` 个用例全部通过；`py_compile`（含 `recovery_engine.py`）退出码 `0`。该 fixture 证明统一协议在 local 进程内的动作与阻断边界；本地 L5 仅为受控 stub，不代表任意第三方平台已提供可用 lifecycle adapter。

## 未覆盖项

- 真实第三方平台插件重载、宿主重启 API、跨进程锁竞争和外部 L5 resume token：当前没有受管平台 adapter，不使用外部服务补证据。
