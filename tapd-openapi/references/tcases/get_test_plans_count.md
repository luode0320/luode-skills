# 说明
计算符合查询条件的测试计划数量并返回


# url
`${TAPD_API_ENDPOINT}/test_plans/count`

# 支持格式
JSON/XML（默认JSON格式）

#  HTTP请求方式
GET

# 请求数限制
只返回评论数量

# 请求参数
|字段名|必选|类型及范围|说明|
|:----:|:----:|:----:|:----:|
| name | 否 | string | 测试计划标题 |
| description | 否 | string | 测试计划详细描述 |
| workspace_id | `是` | integer | 项目ID |
| creator | 否 | string | 创建人 |
| modifier| 否 | string | 修改人 |
| owner | 否 | string | 测试计划负责人 |
| start_date| 否 | date | 预计开始 |
| end_date | 否 | date | 预计结束 |
| iteration_id | 否 | integer | 关联迭代的ID |
| version| 否 | string | 版本号 |
| type| 否 | float | 测试类型 |
| status | 否 | string | 状态，默认开启，值为open |

# 调用示例及返回结果
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password'  '${TAPD_API_ENDPOINT}/test_plans/count?workspace_id=10104801'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN' '${TAPD_API_ENDPOINT}/test_plans/count?workspace_id=10104801'`

### 返回结果
```JSON
{
    "status": 1,
    "data": {
        "count": 4
    },
    "info": "success"
}
```
