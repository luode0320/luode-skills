# 说明
返回符合查询条件的所有测试用例目录（分页显示，默认一页30条）


# url
`${TAPD_API_ENDPOINT}/tcase_categories`

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
| name | 否 | string | 目录名称 | 支持模糊匹配 |
| description | 否 | string | 目录描述 |  |
| parent_id | 否 | integer | 父目录ID |  |
| modified | 否 | datetime | 最后修改时间 | 支持时间查询 |
| created | 否 | datetime | 创建时间 | 支持时间查询 |
| creator | 否 | string | 目录创建人 |  |
| modifier | 否 | string | 目录最后修改人 |  |
| sorting | 否 | integer | 目录排序序号 |  |
| limit | 否 | integer | 设置返回数量限制，默认为30 | |
| page | 否 | integer | 返回当前数量限制下第N页的数据，默认为1（第一页）| |
| order | 否 | string | 排序规则，规则：字段名 ASC或者DESC，然后 urlencode |  如按创建时间逆序：order=created%20desc |
| fields | 否 | string | 设置获取的字段，多个字段间以','逗号隔开 | |

# 调用示例及返回结果
## 获取项目下测试用例目录
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password'  '${TAPD_API_ENDPOINT}/tcase_categories?workspace_id=10158231'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN'  '${TAPD_API_ENDPOINT}/tcase_categories?workspace_id=10158231'`

### 返回结果
```JSON
{
    "status": 1,
    "data": [
        {
            "TcaseCategory": {
                "id": "1010158231075917759",
                "workspace_id": "10158231",
                "name": "None Category",
                "description": "未规划目录",
                "parent_id": "0",
                "modified": "2019-06-26 16:42:50",
                "created": "2019-06-26 16:42:50",
                "creator": null,
                "modifier": null,
                "sorting": "0"
            }
        },
        {
            "TcaseCategory": {
                "id": "1010158231000082521",
                "workspace_id": "10158231",
                "name": "用例目录3",
                "description": null,
                "parent_id": "0",
                "modified": "2017-06-20 16:48:37",
                "created": "2017-06-20 16:48:37",
                "creator": "system",
                "modifier": "system",
                "sorting": null
            }
        },
        {
            "TcaseCategory": {
                "id": "1010158231000082519",
                "workspace_id": "10158231",
                "name": "用例目录2",
                "description": null,
                "parent_id": "0",
                "modified": "2017-06-20 16:48:37",
                "created": "2017-06-20 16:48:37",
                "creator": "system",
                "modifier": "system",
                "sorting": null
            }
        },
        {
            "TcaseCategory": {
                "id": "1010158231000082517",
                "workspace_id": "10158231",
                "name": "用例目录1",
                "description": null,
                "parent_id": "0",
                "modified": "2017-06-20 16:48:37",
                "created": "2017-06-20 16:48:37",
                "creator": "system",
                "modifier": "system",
                "sorting": null
            }
        }
    ],
    "info": "success"
}
```

# 测试用例目录字段说明
## 测试用例目录重要字段说明
|字段|说明|
|:----:|:----:|
| id | id |
| workspace_id | 项目ID |
| name | 目录名称 |
| description | 目录描述 |
| parent_id | 父目录ID |
| modified | 最后修改时间 |
| created | 创建时间 |
| creator | 目录创建人 |
| modifier | 目录最后修改人 |
| sorting | 目录排序序号 |
