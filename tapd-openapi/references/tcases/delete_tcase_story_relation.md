# 说明
将测试用例移出测试计划，同时解除测试用例和需求的关联关系


# url
`${TAPD_API_ENDPOINT}/tcase_instance/delete_tcase_story_relation`

# 支持格式
JSON/XML（默认JSON格式）

# HTTP请求方式
POST

# 请求数限制
支持批量移出测试用例

# 请求参数
|字段名|必选|类型及范围|说明|特殊规则|
|:----:|:----:|:----:|:----:|:----:|
| workspace_id | `是` | integer | 项目ID |  |
| story_id | `是` | integer | 需求ID |  |
| tcase_id | `是` | integer | 测试用例ID |  |
| test_plan_id | `是` | integer | 测试计划ID |  |

# 调用示例及返回结果
## 将测试用例移出测试计划，同时解除测试用例和需求的关联关系
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password' -d 'workspace_id=10158231&story_id=1020357849500705291&tcase_id=1020357849077231363&test_plan_id=1020357849000015397' '${TAPD_API_ENDPOINT}/tcase_instance/delete_tcase_story_relation'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN'  -d 'workspace_id=10158231&story_id=1020357849500705291&tcase_id=1020357849077231363&test_plan_id=1020357849000015397' '${TAPD_API_ENDPOINT}/tcase_instance/delete_tcase_story_relation'`

### 返回结果
```JSON
{
    "status": 1,
    "data": true,
    "info": "success"
}
```
```
