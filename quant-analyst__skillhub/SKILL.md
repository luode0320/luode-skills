---
name: quant-analyst
description: "加密货币量化交易系统：回测、纸面交易、实盘交易、策略参数优化。策略编写（MA/RSI/MACD/Bollinger）、50+ 技术指标、风险管理（仓位/止损/止盈）、性能指标（Sharpe/最大回撤/胜率）。基于 openclaw-quant 外部仓库，使用前需先安装。适用于回测策略、优化参数、纸面交易、实盘交易场景。触发词：quant、量化、回测、backtest、交易策略、策略优化、sharpe、最大回撤、纸面交易、paper trading、实盘交易、量化交易、比特币策略、RSI 策略、均线交叉、网格交易、仓位管理、止损止盈。"
license: MIT
metadata:
  displayName: "量化交易分析（openclaw-quant）"
  version: "0.2.0"
  author: "ZhenStaff"
---

# 量化交易分析（openclaw-quant）

加密货币量化交易系统：回测、纸面交易、实盘、参数优化。**依赖外部仓库 `openclaw-quant`，使用前必须先安装**（本机未安装时回测/实盘功能不可用，见「前置检查与降级」）。

## 前置检查与降级（先读这里）

**每次使用前检查安装状态：**
```bash
ls ~/openclaw-quant            # 仓库是否存在
python -c "import openclaw_quant"   # 包是否可导入
```

**降级规则：**
- ✅ 已安装：按下方流程正常使用。
- ❌ 未安装：**不要假装能回测/实盘**。向用户说明需要先完成「安装」步骤；若用户仅需策略设计/指标/风控方案咨询，可进入「降级咨询模式」（用通用量化方法论回答，不执行代码）。
- 网络不可达 GitHub 时同样视为未安装，提示安装被阻断，不伪造结果。

## 安装

```bash
git clone https://github.com/ZhenRobotics/openclaw-quant.git ~/openclaw-quant
cd ~/openclaw-quant
pip install -r requirements.txt
export BINANCE_API_KEY="your-key"       # 仅实盘/纸面需要
export BINANCE_API_SECRET="your-secret"
python -m openclaw_quant --help          # 验证安装
```

## 使用流程

1. **前置检查**：确认仓库已克隆、包可导入（见上）。
2. **定任务**：回测 / 优化 / 纸面 / 实盘（四选一，实盘需用户显式确认）。
3. **写策略**：继承 `Strategy`，`init()` 用 `self.I()` 计算指标，`next()` 写事件逻辑（见示例）。
4. **回测先行**：`Backtest(strategy, data, cash=10000, commission=0.001).run()`。
5. **看指标**：Sharpe、最大回撤、胜率、Profit Factor（见「性能指标」）。
6. **验证**：结果与直觉交叉核对；实盘前先纸面 ≥1-2 周。

## 快速示例

### 均线交叉策略 + 回测
```python
from openclaw_quant import Strategy, Backtest

class MAStrategy(Strategy):
    fast_period = 10
    slow_period = 30
    def init(self):
        self.fast_ma = self.I(SMA, self.data.Close, self.fast_period)
        self.slow_ma = self.I(SMA, self.data.Close, self.slow_period)
    def next(self):
        if self.fast_ma[-1] > self.slow_ma[-1] and not self.position:
            self.buy()
        elif self.fast_ma[-1] <= self.slow_ma[-1] and self.position:
            self.sell()

bt = Backtest(MAStrategy, data, cash=10000, commission=0.001)
result = bt.run()
print(result)
```

### RSI 均值回归
```python
class RSIStrategy(Strategy):
    rsi_period, oversold, overbought = 14, 30, 70
    def init(self):
        self.rsi = self.I(RSI, self.data.Close, self.rsi_period)
    def next(self):
        if self.rsi[-1] < self.oversold and not self.position:
            self.buy()
        elif self.rsi[-1] > self.overbought and self.position:
            self.sell()
```

### 参数优化
```python
result = bt.optimize(
    fast_period=range(5, 20, 2),
    slow_period=range(20, 60, 5),
    maximize='sharpe_ratio'   # 或 'total_return' / 'profit_factor'
)
print(f"Best: {result.best_params}, Sharpe: {result.sharpe_ratio:.2f}")
```

