# 说明
返回符合查询条件的所有需求关联的群聊ID


# url
`${TAPD_API_ENDPOINT}/stories/get_story_group_chat_id`

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
| story_ids | 是 | integer | 需求ID | 支持多ID查询 |


# 调用示例及返回结果
## 获取项目下需求
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password'  '${TAPD_API_ENDPOINT}/stories/get_story_group_chat_id?workspace_id=10109931&story_ids=1010109931854811265,1010109931854816753,11110'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN'  '${TAPD_API_ENDPOINT}/stories/get_story_group_chat_id?workspace_id=10109931&story_ids=1010109931854811265,1010109931854816753,11110'`

### 返回结果
```JSON
{
    "status": 1,
    "data": {
        "1010109931854811265": "TAPDSTORY1010109931854811265",
        "1010109931854816753": "TAPDSTORY1010109931854816753"
    },
    "info": "success"
}
```

# 字段说明
## 重要字段说明
|字段|说明|
|:----:|:----:|
| key | 需求ID |
| value | 群聊ID |
