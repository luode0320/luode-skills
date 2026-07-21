# 说明
返回符合查询条件的所有需求类别（分页显示，默认一页30条）


# url
`${TAPD_API_ENDPOINT}/workitem_types`

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
| name | 否 | string | 需求类别名称 | 支持模糊匹配 |
| entity_type | 否 | string | 类别别名 |  |
| english_name | 否 | string | 英文名称 |  |
| workflow_id | 否 | integer | 工作流ID |  |
| status | 否 | integer | 状态 |  |
| created | 否 | datetime | 创建时间 |  |
| creator | 否 | datetime | 创建人 |  |
| modified_by | 否 | datetime | 最后修改人 |  |
| modified | 否 | datetime | 最后修改时间 |  |
| limit | 否 | integer | 设置返回数量限制，默认为30 | |
| page | 否 | integer | 返回当前数量限制下第N页的数据，默认为1（第一页）| |
| order | 否 | string | 排序规则，规则：字段名 ASC或者DESC，然后 urlencode |  如按创建时间逆序：order=created%20desc |
| fields | 否 | string | 设置获取的字段，多个字段间以','逗号隔开 | |

# 调用示例及返回结果
## 获取项目下需求类别
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password'  '${TAPD_API_ENDPOINT}/workitem_types?workspace_id=10104801'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN'  '${TAPD_API_ENDPOINT}/workitem_types?workspace_id=10104801'`

### 返回结果
```JSON
{
    "status": 1,
    "data": [
        {
            "WorkitemType": {
                "id": "1010104801000066691",
                "workspace_id": "10104801",
                "app_id": "1",
                "entity_type": "story",
                "name": "bbbee",
                "english_name": "be",
                "status": "3",
                "color": "#3582fb",
                "workflow_id": "1010104801000050043",
                "children_ids": "|",
                "parent_ids": "",
                "icon": "10104801/icon/1010104801503447605",
                "icon_small": "10104801/icon/1010104801503447607",
                "creator": "anyechen",
                "created": "2021-01-26 16:42:16",
                "modified_by": "anyechen",
                "modified": "2024-01-17 16:03:35",
                "icon_viper": "https://viper.wolf.woa.com/icon/files/10104801/icon/1010104801503447605.png?token=6c47847284f7c6b85cc484c32c07c152f4f2d5afd0229b9a27ad0b83c0cdb01b&version=1705478615",
                "icon_small_viper": "https://viper.wolf.woa.com/icon/files/10104801/icon/1010104801503447607.png?token=3369d6880a360a83ff09377aeea128b2b11804184b7d964f504c49bf75125791&version=1705478615"
            }
        },
        {
            "WorkitemType": {
                "id": "1010104801000037383",
                "workspace_id": "10104801",
                "app_id": "1",
                "entity_type": "story",
                "name": "需求",
                "english_name": "story",
                "status": "3",
                "color": "#3582fb",
                "workflow_id": "1010104801000128627",
                "children_ids": "",
                "parent_ids": "",
                "icon": "",
                "icon_small": "",
                "creator": "TAPD system",
                "created": "2020-11-13 17:02:52",
                "modified_by": "",
                "modified": "2024-01-03 19:56:58",
                "icon_viper": "https://wolf.woa.com//img/workitem_type/default_icon/@2/story.png",
                "icon_small_viper": "https://wolf.woa.com//img/workitem_type/default_icon/@2/story_small.png"
            }
        }
    ],
    "info": "success"
}
```
# 需求类别字段说明
## 需求类别重要字段说明
|字段|说明|
|:----:|:----:|
| id | id |
| workspace_id | 项目ID |
| name | 需求类别名称 |
| entity_type | 类别别名 |
| english_name | 英文名称 |
| workflow_id | 工作流ID |
| children_ids | 允许的子需求类别。为空是允许创建任何类别子需求；为 \| 是不允许创建子需求；其它则为指定类别子需求。 |
| parent_ids | 允许的父需求类别。为空是没限制；其它为必须选择指定类别父需求。 |
| created | 创建时间 |
| creator | 创建人 |
| modified_by | 最后修改人 |
| modified | 最后修改时间 |
| status | 状态 |
| color | 颜色 |
| icon | 图标 |
| icon_small | 大图标地址 |
| icon_viper | 图标地址 |
| icon_small_viper | 小图标地址 |

# 状态说明
| 取值 | 说明 |
|:----:|:----:|
| 1 | 未完成 |
| 2 | 未启用 |
| 3 | 已启用 |
