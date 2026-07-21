# 说明
获取指定需求的保密信息


# url
`${TAPD_API_ENDPOINT}/stories/get_secret_info`

# 支持格式
JSON/XML（默认JSON格式）

#  HTTP请求方式
GET

# 请求数限制
每次只允许查询一条需求

# 请求参数
|字段名|必选|类型及范围|说明|
|:----:|:----:|:----:|:----:|
| story_id | `是` | integer | 需求ID |
| workspace_id | `是` | integer | 项目ID |


# 调用示例及返回结果
## 获取需求1010104801871430407的保密信息
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password' '${TAPD_API_ENDPOINT}/stories/get_secret_info?workspace_id=10104801&story_id=1010104801871430407'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN' '${TAPD_API_ENDPOINT}/stories/get_secret_info?workspace_id=10104801&story_id=1010104801871430407'`

### 返回结果
```JSON
{
    "status": 1,
    "data": {
        "creator": "xinweihe",
        "allow_list": "xinweihe;1000000000000000002",
        "secret_root_id": "1010104801871430407",
        "add_participant_fields": "true",
        "secret_scrope": "secret"
    },
    "info": "success"
}
```

# 返回data字段说明
|字段|说明|
|:----:|:----:|
| creator | 该需求的创建人。在计算需求可见性时，需求对于其创建人是默认可见的。 |
| allow_list | 该需求所在保密需求树的白名单。在白名单内的人员或用户组可以见到树上的所有需求。 |
| secret_root_id | 需求所在保密需求树的树根节点，公开时为0。同一个保密树根下的“保密树”共享同样的保密可见范围。 |
| add_participant_fields | 保密范围是否纳入参与人。若为"true"，则这棵保密树下每个需求的每个人名字段内填写的每个人名和用户组都默认可访问该树上的所有需求。 |
| secret_scrope | secret:需求保密; public:需求公开。需求保密与否等价于secret_root_id是否非0. |
