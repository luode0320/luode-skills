# 说明
计算符合查询条件的需求数量并返回


# url
`${TAPD_API_ENDPOINT}/stories/count`

# 支持格式
JSON/XML（默认JSON格式）

#  HTTP请求方式
GET

# 请求数限制
只返回需求数量

# 请求参数
|字段名|必选|类型及范围|说明|特殊规则|
|:----:|:----:|:----:|:----:|:----:|
| id | 否 | integer | ID | 支持多ID查询 |
| name | 否 | string | 标题 | 支持模糊匹配 |
| priority | 否 | string | 优先级。为了兼容自定义优先级，`请使用 priority_label 字段`，详情参考：[如何兼容自定义优先级](/api-doc/API文档/subject/custom_priority/) |
| priority_label | 否 | string | 优先级。推荐使用这个字段 |
| business_value | 否 | integer | 业务价值 |  |
| status | 否 | string | 状态 | 支持枚举查询 |
| v_status | 否 | string | 状态(支持传入中文状态名称) ||
| with_v_status | 否 | string | 值=1可以返回中文状态 ||
| label | 否 | string | 标签查询 | 支持枚举查询  |
| workitem_type_id | 否 | string | 需求类别ID | 支持枚举查询 |
| version | 否 | string | 版本 |  |
| module | 否 | string | 模块 |  |
| feature | 否 | string | 特性 |  |
| test_focus | 否 | string | 测试重点 |  |
| size | 否 | integer | 规模 |  |
| tech_risk | 否 | string | 技术风险 |  |
| business_value | 否 | string | 业务价值 |  |
| owner | 否 | string | 处理人 | 支持模糊匹配 |
| cc | 否 | string | 抄送人 | 支持模糊匹配 |
| creator | 否 | string | 创建人 | 支持多人员查询 |
| developer | 否 | string | 开发人员 |  |
| begin | 否 | date | 预计开始 | 支持时间查询 |
| due | 否 | date | 预计结束 | 支持时间查询 |
| created | 否 | datetime | 创建时间 | 支持时间查询 |
| modified | 否 | datetime | 最后修改时间 | 支持时间查询 |
| completed | 否 | datetime | 完成时间 | 支持时间查询 |
| iteration_id | 否 | string | 迭代ID | 支持不等于查询或枚举查询 |
| effort | 否 | string | 预估工时 |  |
| effort_completed | 否 | string | 完成工时 |  |
| remain | 否 | float | 剩余工时 |  |
| exceed | 否 | float | 超出工时 |  |
| category_id | 否 | integer | 需求分类 | 支持枚举查询 |
| release_id | 否 | integer | 发布计划 |  |
| source | 否 | string | 需求来源 |  |
| type | 否 | string | 需求类型 |  |
| ancestor_id | 否 | integer | 祖先需求，查询指定需求下所有子需求 |  |
| parent_id | 否 | integer | 父需求 |  |
| children_id | 否 | string | 子需求 | 为空查询传：丨 |
| description | 否 | string | 详细描述 | 支持模糊匹配 |
| workspace_id | `是` | integer | 项目ID |  |
| custom_field_* | 否 | string或者integer | 自定义字段参数，具体字段名通过接口 [获取需求自定义字段配置](/api-doc/API文档/api_reference/story/get_story_custom_fields_settings.html) 获取 | 支持枚举查询 |
| custom_plan_field_* | 否 | string或者integer | 自定义计划应用参数，具体字段名通过接口 [获取自定义计划应用](/api-doc/API文档/api_reference/iteration/get_plan_apps.html) 获取 |  |
| include_sub_category | 否 | string | 是否包含子分类 | 取值 0或者1，默认取 0 |
| include_sub_iteration | 否 | string | 是否包含子迭代 | 取值 0或者1，默认取 0 |
| include_leaf_stories | 否 | string | 是否包含子需求 | 取值 0或者1，默认取 0 |
| limit | 否 | integer | 设置返回数量限制，默认为30 | |
| page | 否 | integer | 返回当前数量限制下第N页的数据，默认为1（第一页）| |
| order | 否 | string | 排序规则，规则：字段名 ASC或者DESC，然后 urlencode |  如按创建时间逆序：order=created%20desc |
| fields | 否 | string | 设置获取的字段，多个字段间以','逗号隔开 | |

# 调用示例及返回结果
## 获取项目下需求的数量
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password'  '${TAPD_API_ENDPOINT}/stories/count?workspace_id=10158231'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN'  '${TAPD_API_ENDPOINT}/stories/count?workspace_id=10158231'`

### 返回结果
```JSON
{
    "status": 1,
    "data": {
        "count": 7
    },
    "info": "success"
}
```
## 获取项目下优先级为 High 需求的数量
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password'  '${TAPD_API_ENDPOINT}/stories/count?workspace_id=10158231&priority=4'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN'  '${TAPD_API_ENDPOINT}/stories/count?workspace_id=10158231&priority=4'`

### 返回结果
```JSON
{
    "status": 1,
    "data": {
        "count": 4
    },
    "info": "success"
}
```
