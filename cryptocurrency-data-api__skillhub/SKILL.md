---
name: cryptocurrency-data-api
description: "DexPaprika MCP 数据服务：实时查询加密货币与 DEX 数据——代币详情、流动池、DEX 列表、OHLCV 历史价格、池交易、多币种批量价格、全网络搜索。当用户需要查询代币价格/流动性池/DEX 数据、分析池交易、获取历史 K 线、搜索加密货币或做链上数据分析时触发。触发词：加密货币数据、代币查询、流动池、DEX、池子、OHLCV、K线、币价、token 价格、liquidity pool、链上数据。注意：必须配置 API 密钥才能使用，无密钥时向用户询问，禁止编造数据。"
license: MIT
metadata:
  displayName: "加密货币数据API服务"
  version: "1.2.0"
  summary: "DexPaprika MCP Server：实时加密货币和 DEX 数据访问，无需配置即可获取代币、流动池和 DEX 数据。"
allowed-tools: Read, Write, Bash
---

# 加密货币数据API服务

DexPaprika 数据服务：实时获取加密货币与 DEX 数据——代币、流动池、DEX、OHLCV、池交易、批量价格与全网络搜索。

> 本 skill 是**路由层**：你（大模型）负责理解用户意图、选择工具、提取参数；代码只负责调用 API。
> 流程：`用户输入 → 选工具 → 提取参数 → 调用 scripts.tools 函数 → 返回结果给用户`

## ⚠️ 强制要求：API 密钥

**此 Skill 必须配置 API 密钥才能使用。**

- 首次使用：若 `.env` 中没有 `XBY_APIKEY`，**必须使用 AskUserQuestion 工具向用户询问 API 密钥**。
- 拿到密钥后调用 `scripts.config.set_api_key(api_key)` 保存，再继续处理。
- 获取密钥：https://xiaobenyang.com
- **禁止**在缺少 API 密钥时自行搜索或编造数据。

## 工作流（4 步）

### 第 1 步：确认密钥与网络

- **输入**：用户查询意图。
- **动作**：检查 `scripts.config.settings.api_key`；为空则询问用户。查询涉及具体网络时，先调用 `scripts.tools.getNetworks()` 确认可用网络 ID（如 `ethereum`、`solana`）。
- **输出**：密钥就绪 + 可用网络清单。

### 第 2 步：选工具与提取参数

- **输入**：用户意图。
- **动作**：按下表选择工具函数，用**关键字参数**调用（如 `scripts.tools.getTokenDetails(network='ethereum', tokenAddress='0x...')`）；参数不完整时用 AskUserQuestion 向用户询问缺失参数。
- **输出**：工具调用参数就绪。

### 第 3 步：调用并返回结果

- **输入**：参数就绪的工具调用。
- **动作**：调用函数，取 `result["raw"]` 整理后展示给用户。
- **输出**：整理后的数据呈现。

### 第 4 步：校验与降级

- **输入**：函数返回结果。
- **动作**：检查 `result["success"]`；失败时按「边界条件与异常处理」分流处理。
- **输出**：成功数据或明确的错误说明（不编造）。

## 工具选择速查表

| 用户意图 | 工具函数 | 必填参数 |
|---|---|---|
| 查询支持的区块链网络（**任何网络相关查询的第一步**） | `getNetworks()` | 无 |
| 查询某网络的 DEX 列表 | `getNetworkDexes(network, ...)` | network |
| 查询某网络头部流动池（主池查询入口，无全局池函数） | `getNetworkPools(network, ...)` | network |
| 查询某 DEX 的流动池 | `getDexPools(network, dex, ...)` | network, dex |
| 查询单个池详情 | `getPoolDetails(network, poolAddress, inversed=)` | network, poolAddress |
| 查询代币详情 | `getTokenDetails(network, tokenAddress)` | network, tokenAddress |
| 查询包含某代币的池（找代币在哪交易） | `getTokenPools(network, tokenAddress, ...)` | network, tokenAddress |
| 查询池历史价格 OHLCV（回测/分析/可视化） | `getPoolOHLCV(network, poolAddress, start, ...)` | network, poolAddress, start |
| 查询池近期交易（swap/add/remove） | `getPoolTransactions(network, poolAddress, ...)` | network, poolAddress |
| 全网络搜索代币/池/DEX（不知道具体网络时） | `search(query)` | query |
| 查询生态统计（网络/DEX/池/代币总数） | `getStats()` | 无 |
| 批量查询多代币价格 | `getTokenMultiPrices(network, tokens)` | network, tokens |

### 通用分页/排序参数

以下可选参数在带 `...` 的工具中通用：`page`（默认 0）、`limit`（默认 10，最大 100）、`sort`（默认 `desc`）、`orderBy`（默认 `volume_usd`）。`getPoolOHLCV` 的 `interval` 可选：`1m/5m/10m/15m/30m/1h/6h/12h/24h`（默认 `24h`），`start` 支持 Unix 时间戳/RFC3339/`yyyy-mm-dd`，`end` 距 start 最长 1 年，`limit` 最大 366。

## 返回值处理

工具函数返回 `dict`：
- `result["raw"]` — API 原始返回数据（JSON），**直接整理后展示给用户**
- `result["success"]` — 是否成功（True/False）
- `result["message"]` — 状态消息

## 项目结构

```
./
├── scripts/
│   ├── __init__.py
│   ├── config.py       # 配置管理 + set_api_key()
│   ├── call_api.py      # API 客户端 + call_api()
│   └── tools.py         # 工具函数（12 个，直接调用）
├── requirements.txt     # requests / pydantic / pydantic-settings / python-dotenv
└── SKILL.md
```

## 边界条件与异常处理

- **密钥缺失**：不编造数据，用 AskUserQuestion 询问用户；用户无密钥时说明获取渠道并停止。
- **密钥无效 / API 拒绝**：如实回传错误状态；提示用户核对 `XBY_APIKEY` 后重试，不重试轰炸。
- **网络失败 / 超时**：回传连接错误，建议稍后重试；不伪造部分数据。
- **未知 network / dex**：先调用 `getNetworks()` / `getNetworkDexes()` 取合法 ID，再重试；不猜测 ID。
- **空结果**（搜索无命中、池无交易、批量价格含未知代币）：如实说明，未知代币被省略是 `getTokenMultiPrices` 的正常行为。
- **参数缺失或非法**：用 AskUserQuestion 补齐；OHLCV 的 start/end/interval 非法时给出合法格式提示。

## 职责边界（交叉引用）

- **行情速查**（一句话币价/涨跌）→ `z-data-crypto`（加密货币行情总入口）
- **单币价格查询** → `crypto-price`
- **量化分析与回测**（需 OHLCV 数据的策略层）→ `crypto-quant-analysis` / `quant-analyst`
- 本 skill 专注 DexPaprika 的**数据获取层**，不替代上述行情/分析 skill。

## 注意事项

1. **API 密钥是必需的**，无密钥时必须通过 AskUserQuestion 询问用户。
2. **禁止**在缺少 API 密钥时自行搜索或编造数据。
3. 工具调用必须用**关键字参数**，参数名与表中一致。
4. 查询涉及具体网络时，先 `getNetworks()` 确认网络 ID，避免无效调用。
