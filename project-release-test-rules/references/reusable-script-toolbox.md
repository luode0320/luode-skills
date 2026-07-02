# 可复用测试脚本工具箱规则

本文件定义 `project-release-test-rules/scripts/` 中通用脚本的职责边界和复用优先级，避免 agent 每次上线测试都临时生成同类脚本。

## 复用优先级

每次上线测试前，agent 必须先检查本 skill 的 `scripts/`：

1. 已有脚本能覆盖时，必须复用。
2. 只有通用脚本缺少稳定能力时，才允许扩展脚本。
3. 项目专属适配只能写入项目 `doc/5-tests/基线/script-adapter.yaml` 或当轮测试任务目录，不得写死进通用脚本。
4. 连续两次复用的项目适配逻辑，应抽象为通用脚本参数或插件点。
5. 禁止每轮重复生成扫描、对账、参数解析、执行、判定和报告类脚本。

## 当前通用入口

当前已存在的通用入口为 `generate_release_test_plan.py`。agent 每次上线测试前必须先执行 `--help` 检查已有子命令，已有子命令能覆盖时不得重新生成同类脚本。

| 子命令 | 职责 |
| --- | --- |
| `bootstrap-inventory` | 冷启动扫描项目接口，生成初版接口基线 |
| `reconcile-inventory` | 扫描当前接口事实并与已有基线对账 |
| `generate-plan` | 基于接口基线生成测试计划 |
| `init-release-test-task` | 初始化当轮上线测试任务目录骨架 |
| `init-baseline-assets` | 初始化 `doc/5-tests/基线/` 长期资产库 |
| `build-dependency-graph` | 根据接口基线和参数来源构建依赖图 |
| `validate-reusable-params` | 校验可复用参数状态、TTL、失效原因和复验结果 |
| `resolve-test-data` | 按参数来源规则解析可复用 / fixture / rule 参数并生成依赖追踪 |
| `update-baseline-assets` | 将本轮测试结果、参数状态和历史摘要回写基线资产 |
| `sync-interface-contract-assets` | 对账当前代码、`swag/.swag-manifest.yaml` 与 `interface-inventory.yaml`，同步 OpenAPI 字段并输出 `interface-sync-report.yaml` |

## 可选拆分脚本职责

当某个子命令变复杂、被多个项目连续复用，或需要独立测试时，才拆成同名独立脚本；拆分后仍应保持总入口可调用。

| 脚本 | 职责 |
| --- | --- |
| `build_dependency_graph.py` | 根据接口基线和参数来源构建依赖图 |
| `resolve_test_data.py` | 按参数来源规则解析请求参数并生成依赖追踪 |
| `validate_reusable_params.py` | 校验可复用参数状态、TTL、失效原因和复验结果 |
| `update_baseline_assets.py` | 将本轮测试结果、参数状态和场景结论回写基线资产 |
| `execute_api_scenarios.py` | 后续用于按依赖图执行接口场景 |
| `judge_api_response.py` | 后续用于统一响应判定 |
| `write_release_report.py` | 后续用于统一输出报告 |

## 项目适配配置

项目差异写入 `doc/5-tests/基线/script-adapter.yaml`：

```yaml
base_url_source: local_config
auth:
  provider: login
  token_path: $.data.token
response_wrapper:
  code_path: $.code
  success_values: [0, "0", true]
  data_path: $.data
masking:
  sensitive_keys: [token, password, phone, idCard]
```

通用脚本只能读取这些配置，不应写死业务系统字段。

## 脚本输出约束

- 所有脚本必须显式 UTF-8 读写。
- 所有脚本输出 JSON 或 YAML，便于后续脚本串联。
- 失败时必须输出失败阶段、失败文件和失败原因。
- 脚本不得连接 test / prod / staging 环境。
- 脚本不得把明文密钥、token、手机号、身份证号、银行卡号写入报告或基线。

## 新增脚本验收

新增或修改脚本后至少验证：

1. `--help` 可正常输出。
2. 使用最小样例输入可生成预期输出。
3. 输出文件为 UTF-8。
4. 缺少输入文件时给出明确错误。
5. 不依赖当前业务项目硬编码路径。
