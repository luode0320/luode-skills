# 说明
返回符合查询条件的所有需求分类（分页显示，默认一页30条）


# url
`${TAPD_API_ENDPOINT}/story_categories`

# 支持格式
JSON/XML（默认JSON格式）

# HTTP请求方式
GET

# 请求数限制
默认返回 30 条。可通过传 limit 参数设置，最大取 200。也可以传 page 参数翻页

# 请求参数
|字段名|必选|类型及范围|说明|特殊规则|
|:----:|:----:|:----:|:----:|:----:|
| id | 否 | integer | id | 支持多ID查询 |
| workspace_id | `是` | integer | 项目ID |  |
| name | 否 | string | 需求分类名称 | 支持模糊匹配 |
| description | 否 | string | 需求分类描述 |  |
| parent_id | 否 | integer | 父分类ID |  |
| created | 否 | datetime | 创建时间 | 支持时间查询 |
| modified | 否 | datetime | 最后修改时间 | 支持时间查询 |
| limit | 否 | integer | 设置返回数量限制，默认为30 | |
| page | 否 | integer | 返回当前数量限制下第N页的数据，默认为1（第一页）| |
| order | 否 | string | 排序规则，规则：字段名 ASC或者DESC，然后 urlencode |  如按创建时间逆序：order=created%20desc |
| fields | 否 | string | 设置获取的字段，多个字段间以','逗号隔开 | |

# 调用示例及返回结果
## 获取项目下需求分类
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password'  '${TAPD_API_ENDPOINT}/story_categories?workspace_id=10158231'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN'  '${TAPD_API_ENDPOINT}/story_categories?workspace_id=10158231'`

### 返回结果
```JSON
{
    "status": 1,
    "data": [
        {
            "Category": {
                "id": "-1",
                "workspace_id": "10158231",
                "name": "未分类",
                "description": "未分类",
                "parent_id": "0",
                "modified": "2017-06-20 14:05:53",
                "created": "2017-06-20 14:05:53",
                "creator": null,
                "modifier": "sunyoungsun"
            }
        },
        {
            "Category": {
                "id": "1010158231000072437",
                "workspace_id": "10158231",
                "name": "优化需求",
                "description": "优化需求",
                "parent_id": "1010158231000072431",
                "modified": "2017-06-20 14:05:13",
                "created": "2017-06-20 14:05:13",
                "creator": null,
                "modifier": "ruirayli"
            }
        },
        {
            "Category": {
                "id": "1010158231000072435",
                "workspace_id": "10158231",
                "name": "新功能",
                "description": "新功能",
                "parent_id": "1010158231000072431",
                "modified": "2017-06-20 14:05:13",
                "created": "2017-06-20 14:05:13",
                "creator": null,
                "modifier": "ruirayli"
            }
        },
        {
            "Category": {
                "id": "1010158231000072433",
                "workspace_id": "10158231",
                "name": "技术需求",
                "description": "技术需求",
                "parent_id": "0",
                "modified": "2017-06-20 14:05:13",
                "created": "2017-06-20 14:05:13",
                "creator": null,
                "modifier": "ruirayli"
            }
        },
        {
            "Category": {
                "id": "1010158231000072431",
                "workspace_id": "10158231",
                "name": "产品需求",
                "description": "产品需求",
                "parent_id": "0",
                "modified": "2017-06-20 14:05:13",
                "created": "2017-06-20 14:05:13",
                "creator": null,
                "modifier": "ruirayli"
            }
        }
    ],
    "info": "success"
}
```

# 需求分类字段说明
## 需求分类重要字段说明
|字段|说明|
|:----:|:----:|
| id | id |
| workspace_id | 项目ID |
| name | 需求分类名称 |
| description | 需求分类描述 |
| parent_id | 父分类ID |
| created | 创建时间 |
| modified | 最后修改时间 |
