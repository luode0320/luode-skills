# 机器索引区 Schema

## 目标

定义 `PROJECT_MEMORY.md` 底部 `## 机器索引区` 的最小结构、字段约束和扩展边界。

## 最小骨架

```yaml
version: 1
entities: []
relations: []
evidence: []
contexts: []
lifecycle:
  active: []
  deprecated: []
  stale: []
  conflicted: []
  retired: []
retrieval_hints:
  aliases: {}
  scopes: {}
  sources: {}
extensions:
  external_refs: []
  retrieval_provider: ""
  vector_doc_id: ""
  graph_node_id: ""
```

## 字段说明

### `version`

- 类型: `number`
- 含义: 当前机器索引区结构版本。
- 规则: 当前固定为 `1`。

### `entities`

- 类型: `list`
- 含义: 结构化长期记忆实体列表。
- 主键建议: `entity_id`

单个实体建议字段：

```yaml
- entity_id: term.active-user
  name: 活跃用户
  type: 指标
  aliases:
    - 登录用户
    - active user
  definition: 按登录行为统计的活跃用户数
  scope: 日报
  status: active
  evidence_ids:
    - code.user-service.count-active-users
  context_ids:
    - report.daily
  updated_at: 2026-07-03
```

### `relations`

- 类型: `list`
- 含义: 实体之间的结构化连接。

单条关系建议字段：

```yaml
- relation_id: rel.active-user.from-login-event
  type: derived_from
  from: term.active-user
  to: event.user-login
  evidence_ids:
    - code.user-service.count-active-users
  status: active
```

### `evidence`

- 类型: `list`
- 含义: 支撑某条记忆的真实来源。

单条证据建议字段：

```yaml
- evidence_id: code.user-service.count-active-users
  type: code
  source: UserService.CountActiveUsers
  path: internal/service/user_service.go
  note: 活跃用户统计入口
```

### `contexts`

- 类型: `list`
- 含义: 事实适用的业务范围、模块、流程、阶段或环境。

单条上下文建议字段：

```yaml
- context_id: report.daily
  type: report
  name: 日报
  note: 适用于日报统计口径
```

### `lifecycle`

- 类型: `object`
- 含义: 不同生命周期状态下的实体或关系索引。
- 固定键:
  - `active`
  - `deprecated`
  - `stale`
  - `conflicted`
  - `retired`

### `retrieval_hints`

- 类型: `object`
- 含义: 检索辅助索引。
- 推荐子键:
  - `aliases`
  - `scopes`
  - `sources`

### `extensions`

- 类型: `object`
- 含义: 为未来外部记忆系统预留的扩展字段。
- 当前仅预留，不作为本轮运行依赖。

## 约束

1. 不得把机器索引区拆成第二个主文件。
2. 不得使用自由文本替代结构化字段。
3. `entity_id`、`relation_id`、`evidence_id`、`context_id` 应在本文件内稳定唯一。
4. 机器索引区更新必须幂等。
5. 旧正文可暂不全量迁移，但新增或修订事实应优先进入机器索引区。
