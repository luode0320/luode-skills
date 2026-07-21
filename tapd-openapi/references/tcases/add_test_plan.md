# 说明
新建测试计划，返回新建测试计划的数据


# url
`${TAPD_API_ENDPOINT}/test_plans`

# 支持格式
JSON/XML（默认JSON格式）

#  HTTP请求方式
POST

# 请求数限制
一次插入一条数据

# 请求参数
|字段名|必选|类型及范围|说明|
|:----:|:----:|:----:|:----:|
| name | `是` | string | 测试计划标题 |
| description | 否 | string | 测试计划详细描述 |
| workspace_id | `是` | integer | 项目ID |
| creator | 否 | string | 创建人 |
| modifier| 否 | string | 修改人 |
| owner | 否 | string | 测试计划负责人 |
| start_date| 否 | date | 预计开始 |
| end_date | 否 | date | 预计结束 |
| iteration_id | 否 | integer | 关联迭代的ID |
| version| 否 | string | 版本号 |
| type| 否 | float | 测试类型 |
| status | 否 | string | 状态，默认开启，值为open |
| cus_{$自定义字段别名} | 否 | string | 自定义字段值，参数名会由后台自动转义为custom_field_*，如：cus_自定义字段的名称 |
| custom_field_* | 否 | string或者integer | 自定义字段参数，具体字段名通过接口 [获取测试计划自定义字段配置](/api-doc/API文档/api_reference/tcase/get_test_plan_fields_info.html) 获取 |

# 调用示例及返回结果
## 在项目下创建测试计划
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password' -d 'name=test&workspace_id=10158231&cus_自定义字段的名称=custom_field_value' '${TAPD_API_ENDPOINT}/test_plans'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN' -d 'name=test&workspace_id=10158231&cus_自定义字段的名称=custom_field_value' '${TAPD_API_ENDPOINT}/test_plans'`

### 返回结果
```JSON

{
    "status": 1,
    "data": {
        "TestPlan": {
            "id": "1000000755000016443",
            "workspace_id": "755",
            "name": "test_plan_12",
            "description": "这不是一个测试",
            "version": "123456",
            "owner": "",
            "status": "open",
            "type": "",
            "start_date": null,
            "end_date": null,
            "creator": "dev",
            "created": "2020-01-09 21:11:52",
            "modified": "2020-01-09 21:11:52",
            "modifier": "dev",
            "created_from": "api",
            "cus_自定义字字段的名称": "custom_field_value",
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


## 任务状态(status)取值字段说明
|取值|字面值|
|:----:|:----:|
| open | 开启|
| close | 关闭|
