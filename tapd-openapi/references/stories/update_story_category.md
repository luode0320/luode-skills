# 说明
更新需求分类，返回更新需求分类的数据


# url
`${TAPD_API_ENDPOINT}/story_categories`

# 支持格式
JSON/XML（默认JSON格式）

# HTTP请求方式
POST

# 请求数限制
一次插入一条数据

# 请求参数
|字段名|必选|类型及范围|说明|
|:----:|:----:|:----:|:----:|
| workspace_id | `是` | integer | 项目ID |
| id | `是` | integer | ID |
| name | 否 | string | 分类名称 |
| description | 否 | string | 分类描述 |
| parent_id | 否 | integer | 父分类ID |

# 调用示例及返回结果
## 更新需求分类
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password' -d 'workspace_id=10104801&name=test111&id=1010104801002646384'  '${TAPD_API_ENDPOINT}/story_categories'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN' -d 'workspace_id=10104801&name=test111&id=1010104801002646384'  '${TAPD_API_ENDPOINT}/story_categories'`

### 返回结果
```JSON
{
    "status": 1,
    "data": {
        "Category": {
            "id": "1010104801002646384",
            "workspace_id": "10104801",
            "name": "test111",
            "description": null,
            "parent_id": "0",
            "modified": "2025-07-08 15:22:49",
            "created": "2025-06-16 16:20:51",
            "creator": "v_xuanfang",
            "modifier": "v_xuanfang"
        }
    },
    "info": "success"
}
```

# 需求分类字段说明
## 需求分类重要字段说明
|字段|说明|
|:----:|:----:|
| id | id |
| workspace_id | 项目ID |
| name | 分类名称 |
| description | 分类描述 |
| parent_id | 父分类ID |
| created | 创建时间 |
| creator | 创建人 |
| modified | 最后修改时间 |
| modifier | 最后修改人 |