### 纸面/实盘
```python
from openclaw_quant import LiveTrading
live = LiveTrading(strategy=MAStrategy, exchange='binance',
                   symbol='BTC/USDT', paper=True)        # paper=False 为实盘
live.run()
```

### 风险管理（策略内）
```python
def init(self):
    self.risk_per_trade = 0.02    # 单笔风险 2% 资金
    self.stop_loss = 0.05
    self.take_profit = 0.10
def next(self):
    if self.ma[-1] > self.data.Close[-1] and not self.position:
        size = self.calculate_position_size(risk=self.risk_per_trade,
                                            stop_loss=self.stop_loss)
        self.buy(size=size)
        self.set_stop_loss(self.stop_loss)
        self.set_take_profit(self.take_profit)
```

## CLI 命令

```bash
openclaw-quant backtest --strategy ma_cross --symbol BTCUSDT --days 365
openclaw-quant optimize --strategy rsi --symbol ETHUSDT --metric sharpe_ratio
openclaw-quant paper --strategy ma_cross --symbol BTCUSDT
openclaw-quant live --strategy ma_cross --symbol BTCUSDT --confirm   # 实盘需确认
openclaw-quant results --backtest-id abc123
```

## 性能指标

| 指标 | 含义 |
|---|---|
| Total Return | 总收益率 |
| Annualized Return | 年化收益率 |
| Sharpe / Sortino | 风险调整收益（越高越好） |
| Max Drawdown | 最大回撤（峰到谷） |
| Win Rate | 胜率 |
| Profit Factor | 毛利/毛损 |
| Calmar Ratio | 收益/最大回撤 |
| Expectancy | 每笔期望收益 |

## 内置策略与指标

**策略**：MA Cross、RSI 均值回归、MACD 动量、Bollinger 反弹、突破、网格、DCA、统计套利。

**指标（50+，`self.I()` 调用）**：
- 趋势：SMA/EMA/WMA/MACD/ADX/Supertrend
- 动量：RSI/Stochastic/CCI/Williams %R/ROC
- 波动：Bollinger/ATR/Keltner/StdDev
- 量：OBV/Volume SMA/MFI/VWAP/CMF

## 数据源与配置

- 数据：交易所 API（ccxt：Binance/OKX/Bybit）、CSV、PostgreSQL/SQLite 缓存、WebSocket 实时
- 配置 `config.yaml`：回测参数（initial_capital/commission/slippage）、风控（max_position_size/max_drawdown/daily_loss_limit）

## 排障

| 问题 | 处理 |
|---|---|
| `ccxt.NetworkError` | 查网络/密钥；测试用 testnet |
| 数据不足 | 增大 `warmup=100` 或 `fetch_candles(limit=5000)` |
| 优化太慢 | 步长调大 / `max_tries=50` 限制迭代 |

## 适用边界

**何时用**：用户要回测/优化/纸面/实盘加密货币策略，且 openclaw-quant 已安装。

**何时不用**：
- 未安装外部仓库（本机 `import openclaw_quant` 失败）→ 先安装，或进入降级咨询模式；
- 仅查行情/价格 → 转 `crypto-price__skillhub`；
- 加密量化分析与信号 → 转 `crypto-quant-analysis__skillhub`；
- 已有交易引擎的实盘执行（trading_engine）→ 转 `trading-engine-crypto-futures-trading__skillhub`；
- 金融/投资/股票综合场景 → 转 `wb-finance-skill`。

**红线（DON'T）**：
- 未确认安装不执行回测/实盘；
- 不推荐具体交易策略、不保证收益、不做金融建议；
- 实盘交易必须用户显式确认（`--confirm`），并提示风险。

## 验收清单

- [ ] 已确认 `~/openclaw-quant` 存在且 `import openclaw_quant` 成功（未安装已降级说明）
- [ ] 实盘/纸面前已先跑回测并核对指标
- [ ] 佣金/滑点使用真实值（commission=0.001 级别）
- [ ] 参数优化防止过拟合（walk-forward 或样本外验证）
- [ ] 实盘已设风控参数（单笔风险/止损/日亏限额）且用户显式确认
- [ ] 未推荐具体策略、未承诺收益
