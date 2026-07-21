[[toc]]

# 说明
通过API上传单个附件，业务对象支持需求、缺陷、任务，大小上限限制250MB。

<env-ctrl env="oa">
<div>

<!-- @include: docs/next-tool-doc/SDK/TAPD SDK/sdk函数名.md -->

</div>
</env-ctrl>

# url
`{{ $page.apiHost }}/files/upload_attachment`

# 支持格式
JSON/XML（默认JSON格式）

#  HTTP请求方式
POST

# 请求数限制
- 每次只允许上传一个文件
- 文件大小限小于250MB
- 支持需求、缺陷、任务

# 请求参数
<env-ctrl env="oa">
<div>

|字段名|必选|类型及范围|说明|
|:----:|:----:|:----:|:----:|
|workspace_id| `是` | integer | 项目ID |
|file|`是`|文件| 文件 |
|type|`是`|string| story/bug/task |
|entry_id|`是`|integer| 需求/缺陷/任务id |
|owner|否|string| 附件创建人 |
|overwrite|否|int| 是否同名覆盖。取值：0 不覆盖，1 覆盖 |
|custom_field|否|string| 字段英文名（仅用在轻量项目中，并且为必填） |

</div>
</env-ctrl>

<env-ctrl env="cloud">
<div>

|字段名|必选|类型及范围|说明|
|:----:|:----:|:----:|:----:|
|workspace_id| `是` | integer | 项目ID |
|file|`是`|文件| 文件 |
|type|`是`|string| story/bug/task |
|entry_id|`是`|integer| 需求/缺陷/任务id |
|owner|否|string| 附件创建人 |

</div>
</env-ctrl>

# 调用示例及返回结果
## 把本地的 uu.jpg 上传到项目 755
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password'  -F 'workspace_id=755' -F 'type=task' -F 'entry_id=1000000755859140551' -F 'file=@uu.jpg' '{{ $page.apiHost }}/files/upload_attachment'`
### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN'  -F 'workspace_id=755' -F 'type=task' -F 'entry_id=1000000755859140551' -F 'file=@uu.jpg' '{{ $page.apiHost }}/files/upload_attachment'`
### 返回结果
```json
{
    "status": 1,
    "data": {
        "Attachment": {
            "id": "1000000755503455439",
            "type": "task",
            "entry_id": 1000000755859140551,
            "filename": "uu.jpg",
            "description": "",
            "content_type": "image/jpeg",
            "created": "2021-09-07 21:36:08",
            "workspace_id": 755,
            "owner": ""
        }
    },
    "info": "success"
}
```

# 字段说明
## 返回字段说明
|字段|说明|
|:----:|:----:|
| type | 业务对象类型：story/bug/task |
| entry_id | 业务对象的id |
| filename | 文件名 |
| description | 附件描述 |
| content_type | 文件类型 |
| created | 创建时间 |
| workspace_id | 项目id |
| owner | 附件上传人 |
