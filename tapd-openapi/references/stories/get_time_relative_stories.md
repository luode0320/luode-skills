# 说明
获取需求前后置关系


# url
`${TAPD_API_ENDPOINT}/stories/get_time_relative_stories`

# 支持格式
JSON/XML（默认JSON格式）

#  HTTP 请求方式
GET

# 请求数限制
默认返回所有数据

# 请求参数
|字段名|必选|类型及范围|说明|
|:----:|:----:|:----:|:----:|
| workspace_id | `是` | integer | 源项目ID |
| story_id |  `是`  | integer | 源需求ID |

# 调用示例及返回结果
## curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password''${TAPD_API_ENDPOINT}/stories/get_time_relative_stories?workspace_id=10104801&story_id=1010104801854917775'`

## curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN''${TAPD_API_ENDPOINT}/stories/get_time_relative_stories?workspace_id=10104801&story_id=1010104801854917775'`

### 返回结果
```json
{
    "status": 1,
    "data": [
        {
            "WorkitemTimeRelation": {
                "id": "1210104801000007813",
                "workspace_id": "10104801",
                "workitem_type": "story",
                "workitem_id": "1010104801854915911",
                "src_field": "begin",
                "dst_workspace_id": "10104801",
                "dst_workitem_type": "story",
                "dst_workitem_id": "1010104801854917775",
                "dst_field": "due",
                "relation_type": "after"
            }
        },
        {
            "WorkitemTimeRelation": {
                "id": "1210104801000007815",
                "workspace_id": "10104801",
                "workitem_type": "story",
                "workitem_id": "1010104801854917775",
                "src_field": "due",
                "dst_workspace_id": "10104801",
                "dst_workitem_type": "story",
                "dst_workitem_id": "1010104801854917809",
                "dst_field": "begin",
                "relation_type": "after"
            }
        }
    ],
    "info": "success"
}
```

# 需求字段说明
## 需求重要字段说明
|字段|说明|
|:----:|:----:|
| id | ID |
| workspace_id | 源项目ID |
| workitem_type | 业务对象类型，固定为 story |
| workitem_id | 源需求ID |
| src_field | 源需求被依赖的字段 |
| dst_workspace_id | 被依赖的项目ID |
| dst_workitem_type | 被依赖的业务对象类型，固定为 story |
| dst_workitem_id | 被依赖的需求ID |
| dst_field | 被依赖的字段 |
| relation_type | 依赖类型。before 为前置依赖，after 为后置依赖 |
