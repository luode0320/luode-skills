# Go 工具包用法 Recipe

本文档提供 `package-structure-rules` Catalog 中 Go 工具包的标准用法示例。每个 recipe 包含目录位置、Go import 路径、包别名、核心函数签名、典型用法示例、关联 skill 引用和注意事项。当前首批覆盖 `convert`、`time`、`cache/redis`、`json`、`log`、`http` 六类。

所有示例必须遵循 `code-style-consistency-rules`、`common-util-rules`、`time-util-rules` 等专业 skill 的规则；本文件只做用法索引与示例，不替代专业 skill 正文。

## convert：字符串与数字互转

- 目录位置：`utils/convert/`
- Go import：`<module>/utils/convert`
- 包别名：无（`convert` 不与标准库冲突）
- 关联 skill：`common-util-rules`
- 关联 recipe 索引：`#convert`

### 典型用法

```go
package convert

import "strconv"

// ParseInt64 安全解析 int64，解析失败返回 0
func ParseInt64(s string) int64 {
    n, err := strconv.ParseInt(s, 10, 64)
    if err != nil {
        return 0
    }
    return n
}

// FormatInt64 将 int64 格式化为十进制字符串
func FormatInt64(n int64) string {
    return strconv.FormatInt(n, 10)
}

// ParseFloat64 安全解析 float64，解析失败返回 0
func ParseFloat64(s string) float64 {
    f, err := strconv.ParseFloat(s, 64)
    if err != nil {
        return 0
    }
    return f
}

// FormatFloat64 将 float64 格式化为十进制字符串
func FormatFloat64(f float64) string {
    return strconv.FormatFloat(f, 'f', -1, 64)
}
```

### 注意事项

- 业务层应优先使用 `convert` 包，避免在 controller/service 中散写 `strconv`。
- 入参合法性检查和出参默认值封装在 `convert` 层，调用方不需要再判断 err。
- 关联 `common-util-rules` 的"7 天冻结"策略：超过 7 天后只能新增不能改既有行为。

## time：时间转换与 timeUtil

- 目录位置：`utils/time/`
- Go import：`<module>/utils/time`
- 包别名：`timeUtil`（避免与标准库 `time` 冲突）
- 关联 skill：`time-util-rules`、`common-util-rules`
- 关联 recipe 索引：`#time`

### 典型用法

```go
package timeUtil

import (
    "time"
)

// GetNow 返回当前时间（统一本地时区）
func GetNow() time.Time {
    return time.Now()
}

// ParseTime 解析时间字符串
func ParseTime(s string) (time.Time, error) {
    return time.Parse("2006-01-02 15:04:05", s)
}

// TimeToString 格式化时间字符串
func TimeToString(t time.Time) string {
    return t.Format("2006-01-02 15:04:05")
}

// FormatYYYYToTimestamp 将 YYYYMMDD 字符串转为时间戳
func FormatYYYYToTimestamp(s string) (int64, error) {
    t, err := time.Parse("20060102", s)
    if err != nil {
        return 0, err
    }
    return t.Unix(), nil
}
```

### 注意事项

- 业务代码必须优先复用 `timeUtil`，禁止散写 `time.Now().In(...)`、`time.Date(...)` 或裸日期格式串。
- 日/月边界、自然日/月统计区间统一由 `timeUtil` 提供。
- 如果 `timeUtil` 不够用，先补 `timeUtil`，再改业务调用；关联 `time-util-rules`。

## cache/redis：Redis 缓存适配与连接边界

- 目录位置：`utils/cache/redis/`
- Go import：`<module>/utils/cache/redis`
- 包别名：无
- 关联 skill：`common-util-rules`
- 关联 recipe 索引：`#cache-redis`

### 典型用法

```go
package redis

import (
    "context"
    "time"
)

// Client 表示 Redis 缓存客户端
type Client struct {
    // 内部连接池
    pool any
}

// NewClient 创建 Redis 客户端
func NewClient(addr string, password string, db int) (*Client, error) {
    // 初始化连接池
    return &Client{pool: nil}, nil
}

// Get 获取缓存值
func (c *Client) Get(ctx context.Context, key string) (string, error) {
    // 从连接池获取并返回
    return "", nil
}

// Set 设置缓存值（带过期时间）
func (c *Client) Set(ctx context.Context, key string, value string, expiration time.Duration) error {
    // 写入并设置过期
    return nil
}
```

### 注意事项

- Redis 连接初始化统一放在 `database/connection/`，`utils/cache/redis/` 只做缓存适配。
- Redis Key、Hash、缓存值等数据模型定义在 `database/model/redis/`。
- 业务侧不得直接创建 Redis 客户端，必须通过 `database/connection/` 或 `global/` 已装配引用。
- 关联 `database-query-rules` 的本地连接红线：只允许 local 配置。

## json：JSON 序列化与反序列化

- 目录位置：`utils/json/`
- Go import：`<module>/utils/json`
- 包别名：`jsonUtil`（避免与标准库 `encoding/json` 冲突）
- 关联 skill：`common-util-rules`
- 关联 recipe 索引：`#json`

