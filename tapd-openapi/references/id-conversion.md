# ID 转换与请求规范（吸收自外部 TAPD skill）

> 归属：`tapd-openapi`。吸收自外部 TAPD skill（`clawhub.ai/kevindai/tapd`）的短 ID 转长 ID 机制、`?s=mcp` 请求标记与 Basic Auth 备用认证。这些规则在调用部分接口时是必需的，与本地 `TAPD_TOKEN` Bearer 认证互补。

## 一、短 ID 转长 ID（强制，涉及部分接口）

TAPD 部分接口接受短 ID（≤9 位数字），调用前必须转为长 ID：

- 前缀规则：云环境（`TAPD_API_ENDPOINT` / `TAPD_API_BASE_URL` 包含 `api.tapd.cn`）前缀 `11`；私有化部署前缀 `10`。
- 格式：`{prefix}{workspace_id}{id.zfill(9)}`。
  - 示例：workspace_id=123，短 id=456 → `1012300000456`（私有化）或 `1112300000456`（云）。
- 多 ID 逗号分隔时，逐个转换后再用逗号拼接。

**涉及 ID 转换的常见场景：**

| 场景 | 说明 |
|------|------|
| stories / tasks 的 id | 查询与更新需求/任务时 |
| bugs 的 id | 查询与更新缺陷时 |
| comments 的 entry_id | 评论关联实体时 |
| get_scm_copy_keywords 的 object_id | SCM 提交关键字时 |

**Python 标准库实现参考（tapd_client_stdlib.py 内置）：**

```python
def to_long_id(workspace_id: str, short_id: str, base_url: str) -> str:
    prefix = "11" if "api.tapd.cn" in base_url else "10"
    return f"{prefix}{workspace_id}{short_id.zfill(9)}"
```

## 二、`?s=mcp` 请求标记与 `Via` 头

- 所有 TAPD 请求在 base 后追加 `?s=mcp`（若 URL 已有 query 则用 `&s=mcp`）。
- 请求头加 `Via: mcp`。
- 与本地 curl 调用方式兼容：在现有 URL 末尾追加即可。

```bash
# 本地 curl 追加示例（保持 Authorization: Bearer $TAPD_TOKEN）
curl -s -H "Authorization: Bearer $TAPD_TOKEN" -H "Via: mcp" \
  "${TAPD_API_ENDPOINT}/stories?s=mcp&workspace_id={id}"
```

## 三、Basic Auth 备用认证（二选一）

本地默认使用 Bearer Token（`TAPD_TOKEN`）。外部 skill 提供备用认证，仅在无 Token 时使用：

| 认证方式 | Header | 环境变量 |
|------|------|------|
| Bearer（推荐，本地默认） | `Authorization: Bearer <token>` | `TAPD_TOKEN` / `TAPD_ACCESS_TOKEN` |
| Basic（备用） | `Authorization: Basic <base64(user:password)>` | `TAPD_API_USER` + `TAPD_API_PASSWORD` |

```python
# Basic 生成示例（标准库）
import base64
basic = base64.b64encode(f"{user}:{password}".encode()).decode()
# Header: Authorization: Basic {basic}
```

## 四、自定义字段前置检查（强制）

- 使用 `custom_field_*` 查询/更新前，必须先调用对应实体类型的 `custom_fields_settings` 接口获取字段配置（stories / tasks / iterations / tcases）。
- 任务状态仅三种：open（未开始）、progressing（进行中）、done（已完成）；需求状态需通过 `get_workflows_status_map` / `get_stories_fields_info` 获取项目配置。

## 五、安全与权限建议

- Token 建议**最小权限、短期有效**（仅授予所需项目/接口权限），避免高权限长期令牌。
- `BOT_URL` / `TAPD_API_ENDPOINT` 使用前确认指向**可信端点**（TAPD 官方或自建 TAPD、企业微信官方 webhook）。
- 可选加固：沙盒运行脚本，限制网络仅允许访问 TAPD API 与 BOT_URL。
- 凭据一律从环境变量读取，禁止硬编码；过程性输出禁止回显 Token 明文（与本地规则一致）。
