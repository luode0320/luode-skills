## 说明
返回符合查询条件的所有缺陷变更历史（分页显示，默认一页30条）

## 提示
如果需要做状态停留时长分析，请直接使用 [获取状态流转时间接口](/api-doc/API文档/api_reference/measure/get_life_times.md)


## url
`${TAPD_API_ENDPOINT}/bug_changes`

## 支持格式
JSON/XML（默认JSON格式）

## HTTP请求方式
GET

## 请求数限制
- `created` 参数与 `bug_id` 参数二选一必填。即 bug_id、created 两个参数至少填写一个
- 其中 created 参数要填写成日期格式，比如 created=2022-02-22，则返回 2022-02-22 这一天的变更历史
- 默认返回 30 条。可通过传 limit 参数设置，最大取 200。也可以传 page 参数翻页

## 请求参数
|字段名|必选|类型及范围|说明|特殊规则|
|:----:|:----:|:----:|:----:|:----:|
| workspace_id | `是` | integer | 项目ID |  |
| created | `是` | datetime | 创建时间 | 支持按天查询。比如 created=2022-02-22 |
| bug_id | `是` | integer | 缺陷ID | 支持多ID查询 |
| id | 否 | integer | id | 支持多ID查询 |
| author | 否 | string | 变更人 |  |
| field | 否 | string | 变更字段 |  |
| old_value | 否 | string | 变更前 |  |
| new_value | 否 | string | 变更后 |  |
| memo | 否 | string | 备注 |  |
| include_add_bug | 否 | integer | 设置返回创建缺陷的记录（值传1） |  |
| limit | 否 | integer | 设置返回数量限制，默认为30 | |
| page | 否 | integer | 返回当前数量限制下第N页的数据，默认为1（第一页）| |
| order | 否 | string | 排序规则，规则：字段名 ASC或者DESC，然后 urlencode |  如按创建时间逆序：order=created%20desc |
| fields | 否 | string | 设置获取的字段，多个字段间以','逗号隔开 | |

## 调用示例及返回结果
### 获取项目下缺陷变更历史
#### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password'  '${TAPD_API_ENDPOINT}/bug_changes?workspace_id=10158231'`

#### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN'  '${TAPD_API_ENDPOINT}/bug_changes?workspace_id=10158231'`

#### 返回结果
```JSON
{
    "status": 1,
    "data": [
        {
            "BugChange": {
                "id": "10101582315000015921",
                "bug_id": "1010158231500628815",
                "author": "anyechen",
                "field": "severity",
                "old_value": "serious",
                "new_value": "normal",
                "memo": null,
                "created": "2019-06-26 20:48:52",
                "workspace_id": "10158231"
            }
        },
        {
            "BugChange": {
                "id": "10101582315000015919",
                "bug_id": "1010158231500628815",
                "author": "anyechen",
                "field": "severity",
                "old_value": "fatal",
                "new_value": "serious",
                "memo": null,
                "created": "2019-06-26 20:47:24",
                "workspace_id": "10158231"
            }
        },
        {
            "BugChange": {
                "id": "10101582315000015917",
                "bug_id": "1010158231500628815",
                "author": "anyechen",
                "field": "priority",
                "old_value": "urgent",
                "new_value": "high",
                "memo": null,
                "created": "2019-06-26 20:47:21",
                "workspace_id": "10158231"
            }
        },
        {
            "BugChange": {
                "id": "10101582315000015915",
                "bug_id": "1010158231500628815",
                "author": "anyechen",
                "field": "current_owner",
                "old_value": null,
                "new_value": "anyechen;",
                "memo": null,
                "created": "2019-06-26 20:47:18",
                "workspace_id": "10158231"
            }
        },
        {
            "BugChange": {
                "id": "10101582315000015913",
                "bug_id": "1010158231500628815",
                "author": "anyechen",
                "field": "severity",
                "old_value": "normal",
                "new_value": "fatal",
                "memo": null,
                "created": "2019-06-26 20:47:02",
                "workspace_id": "10158231"
            }
        },
        {
            "BugChange": {
                "id": "10101582315000015911",
                "bug_id": "1010158231500628815",
                "author": "anyechen",
                "field": "priority",
                "old_value": "medium",
                "new_value": "urgent",
                "memo": null,
                "created": "2019-06-26 20:46:59",
                "workspace_id": "10158231"
            }
        },
        {
            "BugChange": {
                "id": "1010158231606851987",
                "bug_id": "1010158231500628817",
                "author": "anyechen",
                "field": "severity",
                "old_value": "serious",
                "new_value": "prompt",
                "memo": null,
                "created": "2018-01-12 14:45:29",
                "workspace_id": "10158231"
            }
        }
    ],
    "info": "success"
}
```
获取缺陷ID为 1010158231500628815 的变更历史
#### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password'  '${TAPD_API_ENDPOINT}/bug_changes?workspace_id=10158231&bug_id=1010158231500628815'`

#### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN'  '${TAPD_API_ENDPOINT}/bug_changes?workspace_id=10158231&bug_id=1010158231500628815'`

#### 返回结果
```JSON
{
    "status": 1,
    "data": [
        {
            "BugChange": {
                "id": "10101582315000015921",
                "bug_id": "1010158231500628815",
                "author": "anyechen",
                "field": "severity",
                "old_value": "serious",
                "new_value": "normal",
                "memo": null,
                "created": "2019-06-26 20:48:52",
                "workspace_id": "10158231"
            }
        },
        {
            "BugChange": {
                "id": "10101582315000015919",
                "bug_id": "1010158231500628815",
                "author": "anyechen",
                "field": "severity",
                "old_value": "fatal",
                "new_value": "serious",
                "memo": null,
                "created": "2019-06-26 20:47:24",
                "workspace_id": "10158231"
            }
        },
        {
            "BugChange": {
                "id": "10101582315000015917",
                "bug_id": "1010158231500628815",
                "author": "anyechen",
                "field": "priority",
                "old_value": "urgent",
                "new_value": "high",
                "memo": null,
                "created": "2019-06-26 20:47:21",
                "workspace_id": "10158231"
            }
        },
        {
            "BugChange": {
                "id": "10101582315000015915",
                "bug_id": "1010158231500628815",
                "author": "anyechen",
                "field": "current_owner",
                "old_value": null,
                "new_value": "anyechen;",
                "memo": null,
                "created": "2019-06-26 20:47:18",
                "workspace_id": "10158231"
            }
        },
        {
            "BugChange": {
                "id": "10101582315000015913",
                "bug_id": "1010158231500628815",
                "author": "anyechen",
                "field": "severity",
                "old_value": "normal",
                "new_value": "fatal",
                "memo": null,
                "created": "2019-06-26 20:47:02",
                "workspace_id": "10158231"
            }
        },
        {
            "BugChange": {
                "id": "10101582315000015911",
                "bug_id": "1010158231500628815",
                "author": "anyechen",
                "field": "priority",
                "old_value": "medium",
                "new_value": "urgent",
                "memo": null,
                "created": "2019-06-26 20:46:59",
                "workspace_id": "10158231"
            }
        }
    ],
    "info": "success"
}
```

## 缺陷变更历史字段说明
### 缺陷变更历史重要字段说明
|字段|说明|
|:----:|:----:|
| id | id |
| bug_id | 缺陷ID |
| author | 变更人 |
| field | 变更字段 |
| old_value | 变更前 |
| new_value | 变更后 |
| memo | 备注 |
| created | 创建时间 |
| workspace_id | 项目ID |


## 最佳实践
### 做状态停留时长分析
如果需要做状态停留时长分析，请直接使用 [获取状态流转时间接口](/api-doc/API文档/api_reference/measure/get_life_times.md)。

### 全量同步变更历史数据
如果需要同步项目全量状态变更历史数据，可以按照如下步骤：
1. 使用获取缺陷数据接口，分页获取缺陷的ID。比如 `${TAPD_API_ENDPOINT}/bugs?workspace_id=项目ID&limit=30&page=1&fields=id`
2. 根据步骤1获取到的缺陷ID，加到 bug_id 参数里面，分页获取变更历史数据。比如 `${TAPD_API_ENDPOINT}/bug_changes?workspace_id=项目ID&bug_id=缺陷ID1,缺陷ID2,缺陷3&limit=30&page=1`
3. 重复步骤1、步骤2直到拿到所有缺陷的变更历史
### 增量同步变更历史数据
因为变更历史数据不会变，只增不减。所以可以传递 created 参数来增量获取变更历史数据。参考这样：
1. 传递 created=日期 。比如 `${TAPD_API_ENDPOINT}/bug_changes?workspace_id=项目ID&created=2022-02-22&limit=30&page=1` 来获取某天的变更历史数据。
