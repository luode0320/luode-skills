# 说明
返回符合查询条件的所有测试用例&测试计划


# url
`${TAPD_API_ENDPOINT}/stories/get_story_tcase`

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
| story_id | `是` | integer | 需求id |  |
| include_test_plan | 否 | integer | 是否包含测试计划 | 取值为1或0，默认为1 |

# 调用示例及返回结果
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password'  '${TAPD_API_ENDPOINT}/stories/get_story_tcase?workspace_id=10104801&story_id=1010104801866191641'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN'  '${TAPD_API_ENDPOINT}/stories/get_story_tcase?workspace_id=10104801&story_id=1010104801866191641'`

### 返回结果
```JSON

{
    "status": 1,
    "data": [
        {
            "TestPlanStoryTcaseRelation": {
                "id": "1010104801021215005",
                "workspace_id": "10104801",
                "test_plan_id": "0",
                "story_id": "1010104801866191641",
                "tcase_id": "1010104801076110789",
                "sort": "0",
                "creator": "v_xuanfang",
                "created": "2021-08-06 12:35:01"
            }
        }
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
| sort | 显示时排序系数 |
