# 注释结构样例

## 更好

- 每个函数、方法都必须标注最近修改时间（北京时间：yyyy-MM-DD HH:mm:ss），例如：

```go
// CreateOrder 创建订单
// [参数] ctx: 请求上下文；req: 创建订单请求
// [返回] *OrderResponse: 订单创建结果；error: 失败原因
// 最近修改时间：2026-03-28 14:30:22
func CreateOrder(ctx context.Context, req *OrderRequest) (*OrderResponse, error) {
    // 1. 校验请求参数
    // ...
}
```

- 无参数或无返回时也要明确写 `无`，例如：

```go
// Warmup 预热缓存
// [参数] 无
// [返回] error: 预热失败时返回错误
// 最近修改时间：2026-03-29 18:08:00
func Warmup() error {
    // ...
}
```

```go
// resetCache 重置本地缓存状态
// [参数] cacheKey: 缓存键
// [返回] 无
// 最近修改时间：2026-03-29 18:08:00
func resetCache(cacheKey string) {
    // ...
}
```

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
- 新增或修改函数时没有 `[参数]` / `[返回]` 注释，或参数返回语义写得过于含糊。
