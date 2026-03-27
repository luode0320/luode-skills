# 请求参数正反例

## 正例

### 正例 1：path 定位资源

- `GET /orders/{id}`
- `id` 放 path。

### 正例 2：query 做筛选

- `GET /orders?page=1&status=paid`
- 分页和筛选放 query。

### 正例 3：body 承载主体输入

- `POST /orders`
- 创建订单主要字段放 body。

## 反例

### 反例 1：把筛选条件塞进 path

- `GET /orders/status/paid/page/1`
- 结论：语义不稳定，不推荐。

### 反例 2：把复杂业务规则写进参数校验

- 参数校验阶段直接判断多表业务状态。
- 结论：越界，应回业务层。
