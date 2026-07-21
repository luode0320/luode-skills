# 说明
返回符合查询条件的所有缺陷（分页显示，默认一页30条）


# url
`${TAPD_API_ENDPOINT}/bugs`

# 支持格式
JSON/XML（默认JSON格式）

# HTTP请求方式
GET

# 请求数限制
默认返回 30 条。可通过传 limit 参数设置，最大取 200。也可以传 page 参数翻页

# 请求参数
|字段名|必选|类型及范围|说明|特殊规则|
|:----:|:----:|:----:|:----:|:----:|
| id | 否 | integer | ID | 支持多ID查询 |
| title | 否 | string | 标题 | 支持模糊匹配 |
| priority | 否 | string | 优先级。为了兼容自定义优先级，`请使用 priority_label 字段`，详情参考：[如何兼容自定义优先级](/api-doc/API文档/subject/custom_priority/) |
| priority_label | 否 | string | 优先级。推荐使用这个字段 |
| severity | 否 | string | 严重程度 | 支持枚举查询 |
| status | 否 | string | 状态 | 支持不等于查询、枚举查询 |
| v_status | 否 | string | 状态(支持传入中文状态名称) ||
| label | 否 | string | 标签查询 | 支持枚举查询  |
| iteration_id | 否 | string | 迭代 | 支持枚举查询 |
| module | 否 | string | 模块 | 支持枚举查询 |
| release_id | 否 | integer | 发布计划 |  |
| version_report | 否 | string | 发现版本 | 枚举查询 |
| version_test | 否 | string | 验证版本 |  |
| version_fix | 否 | string | 合入版本 |  |
| version_close | 否 | string | 关闭版本 |  |
| baseline_find | 否 | string | 发现基线 |  |
| baseline_join | 否 | string | 合入基线 |  |
| baseline_test | 否 | string | 验证基线  |  |
| baseline_close | 否 | string | 关闭基线 |  |
| feature | 否 | string | 特性 |  |
| current_owner | 否 | string | 处理人 | 支持模糊匹配 |
| cc | 否 | string | 抄送人 |  |
| reporter | 否 | string | 创建人 | 支持多人员查询 |
| participator | 否 | string | 参与人 | 支持多人员查询 |
| te | 否 | string | 测试人员 | 支持模糊匹配 |
| de | 否 | string | 开发人员 | 支持模糊匹配 |
| auditer | 否 | string | 审核人 |  |
| confirmer | 否 | string | 验证人 |  |
| fixer | 否 | string | 修复人 |  |
| closer | 否 | string | 关闭人 |  |
| lastmodify | 否 | string | 最后修改人 |  |
| created | 否 | datetime | 创建时间 | 支持时间查询 |
| in_progress_time | 否 | datetime | 接受处理时间  | 支持时间查询 |
| resolved | 否 | datetime | 解决时间 | 支持时间查询 |
| verify_time | 否 | datetime | 验证时间 | 支持时间查询 |
| closed | 否 | datetime | 关闭时间 | 支持时间查询 |
| reject_time | 否 | datetime | 拒绝时间 | 支持时间查询 |
| modified | 否 | datetime | 最后修改时间 | 支持时间查询 |
| begin | 否 | date | 预计开始 |  |
| due | 否 | date | 预计结束 |  |
| deadline | 否 | date | 解决期限 |  |
| os | 否 | string | 操作系统 |  |
| size | 否 | string | 规模 |  |
| platform | 否 | string | 软件平台 |  |
| testmode | 否 | string | 测试方式 |  |
| testphase | 否 | string | 测试阶段 |  |
| testtype | 否 | string | 测试类型 |  |
| source | 否 | string | 缺陷根源 | 支持枚举查询 |
| bugtype | 否 | string | 缺陷类型 |  |
| frequency | 否 | string | 重现规律 | 支持枚举查询 |
| originphase | 否 | string | 发现阶段 |  |
| sourcephase | 否 | string | 引入阶段   |  |
| resolution | 否 | string | 解决方法 | 支持枚举查询 |
| estimate | 否 | integer | 预计解决时间 |  |
| description | 否 | string | 详细描述 | 支持模糊匹配 |
| workspace_id | `是` | integer | 项目ID |  |
| custom_field_* | 否 | string或者integer | 自定义字段参数，具体字段名通过接口 [获取缺陷自定义字段配置](/api-doc/API文档/api_reference/bug/get_bug_custom_fields_settings.html) 获取 | 支持枚举查询 |
| custom_plan_field_* | 否 | string或者integer | 自定义计划应用参数，具体字段名通过接口 [获取自定义计划应用](/api-doc/API文档/api_reference/iteration/get_plan_apps.html) 获取 |  |
| limit | 否 | integer | 设置返回数量限制，默认为30 | |
| page | 否 | integer | 返回当前数量限制下第N页的数据，默认为1（第一页）| |
| order | 否 | string | 排序规则，规则：字段名 ASC或者DESC，然后 urlencode |  如按创建时间逆序：order=created%20desc |
| fields | 否 | string | 设置获取的字段，多个字段间以','逗号隔开 | |

