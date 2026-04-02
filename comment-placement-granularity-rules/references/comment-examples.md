# 注释结构样例

## 更好

- 在风险边界入口补短注释：

```go
// 旧 token 可能已被下游缓存，回收前先做幂等检查，避免重复失效通知。
if cache.ShouldInvalidate(tokenID) {
    // ...
}
```

- 在字段定义和初始化位置同时补字段含义：

```go
type RefundRequest struct {
    UserID  string // 用户 ID
    OrderID string // 订单 ID
}

payload := RefundRequest{
    UserID:  req.UserID,  // 用户 ID
    OrderID: req.OrderID, // 订单 ID
}
```

- 发现旧注释已失效时，先清理旧注释再补新注释。

## 较差

- `i++ // i 加 1`
- 把整段函数流程都堆进函数开头一大段注释里。
- 字段定义有注释，但初始化和出参组装完全没有字段含义提示，迫使读者频繁回跳。
- 代码已经改成“先查缓存再落库”，注释还写成“直接写库”，却未清理。
