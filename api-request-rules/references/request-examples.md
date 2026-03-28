# 请求参数正反例

## 正例

### 正例 1：只使用 JSON body，不使用 path/query 参数

```go
// POST /orders/get
// JSON body:
// {
//   "orderId": "12345"
// }
```

### 正例 2：Controller 中使用 ShouldBindJSON 标准写法

```go
var req request.ReqSetBlacklistEnabled
err := c.ShouldBindJSON(&req)
if err != nil {
    http.AppReturn(c, false, err.Error(), nil)
    return
}
```

### 正例 3：请求结构体放在 internal/entity 包下（参考 package-structure-rules）

```go
// internal/entity/order.go
package entity

type ReqGetOrder struct {
    OrderID string `json:"orderId" binding:"required"` // 订单 ID
}

type ReqAddOrder struct {
    UserID  string `json:"userId" binding:"required"`  // 用户 ID
    ProductID string `json:"productId" binding:"required"` // 商品 ID
    Quantity int `json:"quantity" binding:"required,min=1"` // 数量
}
```

### 正例 4：所有参数都在 JSON body 中

```go
// POST /orders/list
// JSON body:
// {
//   "page": 1,
//   "pageSize": 20,
//   "status": "paid",
//   "startTime": "2026-03-01 00:00:00",
//   "endTime": "2026-03-31 23:59:59"
// }
```

## 反例

### 反例 1：使用了 path 参数

```go
// GET /orders/{id}
```

结论：必须使用 POST + JSON body，如 `POST /orders/get`，body 中传 `{"orderId": "12345"}`。

### 反例 2：使用了 query 参数

```go
// GET /orders?page=1&status=paid
```

结论：必须使用 POST + JSON body，如 `POST /orders/list`，body 中传 `{"page": 1, "status": "paid"}`。

### 反例 3：Controller 中没有使用 ShouldBindJSON

```go
// ❌ 错误写法
orderId := c.Query("orderId")
// 或
orderId := c.Param("id")
```

结论：必须使用 ShouldBindJSON 绑定 JSON body 参数。

### 反例 4：ShouldBindJSON 绑定失败没有统一处理

```go
// ❌ 错误写法
var req request.ReqSetBlacklistEnabled
err := c.ShouldBindJSON(&req)
// 没有处理 err，直接继续执行
```

结论：ShouldBindJSON 绑定失败时必须统一返回错误，例如：

```go
var req request.ReqSetBlacklistEnabled
err := c.ShouldBindJSON(&req)
if err != nil {
    http.AppReturn(c, false, err.Error(), nil)
    return
}
```

### 反例 5：把复杂业务规则写进参数校验

```go
// ❌ 错误：参数校验阶段直接判断多表业务状态
```

结论：越界，应回业务层。
