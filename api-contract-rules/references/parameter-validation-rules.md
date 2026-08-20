# 参数校验规则

## 用途

用于区分基础参数校验和业务规则校验。

## Controller 参数绑定与基础校验

统一在 controller 中使用 ShouldBindJSON 进行参数绑定，这一步会自动处理：

- JSON 格式校验
- 字段类型校验
- 字段必填校验（通过 binding tag）
- 基础格式校验（如邮箱、手机号等，通过 binding tag）

示例：

```go
var req request.ReqSetBlacklistEnabled
err := c.ShouldBindJSON(&req)
if err != nil {
    http.AppReturn(c, false, err.Error(), nil)
    return
}
```

## 基础参数校验（通过 binding tag）

- 必填：`binding:"required"`
- 可选：不加 required tag
- 类型：自动通过 JSON 反序列化校验
- 长度：`binding:"min=1,max=100"`
- 枚举范围：`binding:"oneof=active inactive"`
- 基础格式：`binding:"email"`、`binding:"url"` 等

## 不应放在参数层的内容

- 跨对象业务约束
- 复杂状态判断
- 依赖数据库当前状态的规则
- 明显属于业务流程的审批或权限判断

## 原则

- 参数层先保证"能不能被接收"（通过 ShouldBindJSON 和 binding tag）。
- 业务层再判断"业务上允不允许"。
- ShouldBindJSON 绑定失败时，统一返回错误给前端。
