# Agent Runtime Recovery 案例库

本文件只保存本 skill owner 的脱敏运行期恢复案例。失败分类、candidate/active 生命周期和唯一 owner 规则由 `execution-failure-learning-rules` 统一管理；未复验的猜测不得写入本文件。

## 字段模板

```yaml
id: agent-runtime-recovery-<short-slug>-<stable-id>
status: candidate
owner_skill: agent-runtime-recovery-rules
mode: prevent | recover | learn
failure_stage: probe | reconnect | reload | restart | wait_ready | resume
category: transport | environment | tool-contract | workflow
environment: local
platform_id: <脱敏平台标识>
adapter_id: <脱敏 adapter 标识与版本摘要>
component_kind: mcp | plugin | browser | tool | agent_host | other
error_signature: <状态码/退出码/稳定错误特征，不含 secret>
minimal_input: <非敏感摘要>
root_cause: <已验证根因>
solution: <可执行恢复步骤>
verification:
  command_or_entrypoint: <local fixture 或测试入口>
  success_criteria: <原成功标准>
  result: passed
scope: <版本、配置来源和适用边界>
avoid: <禁止动作>
source: <脱敏任务/日志标识>
occurrences: 1
first_observed: <YYYY-MM-DD>
last_verified: <YYYY-MM-DD>
replaces: null
related: []
```

## 案例边界

- `candidate` 必须有稳定复现或确定性契约证据、同输入同成功标准 local 复验和脱敏结果；`active` 还需要维护授权并满足生命周期门禁。
- 只记录恢复动作和验证结果，不记录 prompt、响应正文、token、密码、路径、用户数据或完整网络地址。
- 不同平台、版本、scope 或副作用不兼容时不得合并；标记 `conflicted` 并暂停自动复用。
- 一次性网络抖动、预期负向测试、用户取消和权限阻断不晋级 active。

## 当前案例

暂无已验证案例。首次发现应先按模板形成 `candidate`，完成同输入 local 复验并经授权后才可 `active`。
