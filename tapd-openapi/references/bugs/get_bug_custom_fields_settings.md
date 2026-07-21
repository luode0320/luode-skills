# 说明
获取缺陷自定义字段配置


# url
`${TAPD_API_ENDPOINT}/bugs/custom_fields_settings`

# 支持格式
JSON/XML（默认JSON格式）

#  HTTP请求方式
GET

# 请求数限制
一次只能获取一个项目的配置

# 请求参数
|字段名|必选|类型及范围|说明|特殊规则|
|:----:|:----:|:----:|:----:|:----:|
| workspace_id | `是` | integer | 项目ID |  |

# 调用示例及返回结果
## 获取缺陷自定义字段配置
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password'  '${TAPD_API_ENDPOINT}/bugs/custom_fields_settings?workspace_id=10158231'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN'  '${TAPD_API_ENDPOINT}/bugs/custom_fields_settings?workspace_id=10158231'`

### 返回结果
```JSON
{
    "status": 1,
    "data": [
        {
            "CustomFieldConfig": {
                "id": "1010158231077902981",
                "workspace_id": "10158231",
                "entry_type": "bug",
                "custom_field": "custom_field_one",
                "type": "radio",
                "name": "安全漏洞类型",
                "options": "XSS注入|SQL注入|越权",
                "enabled": "1",
                "sort": "1"
            }
        }
    ],
    "info": "success"
}
```

# 返回字段说明
| 字段 | 说明 |
|:----:|:----:|
| id | 自定义字段配置的ID |
| workspace_id | 所属项目ID |
| entry_type | 所属实体对象 |
| custom_field | 自定义字段标识（英文名） |
| type | 输入类型 |
| name | 自定义字段显示名称 |
| options | 自定义字段可选值 |
| enabled | 是否启用 |
| sort | 显示时排序系数 |
