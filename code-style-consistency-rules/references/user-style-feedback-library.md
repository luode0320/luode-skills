# 全局用户风格反例库

本文件是**全局、跨项目、跨会话**的用户代码风格反例库，由 `code-style-consistency-rules` 唯一维护。
任何仓库写代码前都应加载本库，把其中 `active` 条目当作用户明确禁止的写法规避。

## 使用约定

- 条目格式见 `style-case-template.md`；只有 `active` 条目落盘于本文件。
- 写入前必须经用户确认（candidate→active），写入流程见 `style-feedback-workflow.md`。
- 命中同一去重键的重复反馈只更新出现次数与确认时间，不新增条目。
- 本库承载“用户跨项目通用风格偏好”；某个项目专属的一次性风格约定仍写入该项目根目录 `PROJECT_STYLE.md`，由 `project-style-rules` 维护。
- `code-generation-style-rules` 在写码前把本库 `active` 条目并入本轮风格契约的“禁用写法”。

## 反例条目

> 下面第一条为库结构示例条目，演示字段与代码块对照格式；后续用户确认的反例按 `style-case-template.md` 追加。

### STYLE-CASE-GO-001：错误处理禁止吞异常
- id: STYLE-CASE-GO-001
- status: active
- 语言/技术栈: Go
- 适用范围: 错误处理
- 去重键: go|错误处理|吞异常忽略error
- 来源: 库结构示例条目（2026-07-13）
- 反例（禁止这样写）:
  ```go
  data, _ := doSomething()   // 忽略 error
  ```
- 正例（应该这样写）:
  ```go
  data, err := doSomething()
  if err != nil {
      return fmt.Errorf("doSomething 失败: %w", err)
  }
  ```
- 规则一句话: Go 中禁止用 `_` 丢弃 error，必须显式判断并包装返回。
- 首次记录: 2026-07-13
- 确认时间: 2026-07-13
- 出现次数: 1

### STYLE-CASE-GO-002：常量枚举禁止使用 iota
- id: STYLE-CASE-GO-002
- status: active
- 语言/技术栈: Go
- 适用范围: 常量与枚举
- 去重键: go|常量枚举|iota
- 来源: 用户文字反馈（2026-07-13）
- 反例（禁止这样写）:
  ```go
  const (
      StatusInit = iota
      StatusRunning
      StatusDone
  )
  ```
- 正例（应该这样写）:
  ```go
  const (
      StatusInit    = 0
      StatusRunning = 1
      StatusDone    = 2
  )
  ```
- 规则一句话: Go 常量和枚举禁止使用 `iota`，必须显式写出每个常量值。
- 首次记录: 2026-07-13
- 确认时间: 2026-07-13
- 出现次数: 1

### STYLE-CASE-GO-003：函数内局部变量禁止 var 分组声明
- id: STYLE-CASE-GO-003
- status: active
- 语言/技术栈: Go
- 适用范围: 局部变量声明
- 去重键: go|局部变量声明|var分组块声明
- 来源: 用户截图反馈（2026-08-06）；用户文字反馈复发（2026-09-12）
- 反例（禁止这样写）:
  ```go
  var (
      bestGap     int64 // 当前最优候选与服务商完成时间的间隔
      bestTimeTsp int64 // 当前最优候选的上链时间
  )
  ```
- 正例（应该这样写）:
  ```go
  var bestGap int64     // 当前最优候选与服务商完成时间的间隔
  var bestTimeTsp int64 // 当前最优候选的上链时间
  ```
- 正例（带初始化的局部声明同样逐行 var）:
  ```go
  var rows []*model.ExchangeCoinsOrdered
  var err error
  var repo = repository.NewExchangeCoinsOrderedRepo()
  ```
- 规则一句话: Go 函数/方法内部禁止用 `var (...)` 分组声明局部变量，必须逐行 `var` 单独声明，行尾中文注释按列对齐；带初始化赋值的局部声明（`var repo = ...`）同样逐行单独声明，不进分组块。
- 首次记录: 2026-08-06
- 确认时间: 2026-09-12
- 出现次数: 2
- 复发提示: 2026-09-12 二次复发场景为 var 块内"纯声明 + 初始化赋值"混排（rows/err/repo 三行），用户判"这种定义风格是禁止"。逐行 var 约束同样覆盖带初始化声明。单行 var 声明中 `var` 与变量名的分隔以 gofmt 输出为准（单空格），用户示例中的 tab / 双空格对齐属编辑器显示，不作规则要求。

