[[toc]]


# 说明
以 base64 格式上传图片保存至附件中，大小限制为15MB以内。

# url
`{{ $page.apiHost }}/files/upload_image_base64`

# 支持格式
JSON/XML（默认JSON格式）

#  HTTP请求方式
POST

# 请求数限制
- 每次只允许上传一个图片
- 文件大小限小于15MB

# 请求参数
|字段名|必选|类型及范围|说明|
|:----:|:----:|:----:|:----:|
|workspace_id| `是` | integer | 项目ID |
|base64_data|`是`|string| 图片 base64 格式数据 |
|type|`是`|string| 类型(固定为story_custom_field) |
|entry_id|`是`|integer| 需求ID |
|owner|否|string| 附件创建人 |


# 调用示例及返回结果
## 把本地的 uu.jpg 的 base64 上传到空间 69995768
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password'  -F 'workspace_id=69995768' -F 'type=story_custom_field'  -F 'entry_id=1069995768115415038' -F 'base64_data=xxxxx' '{{ $page.apiHost }}/files/upload_image_base64'`
### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN'  -F 'workspace_id=69995768' -F 'type=story_custom_field'  -F 'entry_id=1069995768115415038' -F 'base64_data=xxxx' '{{ $page.apiHost }}/files/upload_image_base64'`
### 返回结果
```json
{
    "status": 1,
    "data": {
        "Attachment": {
            "id": "1069995768523406033",
            "type": "story_custom_field",
            "entry_id": 1069995768115415038,
            "filename": "tapd_base64_3031935_1701845640.jpg",
            "description": "",
            "content_type": "image/png",
            "created": "2023-12-05 14:54:01"
        }
    },
    "info": "success"
}
```

# 字段说明
## 返回字段说明
|字段|说明|
|:----:|:----:|
| id | 附件id |
| type | 类型(固定为story_custom_field) |
| entry_id | 工作项id |
| filename | 文件名 |
| description | 附件描述 |
| content_type | 文件类型 |
| created | 创建时间 |
