# 定义位置规则

## 用途

统一代码元素的定义位置：局部变量、包级变量与常量、函数。只约束“写在哪里”，不约束命名、声明形式与结构体分层。

## 局部变量：函数开头集中

- 函数或方法内的局部变量，默认在函数开头集中声明，不散落到分支或循环中间。
- 声明顺序与后续使用顺序一致，保证从上到下通读即可理解，不用回跳查找。
- 例外只限语言机制要求或极小临时变量：`for` 循环变量、`if` / `switch` 短声明、声明处即用且不再复用的临时值。
- 与 `code-style-consistency-rules` 的 Go 局部变量声明风格约定配套：那里约束“怎么声明”（逐行 `var`、禁止 `var (...)` 分组、注释列对齐），本规则约束“声明在哪里”。

## 包级变量与常量

- 包级变量与常量集中在文件顶部或专门的声明块，不散落在函数之间。
- 与某个类型强相关的常量，优先靠近该类型定义；是否单独成文件由 `package-structure-rules` 判定。

## 函数

- 在已有文件中新增函数时追加到文件末尾，不插入已有函数中间（既有规则，见可读性主线）。
- 拆分出的辅助函数紧随其唯一调用者之后；仅当被多处调用时，才上提到文件靠前位置。

## 正反例

反例：变量散落在分支与循环中，读时需要回跳。

```go
func ProcessOrder(order *Order) error {
    if order == nil {
        return errNilOrder
    }
    total := decimal.Zero
    for _, item := range order.Items {
        price := item.Price
        total = total.Add(price)
    }
    return save(total)
}
```

正例：变量在函数开头集中声明，按使用顺序排列。

```go
func ProcessOrder(order *Order) error {
    var total decimal.Decimal

    if order == nil {
        return errNilOrder
    }
    for _, item := range order.Items {
        total = total.Add(item.Price)
    }
    return save(total)
}
```

## 与相邻规则的边界

- 命名：`naming-rules`。
- 声明形式（逐行 `var`、禁止分组、注释列对齐）：`code-style-consistency-rules` 的 Go 局部变量声明风格约定。
- 结构体与类型定义的落点与分层：`package-structure-rules`。
- 函数签名设计（参数顺序、数量、取舍）：`function-signature-rules.md`。
