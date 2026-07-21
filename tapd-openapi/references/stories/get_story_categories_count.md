# 说明
计算符合查询条件的需求分类数量并返回


# url
`${TAPD_API_ENDPOINT}/story_categories/count`

# 支持格式
JSON/XML（默认JSON格式）

#  HTTP请求方式
GET

# 请求数限制
只返回需求分类数量

# 请求参数
|字段名|必选|类型及范围|说明|特殊规则|
|:----:|:----:|:----:|:----:|:----:|
| id | 否 | integer | id | 支持多ID查询 |
| workspace_id | `是` | integer | 项目ID |  |
| name | 否 | string | 需求分类名称 | 支持模糊匹配 |
| description | 否 | string | 需求分类描述 |  |
| parent_id | 否 | integer | 父分类ID |  |
| created | 否 | datetime | 创建时间 | 支持时间查询 |
| modified | 否 | datetime | 最后修改时间 | 支持时间查询 |


# 调用示例及返回结果
## 获取项目下需求分类数量
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password'  '${TAPD_API_ENDPOINT}/story_categories/count?workspace_id=10158231'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN'  '${TAPD_API_ENDPOINT}/story_categories/count?workspace_id=10158231'`

### 返回结果
```JSON
{
    "status": 1,
    "data": {
        "count": 5
    },
    "info": "success"
}
```
