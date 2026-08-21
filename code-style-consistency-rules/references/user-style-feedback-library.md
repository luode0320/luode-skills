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
- 来源: 用户截图反馈（2026-08-06）
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
- 规则一句话: Go 函数/方法内部禁止用 `var (...)` 分组声明局部变量，必须逐行 `var` 单独声明，行尾中文注释按列对齐。
- 首次记录: 2026-08-06
- 确认时间: 2026-08-06
- 出现次数: 1

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

## 变更记录

- 2026-07-13：建立全局用户风格反例库，写入库结构示例条目 STYLE-CASE-GO-001。
- 2026-07-13：经周期01捕获流程演练，用户确认后写入 active 条目 STYLE-CASE-GO-002（禁用 iota）。
- 2026-08-06：用户截图反馈确认后写入 active 条目 STYLE-CASE-GO-003（函数内禁止 var 分组声明）。
- 2026-08-21：用户截图反馈确认后写入 active 条目 STYLE-CASE-GO-004（仓储层禁止硬编码表名，引用 model 的 `TableName()`）；规则定义权威在 `database-schema-rules` 铁律 1.2，访问层检查在 `database-query-rules`，本库只承载写码前规避用的正反例。
- 2026-08-21：用户截图反馈确认后写入 active 条目 STYLE-CASE-GO-005（ORM 模型字段行尾禁止重抄 `comment:` tag）；规则权威在 `comment-rules` 位置分区（`references/comment-placement.md`），`database-schema-rules` 铁律 1 只声明"注释说明的载体是 comment tag / DDL COMMENT"，本库同样只承载正反例。
