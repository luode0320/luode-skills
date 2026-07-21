# 说明
新建测试用例，返回新建测试用例的数据


# url
`${TAPD_API_ENDPOINT}/tcases`

# 支持格式
JSON/XML（默认JSON格式）

#  HTTP请求方式
POST

# 请求数限制
一次插入一条数据

# 请求参数
|字段名|必选|类型及范围|说明|
|:----:|:----:|:----:|:----:|
| id | 否 | integer | id |
| steps | 否 | string | 用例步骤 |
| workspace_id | `是` | integer | 项目ID |
| category_id | 否 | integer | 用例目录 |
| status | 否 | enum('updating','abandon','normal') | 用例状态 |
| name | `是` | string | 用例名称 |
| precondition | 否 | string | 前置条件 |
| expectation | 否 | string | 预期结果 |
| type | 否 | string | 用例类型 |
| priority | 否 | string | 用例等级 |
| creator | 否 | string | 创建人 |
| cus_{$自定义字段别名} | 否 | string | 自定义字段值，参数名会由后台自动转义为custom_field_*，如：cus_自定义字段的名称 |
| custom_field_* | 否 | string或者integer | 自定义字段参数，具体字段名通过接口 [获取测试用例自定义字段配置](/api-doc/API文档/api_reference/tcase/get_tcase_custom_fields_settings.html) 获取 |

# 调用示例及返回结果
## 创建个简单的测试用例
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password' -d 'name=简单用例&workspace_id=10158231&cus_自定义字段的名称=custom_field_value' '${TAPD_API_ENDPOINT}/tcases'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN' -d 'name=简单用例&workspace_id=10158231&cus_自定义字段的名称=custom_field_value' '${TAPD_API_ENDPOINT}/tcases'`

### 返回结果
```JSON
{
    "status": 1,
    "data": {
        "Tcase": {
            "id": "1010158231077224795",
            "steps": null,
            "workspace_id": "10158231",
            "category_id": "-1",
            "created": "2019-06-26 16:42:58",
            "modifier": "api_doc_oauth",
            "modified": "2019-06-26 16:42:58",
            "creator": "api_doc_oauth",
            "status": "normal",
            "name": "简单用例",
            "precondition": null,
            "expectation": null,
            "type": "",
            "priority": "",
            "cus_自定义字段的名称": "custom_field_value",
            "custom_field_1": null,
            "custom_field_2": null,
            "custom_field_3": null,
            "custom_field_4": null,
            "custom_field_5": null,
            "custom_field_6": null,
            "custom_field_7": null,
            "custom_field_8": null,
            "custom_field_9": null,
            "custom_field_10": null,
            "custom_field_11": null,
            "custom_field_12": null,
            "custom_field_13": null,
            "custom_field_14": null,
            "custom_field_15": null,
            "custom_field_16": null,
            "custom_field_17": null,
            "custom_field_18": null,
            "custom_field_19": null,
            "custom_field_20": null,
            "custom_field_21": "",
            "custom_field_22": "",
            "custom_field_23": "",
            "custom_field_24": "",
            "custom_field_25": "",
            "custom_field_26": "",
            "custom_field_27": "",
            "custom_field_28": "",
            "custom_field_29": "",
            "custom_field_30": "",
            "custom_field_31": null,
            "custom_field_32": null,
            "custom_field_33": null,
            "custom_field_34": null,
            "custom_field_35": null,
            "custom_field_36": null,
            "custom_field_37": null,
            "custom_field_38": null,
            "custom_field_39": null,
            "custom_field_40": null,
            "custom_field_41": null,
            "custom_field_42": null,
            "custom_field_43": null,
            "custom_field_44": null,
            "custom_field_45": null,
            "custom_field_46": null,
            "custom_field_47": null,
            "custom_field_48": null,
            "custom_field_49": null,
            "custom_field_50": null
        }
    },
    "info": "success"
}
```## 创建个稍微复杂的测试用例
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password' -d 'type=其它&priority=高&status=待更新&steps=第一二三步&precondition=打开浏览器&expectation=无样式错误&creator=tapd&name=测试浏览器兼容性&workspace_id=10158231&cus_自定义字段的名称=custom_field_value' '${TAPD_API_ENDPOINT}/tcases'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN' -d 'type=其它&priority=高&status=待更新&steps=第一二三步&precondition=打开浏览器&expectation=无样式错误&creator=tapd&name=测试浏览器兼容性&workspace_id=10158231&cus_自定义字段的名称=custom_field_value' '${TAPD_API_ENDPOINT}/tcases'`

