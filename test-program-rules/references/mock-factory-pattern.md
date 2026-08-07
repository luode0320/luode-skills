# Mock 工厂模式 — 依赖注入与构建标签装配

本文档定义运行时 Mock 的依赖注入（DI）工厂模式，提供标准的构建标签装配方案，使 Go 后端项目在本地开发时通过 `-tags mock` 编译运行时 Mock，在生产构建时自动排除。

## 问题背景

Go 后端项目经常需要连接交易所、推送服务、数据库等真实上游。本地开发时这些上游可能不可用，需要通过 Mock 替代。传统做法有缺陷：

1. **源码目录内放 mock**：`internal/business/scalp/api/mock_gateway.go` 污染生产代码，线上构建仍需排除。
2. **运行时分支判断**：`if cfg.TradingMode == Mock` 在 main 中引入运行时分支，实际只在本地开发有用，增加线上路径复杂度。
3. **测试 Mock 与运行时 Mock 混用**：测试 Mock 放进 `test/`，运行时 Mock 放在源码目录，职责不清。

## 推荐方案：构建标签 + 工厂函数

### 架构示意

```
main.go 或 cmd/<binary>/main.go
├── //go:build mock     → newGateway() 返回 mock_api.NewMockGateway()
├── //go:build !mock    → newGateway() 返回 api.NewFuturesGateway(cfg)
└── 调用方（service）    → 统一接收 ExchangeGateway 接口
```

### 模板

**生产工厂（main_real.go）**：

```go
//go:build !mock

package main

import (
    "binance-wangge-go/config"
    "binance-wangge-go/internal/business/scalp/api"
)

func newGateway(cfg *config.Config) (api.ExchangeGateway, error) {
    if err := cfg.Validate(); err != nil {
        return nil, err
    }
    return api.NewFuturesGateway(cfg)
}
```

**Mock 工厂（main_mock.go）**：

```go
//go:build mock

package main

import (
    "binance-wangge-go/config"
    mock_api "binance-wangge-go/mock/internal/business/scalp/api"
)

func newGateway(cfg *config.Config) (api.ExchangeGateway, error) {
    if err := cfg.Validate(); err != nil {
        return nil, err
    }
    return mock_api.NewMockGateway(), nil
}
```

**main.go 调用方**：

```go
package main

func main() {
    cfg := config.Load()
    gateway, err := newGateway(cfg)  // 自动选择实现
    if err != nil {
        panic(err)
    }
    // 使用 gateway
}
```

### 与 `go:build` 标签搭配的惯用文件名

| 文件名 | 构建条件 | 用途 |
|--------|----------|------|
| `main.go` | 无条件 | 共享的 main 入口和通用逻辑 |
| `main_real.go` | `!mock` | 生产工厂实现 |
| `main_mock.go` | `mock` | Mock 工厂实现 |

或者使用一个文件 + 条件块：

```go
//go:build mock

package main

// 工厂函数
```

```go
//go:build !mock

package main

// 工厂函数
```

两种模式均可，选择标准：**当工厂函数较多（3+ 个）时，建议分开文件**；当只有 1-2 个工厂时，一个文件放两个标签块更简洁。

## 多工厂场景

当项目需要多个上游 Mock 时，按以下方式组织：

### 文件结构（推荐分文件）

```
main.go              # 共享 main 入口
internal/
├── factory/
│   ├── factory.go      # 工厂接口定义
│   ├── factory_real.go # //go:build !mock
│   └── factory_mock.go # //go:build mock
```

### 工厂接口定义

```go
// internal/factory/factory.go

package factory

import (
    "binance-wangge-go/config"
    "binance-wangge-go/internal/business/scalp/api"
    "binance-wangge-go/internal/notification"
)

type AppFactories struct {
    NewGateway    func(cfg *config.Config) (api.ExchangeGateway, error)
    NewNotifier   func(cfg *config.Config) (notification.Notifier, error)
}
```

### 统一工厂函数

```go
//go:build !mock
// internal/factory/factory_real.go

package factory

import (
    "binance-wangge-go/config"
    "binance-wangge-go/internal/business/scalp/api"
    "binance-wangge-go/internal/notification"
)

func NewAppFactories(cfg *config.Config) (*AppFactories, error) {
    if err := cfg.Validate(); err != nil {
        return nil, err
    }
    gateway, err := api.NewFuturesGateway(cfg)
    if err != nil {
        return nil, err
    }
    notifier, err := notification.NewEmailNotifier(cfg)
    if err != nil {
        return nil, err
    }
    return &AppFactories{
        NewGateway:  func(cfg *config.Config) (api.ExchangeGateway, error) { return gateway, nil },
        NewNotifier: func(cfg *config.Config) (notification.Notifier, error) { return notifier, nil },
    }, nil
}
```

