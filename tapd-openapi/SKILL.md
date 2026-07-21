---
name: tapd-openapi
description: TAPD OpenAPI 调用。用于需求、缺陷、任务、评论、测试用例、迭代、评论、Wiki、工时、附件、用户等 TAPD 平台操作。只要用户消息中出现 `https://www.tapd.cn` 或任意 `tapd.cn` 域名链接（需求 / 缺陷 / 任务 / 迭代 / Wiki 等实体页），自动触发本 skill 并按需联动 `tapd-addcomment`、`tapd-cli`；执行任何 TAPD 动作前必须先做环境预检，`TAPD_TOKEN` 未配置时阻断 TAPD 任务并提示用户如何配置 env。
allowed-tools: Bash,Read,Glob,Grep
---

# TAPD OpenAPI Skill

## 触发规则（tapd.cn 链接自动触发）

- 用户消息中出现 `https://www.tapd.cn` 或任意 `tapd.cn` 链接时，自动命中本 skill，不需要用户额外说“用 TAPD skill”；写评论场景联动 `tapd-addcomment`，终端批量脚本场景联动 `tapd-cli`。
- 从链接解析定位信息：`{TAPD_SITE_URL}/tapd_fe/{workspace_id}/{module}/detail/{id}`（story→需求、bug→缺陷、task→任务、iteration→迭代），优先走 OpenAPI 查询实体数据，而不是用浏览器打开页面。
- 仅当 API 无法覆盖需求（如需要页面截图、富文本渲染确认、人工登录操作）时，才回退到浏览器链路（`authenticated-url-routing-rules`）。

## 环境预检（强制，未配置即阻断）

命中本 skill 后、调用任何 TAPD API 前，必须先做一次环境预检：

1. 检查 `TAPD_TOKEN` 是否已注入且非空（只判断有无，**禁止回显 Token 明文**），同时检查 `TAPD_API_ENDPOINT`、`TAPD_WORKSPACE_IDS`。
2. `TAPD_TOKEN` 为空或未注入 → **阻断当前 TAPD 任务**（其他非 TAPD 任务不受影响），并向用户输出以下配置指引：
   - 打开项目级配置 `./.codex/config.toml`（缺失时按 `mcp-installation-rules` 的 TAPD 安装规则创建），在 `[shell_environment_policy.set]` 段填写：
     - `TAPD_TOKEN`：登录 TAPD 开放平台 `https://www.tapd.cn/open_platform/open_api_redirect` 获取个人 API Token 后填入
     - `TAPD_WORKSPACE_IDS`：TAPD 项目 ID 列表，逗号分隔（取自 TAPD 项目 URL 中的数字段）
     - `TAPD_API_ENDPOINT = "https://api.tapd.cn"`、`TAPD_SITE_URL = "https://www.tapd.cn"` 保持默认
   - 填写完成后重启 Codex 会话，环境变量才会注入生效。
3. `TAPD_TOKEN` 已配置但 `TAPD_WORKSPACE_IDS` 为空 → 不阻断，但提示用户补齐；若链接中可解析出 workspace_id，可用该值继续本次调用。
4. 预检通过后首个 API 调用若返回鉴权失败，按下方「失败处理」执行，不重复预检。

## 环境变量

调用 API 时**直接引用环境变量**，禁止硬编码：

| 变量 | 用途 |
|------|------|
| `TAPD_API_ENDPOINT` | API 唯一端点 |
| `TAPD_TOKEN` | Bearer Token（**禁止泄露**） |
| `TAPD_WORKSPACE_IDS` | 项目 ID 列表（逗号分隔），**优先使用** |
| `TAPD_WORKSPACE_ID` | 单个项目 ID（兼容旧配置，`TAPD_WORKSPACE_IDS` 为空时降级） |
| `TAPD_SITE_URL` | 前端站点域名（拼实体链接用） |
| `TAPD_ENTRY_TYPE` | 当前实体类型 |
| `TAPD_ENTRY_ID` | 当前实体 ID |
| `TAPD_COMMENT_ID` | 触发评论 ID |
| `TAPD_COMMENT_ROOT_ID` | 根评论 ID |
| `TAPD_NPC_ROLE` | NPC 登录名（写评论时作为 `author`） |
| `TAPD_USER_NAME` | 触发用户名 |
| `TAPD_CONTEXT` | 上下文链接/描述（若有） |

