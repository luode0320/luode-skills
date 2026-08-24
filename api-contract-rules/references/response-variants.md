# 响应变体规则

## 用途

用于处理错误响应、分页结构、兼容字段和版本字段。

## 铁律：成功响应和错误响应都必须包含的四个字段

**成功响应和错误响应都必须包含以下四个字段：**

1. **code** - 状态码/错误码（整型）
2. **status** - 状态/错误状态（布尔值或字符串）
3. **message** - 消息/错误消息（字符串）
4. **data** - 数据/返回数据（对象或 null）

## 错误响应标准格式

```json
{
  "code": 400,
  "status": false,
  "message": "参数错误：orderId 不能为空",
  "data": null
}
```

或者使用字符串 status：

```json
{
  "code": 400,
  "status": "error",
  "message": "参数错误：orderId 不能为空",
  "data": null
}
```

## 错误响应示例

### 参数错误
```json
{
  "code": 400,
  "status": false,
  "message": "参数错误：orderId 不能为空",
  "data": null
}
```

### 未授权
```json
{
  "code": 401,
  "status": false,
  "message": "未授权，请先登录",
  "data": null
}
```

### 禁止访问
```json
{
  "code": 403,
  "status": false,
  "message": "无权限访问该资源",
  "data": null
}
```

### 资源不存在
```json
{
  "code": 404,
  "status": false,
  "message": "订单不存在",
  "data": null
}
```

### 服务器错误
```json
{
  "code": 500,
  "status": false,
  "message": "服务器内部错误，请稍后重试",
  "data": null
}
```

### 错误响应带数据（可选）
如果需要返回错误相关的详细信息，可以在 data 字段中提供：

```json
{
  "code": 400,
  "status": false,
  "message": "参数校验失败",
  "data": {
    "fieldErrors": [
      {
        "field": "orderId",
        "message": "订单ID不能为空"
      },
      {
        "field": "quantity",
        "message": "数量必须大于0"
      }
    ]
  }
}
```

## 业务错误码示例

建议使用规范的业务错误码，例如：

- `200` - 成功
- `400` - 参数错误
- `401` - 未授权
- `403` - 禁止访问
- `404` - 资源不存在
- `500` - 服务器错误
- `10001` - 用户已存在
- `10002` - 用户不存在
- `20001` - 订单已支付
- `20002` - 订单已取消

## HTTP 状态码语义补充

本地响应以业务码（code）为主、成功统一 `200` + 四字段表达，不引入 201/204 语义。以下状态码用于本地确有语义的场景，与错误响应四字段共存：

- `409` Conflict - 重复条目或状态冲突（如订单已支付再取消、用户名已存在），data 可携带冲突详情
- `422` Unprocessable Entity - JSON 合法但语义非法（如年龄越界、关联对象不存在），data.fieldErrors 携带字段级错误
- `429` Too Many Requests - 触发限流，配合 `Retry-After` 响应头（见「限流响应」）
- `503` Service Unavailable - 服务临时不可用（如依赖下游故障），配合 `Retry-After` 响应头

业务错误码映射示例（补充）：

- `409` - 状态冲突
- `422` - 语义校验失败
- `429` - 请求过频
- `503` - 服务暂不可用

## 分页响应

offset 分页（page/pageSize）的标准响应格式与字段说明以 `response-shape-baseline.md` 为单一权威，此处不重复定义；本节只定义分页变体与选择策略。

### 分页变体：cursor（游标）分页

当数据集大（万级及以上）或并发写入频繁导致 offset 分页不稳定时，使用 cursor 分页。本地强制 POST + JSON body，cursor 与 limit 均放 body，不使用 query 参数。

请求示例：

```json
{
  "cursor": "eyJpZCI6MTIzfQ",
  "limit": 20
}
```

响应示例（data.pagination 携带 nextCursor）：

```json
{
  "code": 200,
  "status": true,
  "message": "查询成功",
  "data": {
    "list": [],
    "pagination": {
      "nextCursor": "eyJpZCI6MTQzfQ",
      "hasNext": true
    }
  }
}
```

### offset 与 cursor 选择矩阵

| 场景 | 分页方式 |
|---|---|
| 后台管理、小数据集（< 1 万条）、前端期望页码跳转 | offset（page/pageSize） |
| 无限滚动、feed、大数据集（万级及以上） | cursor |
| 并发写入频繁、要求结果稳定 | cursor |

### cursor 分页实现注意

- cursor 对客户端不透明：由服务端编码/解码，禁止客户端自行拼装。
- 服务端以「游标位置 + limit+1 预取」判断 hasNext，避免多查一次。

## 兼容字段与版本化策略

### 兼容字段

- 兼容字段应有明确保留理由，不要长期堆积。
- 版本字段只在确有版本演进需要时引入，不为"以后可能会用"预埋过多结构。

### 版本化策略

版本前缀放路径首段，与本地路径风格共存：`POST /api/v1/orders/get`、`POST /api/v2/orders/get`。

**何时需要新版本**：破坏性变更必须升版本；非破坏性变更不升版本。

- 非破坏性（不升版本）：新增响应字段、新增可选入参、新增接口
- 破坏性（必须升版本）：删除/重命名字段、变更字段类型、变更 URL 结构、变更鉴权方式

**版本生命周期**：

1. 同时维护最多 2 个活跃版本（当前 + 上一版）。
2. 弃用公告：对外接口至少提前 6 个月通知。
3. 弃用响应头 `Sunset: <RFC1123 时间>` 告知客户端截止时间。
4. 到期后返回 410 Gone（配合错误响应四字段）。

## 限流响应

### 标准响应头

接口统一返回限流头，客户端可据此控制请求频率：

- `X-RateLimit-Limit` - 窗口内允许的总请求数
- `X-RateLimit-Remaining` - 窗口内剩余请求数
- `X-RateLimit-Reset` - 窗口重置的 Unix 时间戳

### 超限响应

触发限流时，HTTP 状态码使用 `429`，返回 `Retry-After` 响应头（秒数），body 保持错误响应四字段：

```json
{
  "code": 429,
  "status": false,
  "message": "请求过于频繁，请稍后重试",
  "data": null
}
```

- 错误码统一 `429`（业务码与 HTTP 码一致）；如需要更细区分，放 message 或 data，不放 code 之外的顶层字段。

### 限流层级（参考）

| 层级 | 窗口限制 | 作用域 | 适用 |
|---|---|---|---|
| 匿名 | 30/分钟 | IP | 公开接口 |
| 已登录 | 100/分钟 | 用户 | 常规接口 |
| 内部服务 | 10000/分钟 | 服务 | 服务间调用 |
