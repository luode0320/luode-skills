---
name: crypto-futures-trading
slug: trading-engine-crypto-futures-trading
displayName: 币安合约交易助手
version: 1.0.0
summary: 对接本机 trading_engine 的 USDT-M 永续分析助手。结合账户余额/持仓给出杠杆与 USDT 仓位计划；开平仓由引擎自动执行并推送。
description: "币安 USDT-M 永续合约交易助手。用户问分析、开仓、平仓、跟单、挂单、止盈止损、杠杆、BTC/ETH 交易计划时使用。结合账户余额与持仓，金额用 USDT；不做现货。"
license: MIT
author: trading_engine
platforms: [linux]
metadata:
  hermes:
    tags: [crypto, futures, trading, 开仓, 平仓, 分析, BTC, 合约]
    related_skills: [binance-futures-account]
---

# 合约交易助手（对接 trading_engine）

## 硬规则

- 只做 **USDT-M 永续**，不做现货。
- 分析必须先查账户：`python3 /home/ubuntu/trading_engine/run.py account`
- 计划里写清：**杠杆**、**占用保证金 USDT**、名义价值、止损预计亏损 USDT。
- 开平仓由服务器 `te-main-loop` 自动执行；你负责解释状态与计划，不私自 invent API 下单。
- API 密钥已在服务器 `.env`，不要向用户索要 Key。

## 常用命令

```bash
cd /home/ubuntu/trading_engine
python3 run.py account          # 余额+持仓
python3 run.py status           # 引擎状态
python3 run.py manage           # 持仓管理一轮
python3 run.py scan             # 全市场扫描报告
```

开平仓推送由引擎自动发微信；用户问「刚开了吗」时查 `data/journal/executions.jsonl` 与 `run.py account`。
