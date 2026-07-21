# 说明
更新缺陷关联群聊的标题


# url
`${TAPD_API_ENDPOINT}/bugs/update_bug_group_chat_title`

# 支持格式
JSON/XML（默认JSON格式）

#  HTTP请求方式
POST

# 请求数限制
- 群聊需要已存在
- 每次只允许更新一条数据

# 请求参数
|字段名|必选|  类型及范围  |     说明     |
|:----:|:----:|:-------:|:----------:|
| workspace_id | `是` | integer |    项目ID    |
| bug_id | `是` | integer |    缺陷ID    |
| chat_title | `是` | string  | 新群聊标题  |


# 调用示例及返回结果
## 更新缺陷  1010104801501437563 的标题为 修改群聊标题
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password' -d 'workspace_id=10104801&bug_id=1010104801501437563&chat_title=修改群聊标题' '${TAPD_API_ENDPOINT}/bugs/update_bug_group_chat_title'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN' -d 'workspace_id=10104801&bug_id=1010104801501437563&chat_title=修改群聊标题' '${TAPD_API_ENDPOINT}/bugs/update_bug_group_chat_title'`

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
