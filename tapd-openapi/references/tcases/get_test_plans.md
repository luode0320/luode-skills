# 说明
返回符合查询条件的所有测试计划（分页显示，默认一页30条）


# url
`${TAPD_API_ENDPOINT}/test_plans`

# 支持格式
JSON/XML（默认JSON格式）

#  HTTP请求方式
GET

# 请求数限制
默认返回 30 条。可通过传 limit 参数设置，最大取 200。也可以传 page 参数翻页

# 请求参数
|字段名|必选|类型及范围|说明|特殊规则|
|:----:|:----:|:----:|:----:|:----:|
| id | 否 | int | 测试计划ID ||
| name | 否 | string | 测试计划标题 ||
| description | 否 | string | 测试计划详细描述 ||
| workspace_id | `是` | integer | 项目ID ||
| creator | 否 | string | 创建人 ||
| created | 否 | date | 创建时间 ||
| modifier| 否 | string | 修改人 ||
| modified| 否 | date | 最后修改时间 ||
| owner | 否 | string | 测试计划负责人 ||
| start_date| 否 | date | 预计开始 ||
| end_date | 否 | date | 预计结束 ||
| version| 否 | string | 版本号 ||
| type| 否 | string | 测试类型 ||
| status | 否 | string | 状态，默认开启，值为open | |
| limit | 否 | integer | 设置返回数量限制，默认为30 | |
| page | 否 | integer | 返回当前数量限制下第N页的数据，默认为1（第一页）| |
| order | 否 | string | 排序规则，规则：字段名 ASC或者DESC，然后 urlencode |  如按创建时间逆序：order=created%20desc |
| fields | 否 | string | 设置获取的字段，多个字段间以','逗号隔开 | |

# 调用示例及返回结果
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password'  '${TAPD_API_ENDPOINT}/test_plans?workspace_id=10104801'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN' '${TAPD_API_ENDPOINT}/test_plans?workspace_id=10104801'`

### 返回结果
```JSON
{
    "status": 1,
    "data": [
        {
            "TestPlan": {
                "id": "1010104801000045351",
                "workspace_id": "10104801",
                "name": "aada",
                "description": "<div>adfa</div>",
                "version": "",
                "owner": "v_xuanfang;",
                "status": "open",
                "type": "",
                "start_date": null,
                "end_date": null,
                "creator": "anyechen",
                "created": "2020-01-09 12:12:37",
                "modified": "2020-08-21 10:58:08",
                "modifier": "v_xuanfang",
                "created_from": "",
                "custom_field_1": "",
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

# 测试计划字段说明
## 测试计划重要字段说明
|字段|说明|
|:----:|:----:|
| id | id |
| workspace_id | 项目ID |
| name | 标题 |
| description | 详细描述 |
| version | 版本 |
| owner | 处理人 |
| type | 类型 |
| startdate | 开始时间 |
| enddate | 结束时间 |
| creator | 结束时间 |
| created | 创建时间 |
| modified | 最后修改时间 |
| status | 状态 |

## 状态(status)取值字段说明
|取值|字面值|
|:----:|:----:|
| open | 开启|
| close | 关闭|
