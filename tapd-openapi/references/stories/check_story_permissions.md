# 说明
批量检查指定用户是否有某些需求查看权限


# url
`${TAPD_API_ENDPOINT}/stories/check_story_permissions`

# 支持格式
JSON/XML（默认JSON格式）

#  HTTP请求方式
GET

# 请求数限制
- 一次只能检查一个项目
- 为防止URL过长导致异常，建议 story_ids 里面需求ID数量不超过50个


# 请求参数
|字段名|必选|类型及范围|说明|特殊规则|
|:----:|:----:|:----:|:----:|:----:|
| workspace_id | `是` | integer | 项目ID |  |
| story_ids | `是` | string | 需求ID | 支持多ID。比如 id1,id2,id3 ，建议不超过50个 |
| nick | `是` | string | 用户昵称 |  |


# 调用示例及返回结果
## 批量检查指定用户 someone 是否有某些需求查看权限
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password'  '${TAPD_API_ENDPOINT}/stories/check_story_permissions?workspace_id=10104801&story_ids=1010104801005762633,1010104801005742817,1010104801005775125&nick=someone'`


### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN'  '${TAPD_API_ENDPOINT}/stories/check_story_permissions?workspace_id=10104801&story_ids=1010104801005762633,1010104801005742817,1010104801005775125&nick=someone'`


### 返回结果
```JSON
{
    "status": 1,
    "data": {
        "1010104801005762633": false,
        "1010104801005742817": true,
        "1010104801005775125": false
    },
    "info": "success"
}
```
