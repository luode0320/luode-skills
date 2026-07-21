# 说明
测试用例移出测试计划


# url
`${TAPD_API_ENDPOINT}/tcase_instance/remove_tcase`

# 支持格式
JSON/XML（默认JSON格式）

# HTTP请求方式
POST

# 请求数限制
支持批量移出测试用例

# 请求参数
|字段名|必选|类型及范围|说明|特殊规则|
|:----:|:----:|:----:|:----:|:----:|
| test_plan_id |  `是` | integer | 测试计划ID | |
| workspace_id | `是` | integer | 项目ID |  |
| story_id | 否 | integer | 需求ID | 如果用例关联了需求，需要传story_id，如果是单独的没有关联需求的用例，不传story_id，否则无法移出 |
| tcase_id | `是` | integer | 测试用例ID，多个测试用例之间用,分割 |  |

# 调用示例及返回结果
## 测试用例移出测试计划
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password' -d 'test_plan_id=1010158231077224799&workspace_id=10158231&story_id=1020357849500705291&tcase_id=1020357849077231363' '${TAPD_API_ENDPOINT}/tcase_instance/remove_tcase'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN'  -d 'test_plan_id=1010158231077224799&workspace_id=10158231&story_id=1020357849500705291&tcase_id=1020357849077231363' '${TAPD_API_ENDPOINT}/tcase_instance/remove_tcase'`

### 返回结果
```JSON
{
    "status": 1,
    "data": null,
    "info": "success"
}
```
