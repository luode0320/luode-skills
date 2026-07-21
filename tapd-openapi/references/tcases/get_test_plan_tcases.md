# 说明
返回符合查询条件的所有测试用例&需求


# url
`${TAPD_API_ENDPOINT}/test_plans/get_test_plan_tcase`

# 支持格式
JSON/XML（默认JSON格式）

# HTTP请求方式
GET

# 请求数限制
返回全部数据

# 请求参数
|字段名|必选|类型及范围|说明|特殊规则|
|:----:|:----:|:----:|:----:|:----:|
| workspace_id | `是` | integer | 项目ID |  |
| test_plan_id | `是` | integer | 测试计划id |  |
| limit | 否 | integer | 设置返回数量限制，默认为30 | |
| page | 否 | integer | 返回当前数量限制下第N页的数据，默认为1（第一页）| |
| order | 否 | string | 排序规则，规则：字段名 ASC或者DESC，然后 urlencode |  如按创建时间逆序：order=created%20desc |

# 调用示例及返回结果
## 获取项目下测试用例
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password'  '${TAPD_API_ENDPOINT}/test_plans/get_test_plan_tcase?test_plan_id=1000000755077233617&workspace_id=755'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN'  '${TAPD_API_ENDPOINT}/test_plans/get_test_plan_tcase?test_plan_id=1000000755077233617&workspace_id=755'`

### 返回结果
```JSON

{
    "status": 1,
    "data": [
        {
            "TestPlanStoryTcaseRelation": {
                "id": "1000000755002248699",
                "workspace_id": "755",
                "test_plan_id": "1000000755077233617",
                "story_id": "0",
                "tcase_id": "1000000755000026804",
                "sort": "0",
                "creator": "v_xuanfang",
                "created": "0000-00-00 00:00:00"
            }
        },
        {
            "TestPlanStoryTcaseRelation": {
                "id": "1000000755002248753",
                "workspace_id": "755",
                "test_plan_id": "1000000755077233617",
                "story_id": "0",
                "tcase_id": "1000000755075912019",
                "sort": "0",
                "creator": "v_xuanfang",
                "created": "0000-00-00 00:00:00"
            }
        },
    ],
"info": "success"
}

```

# 测试用例字段说明
## 测试用例重要字段说明
|字段|说明|
|:----:|:----:|
| id | 关系id |
| workspace_id | 项目ID |
| test_plan_id | 测试计划ID |
| story_id | 需求ID |
| tcase_id | 测试用例ID |
| created | 关系创建时间 |
| creator | 创建人 |
