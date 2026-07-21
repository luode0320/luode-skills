## 说明
把一批缺陷ID转换成页面能用的 QueryToken


## url
`${TAPD_API_ENDPOINT}/bugs/ids_to_query_token`

## 支持格式
JSON/XML（默认JSON格式）

##  HTTP 请求方式
POST

## 请求数限制
为了保证页面显示效果，建议ID数量不超过500

## 请求参数
|字段名|必选|类型及范围|说明|
|:----:|:----:|:----:|:----:|
| workspace_id | `是` | integer | 项目ID |
| ids |  `是`  | string | 缺陷ID，使用英文逗号 , 做分隔 |

## 调用示例及返回结果
### 把缺陷ID 1010104801102653321,1010104801085527301 转换成 queryToken 及返回列表链接
#### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password' -d 'workspace_id=10104801&ids=1010104801102653321,1010104801085527301' '${TAPD_API_ENDPOINT}/bugs/ids_to_query_token'`

#### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN' -d 'workspace_id=10104801&ids=1010104801102653321,1010104801085527301' '${TAPD_API_ENDPOINT}/bugs/ids_to_query_token'`

#### 返回结果


## 重要字段说明
### 返回字段字段说明
|字段|说明|
|:----:|:----:|
| queryToken | 列表queryToken |
| href | 对应的TAPD缺陷列表链接 |
