# Codex App 任务路由

本路由只适用于用户要求在同一保存项目中创建新的本地 Codex 任务。工具返回值始终是事实来源；不要根据项目名称、最近时间或模型猜测工具结果。

## 项目匹配

1. 记录当前任务的工作目录和保存项目短名称，但不把绝对路径写进交接包。
2. 调用 `codex_app__list_projects`。
3. 在返回项目中寻找与当前工作目录完全对应的唯一项目。项目缺失、多匹配、返回值不完整或 `isGitRepository` 无法读取时停止创建。
4. 仅当用户明确要求同项目 `local` 时使用 `target.environment: { "type": "local" }`。不要把 `worktree`、projectless 或 ChatGPT Work Cloud 当作等价替代。

## 创建调用

调用 `codex_app__create_thread` 时使用以下语义：

```json
{
  "target": {
    "type": "project",
    "projectId": "由 list_projects 返回的精确 ID",
    "environment": { "type": "local" }
  },
  "prompt": "按新任务启动契约处理下面的脱敏交接包：<交接包 JSON>",
  "thinking": "沿用用户默认设置"
}
```

不要自行指定模型或思考档位。`prompt` 中先放固定启动要求，再放通过脚本校验的 JSON；不得拼接未校验的原始对话全文。

## 创建结果

- 返回 `threadId` 与 `hostId`：任务已经有可供工具调用的真实身份。只对该二元组调用一次 `codex_app__wait_threads`，等待首次完成或需要关注的状态。
- 只返回 `clientThreadId`：任务仍在创建 / 设置中。它不是 `threadId`，禁止传给 `codex_app__wait_threads`、`codex_app__read_thread` 或 `codex_app__send_message_to_thread`；报告“setup pending”，不要宣称已 ready。
- 返回错误、空对象、字段类型不符或状态无法解释：按 `manual_handoff` 处理，保留旧任务，不调用归档工具。
- `wait_threads` 返回后只报告工具明确给出的完成、需要关注或错误状态；不把等待超时解释为失败，也不把“已创建”解释为“已完成”。

## 新任务启动提示

新任务 prompt 必须包含以下最小要求：

1. 第一条响应先执行 `skill-hit-check-rules`，输出命中技能、知识库判断、并行判断和适用闸门。
2. 读取父目录规则、`PROJECT_CURRENT.md`、`PROJECT_MEMORY.md`；需要历史时再窄读 `PROJECT_HISTORY.md`。
3. 用新任务自己的 `session_id` 校验或建立 projection。不能复制旧任务的 `update_plan` payload，也不能覆盖其它会话 projection。
4. 再次运行交接包校验；以当前代码和项目文档核对 `completed`、`in_progress`、`next_steps` 与 `validation`。
5. 先核验 `in_progress` 中的中断点；涉及非幂等写操作或状态不明时只读查询并暂停。
6. 按 `next_steps` 顺序执行，完成一项就更新自身 projection 和验证证据。

## 归档与回滚

v1 创建路径不调用 `codex_app__set_thread_archived`。旧任务仍可作为事实来源和人工回看入口；新任务 ready 后只提示用户在 UI 中人工归档。创建失败、项目匹配失败或新任务未 ready 时不做任何旧任务状态变更。
