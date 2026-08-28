# 加密货币行情速查官 · 使用指南

**slug**：`z-data-crypto`　**类型**：常规 Skill　**版本**：V1.1.0

## 何时用
当用户要查 BTC/ETH 等加密货币行情时使用。

## 怎么用
1. 识别用户提到的币种并映射为大写符号（如 BTC / ETH / SOL / HYPE），不确定时先确认，不猜测。
2. 调用数据源脚本（duration 缺省 `24h`）：
   ```
   python "D:\谷歌云盘\luode-skills\crypto-price__skillhub\scripts\get_price_chart.py" BTC 24h
   ```
3. 解析返回 JSON（`price` / `change_period_percent` / `text_plain` / `chart_path`）。
4. 输出数值卡片 + 来源与时效 + `仅供参考` 声明；`chart_path` 存在时以图片输出（`MEDIA: <chart_path>` 行）。

## 示例
- 用户：「查一下 BTC 最新价格」
- 执行：`get_price_chart.py BTC 24h`
- 输出：BTC $79,133.00 · 24h +0.57% · 来源 hyperliquid · 仅供参考

## 边界
- 数据来自 Hyperliquid / CoinGecko 公开接口，仅供学习参考，不构成投资建议；实时性以数据源为准，不承诺准确与时效。
- 数据源不可用时明确报错，禁止编造价格。
