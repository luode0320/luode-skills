# 说明
计算符合查询条件的测试用例数量并返回


# url
`${TAPD_API_ENDPOINT}/tcases/count`

# 支持格式
JSON/XML（默认JSON格式）

#  HTTP请求方式
GET

# 请求数限制
只返回测试用例数量

# 请求参数
|字段名|必选|类型及范围|说明|特殊规则|
|:----:|:----:|:----:|:----:|:----:|
| id | 否 | integer | id | 支持多ID查询 |
| steps | 否 | string | 用例步骤 |  |
| workspace_id | `是` | integer | 项目ID |  |
| category_id | 否 | integer | 用例目录 |  |
| created | 否 | datetime | 创建时间 | 支持时间查询 |
| modifier | 否 | string | 最后修改人 |  |
| modified | 否 | datetime | 最后修改时间 | 支持时间查询 |
| creator | 否 | string | 创建人 |  |
| status | 否 | enum('updating','abandon','normal') | 用例状态 |  |
| name | 否 | string | 用例名称 | 支持模糊匹配 |
| precondition | 否 | string | 前置条件 |  |
| expectation | 否 | string | 预期结果 |  |
| type | 否 | string | 用例类型 |  |
| priority | 否 | string | 用例等级 |  |
| is_automated | 否 | string | 是否实现自动化 |  |
| automation_type | 否 | string | 自动化测试类型 |  |
| automation_platform | 否 | string | 自动化测试平台 |  |
| is_serving | 否 | string | 是否上架  |  |
| custom_field_* | 否 | string或者integer | 自定义字段参数，具体字段名通过接口 {{custom_field_url}} 获取 | |
| test_plan_id | 否 | int| 测试计划ID | 该参数可以获取当前测试计划关联的测试用例数量  |
| custom_field_* | 否 | string或者integer | 自定义字段参数，具体字段名通过接口 {{custom_field_url}} 获取 | |

# 调用示例及返回结果
## 获取项目下测试用例数量
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password'  '${TAPD_API_ENDPOINT}/tcases/count?workspace_id=10158231'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN'  '${TAPD_API_ENDPOINT}/tcases/count?workspace_id=10158231'`

### 返回结果
```JSON
{
    "status": 1,
    "data": {
        "count": 10
    },
    "info": "success"
}
```
