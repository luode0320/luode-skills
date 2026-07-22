---
schema_version: 1
doc_id: EVD-SS-04-03-TEST
doc_type: test
source_ids:
  - SRC-SKILL-STREAMLINE-20260721-001
  - CYCLE-SS-04
status: accepted
version: v1.0
template_version: 1
current_slice: Bug 域最小任务 03 test 已完成
updated_at: 2026-07-21
reader_level: business_general
writing_style: plain_chinese
appendix_policy: preserve_existing_or_one_terminal_appendix
review_acceptance_gates:
  - stage: review
    applicability: not_applicable
    reason: 本文件是已执行任务的单类证据，完整任务审查由同任务 REVIEW 证据和周期审查报告承担。
    basis: 任务测试、审查和验收分别独立归档。
    required_by_source: false
    required_now: false
    completed_validation: []
    substitute_validation: []
    manual_follow_up: N/A
    pass_standard: N/A
  - stage: acceptance
    applicability: not_applicable
    reason: 本文件是单类任务证据，不单独构成周期放行。
    basis: 周期放行由四类任务证据和周期验收共同完成。
    required_by_source: false
    required_now: false
    completed_validation: []
    substitute_validation: []
    manual_follow_up: N/A
    pass_standard: N/A
  - stage: third_party
    applicability: not_applicable
    reason: 只验证本地仓库中的文本、索引和脚本，不连接外部业务服务。
    basis: 本任务没有数据库、缓存、消息队列或 HTTP/RPC 调用。
    required_by_source: false
    required_now: false
    completed_validation: []
    substitute_validation: []
    manual_follow_up: N/A
    pass_standard: N/A
---
# EVD-SS-04-03-TEST：Bug source 退役与 post-delete

结论：本任务真实测试通过；影响：Bug 入口收敛的自动触发、保护语义和删除门禁已得到可重复验证；范围：本任务对应的 owner、route、消费者、资产或退役断言；非范围：后续最小任务与六域总体放行；变化：新增或执行确定性验证并记录结果；完成标准：命令返回成功且全部断言满足；术语说明：canonical owner 指承接原入口语义的唯一主入口；验证状态：PASS；图片资产决策：N/A + 原因 + 证据：本任务只处理文本、脚本和索引，无图片生成、编辑或引用。

## 验证结论

本任务的命令、断言和失败预期均已执行并通过。

## 完成标准

本任务的实现、真实测试、审查和验收证据均已落盘，且不存在 P0/P1 阻断。

## 真实测试

```powershell
$env:PYTHONUTF8='1'
.\doc\5-tests\2026-07-21_221037\six-domain-skill-streamlining\run_domain_trigger_cases.ps1 -RepoRoot F:\luode-skills -Phase pre-delete -OnlySource <五个 source 逐个执行>
python -B doc/5-tests/2026-07-21_221037/six-domain-skill-streamlining/validate_cycle04_routes.py --repo-root F:\luode-skills --manifest doc/5-tests/2026-07-21_221037/six-domain-skill-streamlining/mapping/domain-streamlining-manifest.yaml --migration-map doc/5-tests/2026-07-21_221037/six-domain-skill-streamlining/mapping/cycle04-bug-route-migration-map.yaml --phase post-delete
.\doc\5-tests\2026-07-21_221037\six-domain-skill-streamlining\run_domain_trigger_cases.ps1 -RepoRoot F:\luode-skills -Phase post-delete -OnlySource <五个 source 逐个执行>
```

结果：五个 pre-delete 与五个 post-delete scoped validator 均返回 `valid=true`、`errors=[]`；cycle04 route validator 返回 `candidate_count=5`、`retained_count=6`、`valid=true`。

## 删除与追溯

| source | 状态 | 追溯 |
| --- | --- | --- |
| `bug-assertion-diagnostic-rules` | 已删除 | inventory 冻结 hash、`TASK-SS-04-03`、manifest rollback locator。 |
| `bug-debug-log-rules` | 已删除 | inventory 冻结 hash、`TASK-SS-04-03`、manifest rollback locator。 |
| `bug-discovery-rules` | 已删除 | inventory 冻结 hash、`TASK-SS-04-03`、manifest rollback locator。 |
| `bug-gap-rules` | 已删除 | inventory 冻结 hash、`TASK-SS-04-03`、manifest rollback locator。 |
| `bug-runtime-debug-rules` | 已删除 | inventory 冻结 hash、`TASK-SS-04-03`、manifest rollback locator。 |

## 清理与回滚

- 清理：删除前已确认五个绝对目录均在 `F:\luode-skills` 内；未删除仓库外路径或业务数据。
- 回滚：先依据 inventory 冻结文件 hash 和 manifest `baseline_commit` 恢复 source，再恢复 consumer index 和 manifest authorization 状态。
- 停止：任一 post-delete 发现 source 残留、trigger alias 丢失、retained skill 缺失或 consumer 悬空时停止。
