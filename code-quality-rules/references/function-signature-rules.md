# 函数签名规则

## 用途

用于设计函数与方法的参数形态：参数顺序、数量控制，以及什么时候把参数收敛成结构体。

只约束“签名长什么样”，不约束函数内部步骤（见 `function-structure-rules.md`），也不约束排版与换行（见 `code-style-consistency-rules` 的 Go 函数签名风格约定）。

## 参数顺序

1. 上下文与接收对象放最前，例如 `ctx`、`tx`。
2. 必填的业务主参数居中。
3. 可选、配置、扩展类参数放最后，并默认收敛进结构体。

## 数量控制：硬性上限（参数与返回值 ≤ 2）

- **硬性上限**：函数参数和返回值均不得超过 2 个；一旦超过 2 个，必须改用结构体传参或返回。
- **参数收敛**：入参达到 3 个及以上时，必须定义结构体收敛传参（例如 `(ctx context.Context, params XxxParams)`）；只要出现可选参数、默认值或未来会扩展的字段，直接收敛为结构体。
- **返回值收敛**：返回值达到 3 个及以上时，必须定义结果结构体返回（例如 `(res XxxResult, err error)`），禁止直接返回 3 个及以上独立值。

## 独立参数/返回值 与 结构体 的取舍

保持独立参数/返回值：

- 参数数量 ≤ 2 个（例如单业务参数或 `ctx` + 业务主参数）；
- 返回值数量 ≤ 2 个（例如 `(data, error)` 或 `(bool, error)`）；
- 参数彼此独立，没有共同归属；
- 全部必填，没有默认值且短期内不扩展。

收敛为结构体：

- 参数超过 2 个（达到 3 个及以上）必须封装为参数结构体；
- 返回值超过 2 个（达到 3 个及以上）必须封装为结果结构体；
- 存在可选、默认值或扩展字段；
- 需要跨函数、跨层传递。

禁止：

- 参数超过 2 个时继续平铺位置参数；
- 返回值超过 2 个时散落返回多个零散变量；
- 用可变参数 `...T` 规避参数设计；变参只用于同质、不定长集合。

## 命名与注释

- 结构体参数命名：全必填用 `XxxParams`，含可选或配置项用 `XxxOptions`。
- 结构体返回值命名：用 `XxxResult` 或 `XxxResp`。
- 结构体与其字段的注释按 `comment-rules` 执行，本规则不重复。

## 正反例

### 1. 参数收敛

正例：参数超过 2 个时收敛为结构体（`ctx` 算第 1 个参数，`params` 算第 2 个参数，总数不超过 2 个）。

```go
type HandleStageFailureParams struct {
    OrderID  string
    Stage    string
    RetryMax int
}

func HandleStageFailure(ctx context.Context, params HandleStageFailureParams) error
```

反例：参数超过 2 个平铺展开。

```go
func HandleStageFailure(ctx context.Context, orderID string, stage string, retryMax int) error
```

### 2. 返回值收敛

正例：返回值超过 2 个时封装为结果结构体（结果结构体 + error 总数不超过 2 个）。

```go
type OrderSummaryResult struct {
    TotalAmount  int64
    SuccessCount int
    FailCount    int
}

func CalculateOrderSummary(ctx context.Context, orderID string) (*OrderSummaryResult, error)
```

反例：返回值超过 2 个散落多值返回。

```go
func CalculateOrderSummary(ctx context.Context, orderID string) (int64, int, int, error)
```

## 与相邻规则的边界

- 函数内部步骤、控制流与拆分：`function-structure-rules.md`。
- Go 参数单行与换行排版：`code-style-consistency-rules` 的 Go 函数签名风格约定。
- 参数结构体的注释与字段说明：`comment-rules`。
