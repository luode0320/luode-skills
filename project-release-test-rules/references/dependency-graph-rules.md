# 接口依赖图与参数绑定规则

本文件定义上线接口测试如何从单接口列表升级为可执行的接口依赖图，解决“目标接口参数来自另一个接口响应”的通用问题。

## 核心概念

- `provider`：能提供后续测试参数的接口，例如列表、搜索、登录、配置、详情、初始化接口。
- `consumer`：需要参数才能执行的目标接口，例如详情、提交、更新、取消、写入接口。
- `dependency edge`：consumer 的某个参数来自 provider 的响应字段。
- `scenario`：按依赖顺序组织的一组接口调用。

## dependency-graph.yaml 结构

```yaml
interfaces:
  get_order_detail:
    role: consumer
    depends_on:
      - list_orders
    consumes:
      orderId:
        from: list_orders
        param_key: orderId
    blocked_policy: BLOCKED_BY_DEPENDENCY

  list_orders:
    role: provider
    provides:
      orderId:
        response_path: $.data.items[*].id
        selector: first where status in ["created", "paid"]
```

## parameter-sources.yaml 结构

```yaml
parameters:
  orderId:
    priority:
      - reusable_param
      - upstream_api
      - local_database
      - fixture
      - rule
    providers:
      - type: reusable_param
        key: orderId
        require_revalidate: true
      - type: upstream_api
        interface: list_orders
        response_path: $.data.items[*]
        selector: first where status in ["created", "paid"]
        extract: id
      - type: local_database
        table: orders
        field: id
        selector: latest where status in ("created", "paid")
    required: true
    unresolved_policy: PARAM_UNRESOLVED
```

## 执行顺序

agent 必须按依赖图拓扑排序执行：

1. 先执行无依赖 provider。
2. 将 provider 响应按 `response_path` 与 `selector` 提取为候选参数。
3. 将候选参数绑定到 consumer 请求体。
4. consumer 执行成功后，可继续作为后续 provider。
5. 若 provider 失败，依赖它的 consumer 标记为 `BLOCKED_BY_DEPENDENCY`，不得误判为目标接口失败。
6. 若 provider 成功但未提取到必填参数，consumer 标记为 `PARAM_UNRESOLVED`。

## 多来源选择

同一个参数存在多个来源时，必须按 `priority` 顺序尝试：

1. `reusable_param`
2. `upstream_api`
3. `local_database`
4. `local_cache`
5. `fixture`
6. `rule`

只有前一来源不可用、失效或不满足 selector 时，才能继续下一来源。

## 失败归类

- `BLOCKED_BY_DEPENDENCY`：前置接口失败，目标接口未执行。
- `PARAM_UNRESOLVED`：必填参数无法解析。
- `PENDING`：缺少参数来源规则、判定规则或人工确认项。
- `FAIL`：参数已正确构造，目标接口自身失败。

## 证据要求

每次依赖解析必须写入 `dependency-trace.json`：

```yaml
target_interface: get_order_detail
param: orderId
source_type: upstream_api
source_interface: list_orders
response_file: artifacts/raw-response/list_orders.json
response_path: $.data.items[0].id
selector: first where status in ["created", "paid"]
resolved: true
```

没有依赖追踪证据的参数绑定不得作为“已准确构造参数”的证据。
