# 生命周期与触发契约

## 双条件触发

监督 Skill 的唯一自动触发条件是：

| 条件 | 必须事实 | 不满足时 |
|---|---|---|
| Goal 状态 | 当前 Goal 可确认是 `active` | 退出，不创建状态 |
| 用户意图 | 当前用户消息明确表达“监控代码” | 退出，不扫描 |
| 执行模式 | 当前不是 Plan Mode | 退出，不刷新任务投影 |

“用户之前说过监控代码”、普通代码改动、已有旧状态文件或另一个会话 active，都不能替代当前轮双条件。

## 周期扫描

宿主可以按约 30 秒唤醒监督会话。每次唤醒都必须：

1. 重新确认 Goal active 和当前监督意图仍然有效。
2. 重新读取最新 diff 和 Owner Skill 文件。
3. 重新计算 Owner 路由和 finding fingerprint。
4. 先写入脱敏状态，再发送通知；任一步失败都不得宣称全链路成功。

脚本不负责睡眠、调度、Goal 创建、`update_plan` 或宿主消息传输。多个监督周期可能产生多个独立 finding，但相同 fingerprint 不得重复追加。

## 生命周期状态

| 状态 | 进入条件 | 允许动作 | 退出条件 |
|---|---|---|---|
| `inactive` | 双条件未满足或已停止 | 只读状态 | 新一轮双条件满足后 `start` |
| `active` | `start` 校验通过 | 记录 Owner、扫描和 finding | Goal 结束、用户停止或 `stop` |
| `limited` | Owner/来源/通知受限 | 记录限制事实 | 依赖恢复后下一周期重试 |
| `blocked` | 状态损坏或安全校验失败 | 保留原文件、停止写入 | 人工修复后重新 `start` |
| `stopped` | 用户或 Goal 明确结束 | 只读历史摘要 | 不自动重启 |

## 状态安全

- 状态路径：`$CODEX_HOME/state/continuous-code-quality-supervisor/<checkout-sha256>.json`。
- 写入：同目录临时文件、UTF-8、原子替换；失败时保留原文件。
- 禁止字段：`prompt`、`response`、`token`、`password`、`secret`、`private_key`、`api_key` 及其大小写变体。
- 禁止保存：代码正文、完整 diff、Goal 原文、用户原始输入和通知响应正文。
- 读取规则 Skill 时不缓存正文；下一次扫描必须以当前工作树文件为准。
