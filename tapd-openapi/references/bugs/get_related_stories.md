# 说明
返回符合查询条件的所有缺陷关联的需求ID


# url
`${TAPD_API_ENDPOINT}/bugs/get_related_stories`

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
| bug_id | `是` | integer | 缺陷ID | 支持多ID查询 |

# 调用示例及返回结果
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password'  '${TAPD_API_ENDPOINT}/bugs/get_related_stories?workspace_id=10104801&bug_id=1010104801083691309'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN'  '${TAPD_API_ENDPOINT}/bugs/get_related_stories?workspace_id=10104801&bug_id=1010104801083691309'`

### 返回结果
```JSON
{
    "status": 1,
    "data": [
        {
            "workspace_id": "10104801",
            "bug_id": "1010104801083691309",
            "story_id": "1010104801866181263"
        }
    ],
    "info": "success"
}
```

# 缺陷关联需求陷字段说明
## 缺陷关联需求陷重要字段说明
|字段|说明|
|:----:|:----:|
| workspace_id | 项目ID |
| story_id | 需求ID |
| bug_id | 缺陷ID |
