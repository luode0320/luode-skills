# 说明
返回符合查询条件的所有缺陷模板


# url
`${TAPD_API_ENDPOINT}/bugs/template_list`

# 支持格式
JSON/XML（默认JSON格式）

#  HTTP请求方式
GET

# 请求数限制
默认返回所有缺陷模板

# 请求参数
|字段名|必选|类型及范围|说明|特殊规则|
|:----:|:----:|:----:|:----:|:----:|
|workspace_id|`是`|integer|项目ID||

# 调用示例及返回结果
`curl -u 'api_user:api_password' '${TAPD_API_ENDPOINT}/bugs/template_list?workspace_id=10104801'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN'  '${TAPD_API_ENDPOINT}/bugs/template_list?workspace_id=10104801'`

## 返回结果
```JSON
{
    "status": 1,
    "data": [
        {
            "WorkitemTemplate": {
                "id": "1010104801000068639",
                "name": "创建模板",
                "description": "AA",
                "sort": "1",
                "default": "0",
                "creator": "v_xuanfang",
                "editor_type": "1"
            }
        },
        {
            "WorkitemTemplate": {
                "id": "1010104801000031595",
                "name": "System default template",
                "description": "Auto created by the system",
                "sort": "1",
                "default": "1",
                "creator": "SYSTEM",
                "editor_type": "1"
            }
        }
    ],
    "info": "success"
}
```
# 缺陷模板字段说明
## 缺陷模板重要字段说明
|字段|说明|
|:----:|:----:|
|workspace_id|项目ID|
|id|模板ID|
|name|标题|
|description|详细描述|
|default|是否启用|
|creator|提交人|
