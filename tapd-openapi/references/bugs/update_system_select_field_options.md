# 说明
修改缺陷系统字段选项,会覆盖掉原有选项


# url
`${TAPD_API_ENDPOINT}/bugs/update_system_select_field_options`

# 支持格式
JSON/XML（默认JSON格式）

#  HTTP请求方式
POST

# 请求数限制
一次返回所有符合条件的值


# 请求参数
|字段名|必选|类型及范围|说明|特殊规则|
|:----:|:----:|:----:|:----:|:----:|
|workspace_id|`是`|integer|项目ID|无|
|field|`是`|string|字段 目前支持: bugtype（缺陷类型）|无|
|options|`是`|array|选项列表|无|
|value|`是`|string|选项对应value|无|

# 调用示例及返回结果
## 修改bugtype的选项为test和test111
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password'  '${TAPD_API_ENDPOINT}/bugs/update_system_select_field_options --data '{"workspace_id": 62187798,"field": "bugtype","options": [{"value": "test"},{"value": "test111"}]}'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN'  '${TAPD_API_ENDPOINT}/bugs/update_system_select_field_options --data '{"workspace_id": 62187798,"field": "bugtype","options": [{"value": "test"},{"value": "test111"}]}'`

### 返回结果
```JSON
{
    "status": 1,
    "data": true,
    "info": "success"
}
```

# 字段说明
## 重要字段说明
|字段|说明|
|:----:|:----:|
