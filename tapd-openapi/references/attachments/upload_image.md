[[toc]]

# 说明
上传图片文件到 TAPD，并返回图片地址。

<env-ctrl env="oa">
<div>

<!-- @include: docs/next-tool-doc/SDK/TAPD SDK/sdk函数名.md -->

</div>
</env-ctrl>

# url
`{{ $page.apiHost }}/files/upload_image`

# 支持格式
JSON/XML（默认JSON格式）

#  HTTP请求方式
POST

# 请求数限制
- 每次只允许上传一张图片
- 文件名后缀仅限 png、gif、jpg、jpeg、bmp
- 文件大小限小于5MB
- 图片仅限在 TAPD 平台上使用（不允许外链）

# 请求参数
|字段名|必选|类型及范围|说明|
|:----:|:----:|:----:|:----:|
| workspace_id | `是` | integer | 项目ID |
|image|`是`|文件| 文件 |

# 调用示例及返回结果
## 把本地的 uu.jpg 上传到项目 755
### curl 使用 Basic Auth 鉴权调用示例
`curl -u 'api_user:api_password'  -F 'workspace_id=755' -F 'image=@uu.jpg' '{{ $page.apiHost }}/files/upload_image'`
### curl 使用 OAuth Access Token 鉴权调用示例
`curl -H 'Authorization: Bearer ACCESS_TOKEN'  -F 'workspace_id=755' -F 'image=@uu.jpg' '{{ $page.apiHost }}/files/upload_image'`
### 返回结果
```json
{
    "status": 1,
    "data": {
        "image_src": "/tfl/pictures/202008/api_755_15982838491369683433.png",
        "html_code": "<img src=\"/tfl/pictures/202008/api_755_15982838491369683433.png\"/>"
    },
    "info": "success"
}
```

# 字段说明
## 返回字段说明
|字段|说明|
|:----:|:----:|
| image_src | 图片地址 |
| html_code | 示例 html 代码 |
