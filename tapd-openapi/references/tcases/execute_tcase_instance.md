# 说明
执行测试用例，支持批量修改


# url
`${TAPD_API_ENDPOINT}/tcase_instance/execute`

# 支持格式
JSON/XML（默认JSON格式）

# HTTP请求方式
POST

# 请求数限制
最大支持10条

# 请求参数
|字段名|必选|类型及范围|说明|特殊规则|
|:----:|:----:|:----:|:----:|:----:|
| test_plan_id |  `是` | integer | 测试计划ID | |
| tcase_id |  `是` | integer | 用例ID | 支持批量执行 |
| workspace_id | `是` | integer | 项目ID |  |
| result_status | `是` | string | 执行结果 |  |
| last_executor | `是` | string | 执行人 |  |
| result_remark | `否` | string | 实际执行结果 |  |

# 调用示例及返回结果
## 获取项目下测试用例
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password' -d 'test_plan_id=1010158231077224799&tcase_id=1020357849077231381&result_status=pass&workspace_id=10158231' '${TAPD_API_ENDPOINT}/tcase_instance/execute'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN'  -d 'test_plan_id=1010158231077224799&tcase_id=1020357849077231381&result_status=pass&workspace_id=10158231' '${TAPD_API_ENDPOINT}/tcase_instance/execute'`

### 返回结果
```JSON
{
    "status": 1,
    "data": [],
    "info": "success"
}
```
## 结果状态(result_status)取值字段说明
|pass|通过|
|no_pass|不通过|
|block|阻塞|
