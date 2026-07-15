# TEST-06：局部统一风格正例

## 结论

PASS。规则资产能够把相邻重复注册行识别为高度统一的局部模板，并要求新增项只替换业务对象名称和必要中文说明。

## 输入样本

受控注册区段：

```go
func Init() {
    changelly.New().Start(true)     // 创建并注册交易所changelly
    swft.New().Start(true)          // 创建并注册交易所swft
    changenow.New().Start(true)     // 创建并注册交易所changenow
}
```

新增目标：`xx` 交易所。

预期新增内容：

```go
    xx.New().Start(true)            // 创建并注册交易所xx
```

## 命中规则

- `RULE-05`：局部稳定写法优先于个人偏好、外部模板和无关全局重构。
- `DEC-06`：局部风格证据顺序为当前文件、同目录、同模块、`PROJECT_STYLE.md`。
- `TASK-02-03`：识别局部统一风格并执行最小模板替换。

## 通过标准

- 保留 `.New().Start(true)` 调用结构。
- 保持注册区段的顺序、分组、空行、注释位置和排版。
- 不新增 helper、wrapper、factory、manager、临时变量、循环、额外日志、校验或无需求抽象。

## 实际结果

```text
TEST-06 PASS: 局部统一风格仅保留同构模板替换
```

## 失败预期

以下写法应被驳回并改回同构模板：

```go
    registerExchange("xx")
```

原因：引入了局部区段不存在的 helper 和陌生调用结构。

## 清理与回滚

样本仅在内存中构造，未写入业务代码和外部环境；无数据清理。若规则未通过，回滚范围为 `TASK-02-03` 对应 reference、checklist 和 `SKILL.md` 新增段。

## 追踪

`SRC-STYLE-FB-04 -> REQ-07/RULE-05 -> AC-06 -> CYCLE-02 -> TASK-02-03 -> TEST-06 -> EVD-02-03-LOCAL-STYLE`
