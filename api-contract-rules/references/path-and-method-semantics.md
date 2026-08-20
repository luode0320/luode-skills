# 路径命名与 HTTP 语义

## 用途

用于统一路径命名、资源表达和强制使用 POST 方法。

## 铁律：强制使用 POST + JSON

- **所有 API 接口强制使用 POST 请求**，不允许使用 GET、PATCH、PUT、DELETE 等其他请求类型。
- **所有 API 接口使用 JSON 作为 request body**。
- **接口名称要语义清晰、类型清楚**，因为统一使用 POST，必须在路径名称上区分操作类型。

## 路径原则

- 路径格式：`/{资源名}/{操作类型}`
- 资源名使用复数形式，如 `orders`、`users`、`products`
- 操作类型使用清晰的动词，如 `get`、`add`、`del`、`update`、`list`、`query` 等
- 路径层级应反映资源关系，不应反映内部实现细节
- 能用资源 + 操作类型表达的，不额外塞动词

## 路径命名示例

### 查询类操作
- `POST /orders/get` - 获取单个订单
- `POST /orders/list` - 获取订单列表
- `POST /orders/query` - 查询订单（带复杂条件）

### 新增类操作
- `POST /orders/add` - 新增订单
- `POST /orders/create` - 创建订单

### 删除类操作
- `POST /orders/del` - 删除订单
- `POST /orders/delete` - 删除订单（完整拼写）

### 修改类操作
- `POST /orders/update` - 更新订单
- `POST /orders/edit` - 编辑订单

### 其他操作
- `POST /orders/export` - 导出订单
- `POST /orders/import` - 导入订单
- `POST /orders/submit` - 提交订单
- `POST /orders/approve` - 审批订单

## 禁用请求类型

- ❌ `GET /orders/{id}` - 必须使用 `POST /orders/get`
- ❌ `POST /orders` - 必须在路径中明确操作类型，如 `POST /orders/add`
- ❌ `PUT /orders/{id}` - 必须使用 `POST /orders/update`
- ❌ `PATCH /orders/{id}` - 必须使用 `POST /orders/update`
- ❌ `DELETE /orders/{id}` - 必须使用 `POST /orders/del`

## 提醒

- 所有操作都通过 POST 完成，在路径中明确操作类型。
- 语义不清时先澄清资源对象和动作，再命名路径。
- 路径名称要简洁明了，避免过长。
