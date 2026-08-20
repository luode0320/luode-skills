# 响应结构基线

## 用途

用于统一成功响应的基础层次和数据放置方式。

## 铁律：成功响应必须包含的四个字段

**成功响应必须包含以下四个字段：**

1. **code** - 状态码（整型）
2. **status** - 状态（布尔值或字符串）
3. **message** - 消息（字符串）
4. **data** - 返回数据（对象或 null）

## 成功响应标准格式

```json
{
  "code": 200,
  "status": true,
  "message": "操作成功",
  "data": {
    "orderId": "12345",
    "orderNo": "ORD202603280001",
    "status": "paid"
  }
}
```

## 分页响应标准格式

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

## 无数据时的响应格式

当没有返回数据时，data 字段为 null：

```json
{
  "code": 200,
  "status": true,
  "message": "操作成功",
  "data": null
}
```

## 基本原则

- 业务数据与元信息分层明确。
- 顶层字段尽量稳定，不随具体业务频繁漂移。
- 业务数据应进入明确的数据载体，而不是和状态字段混成一团。
- 成功响应必须包含 code、status、message、data 四个字段。

## 建议

- 成功响应优先表达"是否成功""核心数据""必要元信息"。
- 如果项目已存在稳定统一包装，优先沿用，不另起一套。
