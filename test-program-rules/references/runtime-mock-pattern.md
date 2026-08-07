# 运行时 Mock 模式

本文件定义运行时 Mock（本地开发编译进主二进制、替代不可用真实上游的模拟实现）的目录、命名、构建标签与迁移指南。运行时 Mock 与测试 Mock 职责分离，由根 `mock/` 独立管理。

## 与测试 Mock 的关系

| 维度 | 测试 Mock | 运行时 Mock |
|---|---|---|
| 用途 | 仅 `*_test.go` 测试期替换依赖 | 本地开发编译进主二进制，替代不可用上游 |
| 目录 | 根 `test/` 源码镜像 | 根 `mock/` 源码镜像 |
| 构建 | 仅测试编译 | `//go:build mock` 条件编译 |
| 包名 | 外部 `<target>_test` 包 | `mock_<源包名>` |
| 生命周期 | 测试资产，随测试维护 | 本地开发资产，随主程序维护 |
| 选择方式 | 测试代码注入 | 工厂函数按构建标签选择 |

## 目录结构

```
F:\binance-wangge-go/
├── internal/
│   └── business/
│       └── scalp/
│           └── api/
│               ├── gateway.go      # 真实实现
│               └── types.go        # 接口/类型定义
├── mock/                            # [条件·提交] 运行时 Mock 根
│   └── internal/
│       └── business/
│           └── scalp/
│               └── api/
│                   └── gateway.go  # //go:build mock，包名 mock_api
├── test/
│   └── internal/
│       └── business/
│           └── scalp/
│               └── api/
│                   ├── gateway_test.go      # 测试代码
│                   └── gateway_mock.go      # 测试 Mock（仅 *_test.go 使用）
├── main.go
```

## 构建标签

- 单个文件：

```go
//go:build mock

package mock_api
```

- 运行：`go run -tags mock .`
- 构建：`go build -tags mock .`
- 调试：`.vscode/launch.json` 配置 `"buildFlags": "-tags=mock -mod=vendor"`
- 测试：`go test ./test/...`（不携带 `-tags mock`，运行时 Mock 默认不参与测试编译）
- 验证排除：`go list -tags mock ./...` 应能解析全部 mock 包；`go list ./...` 不应包含 `mock/` 下的包。

## 包名约定

- 被测源码包 `api` -> 运行时 Mock 包 `mock_api`
- 被测源码包 `service` -> 运行时 Mock 包 `mock_service`
- 被测源码包 `gateway` -> 运行时 Mock 包 `mock_gateway`
- 文件命名后缀与测试 Mock 一致：`_mock.go`、`_stub.go`、`_fake.go`

## 工厂函数 / 依赖注入切换

推荐在 `main` 或装配层使用构建标签选择实现：

```go
//go:build mock

package main

func newGateway(cfg *config.Config) (api.ExchangeGateway, error) {
    return mock_api.NewMockGateway(), nil
}
```

```go
//go:build !mock

package main

func newGateway(cfg *config.Config) (api.ExchangeGateway, error) {
    return api.NewFuturesGateway(cfg)
}
```

工厂函数必须满足以下约束：

- 两个实现必须保持相同的函数签名、错误语义和调用方视角。
- 生产工厂只能依赖真实实现，mock 工厂只能依赖 `mock/` 包。
- 装配层不允许出现 `if TradingMode == Mock` 这类运行时分支；模式选择完全由构建标签完成。
- 若 mock 工厂需要配置对象，仍应传入 `cfg` 并校验，保证调用方契约一致。

### Go internal 可见性注意事项

