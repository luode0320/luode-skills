# 说明
返回符合查询条件的所有测试用例（分页显示，默认一页30条）


# url
`${TAPD_API_ENDPOINT}/tcases`

# 支持格式
JSON/XML（默认JSON格式）

# HTTP请求方式
GET

# 请求数限制
默认返回 30 条。可通过传 limit 参数设置，最大取 200。也可以传 page 参数翻页


# 调用示例及返回结果
## 获取项目下测试用例
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password'  '${TAPD_API_ENDPOINT}/tcases?workspace_id=10158231'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN'  '${TAPD_API_ENDPOINT}/tcases?workspace_id=10158231'`

### 返回结果
```JSON
{
    "status": 1,
    "data": [
        {
            "Tcase": {
                "id": "1120003271001000049",
                "steps": null,
                "workspace_id": "10158231",
                "category_id": "-1",
                "created": "2019-06-26 16:42:59",
                "modifier": "api_doc_oauth",
                "modified": "2019-06-26 16:43:00",
                "creator": "",
                "status": "abandon",
                "name": "",
                "precondition": null,
                "expectation": null,
                "type": "",
                "priority": "",
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
                "custom_field_21": null,
                "custom_field_22": null,
                "custom_field_23": null,
                "custom_field_24": null,
                "custom_field_25": null,
                "custom_field_26": null,
                "custom_field_27": null,
                "custom_field_28": null,
                "custom_field_29": null,
                "custom_field_30": null,
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
        {
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
        }
    ],
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
