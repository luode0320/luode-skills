# 测试命名正反例

## 铁律正例：目录结构

```
项目根目录/
├── src/                    # 业务代码目录（禁止存放测试资产）
├── test/                   # 统一测试根目录（必须使用）
│   ├── 2026-03-28_143022/
│   │   ├── 用户登录功能验证/
│   │   │   └── README.md
│   │   └── internal/
│   │       └── service/
│   │           ├── history_client_test.go
│   │           └── fixtures/
│   │               └── history_client_response.json
│   ├── 2026-03-28_154511/
│   │   ├── 订单创建接口测试/
│   │   │   └── README.md
│   │   └── api/
│   │       └── order/
│   │           └── create_order_test.go
│   └── archive/             # 旧测试归档目录
│       └── 2026-W12/
│           └── ...
```

## 正例

- 时间戳根目录使用 `yyyy-MM-DD_HHmmss` 格式，如 `2026-03-28_143022`、`2026-03-28_154511`。
- 中文说明目录使用测试任务中文简介，如 `用户登录功能验证/`、`订单创建接口测试/`。
- 测试文件名称与测试对象和层级一致，如 `user-login.api.test.ts`、`cart-service.integration_test.go`。
- 测试数据目录直接表达场景用途，如 `fixtures/order-create/`、`mock/payment-callback/`。
- 共享资源目录突出公共属性，如 `shared-fixtures/`、`common-mocks/`。
- 所有测试资产统一放在 `test/` 根目录下。
- 每个时间戳根目录都包含中文说明目录和其中的 README.md，说明测试目的、执行方式、依赖数据、覆盖范围和验证结论。
- 对 Go 项目，参与编译的路径保持 ASCII，例如 `test/2026-03-28_143022/internal/service/history_client_test.go`。
- 同一会话的多次测试分别创建独立目录，不混在一起。

## 反例

### 目录结构反例

```
项目根目录/
├── src/
│   ├── controllers/
│   │   └── test-login.js      # ❌ 测试脚本放在业务代码目录
│   └── services/
│       └── mock-order.json    # ❌ Mock 数据放在业务代码目录
├── test-login.js               # ❌ 测试脚本放在根目录
├── tmp-test/                   # ❌ 使用了错误的目录名
│   └── ...
└── tests/                      # ❌ 应该是 test/（单数）
    └── ...
```

### 命名反例

- `test1/`、`new-test/`、`final-case/`、`temp/`。
- `data/`、`script/`、`case-a/` 这类无法表达业务目标的目录名。
- 同一层级同时存在 `order_create_test.go`、`order-create.test.ts`、`orderCreateSpec.js`，但项目并没有混用规范。
- 为了追求完整，把多个场景串成超长名称，导致阅读和检索成本过高。
- 时间戳根目录不使用 `yyyy-MM-DD_HHmmss` 格式，如 `用户登录测试/`、`order-test/`。
- 测试资产放在 `tests/`、`qa/`、`verify/`、`tmp-test/` 等非 `test/` 根目录下。
- 缺少中文说明 README.md 的时间戳根目录。
- 把 Go 测试文件放进中文目录，如 `test/2026-03-28_143022/用户登录功能验证/history_client_test.go`。
- 多个测试混在一个时间戳根目录中，如 `2026-03-28_143022/` 同时承载登录、注册、修改等多个独立测试。

## 判定提示

- 如果项目已有统一后缀，例如 `.spec.ts`、`.test.ts`、`_test.go`，直接沿用，不重造后缀。
- 如果目录名已经表达了业务对象，文件名可以聚焦测试层级或子场景，避免重复堆词。
- 如果一个名称需要靠注释才能解释清楚，通常说明名称本身还不够稳定。
- 时间戳根目录必须使用 `yyyy-MM-DD_HHmmss` 格式，中文说明目录单独承担中文描述。
- 会被 Go 编译的路径不得包含中文，这是铁律，没有例外。
- 所有测试相关的任何数据文件、说明，都必须统一在 `test/` 目录下。
