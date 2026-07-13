---
schema_version: 1
doc_id: "TESTDOC-PSENV-20260713"
doc_type: test
source_ids: ["REQDOC-PSENV-20260713", "ACDOC-PSENV-20260713"]
status: accepted
version: "1.0"
current_slice: "TASK-PSENV-11"
updated_at: "2026-07-13 23:08:00"
reader_level: business_general
writing_style: plain_chinese
appendix_policy: preserve_existing_or_one_terminal_appendix
review_acceptance_gates: []
---

# Windows PowerShell 环境可靠性升级测试

本轮测试只验证环境脚本自己的判断和回滚能力。所有会写入的内容都在临时目录中，真实用户 profile、Windows Terminal、执行策略和已安装软件不得变化。

## 文档信息

| 项目 | 内容 |
| --- | --- |
| 对应范围 | Windows PowerShell 环境可靠性升级 |
| 验证结论 | 通过：PowerShell 5.1 与 PowerShell 7 的九项隔离测试均通过 |

图片资产决策：N/A + 原因：测试对象是命令行为和临时文件。证据：没有页面、视觉对比或截图需求。

## 测试范围

- 必需与可选工具的状态判断。
- SessionEnsure 的 marker、TTL 和活锁。
- WhatIf 的零写入。
- Terminal JSONC 的注释保留、回滚和漂移拒绝。
- 未知命令的 candidate 记录。
- Git Bash 与 WSL launcher 的识别边界。

## 执行附录

真实测试脚本位于 `../windows-powershell-environment-rules/scripts/run_v2_environment_tests.ps1`。

```powershell
& powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File doc/5-tests/2026-07-13_214235/windows-powershell-environment-rules/scripts/run_v2_environment_tests.ps1
& pwsh.exe -NoLogo -NoProfile -File doc/5-tests/2026-07-13_214235/windows-powershell-environment-rules/scripts/run_v2_environment_tests.ps1
```

## 完成标准

- 两种 PowerShell 都通过九项断言。
- 测试结束后真实 Windows Terminal 的 hash 保持不变。
- 临时目录在 finally 中清理，未安装软件、未执行网络请求。

## 追踪附录

| 测试 | 覆盖规则 |
| --- | --- |
| TEST-PSENV-001 | RULE-PSENV-001：可选工具不阻断 |
| TEST-PSENV-002 | RULE-PSENV-003：状态、TTL、锁和 WhatIf |
| TEST-PSENV-003 | RULE-PSENV-004：Terminal 回滚与防漂移 |
| TEST-PSENV-004 | RULE-PSENV-005：未知命令与 Git Bash 分流 |
