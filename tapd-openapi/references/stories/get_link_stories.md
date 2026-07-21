# 说明
获取需求与其它需求的所有关联关系（无分页）


# url
`${TAPD_API_ENDPOINT}/stories/get_link_stories`

# 支持格式
JSON/XML（默认JSON格式）

#  HTTP请求方式
GET

# 请求数限制
一次返回所有符合条件的值


# 请求参数
|字段名|必选|类型及范围|说明|特殊规则|
|:----:|:----:|:----:|:----:|:----:|
|workspace_id|`是`|integer|项目ID|无|
|story_id|`是`|integer|19位长度的需求ID|无|

# 调用示例及返回结果
获取需求 1010158231500691431 与其它需求的所有关联关系
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password'  '${TAPD_API_ENDPOINT}/stories/get_link_stories?story_id=1010158231500691431&workspace_id=10158231'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN'  '${TAPD_API_ENDPOINT}/stories/get_link_stories?story_id=1010158231500691431&workspace_id=10158231'`

### 返回结果
```JSON
{
    "status": 1,
    "data": [
        {
            "type": "derivation",
            "id": "1010158231500691433",
            "story_id": "1010158231500691431",
            "workspace_id": "10158231",
            "actas": "target",
            "created": "2019-08-01 16:32:22",
            "modified": "2022-03-18 18:54:25",
            "linked_workspace_id": 10158231
        },
        {
            "type": "sync_copy",
            "id": "1010158231500691437",
            "story_id": "1010158231500691431",
            "workspace_id": "10158231",
            "actas": "target",
            "created": "2019-08-01 16:33:06",
            "modified": "2024-05-10 11:55:03",
            "linked_workspace_id": 10158231
        },
        {
            "type": "copy",
            "id": "1010104801500691441",
            "story_id": "1010158231500691431",
            "workspace_id": "10158231",
            "actas": "target",
            "created": "2019-08-01 16:33:32",
            "modified": "2022-03-18 18:54:25",
            "linked_workspace_id": 10104801
        },
        {
            "type": "direct_relate",
            "id": "1000000755500691185",
            "story_id": "1010158231500691431",
            "workspace_id": "10158231",
            "actas": "target",
            "created": "2019-08-01 16:33:48",
            "modified": "2022-03-18 18:54:25",
            "linked_workspace_id": 755
        }
    ],
    "info": "success"
}
```

# 需求字段说明
## 需求重要字段说明
|字段|说明|
|:----:|:----:|
|type|关系类型。sync_copy 为 同步复制，copy 为复制，derivation 为派生（父子关系），direct_relate 为直接关联，sync_relate 为关联同步|
|id|关联的需求ID|
|workspace_id|项目ID|
| story_id| 原需求ID|
|linked_workspace_id|项目ID|
|actas|角色。target 为操作发起方|
