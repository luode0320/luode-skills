# 归位审查正反例

## 正例

### 正例 1：service 留在业务层

- 业务组合逻辑放 service。
- repository 只做数据访问。
- 结论：职责与位置一致。

### 正例 2：通用目录先拆子目录

- `utils/log/logger.go`、`middleware/auth/middleware.go`、`global/config/provider.go`。
- 根目录只承担命名空间，不直接堆实现文件。
- 结论：通过。

### 正例 3：Go 测试文件不落源码目录

- `test/2026-03-29_201500/internal/service/order_service_test.go`。
- `internal/service/` 下没有同包 `*_test.go`。
- 结论：通过。

## 反例

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
- 命中 `test/` 外 `*_test.go` 禁放规则。
- 结论：驳回。
