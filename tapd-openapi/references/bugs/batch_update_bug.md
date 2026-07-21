# 说明
用于批量更新缺陷的字段 或者 流转缺陷状态，返回缺陷更新后的数据


# url
`${TAPD_API_ENDPOINT}/bugs/batch_update_bug`

# 支持格式
JSON/XML（默认JSON格式）

#  HTTP请求方式
POST

# 请求数限制
每次最多允许批量更新五十条数据

# 请求参数
|字段名|必选|类型及范围|说明|
|:----:|:----:|:----:|:----:|
| project_id | `是` | integer | 项目ID |
| workitems | `是` | array | 要更新对象数组 （下面所有属性数组）|
| id | `是` | integer | ID |
| title | 否 | string | 标题 |
| priority | 否 | string | 优先级。为了兼容自定义优先级，`请使用 priority_label 字段`，详情参考：[如何兼容自定义优先级](/api-doc/API文档/subject/custom_priority/) |
| priority_label | 否 | string | 优先级。推荐使用这个字段 |
| severity | 否 | string | 严重程度 |
| status | 否 | string | 状态 |
| v_status | 否 | string | 状态(支持传入中文状态名称) |
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
| cc | 否 | string | 抄送人 |
| reporter | 否 | string | 创建人 |
| current_user | 否 | string | 变更人 |
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
| os | 否 | string | 操作系统 |
| size | 否 | string | 规模 |
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
| keep_owner | 否 | integer | 是否保存处理人。取 1 则是保留 |
| cus_{$自定义字段别名} | 否 | string | 自定义字段值，参数名会由后台自动转义为custom_field_*，如：cus_自定义字段的名称 |
| custom_field_* | 否 | string或者integer | 自定义字段参数，具体字段名通过接口 [获取缺陷自定义字段配置](/api-doc/API文档/api_reference/bug/get_bug_custom_fields_settings.html) 获取 |
| custom_plan_field_* | 否 | string或者integer | 自定义计划应用参数，具体字段名通过接口 [获取自定义计划应用](/api-doc/API文档/api_reference/iteration/get_plan_apps.html) 获取 |

# 调用示例及返回结果
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password' -d 'project_id=10158231&workitems=[{"id"=123123,"name"="测试“}]' '${TAPD_API_ENDPOINT}/bugs/batch_update_bug'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN' -d 'project_id=10158231&workitems=[{"id"=123123,"name"="测试“}]' '${TAPD_API_ENDPOINT}/bugs/batch_update_bug'`

### 返回结果
```JSON
{
    "status": 1,
    "data": {
        "msg": "batch update success"
    },
    "info": "success"
}
```

# 缺陷字段说明
缺陷字段说明，请参考 [缺陷说明](/api-doc/API文档/api_reference/bug/bug.html)
