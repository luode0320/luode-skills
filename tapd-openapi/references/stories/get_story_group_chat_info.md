# 说明
返回需求关联的拉群信息


# url
`${TAPD_API_ENDPOINT}/stories/get_story_group_chat_info`

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
| story_id | 是 | integer | 需求ID |  |


# 调用示例及返回结果
## 获取项目下需求
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password'  '${TAPD_API_ENDPOINT}/stories/get_story_group_chat_info?workspace_id=10104801&story_id=1010104801006295309'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN'  '${TAPD_API_ENDPOINT}/stories/get_story_group_chat_info?workspace_id=10104801&story_id=1010104801006295309'`

### 返回结果
```JSON
{
    "status": 1,
    "data": {
        "chatid": "wrteppDQAA1l2MrNUUDLWLyuLJdJBghw",
        "name": "1010104801006295309需求",
        "owner": "anyechen",
        "userlist": [
            "davidning",
            "anyechen"
        ]
    },
    "info": "success"
}
```

# 字段说明
## 返回字段说明
|字段|说明|
|:----:|:----:|
| chatid | 群聊ID |
| name | 群聊标题 |
| owner | 群主 |
| userlist | 群成员 |