### STYLE-CASE-GO-004：仓储层禁止硬编码表名字符串
- id: STYLE-CASE-GO-004
- status: active
- 语言/技术栈: Go / GORM（跨 ORM 同理）
- 适用范围: 数据库访问层
- 去重键: go|数据库访问|repository硬编码表名
- 来源: 用户截图反馈（2026-08-21，圈出 model 的 `TableName()` 与 repository 的 `tableName: "coins_browser_url_dict"` 两处同名字面量）
- 反例（禁止这样写）:
  ```go
  func NewCoinsBrowserUrlDictRepo() *CoinsBrowserUrlDictRepo {
      return &CoinsBrowserUrlDictRepo{
          db:        connection.GetDB(),
          tableName: "coins_browser_url_dict", // 与 model.TableName() 重复，两个真相源
      }
  }
  ```
- 正例（应该这样写）:
  ```go
  func NewCoinsBrowserUrlDictRepo() *CoinsBrowserUrlDictRepo {
      return &CoinsBrowserUrlDictRepo{
          db:        connection.GetDB(),
          tableName: model.CoinsBrowserUrlDict{}.TableName(),
      }
  }
  ```
- 规则一句话: 表名只在 model 的 `TableName()` 定义一次，repository / DAO / 脚本一律引用该方法，禁止重复写表名字面量。
- 首次记录: 2026-08-21
- 确认时间: 2026-08-21
- 出现次数: 1

### STYLE-CASE-GO-005：ORM 模型字段禁止行尾重抄 comment tag
- id: STYLE-CASE-GO-005
- status: active
- 语言/技术栈: Go / GORM（其他 ORM 与 schema description 同理）
- 适用范围: 注释放置 / 数据库模型
- 去重键: go|注释放置|模型字段行尾重复comment tag
- 来源: 用户截图反馈（2026-08-21，`database/model/db/coinsBrowserUrlDict.go` 每行 `comment:xxx` 后又跟 `// xxx`）
- 反例（禁止这样写）:
  ```go
  CType   string `gorm:"column:cType;...;comment:网络类型" json:"cType"`      // 网络类型
  AddrUrl string `gorm:"column:addrUrl;...;comment:钱包地址url" json:"addrUrl"` // 钱包地址url
  ```
- 正例（应该这样写）:
  ```go
  CType   string `gorm:"column:cType;...;comment:网络类型" json:"cType"`
  AddrUrl string `gorm:"column:addrUrl;...;comment:钱包地址url" json:"addrUrl"`
  Enabled int8   `gorm:"column:enabled;...;comment:是否启用" json:"enabled"` // 1=启用 0=禁用
  ```
- 规则一句话: 字段含义已由 `comment:` tag 承载时不写行尾重复注释；tag 缺 `comment:` 时把说明补进 tag 而不是只写行尾；行尾只留元数据放不下的信息（单位、枚举取值、业务约束、为什么）。
- 首次记录: 2026-08-21
- 确认时间: 2026-08-21
- 出现次数: 1

### STYLE-CASE-ALL-001：匿名闭包尽量用具名函数替换
- id: STYLE-CASE-ALL-001
- status: active
- 语言/技术栈: 通用（Go / JS-TS / Python 等，凡能用具名函数替代处）
- 适用范围: 匿名函数 / 闭包写法
- 去重键: 通用|匿名函数闭包|匿名闭包尽量用具名函数替换
- 来源: 用户文字反馈（2026-09-03）
- 反例（不推荐这样写）:
  ```go
  // 内联匿名函数闭包：一段逻辑被包进匿名函数，函数套函数，读起来要先跳进闭包体
  sorted := slices.SortFunc(items, func(a, b Item) int {
      if a.Priority != b.Priority {
          return b.Priority - a.Priority
      }
      return strings.Compare(a.Name, b.Name)
  })
  ```
