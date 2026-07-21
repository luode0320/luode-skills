# 说明
* 获取测试计划整体执行进度
* 获取指定执行人的测试计划执行进度


# url
`${TAPD_API_ENDPOINT}/test_plans/progress`

# 支持格式
JSON/XML（默认JSON格式）

# HTTP请求方式
GET

# 请求数限制
一次获取一条测试计划执行进度

# 请求参数
|字段名|必选|类型及范围|说明|特殊规则|
|:----:|:----:|:----:|:----:|:----:|
| id |  `是` | integer | 测试计划ID | |
| workspace_id | `是` | integer | 项目ID |  |


# 调用示例及返回结果
## 获取测试计划执行进度
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password'  '${TAPD_API_ENDPOINT}/test_plans/progress?id=1010158231077224799&workspace_id=10158231'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN'  '${TAPD_API_ENDPOINT}/test_plans/progress?id=1010158231077224799&last_executor=peter&workspace_id=10158231'`

### 返回结果
```JSON
{
    "status": 1,
    "data": {
        "story_count": 1,
        "tcase_count": 10,
        "status_counter": {
            "pass": "5",
            "no_pass": "0",
            "block": "0",
            "unexecuted": 5
        },
        "executed_rate": "50%"
    },
    "info": "success"
}
```
