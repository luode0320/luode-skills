# 归位检查清单

## 用途

用于检查当前文件和模块是否归属到正确位置。

## 检查项

- 文件是否放在正确目录。
- 模块职责是否与目录职责一致。
- 当前层是否承担了不属于自己的逻辑。
- 公共层代码是否夹带强业务语义。
- `utils`、`common`、`global`、`middleware` 根目录是否直接出现实现文件（如 `xx.go`）。
- Go `internal/service` 根目录是否直接堆业务实现文件，而未拆业务子目录。
- Go `internal/service` 实现文件是否散落请求/响应/第三方结果结构体（应归位 `internal/entity/<domain>/`）。
- Go 项目中，`test/` 外是否出现 `*_test.go`。
- 本轮重点业务文件是否达到 500 行及以上且仍在持续新增功能（命中时需拆分或给出拆分方案）。

## 原则

- 位置合理只是最低标准。
- 职责也必须对位。
- 公共根目录优先承担命名空间职责，具体实现优先放子目录。
- Go `internal/service` 默认先按业务域拆子目录，再放实现文件。
- Go 请求/响应/第三方结果结构体默认放 `internal/entity`，`internal/service` 只保留行为实现。
- Go 测试文件默认只允许落在 `test/` 根目录体系内。
- 500+ 行持续膨胀文件不应继续“就地堆方法”，应按功能职责拆到多文件，必要时拆子目录。

## Go 禁放扫描示例

- 扫描命令：`rg --files -g "*_test.go"`
- 判定命令（PowerShell）：`rg --files -g "*_test.go" | rg -v "^test/"`
- 判定规则：命中结果非空即未通过。

## Go 结构体归位扫描示例

- 扫描命令：`rg -n "^\s*type\s+[A-Za-z_][A-Za-z0-9_]*\s+struct\s*{" internal/service`
- 判定说明：命中后需人工判断是否为请求/响应/第三方结果结构体；该类结构体应迁移到 `internal/entity/<domain>/`。
