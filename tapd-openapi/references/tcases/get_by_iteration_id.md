# 说明
返回迭代下的测试计划


# url
`${TAPD_API_ENDPOINT}/test_plans/get_by_iteration_id`

# 支持格式
JSON/XML（默认JSON格式）

# HTTP请求方式
GET

# 请求参数
|     字段名      | 必选  |类型及范围|  说明  |特殊规则|
|:------------:|:---:|:----:|:----:|:----:|
| workspace_id | `是` | integer | 项目ID |  |
| iteration_id |  `是`  | integer | 迭代ID |  |
| limit | 否 | integer | 设置返回数量限制，默认为30 | |
| page | 否 | integer | 返回当前数量限制下第N页的数据，默认为1（第一页）| |
| order | 否 | string | 排序规则，规则：字段名 ASC或者DESC，然后 urlencode |  如按创建时间逆序：order=created%20desc |

# 调用示例及返回结果
## 获取迭代下测试计划
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password'  '${TAPD_API_ENDPOINT}/test_plans/get_by_iteration_id?iteration_id=1151650666001000111&workspace_id=51650666'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN'  '${TAPD_API_ENDPOINT}/test_plans/get_by_iteration_id?iteration_id=1151650666001000111&workspace_id=51650666'`

### 返回结果
```JSON
{
    "status": 1,
    "data": [
        {
            "workspace_id": "51650666",
            "iteration_id": "1151650666001000111",
            "test_plan_id": "1151650666001000019"
        },
        {
            "workspace_id": "51650666",
            "iteration_id": "1151650666001000111",
            "test_plan_id": "1151650666001000018"
        },
        {
            "workspace_id": "51650666",
            "iteration_id": "1151650666001000111",
            "test_plan_id": "1151650666001000017"
        }
    ],
    "info": "success"
}
```

## 字段说明
|      字段      |   说明   |
|:------------:|:------:|
| workspace_id |  项目id  |
|   iteration_id   | 迭代id |
|  test_plan_id  | 测试计划id |