### 典型用法

```go
package jsonUtil

import (
    "encoding/json"
)

// Marshal 序列化为 JSON 字节
func Marshal(v any) ([]byte, error) {
    return json.Marshal(v)
}

// Unmarshal 反序列化 JSON 字节到结构体
func Unmarshal(data []byte, v any) error {
    return json.Unmarshal(data, v)
}

// ToJSONString 序列化为 JSON 字符串
func ToJSONString(v any) (string, error) {
    data, err := json.Marshal(v)
    if err != nil {
        return "", err
    }
    return string(data), nil
}

// PrettyPrint 格式化 JSON 字符串
func PrettyPrint(data []byte) (string, error) {
    var buf bytes.Buffer
    if err := json.Indent(&buf, data, "", "  "); err != nil {
        return "", err
    }
    return buf.String(), nil
}
```

### 注意事项

- 统一使用 `jsonUtil`，避免业务代码直接 import `encoding/json`。
- 数据脱敏、日志字段、响应序列化等统一封装在 `jsonUtil`。
- 关联 `common-util-rules` 的复用红线：已存在公共实现时禁止重复封装。

## log：统一日志框架封装

- 目录位置：`utils/log/`
- Go import：`<module>/utils/log`
- 包别名：`logUtil`（避免与标准库 `log` 冲突）
- 关联 skill：`common-util-rules`
- 关联 recipe 索引：`#log`

### 典型用法

```go
package logUtil

// Info 输出信息日志
func Info(msg string, fields ...any) {
    // 统一日志框架调用
}

// Error 输出错误日志
func Error(err error, fields ...any) {
    // 统一日志框架调用
}

// Debug 输出调试日志
func Debug(msg string, fields ...any) {
    // 统一日志框架调用
}

// WithContext 注入请求上下文
func WithContext(ctx context.Context, fields ...any) {
    // 从 context 提取 trace/span 并注入日志
}
```

### 注意事项

- 项目唯一日志调用入口是 `utils/log/`，业务代码不得直接使用第三方日志库。
- 日志字段、脱敏、trace/span 传递统一由 `logUtil` 处理。
- 关联 `logging-trace-rules`：日志等级、字段、脱敏、上下文信息必须符合项目规则。

## http：通用 HTTP Client

- 目录位置：`utils/http/`
- Go import：`<module>/utils/http`
- 包别名：`httpUtil`（避免与标准库 `net/http` 冲突）
- 关联 skill：`common-util-rules`
- 关联 recipe 索引：`#http`

### 典型用法

```go
package httpUtil

import (
    "context"
    "net/http"
    "time"
)

// Client 表示通用 HTTP 客户端
type Client struct {
    httpClient *http.Client
}

// NewClient 创建 HTTP 客户端
func NewClient(timeout time.Duration) *Client {
    return &Client{
        httpClient: &http.Client{Timeout: timeout},
    }
}

// Get 发起 GET 请求
func (c *Client) Get(ctx context.Context, url string, headers map[string]string) (*http.Response, error) {
    req, err := http.NewRequestWithContext(http.MethodGet, url, nil)
    if err != nil {
        return nil, err
    }
    for k, v := range headers {
        req.Header.Set(k, v)
    }
    return c.httpClient.Do(req)
}

// Post 发起 POST 请求
func (c *Client) Post(ctx context.Context, url string, body []byte, headers map[string]string) (*http.Response, error) {
    req, err := http.NewRequestWithContext(http.MethodPost, url, bytes.NewReader(body))
    if err != nil {
        return nil, err
    }
    for k, v := range headers {
        req.Header.Set(k, v)
    }
    return c.httpClient.Do(req)
}
```

### 注意事项

- 通用 HTTP 只能位于 `utils/http/`，禁止 `utils/api/http/`。
- 第三方 API 客户端（如 Binance、微信）进入 `utils/api/<provider>/`，复用 `httpUtil` 但不得绕过其超时/错误处理。
- 关联 `common-util-rules`：已有公共封装时禁止重复实现。


## decimal：Decimal 高精度数值类型

- 目录位置：`utils/decimal/`
- Go import：`<module>/utils/decimal`
- 包别名：`decimalUtil`（避免与 `decimal` 标准库名冲突，与其余工具包保持统一 `xxxUtil` 命名风格）
- 关联 skill：`common-util-rules`、`database-query-rules`、`database-schema-rules`
- 关联 recipe 索引：`#decimal`

### 典型用法

