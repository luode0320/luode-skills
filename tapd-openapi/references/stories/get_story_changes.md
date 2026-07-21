## 说明
返回符合查询条件的所有需求变更历史（分页显示，默认一页30条）

## 提示
如果需要做状态停留时长分析，请直接使用 [获取状态流转时间接口](/api-doc/API文档/api_reference/measure/get_life_times.md)


## url
`${TAPD_API_ENDPOINT}/story_changes`

## 支持格式
JSON/XML（默认JSON格式）

## HTTP请求方式
GET

## 请求数限制
- `created` 参数与 `story_id` 参数二选一必填。即 story_id、created 两个参数至少填写一个
- 其中 created 参数要填写成日期格式，比如 created=2022-02-22，则返回 2022-02-22 这一天的变更历史
- 默认返回 30 条。可通过传 limit 参数设置，最大取 100。也可以传 page 参数翻页

## 请求参数
|字段名|必选|类型及范围|说明|特殊规则|
|:----:|:----:|:----:|:----:|:----:|
| id | 否 | integer | 变更历史id | 支持多ID查询 |
| story_id |否|integer|需求id|支持多ID查询|
| workspace_id | `是` | integer | 项目ID |  |
| creator | 否 | string | 创建人（操作人） |  |
| created | 否 | datetime | 创建时间（变更时间） | 支持时间查询 |
| change_type | 否 | string | 变更类型 | 值范围见文档下方附录1|
| change_summary | 否 | string | 需求变更描述 |  |
| comment | 否 | string | 评论 |  |
| entity_type | 否 | string | 变更的对象类型 |  |
| change_field | 否 | string | 设置获取变更字段如（status） | |
| need_parse_changes | 否 | integer | 设置field_changes字段是否返回（默认取 1。取 0 则不返回） |  |
| limit | 否 | integer | 设置返回数量限制，默认为30，最大取 100 | |
| page | 否 | integer | 返回当前数量限制下第N页的数据，默认为1（第一页）| |
| order | 否 | string | 排序规则，规则：字段名 ASC或者DESC，然后 urlencode |  如按创建时间逆序：order=created%20desc |
| fields | 否 | string | 设置获取的字段，多个字段间以','逗号隔开 | |


## 调用示例及返回结果
### 获取项目下需求变更历史
#### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password'  '${TAPD_API_ENDPOINT}/story_changes?workspace_id=10104801'`

#### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN'  '${TAPD_API_ENDPOINT}/story_changes?workspace_id=10104801'`

#### 返回结果
```JSON
{
    "status": 1,
    "data": [
        {
            "WorkitemChange": {
                "id": "1010104801027730979",
                "workspace_id": "10104801",
                "app_id": "1",
                "workitem_type_id": "0",
                "creator": "anyechen",
                "created": "2015-06-30 14:28:53",
                "change_summary": "planning",
                "comment": null,
                "changes": "[{\"field\":\"parent_id\",\"value_before\":\"0\",\"value_after\":\"1010104801056751739\"}]",
                "entity_type": "Story",
                "change_type": "",
                "change_type_detail": "",
                "updated": "2024-09-05 22:35:46",
                "change_type_text": "",
                "field_changes": [
                    {
                        "field": "parent_id",
                        "value_before": "0",
                        "value_after": "1010104801056751739",
                        "value_before_parsed": "0",
                        "value_after_parsed": "工具调研",
                        "field_label": "父需求"
                    }
                ],
                "story_id": "1010104801056751735"
            }
        },
        {
            "WorkitemChange": {
                "id": "1010104801027731105",
                "workspace_id": "10104801",
                "app_id": "1",
                "workitem_type_id": "0",
                "creator": "anyechen",
                "created": "2015-06-30 14:31:26",
                "change_summary": "planning",
                "comment": null,
                "changes": "[{\"field\":\"parent_id\",\"value_before\":\"0\",\"value_after\":\"1010104801056751739\"}]",
                "entity_type": "Story",
                "change_type": "",
                "change_type_detail": "",
                "updated": "2024-09-05 22:35:46",
                "change_type_text": "",
                "field_changes": [
                    {
                        "field": "parent_id",
                        "value_before": "0",
                        "value_after": "1010104801056751739",
                        "value_before_parsed": "0",
                        "value_after_parsed": "工具调研",
                        "field_label": "父需求"
                    }
                ],
                "story_id": "1010104801056751727"
            }
        }
    ],
    "info": "success"
}
```
### 获取需求ID为 1010104801056751735 的需求变更历史
#### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password'  '${TAPD_API_ENDPOINT}/story_changes?workspace_id=10104801&story_id=1010104801056751735'`

#### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN'  '${TAPD_API_ENDPOINT}/story_changes?workspace_id=10104801&story_id=1010104801056751735'`

#### 返回结果
```JSON
{
    "status": 1,
    "data": [
        {
            "WorkitemChange": {
                "id": "1010104801027730979",
                "workspace_id": "10104801",
                "app_id": "1",
                "workitem_type_id": "0",
                "creator": "anyechen",
                "created": "2015-06-30 14:28:53",
                "change_summary": "planning",
                "comment": null,
                "changes": "[{\"field\":\"parent_id\",\"value_before\":\"0\",\"value_after\":\"1010104801056751739\"}]",
                "entity_type": "Story",
                "change_type": "",
                "change_type_detail": "",
                "updated": "2024-09-05 22:35:46",
                "change_type_text": "",
                "field_changes": [
                    {
                        "field": "parent_id",
                        "value_before": "0",
                        "value_after": "1010104801056751739",
                        "value_before_parsed": "0",
                        "value_after_parsed": "工具调研",
                        "field_label": "父需求"
                    }
                ],
                "story_id": "1010104801056751735"
            }
        }
    ],
    "info": "success"
}
```

## 需求变更历史字段说明
### 需求变更历史重要字段说明
|字段|说明|
|:----:|:----:|
| id | id |
| workspace_id | 项目ID |
| workitem_type_id | 需求类别ID |
| updated | 更新时间 |
| app_id | 检查项 |
| creator | 创建人（操作人） |
| created | 创建时间（变更时间） |
| change_summary | 需求变更描述 |
| comment | 评论 |
| changes | 变更详细记录 |
| entity_type | 变更的对象类型 |
| change_type | 变更类型 |
| change_type_text | 变更类型结果中文 |
| change_type_detail | api账号 |
| field_changes | 变更详细记录 |

##附录1
|参数值|参数含义|
|:----:|:----:|
| sync_copy| 同步复制联动 |
| story_status_relation | 父子需求联动 |
| story_task_relation| 需求任务联动 |
| api | API变更 |
| smart_commit | Smart Commit触发 |
| auto_task | 自动化任务触发|
| auto_workflow | 自动化工作流触发 |
| manual_update | 手动变更 |
| import_update | 导入更新 |
| code_change | 代码变更 |
| status_delete | 状态删除 |
| exit_workspace | 退出项目触发 |
| link_update | 更新关联 |
| link_create | 创建关联 |
| link_delete | 删除关联 |
| create_story_from_copy | 复制创建 |


## 最佳实践
### 做状态停留时长分析
如果需要做状态停留时长分析，请直接使用 [获取状态流转时间接口](/api-doc/API文档/api_reference/measure/get_life_times.md)。

### 全量同步变更历史数据
如果需要同步项目全量状态变更历史数据，可以按照如下步骤：
1. 使用获取需求数据接口，分页获取需求的ID。比如 `${TAPD_API_ENDPOINT}/stories?workspace_id=项目ID&limit=30&page=1&fields=id`
2. 根据步骤1获取到的需求ID，加到 story_id 参数里面，分页获取变更历史数据。比如 `${TAPD_API_ENDPOINT}/story_changes?workspace_id=项目ID&story_id=需求ID1,需求ID2,需求3&limit=30&page=1`
3. 重复步骤1、步骤2直到拿到所有需求的变更历史

### 增量同步变更历史数据
因为变更历史数据不会变，只增不减。所以可以传递 created 参数来增量获取变更历史数据。参考这样：
1. 传递 created=日期 。比如 `${TAPD_API_ENDPOINT}/story_changes?workspace_id=项目ID&created=2022-02-22&limit=30&page=1` 来获取某天的变更历史数据