## 调用方式

```bash
# Workspace 列表（多个时需逐一调用再汇总）
WS_LIST=${TAPD_WORKSPACE_IDS:-$TAPD_WORKSPACE_ID}

# GET
curl -s -H "Authorization: Bearer $TAPD_TOKEN" \
  "${TAPD_API_ENDPOINT}/{path}?workspace_id={id}&其他参数"

# POST（表单，推荐用于含 HTML 的字段如评论）
curl -s -X POST -H "Authorization: Bearer $TAPD_TOKEN" \
  --data-urlencode "workspace_id={id}" \
  --data-urlencode "其他参数=值" \
  "${TAPD_API_ENDPOINT}/{path}"

# POST（JSON）
curl -s -X POST -H "Authorization: Bearer $TAPD_TOKEN" \
  -H "Content-Type: application/json" \
  "${TAPD_API_ENDPOINT}/{path}" -d '{"workspace_id":"{id}",...}'

# 查看详细参数（按需查阅，只 cat 当前任务需要的文档）
cat ./references/{模块}/{文件名}.md
```

## 关键规则

1. **优先 python3**（标准库 + requests）；禁止含 `#` 注释的多行 shell 赋值脚本
2. **评论必须 HTML**：`description` 用 `<p>内容</p>` 格式，Markdown 不会渲染；GET `/comments` 是查询，POST 是写入，**不可混用**
3. **写评论带齐参数**（高频操作，直接复制使用）：
```bash
curl -s -X POST -H "Authorization: Bearer $TAPD_TOKEN" \
  --data-urlencode "workspace_id=$(echo $TAPD_WORKSPACE_IDS | cut -d',' -f1)" \
  --data-urlencode "entry_type=$TAPD_ENTRY_TYPE" \
  --data-urlencode "entry_id=$TAPD_ENTRY_ID" \
  --data-urlencode "root_id=$TAPD_COMMENT_ROOT_ID" \
  --data-urlencode "reply_id=$TAPD_COMMENT_ID" \
  --data-urlencode "author=$TAPD_NPC_ROLE" \
  --data-urlencode "description=<p>这里填写回复内容（HTML格式）</p>" \
  "$TAPD_API_ENDPOINT/comments"
```

4. **生成文件必须上传**：`POST /files/upload_attachment`，用户无法访问本地文件系统
5. **实体链接**：`$TAPD_SITE_URL/tapd_fe/{项目ID}/{module}/{action}/{ID}`（需求→story/detail、缺陷→bug/detail、任务→task/detail、迭代→iteration/card）

## 失败处理

接口最多 **2 次**（原始 + 1 次降级），禁止反复重试：

1. GET 失败 → 探测：`curl -s -H "Authorization: Bearer $TAPD_TOKEN" $TAPD_API_ENDPOINT/users/info`
2. 探测也失败 → Token 无效，告知用户
3. 探测成功 + GET 返回 `invalid request_name` → POST 同一端点（仅传 `workspace_id` + `id`）
4. POST 也失败 → 说明无法读取，基于已知上下文尽力完成

---

## API 索引

下表中 **文档** 列为相对路径，基于 `./references/` 目录。调用前用 `cat` 查看对应文档获取完整参数：

```bash
# 示例：查看"写评论"接口的参数说明
cat ./references/comments/addcomment.md
```

