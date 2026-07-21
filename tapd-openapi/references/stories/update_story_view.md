# 说明
更新需求视图标题或者视图条件（数据范围）


# url
`${TAPD_API_ENDPOINT}/stories/update_story_view`

# 支持格式
JSON/XML（默认JSON格式）

#  HTTP请求方式
POST

# 请求数限制
- 每次只允许更新一条数据
-

# 请求参数
|字段名|必选|  类型及范围  |     说明     |
|:----:|:----:|:-------:|:----------:|
| workspace_id | `是` | integer |    项目ID    |
| view_conf_id | `是` | integer |    视图ID    |
| search_data | 否 | string  | 视图条件（数据范围），需要转化成json字符串  |
| title | 否 | string  | 视图标题  |


# 调用示例及返回结果
## 更新需求视图  1010104801018689816
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password' -d 'workspace_id=10104801&view_conf_id=1010104801018689816&title=aview&search_data=%7B%22data%22%3A%5B%7B%22id%22%3A2%2C%22fieldDisplayName%22%3A%22%E7%8A%B6%E6%80%81%22%2C%22fieldIsSystem%22%3A1%2C%22fieldOption%22%3A%22in%22%2C%22fieldSystemName%22%3A%22status%22%2C%22fieldType%22%3A%22multi_select%22%2C%22selectOption%22%3A%5B%5D%2C%22value%22%3A%22%24%7Bworkflow_done%7D%7C%E5%AE%9E%E7%8E%B0%E4%B8%AD%7C%E8%A7%84%E5%88%92%E4%B8%AD%22%2C%22entity%22%3A%22story%22%2C%22fieldLabel%22%3A%22%E7%8A%B6%E6%80%81%22%7D%5D%2C%22optionType%22%3A%22AND%22%2C%22needInit%22%3Atrue%7D' '${TAPD_API_ENDPOINT}/stories/update_story_view'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN' -d 'workspace_id=10104801&view_conf_id=1010104801018689816&title=aview&search_data=%7B%22data%22%3A%5B%7B%22id%22%3A2%2C%22fieldDisplayName%22%3A%22%E7%8A%B6%E6%80%81%22%2C%22fieldIsSystem%22%3A1%2C%22fieldOption%22%3A%22in%22%2C%22fieldSystemName%22%3A%22status%22%2C%22fieldType%22%3A%22multi_select%22%2C%22selectOption%22%3A%5B%5D%2C%22value%22%3A%22%24%7Bworkflow_done%7D%7C%E5%AE%9E%E7%8E%B0%E4%B8%AD%7C%E8%A7%84%E5%88%92%E4%B8%AD%22%2C%22entity%22%3A%22story%22%2C%22fieldLabel%22%3A%22%E7%8A%B6%E6%80%81%22%7D%5D%2C%22optionType%22%3A%22AND%22%2C%22needInit%22%3Atrue%7D' '${TAPD_API_ENDPOINT}/stories/update_story_view'`

### 返回结果
```JSON
{
    "status": 1,
    "data": {
        "success": true
    },
    "info": "success"
}
```
