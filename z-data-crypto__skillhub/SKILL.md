---
name: z-data-crypto
description: 当用户要查 BTC/ETH 等加密货币行情时使用。触发词：加密货币 / 币价查询 / crypto / 查币 / 比特币价格。调用 crypto-price 数据源脚本（Hyperliquid 优先 + CoinGecko 兜底，免密钥）返回最新价格、区间涨跌与 K 线图。
license: MIT
metadata:
  id: z-data-crypto
  version: 1.1.0
  platforms: 全平台
  category: data-analysis
  slug: z-data-crypto
  displayName: 加密货币行情速查官
  summary: 加密货币行情速查官：输入币种即返回最新价格、区间涨跌与来源时效。
  icon: _icon.png
---
# 加密货币行情速查官

> 类型：常规 Skill（行情速查官）｜slug：`z-data-crypto`｜版本 V1.1.0

## 一、定位 / 适用边界
- **定位**：加密货币行情速查官：输入币种即返回最新价格、区间涨跌与来源时效。
- **适用**：当用户要查 BTC/ETH 等加密货币行情时使用。
- **不适用**：不做量化分析、不做 DEX 池子/深度 OHLCV（见交叉引用）；不替代专业服务/官方系统。
- **标签**：加密货币, 行情, 数据, 区块链

## 二、触发词
加密货币 / 币价查询 / crypto / 查币 / 比特币价格 / ETH 价格

## 三、数据源与调用
- **主数据源**：仓库 `crypto-price__skillhub/scripts/get_price_chart.py`，本 skill 只引用不复制（唯一事实源防漂移）。
- **命令（Windows 本机）**：
  ```
  python "D:\谷歌云盘\luode-skills\crypto-price__skillhub\scripts\get_price_chart.py" <SYMBOL> [duration]
  ```
- **命令（WSL）**：
  ```
  python3 /mnt/d/谷歌云盘/luode-skills/crypto-price__skillhub/scripts/get_price_chart.py <SYMBOL> [duration]
  ```
- **duration 格式**：`30m` / `3h` / `12h` / `24h`（默认）/ `2d`
- **数据源策略**：Hyperliquid API 优先（HYPE 等原生币），CoinGecko API 兜底；300 秒缓存、内置 3 次重试。
- **实测基线**：BTC / ETH 查询已实测通过（2026-08-25，exit 0，真实返回）。

## 四、工作流程（5 步，按序执行）
1. **识别标的**：从用户描述提取币种（代码/名称），如 BTC / ETH / SOL / HYPE。
2. **符号映射**：名称 → 大写符号（比特币→BTC、以太坊→ETH）；不确定时先向用户确认，禁止猜测。
3. **拉取行情**：调用 `get_price_chart.py <SYMBOL> [duration]`，未指定 duration 时用 `24h`。
4. **解析 JSON**：读取 `price` / `change_period_percent` / `text_plain` / `chart_path` 字段。
5. **输出卡片**：最新价 + 区间涨跌 + 来源与时效 + `仅供参考` 声明；`chart_path` 存在时以图片输出（`MEDIA: <chart_path>` 行），不用文本占位符。

## 五、输出规范
- 输出 = 关键数值卡片（最新价 / 区间涨跌 / 来源与时效）+ 简短对比 + `仅供参考` 声明。
- JSON 字段：`price`（USD/USDT 计价）、`change_period_percent`（区间涨跌 %）、`text_plain`（格式化文本）、`chart_path`（K 线图 PNG 路径，可能为空）。
- 图表输出：`chart_path` 非空时输出 `MEDIA: <chart_path>`，禁止写 `[chart: path]` 占位符。

## 六、红蓝对抗（高频疑问）
- Q：数据滞后？→ 以数据源刷新为准（缓存 300 秒，可等过期后重查）。
- Q：查不到？→ 先做符号映射再重试；仍失败按失败回退表处理。
- Q：能投资建议吗？→ 仅给数据，不给买卖建议。

## 七、失败回退表
| 症状 | 根因 | 回退 |
| --- | --- | --- |
| symbol 无效 | 符号映射错误 | 查词库.md 别名表，修正符号后重试 |
| API 超时/网络失败 | 上游不可达 | 等待后重试（脚本内置 3 次重试）；仍失败明确告知数据源不可用，禁止编造价格 |
| 输出乱码 | 编码问题 | 按 `windows-encoding-rules` / `charset-fix` 处理 |
| 用户要 DEX 池子/深度 OHLCV | 超出本 skill 范围 | 指回 `cryptocurrency-data-api__skillhub` |

## 八、交叉引用（不复制正文）
- **DEX 池子 / 深度 OHLCV / 多网络数据**：`cryptocurrency-data-api__skillhub`（DexPaprika MCP，需密钥配置，不做主源）。
- **从"速查"升级为量化分析**：`crypto-quant-analysis__skillhub`。
- **更广的金融分析兜底**：`wb-finance-skill` / `quant-analyst`。

## 九、使用建议 / 错题本
- 建议用户结合多源交叉验证；重大决策咨询持牌顾问。
- 本 skill 只做行情速查：不做买卖建议、不做链上分析。

## 十、红线 / 安全审查
- 数据来自公开接口（Hyperliquid / CoinGecko），仅供学习参考，不构成投资建议；实时性以数据源为准，不承诺准确与时效。
- 不含密钥/token；不生成违规或侵权内容；发布须符合平台规范。
- 数据源不可用时明确报错，禁止编造价格。

## 十一、版本与来源
- V1.1.0 · 由本工作空间基于 SkillHub 已发布 492 个覆盖的缺口分析催生（方向 行情速查官）；V1.1.0 起接入 `crypto-price__skillhub` 真实数据源（Hyperliquid + CoinGecko，免密钥，已实测）。
