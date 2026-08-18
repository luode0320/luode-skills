# WorkBuddy 宿主会话标题契约

本契约约束 `thread-title-rules` 在 WorkBuddy Desktop 宿主（`CODEBUDDY_HOST=workbuddy-desktop`）上的会话标题写入。它与 [rename-tool-contract.md](rename-tool-contract.md) 描述的 Codex MCP 路径互斥分流：**同一轮只走一条宿主路径**，两条路径共享同一套标题生成规则与跳过条件。

## 背景：为什么需要本契约

WorkBuddy Desktop 未暴露 `rename_current_thread` / `set_thread_title` 等会话重命名 MCP 工具（官方文档亦无重命名 API），因此 Codex 专属的统一 MCP 工具在 WorkBuddy 宿主静默不可用。但 WorkBuddy 原生在 `~/.workbuddy/workbuddy.db` 的 `sessions` 表中持久化会话标题（`title` 自动生成、`custom_title` 自定义），且该标题**不是每轮实时更新**——实测会话创建后标题保持早期摘要，说明本地主动写入有实际价值且不会被立即覆盖。本契约定义该原生存储上的安全写入方式。

## 宿主检测

按以下顺序判定当前宿主为 WorkBuddy：

1. 环境变量 `CODEBUDDY_HOST` 等于 `workbuddy-desktop`。
2. 或 `WORKBUDDY_CONFIG_DIR` / `CODEBUDDY_CONFIG_DIR` 存在且指向的目录内含 `workbuddy.db`。
3. 或 `WORKBUDDY_APP_VERSION` 存在。

任一命中即走本契约路径。不得仅凭模型名称（GPT / Claude / 其他）推断宿主。

## 当前会话身份

按以下顺序解析可信会话 ID，**禁止通过线程列表、路径、最近更新时间、标题相似度猜测**：

1. 环境变量 `CODEBUDDY_MCP_CONFIG` 中 `mcpServers.*.headers["X-WorkBuddy-Session-Id"]`（由宿主注入的可信元数据）。
2. 同一环境变量中的 UUID 兜底正则（仅当 JSON 结构解析失败时）。
3. 调用方显式传入 `--session-id`（子代理 / 自动化场景）。

解析结果必须是合法 UUID 格式。多个非空来源不一致时，以宿主注入（第 1 项）为准；无法可靠确定时显式跳过。

> 安全细节：`CODEBUDDY_MCP_CONFIG` 同时携带 `Authorization: Bearer <token>`。**任何路径都不得打印该环境变量全文或 token 原值**；脚本只提取会话 ID。本契约的会话 ID 是宿主身份元数据而非授权凭据，不提供跨用户隔离。

## 存储与字段语义

- 存储：`$WORKBUDDY_CONFIG_DIR/workbuddy.db`（`WORKBUDDY_CONFIG_DIR` > `CODEBUDDY_CONFIG_DIR` > `~/.workbuddy` 依次解析）。
- 表：`sessions`。
- 字段：
  - `title` —— **自动摘要槽（主进程独占）**。由 WorkBuddy 主进程基于会话内容自动生成并回写；agent 直接写入会被主进程内存回写覆盖（已实测），**禁止作为改名目标**，仅作诊断读取。
  - `custom_title` —— **用户改名槽（本 skill 默认写入）**。语义等同 UI「重命名」修改任务名；主进程不主动改写，写入后可存活。UI 显示优先级 `custom_title` > `title`。
- 会话必须存在且 `deleted_at IS NULL`；`updated_at` 随写入刷新为当前毫秒时间戳。

## 写入方式

统一经 `workbuddy/rename-session.py` 执行，禁止在主回复正文中伪造工具调用结果：

```bash
python thread-title-rules/workbuddy/rename-session.py --check                     # 只读探测（子代理检测用）
python thread-title-rules/workbuddy/rename-session.py --title "新标题"            # 写 custom_title 用户改名槽（默认）
python thread-title-rules/workbuddy/rename-session.py --title "新标题" \
  --expect-old "旧标题"                                                           # 原子保护（写入前重查）
```

脚本契约（与 `mcp/bootstrap.mjs` 同风格）：

- 幂等：同一标题重复写入安全，不产生重复副作用。
- 备份：写入前用 sqlite backup API（WAL 安全）整库备份到 `workbuddy.db.bak-<时间戳>`；备份文件与既有文件重名时拒绝写入。备份保留，可手动清理。
- 原子保护：`--expect-old` 传入调用方读取到的旧标题；写入前重查发现标题已被其他方修改则拒绝覆盖并返回 `title_changed_since_read`。
- 回读校验：UPDATE 后 `SELECT` 回读，`verified:true` 才视为成功；`rowcount=0` 或回读不一致按失败处理。
- 输出：稳定 JSON `{ok, mode, sessionId, field, oldTitle, newTitle, backupPath, verified}`；失败时 `{ok:false, error, ...}` 且退出码非 0。
- 只写单行单字段：不删行、不触碰其他表、不修改其他字段。

## 成功 / 失败路由

| 结果 | Skill 动作 |
| --- | --- |
| `ok:true, verified:true` | 输出 `会话标题: 已通过 WorkBuddy 原生存储重命名为「标题」`，停止路由 |
| `title_changed_since_read` | 按并发保护跳过，不强制覆盖；说明原因后继续主任务 |
| `session_not_found` | 会话 ID 不可信或已删除，显式跳过，禁止猜测其他会话 |
| `session_id_unavailable` | 宿主未注入会话 ID，显式跳过并说明 |
| `db_not_found` / 备份失败 / 其他 | 记录失败原因，继续主任务（标题失败不阻断研发任务） |

## 失败降级（吸收自外部 hook）

仅当能**可靠取得当前会话首条用户消息文本**时，允许把标题降级为"截断后的首条用户消息"（截断到 40 字内并去除换行）：此时 `--title` 传截断结果。无法可靠取得消息文本时**不得编造**，直接显式跳过。降级结果写入同一 `custom_title` 槽位。

## 安全与兼容边界

- 只写本机 WorkBuddy 会话元数据；不修改项目文件、不修改 Codex 配置、不做 UI 模拟点击。
- 不打印 `CODEBUDDY_MCP_CONFIG` 全文 / token；日志与输出只含会话 ID 与标题。
- App 运行中写入依赖 SQLite 多进程并发（WAL）；UI 列表可能不实时刷新，重开会话 / 下次会话列表刷新后可见，如实说明即可。
- 同一轮内 Codex MCP 路径与 WorkBuddy 原生路径互斥：工具已暴露时优先走 MCP，绝不双写。
- 本契约只解决"把当前 WorkBuddy 会话标题改成给定标题"，不负责判断何时改名、不允许选择其他会话。
