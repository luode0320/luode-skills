---
name: go-http-timeout-hardening
description: 当排查「请求挂死 N 分钟才失败」「上游无响应」「网关/代理层超时」类问题，或需要为 Go HTTP 客户端补超时兜底时触发。核心前提：Go 的 http.Transport.ResponseHeaderTimeout 默认 0 = 无限等待，http.DefaultTransport 根本不设该字段，http.Client.Timeout 默认 0 = 端到端不限制。因此「没有超时配置」是默认状态，不是异常状态。本 Skill 提供分层诊断法、统一注入点定位法、以及三个必踩陷阱（nil transport 回落全局需克隆、配置项需指针类型区分未配置与显式禁用、自定义 RoundTripper 无法承载该字段）。
agent_created: true
---

# Go HTTP 客户端超时加固

## 核心前提（先记住这条，能省掉大半排查时间）

**「没有超时」才是 Go 的默认状态。**

| 字段 | 默认值 | 含义 |
|---|---|---|
| `http.Transport.ResponseHeaderTimeout` | **0** | 等待上游响应头**无限期** |
| `http.Client.Timeout` | **0** | 端到端**不限制** |
| `http.DefaultTransport` | 不含 `ResponseHeaderTimeout` | 克隆它 ≠ 获得超时保护 |
| `net.Dialer.Timeout`（stdlib 默认） | 30s | 只管**建连**，不管建连后静默 |

所以现象常表现为：上游**接受了 TCP 连接但一个字节都不回**，此时既不是 dial 超时、也不是 TLS 超时、也不是响应体读取超时——只能等操作系统 TCP 重传耗尽（Linux 默认约 924 秒 ≈ 15 分钟），叠加重试后可达数十分钟。

**关键判据**：日志显示"首字延迟不适用/无首字节"+ 耗时是 15/30 分钟的整齐量级 → 高度指向响应头等待无上限。

## 一、分层诊断法

链路上**每一层都必须独立设防**，任一层的超时都不能替代另一层：

```
客户端 → 网关/聚合层 → 中间代理层 → 上游服务
          ①            ②            ③
```

排查顺序：**从最内层（③）往外查**，因为最内层最先能止损。

常见失误是「只修了一层」——网关设了超时，但网关到代理层那段仍无保护，代理层到上游那段也无保护，故障依旧能复现。

## 二、定位统一注入点

不要在几十个调用点逐个加超时。找**统一构建入口**：

```bash
# 1. 找客户端构建函数（名字通常含 HTTPClient / newClient / buildTransport）
grep -rn "func .*HTTPClient\|func newClient\|func buildTransport" --include="*.go" . | grep -v _test

# 2. 统计该函数的调用点数量，确认它确实是统一入口
grep -rn "NewXxxHTTPClient" --include="*.go" . | grep -v _test | wc -l

# 3. 确认全库此前是否设过该字段（空 = 从未设防）
grep -rn "ResponseHeaderTimeout" --include="*.go" .
```

若调用点数量在几十个量级，且构建函数是唯一入口 → 在**函数出口**统一施加，一次覆盖全部调用点。

## 三、三个必踩陷阱

### 陷阱 1：nil Transport 会回落到进程级全局对象

`client.Transport == nil` 时，`net/http` 回落到**进程共享的** `http.DefaultTransport`。

**直接改它的字段 = 静默重调整个进程所有 HTTP 调用**。必须克隆：

```go
case nil:
    base, ok := http.DefaultTransport.(*http.Transport)
    if !ok {
        return // 自定义了全局默认传输，不强行处理
    }
    cloned := base.Clone()
    cloned.ResponseHeaderTimeout = headerTimeout
    client.Transport = cloned  // 注意：Proxy 等原有语义由 Clone 保留
```

注意：不要用 `Proxy = nil` 的"直连传输"替代克隆，那会**顺带关闭环境代理**，属于行为变更。

### 陷阱 2：配置项要用指针类型区分「未配置」与「显式禁用」

若用 `int`，`0` 会同时表示"用户没填"和"用户要禁用"，无法给出默认值。用 `*int`：

```go
Field *int `yaml:"xxx-timeout,omitempty"`

func (c *Config) EffectiveSeconds() int {
    if c == nil || c.Field == nil {
        return DefaultTimeout   // 未配置 → 用默认值
    }
    return *c.Field             // 显式 0/负 → 调用方据此禁用
}
```

**并务必给代码级默认值**，让修复无需改动部署配置即生效——否则修复要等运维改配置，链路会断。

### 陷阱 3：自定义 RoundTripper 承载不了该字段

`ResponseHeaderTimeout` 是 `*http.Transport` 的字段，`http.RoundTripper` 接口上**没有等价物**。

uTLS/指纹伪装类传输、自定义包装传输（`fallbackRoundTripper` 等）都无法设置。正确处理：**类型断言失败时记 debug 日志并保持原行为**，不要假装设上了。

若要覆盖这类路径，需另用 `context.WithTimeout` 在请求级处理。

## 四、施加位置与结构

若构建函数原本用「提前 return」处理各分支，需先**重构为单一出口**，否则后处理会漏掉部分分支：

```go
// 改造前：分支内直接 return，后处理无处安放
if transport != nil {
    client.Transport = transport
    return client          // ← 提前返回，后续逻辑执行不到
}

// 改造后：分支只赋值，统一出口做后处理
if transport != nil {
    client.Transport = transport
} else if rt, ok := ctx.Value(key).(http.RoundTripper); ok {
    client.Transport = rt
}

applyTimeout(client, cfg)   // 统一后处理
return client
```

重构时**逐分支核对语义等价**（原提前 return 会跳过哪些分支，新结构是否同样跳过）。

## 五、测试守护点（每一条都要有）

| 用例 | 断言 |
|---|---|
| 默认值生效 | 未配置时 transport 上是约定的默认秒数 |
| 显式自定义值 | 配置值被正确应用 |
| 显式禁用 | transport **保持未设置**（不是"设为 0"），即行为完全等价于修复前 |
| 代理路径也生效 | 走代理构建的 transport 同样带上该上限 |
| **全局未被污染** | `http.DefaultTransport` 的字段值前后不变，且 `client.Transport != http.DefaultTransport` |

最后一条最关键——它守护的是最致命的回归：修复引入了全局污染。

## 六、收敛清单

- [ ] 确认全库此前从未设过 `ResponseHeaderTimeout`
- [ ] 定位统一构建入口并统计调用点数量
- [ ] 重构为单一出口，逐分支核对语义等价
- [ ] nil transport 走 Clone，**不**改全局
- [ ] 配置项用 `*int`，且有代码级默认值
- [ ] 自定义 RoundTripper 记日志保持原行为
- [ ] 5 类测试全部落地并跑通
- [ ] `gofmt` / `go vet` / 目标包测试全绿
- [ ] 明确记录：该上限只约束**响应头等待**，不影响响应头到达后的流式传输

## 七、遗留项别忘

1. **重试会放大**：若上游错误码落在可重试范围，实际最坏耗时 = `单次上限 × (1 + 重试次数)`。重试次数常存于**数据库配置表**而非代码，必须单独确认。
2. **慢速吐字节（trickle）不受本上限约束**：上游持续低速发字节时 `ResponseHeaderTimeout` 永远不触发（它在收到响应头后就失效了），需整体超时或空闲超时另行防护。
3. **部署生效需验证**：改配置/代码后，用 `docker inspect` 或等效手段确认目标实例实际拿到了新值。
