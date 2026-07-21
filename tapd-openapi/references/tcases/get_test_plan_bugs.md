# 说明
获取测试计划整体bug情况


# url
`${TAPD_API_ENDPOINT}/test_plans/result_relation_bugs`

# 支持格式
JSON/XML（默认JSON格式）

# HTTP请求方式
GET

# 请求数限制
一次获取一条测试计划的关联bug情况

# 请求参数
|字段名|必选|类型及范围|说明|特殊规则|
|:----:|:----:|:----:|:----:|:----:|
| id |  `是` | integer | 测试计划ID | |
| workspace_id | `是` | integer | 项目ID |  |
| limit | 否 | integer | 设置返回数量限制，默认为30 | |
| page | 否 | integer | 返回当前数量限制下第N页的数据，默认为1（第一页）| |
| order | 否 | string | 排序规则，规则：字段名 ASC或者DESC，然后 urlencode |  如按创建时间逆序：order=created%20desc |

# 调用示例及返回结果
## 获取测试计划关联bug
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password'  '${TAPD_API_ENDPOINT}/test_plans/result_relation_bugs?id=1010158231077224799&workspace_id=10158231'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN'  '${TAPD_API_ENDPOINT}/test_plans/result_relation_bugs?id=1010158231077224799&workspace_id=10158231'`

### 返回结果
```JSON
{
    "status": 1,
    "data": [
        {
            "id": 1020357849077231365,
            "name": "用例2",
            "tcase_result_relate_bugs": {
                "1020357849000703497": {
                    "id": "1020357849000703497",
                    "executed_at": "2020-03-05 10:15:22",
                    "executor": "jeffjffang",
                    "result_status": "no_pass",
                    "result_remark": null,
                    "bug_id": [
                        "1020357849500646067"
                    ],
                    "Bug": [
                        {
                            "id": "1020357849500646067",
                            "title": "【示例】缺陷1",
                            "severity": "serious",
                            "priority": "high",
                            "status": "接受/处理"
                        }
                    ]
                }
            }
        },
        {
            "id": 1020357849077231363,
            "name": "用例1",
            "tcase_result_relate_bugs": {
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
            }
        }
    ],
    "info": "success"
}
```
