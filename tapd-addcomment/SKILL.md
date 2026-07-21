---
name: tapd-addcomment
description: TAPD 写评论工具。在需求、缺陷、任务等业务对象下添加评论，支持 Markdown / HTML / 纯文本自动识别，Markdown 自动转 HTML。支持 @提及、回复评论、富文本格式。通过 Python 脚本调用，方便 AI 直接写评论。当用户给出 `tapd.cn` 链接并要求评论 / 回复时随 `tapd-openapi` 自动联动触发；执行前遵守 `tapd-openapi` 的环境预检，`TAPD_TOKEN` 未配置时阻断并提示用户配置 env。
allowed-tools: Bash,Read
---

# TAPD AddComment Skill

在 TAPD 业务对象（需求、缺陷、任务等）下添加一条评论。

## 环境变量

调用前确保以下环境变量已配置：

| 变量 | 必须 | 用途 |
|------|------|------|
| `TAPD_API_ENDPOINT` | 是 | API 端点 |
| `TAPD_TOKEN` | 是 | Bearer Token（**禁止泄露**） |
| `TAPD_WORKSPACE_IDS` | 否 | 项目 ID 列表（逗号分隔），优先使用 |
| `TAPD_WORKSPACE_ID` | 否 | 单个项目 ID（兼容旧配置） |
| `TAPD_ENTRY_TYPE` | 否 | 当前实体类型（stories/bug/bug_remark/tasks） |
| `TAPD_ENTRY_ID` | 否 | 当前实体 ID |
| `TAPD_COMMENT_ID` | 否 | 触发评论 ID（回复时用作 reply_id） |
| `TAPD_COMMENT_ROOT_ID` | 否 | 根评论 ID（回复时用作 root_id） |
| `TAPD_NPC_ROLE` | 否 | NPC 登录名（作为 author） |

## 使用方式

通过 Python 脚本 `scripts/add_comment.py` 调用：

```bash
# 基础用法：添加简单评论（使用环境变量中的默认值）
python3 scripts/add_comment.py --description '<p>这是一条评论</p>'

# ✅ 直接传 Markdown（自动检测并转为 HTML）
python3 scripts/add_comment.py --description '## 分析结果

- 第一点：xxx
- 第二点：xxx

> 总结：**非常好**'

# 从 stdin 读取 Markdown 长文本
cat analysis.md | python3 scripts/add_comment.py --description -

# 完整参数用法
python3 scripts/add_comment.py \
  --workspace-id 12345678 \
  --entry-type stories \
  --entry-id 1131372104001000001 \
  --author username \
  --description '## 代码审查意见

1. `main.go` 第 42 行有潜在空指针
2. 建议增加单元测试

**结论**: 需修改后合入'

# 回复某条评论
python3 scripts/add_comment.py \
  --workspace-id 12345678 \
  --entry-type stories \
  --entry-id 1131372104001000001 \
  --author username \
  --root-id 1131372104001000040 \
  --reply-id 1131372104001000040 \
  --description '<p>这是一条回复</p>'

# 带 @提及 的评论
python3 scripts/add_comment.py \
  --description '<p><b class="at-who" contenteditable="false" data-userid="target_user" data-type="user">@target_user</b> 请看一下</p>'

# 从 stdin 读取评论内容（适合长文本 / 含特殊字符的 HTML）
echo '<p>评论内容</p>' | python3 scripts/add_comment.py --description -
```

## 参数说明

| 参数 | 必选 | 说明 |
|------|------|------|
| `--workspace-id` | 否 | 项目 ID（默认取 `TAPD_WORKSPACE_IDS` 或 `TAPD_WORKSPACE_ID`） |
| `--entry-type` | 否 | 评论类型：`stories` / `bug` / `bug_remark` / `tasks`（默认取 `TAPD_ENTRY_TYPE`） |
| `--entry-id` | 否 | 业务对象实体 ID（默认取 `TAPD_ENTRY_ID`） |
| `--author` | 否 | 评论人（默认取 `TAPD_NPC_ROLE`） |
| `--description` | **是** | 评论内容，**支持 HTML / Markdown / 纯文本**（自动检测格式并转换）；传 `-` 表示从 stdin 读取 |
| `--root-id` | 否 | 根评论 ID（回复评论线程时必填，默认取 `TAPD_COMMENT_ROOT_ID`） |
| `--reply-id` | 否 | 被回复的评论 ID（回复某条评论时必填，默认取 `TAPD_COMMENT_ID`） |

## 关键规则

1. **description 支持三种格式**（自动检测，无需手动指定）：
   - **HTML**：直接使用，如 `<p>内容</p>`
   - **Markdown**：自动转换为 HTML（支持标题、列表、表格、代码块、加粗、斜体、链接等）
   - **纯文本**：自动包裹 `<p>` 标签
2. **Markdown 转换依赖**：使用 `markdown` Python 库（需提前安装：`pip install markdown`），启用表格、围栏代码块、换行转 `<br>` 等扩展
3. **@提及**：在 description 中使用 `<b class="at-who" contenteditable="false" data-userid="用户ID" data-type="user">@用户名</b>` 触发通知（@提及部分请用 HTML 格式）
4. **回复评论**：`root_id` 和 `reply_id` 必须同时提供
   - 回复根评论：`root_id` = `reply_id` = 被回复评论的 ID
   - 回复子评论：`root_id` = 线程根评论 ID，`reply_id` = 被回复的子评论 ID
5. **支持的 HTML 标签**：`<b>` 加粗、`<i>` 斜体、`<u>` 下划线、`<s>` 删除线、`<span style="color:red;">` 颜色、`<ul><li>` / `<ol><li>` 列表、`<pre><code>` 代码块、`<blockquote>` 引用、`<a href>` 链接、`<table>` 表格
