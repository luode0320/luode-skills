## 说明
获取 queryToken 对应的缺陷列表


## url
`${TAPD_API_ENDPOINT}/bugs/get_bugs_by_query_token`

## 支持格式
JSON/XML（默认JSON格式）

##  HTTP 请求方式
GET

## 请求数限制
默认返回 30 条。可通过传 limit 参数设置，最大取 200。也可以传 page 参数翻页

## 请求参数
|字段名|必选|类型及范围|说明|
|:----:|:----:|:----:|:----:|
| workspace_id | `是` | integer | 项目ID |
| query_token |  `是`  | string | query_token |
| page | 否 | integer | 返回当前数量限制下第N页的数据，默认为1（第一页） |
| limit | 否 | integer | 设置返回数量限制，默认为30 |

## 调用示例及返回结果
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password' 'http://apiv2.tapd.oa.com/bugs/get_bugs_by_query_token?workspace_id=755&query_token=5bd5467b2cbe938649999ddcdd2a5ad5'`

#### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN' 'http://apiv2.tapd.oa.com/bugs/get_bugs_by_query_token?workspace_id=755&query_token=5bd5467b2cbe938649999ddcdd2a5ad5'`

#### 返回结果


# 缺陷字段说明
缺陷字段说明，请参考 [缺陷说明](/api-doc/API文档/api_reference/bug/bug.html)
