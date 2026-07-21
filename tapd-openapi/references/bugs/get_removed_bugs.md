# 说明
返回符合查询条件的所有回收站中的缺陷


# url
`${TAPD_API_ENDPOINT}/bugs/get_removed_bugs`

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
| id | 否 | integer | 缺陷ID |  |
| creator | 否 | string | 创建人 |  |
| created | 否 | date | 创建时间 |  |
| modified | 否 | date | 删除时间 |  |
| include_all | 否 | string | 取 1 会返回所有删除的缺陷，包括 移动、合并、删除 的 |
| limit | 否 | integer | 设置返回数量限制，默认为30 | |
| page | 否 | integer | 返回当前数量限制下第N页的数据，默认为1（第一页）| |

# 调用示例及返回结果
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password'  '${TAPD_API_ENDPOINT}/bugs/get_removed_bugs?workspace_id=10104801'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN'  '${TAPD_API_ENDPOINT}/bugs/get_removed_bugs?workspace_id=10104801'`

### 返回结果
```JSON
{
    "status": 1,
    "data": [
        {
            "RemovedBug": {
                "id": "1100000755500695186",
                "title": "标题呀阿斯蒂芬你不是分别就开始放缓觉得斯芬克斯地方卡积分看到as艰苦地方阿克苏",
                "reporter": "gobichen",
                "created": "2021-04-22 21:29:41",
                "operation_user": "v_tingtdong",
                "modified": "2021-04-23 11:04:59",
                "removed_comment": "{\"action\":\"delete\"}",
                "type": "delete",
                "new_bug_url": ""
            }
        },
        {
            "RemovedBug": {
                "id": "1100000755500695184",
                "title": "标题呀",
                "reporter": "gobichen",
                "created": "2021-04-22 21:17:13",
                "operation_user": "v_tingtdong",
                "modified": "2021-04-23 10:25:05",
                "removed_comment":"{\"action\":\"merge\",\"comment\":\"\已\经\被\合\并\到 Bug#500695186, \点\击<a href=\\\"http:\\/\\/tiger.oa.com\\/755\\/bugtrace\\/bugs\\/view?bug_id=1100000755500695186\\\">\这\里<\\/a>\查\看\"}",
                "type": "merge",
                "new_bug_url": "http://tiger.oa.com/755/bugtrace/bugs/view?bug_id=1100000755500695186"
            }
        }
    ],
    "info": "success"
}
```

# 回收站字段说明
## 回收站重要字段说明
|字段|说明|
|:----:|:----:|
| id | 缺陷ID |
| title | 标题 |
| reporter | 创建人 |
| created | 创建时间 |
| operation_user | 删除人 |
| modified | 删除时间 |
| removed_comment | 删除附加信息 |
| type | 删除操作类型，取值：delete 删除、move 移动、merge 合并 |
| new_bug_url | 当 type 为 move、merge 时，这个字段会指向新的缺陷链接 |
