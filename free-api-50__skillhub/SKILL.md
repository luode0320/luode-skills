---
name: "free-api-50"
description: "查询国内免费公开 API（无密钥）：天气、股票、油价、快递、日历、成语、百科、汇率、翻译、星座、二维码等 50+ 实用查询命令。适用于免登录免费数据速查、生活/金融/娱乐信息查询场景。触发词：免费api、api大全、天气查询、股票查询、快递查询、油价、汇率查询、成语查询、二维码、去水印、星座运势、翻译、随机笑话、百科查询、IP查询。"
license: MIT
metadata:
  displayName: "中国免费 API 大全"
  version: "1.1.0"
  author: "Clawhub Developer"
---

# 中国免费 API 大全（CLI）

一个聚合国内免费公开 API 的命令行工具：**54 个查询命令、无需注册、无需 API Key**（1 个走 `wttr.in` + 53 个走木小果聚合 API），覆盖天气、金融、生活、娱乐、工具五大类。核心逻辑在 `china_free_api.py`（纯 `requests` 实现，无第三方框架依赖），`start.sh` 为透传入口。

## 数据源状态（先看这里）

| 数据源 | 覆盖命令 | 实测状态 | 说明 |
|---|---|---|---|
| `wttr.in` | `weather` | ✅ 本机实测可用 | 免费无 key，无需额外配置 |
| `api.muxiaoguo.cn` | 其余 53 个命令 | ⚠️ 需网络可达性验证 | 依赖公网可达；某些内网/代理环境不可达 |

**先用 `--check` 探测**：`python china_free_api.py --check` 会分别探测两个数据源并给出 OK/FAIL。木小果不可达时 `weather` 仍可用，其余命令返回 `❌ 查询失败`——这是预期降级，不是脚本 bug。

## 使用流程

1. **探测环境**：跑 `python china_free_api.py --check`，确认数据源可达性（首次使用必做）。
2. **查命令**：在下方「命令速查表」找到目标命令与参数格式。
3. **执行查询**：从本 skill 目录运行 `python china_free_api.py <command> [args...]`，或 `bash start.sh <command> [args...]`。
4. **验收**：核对输出是否含预期字段（见「验收清单」）；不可达降级时按第 1 步提示处理。

## 命令速查表

全部命令：`python china_free_api.py --list`。按类分组如下：

| 类 | 命令 | 参数 | 示例 |
|---|---|---|---|
| 天气 | `weather` | 城市名 | `weather 北京` |
| 天气 | `weather7` / `weather24` | 城市名 | `weather7 北京` |
| 金融 | `stock` | 股票代码/名称 | `stock 600519` |
| 金融 | `oil` | 无 | `oil` |
| 金融 | `exchange` | 金额(默认100) | `exchange 100` |
| 信息 | `phone` / `phoneluck` | 11位手机号 | `phone 13800138000` |
| 信息 | `ip` / `ipprecise` | IP 地址 | `ip 8.8.8.8` |
| 信息 | `express` | 快递单号 | `express SF123` |
| 信息 | `bank` | 银行卡号 | `bank 622202***` |
| 信息 | `plate` / `carprice` | 车牌号 | `plate 京A12345` |
| 生活 | `calendar` / `countdown` | 日期(后者) | `calendar` / `countdown 2026-05-01` |
| 生活 | `rubbish` | 垃圾名称 | `rubbish 电池` |
| 生活 | `history` | 无 | `history` |
| 娱乐 | `star` | 星座名 | `star 双子` |
| 娱乐 | `poem` / `idiom` / `idiomlink` | 关键词 | `poem 李白` |
| 娱乐 | `joke` / `love` / `word` / `emote` | 无 | `joke` |
| 娱乐 | `girl` / `anime` / `dog` / `cat` | 无 | `cat` |
| 工具 | `qrcode` / `qrcodedecode` | 文本/图片URL | `qrcode hello` |
| 工具 | `dy` | 抖音分享链接 | `dy https://v.douyin.com/xxx` |
| 工具 | `short` | 长链接 | `short https://example.com` |
| 工具 | `password` | 长度(默认12) | `password 16` |
| 工具 | `translate` / `traditional` / `pinyin` | 文本 | `translate hello` |
| 工具 | `ocr` | 图片URL | `ocr https://xxx.png` |
| 工具 | `avatar` / `wallpaper` / `wallpaper4k` / `acg` | 类型(可选) | `wallpaper` |
| 工具 | `name` | 性别(默认男) | `name 女` |
| 工具 | `nav` / `city` | 无 | `city` |
| 更多 | `news` / `newstype` | 分类(可选) | `news` |
| 更多 | `wiki` / `lyric` / `song` / `school` / `food` / `dream` | 关键词 | `wiki 腾讯` |

## 适用边界

**何时用**：需要免登录、无密钥的公开数据速查（天气、股票、油价、快递、翻译等）；原型验证或临时数据获取。

**何时不用**：
- 生产环境 / 需要 SLA 保障的业务调用——免费 API 无可用性承诺；
- 企业级或隐私敏感数据（银行卡、手机号等仅限个人临时查询）；
- 需要稳定字段契约的场景——第三方接口字段可能变更；
- 本机网络无法访问 `api.muxiaoguo.cn` 时，木小果系 53 个命令不可用（先跑 `--check`）。

## 验收清单

- [ ] 先跑 `--check`，确认当前网络下哪些数据源可用
- [ ] 命令名拼写正确（`--list` 可查全量）
- [ ] 参数格式正确：手机号 11 位、日期 `YYYY-MM-DD`、密码长度为整数
- [ ] 输出包含预期字段（如 `weather` 含温度/天气/湿度/风速）
- [ ] 返回 `❌ 查询失败` 时，先判断是数据源不可达（`--check`）还是参数错误（会提示 `参数错误` 且 exit 1）
- [ ] 脚本异常时 exit code 非 0（未知命令 / 参数错误），正常查询 exit 0

## 环境自检

```bash
python --version   # 需 Python 3.8+
pip install -r requirements.txt   # 仅需 requests
python china_free_api.py --check  # 数据源可达性探测
```

- 依赖仅 1 项：`requests`（`requirements.txt` 已声明）
- 无需任何 API Key；若 `--check` 显示 FAIL，换网络环境后重试

## 相关技能

- `apifox-cli`：自家 API 的调试与管理工具，与本 skill（第三方公开 API 查询）互补
- `api-contract-rules`：自家接口的契约规范，本 skill 不涉及接口设计
- `cryptocurrency-data-api`：加密货币行情专用查询，本 skill 未覆盖币圈

## 免责声明

本 skill 所有接口均来自第三方公开免费服务，可用性与数据准确性以服务方为准；本 skill 仅做调用封装，不对数据真实性负责。
