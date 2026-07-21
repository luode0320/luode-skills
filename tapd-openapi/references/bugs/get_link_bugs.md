# 说明
获取缺陷与其它缺陷的所有关联关系（无分页）


# url
`${TAPD_API_ENDPOINT}/bugs/get_link_bugs`

# 支持格式
JSON/XML（默认JSON格式）

#  HTTP请求方式
GET

# 请求数限制
一次返回所有符合条件的值


# 请求参数
|字段名|必选|类型及范围|说明|特殊规则|
|:----:|:----:|:----:|:----:|:----:|
|workspace_id|`是`|integer|项目ID|无|
|bug_id|`是`|integer|19位长度的缺陷ID|无|

# 调用示例及返回结果
## 获取缺陷 1010104801086995895 与其它缺陷的所有关联关系
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password'  '${TAPD_API_ENDPOINT}/bugs/get_link_bugs?workspace_id=10104801&bug_id=1010104801086995895'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN'  '${TAPD_API_ENDPOINT}/bugs/get_link_bugs?workspace_id=10104801&bug_id=1010104801086995895'`

### 返回结果
```JSON
{
    "status": 1,
    "data": [
        {
            "type": "repeat",
            "id": "1010104801085894269",
            "workspace_id": "10104801",
            "actas": "target",
            "linked_workspace_id": 10104801,
            "link_id": "1162187798001000534"
        },
        {
            "type": "copy",
            "id": "1010104801085924155",
            "workspace_id": "10104801",
            "actas": "source",
            "linked_workspace_id": 10104801,
            "link_id": "1162187798001000535",
        }
    ],
    "info": "success"
}
```

# 字段说明
## 重要字段说明
|字段|说明|
|:----:|:----:|
|type|关系类型。sync_copy 为 同步复制，copy 为复制，repeat 为重复，direct_relate 为直接关联，sync_relate 为同步重复|
|id|关联的缺陷ID|
|workspace_id|项目ID|
|linked_workspace_id|项目ID|
|actas|角色。target 为操作发起方|
|link_id|bug之间关联关系link的id|
