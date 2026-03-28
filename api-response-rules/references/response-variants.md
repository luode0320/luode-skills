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

## 分页响应

分页响应的数据部分包含列表和分页信息，必须包含是否还有下一页的字段：

```json
{
  "code": 200,
  "status": true,
  "message": "查询成功",
  "data": {
    "list": [
      {
        "orderId": "12345",
        "orderNo": "ORD202603280001"
      },
      {
        "orderId": "12346",
        "orderNo": "ORD202603280002"
      }
    ],
    "pagination": {
      "page": 1,
      "pageSize": 20,
      "total": 100,
      "totalPages": 5,
      "hasNext": true
    }
  }
}
```

### 分页信息字段说明

- `page` - 当前页码（从 1 开始）
- `pageSize` - 每页条数
- `total` - 总条数
- `totalPages` - 总页数
- `hasNext` - 是否还有下一页（布尔值）

## 兼容字段与版本字段

- 兼容字段应有明确保留理由，不要长期堆积。
- 版本字段只在确有版本演进需要时引入，不为"以后可能会用"预埋过多结构。
