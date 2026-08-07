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
