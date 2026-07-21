# 说明
返回视图下最新的30条需求（分页显示，默认一页30条）


# url
`${TAPD_API_ENDPOINT}/stories/get_stories_by_view_conf_id`

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
| 需求字段 | 否 | string | 需求字段均可参与基于视图的二次过滤。具体字段及规则可以参考：[获取需求](/api-doc/API文档/api_reference/story/get_stories.html) | |
| limit | 否 | integer | 设置返回数量限制，默认为30 | |
| page | 否 | integer | 返回当前数量限制下第N页的数据，默认为1（第一页）| |
| fields | 否 | string | 设置获取的字段，多个字段间以','逗号隔开 | |

# 调用示例及返回结果
## 获取项目下的需求数据
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password'  '${TAPD_API_ENDPOINT}/stories/get_stories_by_view_conf_id?view_conf_id=1010104801030259563&workspace_id=10104801'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN'  '${TAPD_API_ENDPOINT}/stories/get_stories_by_view_conf_id?view_conf_id=1010104801030259563&workspace_id=10104801'`

### 返回结果
```JSON
{
    "status": 1,
    "data": [
        {
            "Story": {
                "id": "1010104801855983211",
                "name": "sss1",
                "priority": "",
                "status": "developing",
                "owner": "anyechen;",
                "iteration_id": "1010104801000708781",
                "begin": "2022-05-01",
                "due": "2022-05-31",
                "progress": "0"
            }
        },
        {
            "Story": {
                "id": "1010104801855713221",
                "name": "adadf",
                "priority": "",
                "status": "planning",
                "owner": "davidning;anyechen;",
                "iteration_id": "1010104801000708781",
                "begin": "2022-05-01",
                "due": "2022-05-31",
                "progress": "0"
            }
        }
    ],
    "info": {
        "total": 90,
        "current_page": 1,
        "page_size": 30,
        "total_page": 3
    }
}
```

## 获取视图 1010104801030259563 的数据，并根据创建时间过滤出 2024 之后的需求
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password'  '${TAPD_API_ENDPOINT}/stories/get_stories_by_view_conf_id?view_conf_id=1010104801030259563&workspace_id=10104801&created=>2024-01-01'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN'  '${TAPD_API_ENDPOINT}/stories/get_stories_by_view_conf_id?view_conf_id=1010104801030259563&workspace_id=10104801&created=>2024-01-01'`

### 返回结果
```json
{
    "status": 1,
    "data": [
        {
            "Story": {
                "id": "1010104801855983211",
                "name": "sss1",
                "priority": "",
                "status": "developing",
                "owner": "anyechen;",
                "iteration_id": "1010104801000708781",
                "begin": "2022-05-01",
                "due": "2022-05-31",
                "progress": "0"
            }
        }
    ],
    "info": {
        "total": 1,
        "current_page": 1,
        "page_size": 1,
        "total_page": 1
    }
}
```


# 需求字段说明
## 需求重要字段说明
|字段|说明|
|:----:|:----:|
| id | ID |
| name | 标题 |
| priority | 优先级 |
| business_value | 业务价值 |
| status | 状态 |
| version | 版本 |
| module | 模块 |
| feature | 特性 |
| test_focus | 测试重点 |
| size | 规模 |
| owner | 处理人 |
| cc | 抄送人 |
| creator | 创建人 |
| developer | 开发人员 |
| begin | 预计开始 |
| due | 预计结束 |
| created | 创建时间 |
| modified | 最后修改时间 |
| completed | 完成时间 |
| iteration_id | 迭代ID |
| template_id | 模板ID |
| effort | 预估工时 |
| effort_completed | 完成工时 |
| remain | 剩余工时 |
| exceed | 超出工时 |
| category_id | 需求分类 |
| release_id | 发布计划 |
| is_archived | 是否归档 |
| source | 来源 |
| type | 类型 |
| parent_id | 父需求 |
| children_id | 子需求 |
| description | 详细描述 |
| workspace_id | 项目ID |
| workitem_type_id | 需求类别 |
| confidential | 是否保密 |
| created_from | 需求创建来源（为空时代表web创建） |

## 需求优先级(priority)取值字段说明
|取值|字面值|
|:----:|:----:|
| 4 | High |
| 3 | Middle |
| 2 | Low |
| 1 | Nice To Have |
