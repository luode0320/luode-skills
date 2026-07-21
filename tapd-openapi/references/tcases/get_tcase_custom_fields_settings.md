# 说明
获取测试用例自定义字段配置


# url
`${TAPD_API_ENDPOINT}/tcases/custom_fields_settings`

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
## 获取迭代自定义字段配置
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password'  '${TAPD_API_ENDPOINT}/tcases/custom_fields_settings?workspace_id=755'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN'  '${TAPD_API_ENDPOINT}/tcases/custom_fields_settings?workspace_id=755'`

### 返回结果
```JSON
{
    "status": 1,
    "data": [
        {
            "CustomFieldConfig": {
                "id": "1000000755214854654",
                "workspace_id": "755",
                "entry_type": "tcase",
                "custom_field": "custom_field_30",
                "type": "select",
                "name": "AT已实现？",
                "options":"{\"1\":\"\已\实\现\",\"2\":\"\未\实\现\"}",
                "enabled": "1",
                "sort": null,
                "memo": null
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
