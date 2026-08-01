---
name: continuous-code-quality-supervisor-rules
description: 仅当当前会话处于 Goal active 且用户当前消息明确表达“监控代码”时触发。负责每个监督周期读取最新 diff，复用 `code-style-consistency-rules` 拥有的共享静态 Owner 路由，记录可去重的 finding，并通知实际实施会话；不复制 Owner 正文、路由常量或来源映射，不自动改码、格式化、执行测试、做阶段审查、提交或交付。
---

# 持续代码质量监督规则

## 触发闸门

1. 先确认 Goal 当前为 active。
2. 再确认当前用户消息包含“监控代码”意图。
3. 任一条件不满足时立即退出，不创建监督状态、不扫描代码、不发送通知。
4. Plan Mode、Goal inactive、Goal 状态不明或用户未提出监控意图时均不触发。

## 执行流程

1. 读取 [生命周期与触发契约](references/lifecycle-and-trigger-contract.md)。
2. 每个周期重新读取最新 diff、当前工作树中的 Owner Skill 正文、[共享静态 Owner 路由契约](../code-style-consistency-rules/references/static-owner-routing-contract.md)和[监督消费边界](references/owner-routing-matrix.md)，禁止使用旧快照或本 Skill 内的规则副本。
3. 通过 `code-style-consistency-rules/scripts/static_owner_router.py` 获得基础 Owner 与条件 Owner；Schema 路由先于 Query，接口四 Owner 按 endpoint、request、response、swagger 顺序处理。
4. 只执行静态质量检查。测试程序只能路由到 `test-program-rules` 做结构检查，不调用测试策略、功能验证或回归 Skill。
5. 按 [finding 与通知契约](references/finding-notification-contract.md) 生成 finding、计算指纹、去重并通知实际实施会话。
6. Owner 文件缺失、名称不一致或规则来源无法读取时，记录 `unclassified/limited` finding，并停止该 Owner 路由，不猜测规则。
7. 使用 `scripts/supervisor_state.py` 管理脱敏状态；状态成功写入不等于通知成功，也不等于代码已修复。

## 责任边界

- 只负责编排既有代码规则、观察增量变化、记录 finding 和发送通知。
- 不创建新代码规范，不复制 Owner 正文、路由常量或来源映射，不回写 `PROJECT_STYLE.md`，不创建项目私有 Skill。
- 不调用阶段审查、最终收口、测试执行、验收、交付、Git、需求、Bug、状态管理或其他元流程 Skill。
- `code-context-resync-rules` 不是 Owner；每个扫描周期直接重新读取最新 diff。
- `codegraph-analysis-rules` 不是 Owner；复杂影响面由主流程按需单独调用。

## 状态接口

状态文件固定为 `$CODEX_HOME/state/continuous-code-quality-supervisor/<checkout-sha256>.json`。建议由 Goal 宿主按约 30 秒重新唤醒并调用：

```text
python continuous-code-quality-supervisor-rules/scripts/supervisor_state.py start --checkout <repo> --goal-active --intent 监控代码
python continuous-code-quality-supervisor-rules/scripts/supervisor_state.py record-scan --checkout <repo> --diff-id <id> --changed-file <path>
python continuous-code-quality-supervisor-rules/scripts/supervisor_state.py status --checkout <repo>
python continuous-code-quality-supervisor-rules/scripts/supervisor_state.py stop --checkout <repo>
```

脚本只保存状态摘要和 finding 元数据，不保存代码正文、Goal 原文、提示词、响应或凭据。脚本不实现定时器，不伪造 Goal 状态，不执行测试，不自动发送宿主消息。

## 结果判定

- `active`：双条件满足且状态可安全写入。
- `limited`：Owner 缺失、来源不可读或通知能力不可验证；只记录限制事实。
- `inactive`：未满足触发条件、已停止或 Goal 已结束。
- `blocked`：状态损坏、敏感字段校验失败或安全边界无法保证；保持原状态文件并停止继续写入。
