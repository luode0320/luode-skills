# 归位与依赖方向检查

## 用途

用于定义 `implementation-review-rules` 内置的目录归位、职责对位、依赖方向与 Go 特定落点闸门。

## 归位检查项

- 文件是否放在正确目录。
- 模块职责是否与目录职责一致。
- 当前层是否承担了不属于自己的逻辑。
- 公共层代码是否夹带强业务语义。
- `utils`、`common`、`global`、`middleware` 根目录是否直接出现实现文件。
- Go `internal/service` 根目录是否直接堆业务实现文件，而未拆业务子目录。
- Go `internal/service` 实现文件是否散落请求 / 响应 / 第三方结果结构体。
- Go 项目中，`doc/5-tests/` 外是否出现 `*_test.go`。
- 本轮重点业务文件是否达到 500 行及以上且仍在持续新增功能。

## 依赖方向常见问题

- 入口层被数据层反向依赖
- 公共层依赖业务层
- 测试代码泄漏回生产代码层
- 数据访问层承载业务编排

## 处理原则

- 位置合理只是最低标准，职责也必须对位。
- 依赖应尽量单向，反向依赖和循环依赖优先视为结构问题。
- 公共根目录优先承担命名空间职责，具体实现优先放子目录。
- Go `internal/service` 默认先按业务域拆子目录，再放实现文件。
- Go 请求 / 响应 / 第三方结果结构体默认放 `internal/entity`，`internal/service` 只保留行为实现。
- Go 测试文件默认只允许落在 `doc/5-tests/` 根目录体系内。
- 500+ 行持续膨胀文件不应继续就地堆方法，应按功能职责拆到多文件，必要时拆子目录。

## 扫描示例

- Go 禁放测试扫描：`rg --files -g "*_test.go" | rg -v "^doc/5-tests/"`
- Go 服务层结构体扫描：`rg -n "^\\s*type\\s+[A-Za-z_][A-Za-z0-9_]*\\s+struct\\s*{" internal/service`

## 正反例

### 正例 1：service 留在业务层

- 业务组合逻辑放 service。
- repository 只做数据访问。
- 结论：职责与位置一致。

### 正例 2：通用目录先拆子目录

- `utils/log/logger.go`、`middleware/auth/middleware.go`、`global/config/provider.go`。
- 根目录只承担命名空间，不直接堆实现文件。
- 结论：通过。

### 正例 3：Go 服务层按业务子目录分层

- `internal/service/order/create.go`、`internal/service/user/profile.go`。
- `internal/service/` 根目录不直接堆业务实现文件。
- 结论：通过。

### 正例 4：Go 测试文件不落源码目录

- `doc/5-tests/2026-03-29_201500/internal/service/order_service_test.go`。
- `internal/service/` 下没有同包 `*_test.go`。
- 结论：通过。

### 正例 5：500+ 行文件按职责拆分

- 原 `internal/service/order/process.go` 已超过 500 行。
- 本轮将“校验”“编排”“回写”拆为 `validate.go`、`workflow.go`、`persist.go`，并保持同一业务子目录。
- 结论：通过。

### 正例 6：Go 结构体归位到 `internal/entity`

- `internal/service/order/create.go` 仅保留服务编排与方法逻辑。
- 请求 / 响应结构体迁移到 `internal/entity/order/create_entity.go`。
- 结论：通过。

### 反例 1：repository 里写业务编排

- 位置在数据层，职责却已越界到业务层。
- 结论：驳回。

### 反例 2：utils 里塞订单专属逻辑

- 目录看似公共层，实际强依赖订单业务语义。
- 结论：驳回。

### 反例 3：公共根目录直接放实现文件

- 直接新增 `utils/string.go`、`common/cache.go`、`global/config.go`、`middleware/auth.go`。
- 目录层级过平，职责边界不清，容易引发命名冲突和循环依赖。
- 结论：驳回。

### 反例 4：Go 测试文件落在禁放目录

- 在 `internal/service/order_service_test.go` 直接新增同包白盒测试文件。
- 命中 `doc/5-tests/` 外 `*_test.go` 禁放规则。
- 结论：驳回。

### 反例 5：Go 服务层大平层堆叠

- `internal/service/create_order.go`、`internal/service/cancel_order.go`、`internal/service/refund_order.go` 等大量业务实现都放在根目录。
- 结论：驳回，先按业务域拆子目录。

### 反例 6：500+ 行文件继续堆功能

- 单文件已经超过 500 行，本轮仍继续新增多个方法和流程分支。
- 未执行拆分，也未给出本轮可落地拆分方案。
- 结论：驳回。

### 反例 7：service 文件散落结构体定义

- 在 `internal/service/order/create.go` 中定义请求 / 响应 / 第三方结果 `type Xxx struct`。
- 结论：驳回，迁移到 `internal/entity/<domain>/` 后再继续。
