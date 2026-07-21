# 说明
解除需求关联关系


# url
`${TAPD_API_ENDPOINT}/stories/remove_story_link_relation`

# 支持格式
JSON/XML（默认JSON格式）

#  HTTP请求方式
POST

# 请求数限制
一次只能删除一条关联关系


# 请求参数
|字段名|必选|类型及范围|说明|
|:----:|:----:|:----:|:----:|
| workspace_id | `是` | integer | 项目ID |
| src_story_id | `是` | integer | 源需求ID |
| target_story_id | `是` | integer | 目标需求ID |

# 调用示例及返回结果

### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password' -d 'workspace_id=10104801&src_story_id=1010104801115147834&target_story_id=1010104801115129060'  '${TAPD_API_ENDPOINT}/stories/remove_story_link_relation'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN' -d 'workspace_id=10104801&src_story_id=1010104801115147834&target_story_id=1010104801115129060'  '${TAPD_API_ENDPOINT}/stories/remove_story_link_relation'`

### 返回结果
```JSON
{
    "status": 1,
    "data": {
        "success": 1
    },
    "info": "success"
}
```
