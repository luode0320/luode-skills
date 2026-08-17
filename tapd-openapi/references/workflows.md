# Workflows（工作流流转）

> 归属：`tapd-openapi`。吸收自外部 TAPD skill（`clawhub.ai/kevindai/tapd`）的工作流能力缺口。用于查询工作流流转规则、状态映射、结束状态与工作项类型。

## 一、工作流流转规则

**请求方法：** GET

**请求地址：** `${TAPD_API_ENDPOINT}/workflows/all_transitions`

**请求参数：**

| 参数 | 必填 | 说明 |
|------|------|------|
| workspace_id | 是 | 项目 ID |
| system | 是 | 工作流系统：story / bug |
| workitem_type_id | 否 | 工作项类型 ID（缺省为默认类型） |

**请求示例：**

```bash
curl -s -H "Authorization: Bearer $TAPD_TOKEN" \
  "${TAPD_API_ENDPOINT}/workflows/all_transitions?workspace_id={id}&system=story"
```

**用途：** 查询某状态下可流转到哪些状态，用于自动化状态流转、判断状态机合法性。

## 二、工作流状态中英文映射

**请求方法：** GET

**请求地址：** `${TAPD_API_ENDPOINT}/workflows/status_map`

**请求参数：** 同 `all_transitions`（workspace_id / system / workitem_type_id）。

**用途：** 获取状态英文 key 与中文名映射，用于展示与解析状态字段。

## 三、工作流结束状态

**请求方法：** GET

**请求地址：** `${TAPD_API_ENDPOINT}/workflows/last_steps`

**请求参数：**

| 参数 | 必填 | 说明 |
|------|------|------|
| workspace_id | 是 | 项目 ID |
| system | 是 | 工作流系统：story / bug |
| workitem_type_id | 否 | 工作项类型 ID |
| type | 否 | 结束状态类型 |

**用途：** 获取工作流的结束状态（终态），判断需求/缺陷是否已完结。

## 四、工作项类型列表

**请求方法：** GET

**请求地址：** `${TAPD_API_ENDPOINT}/workitem_types`

**请求参数：**

| 参数 | 必填 | 说明 |
|------|------|------|
| workspace_id | 是 | 项目 ID |

**用途：** 获取项目内的工作项类型（如需求、缺陷、任务下的子类型），配合 `workitem_type_id` 使用。

## 通用调用（使用 tapd_client_stdlib.py）

```bash
python3 {baseDir}/scripts/tapd_client_stdlib.py get --endpoint "workflows/all_transitions" -p workspace_id={id} -p system=story
python3 {baseDir}/scripts/tapd_client_stdlib.py get --endpoint "workflows/status_map" -p workspace_id={id} -p system=bug
python3 {baseDir}/scripts/tapd_client_stdlib.py get --endpoint "workflows/last_steps" -p workspace_id={id} -p system=story
python3 {baseDir}/scripts/tapd_client_stdlib.py get --endpoint "workitem_types" -p workspace_id={id}
```
