# 微业务隔离与 JSON RPC 通信契约

## 规则定位

本文件拥有跨业务导入隔离的解释与检查流程；`package-structure-rules` 拥有 `rpc/` 的物理位置、允许扩展名、JSON 响应语义和 Catalog 查询。两者对同一规则不重复定义。

## 允许与禁止的导入

`business/A` 导入 `business/B` 时，唯一允许路径是精确的 `business/B/rpc`。`business/B/rpc/<child>` 也不允许，因为 `rpc/` 本身已经是公开包入口；其余目标域子目录均为私有层。

| 导入路径 | 结论 | 修复方式 |
|---|---|---|
| `.../business/users/rpc` | 允许 | 调用公开 JSON 字符串函数。 |
| `.../business/users/service` | 禁止 | 在 `users/rpc/` 增加真实需要的公开函数。 |
| `.../business/users/entity` | 禁止 | 返回序列化的 `Response.data`，调用方自行解析自己的私有结构。 |
| `.../business/users/util` | 禁止 | 将跨域能力收敛到 `users/rpc/`。 |
| `.../business/users/rpc/internal` | 禁止 | 把公开函数直接放在 `users/rpc/` 根。 |

`scripts/micro_business.py check` 是确定性门禁：扫描 Go import，仅对另一个真实业务域的精确 `rpc` 导入放行。它必须在 CodeGraph 审查前通过。

## JSON 通信范式

1. 调用方把业务所需参数序列化为 `requestJSON string`，只调用目标域 `rpc/` 的公开函数。
2. 目标域 `rpc/` 在自身边界解析 JSON、执行本域校验、调用自身 `service/` 等私有层。
3. 目标域把成功、解析失败、校验失败或业务失败都序列化为 JSON 字符串返回。
4. 调用方只解析统一响应 JSON，再转换为调用方自己的私有结构；不得依赖目标域实体或异常类型。

返回 JSON 采用根 `common/response.Response` 语义：

| 字段 | 含义 |
|---|---|
| `code` | 与 HTTP 语义对应的业务状态码。 |
| `status` | 是否成功完成。 |
| `message` | 不含敏感信息的结果说明。 |
| `data` | 结构化结果；无结果时为 `null`。 |

Go 示例：

```go
// internal/business/users/rpc/get_profile.go
package rpc

func GetProfile(requestJSON string) string {
    // 1. 解析 requestJSON，调用 users 域 service，并序列化统一 Response。
    return `{"code":200,"status":true,"message":"ok","data":null}`
}
```

调用方只持有 `string -> string` 的函数边界；这不是网络调用，也不建立 interface、注册或注入层。

## CodeGraph 审查闸门

目的：以实际导入节点证明确定性门禁没有漏判，并让审查者定位违规来源文件和行号。

1. 在包含 fixture 或目标项目的根执行 `codegraph sync <root>`。
2. 对每个目标域执行 `codegraph query -p <root> --kind import --limit 1000 --json "<module>/business/<target>"`。
3. 合规证据必须显示调用文件导入精确 `business/<target>/rpc`。
4. 违规证据必须显示调用文件导入 `service`、`entity`、`util` 或其他私有路径；审查与验收均失败。
5. CodeGraph 只提供可追溯的导入证据；允许路径的确定性裁决仍由 `micro_business.py check` 负责。

## 公共例外和 global 边界

- 可直接跨域使用的公共结构仅为根 `common/request`、`response`、`constant`、`error`、`validation`。
- `global/` 只暴露配置、日志、数据库连接、技术客户端等已装配的非业务运行引用。
- `global/` 不保存、传递或缓存任何业务实体、业务列表、业务状态和可变业务缓存；这些数据不能绕过 `rpc/` 流通。
