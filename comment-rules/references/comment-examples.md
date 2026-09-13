# 注释结构样例

## 注释分层

只有函数/方法注释写完整——整体说明（做什么）+ `[参数]` + `[返回]` + `最近修改时间`；其余位置（字段、属性、结构体字面量、代码块内某一行、补丁位点）只写**一句话作用或目的**。同一处改动里两层的样子：

```go
// Quote 一次取回币对的可兑换范围与标准汇率。
// [参数] req: 报价请求参数(含币对与标准报价数量)。
// [返回] *entity.RespProviderQuote: 范围与标准汇率；error: 请求或解析异常。
// 最近修改时间: 2026-09-09 14:20:00 新增, MoonPay 卖币独立接入。
func (p *provider) Quote(req entity.ReqProviderQuote) (*entity.RespProviderQuote, error) {
    // 卖币走独立报价通道
    if req.Side == entity.SideSell {
        return p.sellQuote(req)
    }
    // ...
}

type SellConfig struct {
    Channel string // 卖币通道名
    Timeout int    // 超时时间，单位：毫秒
}
```

反面：把函数注释的完整格式平摊到行内，给每一行都套 `做了什么` + `为什么要加`——行内只需要一句 `// 卖币走独立报价通道`。

## 更好

- 风险边界处只写边界事实，不写"为什么会有这个风险"：

```go
// 仅回收已终态的交易
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

- 函数头只说清目的与结果（不含方案权衡），本次改动的一句话简单说明压缩进 `最近修改时间` 一行：

```go
// Quote 一次取回币对的可兑换范围与标准汇率。
// [参数] req: 报价请求参数(含币对与标准报价数量)。
// [返回] *entity.RespProviderQuote: 范围与标准汇率；error: 请求或解析异常。
// 最近修改时间: 2026-09-05 12:00:00，币对由函数参数收进 req，与 Create 入参形态统一。
func (p *exchangeProvider) Quote(req entity.ReqProviderQuote) (*entity.RespProviderQuote, error)
```

## 较差

- `i++ // i 加 1`
- 把整段函数流程都堆进函数开头一大段注释里。

- 把决策过程、方案对比、实测数据、历史演进写进函数头 —— 这些都是一次性的过程信息，写进注释就变成了永久维护负担，且随代码演进迅速失真：

```go
// 较差：读者要先消化四段往事，才能知道这个函数到底做什么
//
// 【为什么是并发两次而不是一次】
// 范围在 /v2/exchange/range、汇率在 /v2/exchange/estimated-amount，是两个独立接口……
//
// 【报价金额落在范围外时直接失败，不做回退】
// 既有 GetRateFromProvider 会在金额超范围时回退到最小值再问一次价，那是给用户金额准备的补救；
// 本接口只回答「这个币对在标准额度上是什么价」……
//
// 【换算的前提与实测误差】
// 2026-08-31 在 local 用同一币对连抓各档位实测两轮：SWAPKIT 0.003%~0.031%、
// NEXCHANGE 0.019%~0.083%……
func (p *exchangeProvider) Quote(req entity.ReqProviderQuote) (*entity.RespProviderQuote, error)
```

- 多次修改后并列堆叠多行 `最近修改时间`，把函数头写成变更日志（历史该由 `git log` 承载）：

```go
// 较差：三行历史里只有最后一行描述当前实现，前两行永远没人删
// 最近修改时间: 2026-08-29 23:36:00，将 Check 检测拆分为独立函数……
// 最近修改时间: 2026-08-30 00:24:00，主函数收敛为纯编排……
// 最近修改时间: 2026-08-31 00:00:00，gas 取值时机按最大兑换场景分流……
```
- 字段定义有注释，但初始化和出参组装完全没有字段含义提示，迫使读者频繁回跳。
- ORM 模型字段行尾注释逐字重抄 `comment:` tag，一个含义维护两处，改字段说明时必然漂移：

```go
// 较差：同一行的 comment tag 与行尾注释互为副本
CType   string `gorm:"column:cType;...;comment:网络类型" json:"cType"`      // 网络类型
AddrUrl string `gorm:"column:addrUrl;...;comment:钱包地址url" json:"addrUrl"` // 钱包地址url
```

- ORM 模型字段只写了行尾注释、`comment:` tag 空着，字段说明进不了数据库列注释：`ID int \`gorm:"column:id;primaryKey"\` // 主键` —— 应把「主键」补进 `comment:`，再删行尾。
- 代码已经改成"先查缓存再落库"，注释还写成"直接写库"，却未清理。

- 简单字段映射加了冗余注释，把代码变成"注释 + 重复"：

```go
// 较差：每行字段映射都加注释，注释只是逐字复述代码
// 用户 ID
UserID: user.ID,
// 用户名
UserName: user.Name,
// 邮箱
Email: user.Email,
// 手机号
Phone: user.Phone,
```

正确做法：字段名本身已语义自明，不需要任何注释：

```go
UserID:  user.ID,
UserName: user.Name,
Email:   user.Email,
Phone:   user.Phone,
```

- 函数调用替换时加了只描述代码功能的注释，注释没有提供额外信息：

