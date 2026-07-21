# 说明
批量删除需求前后置关系


# url
`${TAPD_API_ENDPOINT}/stories/delete_time_relations`

# 支持格式
JSON/XML（默认JSON格式）

#  HTTP请求方式
POST

# 请求参数
|字段名|必选|类型及范围|说明|
|:----|:----:|:----:|:----|
| workspace_id | `是` | integer | 项目ID |
| relations | `否` | array | 所需删除的关系列表（按起点和终点） |
| relations[0][workitem_id] | `否` | integer | 示例, 所需按节点删除的第0条关系的“起点需求id” |
| relations[0][dst_workitem_id] | `否` | integer | 示例, 所需按节点删除的第0条关系的“终点需求id” |
| relation_ids | `否` | array | 所需删除的关系列表（按id） |
| relation_ids[0] | `否` | integer | 所需按id删除的第0条关系的id |
| current_user | `是` | string | 执行此操作的用户的nick |


# 调用示例及返回结果

### 备注和调用推荐

- 理想情况下，开发者能够提前知道所需删除的关系的id，直接利用“按id删除”模式调用即可。
- 但在一些特殊情况下，难免会出现“只知道要删除从需求A到需求B的关系，却不知道它的具体id是什么”的情况。在这种情况下，如果需要额外获取关系的id，路径比较曲折且不必要。此时则可以在参数中采用“按节点删除”的模式。
- 如果上述两种情况都存在，那么可以在参数里混传两个列表，系统会分别按照id和按照节点查询各自所需删除的实际关系，并将两个列表合并后进行删除。

## 按照节点，删除从需求A（1020375552855142317）指向需求B（1020375552855139943）的前后置关系

### curl 使用 Basic Auth 鉴权调用示例

`curl -u 'api_user:api_password' -d 'workspace_id=20375552&relations[0][workitem_id]=1020375552855142317&relations[0][dst_workitem_id]=1020375552855139943&current_user=xinweihe' '${TAPD_API_ENDPOINT}/stories/delete_time_relations'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN' -d 'workspace_id=20375552&relations[0][workitem_id]=1020375552855142317&relations[0][dst_workitem_id]=1020375552855139943&current_user=xinweihe' '${TAPD_API_ENDPOINT}/stories/delete_time_relations'`

## 按照ID，删除前后置关系

### curl 使用 Basic Auth 鉴权调用示例

`curl -u 'api_user:api_password' -d 'workspace_id=20375552&relation_ids[0]=1220375552000009739&current_user=xinweihe' '${TAPD_API_ENDPOINT}/stories/delete_time_relations'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN' -d 'workspace_id=20375552&relation_ids[0]=1220375552000009739&current_user=xinweihe' '${TAPD_API_ENDPOINT}/stories/delete_time_relations'`

### 返回结果
结果中的num代表了实际删除的条数。
```JSON
{
    "status": 1,
    "data": {
        "num": 1,
    },
    "info": "success"
}
```
