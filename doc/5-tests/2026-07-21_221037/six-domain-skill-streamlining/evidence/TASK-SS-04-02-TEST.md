---
schema_version: 1
doc_id: EVD-SS-04-02-TEST
doc_type: test
source_ids:
  - SRC-SKILL-STREAMLINE-20260721-001
  - CYCLE-SS-04
status: accepted
version: v1.0
template_version: 1
current_slice: Bug 域最小任务 02 test 已完成
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
# EVD-SS-04-02-TEST：Bug 域活跃消费者迁移

结论：本任务真实测试通过；影响：Bug 入口收敛的自动触发、保护语义和删除门禁已得到可重复验证；范围：本任务对应的 owner、route、消费者、资产或退役断言；非范围：后续最小任务与六域总体放行；变化：新增或执行确定性验证并记录结果；完成标准：命令返回成功且全部断言满足；术语说明：canonical owner 指承接原入口语义的唯一主入口；验证状态：PASS；图片资产决策：N/A + 原因 + 证据：本任务只处理文本、脚本和索引，无图片生成、编辑或引用。

## 验证结论

本任务的命令、断言和失败预期均已执行并通过。

## 完成标准

本任务的实现、真实测试、审查和验收证据均已落盘，且不存在 P0/P1 阻断。

## 真实测试

```powershell
$env:PYTHONUTF8='1'
python -B doc/5-tests/2026-07-21_221037/six-domain-skill-streamlining/validate_cycle04_routes.py --repo-root F:\luode-skills --manifest doc/5-tests/2026-07-21_221037/six-domain-skill-streamlining/mapping/domain-streamlining-manifest.yaml --migration-map doc/5-tests/2026-07-21_221037/six-domain-skill-streamlining/mapping/cycle04-bug-route-migration-map.yaml --phase pre-delete
```

结果：退出码 `0`；`valid=true`、`errors=[]`。验证器对 consumer index 的所有非 `.tmp/` 路径做存在性检查，并排除迁移资源命名空间与 README 历史记录后，断言没有活跃 consumer 继续引用退役 source。

## 迁移范围

- `README.md`、`编码skill.md`：收敛为一个 Bug 主入口和两个条件路由。
- `bug-reproduction-rules`、`bug-root-cause-rules`、`bug-fix-proposal-rules`：让路或回流改为 canonical route。
- `team-development-rules`、`parallel-task-dispatch-rules`：裁决和路由不再把日志、断言、断点拆成竞争 owner。
- `artifact-delivery-gate-rules`：模板登记切换到迁移后的 canonical resource。
- `active-consumers.json`：移除五个 source 目录及其交叉自引用，避免 post-delete 出现不存在路径。

## 清理与回滚

- 清理：未连接外部服务，未写入业务数据；未重写 `.tmp/`、历史归档或字典生成物。
- 回滚：使用 mapping 和 consumer index 的基线记录还原各 consumer 文本与路径清单。
- 停止：发现非历史活跃 consumer 仍以旧 source 作为路由入口时停止，不进入删除。
