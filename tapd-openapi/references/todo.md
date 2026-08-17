# Todo（用户待办）

> 归属：`tapd-openapi`。吸收自外部 TAPD skill（`clawhub.ai/kevindai/tapd`）的用户待办能力缺口。

## 查询用户待办

**请求方法：** GET

**请求地址：** `${TAPD_API_ENDPOINT}/users/todo/{user_nick}/{entity_type}`

**请求参数（路径）：**

| 参数 | 必填 | 说明 |
|------|------|------|
| user_nick | 是 | 用户英文昵称（未指定时可用 `CURRENT_USER_NICK` 环境变量） |
| entity_type | 是 | 实体类型：story / bug / task |

**请求示例：**

```bash
curl -s -H "Authorization: Bearer $TAPD_TOKEN" \
  "${TAPD_API_ENDPOINT}/users/todo/user1/story"
```

## 通用调用（使用 tapd_client_stdlib.py）

```bash
python3 {baseDir}/scripts/tapd_client_stdlib.py get --endpoint "users/todo/user1/story"
```

## 用途

- 获取某用户当前待办的需求/缺陷/任务，用于个人工作台、日报汇总。
- 未传 `CURRENT_USER_NICK` 时，可先用 `GET /users/info` 解析当前用户 nick，再查待办。
