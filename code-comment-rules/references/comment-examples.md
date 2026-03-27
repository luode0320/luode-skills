# 注释结构样例

## 更好

- 在多步骤代码块中使用中文编号步骤注释，例如：

```go
// 1. 校验请求参数并提取订单 ID
orderID := strings.TrimSpace(req.OrderID)
if orderID == "" {
    return errors.New("orderID is required")
}

// 2. 查询订单并校验当前状态是否允许退款
order, err := repository.GetOrder(ctx, orderID)
if err != nil {
    return err
}

// 3. 生成退款单并回写订单状态
refund, err := service.CreateRefund(ctx, order)
if err != nil {
    return err
}
```

- 在字段定义和初始化位置同时补字段注释，例如：

```go
type RefundRequest struct {
    UserID  string // 用户 ID
    OrderID string // 订单 ID
    Reason  string // 退款原因
}

payload := RefundRequest{
    UserID:  req.UserID,  // 用户 ID
    OrderID: req.OrderID, // 订单 ID
    Reason:  req.Reason,  // 退款原因
}
```

- 在字段使用位置也重复补字段注释，例如：

```go
result := map[string]any{
    "userId":  payload.UserID,  // 用户 ID
    "orderId": payload.OrderID, // 订单 ID
    "reason":  payload.Reason,  // 退款原因
}
```

## 较差

- `i++ // i 加 1`
- 给每一行链式调用都补一条重复注释。
- 一个三段式流程没有 `1.`、`2.`、`3.` 步骤注释，只靠读者自己推断顺序。
- 结构体字段定义有注释，但初始化对象时字段列表完全没有重复注释。
- 结构体字段定义有注释，但字段组装和字段使用位置完全没有重复注释。
