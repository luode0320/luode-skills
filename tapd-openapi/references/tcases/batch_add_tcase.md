# 说明
批量新建测试用例，返回新建测试用例的数据


# url
`${TAPD_API_ENDPOINT}/tcases/batch_save`

# 支持格式
JSON/XML（默认JSON格式）

#  HTTP请求方式
POST

# 请求数限制
每次新增最大为两百

# 请求参数
测试用例列表
|字段名|必选|类型及范围|说明|
|:----:|:----:|:----:|:----:|
| workspace_id | `是` | integer | 项目ID |
| name | `是` | string | 用例名称 |
| steps | 否 | string | 用例步骤 |
| category_id | 否 | integer | 用例目录 |
| status | 否 | 取值 updating, abandon, normal | 用例状态 |
| precondition | 否 | string | 前置条件 |
| expectation | 否 | string | 预期结果 |
| type | 否 | string | 用例类型 |
| priority | 否 | string | 用例等级 |
| creator | 否 | string | 创建人 |
| custom_field_* | 否 | string或者integer | 自定义字段参数，具体字段名通过接口 {{custom_field_url}} 获取 |

# 调用示例及返回结果
### 请求参数示例
```JSON
[
    {
        "workspace_id": "69992160",
        "category_id": "-1",
        "status": "normal",
        "name": "简单用例1",
        "creator":"XX1"
    },
    {
        "steps": null,
        "workspace_id": "69992160",
        "category_id": "-1",
        "status": "normal",
        "name": "简单用例2",
        "creator":"XX2"
    }
]
```
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password' -d '[{"workspace_id": "69992160",  "name": "简单用例1","creator":"XX1"}, {"workspace_id": "69992160",  "name": "简单用例2","creator":"XX2"}]' '${TAPD_API_ENDPOINT}/tcases/batch_save'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN' -d '[{"workspace_id": "69992160",  "name": "简单用例1","creator":"XX1"}, {"workspace_id": "69992160",  "name": "简单用例2","creator":"XX2"}]' '${TAPD_API_ENDPOINT}/tcases/batch_save'`

### 返回结果
```JSON
{
    "status": 1,
    "data": [
        {
            "Tcase": {
                "id": "1069992160077456793",
                "mid": "1069992160077456793",
                "steps": null,
                "workspace_id": "69992160",
                "category_id": "-1",
                "version": "0",
                "created": "2023-07-10 16:30:06",
                "modifier": "XX1",
                "modified": "2023-07-10 16:30:06",
                "creator": "XX1",
                "status": "normal",
                "name": "简单用例1",
                "precondition": null,
                "expectation": null,
                "sort": "0",
                "indexcode": "",
                "type": "",
                "priority": "",
                "is_automated": "0",
                "automation_type": "",
                "automation_platform": "",
                "is_serving": "0",
                "template_id": "0",
                "created_from": "",
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
        {
            "Tcase": {
                "id": "1069992160077456795",
                "mid": "1069992160077456795",
                "steps": null,
                "workspace_id": "69992160",
                "category_id": "-1",
                "version": "0",
                "created": "2023-07-10 16:30:06",
                "modifier": "XX2",
                "modified": "2023-07-10 16:30:06",
                "creator": "XX2",
                "status": "normal",
                "name": "简单用例2",
                "precondition": null,
                "expectation": null,
                "sort": "0",
                "indexcode": "",
                "type": "",
                "priority": "",
                "is_automated": "0",
                "automation_type": "",
                "automation_platform": "",
                "is_serving": "0",
                "template_id": "0",
                "created_from": "",
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