- 正例（建议这样写）:
  ```go
  // 抽成具名函数，调用处一眼看懂比较逻辑，也便于单独测试
  func compareByPriorityThenName(a, b Item) int {
      if a.Priority != b.Priority {
          return b.Priority - a.Priority
      }
      return strings.Compare(a.Name, b.Name)
  }

  sorted := slices.SortFunc(items, compareByPriorityThenName)
  ```
- 规则一句话: 强烈不推荐使用匿名函数闭包包裹逻辑（阅读可读性低），尽量抽成具名函数替换以便阅读与测试；仅在没有具名替代的语言强约束场景（如 goroutine/defer 起步、立即捕获循环变量的短回调）非不得已才保留，不作绝对禁用。
- 首次记录: 2026-09-03
- 确认时间: 2026-09-03
- 出现次数: 1

### STYLE-CASE-ALL-002：禁用泛型+高阶函数+多回调的过度抽象（抽象收益 < 认知成本）
- id: STYLE-CASE-ALL-002
- status: active
- 语言/技术栈: 通用（Go / JS-TS / Python 等，凡存在泛型/高阶函数/回调抽象处）
- 适用范围: 泛型工具函数 + 高阶函数 + 多回调叠加的过度抽象
- 去重键: 通用|过度抽象|为省少量重复叠泛型高阶多回调宁可直写
- 来源: 用户代码反馈（2026-09-03）
- 反例（不推荐这样写）:
  ```go
  // loadSnapshot[V any] 把"缓存读->未命中->单飞构建->回填"抽象成通用工具，
  // 调用处要传 get/set/build 三个闭包，各自捕获一堆外层变量，读调用处根本看不清每个闭包做什么，
  // 必须先把工具的"契约"装进脑子，再反向拼接每个回调，认知成本被泛型+高阶+单飞三层叠加吞噬。
  loadSnapshot(key, fromBusinessSnapshotCache.Get,
      func(k string, v *FromBusinessSnapshot) {
          fromBusinessSnapshotCache.SetWithTTL(k, v, 1, swapSnapshotTTL)
      },
      func() *FromBusinessSnapshot { return buildFromBusinessSnapshot(gen, ctx, cTypeKeyword) })
  ```
- 正例（应该这样写，仅此一处调用时直写在业务层）:
  ```go
  // 缓存命中直接返回；未命中用具名构建函数平铺出逻辑，读者一行行顺着看即懂，无需理解工具契约。
  if v, ok := fromBusinessSnapshotCache.Get(key); ok {
      return v
  }
  snap, _, _ := snapshotSingleflight.Do(key, func() (any, error) {
      if v, ok := fromBusinessSnapshotCache.Get(key); ok { // 双重检查
          return v, nil
      }
      built := buildFromBusinessSnapshot(gen, ctx, cTypeKeyword) // 具名业务函数，意图自明
      fromBusinessSnapshotCache.SetWithTTL(key, built, 1, swapSnapshotTTL)
      return built, nil
  })
  return snap.(*FromBusinessSnapshot)
  ```
- 规则一句话: 强烈不推荐把仅为消除少量重复的逻辑抽象成"泛型工具函数 + 多回调/高阶函数"包裹，因为读调用处要先理解工具契约再反向拼回调，抽象收益 < 认知成本；当某个工具函数只服务一两处调用、却逼调用方传多个回调或叠泛型时，宁可容忍少量重复在业务层平铺直写，也不要上泛型高阶抽象。仅当工具函数确实有多个调用点、能稳定收敛重复时才允许抽成通用具名工具，且不得以泛型+回调层层包裹牺牲直线可读性。
- 首次记录: 2026-09-03
- 确认时间: 2026-09-03
- 出现次数: 1

