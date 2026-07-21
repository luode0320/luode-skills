# 说明
* 获取测试计划关联的需求ID


# url
`${TAPD_API_ENDPOINT}/test_plans/get_relative_stories`

# 支持格式
JSON/XML（默认JSON格式）

# HTTP请求方式
GET

# 请求数限制
一次获取一条测试计划关联的需求

# 请求参数
|字段名|必选|类型及范围|说明|特殊规则|
|:----:|:----:|:----:|:----:|:----:|
| workspace_id | `是` | integer | 项目ID |  |
| test_plan_id |  `是` | integer | 测试计划ID | |


# 调用示例及返回结果
## 获取测试计划执行进度
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password'  '${TAPD_API_ENDPOINT}/test_plans/get_relative_stories?workspace_id=10104801&test_plan_id=1010104801077236545'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN'  '${TAPD_API_ENDPOINT}/test_plans/get_relative_stories?workspace_id=10104801&test_plan_id=1010104801077236545'`

### 返回结果
```JSON
{
    "status": 1,
    "data": {
        "story_ids": [
            "1010104801500706241",
            "1010104801854890913"
        ]
    },
    "info": "success"
}
```
