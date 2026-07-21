# 说明
返回符合查询条件的所有需求关联的缺陷ID


# url
`${TAPD_API_ENDPOINT}/stories/get_related_bugs`

# 支持格式
JSON/XML（默认JSON格式）

# HTTP请求方式
GET

# 请求数限制
默认返回所有关系

# 请求参数
|字段名|必选|类型及范围|说明|特殊规则|
|:----:|:----:|:----:|:----:|:----:|
| workspace_id | `是` | integer | 项目ID |  |
| story_id | `是` | integer | 需求ID | 支持多ID查询 |

# 调用示例及返回结果
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password'  '${TAPD_API_ENDPOINT}/stories/get_related_bugs?workspace_id=10104801&story_id=1010104801866181263'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN'  '${TAPD_API_ENDPOINT}/stories/get_related_bugs?workspace_id=10104801&story_id=1010104801866181263'`

### 返回结果
```JSON
{
    "status": 1,
    "data": [
        {
            "workspace_id": 10104801,
            "story_id": "1010104801866181263",
            "bug_id": "1010104801083691309"
        },
        {
            "workspace_id": 10104801,
            "story_id": "1010104801866181263",
            "bug_id": "1010104801085894269"
        },
        {
            "workspace_id": 10104801,
            "story_id": "1010104801866181263",
            "bug_id": "1010104801083691321"
        },
        {
            "workspace_id": 10104801,
            "story_id": "1010104801866181263",
            "bug_id": "1010104801083691305"
        }
    ],
    "info": "success"
}
```

# 需求关联缺陷字段说明
## 需求关联缺陷重要字段说明
|字段|说明|
|:----:|:----:|
| workspace_id | 项目ID |
| story_id | 需求ID |
| bug_id | 缺陷ID |
