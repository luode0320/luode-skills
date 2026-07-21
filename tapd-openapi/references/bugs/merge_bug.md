# 说明
合并缺陷。合并缺陷操作会把源缺陷的评论、附件合并到目标缺陷中去；`原缺陷会被删除`。


# url
`${TAPD_API_ENDPOINT}/bugs/merge_bug`

# 支持格式
JSON/XML（默认JSON格式）

#  HTTP 请求方式
POST

# 请求数限制
- 一次合并一条缺陷

# 请求参数
|字段名|必选|类型及范围|说明|
|:----:|:----:|:----:|:----:|
| workspace_id | `是` | integer | 源项目ID |
| source_bug_id |  `是`  | integer | 源缺陷ID（会被删除） |
| target_bug_id |  `是`  | integer | 目标缺陷ID |
| will_delete_source_bug |  `是`  | integer | 源缺陷ID，要与 source_bug_id 取值一致 |


# 调用示例及返回结果
## 合并缺陷
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password' -d 'workspace_id=10104801&target_bug_id=1010104801122145365&source_bug_id=1010104801125853159&will_delete_source_bug=1010104801125853159' '${TAPD_API_ENDPOINT}/bugs/merge_bug'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN' -d 'workspace_id=10104801&target_bug_id=1010104801122145365&source_bug_id=1010104801125853159&will_delete_source_bug=1010104801125853159' '${TAPD_API_ENDPOINT}/bugs/merge_bug'`

### 返回结果
```json
{
    "status": 1,
    "data": {
        "ret": "1010104801122145365"
    },
    "info": "success"
}
```
