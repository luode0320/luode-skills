# 说明
获取指定分类下需求数量


# url
`${TAPD_API_ENDPOINT}/stories/count_by_categories`

# 支持格式
JSON/XML（默认JSON格式）

#  HTTP请求方式
GET

# 请求数限制
返回需求数量，会返回子分类的数量，及做子分类下面需求数量的累加。


# 请求参数
|字段名|必选|类型及范围|说明|特殊规则|
|:----:|:----:|:----:|:----:|:----:|
| workspace_id | `是` | integer | 项目ID |  |
| category_id | 否 | integer | 需求分类 | 支持多ID。比如 id1,id2,id3 |


# 调用示例及返回结果
## 获取指定分类下需求数量
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password'  '${TAPD_API_ENDPOINT}/stories/count_by_categories?workspace_id=10158231&category_id=1010104801000079035,1010104801000086901'`


### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN'  '${TAPD_API_ENDPOINT}/stories/count_by_categories?workspace_id=10158231&category_id=1010104801000079035,1010104801000086901'`


### 返回结果
```JSON
{
    "status": 1,
    "data": {
        "1010104801000079035": 4,
        "1010104801000086901": 2,
        "1010104801003796129": 1,
        "1010104801000086915": 0,
        "1010104801000079037": 2
    },
    "info": "success"
}
```
