# 说明
创建/提交一个缺陷（bug）单到项目中.


# url
`${TAPD_API_ENDPOINT}/bugs`

# 支持格式
JSON/XML（默认JSON格式）

#  HTTP请求方式
POST

# 请求数限制
一次插入一条数据

# 请求参数
|字段名|必选|类型及范围|说明|
|:----:|:----:|:----:|:----:|
| workspace_id | `是` | integer | 项目ID |
| title | `是` | string | 缺陷标题 |
| priority | 否 | string | 优先级。为了兼容自定义优先级，`请使用 priority_label 字段`，详情参考：[如何兼容自定义优先级](/api-doc/API文档/subject/custom_priority/) |
| priority_label | 否 | string | 优先级。推荐使用这个字段 |
| severity | 否 | string | 严重程度 |
| module | 否 | string | 模块 |
| feature | 否 | string | 特性 |
| release_id | 否 | integer | 发布计划 |
| version_report | 否 | string | 发现版本 |
| version_test | 否 | string | 验证版本 |
| version_fix | 否 | string | 合入版本 |
| version_close | 否 | string | 关闭版本 |
| baseline_find | 否 | string | 发现基线 |
| baseline_join | 否 | string | 合入基线 |
| baseline_test | 否 | string | 验证基线  |
| baseline_close | 否 | string | 关闭基线 |
| current_owner | 否 | string | 处理人 |
| template_id | 否 | integer | 模板ID |
| cc | 否 | string | 抄送人 |
| reporter | 否 | string | 创建人 |
| participator | 否 | string | 参与人 |
| te | 否 | string | 测试人员 |
| de | 否 | string | 开发人员 |
| auditer | 否 | string | 审核人 |
| confirmer | 否 | string | 验证人 |
| fixer | 否 | string | 修复人 |
| closer | 否 | string | 关闭人 |
| lastmodify | 否 | string | 最后修改人 |
| in_progress_time | 否 | datetime | 接受处理时间  |
| verify_time | 否 | datetime | 验证时间 |
| reject_time | 否 | datetime | 拒绝时间 |
| begin | 否 | date | 预计开始 |
| due | 否 | date | 预计结束 |
| deadline | 否 | date | 解决期限 |
| iteration_id | 否 | string | 迭代ID |
| size | 否 | string | 规模 |
| os | 否 | string | 操作系统 |
| platform | 否 | string | 软件平台 |
| testmode | 否 | string | 测试方式 |
| testphase | 否 | string | 测试阶段 |
| testtype | 否 | string | 测试类型 |
| source | 否 | string | 缺陷根源 |
| bugtype | 否 | string | 缺陷类型 |
| frequency | 否 | string | 重现规律 |
| originphase | 否 | string | 发现阶段 |
| sourcephase | 否 | string | 引入阶段   |
| resolution | 否 | string | 解决方法 |
| estimate | 否 | integer | 预计解决时间 |
| description | 否 | string | 详细描述 |
| label | 否 | string |     标签，标签不存在时将自动创建，多个以英文坚线分格      |
| effort | 否 | integer | 预估工时 |
| is_apply_template_default_value | 否 | integer | 是否从模板继承默认值（传值=1继承模板默认值） |
| cus_{$自定义字段别名} | 否 | string |     缺陷自定义字段值，参数名会由后台自动转义为custom_field_*，如：cus_自定义字段的名称 |
| custom_field_* | 否 | string或者integer | 缺陷自定义字段参数，具体字段名通过接口 [获取缺陷自定义字段配置](/api-doc/API文档/api_reference/bug/get_bug_custom_fields_settings.html) 获取 |
| custom_plan_field_* | 否 | string或者integer | 自定义计划应用参数，具体字段名通过接口 [获取自定义计划应用](/api-doc/API文档/api_reference/iteration/get_plan_apps.html) 获取 |

# 调用示例及返回结果
## 在项目下创建缺陷
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password' -d 'title=bug_created_by_api&workspace_id=10158231&cus_自定义字段的名称=custom_field_value' '${TAPD_API_ENDPOINT}/bugs'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN' -d 'title=bug_created_by_api&workspace_id=10158231&cus_自定义字段的名称=custom_field_value' '${TAPD_API_ENDPOINT}/bugs'`

### 返回结果
```JSON
{
    "status": 1,
    "data": {
        "Bug": {
            "id": "1010158231500643487",
            "title": "bug_created_by_api",
            "description": null,
            "priority": "",
            "severity": "",
            "module": null,
            "status": "new",
            "reporter": "api_doc_oauth",
            "deadline": null,
            "created": "2019-06-27 14:19:47",
            "bugtype": "",
            "resolved": null,
            "closed": null,
            "modified": "2019-06-27 14:19:47",
            "lastmodify": "api_doc_oauth",
            "auditer": null,
            "de": null,
            "fixer": null,
            "version_test": "",
            "version_report": "",
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
            "created_from": "api",
            "in_progress_time": null,
            "verify_time": null,
            "reject_time": null,
            "reopen_time": null,
            "audit_time": null,
            "suspend_time": null,
            "due": null,
            "begin": null,
            "release_id": null,
	        "label": "阻塞|延期",
	        "effort": null,
            "effort_completed": "0",
            "exceed": "0",
            "remain": "0",
            "cus_自定义字段的名称": "custom_field_value",
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
    "info": "success"
}
```
## 在项目下创建一张带 tapd.cn logo 、优先级为高的缺陷
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password' -d 'title=tapd_logo&description=<img src="https://file.tapd.cn/img/tapd_logo_svg_fix_new.png"/>&priority=high&workspace_id=10158231' '${TAPD_API_ENDPOINT}/bugs'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN' -d 'title=tapd_logo&description=<img src="https://file.tapd.cn/img/tapd_logo_svg_fix_new.png"/>&priority=high&workspace_id=10158231' '${TAPD_API_ENDPOINT}/bugs'`

### 返回结果
```JSON
{
    "status": 1,
    "data": {
        "Bug": {
            "id": "1010158231500643491",
            "title": "tapd_logo",
            "description": "<img src=\"https:\/\/file.tapd.cn\/img\/tapd_logo_svg_fix_new.png\"  \/>",
            "priority": "high",
            "severity": "",
            "module": null,
            "status": "new",
            "reporter": "api_doc_oauth",
            "deadline": null,
            "created": "2019-06-27 14:19:48",
            "bugtype": "",
            "resolved": null,
            "closed": null,
            "modified": "2019-06-27 14:19:48",
            "lastmodify": "api_doc_oauth",
            "auditer": null,
            "de": null,
            "fixer": null,
            "version_test": "",
            "version_report": "",
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
            "created_from": "api",
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
    },
    "info": "success"
}
```

缺陷字段说明，请参考 [缺陷说明](/api-doc/API文档/api_reference/bug/bug.html)