> **快速定位**：创建→`add*`/`create*` | 查询→`list*`/`get*` | 统计→`count*` | 更新→`update*` | 删除→`delete*`/`remove*` | 字段候选值→`*fields_info`

### 一、stories（需求）

| 方法 | 路径 | 功能 | 文档 |
|------|------|------|------|
| GET | `/stories` | 查询需求列表 | `stories/liststories.md` |
| GET | `/stories/count` | 统计需求数量 | `stories/countstories.md` |
| POST | `/stories` | 创建需求 | `stories/addstory.md` |
| POST | `/stories` | 更新需求（需传 id） | `stories/updatestory.md` |
| GET | `/stories/get_fields_info` | 获取字段及候选值 | `stories/getstoryfieldsinfo.md` |
| GET | `/stories/get_related_bugs` | 获取关联缺陷 | `stories/getrelatedbugs.md` |
| POST | `/stories/add_story_link_relations` | 创建需求关联关系 | `stories/addstorylinkrelations.md` |

### 二、bugs（缺陷）

| 方法 | 路径 | 功能 | 文档 |
|------|------|------|------|
| GET | `/bugs` | 查询缺陷列表 | `bugs/listbugs.md` |
| GET | `/bugs/count` | 统计缺陷数量 | `bugs/countbugs.md` |
| POST | `/bugs` | 创建缺陷 | `bugs/addbug.md` |
| POST | `/bugs` | 更新缺陷（需传 id） | `bugs/updatebug.md` |
| GET | `/bugs/get_fields_info` | 获取字段及候选值 | `bugs/getbugfieldsinfo.md` |

### 三、tasks（任务）

| 方法 | 路径 | 功能 | 文档 |
|------|------|------|------|
| GET | `/tasks` | 查询任务列表 | `tasks/listtasks.md` |
| GET | `/tasks/count` | 统计任务数量 | `tasks/counttasks.md` |
| POST | `/tasks` | 创建任务 | `tasks/addtask.md` |
| POST | `/tasks` | 更新任务（需传 id） | `tasks/updatetask.md` |

### 四、iterations（迭代）

| 方法 | 路径 | 功能 | 文档 |
|------|------|------|------|
| GET | `/iterations` | 查询迭代列表 | `iterations/listiterations.md` |

### 五、tcases（测试）

> tcases 文档有精简版（如 `addtcase.md`）和原始版（如 `add_tcase.md`），**优先用精简版**。

#### 5.1 用例 CRUD

| 方法 | 路径 | 功能 | 文档 | 原始版 |
|------|------|------|------|--------|
| GET | `/tcases` | 查询用例列表 | `tcases/listtcases.md` | `tcases/get_tcases.md` |
| GET | `/tcases/count` | 统计用例数量 | `tcases/counttcases.md` | `tcases/get_tcases_count.md` |
| POST | `/tcases` | 创建用例 | `tcases/addtcase.md` | `tcases/add_tcase.md` |
| POST | `/tcases/batch_save` | 批量创建（≤200条/次） | `tcases/batchaddtcases.md` | `tcases/batch_add_tcase.md` |
| POST | `/tcases` | 更新用例（需传 id） | `tcases/updatetcase.md` | `tcases/update_tcase.md` |
| GET | `/tcases/get_fields_info` | 获取字段及候选值 | — | `tcases/get_tcase_fields_info.md` |
| GET | `/tcases/get_custom_fields_settings` | 自定义字段配置 | — | `tcases/get_tcase_custom_fields_settings.md` |
| GET | `/tcases/get_tcase_result` | 用例执行结果 | — | `tcases/get_tcase_result.md` |
| GET | `/tcases/get_story_by_tcase_id` | 用例关联的需求 | — | `tcases/get_story_by_tcase_id.md` |
| GET | `/bugs/get_bug_link_tcase` | 缺陷关联的用例 | — | `tcases/get_bug_link_tcase.md` |

#### 5.2 用例目录

