# 最近会话快照托管区契约

## 托管区边界

`PROJECT_CURRENT.md` 中的最近会话快照托管区由 marker 对 `<!-- BEGIN RECENT PROJECT SESSIONS -->` / `<!-- END RECENT PROJECT SESSIONS -->` 标识。标记必须成对、顺序正确且只出现一次。零个区块时可在文件末尾追加；已有一个区块时只替换区块本身。缺半边、重复、嵌套或逆序标记全部拒绝，原文件保持不变。

## 字段白名单

每条快照从 Codex App 元数据提取，只保留以下字段用于展示：

| 字段 | 来源 | 处理规则 |
|---|---|---|
| `title` | `list_threads` 返回的标题 | 最多 48 个 Unicode 字符，清洗 Markdown/HTML/控制字符，脱敏敏感信息 |
| `summary` | `list_threads` 返回的摘要 | 最多 120 个 Unicode 字符，清洗规则同上，空时回退为"无摘要" |
| `status` | 宿主元数据状态 | 映射为中文：`active`->`活动中`、`idle`->`空闲`、`notLoaded`->`未加载`、未知->`未知` |
| `updatedAt` | 最后更新时间 | 转换为北京时间，格式 `YYYY-MM-DD HH:mm:ss +08:00` |

## 字符与大小限制

- 标题最多 48 个 Unicode 字符。
- 摘要最多 120 个 Unicode 字符；摘要为空时使用固定说明"无摘要"。
- 整个最近会话托管区最多 4,096 个 UTF-8 字节。
- `PROJECT_CURRENT.md` 全文继续硬限制为 51,200 字节；恰好 51,200 允许，51,201 拒绝。

## 脱敏规则

禁止持久化以下字段到快照托管区：

- 会话 ID、线程 ID、`projectId`、`cwd`、`hostId`
- 原始 prompt、完整日志、Agent 回复
- API key、token、密码、Cookie、私钥、连接串
- Windows 绝对附件路径、UNC 路径

标题和摘要必须被清洗以下内容：

1. Markdown 标记字符（`* _ ~ # [ ] ( ) > | \ `）
2. HTML 标签
3. 控制字符（`\x00-\x1f`, `\x7f`）
4. 敏感信息模式（API key 前缀、`sk-` 开头的 token、Base64 长串）
5. Windows 绝对路径（`X:\path\to\...`）

## 锁协议

快照写入必须与任务投影脚本共用锁文件 `.PROJECT_CURRENT.md.lock`：

1. 最多重试 40 次，每次间隔 50ms。
2. 持锁后重新读取 `PROJECT_CURRENT.md` 最新全文。
3. 只替换最近会话托管区（`BEGIN RECENT PROJECT SESSIONS` 到 `END RECENT PROJECT SESSIONS`）。
4. 任务投影托管区（`BEGIN TASK PLAN PROJECTION` 到 `END TASK PLAN PROJECTION`）逐字节保持不变。
5. 使用同目录临时文件 + `flush` + `fsync` + `os.replace` 原子替换。
6. 失败时清理临时文件，原文件保持不变。

## 写入顺序

默认执行模式的任务收口顺序必须为：

1. 任务投影落盘（`task_plan_projection.py write`）
2. 立即调用 `update_plan`
3. 最近会话快照刷新（`sync_recent_project_sessions.py`）

快照刷新不得插入投影落盘与 `update_plan` 之间。

## 非 Codex App 宿主

非 Codex App 宿主：

- 不执行快照写入。
- 不伪造空快照。
- 不清空已有快照。
- 不阻断普通项目任务。
- 只读取已有快照用于上下文。

## 状态格式

快照条目格式为：

```
- YYYY-MM-DD HH:mm:ss +08:00 [状态中文] 标题：摘要
```

示例：

```
- 2026-08-10 14:32:00 +08:00 [活动中] 凭据默认代码持久化：配置凭据来源优先级统一和九个 Skill 修改
- 2026-08-09 22:15:00 +08:00 [空闲] 运行时Mock分离：将runtime Mock从测试Mock中分离并更新目录契约
```

## 错误处理

| 错误条件 | 行为 |
|---|---|
| 半 marker / 重复 marker | 原文件保持不变，报错退出 |
| 非法 UTF-8 | 原文件保持不变，报错退出 |
| 锁获取失败 | 不写入，报错退出 |
| 托管区超限（>4,096 字节） | 先尝试缩短摘要重试；仍超限则报错退出 |
| 全文超限（>51,200 字节） | 原文件保持不变，报错退出 |
| 原子写入失败 | 原文件保持不变，清理临时文件 |
