# 说明
创建测试用例目录，返回创建测试用例目录的数据


# url
`${TAPD_API_ENDPOINT}/tcase_categories`

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
| name | `是` | string | 目录名称 |
| description | 否 | string | 目录描述 |
| parent_id | 否 | integer | 父目录ID |
| creator | 否 | string | 创建人 |

# 调用示例及返回结果
## 创建测试用例目录
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password' -d 'workspace_id=20355782&name=test'  '${TAPD_API_ENDPOINT}/tcase_categories'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN' -d 'workspace_id=20355782&name=test'  '${TAPD_API_ENDPOINT}/tcase_categories'`

### 返回结果
```JSON
{
    "status": 1,
    "data": {
        "TcaseCategory": {
            "id": "1020355782075922101",
            "workspace_id": "20355782",
            "name": "test",
            "description": null,
            "parent_id": "0",
            "modified": "2020-05-26 15:04:19",
            "created": "2020-05-26 15:04:19",
            "creator": "v_xuanfang",
            "modifier": "v_xuanfang",
            "sorting": "0"
        }
    },
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
