# 说明
返回符合查询条件的所有缺陷关联的群聊ID


# url
`${TAPD_API_ENDPOINT}/bugs/get_bug_group_chat_id`

# 支持格式
JSON/XML（默认JSON格式）

# HTTP请求方式
GET

# 请求数限制
默认返回所有

# 请求参数
|字段名|必选|类型及范围|说明|特殊规则|
|:----:|:----:|:----:|:----:|:----:|
| workspace_id | 是 | integer | 项目ID |  |
| bug_ids | 是 | integer | 缺陷ID | 支持多ID查询 |


# 调用示例及返回结果
## 获取项目下缺陷
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password'  '${TAPD_API_ENDPOINT}/bugs/get_bug_group_chat_id?workspace_id=1000351&bug_ids=1001000351082244337'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN'  '${TAPD_API_ENDPOINT}/bugs/get_bug_group_chat_id?workspace_id=1000351&bug_ids=1001000351082244337'`

### 返回结果
```JSON
{
    "status": 1,
    "data": {
        "1001000351082244337": "TAPDBUG1001000351082244337"
    },
    "info": "success"
}
```

# 字段说明
## 重要字段说明
|字段|说明|
|:----:|:----:|
| key | 缺陷ID |
| value | 群聊ID |
