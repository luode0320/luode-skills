# 说明
获取需求自定义字段配置


# url
`${TAPD_API_ENDPOINT}/stories/custom_fields_settings`

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
## 获取需求自定义字段配置
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password'  '${TAPD_API_ENDPOINT}/stories/custom_fields_settings?workspace_id=10104801'`

### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN'  '${TAPD_API_ENDPOINT}/stories/custom_fields_settings?workspace_id=10104801'`

### 返回结果
```JSON
{
    "status": 1,
    "data": [
        {
            "CustomFieldConfig": {
                "id": "1010104801216209053",
                "workspace_id": "10104801",
                "app_id": "1",
                "entry_type": "story",
                "custom_field": "custom_field_17",
                "type": "cascade_radio",
                "name": "联动字段测试",
                "options": "[{\"name\":\"a1\",\"children\":[{\"name\":\"a11\"},{\"name\":\"a12\",\"children\":[{\"name\":\"a123\"}]}]},{\"name\":\"a2\"},{\"name\":\"a3\"}]",
                "extra_config": null,
                "enabled": "1",
                "creator": "",
                "created": "0000-00-00 00:00:00",
                "modified": "0000-00-00 00:00:00",
                "freeze": "0",
                "sort": "0",
                "memo": null,
                "open_extension_id": "",
                "is_out": 0,
                "is_uninstall": 0,
                "app_name": ""
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
| app_id | 检查项 |
| extra_config | 额外配置(颜色信息等) |
| creator | 创建人 |
| created | 创建时间 |
| modified | 最后修改时间 |
| sort | 显示时排序系数 |
| memo | 备注 |
| open_extension_id | 插件扩展字段标识 |
| is_out | 已弃用 |
| is_uninstall | 应用是否安装到当前项目 |
| app_name | 应用名 |