- `mock/` 下的包（如 `mock/internal/business/scalp/api`）可以正常导入 `internal/...`，因为 Go `internal` 规则检查的是**导入者路径的模块前缀**：`mock/internal/...` 的模块前缀是 `binance-wangge-go/mock/`，而 `internal/...` 的父目录是 `binance-wangge-go/`，前缀匹配，所以允许。
- 但 module 根（如 `main.go`）不可以直接导入 `mock/internal/...`，因为 main 的模块前缀是 `binance-wangge-go`，而 `mock/internal/...` 需要调用者前缀为 `binance-wangge-go/mock/`，前缀不匹配，Go 编译器拒绝。
- 解决方法：在 `mock/assembly/` 下创建装配层，由它导入 `mock/internal/...`，再由 `main_mock.go` 调用 `mock/assembly`。

### 推荐文件结构（含装配层）

```
F:\binance-wangge-go/
├── main.go                    # 共享 main 入口
├── main_real.go               # //go:build !mock — 生产工厂
├── main_mock.go               # //go:build mock  — 调用 mock/assembly
├── mock/                      # 运行时 Mock 根
│   ├── assembly/
│   │   └── assembly.go        # //go:build mock — 装配层，绕开 internal 限制
│   └── internal/
│       └── business/
│           └── scalp/
│               └── api/
│                   └── gateway_mock.go  # //go:build mock，包名 mock_api
├── internal/
│   └── business/scalp/api/
│       ├── gateway.go         # 真实实现
│       ├── types.go           # 接口/类型定义
│       └── mock_gateway.go    # 测试 Mock（仅 *_test.go 使用）
├── test/
│   └── internal/business/scalp/api/
│       ├── gateway_test.go    # 测试代码
│       └── gateway_mock.go    # 测试 Mock（可选）
```

## 接口契约要求

运行时 Mock 必须实现被测源码声明的接口，并对接口契约负责：

- 新增接口方法时，mock 包必须同步实现，否则 `go build -tags mock ./...` 在装配处失败关闭。
- mock 的返回类型、错误条件、幂等语义应与真实实现保持一致，避免本地环境出现测试环境漂移。
- 需要确定性能力（时间、K 线、权益、持仓）时，通过公开 setter（如 `SetClock`）注入，不写死内部状态。
- mock 内部可变状态必须使用互斥锁保护，避免并发读写竞争。

## 边界与不适用场景

- 运行时 Mock 只用于本地开发联调和无法访问真实上游的演示环境，不用于线上发布。
- 生产镜像构建不得携带 `-tags mock`。
- 运行时 Mock 不替代真实接口契约测试；接口行为差异仍由根 `test/` 的测试 Mock 和契约测试覆盖。
- 前端既有 `mocks/`（复数）保持不变，本规则只约束后端 `mock/`（单数）。

## .vscode mock 调试配置

```json
{
  "name": "Debug binance-wangge-go (mock)",
  "type": "go",
  "request": "launch",
  "mode": "debug",
  "program": "${workspaceFolder}",
  "cwd": "${workspaceFolder}",
  "buildFlags": "-tags=mock -mod=vendor",
  "args": ["-env=local"],
  "console": "integratedTerminal"
}
```

## 迁移指南

将现有 `internal/business/scalp/api/mock_gateway.go` 迁移到根 `mock/`：

1. 在 `mock/internal/business/scalp/api/` 创建包目录。
2. 将文件内容复制并改包名为 `mock_api`。
3. 文件头追加 `//go:build mock`。
4. 将 `NewExchangeGateway` 或装配层按构建标签切换实现。
5. 删除源码目录 `internal/business/scalp/api/mock_gateway.go`。
6. 验证：`go build ./...`（无 mock 标签应失败于缺少 mock 引用，或无 mock 引用则通过）；`go build -tags mock ./...` 应通过。
7. 验证：`go test ./test/...` 不携带 `-tags mock`，运行时 Mock 不参与测试编译。
8. 验证：`git status` 确认源 mock 文件已删除、根 `mock/` 文件已新增，无残留副本。
9. 若原 mock 文件被测试代码引用，必须先迁移测试引用到根 `test/` 的测试 Mock，再删除源码内 mock。
