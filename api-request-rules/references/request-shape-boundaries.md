# 请求结构边界

## 用途

用于统一 JSON body 和 DTO 在接口中的职责。

**重要：必须以 `api-endpoint-rules` 为基准，只使用 POST 请求，所有请求参数必须通过 JSON body 传递；不使用 path 参数、query 参数。**

## 铁律：只使用 JSON body

- **不使用 path 参数**：不要在 URL 路径中传递参数，如 `/orders/{id}`。
- **不使用 query 参数**：不要在 URL 查询字符串中传递参数，如 `/orders?page=1&status=paid`。
- **只使用 JSON body**：所有请求参数统一放在 POST 请求的 JSON body 中。
- **统一在 controller 中使用 ShouldBindJSON 进行参数绑定和错误处理**。

## 常见边界

- `JSON body`
  所有请求参数（包括资源定位、筛选条件、分页、排序、主体输入载荷等）统一放在 JSON body 中。
- `DTO`
  适合作为请求层稳定输入模型，不直接暴露内部持久化模型。请求结构体建议放在 `internal/entity` 包下（参考 package-structure-rules）。

## Controller 参数绑定标准写法

```go
var req request.ReqSetBlacklistEnabled
err := c.ShouldBindJSON(&req)
if err != nil {
    http.AppReturn(c, false, err.Error(), nil)
    return
}
```

## 原则

- 所有参数统一放 JSON body。
- DTO 服务于接口契约，不服务于偷懒复用内部结构。
- 请求结构体建议放在 `internal/entity` 包下（参考 package-structure-rules）。
- 统一使用 ShouldBindJSON 进行参数绑定，绑定失败时统一返回错误。
