# 上线测试基线资产库规则

本文件定义每个业务项目在 `doc/5-tests/基线/` 下长期维护哪些上线测试资产，以及这些资产如何在多次上线测试之间持续复用、复验和更新。

## 基线目录结构

每个项目的基线目录固定为 `doc/5-tests/基线/`，推荐包含：

```text
doc/5-tests/基线/
  interface-inventory.yaml
  dependency-graph.yaml
  parameter-sources.yaml
  reusable-params.yaml
  scenario-catalog.yaml
  script-adapter.yaml
  execution-history.yaml
  baseline-change-log.md
  README.md
```

## 资产职责

| 文件 | 职责 |
| --- | --- |
| `interface-inventory.yaml` | 接口清单、请求响应契约、风险等级、最近扫描和最近测试结论 |
| `dependency-graph.yaml` | 接口之间的执行顺序、provider / consumer 关系、参数依赖边 |
| `parameter-sources.yaml` | 每个请求参数的候选来源、提取路径、选择规则、兜底策略 |
| `reusable-params.yaml` | 已验证通过且可复用的参数样本、复验状态、失效原因 |
| `scenario-catalog.yaml` | 已验证可复用的端到端接口场景和步骤链路 |
| `script-adapter.yaml` | 当前项目对通用脚本的配置适配，例如 base_url、响应包装、鉴权来源 |
| `execution-history.yaml` | 历次上线测试的摘要、结论、失败类型和基线变更摘要 |
| `baseline-change-log.md` | 人可读的基线变更记录 |
| `README.md` | 基线目录维护说明和敏感信息约束 |

## 可复用参数生命周期

`reusable-params.yaml` 中的每条参数样本必须有生命周期状态：

- `candidate`：刚发现，还没有稳定复验。
- `reusable`：最近测试通过，可优先复用。
- `stale`：超过有效期，或接口 schema / 依赖规则变化，需要复验。
- `invalid`：最近复验失败，不得直接复用。
- `quarantined`：失效原因不明确，暂时隔离。
- `retired`：接口、字段或业务规则已经废弃。

推荐结构：

```yaml
params:
  orderId:
    - value_masked: "ord_***"
      value_ref: "local-secure-reference-or-artifact-path"
      source_type: upstream_api
      source_interface: list_orders
      source_response_path: $.data.items[0].id
      first_verified_at: "2026-07-02 16:30:00"
      last_verified_at: "2026-07-02 16:45:00"
      last_success_interface: get_order_detail
      success_count: 3
      fail_count: 0
      status: reusable
      ttl: 7d
      invalidation_reason: ""
```

## 复用前检查

agent 构造请求参数时必须先查 `reusable-params.yaml`，但不能无条件信任历史值：

1. 状态为 `reusable` 且未过期的参数可优先候选。
2. P0 / P1 接口、写接口、状态敏感接口在复用前必须做轻量复验。
3. 复验通过时更新 `last_verified_at` 与 `success_count`。
4. 复验失败时更新 `fail_count`、`last_failed_at`、`failed_interface`、`failure_type` 和 `invalidation_reason`，并按规则转为 `stale`、`invalid` 或 `quarantined`。
5. 失效参数不得继续作为后续接口参数来源。

## 失效类型

失效原因必须归一到以下类型之一：

- `not_found`：数据不存在。
- `expired`：token、订单、任务、临时凭证或会话过期。
- `state_changed`：状态变化，不再满足 selector。
- `permission_denied`：鉴权或权限变化。
- `schema_changed`：字段结构变化。
- `business_rule_changed`：业务规则变化。
- `environment_blocked`：local 环境、代理、服务或依赖不可用。
- `unknown`：原因不明，进入隔离。

## 持续更新规则

每次上线测试完成后必须回写基线资产：

1. 新发现接口回写 `interface-inventory.yaml`。
2. 新发现参数来源回写 `parameter-sources.yaml`。
3. 新发现依赖关系回写 `dependency-graph.yaml`。
4. 新跑通参数回写 `reusable-params.yaml`。
5. 新跑通链路回写 `scenario-catalog.yaml`。
6. 本轮摘要回写 `execution-history.yaml`。
7. 人可读变化写入 `baseline-change-log.md`。

## 安全约束

- 禁止保存明文 token、密码、手机号、身份证号、银行卡号、密钥和生产连接串。
- 禁止保存 test / prod / staging 等非 local 环境连接信息。
- 可复用参数必须脱敏；真实值只能通过本地安全引用、当前测试产物或 local 环境重新解析获得。
- 自动回写前必须做 YAML 结构校验，避免污染基线资产。