```go
// 较差：注释只是复述了代码做了什么
// 两个简称取括号外的纯简称
PairShortName1: pureShortName(fromCurrency),
// pair 保留带链后缀的显示形态
PairShowName1: msgData.PairShowName1,
```

正确做法：函数名 `pureShortName` 已经表达了意图，不需要注释：

```go
PairShortName1: pureShortName(fromCurrency),
PairShowName1:  msgData.PairShowName1,
```

- 在注释中记载改动历史，把注释变成了变更日志：

```go
// 较差：在注释中记录改动历史 —— 这是禁止的
// 这个函数用于处理用户订单
// 修复了当用户余额不足时返回空指针的问题
// 2026-09-09: 修复余额不足空指针，在 GetBalance 后增加判空处理
// 2026-09-08: 增加超时重试机制，防止上游超时导致订单失败
// 最近修改时间: 2026-09-09 10:00:00，修复余额不足空指针
func (s *Service) Process(ctx context.Context, userID string) error {
    balance, err := s.repo.GetBalance(ctx, userID)
    if err != nil {
        return err
    }
    // 这里就是修复的内容：判空
    if balance == nil {
        return ErrBalanceNotFound
    }
    // ...
}
```

正确做法：函数头只保留"当前代码是什么、做什么用"的信息，`最近修改时间` 只有一行一句话简单说明。修复的来龙去脉（根因、方案、风险）写在 `doc/bugs/xxx/` 的 Bug 主文档中，改动历史写在 `git log` 中：

```go
// 正确：注释只描述当前状态，不记载改动历史
// Process 处理用户订单，返回余额不足错误时上游自行处理提示。
// [参数] userID: 用户标识。
// [返回] *Order: 处理完成的订单；error: 余额不足或系统异常。
// 最近修改时间: 2026-09-09 10:00:00，GetBalance 后增加余额判空，防范空指针。
func (s *Service) Process(ctx context.Context, userID string) (*Order, error) {
    balance, err := s.repo.GetBalance(ctx, userID)
    if err != nil {
        return nil, err
    }
    if balance == nil {
        // 余额不存在视为余额不足，不再继续处理
        return nil, ErrBalanceNotFound
    }
    // ...
}
```

- 在注释中写"原来是…现在改成…"的历史对比叙述：

```go
// 较差：在注释中叙述改动历史
// 原来是这里直接调用了旧接口 fetchV1，因为旧接口已废弃，现在改为 fetchV2
// 同时删除了旧的 retry 逻辑，因为 V2 接口自带重试
func (s *Service) FetchData(ctx context.Context, id string) (*Data, error) {
    return s.client.fetchV2(ctx, id)
}
```

正确做法：旧接口废弃、删除旧逻辑的理由在 `doc/` 的变更文档中记录，代码注释只说明当前在做什么：

```go
// 正确：注释只回答当前代码是什么、做什么用
// FetchData 从 V2 接口获取数据，V2 自带重试，调用方无需额外处理。
// [参数] id: 数据标识。
// [返回] *Data: 查询结果；error: 获取或解析异常。
// 最近修改时间: 2026-09-09 10:00:00，从 fetchV1 迁移至 fetchV2，移除手动重试。
func (s *Service) FetchData(ctx context.Context, id string) (*Data, error) {
    return s.client.fetchV2(ctx, id)
}
```

## 耦合约束正反例

上线顺序、注册与排除配对、开关联动这类"跨模块耦合约束"是过程注释的重灾区：写的人觉得自己在帮后人避坑，实际是让每个读者先消化一段推演才能回到代码。判据固定为——**代码只留目的注释，约束与推演都不进代码**。

较差：用 4 行把约束写成反事实推演链，读者被迫先理解"只注册不排除会怎样、只排除不注册又会怎样"两个分支，才能回到原本两行的代码：

```go
func Init() {
    onramper.New().Start(true) // 创建并注册交易所onramper
    // moonpay 的注册与 onramper 侧的 excludedRamps 排除必须同批上线:
    // 只注册不排除会让 Onramper 仍出 moonpay 报价、下单却按 channelName 改道到这里, 造成订单归属错配;
    // 只排除不注册则 moonpay 卖币直接从报价里消失。见 sell/onramper/base.go 的 excludedRamps
    moonpay.New().Start(true) // 创建并注册交易所moonpay
}
```

更好：注册列表是同构语句组，保持一行短注释的一致节奏，不插入块注释。约束的后台由提交说明与 `doc/` 承载：

```go
func Init() {
    onramper.New().Start(true) // 创建并注册交易所onramper
    moonpay.New().Start(true)  // 创建并注册交易所moonpay
}
```

**没有第三种形态。** 不需要"压成一行结论 + 文档锚点"之类的折中——耦合约束本身就不写进代码。这类"不写就会被后人改错"的顾虑，由「两处必须同批上线」的工程约束、提交说明与 `doc/` 承载。

唯一合格形态就是上面那样：**一行目的注释**（这段代码做什么），过程信息一律不留。代码注释不承担"防后人改错"的职责——那要靠结构调整、测试和评审。
