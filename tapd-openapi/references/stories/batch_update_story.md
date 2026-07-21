# 说明
批量更新需求，返回需求更新后的数据


# url
`${TAPD_API_ENDPOINT}/stories/batch_update_story`

# 支持格式
JSON/XML（默认JSON格式）

#  HTTP请求方式
POST

# 请求数限制
每次最多允许批量更新五十条数据

# 请求参数
|字段名|必选|类型及范围|说明|
|:----:|:----:|:----:|:----:|
| workspace_id | `是` | integer | 项目ID |
| workitems | `是` | array | 要更新对象数组 （下面所有属性数组）|
| id | `是` | integer | ID |
| name | 否 | string | 标题 |
| priority | 否 | string | 优先级。为了兼容自定义优先级，`请使用 priority_label 字段`，详情参考：[如何兼容自定义优先级](/api-doc/API文档/subject/custom_priority/) |
| priority_label | 否 | string | 优先级。推荐使用这个字段 |
| business_value | 否 | integer | 业务价值 |
| status | 否 | string | 状态。需求当前使用并行工作流时，将按状态重置来更新节点，进行中节点变更参考[节点完成接口](/api-doc/API文档/api_reference/story/update_story_step_status.html)  |
| v_status | 否 | string | 状态(支持传入中文状态名称) |
| version | 否 | string | 版本 |
| module | 否 | string | 模块 |
| test_focus | 否 | string | 测试重点 |
| size | 否 | integer | 规模 |
| owner | 否 | string | 处理人 |
| current_user | 否 | string | 变更人 |
| cc | 否 | string | 抄送人 |
| developer | 否 | string | 开发人员 |
| begin | 否 | date | 预计开始 |
| due | 否 | date | 预计结束 |
| iteration_id | 否 | string | 迭代ID |
| effort | 否 | string | 预估工时 |
| effort_completed | 否 | string | 完成工时 |
| remain | 否 | float | 剩余工时 |
| exceed | 否 | float | 超出工时 |
| category_id | 否 | integer | 需求分类 |
| release_id | 否 | integer | 发布计划 |
| source | 否 | string | 来源 |
| type | 否 | string | 类型 |
| description | 否 | string | 详细描述 |
| is_auto_close_task | 否 | integer | 需求流转到结束状态时，是否自动关闭关联的任务。为 1 时会自动关闭；默认取 0，不关闭 |
| label | 否 | string |     标签，标签不存在时将自动创建，多个以英文坚线分格      |
| cus_{$自定义字段别名} | 否 | string |     自定义字段值，参数名会由后台自动转义为custom_field_*，如：cus_这是一个自定义字段的名称 |
| custom_field_* | 否 | string或者integer | 自定义字段参数，具体字段名通过接口 [获取需求自定义字段配置](/api-doc/API文档/api_reference/story/get_story_custom_fields_settings.html) 获取 |
| custom_plan_field_* | 否 | string或者integer | 自定义计划应用参数，具体字段名通过接口 [获取自定义计划应用](/api-doc/API文档/api_reference/iteration/get_plan_apps.html) 获取 |

# 调用示例及返回结果
## 更新需求 1010104801125341253 的优先级为高，处理人为 anyechen
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password' -d 'workspace_id=10158231&workitems=[{"id"=123123,"name"="测试“}]' '${TAPD_API_ENDPOINT}/stories/batch_update_story'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN' -d 'workspace_id=10158231&workitems=[{"id"=123123,"name"="测试“}]' '${TAPD_API_ENDPOINT}/stories/batch_update_story'`

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

# 需求字段说明
需求字段说明，请参考：[需求字段说明](/api-doc/API文档/api_reference/story/story.md)
