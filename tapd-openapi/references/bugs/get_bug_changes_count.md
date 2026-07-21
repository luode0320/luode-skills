# 说明
计算符合查询条件的缺陷变更历史数量并返回


# url
`${TAPD_API_ENDPOINT}/bug_changes/count`

# 支持格式
JSON/XML（默认JSON格式）

#  HTTP请求方式
GET

# 请求数限制
只返回缺陷变更历史数量

# 请求参数
|字段名|必选|类型及范围|说明|特殊规则|
|:----:|:----:|:----:|:----:|:----:|
| id | 否 | integer | id | 支持多ID查询 |
| bug_id | 否 | integer | 缺陷ID | 支持多ID查询 |
| author | 否 | string | 变更人 |  |
| field | 否 | string | 变更字段 |  |
| old_value | 否 | string | 变更前 |  |
| new_value | 否 | string | 变更后 |  |
| memo | 否 | string | 备注 |  |
| created | 否 | datetime | 创建时间 | 支持时间查询 |
| workspace_id | `是` | integer | 项目ID |  |


# 调用示例及返回结果
## 获取项目下缺陷变更次数
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password'  '${TAPD_API_ENDPOINT}/bug_changes/count?workspace_id=10158231'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN'  '${TAPD_API_ENDPOINT}/bug_changes/count?workspace_id=10158231'`

### 返回结果
```JSON
{
    "status": 1,
    "data": {
        "count": 7
    },
    "info": "success"
}
```
## 获取缺陷ID为 1010158231500628815 的变更次数
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password'  '${TAPD_API_ENDPOINT}/bug_changes/count?workspace_id=10158231&bug_id=1010158231500628815'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN'  '${TAPD_API_ENDPOINT}/bug_changes/count?workspace_id=10158231&bug_id=1010158231500628815'`

### 返回结果
```JSON
{
    "status": 1,
    "data": {
        "count": 6
    },
    "info": "success"
}
```
