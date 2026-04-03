---
name: golang-patterns
description: Go 语言惯用模式、最佳实践与编码约定，用于构建健壮、高效、可维护的 Go 应用。
origin: ECC
---

# Go 开发模式

本 Skill 提供 Go 语言常用工程模式与最佳实践，目标是：代码可读、行为可预测、易维护。

## 何时启用

- 编写新的 Go 代码
- 评审 Go 代码
- 重构已有 Go 代码
- 设计 Go 包与模块边界

## 核心原则

### 1. 简单与清晰优先

Go 倾向简单直接，避免“聪明但难懂”的写法。

### 2. 零值可用

类型设计应让零值就能安全使用，尽量减少额外初始化负担。

### 3. 接口输入、结构体输出

函数参数优先接收接口，返回值优先返回具体类型，减少不必要抽象。

### 4. 错误是值（error as value）

错误必须显式处理，不要忽略或滥用 panic。

### 5. 清晰的数据流和依赖注入

避免包级可变全局状态，尽量通过构造函数注入依赖。

## 错误处理模式

### 包装错误并补上下文

```go
func LoadConfig(path string) (*Config, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return nil, fmt.Errorf("load config %s: %w", path, err)
	}

	var cfg Config
	if err := json.Unmarshal(data, &cfg); err != nil {
		return nil, fmt.Errorf("parse config %s: %w", path, err)
	}
	return &cfg, nil
}
```

### 使用 `errors.Is` / `errors.As`

- `errors.Is`：判断哨兵错误（如 `sql.ErrNoRows`）
- `errors.As`：判断具体错误类型（自定义错误）

### 不要忽略错误

- 禁止无理由 `result, _ := ...`
- 若确实可忽略，写出明确注释说明原因

## 并发模式

### Worker Pool

适用于可并行任务批量处理，配合 `sync.WaitGroup` 管理生命周期。

### Context 驱动取消与超时

- I/O / 网络调用应使用 `context.Context`
- 使用 `context.WithTimeout` 设置上限

### 优雅停机

- 捕获 `SIGINT` / `SIGTERM`
- 使用 `server.Shutdown(ctx)` 平滑下线

### `errgroup` 协调并发

- 并行任务中任一失败可统一中断
- 适合聚合多个外部请求

### 防止 goroutine 泄漏

- channel 写入用 `select` + `ctx.Done()` 兜底
- 必要时使用带缓冲 channel

## 接口设计

### 接口小而专注

- 倾向单一职责小接口（如 `io.Reader`）
- 通过组合扩展能力

### 接口定义在使用方

- 在消费侧定义“我需要什么能力”
- 实现侧只负责实现，不强绑定上层接口

## 包结构与命名

### 命名约定

- 避免冗余后缀（如 `userService`）

### 避免包级可变状态

- 不要在 `init()` 中创建全局数据库连接并共享
- 通过构造器注入依赖更清晰可测

## 结构体与 API 设计

### Functional Options

适用于可选参数较多的构造函数。

### 组合优于继承

使用 embedding 复用能力，但要避免语义混乱。

## 性能与内存

### 预分配 slice

已知大小时用 `make([]T, 0, n)`，减少扩容次数。

### 热点场景复用对象

高频分配可考虑 `sync.Pool`，但不要过度使用。

### 字符串拼接

循环拼接优先 `strings.Builder` 或 `strings.Join`。

## 工具链与质量门禁

### 常用命令

```bash
go build ./...
go test ./...
go test -race ./...
go vet ./...
golangci-lint run
go mod tidy
gofmt -w .
goimports -w .
```

### 推荐实践

- 本地与 CI 都执行格式化和 lint
- 优先修复 `errcheck`、`staticcheck`、`govet` 关键问题

## 快速记忆

- 接口入参，结构体返回
- 错误必须处理
- 上下文贯穿 I/O 调用
- 尽早返回，减少嵌套
- 代码要“无聊但可靠”

## 常见反模式

- 长函数中使用裸返回（`return`）
- 用 panic 做业务分支控制
- 把 `context.Context` 放进 struct 字段
- 同一类型混用值接收者和指针接收者但无明确规则

## 最终要求

当存在多个可行写法时，优先选择：

1. 更可读
2. 更显式
3. 更容易测试
4. 更容易定位问题

记住：Go 的优秀代码通常不是“技巧最多”，而是“最容易让团队看懂并稳定迭代”。
