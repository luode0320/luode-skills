# SCM 提交关键字（get_scm_copy_keywords）

> 归属：`tapd-openapi`。吸收自外部 TAPD skill（`clawhub.ai/kevindai/tapd`）的 SCM 提交关键字能力缺口。

## 获取提交关键字

**请求方法：** GET

**请求地址：** `${TAPD_API_ENDPOINT}/svn_commits/get_scm_copy_keywords`

**请求参数：**

| 参数 | 必填 | 说明 |
|------|------|------|
| workspace_id | 是 | 项目 ID |
| object_id | 是 | 实体长 ID（需先按短 ID 转长 ID 规则转换） |
| type | 是 | 实体类型：story / task / bug |

**请求示例：**

```bash
curl -s -H "Authorization: Bearer $TAPD_TOKEN" \
  "${TAPD_API_ENDPOINT}/svn_commits/get_scm_copy_keywords?workspace_id={id}&object_id={long_id}&type=story"
```

## 通用调用（使用 tapd_client_stdlib.py）

```bash
python3 {baseDir}/scripts/tapd_client_stdlib.py get --endpoint "svn_commits/get_scm_copy_keywords" -p workspace_id={id} -p object_id={long_id} -p type=story
```

## 用途

- 获取需求/缺陷/任务对应的 SCM 提交关键字，用于 git commit message 关联（如 `--story 1112345678001000001`）。
- 注意：`object_id` 需要长 ID，短 ID 必须先转换（见 `id-conversion.md`）。
