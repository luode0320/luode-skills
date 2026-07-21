# 说明
返回符合查询条件的所有缺陷模板字段


# url
`${TAPD_API_ENDPOINT}/bugs/get_default_bug_template`

# 支持格式
JSON/XML（默认JSON格式）

#  HTTP请求方式
GET

# 请求数限制
默认返回所有缺陷模板字段

# 请求参数
|字段名|必选|类型及范围|说明|特殊规则|
|:----:|:----:|:----:|:----:|:----:|
|workspace_id|`是`|integer|项目ID||
|template_id|`是`|integer|模板ID||
|use_priority_label|否|integer|是否替换优先级字段为 priority_label。取值0和1，默认值是 0 ||

# 调用示例及返回结果
`curl -u 'api_user:api_password' '${TAPD_API_ENDPOINT}/bugs/get_default_bug_template?template_id=1010104801000068639&workspace_id=10104801'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN'  '${TAPD_API_ENDPOINT}/bugs/get_default_bug_template?template_id=1010104801000068639&workspace_id=10104801'`

## 返回结果
```JSON
{
    "status": 1,
    "data": [
        {
            "WorkitemTemplateField": {
                "id": "1010104801000778831",
                "workspace_id": "10104801",
                "type": "bug",
                "template_id": "1010104801000068639",
                "field": "title",
                "value": "",
                "required": "1",
                "sort": "0"
            }
        },
        {
            "WorkitemTemplateField": {
                "id": "1010104801000778833",
                "workspace_id": "10104801",
                "type": "bug",
                "template_id": "1010104801000068639",
                "field": "description",
                "value": "",
                "required": "1",
                "sort": "0"
            }
        },
        {
            "WorkitemTemplateField": {
                "id": "1010104801000778835",
                "workspace_id": "10104801",
                "type": "bug",
                "template_id": "1010104801000068639",
                "field": "current_owner",
                "value": "",
                "required": "1",
                "sort": "1"
            }
        },
        {
            "WorkitemTemplateField": {
                "id": "1010104801000778837",
                "workspace_id": "10104801",
                "type": "bug",
                "template_id": "1010104801000068639",
                "field": "module",
                "value": "test2",
                "required": "0",
                "sort": "2"
            }
        },
        {
            "WorkitemTemplateField": {
                "id": "1010104801000778839",
                "workspace_id": "10104801",
                "type": "bug",
                "template_id": "1010104801000068639",
                "field": "priority",
                "value": "",
                "required": "1",
                "sort": "3"
            }
        },
        {
            "WorkitemTemplateField": {
                "id": "1010104801000778841",
                "workspace_id": "10104801",
                "type": "bug",
                "template_id": "1010104801000068639",
                "field": "severity",
                "value": "",
                "required": "0",
                "sort": "4"
            }
        },
        {
            "WorkitemTemplateField": {
                "id": "1010104801000778847",
                "workspace_id": "10104801",
                "type": "bug",
                "template_id": "1010104801000068639",
                "field": "version_report",
                "value": "",
                "required": "0",
                "sort": "5"
            }
        },
        {
            "WorkitemTemplateField": {
                "id": "1010104801000778843",
                "workspace_id": "10104801",
                "type": "bug",
                "template_id": "1010104801000068639",
                "field": "begin",
                "value": "",
                "required": "0",
                "sort": "6"
            }
        },
        {
            "WorkitemTemplateField": {
                "id": "1010104801000778845",
                "workspace_id": "10104801",
                "type": "bug",
                "template_id": "1010104801000068639",
                "field": "due",
                "value": "",
                "required": "0",
                "sort": "7"
            }
        }
    ],
    "info": "success"
}
```
# 模板字段说明
## 模板重要字段说明
|字段|说明|
|:----:|:----:|
|workspace_id|项目ID|
|id|模板字段ID|
|type|类型|
|template_id|模板ID|
|field|字段英文名|
|value|默认值|
|required|是否必填|
|sort|计数|