### STYLE-CASE-ALL-003：同构语句组内禁止插入多行块注释
- id: STYLE-CASE-ALL-003
- status: active
- 语言/技术栈: 通用（Go / JS-TS / Python 等，凡存在逐行平行同构语句处）
- 适用范围: 注释放置 / 注释风格一致性
- 去重键: 通用|注释放置|同构语句组内插入多行块注释
- 来源: 用户代码反馈（2026-09-08，`internal/provider/buy/init.go` 的 `Init()` 三行服务商注册）；2026-09-10 同场景二次复发（注册区注释膨胀为 4 行反事实推演链）；2026-09-10 用户进一步澄清口径——不需要过程注释，只保留简单的目的注释，不做"压成一行 + 锚点"的折中
- 反例（禁止这样写）:
  ```go
  func Init() {
      onramper.New().Start(true) // 创建并注册交易所onramper
      simplex.New().Start(true)  // 创建并注册交易所simplex
      // moonpay 的注册与 onramper.excludedRamps 里的 moonpay 必须同批上线:
      // ResolveBuyProviderName 按已注册服务商判定归属, 只注册不排除会让 Onramper 仍出 moonpay 报价、
      // 下单却改道到这里, 造成 quoteId 错配
      moonpay.New().Start(true) // 创建并注册交易所moonpay
  }
  ```
- 正例（应该这样写）:
  ```go
  func Init() {
      onramper.New().Start(true) // 创建并注册交易所onramper
      simplex.New().Start(true)  // 创建并注册交易所simplex
      moonpay.New().Start(true)  // 创建并注册交易所moonpay
  }
  ```
- 规则一句话: 注册列表、初始化列表、路由表、枚举常量等逐行平行的同构语句组，一旦已形成统一的行尾短注释风格，就必须整组保持同一形态并按列对齐，禁止在其中某一行上方插入多行块注释。背景、上线顺序、耦合约束和风险权衡写进 `doc/` 或提交说明，**代码里一行都不留**——耦合约束直接删除，不做"压成一行 + 文档锚点"的折中。代码注释只写**目的**（`// 创建并注册交易所moonpay`，这段代码做什么），不写**过程**（为什么这样做、不这样做会怎样）。
- 首次记录: 2026-09-08
- 确认时间: 2026-09-10
- 出现次数: 2
- 复发提示: 该反例已在同一文件同一函数上复发一次；命中"注册/初始化列表 + 多行解释"组合时按硬禁处理，不因"约束看起来很重要"而放宽。用户已明确：这类过程注释**直接删除**即可，代码里只保留一行目的注释。

### STYLE-CASE-GO-006：模型字段上方禁止多行机制/决策块注释
- id: STYLE-CASE-GO-006
- status: active
- 语言/技术栈: Go / GORM（其他 ORM 与 schema description 同理）
- 适用范围: 注释放置 / 数据库模型
- 去重键: go|注解放置|模型字段上方多行机制决策注释
- 来源: 用户文字反馈（2026-09-12，`ToTokenId` 字段上方 3 行机制 + 决策注释）
- 反例（禁止这样写）:
  ```go
  // 空串与非空值都由自动探测写入与解除：采样方向全部失败写空串（整个兑出币不可用），
  // 部分失败则对失败的方向各写一行非空值。人工写入的行目前与自动行不做区分，
  // 会被下一轮探测按同样规则解除（用户 2026-09-12 决定暂不区分来源，做人工下架后台时再加列）。
  ToTokenId string `gorm:"column:to_token_id;...;comment:兑入币种标识，格式同兑出币，空串表示该兑出币的全部兑入方向" json:"toTokenId"`
  ```
- 正例（应该这样写）:
  ```go
  ToTokenId string `gorm:"column:to_token_id;...;comment:兑入币种标识，格式同兑出币，空串表示该兑出币的全部兑入方向" json:"toTokenId"`
  ```
- 规则一句话: 模型字段上方禁止多行块注释；字段语义进 `comment:` tag，运行机制、来源区分决策、未来计划等过程信息一律删除，写进模块文档或提交说明，代码里一行不留。
- 规则权威: `comment-rules` 硬约束（注释只留目的）+ `comment-placement.md` 第 5/8/10 条；本库只承载写码前规避用的正反例。
- 首次记录: 2026-09-12
- 确认时间: 2026-09-12
- 出现次数: 1

## 变更记录