```go
//go:build mock
// internal/factory/factory_mock.go

package factory

import (
    "binance-wangge-go/config"
    "binance-wangge-go/internal/business/scalp/api"
    "binance-wangge-go/internal/notification"
    mock_api "binance-wangge-go/mock/internal/business/scalp/api"
    mock_notification "binance-wangge-go/mock/internal/notification"
)

func NewAppFactories(cfg *config.Config) (*AppFactories, error) {
    if err := cfg.Validate(); err != nil {
        return nil, err
    }
    return &AppFactories{
        NewGateway:  func(cfg *config.Config) (api.ExchangeGateway, error) { return mock_api.NewMockGateway(), nil },
        NewNotifier: func(cfg *config.Config) (notification.Notifier, error) { return mock_notification.NewMockNotifier(), nil },
    }, nil
}
```

## 常见问题

### Q: 为什么不用 `if cfg.TradingMode == Mock` 运行时分支？

运行时分支把本地开发决策带入生产执行路径，增加线上代码的复杂度测试面。构建标签由编译期决定，生产构建天然不包含 mock 代码，零运行时开销。

### Q: 工厂函数可以放在 `internal/` 下吗？

可以。工厂函数本身不是 Mock，属于装配逻辑，放在 `internal/factory/` 或 `internal/assembly/` 均可。Mock 包本身必须放在根 `mock/`。

### Q: 需要 mock 的服务很多，每个文件都要写两个标签块？

当需要 mock 的接口超过 3 个时，建议使用统一工厂（`AppFactories` 结构体）模式，避免每个 main 函数都写条件编译。

### Q: 运维配置中 TradimgMode 还需要保留吗？

如果项目需要在运行时动态切换模式（如支持 mock/testnet/live 通过配置文件切换），则 `TradingMode` 仍然保留，但此时构建标签只解决"本地开发默认编译为 mock 模式"的需求，不替代运行时配置。两种方式可以共存：`go build -tags mock .` 默认进入 mock 模式，但配置仍可通过 `-env` 参数覆盖。

## 与其他模式的关系

| 模式 | 用途 | 与 Mock 工厂的关系 |
|------|------|-------------------|
| 测试 Mock（`test/`） | `*_test.go` 测试期替换依赖 | 独立，测试代码内部注入 |
| 运行时 Mock（`mock/`） | 本地开发编译进主二进制 | 由工厂函数按构建标签选择 |
| 接口抽象（`types.go`） | 定义 ExchangeGateway 接口 | 工厂函数依据接口类型返回实现 |
| 依赖注入 | 运行时注入实现 | 与构建标签正交，可组合使用 |

## Go internal 可见性限制与装配层

**关键发现**：Go 的 `internal` 包可见性规则会影响根 `mock/` 的使用。

### 规则

- `mock/internal/...` → 可以导入 `internal/...`（前缀匹配）
- `main.go`（module 根）→ 不可以直接导入 `mock/internal/...`（前缀不匹配）

### 解决方案：mock/assembly 装配层

在 `mock/assembly/` 下创建装配层包，由它转发调用：

```
mock/assembly/assembly.go   //go:build mock — 导入 mock/internal/...，暴露公开工厂
main_mock.go                //go:build mock — 调用 mock/assembly.NewExchangeGateway()
```

### 完整文件示例

**mock/assembly/assembly.go**：

```go
//go:build mock

package assembly

import (
    config "binance-wangge-go/config"
    binance "binance-wangge-go/internal/business/scalp/api"
    mock_api "binance-wangge-go/mock/internal/business/scalp/api"
)

func NewExchangeGateway(cfg *config.Config) (binance.ExchangeGateway, error) {
    if err := cfg.Validate(); err != nil {
        return nil, err
    }
    return mock_api.NewMockGateway(), nil
}
```

**main_mock.go**：

```go
//go:build mock

package main

import (
    config "binance-wangge-go/config"
    binance "binance-wangge-go/internal/business/scalp/api"
    "binance-wangge-go/mock/assembly"
)

func newGateway(cfg *config.Config) (binance.ExchangeGateway, error) {
    return assembly.NewExchangeGateway(cfg)
}
```

### 与 `internal/factory/` 模式对比

| 方案 | 适用场景 | 优点 | 缺点 |
|------|----------|------|------|
| `mock/assembly/` | 单一主入口 | 简单直接，装配层在 mock/ 下 | 需额外文件 |
| `internal/factory/` | 多工厂、多接口 | 集中管理所有工厂 | 工厂代码在源码目录 |
| `main_real.go` + `main_mock.go` | 仅 1-2 个工厂 | 最简洁，不额外建包 | 工厂函数直接返回实现，不灵活 |

两者可以共存：`mock/assembly` 负责绕过 internal 限制，工厂函数本身仍可放在 `internal/factory/`。

