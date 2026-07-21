# 说明
解除需求缺陷关联关系


# url
`${TAPD_API_ENDPOINT}/stories/remove_story_bug_raletions`

# 支持格式
JSON/XML（默认JSON格式）

#  HTTP请求方式
POST

# 请求数限制
每次只允许解除一条数据

# 请求参数
|字段名|必选|类型及范围|说明|
|:----:|:----:|:----:|:----:|
| workspace_id | `是` | integer | 项目ID |
| story_id | `是` | integer | 需求id |
| bug_id | `是` | integer | 缺陷id |
| current_user | 否 | string | 操作人 |


# 调用示例及返回结果
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password' -d 'workspace_id=10104801&story_id=1010104801855713221&bug_id=1010104801500637481' '${TAPD_API_ENDPOINT}/stories/remove_story_bug_raletions'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN' -d 'workspace_id=10104801&story_id=1010104801855713221&bug_id=1010104801500637481' '${TAPD_API_ENDPOINT}/stories/remove_story_bug_raletions'`

### 返回结果
```JSON
{
    "status": 1,
    "data": {
        "success": true
    },
    "info": "success"
}
```
