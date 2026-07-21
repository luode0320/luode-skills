# 说明
返回视图下最新的30条缺陷（分页显示，默认一页30条）


# url
`${TAPD_API_ENDPOINT}/bugs/get_bugs_by_view_conf_id`

# 支持格式
JSON/XML（默认JSON格式）

# HTTP请求方式
GET

# 请求数限制
默认返回 30 条。可通过传 limit 参数设置，最大取 200。也可以传 page 参数翻页

# 请求参数
|字段名|必选|类型及范围|说明|特殊规则|
|:----:|:----:|:----:|:----:|:----:|
| view_conf_id | `是` | integer | 视图ID |  |
| workspace_id | `是` | integer | 项目ID |  |
| current_user | 否 | string | 当前登录用户视图 |  |
| limit | 否 | integer | 设置返回数量限制，默认为30 | |
| page | 否 | integer | 返回当前数量限制下第N页的数据，默认为1（第一页）| |
| fields | 否 | string | 设置获取的字段，多个字段间以','逗号隔开 | |

# 调用示例及返回结果
## 获取项目下的缺陷数据
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password'  '${TAPD_API_ENDPOINT}/bugs/get_bugs_by_view_conf_id?view_conf_id=1010104801030259563&workspace_id=10104801'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN'  '${TAPD_API_ENDPOINT}/bugs/get_bugs_by_view_conf_id?view_conf_id=1010104801030259563&workspace_id=10104801'`

### 返回结果
```JSON
{
    "status": 1,
    "data": [
        {
            "Bug": {
                "id": "1010104801084955735",
                "title": "test",
                "version_report": "",
                "severity": "",
                "priority": "",
                "status": "new",
                "current_owner": "",
                "created": "2021-01-21 11:02:09",
                "reporter": "v_xuanfang",
                "resolution": ""
            }
        },
        {
            "Bug": {
                "id": "1010104801083011055",
                "title": "aaa",
                "version_report": "",
                "severity": "",
                "priority": "",
                "status": "new",
                "current_owner": "",
                "created": "2020-10-28 18:28:27",
                "reporter": "v_xuanfang",
                "resolution": ""
            }
        },
        {
            "Bug": {
                "id": "1010104801082968057",
                "title": "aaaa",
                "version_report": "",
                "severity": "",
                "priority": "",
                "status": "in_progress",
                "current_owner": "",
                "created": "2020-10-27 10:14:20",
                "reporter": "v_xuanfang",
                "resolution": ""
            }
        }
    ],
    "info": {
        "total": 13,
        "current_page": 1,
        "page_size": 3,
        "total_page": 5
    }
}
```

# 缺陷字段说明
缺陷字段说明，请参考 [缺陷说明](/api-doc/API文档/api_reference/bug/bug.html)
