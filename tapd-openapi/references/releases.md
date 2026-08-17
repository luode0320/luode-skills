# Releases（发布计划）

> 归属：`tapd-openapi`。吸收自外部 TAPD skill（`clawhub.ai/kevindai/tapd`）的发布计划能力缺口。

## 查询发布计划列表

**请求方法：** GET

**请求地址：** `${TAPD_API_ENDPOINT}/releases`

**请求参数：**

| 参数 | 必填 | 说明 |
|------|------|------|
| workspace_id | 是 | 项目 ID |
| id | 否 | 发布计划 ID |
| name | 否 | 名称筛选 |
| startdate / enddate | 否 | 起止日期筛选 |
| page / limit | 否 | 分页（默认 limit 30） |

**请求示例：**

```bash
curl -s -H "Authorization: Bearer $TAPD_TOKEN" \
  "${TAPD_API_ENDPOINT}/releases?workspace_id={id}&limit=30"
```

## 通用调用（使用 tapd_client_stdlib.py）

```bash
# 获取发布计划列表（脚本已内置 releases 子命令）
python3 {baseDir}/scripts/tapd_client_stdlib.py releases --workspace-id {id} [--limit 30] [--page 1]

# 通用 GET（任意筛选）
python3 {baseDir}/scripts/tapd_client_stdlib.py get --endpoint "releases" -p workspace_id={id} -p name=某版本
```

## 用途

- 资源规划与容量预测：查询各发布计划的排期与范围。
- 需求关联发布计划：配合需求字段 `release_id` 理解需求归属版本。
- 生成发布报告：按发布计划聚合需求/缺陷/工时数据。
