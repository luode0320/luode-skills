# 说明
* 支持修改测试用例执行人、负责人
* 支持通过tcase_id批量修改
* 支持通过用例目录批量修改


# url
`${TAPD_API_ENDPOINT}/tcase_instance/assign`

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
| tcase_id |  否 | integer | 用例ID | 支持批量执行，用,分割，如1020357849077231381,1020357849077231382 |
| category_id | 否 | integer | 用例目录ID | tcase_id和category_id不能同时为空|
| workspace_id | `是` | integer | 项目ID |  |
| executor | 否 | string | 执行人 |  |
| assignee| 否 | string | 负责人 |  |

# 调用示例及返回结果
## 分配测试用例
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password' -d 'test_plan_id=1010158231077224799&tcase_id=1020357849077231381&executor=peter&workspace_id=10158231' '${TAPD_API_ENDPOINT}/tcase_instance/assign'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN'  -d 'test_plan_id=1010158231077224799&tcase_id=1020357849077231381&executor=peter&workspace_id=10158231' '${TAPD_API_ENDPOINT}/tcase_instance/assign'`

### 返回结果
```JSON
{
    "status": 1,
    "data": [],
    "info": "success"
}
```
