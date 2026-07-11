# 案例模板与去重

## Canonical candidate 模板

将以下字段写入 owner skill 的 casebook；字段值必须脱敏。没有值时写 `unknown`，不要用猜测填充。

```yaml
id: <owner>-<short-slug>-<stable-id>
status: candidate
owner_skill: <唯一 owner skill>
mode: prevent | recover | learn
failure_stage: <调用阶段>
category: input-contract | environment | auth | transport | tool-contract | artifact | workflow
environment: local
tool_or_model: <名称与版本摘要>
error_signature: <状态码/退出码/稳定错误特征，不含 secret>
minimal_input: <可复现的非敏感摘要>
root_cause: <已验证根因>
solution: <可执行恢复或预防步骤>
verification:
  command_or_entrypoint: <验证入口>
  success_criteria: <原成功标准>
  result: passed
scope: <适用版本、输入和边界>
avoid: <禁止动作>
source: <任务/日志/案例来源的脱敏标识>
occurrences: 1
first_observed: <YYYY-MM-DD>
last_verified: <YYYY-MM-DD>
replaces: null
related: []
```

## 去重键

先规范化大小写、空白、绝对路径和动态 request id，再用以下字段组合判断重复：

`owner_skill + category + tool_or_model major version + error_signature + normalized minimal_input + scope`

命中同一去重键时更新原案例的验证时间、出现次数和来源，不新增正文。解决方案不同或边界不兼容时保留两条并标记 `conflicted`，等待裁决。

## 写入与引用规则

- candidate 必须追加到 owner 已声明的 casebook，不能修改其他 skill 的案例正文。
- 其他 skill 需要复用时只引用 `owner_skill + id`，不要复制一份案例。
- active 案例必须包含可重复验证入口、禁止动作和适用范围；缺任一项不得晋级。
- 旧方案失效时更新其状态为 `superseded` 或 `stale`，填写 `replaces`/替代案例 ID；不要删除历史证据。
- 无法脱敏、无法复验、owner 不唯一或仅适用于一次性机器状态的记录标记 `rejected`，只保留在当轮诊断输出。

## 最小交付报告

```text
执行失败学习：<observed/classified/...>
失败类别：<category>
Owner：<skill> / <case-id 或无>
根因：<一句话>
恢复与验证：<动作；同输入 + 原成功标准 + local 结果>
案例变更：<candidate/active/stale/conflicted/rejected；路径>
```
