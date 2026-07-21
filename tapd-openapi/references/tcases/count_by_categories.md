# 说明
获取指定目录下用例数量


# url
`${TAPD_API_ENDPOINT}/tcases/count_by_categories`

# 支持格式
JSON/XML（默认JSON格式）

#  HTTP请求方式
GET

# 请求数限制
返回用例数量，会返回子目录的数量，及做子分类下面用例数量的累加。


# 请求参数
|字段名|必选|类型及范围|说明|特殊规则|
|:----:|:----:|:----:|:----:|:----:|
| workspace_id | `是` | integer | 项目ID |  |
| category_id | 否 | integer | 目录ID | 支持多ID。比如 id1,id2,id3 |


# 调用示例及返回结果
## 获取指定目录下用例数量
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password'  '${TAPD_API_ENDPOINT}/tcases/count_by_categories?workspace_id=755&category_id=1000000755000075865,1000000755000072430,1000000755075915401,1000000755000065944'`


### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN'  '${TAPD_API_ENDPOINT}/tcases/count_by_categories?workspace_id=755&category_id=1000000755000075865,1000000755000072430,1000000755075915401,1000000755000065944'`


### 返回结果
```JSON
{
    "status": 1,
    "data": {
        "1000000755000065944": 11,
        "1000000755000072430": 7,
        "1000000755000075865": 36,
        "1000000755075915401": 7,
        "1000000755000072435": 0,
        "1000000755000067336": 0
    },
    "info": "success"
}
```