# 调用示例及返回结果
## 获取项目下的缺陷数据
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password'  '${TAPD_API_ENDPOINT}/bugs?workspace_id=10158231&limit=2'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN'  '${TAPD_API_ENDPOINT}/bugs?workspace_id=10158231&limit=2'`

### 返回结果
```JSON
{
    "status": 1,
    "data": [
        {
            "Bug": {
                "id": "1010158231500628817",
                "title": "【示例】新官网Chrome浏览器兼容性bug",
                "description": null,
                "priority": "high",
                "severity": "prompt",
                "module": null,
                "status": "in_progress",
                "reporter": "anyechen",
                "deadline": null,
                "created": "2017-06-20 16:49:19",
                "bugtype": "",
                "resolved": null,
                "closed": null,
                "modified": "2018-01-12 14:45:27",
                "lastmodify": "anyechen",
                "auditer": null,
                "de": null,
                "fixer": null,
                "version_test": "",
                "version_report": "版本1",
                "version_close": "",
                "version_fix": "",
                "baseline_find": "",
                "baseline_join": "",
                "baseline_close": "",
                "baseline_test": "",
                "sourcephase": "",
                "te": null,
                "current_owner": null,
                "iteration_id": "0",
                "resolution": "",
                "source": "",
                "originphase": "",
                "confirmer": null,
                "milestone": null,
                "participator": null,
                "closer": null,
                "platform": "",
                "os": "",
                "testtype": "",
                "testphase": "",
                "frequency": "",
                "cc": null,
                "regression_number": "0",
                "flows": "new",
                "feature": null,
                "testmode": "",
                "estimate": null,
                "issue_id": null,
                "created_from": null,
                "in_progress_time": null,
                "verify_time": null,
                "reject_time": null,
                "reopen_time": null,
                "audit_time": null,
                "suspend_time": null,
                "due": null,
                "begin": null,
                "release_id": null,
				"label": "阻塞|重点关注",
                "custom_field_one": "",
                "custom_field_two": "",
                "custom_field_three": "",
                "custom_field_four": "",
                "custom_field_five": "",
                "custom_field_6": "",
                "custom_field_7": "",
                "custom_field_8": "",
                "custom_field_9": "",
                "custom_field_10": "",
                "custom_field_11": "",
                "custom_field_12": "",
                "custom_field_13": "",
                "custom_field_14": "",
                "custom_field_15": "",
                "custom_field_16": "",
                "custom_field_17": "",
                "custom_field_18": "",
                "custom_field_19": "",
                "custom_field_20": "",
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
                "custom_field_31": "",
                "custom_field_32": "",
                "custom_field_33": "",
                "custom_field_34": "",
                "custom_field_35": "",
                "custom_field_36": "",
                "custom_field_37": "",
                "custom_field_38": "",
                "custom_field_39": "",
                "custom_field_40": "",
                "custom_field_41": "",
                "custom_field_42": "",
                "custom_field_43": "",
                "custom_field_44": "",
                "custom_field_45": "",
                "custom_field_46": "",
                "custom_field_47": "",
                "custom_field_48": "",
                "custom_field_49": "",
                "custom_field_50": "",
                "workspace_id": "10158231"
            }
        },
        {
            "Bug": {
                "id": "1010158231500628815",
                "title": "【示例】新官网页面宽度自适应bug",
                "description": null,
                "priority": "medium",
                "severity": "normal",
                "module": null,
                "status": "new",
                "reporter": "anyechen",
                "deadline": null,
                "created": "2017-06-20 16:49:19",
                "bugtype": "",
                "resolved": null,
                "closed": null,
                "modified": "2017-06-20 16:49:19",
                "lastmodify": "ruirayli",
                "auditer": null,
                "de": null,
                "fixer": null,
                "version_test": "",
                "version_report": "版本1",
                "version_close": "",
                "version_fix": "",
                "baseline_find": "",
                "baseline_join": "",
                "baseline_close": "",
                "baseline_test": "",
                "sourcephase": "",
                "te": null,
                "current_owner": null,
                "iteration_id": "0",
                "resolution": "",
                "source": "",
                "originphase": "",
                "confirmer": null,
                "milestone": null,
                "participator": null,
                "closer": null,
                "platform": "",
                "os": "",
                "testtype": "",
                "testphase": "",
                "frequency": "",
                "cc": null,
                "regression_number": "0",
                "flows": "new",
                "feature": null,
                "testmode": "",
                "estimate": null,
                "issue_id": null,
                "created_from": null,
                "in_progress_time": null,
                "verify_time": null,
                "reject_time": null,
                "reopen_time": null,
                "audit_time": null,
                "suspend_time": null,
                "due": null,
                "begin": null,
                "release_id": null,
                "custom_field_one": "",
                "custom_field_two": "",
                "custom_field_three": "",
                "custom_field_four": "",
                "custom_field_five": "",
                "custom_field_6": "",
                "custom_field_7": "",
                "custom_field_8": "",
                "custom_field_9": "",
                "custom_field_10": "",
                "custom_field_11": "",
                "custom_field_12": "",
                "custom_field_13": "",
                "custom_field_14": "",
                "custom_field_15": "",
                "custom_field_16": "",
                "custom_field_17": "",
                "custom_field_18": "",
                "custom_field_19": "",
                "custom_field_20": "",
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
                "custom_field_31": "",
                "custom_field_32": "",
                "custom_field_33": "",
                "custom_field_34": "",
                "custom_field_35": "",
                "custom_field_36": "",
                "custom_field_37": "",
                "custom_field_38": "",
                "custom_field_39": "",
                "custom_field_40": "",
                "custom_field_41": "",
                "custom_field_42": "",
                "custom_field_43": "",
                "custom_field_44": "",
                "custom_field_45": "",
                "custom_field_46": "",
                "custom_field_47": "",
                "custom_field_48": "",
                "custom_field_49": "",
                "custom_field_50": "",
                "workspace_id": "10158231"
            }
        }
    ],
    "info": "success"
}
```

# 缺陷字段说明
缺陷字段说明，请参考 [缺陷说明](/api-doc/API文档/api_reference/bug/bug.html)
