# 接口入口正反例

## 正例

### 正例 1：路径语义清晰，使用 POST + JSON

- `POST /orders/get` - 获取单个订单，JSON body 传订单 ID
- `POST /orders/list` - 获取订单列表，JSON body 传分页和筛选条件
- `POST /orders/add` - 新增订单，JSON body 传订单信息
- `POST /orders/update` - 更新订单，JSON body 传订单更新信息
- `POST /orders/del` - 删除订单，JSON body 传订单 ID

### 正例 2：入口薄、业务在服务层

- controller 只接参数、调 service、返回结果。
- 复杂规则放在 service 中处理。
- 使用 `internal/controller`、`internal/router`，不使用 handler。

### 正例 3：完整目录结构参考 package-structure-rules

```
项目根目录/
├── internal/
│   ├── router/       # 路由注册
│   ├── controller/   # 控制器（不使用 handler）
│   ├── service/      # 业务逻辑
│   └── entity/       # API 结构体
├── common/
│   ├── model/        # 数据库模型
│   └── repository/   # 数据访问
└── ...
```

### 正例 4：Go 路由批量注册使用代码块收口

```go
// 4. 最后注册订单业务路由。
{
	// /orders/add 建单接口。
	serviceGroup.POST("/orders/add", controllers.orderController.CreateOrder)
	// /orders/get 查单接口。
	serviceGroup.POST("/orders/get", controllers.orderController.GetOrder)
}
```

## 反例

### 反例 1：使用了非 POST 请求类型

- `GET /orders/{id}`
- `PUT /orders/{id}`
- `PATCH /orders/{id}`
- `DELETE /orders/{id}`
- 结论：必须统一使用 POST 请求。

### 反例 2：路径中没有明确操作类型

- `POST /orders`
- `POST /users`
- 结论：必须在路径中明确操作类型，如 `/orders/add`、`/orders/get`。

### 反例 3：controller 直接承载业务中心

- controller 里写完整业务编排、状态机、落库、通知。
- 结论：入口层过重，不通过。

### 反例 4：使用了 handler 包名

- `handler/` 目录
- `internal/handler/` 目录
- 结论：必须使用 `internal/controller`，不使用 handler。

### 反例 5：动作堆砌路径，资源语义不清

- `/doCreateOrder`
- `/handleUserAction`
- 结论：不利于资源语义稳定，应使用 `/orders/add`、`/users/update` 等格式。

### 反例 6：Go 路由批量注册未用代码块

```go
// 4. 最后注册订单业务路由。
// /orders/add 建单接口。
serviceGroup.POST("/orders/add", controllers.orderController.CreateOrder)
// /orders/get 查单接口。
serviceGroup.POST("/orders/get", controllers.orderController.GetOrder)
```

- 结论：批量路由注册应使用代码块 `{ ... }` 收口，避免步骤边界不清。
