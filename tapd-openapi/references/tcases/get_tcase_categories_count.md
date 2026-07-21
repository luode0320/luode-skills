# 说明
计算符合查询条件的测试计划数量并返回


# url
`${TAPD_API_ENDPOINT}/tcase_categories/count`

# 支持格式
JSON/XML（默认JSON格式）

#  HTTP请求方式
GET

# 请求数限制
只返回测试计划数量

# 请求参数
|字段名|必选|类型及范围|说明|特殊规则|
|:----:|:----:|:----:|:----:|:----:|
| id | 否 | integer | id | 支持多ID查询 |
| workspace_id | `是` | integer | 项目ID |  |
| name | 否 | string | 目录名称 | 支持模糊匹配 |
| description | 否 | string | 目录描述 |  |
| parent_id | 否 | integer | 父目录ID |  |
| modified | 否 | datetime | 最后修改时间 | 支持时间查询 |
| created | 否 | datetime | 创建时间 | 支持时间查询 |
| creator | 否 | string | 目录创建人 |  |
| modifier | 否 | string | 目录最后修改人 |  |
| sorting | 否 | integer | 目录排序序号 |  |


# 调用示例及返回结果
## 获取项目下用例目录数量
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password'  '${TAPD_API_ENDPOINT}/tcase_categories/count?workspace_id=10158231'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN'  '${TAPD_API_ENDPOINT}/tcase_categories/count?workspace_id=10158231'`

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
