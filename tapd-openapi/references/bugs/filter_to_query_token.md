## 说明
将过滤条件转换成页面能用的 QueryToken


## url
`${TAPD_API_ENDPOINT}/bugs/filter_to_query_token`

## 支持格式
JSON/XML（默认JSON格式）

##  HTTP 请求方式
POST

## 请求数限制
过滤条件不能超过10个

## 请求参数
|字段名|必选|类型及范围|                              说明                               |
|:----:|:----:|:----:|:-------------------------------------------------------------:|
| workspace_id | `是` | integer |                             项目ID                              |
| filter[owner]   | `是` | string | 过滤条件，格式为 filter[字段名] = 过滤值，如 filter[current_owner]=当前登录用户;张三; |
| block_type | `否` | string |                             分组字段                              |
| show_fields | `否` | string |                          显示字段，以,号分割                           |

### filter 参数说明
- 时间字段类型说明：filter[created]=2024-12-24 00:00,2024-12-24 23:59
- 成员名称字段类型说明：filter[owner]=当前登录用户;张三;

## 调用示例及返回结果
### 把缺陷过滤条件转换成 queryToken 及返回列表链接
#### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password' -d 'workspace_id=20358527&filter[custom_field_one]=是&show_fields=title,current_owner,status,custom_field_one&block_type=current_owner' '${TAPD_API_ENDPOINT}/bugs/filter_to_query_token'`

#### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN' -d 'workspace_id=20358527&filter[custom_field_one]=是&show_fields=title,current_owner,status,custom_field_one&block_type=current_owner' '${TAPD_API_ENDPOINT}/bugs/filter_to_query_token'`

#### 返回结果


## 重要字段说明

该接口过滤字段和值与 WEB 页面过滤器保持一致，与其他API略有差异，请注意

|       字段       |             说明              |
|:--------------:|:---------------------------:|
|     status     |        状态，传别名（一般是中文）        |
|    severity    |   缺陷严重程度，传英文，具体值参考下面字段说明    |
| priority_label | 优先级，页面显示值，与 priority 存在映射关系 |

其他缺陷字段说明，请参考 [缺陷说明](/api-doc/API文档/api_reference/bug/bug.html)

### 返回字段字段说明
|字段|说明|
|:----:|:----:|
| queryToken | 列表queryToken |
| href | 对应的TAPD缺陷列表链接 |
