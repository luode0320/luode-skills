# 响应结构正反例

## 正例

### 正例 1：成功响应完整包含四个字段

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

### 正例 2：成功响应无数据时 data 为 null

```json
{
  "code": 200,
  "status": true,
  "message": "操作成功",
  "data": null
}
```

### 正例 3：分页响应数据结构（包含 hasNext）

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

### 正例 4：分页响应（最后一页，hasNext 为 false）

```json
{
  "code": 200,
  "status": true,
  "message": "查询成功",
  "data": {
    "list": [
      {
        "orderId": "12399",
        "orderNo": "ORD202603280099"
      },
      {
        "orderId": "12400",
        "orderNo": "ORD202603280100"
      }
    ],
    "pagination": {
      "page": 5,
      "pageSize": 20,
      "total": 100,
      "totalPages": 5,
      "hasNext": false
    }
  }
}
```

### 正例 5：错误响应完整包含四个字段

```json
{
  "code": 400,
  "status": false,
  "message": "参数错误：orderId 不能为空",
  "data": null
}
```

### 正例 6：使用字符串 status 的错误响应

```json
{
  "code": 400,
  "status": "error",
  "message": "参数错误：orderId 不能为空",
  "data": null
}
```

### 正例 7：错误响应带详细数据

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

## 反例

### 反例 1：成功响应缺少 code 字段

```json
{
  "status": true,
  "message": "操作成功",
  "data": {
    "orderId": "12345"
  }
}
```

结论：缺少 code 字段，必须补全。

### 反例 2：成功响应缺少 status 字段

```json
{
  "code": 200,
  "message": "操作成功",
  "data": {
    "orderId": "12345"
  }
}
```

结论：缺少 status 字段，必须补全。

### 反例 3：成功响应缺少 message 字段

```json
{
  "code": 200,
  "status": true,
  "data": {
    "orderId": "12345"
  }
}
```

结论：缺少 message 字段，必须补全。

### 反例 4：成功响应缺少 data 字段

```json
{
  "code": 200,
  "status": true,
  "message": "操作成功"
}
```

结论：缺少 data 字段，必须补全（无数据时用 null）。

### 反例 5：错误响应缺少 code 字段

```json
{
  "status": false,
  "message": "参数错误",
  "data": null
}
```

结论：缺少 code 字段，必须补全。

### 反例 6：错误响应缺少 status 字段

```json
{
  "code": 400,
  "message": "参数错误",
  "data": null
}
```

结论：缺少 status 字段，必须补全。

### 反例 7：错误响应缺少 message 字段

```json
{
  "code": 400,
  "status": false,
  "data": null
}
```

结论：缺少 message 字段，必须补全。

### 反例 8：错误响应缺少 data 字段

```json
{
  "code": 400,
  "status": false,
  "message": "参数错误"
}
```

结论：缺少 data 字段，必须补全（无数据时用 null）。

### 反例 9：分页响应缺少 hasNext 字段

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
      }
    ],
    "pagination": {
      "page": 1,
      "pageSize": 20,
      "total": 100,
      "totalPages": 5
    }
  }
}
```

结论：缺少 hasNext 字段，必须补全。

### 反例 10：成功和错误结构混乱

```json
// 成功时
{
  "success": true,
  "result": {
    "orderId": "12345"
  }
}

// 失败时
{
  "errCode": 400,
  "errMsg": "参数错误"
}
```

结论：同一接口成功和失败时字段层次完全不同，且无稳定规律，必须统一格式。

### 反例 11：兼容字段四处散落

```json
{
  "code": 200,
  "status": true,
  "message": "操作成功",
  "data": {
    "orderId": "12345",
    "oldOrderId": "67890",
    "orderNo": "ORD202603280001",
    "orderNoV2": "ORD202603280001-V2"
  }
}
```

结论：旧字段、新字段混在不同层级，无法判断哪一个才是主字段，应有明确的版本演进策略。