| 方法 | 路径 | 功能 | 文档 | 原始版 |
|------|------|------|------|--------|
| GET | `/tcase_categories` | 查询目录列表 | `tcases/listtcasecategories.md` | `tcases/get_tcase_categories.md` |
| GET | `/tcase_categories/count` | 统计目录数量 | — | `tcases/get_tcase_categories_count.md` |
| GET | `/tcases/count_by_categories` | 目录下用例数（含子目录） | — | `tcases/count_by_categories.md` |
| POST | `/tcase_categories` | 创建目录 | `tcases/addtcasecategory.md` | `tcases/add_tcase_category.md` |

#### 5.3 测试计划

| 方法 | 路径 | 功能 | 文档 | 原始版 |
|------|------|------|------|--------|
| GET | `/test_plans` | 查询计划列表 | `tcases/listtestplans.md` | `tcases/get_test_plans.md` |
| GET | `/test_plans/count` | 统计计划数量 | `tcases/counttestplans.md` | `tcases/get_test_plans_count.md` |
| POST | `/test_plans` | 创建计划 | `tcases/addtestplan.md` | `tcases/add_test_plan.md` |
| POST | `/test_plans` | 更新计划（需传 id） | `tcases/updatetestplan.md` | `tcases/update_test_plan.md` |
| GET | `/test_plans/get_fields_info` | 计划字段及候选值 | — | `tcases/get_test_plan_fields_info.md` |
| GET | `/test_plans/details` | 计划测试结果 | — | `tcases/get_test_plan_details.md` |
| GET | `/test_plans/progress` | 计划执行进度 | — | `tcases/get_test_plan_progress.md` |
| GET | `/test_plans/get_test_plan_bugs` | 计划关联 Bug | — | `tcases/get_test_plan_bugs.md` |
| GET | `/test_plans/get_relative_stories` | 计划关联需求 | — | `tcases/get_test_plan_relative_stories.md` |
| GET | `/test_plans/get_test_plan_tcases` | 计划关联用例 | — | `tcases/get_test_plan_tcases.md` |
| GET | `/test_plans/get_by_iteration_id` | 按迭代查计划 | — | `tcases/get_by_iteration_id.md` |

#### 5.4 计划关联 & 执行

| 方法 | 路径 | 功能 | 文档 | 原始版 |
|------|------|------|------|--------|
| POST | `/test_plans/create_story_relation` | 关联需求（≤10条） | `tcases/createstoryrelation.md` | `tcases/create_story_relation.md` |
| POST | `/test_plans/create_tcase_relation` | 关联用例（≤10条） | `tcases/createtcaserelation.md` | `tcases/create_tcase_relation.md` |
| POST | `/test_plans/delete_story_relation` | 解除需求关联 | — | `tcases/delete_story_relation.md` |
| POST | `/test_plans/delete_tcase_story_relation` | 移出用例并解除关联 | — | `tcases/delete_tcase_story_relation.md` |
| POST | `/tcase_instance/remove` | 移出用例 | — | `tcases/remove_tcase_instance.md` |
| POST | `/tcase_instance/assign` | 分配执行人 | — | `tcases/assign_tcase_instance.md` |
| POST | `/tcase_instance/execute` | 执行用例（≤10条） | — | `tcases/execute_tcase_instance.md` |

#### 5.5 文件导入批量创建

从 XMind/Excel 批量导入测试用例的流程：

1. **获取源文件**：用户提供或从实体附件获取（附件接口可能延迟，间隔30s重试3次）
2. **解析为 JSON**：
   - XMind: `python3 references/tcases/scripts/parse_xmind_tcases.py <file> -w $TAPD_WORKSPACE_ID -f output.json`
   - Excel: `python3 references/tcases/scripts/parse_excel_tcases.py <file> -w $TAPD_WORKSPACE_ID -f output.json`
