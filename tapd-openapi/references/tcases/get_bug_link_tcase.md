# 说明
返回缺陷关联的所有测试用例


# url
`${TAPD_API_ENDPOINT}/tcases/get_bug_link_tcase`

# 支持格式
JSON/XML（默认JSON格式）

# HTTP请求方式
GET

# 请求参数
|     字段名      | 必选  |类型及范围|  说明  |特殊规则|
|:------------:|:---:|:----:|:----:|:----:|
| workspace_id | `是` | integer | 项目ID |  |
|    bug_id    |  `是`  | integer | 缺陷ID |  |

# 调用示例及返回结果
## 获取项目下测试用例
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password'  '${TAPD_API_ENDPOINT}/tcases/get_bug_link_tcase?workspace_id=10158231'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN'  '${TAPD_API_ENDPOINT}/tcase/get_bug_link_tcase?workspace_id=10158231'`

### 返回结果
```JSON
{
  "status": 1,
  "data": {
    "count": 2,
    "list": [
      {
        "id": "1150972960001200014",
        "workspace_id": 50972961,
        "tcase_id": "1150972960001`00021",
        "tcase_name": "用例2",
        "test_plan_name": "测试计划1",
        "test_plan_id": "1150972960001100004",
        "executor": "aabb",
        "executed_at": "2025-05-22 09:48:33",
        "result_status": "通过"
      },
      {
        "id": "1150972960001000015",
        "workspace_id": 50972961,
        "tcase_id": "1150972960001000012",
        "tcase_name": "用例1",
        "test_plan_name": "测试计划1",
        "test_plan_id": "1150972960001000005",
        "executor": "aabb",
        "executed_at": "2025-05-22 09:47:10",
        "result_status": "通过"
      }
    ]
  },
  "info": "success"
}
```

# 测试用例字段说明
## 测试用例重要字段说明
|      字段      |   说明   |
|:------------:|:------:|
|      id      | 测试用例id |
| workspace_id |  项目id  |
|   tcase_id   | 测试用例id |
|  tcase_name  | 测试用例名称 |
|   test_plan_name    | 测试计划名称 |
|   test_plan_id   | 测试计划id |
|   executor   |  执行人   |
|   executed_at    |  执行时间  |
|    result_status    |  执行结果  |
