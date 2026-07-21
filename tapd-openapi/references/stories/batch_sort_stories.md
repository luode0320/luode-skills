# 说明
批量排序需求


# url
`${TAPD_API_ENDPOINT}/stories/batch_sort_stories`

# 支持格式
JSON/XML（默认JSON格式）

#  HTTP请求方式
POST

# 请求数限制
- 需求数不能大于 200 个
- 传的需求ID，要在同个父需求下，并且要传这个父需求下所有的需求ID


# 请求参数
|字段名|必选|类型及范围|说明|
|:----:|:----:|:----:|:----:|
| workspace_id | `是` | integer | 项目ID |
| story_ids | `是` | string | 所需修改的需求id, 用英文逗号,隔开 |


# 调用示例及返回结果
## 排序五个需求
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password' -d 'workspace_id=10104801&story_ids=1010104801007103983,1010104801007103981,1010104801007103982,1010104801007103984,1010104801007103985' '${TAPD_API_ENDPOINT}/stories/batch_sort_stories'`
### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN' -d 'workspace_id=10104801&story_ids=1010104801007103983,1010104801007103981,1010104801007103982,1010104801007103984,1010104801007103985' '${TAPD_API_ENDPOINT}/stories/batch_sort_stories'`

### 返回结果
```JSON
{
    "status": 1,
    "data": [
        "1010104801007103983",
        "1010104801007103981",
        "1010104801007103982",
        "1010104801007103984",
        "1010104801007103985"
    ],
    "info": "success"
}
```
