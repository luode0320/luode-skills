# 说明
创建需求与测试用例关联关系


# url
`${TAPD_API_ENDPOINT}/stories/add_story_tcase`

# 支持格式
JSON/XML（默认JSON格式）

# HTTP请求方式
POST

# 请求数限制
- 测试用例支持传多ID，一次不超过20个

# 请求参数
|字段名|必选|类型及范围|说明|特殊规则|
|:----:|:----:|:----:|:----:|:----:|
| workspace_id | `是` | integer | 项目ID |  |
| story_id | `是` | integer | 需求ID |  |
| tcase_id| `是` | string | 测试用例ID | 支持传多ID，使用英文逗号 , 分隔，不超过20个 |

# 调用示例及返回结果
## 创建需求与测试用例关联关系
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password' -d 'workspace_id=10104801&story_id=1010104801854919725&tcase_id=1010104801077291609' '${TAPD_API_ENDPOINT}/stories/add_story_tcase'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN'  -d 'workspace_id=10104801&story_id=1010104801854919725&tcase_id=1010104801077291609' '${TAPD_API_ENDPOINT}/stories/add_story_tcase'`

### 返回结果
```JSON
{
    "status": 1,
    "data": {
        "success_id": [
            "1010104801077291609"
        ]
    },
    "info": "success"
}
```
