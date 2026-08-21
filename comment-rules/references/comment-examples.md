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

- 字段含义已由 ORM `comment:` tag 承载时，不再写行尾重复副本；行尾只留元数据放不下的信息：

```go
type CoinsBrowserUrlDict struct {
    ID      int    `gorm:"column:id;type:int(11);primaryKey;autoIncrement;comment:主键" json:"id"`
    CType   string `gorm:"column:cType;type:varchar(100);not null;default:'';comment:网络类型" json:"cType"`
    Enabled int8   `gorm:"column:enabled;type:tinyint(1);not null;default:1;comment:是否启用" json:"enabled"` // 1=启用 0=禁用
}
```

- 发现旧注释已失效时，先清理旧注释再补新注释。

## 较差

- `i++ // i 加 1`
- 把整段函数流程都堆进函数开头一大段注释里。
- 字段定义有注释，但初始化和出参组装完全没有字段含义提示，迫使读者频繁回跳。
- ORM 模型字段行尾注释逐字重抄 `comment:` tag，一个含义维护两处，改字段说明时必然漂移：

```go
// 较差：同一行的 comment tag 与行尾注释互为副本
CType   string `gorm:"column:cType;...;comment:网络类型" json:"cType"`      // 网络类型
AddrUrl string `gorm:"column:addrUrl;...;comment:钱包地址url" json:"addrUrl"` // 钱包地址url
```

- ORM 模型字段只写了行尾注释、`comment:` tag 空着，字段说明进不了数据库列注释：`ID int \`gorm:"column:id;primaryKey"\` // 主键` —— 应把「主键」补进 `comment:`，再删行尾。
- 代码已经改成“先查缓存再落库”，注释还写成“直接写库”，却未清理。
