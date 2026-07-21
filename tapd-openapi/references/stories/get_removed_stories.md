# 说明
返回符合查询条件的所有回收站中的需求


# url
`${TAPD_API_ENDPOINT}/stories/get_removed_stories`

# 支持格式
JSON/XML（默认JSON格式）

# HTTP请求方式
GET

# 请求数限制
默认返回 30 条。可通过传 limit 参数设置，最大取 200。也可以传 page 参数翻页

# 请求参数
|字段名|必选|类型及范围|说明|特殊规则|
|:----:|:----:|:----:|:----:|:----:|
| workspace_id | `是` | integer | 项目ID |  |
| id | 否 | integer | 需求ID |  |
| creator | 否 | string | 创建人 |  |
| is_archived | 否 | integer | 是否为归档。默认取 0，为不返回归档的需求。传 is_archived=1 参数则仅返回归档的需求 |  |
| created | 否 | date | 创建时间 |  |
| deleted | 否 | date | 删除时间 |  |
| limit | 否 | integer | 设置返回数量限制，默认为30 | |
| page | 否 | integer | 返回当前数量限制下第N页的数据，默认为1（第一页）| |

# 调用示例及返回结果
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password'  '${TAPD_API_ENDPOINT}/stories/get_removed_stories?workspace_id=10104801'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN'  '${TAPD_API_ENDPOINT}/stories/get_removed_stories?workspace_id=10104801'`

### 返回结果
```JSON
{
    "status": 1,
    "data": [
        {
            "RemovedStory": {
                "id": "1010104801854921589",
                "name": "cat",
                "creator": "tapd",
                "created": "2021-08-25 15:37:16",
                "operation_user": "v_xuanfang",
                "deleted": "2021-09-13 16:48:16",
                "is_archived": "0"
            }
        },
        {
            "RemovedStory": {
                "id": "1010104801854923037",
                "name": "嗷嗷嗷",
                "creator": "v_xuanfang",
                "created": "2021-08-31 11:01:51",
                "operation_user": "anyechen",
                "deleted": "2021-09-14 15:46:11",
                "is_archived": "0"
            }
        }
    ],
    "info": "success"
}
```

# 回收站字段说明
## 回收站重要字段说明
|字段|说明|
|:----:|:----:|
| id | 需求ID |
| name | 标题 |
| creator | 创建人 |
| created | 创建时间 |
| operation_user | 删除人 |
| deleted | 删除时间 |
| is_archived | 是否为归档 |
