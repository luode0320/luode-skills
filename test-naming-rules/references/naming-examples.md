# 测试命名正反例

## 正例

- 任务目录使用能表达业务目标的名称，如 `order-create-success/`、`refund-timeout-retry/`。
- 测试文件名称与测试对象和层级一致，如 `user-login.api.test.ts`、`cart-service.integration_test.go`。
- 测试数据目录直接表达场景用途，如 `fixtures/order-create/`、`mock/payment-callback/`。
- 共享资源目录突出公共属性，如 `shared-fixtures/`、`common-mocks/`。

## 反例

- `test1/`、`new-test/`、`final-case/`
- `data/`、`script/`、`case-a/` 这类无法表达业务目标的目录名
- 同一层级同时存在 `order_create_test.go`、`order-create.test.ts`、`orderCreateSpec.js`，但项目并没有混用规范
- 为了追求完整，把多个场景串成超长名称，导致阅读和检索成本过高

## 判定提示

- 如果项目已有统一后缀，例如 `.spec.ts`、`.test.ts`、`_test.go`，直接沿用，不重造后缀。
- 如果目录名已经表达了业务对象，文件名可以聚焦测试层级或子场景，避免重复堆词。
- 如果一个名称需要靠注释才能解释清楚，通常说明名称本身还不够稳定。
