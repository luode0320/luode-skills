# 说明
获取需求关联的项目集


# url
`${TAPD_API_ENDPOINT}/stories/get_program_list_by_story_id`

# 支持格式
JSON/XML（默认JSON格式）

# HTTP请求方式
GET

# 请求数限制
- 默认返回所有关联的项目集


# 请求参数
|字段名|必选|类型及范围|说明|特殊规则|
|:----:|:----:|:----:|:----:|:----:|
| workspace_id | `是` | integer | 项目ID |  |
| story_id | 否 | integer | 需求ID |  |
| user_nick | 否 | string | 用户昵称 |  |


# 调用示例及返回结果
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password'  '${TAPD_API_ENDPOINT}/stories/get_program_list_by_story_id?workspace_id=10104801&story_id=1010104801117731890&user_nick=anyechen'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN'  '${TAPD_API_ENDPOINT}/stories/get_program_list_by_story_id?workspace_id=10104801&story_id=1010104801117731890&user_nick=anyechen'`

### 返回结果
```JSON
{
    "status": 1,
    "data": [
        {
            "program_id": "70135033",
            "operator": "anyechen",
            "modified": "2024-07-16 15:34:57",
            "logo": false,
            "can_unbind": 1,
            "program_name": "暗夜项目集"
        }
    ],
    "info": "success"
}
```

# 字段说明
## 返回字段说明
|字段|说明|
|:----:|:----:|
| program_id | 项目集ID |
| program_name | 项目集名称 |
| operator | 关联操作人 |
| modified | 关联时间 |
| can_unbind | 是否可解绑 |
