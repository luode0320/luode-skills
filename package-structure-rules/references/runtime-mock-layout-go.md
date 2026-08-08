# Go 运行时 Mock 目录与装配契约

本文档定义 Go 后端和前后端同仓后端运行时 Mock 的唯一目录位置、入口选择器、装配桥和构建标签。它是 `package-structure-rules` 的运行时 Mock 专项事实源，目录检查以 Catalog 机器事实为准。

## 核心边界

- 根 `mock/` 是运行时 Mock 唯一合法根，独立后端和同仓后端均使用项目根下的 `mock/`。
- `mock/` 按 `internal/` 的相对路径镜像：`internal/business/scalp/api` 对应 `mock/business/scalp/api`。
- `mock/assembly/` 是绕开 Go `internal` 可见性的唯一装配桥，包名固定为 `assembly`。
- 根入口 `main.go` 同级按需配对 `main_mock.go` 与 `main_real.go`；额外二进制入口在 `cmd/<binary>/main.go` 同级配对。
- `main_mock.go` 使用 `//go:build mock`，`main_real.go` 使用 `//go:build !mock`；`main.go` 不携带 mock 标签。
- 每个可替换根依赖在两份 selector 中定义同名 `newXxx()`；`main.go` 只调用 selector，不直接判断 Mock。
- Mock 实现文件必须使用 `//go:build mock`，包名为 `mock_<源包名>`；assembly 包名固定为 `assembly`。
- 入口只能导入 `mock/assembly`，不得直接导入 `mock/business/...` 等实现包；生产代码不得导入运行时 Mock。
- 测试专用 Mock 继续放在根 `test/`，不与运行时 Mock 混用。

## 目录树

独立后端：

```text
<backend-project>/
├── main.go                         # 通用入口，只调用 newXxx() 选择器
├── main_mock.go                    # //go:build mock；mock selector
├── main_real.go                    # //go:build !mock；real selector
├── internal/
│   └── business/scalp/api/         # 被镜像的源码根
├── mock/
│   ├── assembly/
│   │   └── assembly.go             # package assembly；mock 装配桥
│   └── business/scalp/api/         # 镜像 internal 相对路径
│       └── gateway_mock.go         # package mock_<源包名>
└── test/                           # 测试专用 Mock，不属于运行时 Mock
```

前后端同仓后端：

```text
<fullstack-workspace>/
├── backend/
│   ├── main.go
│   ├── main_mock.go
│   ├── main_real.go
│   ├── internal/
│   │   └── business/scalp/api/
│   └── cmd/<binary>/main.go        # 额外二进制入口，同样配对 selector
├── mock/
│   ├── assembly/
│   │   └── assembly.go
│   └── business/scalp/api/
│       └── gateway_mock.go
└── test/
```

## 入口选择器

`main_mock.go` 与 `main_real.go` 必须同时存在，且与对应 `main.go` 同级。两份文件声明相同名称和签名的 `newXxx()` 函数，只通过装配桥选择 Mock 或真实实现：

```go
//go:build mock
package main

func newGateway(cfg *config.Config) (api.ExchangeGateway, error) {
    return assembly.NewExchangeGateway(cfg)
}
```

```go
//go:build !mock
package main

func newGateway(cfg *config.Config) (api.ExchangeGateway, error) {
    return api.NewFuturesGateway(cfg)
}
```

`main.go` 不得直接导入 `mock/` 下的实现包，只调用 `newXxx()`。

## Assembly 装配桥

`mock/assembly/` 是唯一允许直接导入 Mock 实现的目录级装配包，用于解决 Go `internal` 包只能被同 module 内路径导入的可见性限制。`mock/assembly` 包名固定为 `assembly`，文件必须使用 `//go:build mock`。

入口的 `main_mock.go` 可以导入 `mock/assembly`，不得直接导入 `mock/business/...` 或 `mock/internal/...` 下的实现包。

## 镜像与包名

`mock/` 下除 `assembly` 外的实现文件必须镜像 `internal/` 下的相对路径。`internal/business/scalp/api` 对应的 Mock 文件应位于 `mock/business/scalp/api`，且镜像源目录必须存在对应源码。

Mock 实现包名约定为 `mock_<源包名>`：源包为 `package api` 时，Mock 包为 `package mock_api`。`mock/assembly` 下的文件固定为 `package assembly`。

## 反例

- 缺少 `main_real.go` 或缺少 `main_mock.go`。
- `main_mock.go` 缺少 `//go:build mock`，或 `main_real.go` 缺少 `//go:build !mock`。
- 两份 selector 的 `newXxx()` 名称集合不一致。
- Mock 实现未镜像 `internal/` 相对路径，例如直接放在 `mock/random/`。
- Mock 文件缺少 `//go:build mock`。
- Mock 包名不是 `mock_<源包名>`，assembly 包名不是 `assembly`。
- 入口直接导入 `mock/business/...` 或 `mock/internal/...` 实现包。
- 生产代码（`main.go`、`main_real.go`）导入运行时 Mock。
- 运行时 Mock 文件放入 `internal/` 源码根。

## 构建与验证

合规项目必须同时通过普通构建和 Mock 构建：

```bash
go build -mod=vendor .
go build -tags mock -mod=vendor .
```

VSCode 调试配置中的 Mock 模式必须携带 `-tags=mock`，普通模式不得携带该标签；两种模式均使用 `-env=local` 本地环境，禁止连接 test/prod 或 live 交易服务。

## 边界说明

- 本文档只约束 Go 运行时 Mock 的位置与装配；Java、Node.js、Python 的 Mock 规则不由此文档扩展。
- 前端开发 Mock（如 `src/mocks/`）不受运行时 Mock 规则约束。
- 测试专用 Mock 属于根 `test/`，由 `test-strategy-rules` 治理。
- 目录检查保持只读，不自动创建、迁移、删除或改写 Mock 文件。
