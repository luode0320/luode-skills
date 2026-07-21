# 说明
返回符合查询条件的所有需求模板字段


# url
`${TAPD_API_ENDPOINT}/stories/get_default_story_template`

# 支持格式
JSON/XML（默认JSON格式）

#  HTTP请求方式
GET

# 请求数限制
默认返回所有需求模板字段

# 请求参数
|字段名|必选|类型及范围|说明|特殊规则|
|:----:|:----:|:----:|:----:|:----:|
|workspace_id|`是`|integer|项目ID||
|template_id|`是`|integer|模板ID||
|use_priority_label|否|integer|是否替换优先级字段为 priority_label。取值0和1，默认值是 0 ||

# 调用示例及返回结果
`curl -u 'api_user:api_password' '${TAPD_API_ENDPOINT}/stories/get_default_story_template?template_id=1010104801000068641&workspace_id=10104801'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN'  '${TAPD_API_ENDPOINT}/stories/get_default_story_template?template_id=1010104801000068641&workspace_id=10104801'`

## 返回结果
```JSON
{
    "status": 1,
    "data": [
        {
            "WorkitemTemplateField": {
                "id": "1010104801015287651",
                "workspace_id": "10104801",
                "type": "story",
                "template_id": "1010104801000850579",
                "field": "description",
                "value": "",
                "required": "1",
                "sort": "0",
                "linkage_rules": ""
            }
        },
        {
            "WorkitemTemplateField": {
                "id": "1010104801015287653",
                "workspace_id": "10104801",
                "type": "story",
                "template_id": "1010104801000850579",
                "field": "name",
                "value": "",
                "required": "1",
                "sort": "0",
                "linkage_rules": ""
            }
        },
        {
            "WorkitemTemplateField": {
                "id": "1010104801016243901",
                "workspace_id": "10104801",
                "type": "story",
                "template_id": "1010104801000850579",
                "field": "sub_stories_auto_succeed_name",
                "value": "",
                "required": "0",
                "sort": "0",
                "linkage_rules": ""
            }
        },
        {
            "WorkitemTemplateField": {
                "id": "1010104801016243903",
                "workspace_id": "10104801",
                "type": "story",
                "template_id": "1010104801000850579",
                "field": "auto_succeed_story_fields",
                "value": "",
                "required": "0",
                "sort": "0",
                "linkage_rules": ""
            }
        },
        {
            "WorkitemTemplateField": {
                "id": "1010104801016243905",
                "workspace_id": "10104801",
                "type": "story",
                "template_id": "1010104801000850579",
                "field": "category_id",
                "value": "",
                "required": "0",
                "sort": "0",
                "linkage_rules": ""
            }
        },
        {
            "WorkitemTemplateField": {
                "id": "1010104801016243907",
                "workspace_id": "10104801",
                "type": "story",
                "template_id": "1010104801000850579",
                "field": "priority",
                "value": "",
                "required": "0",
                "sort": "0",
                "linkage_rules": ""
            }
        },
        {
            "WorkitemTemplateField": {
                "id": "1010104801016243909",
                "workspace_id": "10104801",
                "type": "story",
                "template_id": "1010104801000850579",
                "field": "owner",
                "value": "",
                "required": "1",
                "sort": "0",
                "linkage_rules": ""
            }
        },
        {
            "WorkitemTemplateField": {
                "id": "1010104801016243911",
                "workspace_id": "10104801",
                "type": "story",
                "template_id": "1010104801000850579",
                "field": "iteration_id",
                "value": "",
                "required": "0",
                "sort": "0",
                "linkage_rules": ""
            }
        },
        {
            "WorkitemTemplateField": {
                "id": "1010104801016243913",
                "workspace_id": "10104801",
                "type": "story",
                "template_id": "1010104801000850579",
                "field": "cc",
                "value": "",
                "required": "0",
                "sort": "0",
                "linkage_rules": ""
            }
        },
        {
            "WorkitemTemplateField": {
                "id": "1010104801016243915",
                "workspace_id": "10104801",
                "type": "story",
                "template_id": "1010104801000850579",
                "field": "developer",
                "value": "",
                "required": "0",
                "sort": "0",
                "linkage_rules": ""
            }
        },
        {
            "WorkitemTemplateField": {
                "id": "1010104801016243917",
                "workspace_id": "10104801",
                "type": "story",
                "template_id": "1010104801000850579",
                "field": "custom_field_14",
                "value": "",
                "required": "0",
                "sort": "0",
                "linkage_rules": ""
            }
        },
        {
            "WorkitemTemplateField": {
                "id": "1010104801016243919",
                "workspace_id": "10104801",
                "type": "story",
                "template_id": "1010104801000850579",
                "field": "begin",
                "value": "",
                "required": "0",
                "sort": "0",
                "linkage_rules": "",
                "default_value": ""
            }
        },
        {
            "WorkitemTemplateField": {
                "id": "1010104801016243921",
                "workspace_id": "10104801",
                "type": "story",
                "template_id": "1010104801000850579",
                "field": "due",
                "value": "",
                "required": "0",
                "sort": "0",
                "linkage_rules": "",
                "default_value": ""
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
|field|字段名称|
|value|默认值|
|required|是否必填|
|sort|计数|
| linkage_rules | 配置显示规则 |
| default_value | 默认值 |
