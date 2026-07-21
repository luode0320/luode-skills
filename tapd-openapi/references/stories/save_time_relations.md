# 说明
批量新增/修改需求前后置关系


# url
`${TAPD_API_ENDPOINT}/stories/save_time_relations`

# 支持格式
JSON/XML（默认JSON格式）

#  HTTP请求方式
POST

# 请求参数
|字段名|必选|类型及范围|说明|
|:----|:----:|:----:|:----|
| workspace_id | `是` | integer | 项目ID |
| relations | `是` | array | 所需新增或修改的关系列表 |
| relations[0][workitem_id] | `是` | integer | 示例, 所需添加或修改的第0条关系的“起点需求id” |
| relations[0][dst_workitem_id] | `是` | integer | 示例, 所需添加或修改的第0条关系的“终点需求id” |
| relations[0][src_field] | `是` | string | 示例, 所需添加或修改的第0条关系的“起点字段”，只能是`begin`或`due`，代表需求开始或结束事件 |
| relations[0][dst_field] | `是` | string | 示例, 所需添加或修改的第0条关系的“终点字段”，只能是`begin`或`due`，代表需求开始或结束事件 |
| current_user | `是` | string | 执行此操作的用户的nick |


# 调用示例及返回结果

## 修改需求A（1020375552855142317）和需求B（1020375552855139943）的前后置关系，需求A在开始之后，需求B才能结束。

### 备注与限制条件
1. 若需求A和需求B之间不存在前后置关系，则会新建一条如此的关系。
2. 若需求A和需求B之间已经存在关系，则会修改、覆盖此关系。任何时候，两个需求之间至多能有1条前后置关系。
3. 需求A和需求B必须是同一个项目下的需求。
4. 起点需求不能是终点需求（关系不能从自己指向自己）。
5. 目前支持的四种关系
	- 开始后开始：需求A开始后，需求B才能开始。此时`src_field` = `begin`, `dst_field` = `begin`.
	- 开始后结束：需求A开始后，需求B才能结束。此时`src_field` = `begin`, `dst_field` = `due`.
	- 结束后开始：需求A结束后，需求B才能开始。此时`src_field` = `due`, `dst_field` = `begin`.
	- 结束后结束：需求A结束后，需求B才能结束。此时`src_field` = `due`, `dst_field` = `due`.
6. 若想创建一条从B指向A的关系，让`workitem_id`（起点需求id）为B的id，`dst_workitem_id`（终点需求id）为A的id即可。

### curl 使用 Basic Auth 鉴权调用示例

`curl -u 'api_user:api_password' -d 'workspace_id=20375552&relations[0][workitem_id]=1020375552855142317&relations[0][dst_workitem_id]=1020375552855139943&relations[0][src_field]=begin&relations[0][dst_field]=due&current_user=xinweihe' '${TAPD_API_ENDPOINT}/stories/save_time_relations'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN' -d 'workspace_id=20375552&relations[0][workitem_id]=1020375552855142317&relations[0][dst_workitem_id]=1020375552855139943&relations[0][src_field]=begin&relations[0][dst_field]=due&current_user=xinweihe' '${TAPD_API_ENDPOINT}/stories/save_time_relations'`

### 返回结果
```JSON
{
    "status": 1,
    "data": {
        "result": true,
    },
    "info": "success"
}
```