### 返回结果
```JSON
{
    "status": 1,
    "data": {
        "Tcase": {
            "id": "1010158231077224799",
            "steps": "第一二三步",
            "workspace_id": "10158231",
            "category_id": "-1",
            "created": "2019-06-26 16:42:59",
            "modifier": "tapd",
            "modified": "2019-06-26 16:42:59",
            "creator": "tapd",
            "status": "",
            "name": "测试浏览器兼容性",
            "precondition": "打开浏览器",
            "expectation": "无样式错误",
            "type": "其它",
            "priority": "高",
            "cus_自定义字段的名称": "custom_field_value",
            "custom_field_1": null,
            "custom_field_2": null,
            "custom_field_3": null,
            "custom_field_4": null,
            "custom_field_5": null,
            "custom_field_6": null,
            "custom_field_7": null,
            "custom_field_8": null,
            "custom_field_9": null,
            "custom_field_10": null,
            "custom_field_11": null,
            "custom_field_12": null,
            "custom_field_13": null,
            "custom_field_14": null,
            "custom_field_15": null,
            "custom_field_16": null,
            "custom_field_17": null,
            "custom_field_18": null,
            "custom_field_19": null,
            "custom_field_20": null,
            "custom_field_21": "",
            "custom_field_22": "",
            "custom_field_23": "",
            "custom_field_24": "",
            "custom_field_25": "",
            "custom_field_26": "",
            "custom_field_27": "",
            "custom_field_28": "",
            "custom_field_29": "",
            "custom_field_30": "",
            "custom_field_31": null,
            "custom_field_32": null,
            "custom_field_33": null,
            "custom_field_34": null,
            "custom_field_35": null,
            "custom_field_36": null,
            "custom_field_37": null,
            "custom_field_38": null,
            "custom_field_39": null,
            "custom_field_40": null,
            "custom_field_41": null,
            "custom_field_42": null,
            "custom_field_43": null,
            "custom_field_44": null,
            "custom_field_45": null,
            "custom_field_46": null,
            "custom_field_47": null,
            "custom_field_48": null,
            "custom_field_49": null,
            "custom_field_50": null
        }
    },
    "info": "success"
}
```

# 测试用例字段说明
## 测试用例重要字段说明
|字段|说明|
|:----:|:----:|
| id | id |
| steps | 用例步骤 |
| workspace_id | 项目ID |
| category_id | 用例目录 |
| created | 创建时间 |
| modifier | 最后修改人 |
| modified | 最后修改时间 |
| creator | 创建人 |
| status | 用例状态 |
| name | 用例名称 |
| precondition | 前置条件 |
| expectation | 预期结果 |
| type | 用例类型 |
| priority | 用例等级 |

## 测试用例类型(type)取值字段说明
|取值|字面值|
|:----:|:----:|
| 功能测试 | 功能测试 |
| 性能测试 | 性能测试 |
| 安全性测试 | 安全性测试 |
| 其他 | 其他 |

## 测试用例等级(priority)取值字段说明
|取值|字面值|
|:----:|:----:|
| 高 | 高 |
| 中 | 中 |
| 低 | 低 |

## 测试用例状态(status)取值字段说明
|取值|字面值|
|:----:|:----:|
| normal | 正常 |
| updating | 待更新 |
| abandon | 已废弃 |
