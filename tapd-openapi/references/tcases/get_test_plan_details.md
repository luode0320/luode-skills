# 说明
获取测试计划测试结果


# url
`${TAPD_API_ENDPOINT}/test_plans/details`

# 支持格式
JSON/XML（默认JSON格式）

#  HTTP请求方式
GET

# 请求数限制
默认返回所有数据。


# 请求参数
|字段名|必选|类型及范围|说明|
|:----:|:----:|:----:|:----:|
| workspace_id | `是` | integer | 项目ID |
|id|`是`|integer|测试计划ID|
| last_executor |否|string|最后执行人|
| include_repeat | 否 | integer | include_repeat=1 可以获取到所有数据 |


# 调用示例及返回结果
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password' '${TAPD_API_ENDPOINT}/test_plans/details?workspace_id=10158231&id=1010158231000005241'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN' '${TAPD_API_ENDPOINT}/test_plans/details?workspace_id=10158231&id=1010158231000005241'`

### 返回结果
```JSON

{
	"status": 1,
	"data": [{
		"Tcase": {
			"id": "1010158231075919347",
			"mid": "1010158231075919347",
			"steps": null,
			"workspace_id": "10158231",
			"category_id": "-1",
			"version": "0",
			"created": "2017-06-20 16:49:29",
			"modifier": "anyechen",
			"modified": "2017-06-20 16:49:29",
			"creator": "anyechen",
			"status": "normal",
			"name": "Firefox\u6d4f\u89c8\u5668\u517c\u5bb9\u6027\u6d4b\u8bd5",
			"precondition": null,
			"expectation": null,
			"sort": "0",
			"indexcode": "",
			"type": "",
			"priority": "",
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
			"custom_field_50": null,
			"TcaseResult": {
				"id": 0,
				"tcase_id": 1010158231075919347,
				"created": "",
				"test_plan_id": 0,
				"result_status": "unexecuted",
				"result_remark": "",
				"workspace_id": 10158231,
				"status": "",
				"executor": "",
				"executed_at": ""
			}
		}
	}, {
		"Tcase": {
			"id": "1010158231075919345",
			"mid": "1010158231075919345",
			"steps": null,
			"workspace_id": "10158231",
			"category_id": "-1",
			"version": "0",
			"created": "2017-06-20 16:49:28",
			"modifier": "anyechen",
			"modified": "2017-06-20 16:49:29",
			"creator": "anyechen",
			"status": "normal",
			"name": "Chrome\u6d4f\u89c8\u5668\u517c\u5bb9\u6027\u6d4b\u8bd5",
			"precondition": null,
			"expectation": null,
			"sort": "0",
			"indexcode": "",
			"type": "",
			"priority": "",
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
			"custom_field_50": null,
			"TcaseResult": {
				"id": "1010158231000703323",
				"tcase_id": "1010158231077230667",
				"created": "2020-02-12 23:42:56",
				"test_plan_id": "1010158231000005241",
				"result_status": "block",
				"result_remark": "xxx",
				"workspace_id": "10158231",
				"status": "normal",
				"executor": "anyechen",
				"executed_at": "2020-02-12 23:42:56"
			}
		}
	}, {
		"Tcase": {
			"id": "1010158231075919341",
			"mid": "1010158231075919341",
			"steps": null,
			"workspace_id": "10158231",
			"category_id": "-1",
			"version": "0",
			"created": "2017-06-20 16:49:26",
			"modifier": "anyechen",
			"modified": "2017-06-20 16:49:26",
			"creator": "anyechen",
			"status": "normal",
			"name": "IE\u6d4f\u89c8\u5668\u517c\u5bb9\u6027\u6d4b\u8bd5",
			"precondition": null,
			"expectation": null,
			"sort": "0",
			"indexcode": "",
			"type": "",
			"priority": "",
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
			"custom_field_50": null,
			"TcaseResult": {
				"id": "1010158231000018041",
				"tcase_id": "1010158231075919343",
				"created": "2017-06-20 16:49:28",
				"test_plan_id": "1010158231000005241",
				"result_status": "pass",
				"result_remark": null,
				"workspace_id": "10158231",
				"status": "normal",
				"executor": "ruirayli",
				"executed_at": "2017-06-20 16:49:28"
			}
		}
	}],
	"info": "success"
}


```
# 测试字段说明
## 测试重要字段说明
|字段|说明|
|:----:|:----:|
| id |用例ID |
| steps | 用例步骤 |
| workspace_id | 项目ID |
| category_id | 用例目录 |
| created | 创建时间 |
| modifier | 最后修改人 |
| modified | 最后修改时间 |
| creator | 创建人 |
| version | 版本 |
| status | 用例状态 |
| name | 用例名称 |
| precondition | 前置条件 |
| expectation | 预期结果 |
| type | 用例类型 |
| priority | 用例等级 |

## 测试结果(TcaseResult)中字段说明
|取值|字面值|
|:----:|:----:|
|id|测试结果id|
|tcase_id|测试用例id|
|created|创建时间|
|test_plan_id|测试计划id|
|result_status|结果状态|
|result_remark|结果备注|
|status|状态|
|executor|最后执行人|
|executed_at|执行时间|

## 结果状态(result_status)取值字段说明
|取值|字面值|
|:----:|:----:|
|pass|通过|
|no_pass|不通过|
|block|阻塞|
|unexecuted|未执行|

## 用例状态(status)取值字段说明
|取值|字面值|
|:----:|:----:|
| normal | 正常|
| updating |待更新|
| abandon | 已废弃|
