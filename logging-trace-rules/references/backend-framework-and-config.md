# 后端日志框架与配置要求

## 核心约束

- 后端日志禁止使用控制台打印（例如 `fmt.Println`、`println`、`console.log`）。
- 后端日志必须通过项目统一日志框架输出。
- Go 服务默认使用 `go.uber.org/zap`（通过项目 `utils/log/` 封装统一调用）。
- Go 日志框架实现目录统一为 `utils/log/`，禁止在其他目录重复实现一套 logger。
- 日志必须配置化管理，禁止在业务代码里硬编码日志级别、文件路径和轮转参数。
- 日志初始化必须在 `LoadConfig` 之后执行，禁止在配置加载前初始化。
- 日志初始化只能执行一次，禁止多处重复初始化。
- 禁止使用空配置做预初始化（例如 `Init(config.LogConfig{})`）。

## 初始化顺序要求（强制）

推荐顺序：

1. `LoadConfig` 读取配置文件。
2. 从配置对象中取 `LogConfig`。
3. 执行一次 `InitLogger(logConfig)`。
4. 业务代码统一调用 logger，不再初始化。

## Go 初始化示例

```go
package main

import (
    "finance-go/config"
    "finance-go/utils/log"
)

func main() {
    cfg, err := config.LoadConfig()
    if err != nil {
        panic(err)
    }

    if err := log.Init(cfg.LogConfig); err != nil {
        panic(err)
    }

    // 之后统一使用 log.Infof / log.Errorf，不再重复 Init
}
```

## 禁止示例

```go
// ❌ 禁止：配置加载前用空配置预初始化
log.Init(config.LogConfig{})

cfg, _ := config.LoadConfig()
// ❌ 禁止：重复初始化
log.Init(cfg.LogConfig)
```

## Go 推荐调用方式

优先使用项目封装的 logger（示例）：

```go
import "finance-go/utils/log"

func CreateOrder(req *CreateOrderReq) error {
    log.Infof("########################### 创建订单开始: [%s]", req.OrderId)
    // ...
    log.Infof("########################### 创建订单结束: [%s]", req.OrderId)
    return nil
}
```

若需直接说明底层框架，可在初始化层明确 `zap`，业务层仍建议走封装：

```go
import "go.uber.org/zap"

func newLogger() (*zap.Logger, error) {
    cfg := zap.NewProductionConfig()
    cfg.Level = zap.NewAtomicLevelAt(zap.InfoLevel)
    return cfg.Build()
}
```

## 配置文件要求

日志配置至少包含以下字段（示例）：

```yaml
logConfig:
  level: INFO
  maxBackup: 100
  fileName: app.log
  filePath: log/finance-go
  sizeMB: 256
  reqLoggerMiddware: true
  enableSqlLog: true
  enableLog2Stdout: false
```

## 字段说明

- `level`: 日志级别。
- `maxBackup`: 滚动文件最大保留数量。
- `fileName`: 日志文件名。
- `filePath`: 日志输出目录。
- `sizeMB`: 单文件滚动阈值（MB）。
- `reqLoggerMiddware`: 是否启用请求日志中间件。
- `enableSqlLog`: 是否启用 SQL 日志。
- `enableLog2Stdout`: 是否输出到标准输出；后端服务默认应为 `false`。

## 落地检查清单

- 是否仍存在控制台打印日志。
- 是否统一走 `utils/log/` 封装。
- 是否有配置文件驱动日志参数。
- 是否区分了文件日志与标准输出开关。
- 是否先执行 `LoadConfig` 再执行日志初始化。
- 是否保证日志只初始化一次。
- 是否不存在 `Init(config.LogConfig{})` 这类空配置预初始化。
