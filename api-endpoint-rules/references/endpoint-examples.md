# 接口入口正反例

## 正例

### 正例 1：资源语义清晰

- `GET /orders/{id}`
- `POST /orders`
- `PATCH /orders/{id}`

### 正例 2：入口薄、业务在服务层

- handler 只接参数、调 service、返回结果。
- 复杂规则放在 service 中处理。

## 反例

### 反例 1：动作堆砌路径

- `/doCreateOrder`
- `/handleUserAction`
- 结论：不利于资源语义稳定。

### 反例 2：handler 直接承载业务中心

- handler 里写完整业务编排、状态机、落库、通知。
- 结论：入口层过重，不通过。