3. **匹配目录**：通过 `listtcasecategories` 查询已有目录，按 `category_path` 匹配或创建 `category_id`
4. **批量提交**：`POST /tcases/batch_save`（每批≤200条），详见 `tcases/batchaddtcases.md`

需求与用例关联：详见 `stories/addstorylinkrelations.md`

---

### 六、comments（评论）

| 方法 | 路径 | 功能 | 文档 |
|------|------|------|------|
| GET | `/comments` | 查询评论列表 | `comments/listcomments.md` |
| GET | `/comments/count` | 统计评论数量 | `comments/countcomments.md` |
| POST | `/comments` | 添加评论（支持@和回复） | `comments/addcomment.md` |

> 评论内容须用 HTML 富文本（如 `<p>内容</p>`）。`entry_type`: bug / bug_remark / stories / tasks。

### 七、wikis（Wiki）

| 方法 | 路径 | 功能 | 文档 |
|------|------|------|------|
| GET | `/tapd_wikis` | 查询 Wiki 列表 | `wikis/listwikis.md` |
| GET | `/tapd_wikis/count` | 统计 Wiki 数量 | `wikis/countwikis.md` |
| POST | `/tapd_wikis` | 创建 Wiki | `wikis/addwiki.md` |
| POST | `/tapd_wikis` | 更新 Wiki（需传 id） | `wikis/updatewiki.md` |
| — | 本地脚本 | Wiki 全文搜索 | `wikis/searchwiki.md` |

**Wiki 搜索**（TAPD API 不支持全文搜索，通过本地脚本实现）：
```bash
python3 ./scripts/search_wiki.py sync           # 同步到本地
python3 ./scripts/search_wiki.py search 关键词   # 搜索（多词取交集）
```

### 八、timesheets（工时）

| 方法 | 路径 | 功能 | 文档 |
|------|------|------|------|
| GET | `/timesheets` | 查询工时列表 | `timesheets/listtimesheets.md` |
| GET | `/timesheets/count` | 统计工时数量 | `timesheets/counttimesheets.md` |
| POST | `/timesheets` | 新建工时 | `timesheets/addtimesheet.md` |
| POST | `/timesheets` | 更新工时（需传 id） | `timesheets/updatetimesheet.md` |

> 同一 entity_type + entity_id + spentdate + owner 只允许一条记录。

### 九、attachments（附件）

| 方法 | 路径 | 功能 | 文档 |
|------|------|------|------|
| GET | `/attachments` | 查询附件列表 | `attachments/listattachments.md` |
| GET | `/attachments` | 按实体查附件（需传 type + entry_id） | `attachments/getattachmentsbyentity.md` |
| GET | `/attachments/down` | 获取附件下载链接（有效期300s） | `attachments/downloadattachment.md` |
| GET | `/documents/down` | 获取文档下载链接 | `attachments/downloaddocument.md` |
| GET | `/files/get_image` | 获取图片链接（有效期300s） | `attachments/getimage.md` |
| POST | `/files/upload_attachment` | 上传附件（≤250MB） | `attachments/upload_attachment.md` |
| POST | `/files/upload_image` | 上传图片（≤5MB） | `attachments/upload_image.md` |
| POST | `/files/upload_image_base64` | Base64上传图片（≤15MB） | `attachments/upload_image_base64.md` |

### 十、users（用户）

| 方法 | 路径 | 功能 | 文档 |
|------|------|------|------|
| GET | `/users/info` | 获取当前用户信息 | `users/getuserinfo.md` |
| GET | `/open_user_app/workspace_list` | 获取可访问的项目列表 | `users/listworkspaces.md` |

---

## 辅助脚本

| 脚本 | 用途 |
|------|------|
| `references/tcases/scripts/parse_xmind_tcases.py` | XMind → 测试用例 JSON |
| `references/tcases/scripts/parse_excel_tcases.py` | Excel → 测试用例 JSON |
| `scripts/search_wiki.py` | Wiki 全文搜索 |
