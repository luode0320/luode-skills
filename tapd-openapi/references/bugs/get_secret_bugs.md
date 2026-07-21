# 说明
批量查询所有保密缺陷（bug）单列表（分页显示，默认一页30条）
结果以列表形式返回


# url
`${TAPD_API_ENDPOINT}/secret_bugs`

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
| limit | 否 | integer | 设置返回数量限制，默认为30 | |
| page | 否 | integer | 返回当前数量限制下第N页的数据，默认为1（第一页）| |
| order | 否 | string | 排序规则，规则：字段名 ASC或者DESC，然后 urlencode |  如按创建时间逆序：order=created%20desc |

# 调用示例及返回结果
## 获取项目下保密缺陷
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password'  '${TAPD_API_ENDPOINT}/secret_bugs?workspace_id=10158231'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN'  '${TAPD_API_ENDPOINT}/secret_bugs?workspace_id=10158231'`

### 返回结果
```JSON
{
    "status": 1,
    "data": {
        "list": [
            "11516xxxxx000063",
            "11516xxxxx000062",
            "11516xxxxx000061"
        ]
    },
    "info": "success"
}
```