```go
package decimalUtil

import (
	"database/sql/driver"
	"fmt"

	"github.com/shopspring/decimal"
)

// Decimal 自定义 Decimal 类型，用于 GORM 映射和金额运算。
type Decimal struct {
	decimal.Decimal
}

// Scan 实现 sql.Scanner 接口，从数据库读取数据并转换为 Decimal。
func (d *Decimal) Scan(value interface{}) error {
	if value == nil {
		d.Decimal = decimal.NewFromInt(0)
		return nil
	}
	switch v := value.(type) {
	case float64:
		d.Decimal = decimal.NewFromFloat(v)
	case int64:
		d.Decimal = decimal.NewFromInt(v)
	case string:
		dec, err := decimal.NewFromString(v)
		if err != nil {
			return err
		}
		d.Decimal = dec
	case []byte:
		dec, err := decimal.NewFromString(string(v))
		if err != nil {
			return err
		}
		d.Decimal = dec
	default:
		return fmt.Errorf("cannot scan %%T into Decimal", value)
	}
	return nil
}

// Value 实现 driver.Valuer 接口，将 Decimal 转为字符串写入数据库。
func (d Decimal) Value() (driver.Value, error) {
	return d.Decimal.String(), nil
}

// ToFloat64 转换为 float64 类型。
func (d Decimal) ToFloat64() float64 {
	return d.Decimal.InexactFloat64()
}

// Add 返回当前值与另一值的和。
func (d Decimal) Add(other Decimal) Decimal {
	return Decimal{d.Decimal.Add(other.Decimal)}
}

// Sub 返回当前值减去另一值的差。
func (d Decimal) Sub(other Decimal) Decimal {
	return Decimal{d.Decimal.Sub(other.Decimal)}
}

// Mul 返回当前值与另一值的积。
func (d Decimal) Mul(other Decimal) Decimal {
	return Decimal{d.Decimal.Mul(other.Decimal)}
}

// Div 返回当前值除以另一值的商。
func (d Decimal) Div(other Decimal) Decimal {
	return Decimal{d.Decimal.Div(other.Decimal)}
}

// Cmp 比较两个 Decimal 值。返回 -1（d < other）、0（d == other）或 1（d > other）。
func (d Decimal) Cmp(other Decimal) int {
	return d.Decimal.Cmp(other.Decimal)
}

// Equals 判断两个 Decimal 值是否相等。
func (d Decimal) Equals(other Decimal) bool {
	return d.Decimal.Equal(other.Decimal)
}

// IsZero 判断当前值是否为零。
func (d Decimal) IsZero() bool {
	return d.Decimal.IsZero()
}

// IsPositive 判断当前值是否为正数。
func (d Decimal) IsPositive() bool {
	return d.Decimal.IsPositive()
}

// IsNegative 判断当前值是否为负数。
func (d Decimal) IsNegative() bool {
	return d.Decimal.IsNegative()
}

// Abs 返回当前值的绝对值。
func (d Decimal) Abs() Decimal {
	return Decimal{d.Decimal.Abs()}
}

// Round 四舍五入到指定小数位数。
func (d Decimal) Round(places int32) Decimal {
	return Decimal{d.Decimal.Round(places)}
}

// Max 返回两个 Decimal 值中的最大值。
func Max(a, b Decimal) Decimal {
	if a.Cmp(b) >= 0 {
		return a
	}
	return b
}

// Min 返回两个 Decimal 值中的最小值。
func Min(a, b Decimal) Decimal {
	if a.Cmp(b) <= 0 {
		return a
	}
	return b
}

// NewDecimalFromFloat64 从 float64 创建 Decimal。
func NewDecimalFromFloat64(f float64) Decimal {
	return Decimal{decimal.NewFromFloat(f)}
}

// NewDecimalFromString 从字符串解析创建 Decimal。
func NewDecimalFromString(s string) (Decimal, error) {
	d, err := decimal.NewFromString(s)
	return Decimal{d}, err
}

// NewDecimalFromInt64 从 int64 创建 Decimal。
func NewDecimalFromInt64(i int64) Decimal {
	return Decimal{decimal.NewFromInt(i)}
}

// NewDecimalFromDecimal 从 shopspring Decimal 创建 Decimal。
func NewDecimalFromDecimal(d decimal.Decimal) Decimal {
	return Decimal{d}
}
```

### 注意事项

- Go 中 `utils/decimal/` 的 package 声明使用 `decimalUtil` 别名，避免与 `decimal` 标准库名冲突。
- 业务模型字段应使用 `decimalUtil.Decimal` 类型，配合 GORM 的 `type:decimal(...)` 标签实现数据库映射。
- 金额计算必须使用 `decimalUtil.Decimal`，禁止使用 `float64` 直接进行金额运算。
- 创建 Decimal 的首选入口是 `NewDecimalFromString`（字符串解析，推荐用于外部输入）和 `NewDecimalFromInt64`（整数，推荐用于内部计算）。
- 关联 `database-query-rules` 的本地连接红线与 `database-schema-rules` 的字段映射规则。

## recipe 持续扩展示例框架

新增 recipe 的流程：

1. 在本文档中新增 `## <category>` 小节
2. 更新 Catalog 中对应条目的 `usage_recipes` 字段
3. 更新 `directory-usage-routing.md` 的 recipe 索引表
4. 运行 `placement_catalog.py guide --category <category> --language go` 验证

新增 recipe 的准入条件：

- 该工具包目录已稳定存在（非推测性）
- 已有至少 1 个真实项目的使用经验
- 关联 skill 的编码规则已明确