- 2026-07-13：建立全局用户风格反例库，写入库结构示例条目 STYLE-CASE-GO-001。
- 2026-07-13：经周期01捕获流程演练，用户确认后写入 active 条目 STYLE-CASE-GO-002（禁用 iota）。
- 2026-08-06：用户截图反馈确认后写入 active 条目 STYLE-CASE-GO-003（函数内禁止 var 分组声明）。
- 2026-08-21：用户截图反馈确认后写入 active 条目 STYLE-CASE-GO-004（仓储层禁止硬编码表名，引用 model 的 `TableName()`）；规则定义权威在 `database-schema-rules` 铁律 1.2，访问层检查在 `database-query-rules`，本库只承载写码前规避用的正反例。
- 2026-08-21：用户截图反馈确认后写入 active 条目 STYLE-CASE-GO-005（ORM 模型字段行尾禁止重抄 `comment:` tag）；规则权威在 `comment-rules` 位置分区（`references/comment-placement.md`），`database-schema-rules` 铁律 1 只声明"注释说明的载体是 comment tag / DDL COMMENT"，本库同样只承载正反例。
- 2026-09-03：用户文字反馈确认后写入 active 条目 STYLE-CASE-ALL-001（匿名闭包尽量用具名函数替换，语气为强烈不推荐而非绝对禁用，通用/Go/JS-TS/Python）。
- 2026-09-08：用户贴 `internal/provider/buy/init.go` 正反对照并确认后写入 active 条目 STYLE-CASE-ALL-003（同构语句组内禁止插入多行块注释）；规则权威在 `comment-rules` 位置分区（`references/comment-placement.md` 末条），本库只承载写码前规避用的正反例，不重复定义规则。
- 2026-09-03：用户贴具体代码并确认"①+②过度抽象"后写入 active 条目 STYLE-CASE-ALL-002（禁用泛型+高阶函数+多回调的过度抽象，抽象收益<认知成本时宁可平铺直写；实例来自 loadSnapshot[V any] 通用快照工具，正例为单点调用时在业务层展开）。
- 2026-09-10（复发）：STYLE-CASE-ALL-003 同去重键二次复发（用户在 `Init()` 注册区再次贴出 4 行反事实推演链，仍判"烂注释"），更新出现次数 1→2、确认时间为 2026-09-10，新增"复发提示"字段。同步在 `comment-rules`（SKILL.md 硬约束、comment-granularity.md、comment-placement.md、comment-examples.md「耦合约束正反例」）与 `code-generation-style-rules/references/style-contract-template.md` 注释契约对齐。
- 2026-09-10（口径收敛，撤销折中形态）：用户澄清"就是删除就行了，我们不需要过程注释，有一个简单的目的注释就行了"。据此撤销同日早先引入的"压成一行结论 + 文档锚点"折中形态：`comment-rules` SKILL.md 硬约束改为"注释只留目的，过程一律删除，不设折中形态"，`comment-granularity.md` 撤掉"允许一句因果说明"的例外条款，`comment-placement.md`、`comment-examples.md`（「耦合约束正反例」改为"没有第三种形态"）与 `code-generation-style-rules/references/style-contract-template.md` 同步。`comment-rules` 收口口径统一为：**代码注释只有"目的注释"一类合格形态，过程信息（原因、权衡、后果推演、耦合约束）一律直接删除**。
- 2026-09-12：STYLE-CASE-GO-003 同去重键二次复发（用户贴出 var 块内 rows/err/repo 声明与初始化混排并判"这种定义风格是禁止"），出现次数 1→2、确认时间更新为 2026-09-12；正例补充带初始化的逐行 var 写法（`var repo = repository.NewExchangeCoinsOrderedRepo()`），规则一句话同步覆盖"带初始化赋值的局部声明同样逐行单独声明"，新增"复发提示"注明 var 与变量名分隔以 gofmt 输出为准（单空格），用户示例中的 tab / 双空格对齐不作规则要求。规则条文无需改动：`SKILL.md`「Go 局部变量声明风格约定」与 `go-coding-rules.md` 既有 bullet 已完整覆盖。
- 2026-09-12：经用户确认新增 active 条目 STYLE-CASE-GO-006（模型字段上方禁止多行机制/决策块注释；字段语义进 `comment:` tag，运行机制、来源区分决策、未来计划等过程信息一律删除，写进模块文档或提交说明）。去重判定为新增而非复发：GO-005 管"行尾重抄 tag"、ALL-003 前提是"组内已形成行尾短注释风格"，均不覆盖"裸行组上方挂块注释"形态。规则权威在 `comment-rules` 硬约束与 `comment-placement.md` 第 5/8/10 条（同日第 10 条同步微调），本库只承载正反例。
