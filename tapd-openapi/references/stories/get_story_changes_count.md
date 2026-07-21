# 说明
计算符合查询条件的需求变更历史数量并返回


# url
`${TAPD_API_ENDPOINT}/story_changes/count`

# 支持格式
JSON/XML（默认JSON格式）

#  HTTP请求方式
GET

# 请求数限制
只返回需求变更历史数量

# 请求参数
|字段名|必选|类型及范围|说明|特殊规则|
|:----:|:----:|:----:|:----:|:----:|
| id | 否 | integer | 变更历史id |  |
| story_id | 否 | integer | 需求ID |  |
| workspace_id | `是` | integer | 项目ID |  |
| creator | 否 | string | 创建人（操作人） |  |
| created | 否 | datetime | 创建时间（变更时间） | 支持时间查询 |
| change_summary | 否 | string | 需求变更描述 |  |
| comment | 否 | string | 评论 |  |
| changes | 否 | string | 变更详细记录 |  |
| entity_type | 否 | string | 变更的对象类型 |  |


# 调用示例及返回结果
## 获取项目下需求变更次数
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password'  '${TAPD_API_ENDPOINT}/story_changes/count?workspace_id=10158231'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN'  '${TAPD_API_ENDPOINT}/story_changes/count?workspace_id=10158231'`

### 返回结果
```JSON
{
    "status": 1,
    "data": {
        "count": 21
    },
    "info": "success"
}
```

## 获取需求ID为 1010158231500625827 的需求变更次数
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password'  '${TAPD_API_ENDPOINT}/story_changes/count?workspace_id=10158231&story_id=1010158231500625827'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN'  '${TAPD_API_ENDPOINT}/story_changes/count?workspace_id=10158231&story_id=1010158231500625827'`

### 返回结果
```JSON
{
    "status": 1,
    "data": {
        "count": 1
    },
    "info": "success"
}
```
