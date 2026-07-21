# 说明
返回缺陷所有字段及候选值


# url
`${TAPD_API_ENDPOINT}/test_plans/get_fields_info`

# 支持格式
JSON/XML（默认JSON格式）

# HTTP请求方式
GET

# 请求数限制
默认返回所有数据

# 请求参数
|字段名|必选|类型及范围|说明|特殊规则|
|:----:|:----:|:----:|:----:|:----:|
| workspace_id | `是` | integer | 项目ID |  |

# 调用示例及返回结果
## 获取项目下的测试计划字段
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password'  '${TAPD_API_ENDPOINT}/test_plans/get_fields_info?workspace_id=10104801'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN'  '${TAPD_API_ENDPOINT}/test_plans/get_fields_info?workspace_id=10104801'`

### 返回结果
```JSON
{
    "status": 1,
    "data": {
        "id": {
            "html_type": "input",
            "options": [],
            "label": "ID"
        },
        "name": {
            "html_type": "input",
            "options": [],
            "label": "计划名称"
        },
        "description": {
            "html_type": "textarea",
            "options": [],
            "label": "测试描述"
        },
        "version": {
            "html_type": "select",
            "options": [],
            "label": "版本"
        },
        "owner": {
            "html_type": "user_chooser",
            "options": [],
            "label": "测试负责人"
        },
        "status": {
            "html_type": "select",
            "options": {
                "open": "开启",
                "close": "关闭"
            },
            "label": "状态"
        },
        "type": {
            "html_type": "select",
            "options": {
                "功能测试": "功能测试",
                "性能测试": "性能测试",
                "安全性测试": "安全性测试",
                "其他": "其他"
            },
            "label": "测试类型"
        },
        "start_date": {
            "html_type": "dateinput",
            "options": [],
            "label": "开始时间"
        },
        "end_date": {
            "html_type": "dateinput",
            "options": [],
            "label": "结束时间"
        },
        "creator": {
            "html_type": "user_chooser",
            "options": [],
            "label": "创建人"
        },
        "modifier": {
            "html_type": "user_chooser",
            "options": [],
            "label": "最后修改人"
        },
        "created": {
            "html_type": "dateinput",
            "options": [],
            "label": "创建时间"
        },
        "modified": {
            "html_type": "dateinput",
            "options": [],
            "label": "最后修改时间"
        },
        "iteration_id": {
            "html_type": "select",
            "options": {
                "1010104801001343229": "iterations",
                "1010104801001248517": "adra",
                "1010104801001179909": "aaaassssss",
                "1010104801001179887": "cjdd",
                "1010104801001171067": "oyctest20190911xxx1111",
                "1010104801001169803": "oyctest20190911xxx1111",
                "1010104801001123207": "oyctest20190911",
                "1010104801001112221": "myI",
                "1010104801001105965": "oyctest20190911xxx1111",
                "1010104801001105193": "oyctest20190911xxx1111",
                "1010104801001103985": "对对对",
                "1010104801001082017": "日常发布",
                "1010104801001082013": "日常发布",
                "1010104801001081899": "oyctest20190917ABC2",
                "1010104801001080913": "【Word】191001常规发布",
                "1010104801001080783": "日常发布",
                "1010104801000648821": "ssss",
                "1010104801000507689": "i1",
                "1010104801000423181": "迭代1"
            },
            "label": "迭代"
        },
        "custom_field_1": {
            "html_type": "text",
            "options": [],
            "label": "输入框"
        }
    },
    "info": "success"
}
```
# 返回字段说明
| 字段 | 说明 |
|:----:|:----:|
| name | name |
| options | 候选值 |
| html_type | 类型 |
| label | 中文名称 |
