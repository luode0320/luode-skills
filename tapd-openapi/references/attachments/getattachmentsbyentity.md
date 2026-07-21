# GetAttachmentsByEntity

## 接口描述
根据传入的实体类型（entity_type）和实体ID（entity_id），查询该实体下的附件列表。支持按缺陷、需求等业务对象查询其关联的附件。

## 请求信息

**请求方法：** GET

**请求地址：** ${TAPD_API_ENDPOINT}/attachments

**支持格式：** JSON/XML（默认 JSON）

**请求数限制：** 默认返回30条，可通过 limit 参数设置，最大200。也可传 page 参数翻页。

### 请求参数

| 参数名 | 必选 | 类型 | 说明 | 特殊规则 |
|--------|------|------|------|----------|
| workspace_id | 是 | integer | 项目ID | |
| type | 是 | string | 业务对象类型，如 `bug`（缺陷）、`story`（需求）、`task`（任务）、`wiki`（文档）等 | |
| entry_id | 是 | integer | 实体ID，即对应的业务对象ID | |
| filename | 否 | string | 附件名称（模糊匹配） | |
| owner | 否 | string | 上传人 | |
| limit | 否 | integer | 返回数量限制，默认30，最大200 | |
| page | 否 | integer | 页码，默认1 |

### type 字段常用值说明

| type 值 | 对应业务对象 |
|---------|-------------|
| bug | 缺陷 |
| story | 需求 |
| task | 任务 |
| wiki | 文档 |
| wiki_description | 文档描述 |
| iteration_report | 迭代报告 |

## 请求示例

### 查询某缺陷下的所有附件

```bash
# 查询缺陷 ID=1010148010001000011 下的附件
curl -H 'Authorization: Bearer $TAPD_TOKEN' \
  '${TAPD_API_ENDPOINT}/attachments?workspace_id=$TAPD_WORKSPACE_ID&type=bug&entry_id=1010148010001000011'
```

### 查询某需求下的所有附件

```bash
# 查询需求 ID=1010148010001000022 下的附件
curl -H 'Authorization: Bearer $TAPD_TOKEN' \
  '${TAPD_API_ENDPOINT}/attachments?workspace_id=$TAPD_WORKSPACE_ID&type=story&entry_id=1010148010001000022'
```

## 返回示例

```json
{
    "status": 1,
    "data": [
        {
            "Attachment": {
                "id": "1210104801000028203",
                "type": "bug",
                "entry_id": "1010148010001000011",
                "filename": "error_screenshot.png",
                "content_type": "image/png",
                "created": "2021-04-08 15:51:27",
                "workspace_id": "10104801",
                "owner": "zhangsan"
            }
        },
        {
            "Attachment": {
                "id": "1210104801000028204",
                "type": "bug",
                "entry_id": "1010148010001000011",
                "filename": "log_file.txt",
                "content_type": "text/plain",
                "created": "2021-04-08 16:30:00",
                "workspace_id": "10104801",
                "owner": "lisi"
            }
        }
    ],
    "info": "success"
}
```

### 返回字段说明

| 字段 | 说明 |
|------|------|
| id | 附件ID |
| type | 业务对象类型，表示该附件归属的实体类型 |
| entry_id | 业务对象的ID，表示该附件归属的实体ID |
| filename | 附件名称 |
| content_type | 内容类型（MIME类型） |
| created | 创建时间 |
| workspace_id | 项目ID |
| owner | 上传人 |
