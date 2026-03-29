# 测试目录落点样例

## 正例

### 正确的目录结构
```
项目根目录/
├── src/
│   ├── controllers/      # 业务代码，无测试资产
│   ├── services/         # 业务代码，无测试资产
│   └── utils/            # 业务代码，无测试资产
├── test/
│   ├── 2026-03-28_143022/
│   │   ├── 用户登录功能验证/
│   │   │   └── README.md
│   │   └── src/
│   │       └── service/
│   │           ├── user_login_test.go
│   │           └── fixtures/
│   │               └── user_data.json
│   ├── 2026-03-28_154511/
│   │   ├── 订单创建接口测试/
│   │   │   └── README.md
│   │   └── internal/
│   │       └── service/
│   │           └── create_order_test.go
│   ├── 2026-03-28_162033/
│   │   ├── 数据导出功能验证/
│   │   │   └── README.md
│   │   └── app/
│   │       └── export/
│   │           └── export_test.js
│   └── archive/
│       └── 2026-W12/
│           └── ...
```

### 正确的 README.md 内容示例
```markdown
# 用户登录功能验证

## 测试目的
验证用户登录功能的正常流程和异常场景。

## 执行方式
```bash
go test ./test/2026-03-28_143022/src/service
```

## 依赖数据
- `test/2026-03-28_143022/src/service/fixtures/user_data.json`
- 使用测试环境数据库

## 覆盖范围
- 正常登录成功
- 密码错误
- 用户不存在
- 账号被锁定

## 验证结论
✅ 所有测试用例通过，登录功能正常。
```

### 同一会话多次测试的正确做法
```
test/
├── 2026-03-28_143022/
│   └── 用户登录功能验证/
│       └── README.md
├── 2026-03-28_144511/
│   └── 用户注册功能验证/
│       └── README.md
└── 2026-03-28_150033/
    └── 用户信息修改功能验证/
        └── README.md
```

## 反例

### 错误的位置
- 把 `create-order-test.js` 直接放在仓库根目录。
- 把接口返回样例 JSON 放进 `src/controllers/`、`app/services/` 之类的生产目录。
- 把验证脚本命名成临时文件后长期留在 `scripts/` 或 `tmp/` 中。
- 把测试说明写到 `docs/`，但目录里没有对应测试代码和测试数据，导致说明与资产脱节。
- 把 Go 测试包直接放进中文目录，例如 `test/2026-03-28_143022/用户登录功能验证/service/login_test.go`。
- 在源码目录落地同包白盒测试文件，例如 `internal/service/order_service_test.go`。

### 错误的目录结构
```
项目根目录/
├── src/
│   ├── controllers/
│   │   └── test-login.js      # ❌ 测试脚本放在业务代码目录
│   ├── services/
│   │   └── mock-order.json    # ❌ Mock 数据放在业务代码目录
│   └── utils/
├── test-login.js               # ❌ 测试脚本放在根目录
├── test/
│   └── 2026-03-28_143022_用户登录功能验证/  # ❌ 时间戳根目录混入中文
│       └── service/
│           └── login_test.go
├── tmp-test/                   # ❌ 使用了错误的目录名
│   └── ...
└── tests/                      # ❌ 应该是 test/（单数）
    └── ...
```

### 缺少 README.md
```
test/
└── 2026-03-28_143022/
    └── internal/
        └── service/
            └── history_client_test.go   # ❌ 缺少中文说明目录和 README.md
```

### 多个测试混在一个目录
```
test/
└── 2026-03-28_143022/
    ├── 用户功能测试/
    │   └── README.md
    ├── internal/
    │   └── service/
    │       ├── login_test.go
    │       ├── register_test.go        # ❌ 不同独立测试混在一个时间戳根目录
    │       └── profile_test.go
```

### 白盒诉求的正确处理

- 诉求：需要访问 `internal/service/order_service.go` 中未导出逻辑。
- 错误做法：在 `internal/service/order_service_test.go` 同包落地白盒测试。
- 正确做法：先补 seam（导出接口/测试钩子/依赖注入点），再将测试文件放在 `test/<时间戳>/internal/service/order_service_test.go`。

## 判定示例

- 如果当前仓库没有 `test/` 目录，必须创建并使用它。
- 如果已有 `tests/`（复数）目录，建议逐步迁移到 `test/`（单数）。
- 如果当前测试资产只服务一个需求任务，应优先在该时间戳根目录内聚合，不要拆散到多个无关公共目录。
- 同一需求的多个独立测试验证，必须分别创建独立的时间戳根目录。
- 每个时间戳根目录都必须包含中文说明目录和 `README.md`，否则视为不完整。
- 对 Go 项目，任何会被 `go test ./...` 扫描到的测试包路径都必须保持 ASCII。
