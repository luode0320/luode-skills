# 说明
返回符合查询条件的所有需求ID和测试计划ID


# url
`${TAPD_API_ENDPOINT}/tcases/get_story_by_tcase_id?workspace_id=20358306&tcase_ids=1020358306077237055,1020358306077237053`

# 支持格式
JSON/XML（默认JSON格式）

# HTTP请求方式
GET

# 请求数限制
tcase_ids 多个使用,隔开，一次最多传20个

# 请求参数
|字段名|必选|类型及范围|说明|特殊规则|
|:----:|:----:|:----:|:----:|:----:|
| workspace_id | `是` | integer | 项目ID |  |
| tcase_ids | `是` | integer | 测试用例ID | 多个用 , 隔开 |

# 调用示例及返回结果
## 获取项目下测试用例
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password'  '${TAPD_API_ENDPOINT}/tcases/get_story_by_tcase_id?workspace_id=20358306&tcase_ids=1020358306077237055,1020358306077237053'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN'  '${TAPD_API_ENDPOINT}/tcases/get_story_by_tcase_id?workspace_id=20358306&tcase_ids=1020358306077237055,1020358306077237053'`

### 返回结果
```JSON

{
    "status": 1,
    "data": [
        {
            "workspace_id": "20358306",
            "tcase_id": "1020358306077237053",
            "story_id": "1020358306854812395",
            "test_plan_id": "0"
        },
        {
            "workspace_id": "20358306",
            "tcase_id": "1020358306077237055",
            "story_id": "1020358306854812395",
            "test_plan_id": "0"
        }
    ],
    "info": "success"
}


```

# 测试用例字段说明
## 测试用例重要字段说明
|字段|说明|
|:----:|:----:|
| workspace_id | 项目ID |
| tcase_id | 测试用例ID |
| story_id | 需求ID |
| test_plan_id | 测试计划ID |
