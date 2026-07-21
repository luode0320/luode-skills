# 说明
关联缺陷


# url
`${TAPD_API_ENDPOINT}/bugs/link_bugs`

# 支持格式
JSON/XML（默认JSON格式）

#  HTTP请求方式
POST

# 请求数限制
一次返回所有符合条件的值


# 请求参数
|字段名|必选|类型及范围|说明|特殊规则|
|:----:|:----:|:----:|:----:|:----:|
|workspace_id|`是`|integer|项目ID|无|
|bug_id|`是`|integer|19位长度的缺陷ID（原始缺陷）|无|
|relate_bugs|`是`|string|多个bug_id（关联缺陷）使用“，”隔开|无|

# 调用示例及返回结果
## 关联缺陷 1162187798001003385 与其它缺陷1162187798001000128,1162187798001000127,1162187798001000126
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password'  '${TAPD_API_ENDPOINT}/bugs/link_bugs --data '{"workspace_id": 62187798,"bug_id": 1162187798001003385,"relate_bugs":"1162187798001000128,1162187798001000127,1162187798001000126"}'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN'  '${TAPD_API_ENDPOINT}/bugs/link_bugs --data '{"workspace_id": 62187798,"bug_id": 1162187798001003385,"relate_bugs":"1162187798001000128,1162187798001000127,1162187798001000126"}'`

### 返回结果
```JSON
{
    "status": 1,
    "data": true,
    "info": "success"
}
```
