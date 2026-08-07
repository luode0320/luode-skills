# Go 编码规则清单

## 用途

用于沉淀团队在 Go 编码中反复出现、需要显式约束的局部编码规则。

## 规则格式

后续新增规则统一使用 bullet 追加：

- 规则内容。

## 当前规则

- 字符串去除首尾空格不是默认防御动作；只有业务规则明确要求输入归一化、外部数据已知存在首尾脏空格、或比较 / 判空 / 入库前必须统一口径时，才使用 `strings.TrimSpace`。
- 禁止在没有明确必要性的情况下，对 `item.ID`、`order.TxHash` 等字段随手包裹 `strings.TrimSpace(...)`；这类多余操作会隐藏真实数据形态，也会增加无意义的代码噪音。
- Go 常量和枚举禁止使用 `iota`，必须显式写出每个常量值；可视化和长期维护优先于少写几行代码。
- 根 `utils/` 下的工具包目录名与 Go 标准库包名冲突时（如 `time`、`json` 对应 `encoding/json`、`log`、`http` 对应 `net/http`），目录名保持不变，但该目录内 `.go` 文件的 `package` 声明必须使用带 `Util` 后缀的别名（`package timeUtil`、`package jsonUtil`、`package logUtil`、`package httpUtil`），避免调用方同时导入标准库和本工具包时出现标识符冲突。
- `utils/cron` 不与标准库冲突，但为了和上述几个工具包保持统一的 `xxxUtil` 内部命名风格，同样使用别名 `package cronUtil`；其余目录（如 `async`、`convert`）package 名与目录名保持一致，不强制加 `Util` 后缀。
- Go 函数或方法内部禁止使用 `var (...)` 分组声明局部变量，必须逐行单独 `var` 声明（如 `var bestGap int64`）；多条相邻声明的行尾中文注释按列对齐。本条只约束函数/方法内局部变量，不改动包级 `var (...)` 历史写法。
