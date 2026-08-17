# 企业微信通知（BOT_URL）

> 归属：`tapd-openapi`。吸收自外部 TAPD skill（`clawhub.ai/kevindai/tapd`）的企业微信机器人通知能力缺口。

## 配置

- 环境变量 `BOT_URL`：企业微信群机器人 webhook 地址（可选，仅发送群消息时需要）。
- 使用前必须确认 `BOT_URL` 指向**可信端点**（企业微信官方 webhook 地址），避免指向不可信第三方。
- 该接口**不是 TAPD API**，直接 POST 到 webhook。

## 发送群消息

**请求方法：** POST

**请求地址：** `${BOT_URL}`

**请求头：** `Content-Type: application/json`

**请求体：**

| 字段 | 说明 |
|------|------|
| msgtype | `markdown` 或 `markdown_v2`；含 @ 时用 `markdown`，否则可用 `markdown_v2` |
| content | 消息内容（markdown 格式） |

**请求示例：**

```bash
curl -s -X POST -H "Content-Type: application/json" "$BOT_URL" \
  -d '{"msgtype":"markdown","content":"**需求更新** <@user1> 需求 #123 已流转到开发中"}'
```

## 通用调用（使用 tapd_client_stdlib.py）

```bash
python3 {baseDir}/scripts/tapd_client_stdlib.py post --endpoint "" -b '{"msgtype":"markdown","content":"..."}'  # 需设置 BOT_URL
```

## 用途

- TAPD 更新、迭代提醒、工作流通知推送到企业微信群。
- 优先级变更、截止日期临近、新任务分派等自动化通知。

## 安全

- 最小权限、短期令牌原则同样适用于 webhook：仅给机器人配置发送权限。
- 可选加固：在沙盒环境运行脚本并限制网络仅允许访问 TAPD API 与 BOT_URL。
