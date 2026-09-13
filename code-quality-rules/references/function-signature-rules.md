# 函数签名规则

## 用途

用于设计函数与方法的参数形态：参数顺序、数量控制，以及什么时候把参数收敛成结构体。

只约束“签名长什么样”，不约束函数内部步骤（见 `function-structure-rules.md`），也不约束排版与换行（见 `code-style-consistency-rules` 的 Go 函数签名风格约定）。

## 参数顺序

1. 上下文与接收对象放最前，例如 `ctx`、`tx`。
2. 必填的业务主参数居中。
3. 可选、配置、扩展类参数放最后，并默认收敛进结构体。

## 数量控制：以语义为准

- 不以固定数字作为唯一标准，优先判断参数是否“同源”，即是否属于同一业务对象或同一次操作。
- 同源参数达到 3 个及以上时，建议收敛为结构体。
- 只要出现可选参数、默认值或未来会扩展的字段，就直接收敛为结构体，不再继续追加位置参数。

## 单参数 与 结构体参数 的取舍

保持独立参数：

- 参数彼此独立，没有共同归属；
- 全部必填，没有默认值；
- 短期内不会扩展；
- 所有调用点用法一致。

收敛为结构体参数：

- 同源参数达到 3 个及以上；
- 存在可选、默认值或扩展字段；
- 这组参数需要跨函数、跨层传递；
- 参数会随需求演进，需要保持签名稳定。

禁止：

- 参数只有 1-2 个时硬造结构体，属过度封装，按主线 1 的反对项处理；
- 用可变参数 `...T` 规避参数设计；变参只用于同质、不定长集合。

## 命名与注释

- 结构体参数命名：全必填用 `XxxParams`，含可选或配置项用 `XxxOptions`。
- 结构体与其字段的注释按 `comment-rules` 执行，本规则不重复。

## 正反例

正例：同源参数 3 个及以上时收敛为结构体。

```go
type HandleStageFailureParams struct {
    OrderID  string
    Stage    string
    RetryMax int
}

func HandleStageFailure(ctx context.Context, params HandleStageFailureParams) error
```

反例：同源参数堆叠，还混入可选开关。

```go
func HandleStageFailure(ctx context.Context, orderID, stage string, retryMax int, withNotify bool) error
```

## 与相邻规则的边界

- 函数内部步骤、控制流与拆分：`function-structure-rules.md`。
- Go 参数单行与换行排版：`code-style-consistency-rules` 的 Go 函数签名风格约定。
- 参数结构体的注释与字段说明：`comment-rules`。
