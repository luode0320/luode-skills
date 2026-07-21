# 说明
创建需求与缺陷关联关系


# URL
`${TAPD_API_ENDPOINT}/relations`

# 支持格式
JSON/XML (默认JSON格式)

# HTTP请求方式
POST

# 请求数限制
一次插入一条数据

# 请求参数
|字段名|必选|类型及范围|说明|特殊规则|
|:----:|:----:|:----:|:----:|:----:|
| workspace_id | 是 | integer | 所属TAPD项目ID | |
| source_type | 是 | string | 关联关系源对象类型（story、bug） | |
| target_type | 是 | string | 关联关系目标对象类型（story、bug）| |
| source_id | 是 | integer | 关联关系源对象id | |
| target_id | 是 | integer | 关联关系目标对象id | |

## 创建 需求1010104801864772561 与 缺陷1010104801085924155 关联关系
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password' -d 'workspace_id=10104801&source_type=bug&source_id=1010104801085924155&target_type=story&target_id=1010104801864772561' '${TAPD_API_ENDPOINT}/relations'`
### curl 使用 OAuth Access Token 鉴权调用示例
`curl -u 'Authorization: Bearer ACCESS_TOKEN' -d 'workspace_id=10104801&source_type=bug&source_id=1010104801085924155&target_type=story&target_id=1010104801864772561' '${TAPD_API_ENDPOINT}/relations'`

# 返回结果
以返回结果为准
```JSON
{
    "status": 1,
    "data": {
        "Relation": {
            "id": "22265547",
            "workspace_id": "10104801",
            "source_type": "story",
            "source_id": "1010104801864772561",
            "target_type": "bug",
            "target_id": "1010104801085924155",
            "modified": "2021-05-20 15:10:59",
            "created": "2021-05-20 15:10:59"
        }
    },
    "info": "success"
}
```

# 返回结果字段说明
|字段|说明|
|:----:|:----:|
| id | 主键ID |
| workspace_id | 项目ID |
| source_type | 关联关系源对象类型 |
| source_id | 关联关系源对象id |
| target_type | 关联关系目标对象类型 |
| target_id | 关联关系目标对象id |
| created | 创建时间 |
| modified | 最后修改时间 |
