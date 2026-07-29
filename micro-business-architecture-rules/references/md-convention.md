# 微业务 Markdown 规范

## 文档职责

微业务的说明文档只帮助定位业务域、公开 RPC 和跨域关系；实际目录与通信契约以 `package-structure-rules` 为准。文档落在业务代码目录，不替代 `doc/` 研发产物。

| 文档 | 落点 | 职责 |
|---|---|---|
| 业务域 README | `<source-root>/business/<domain>/README.md` | 说明本域职责、私有边界、对外 RPC 与依赖的其他域 RPC。 |
| 全局业务索引 | `<source-root>/business/README.md` | 列出业务域、职责、状态和 README 链接，并登记真实 RPC 调用关系。 |

不再维护根 `contract/README.md` 或公共接口契约清单。跨域能力的权威入口是被调用业务域自身的 `rpc/`。

## 业务域 README 必填字段

| 字段 | 内容要求 |
|---|---|
| 业务职责 | 说明本域负责的核心能力。 |
| 边界 | 分别说明本域负责与不负责的事项。 |
| 目录结构 | 按 `package-structure-rules` 列出本域实际子目录。 |
| 对外 RPC | 列出 `rpc/<operation>.<ext>`、JSON 请求说明、JSON 响应说明和调用方业务；无调用方时写 `N/A + 原因`。 |
| 依赖的其他业务 RPC | 只列目标域 `rpc/` 公开函数，禁止写私有层路径。 |
| 私有数据入口 | 指向本域 `entity/`、`service/` 等私有实现，明确其他业务不得引用。 |
| 关键链路 | 描述入口、本域处理、必要 RPC 调用与响应解析。 |

## 全局业务索引

业务索引至少有两张表：业务清单和真实 RPC 关系。后者只登记已经存在的跨域调用，不为未来需要预建目录或函数。

```markdown
| 业务域 | 一句话职责 | 状态 | README |
|---|---|---|---|
| orders | 订单业务 | 活跃 | [orders](./orders/README.md) |
| users | 用户资料业务 | 活跃 | [users](./users/README.md) |

| 调用方 | 目标业务 | RPC 函数 | 请求与响应 | 用途 |
|---|---|---|---|---|
| orders | users | `rpc.GetProfile(string) string` | JSON 字符串 / Response JSON | 查询用户资料 |
```

## 维护规则

- 新增业务域时必须建立该域 README，并更新全局业务索引。
- 新增公开 RPC 或调用关系时，必须更新目标域 README、调用方 README 和全局业务索引的 RPC 关系表。
- 移除最后一个调用方时，可以删除无用 `rpc/`，并从三处文档同步移除。
- 文档不得把目标业务的实体、服务、私有常量或异常类型写成跨域可引用能力。
