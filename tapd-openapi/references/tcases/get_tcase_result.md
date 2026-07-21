# 说明
获取测试用例的执行结果，及关联bug的情况


# url
`${TAPD_API_ENDPOINT}/tcase_instance/result`

# 支持格式
JSON/XML（默认JSON格式）

# HTTP请求方式
GET

# 请求数限制
一次获取一条测试用例执行结果

# 请求参数
|字段名|必选|类型及范围|说明|特殊规则|
|:----:|:----:|:----:|:----:|:----:|
| test_plan_id |  `是` | integer | 测试计划ID | |
| tcase_id |  `是` | integer | 用例ID | |
| workspace_id | `是` | integer | 项目ID |  |

# 调用示例及返回结果
## 分配测试用例
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password' '${TAPD_API_ENDPOINT}/tcase_instance/result?test_plan_id=1010158231077224799&tcase_id=1020357849077231381&workspace_id=10158231'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN'  '${TAPD_API_ENDPOINT}/tcase_instance/result?test_plan_id=1010158231077224799&tcase_id=1020357849077231381&workspace_id=10158231'`

### 返回结果
```JSON
{
    "status": 1,
    "data": {
        "1020357849000703565": {
            "id": "1020357849000703565",
            "executed_at": "2020-03-06 17:46:13",
            "executor": "jeffjffang",
            "result_status": "pass",
            "result_remark": null,
            "bug_id": [],
            "Bug": []
        },
        "1020357849000703563": {
            "id": "1020357849000703563",
            "executed_at": "2020-03-06 17:33:49",
            "executor": "jeffjffang",
            "result_status": "no_pass",
            "result_remark": null,
            "bug_id": [],
            "Bug": []
        },
        "1020357849000703543": {
            "id": "1020357849000703543",
            "executed_at": "2020-03-05 16:05:21",
            "executor": "jeffjffang",
            "result_status": "pass",
            "result_remark": null,
            "bug_id": [],
            "Bug": []
        },
        "1020357849000703535": {
            "id": "1020357849000703535",
            "executed_at": "2020-03-05 14:50:28",
            "executor": "jeffjffang",
            "result_status": "no_pass",
            "result_remark": null,
            "bug_id": [],
            "Bug": []
        },
        "1020357849000703491": {
            "id": "1020357849000703491",
            "executed_at": "2020-03-05 10:14:19",
            "executor": "jeffjffang",
            "result_status": "block",
            "result_remark": null,
            "bug_id": [],
            "Bug": []
        },
        "1020357849000703489": {
            "id": "1020357849000703489",
            "executed_at": "2020-03-05 10:12:03",
            "executor": "jeffjffang",
            "result_status": "no_pass",
            "result_remark": null,
            "bug_id": [],
            "Bug": []
        },
        "1020357849000703483": {
            "id": "1020357849000703483",
            "executed_at": "2020-03-04 17:29:29",
            "executor": "jeffjffang",
            "result_status": "pass",
            "result_remark": null,
            "bug_id": [
                "1020357849500655643",
                "1020357849500655855"
            ],
            "Bug": [
                {
                    "id": "1020357849500655643",
                    "title": "1231",
                    "severity": "",
                    "priority": "",
                    "status": "新"
                },
                {
                    "id": "1020357849500655855",
                    "title": "用例失败bug关联",
                    "severity": "",
                    "priority": "",
                    "status": "新"
                }
            ]
        }
    },
    "info": "success"
}
```
# 返回结果重要字段说明
|字段名|说明|
|:----:|:----:|
| id  | ID |
| executed_at | 执行时间 |
| executor | 执行人 |
| result_status | 执行结果 |
| result_remark | 执行结果备注 |
| bug_id | 关联缺陷ID |
| Bug | 关联缺陷详情 |
