---
schema_version: 1
doc_id: EVD-SS-04-01-TEST
doc_type: test
source_ids:
  - SRC-SKILL-STREAMLINE-20260721-001
  - CYCLE-SS-04
status: accepted
version: v1.0
template_version: 1
current_slice: Bug 域最小任务 01 test 已完成
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
# EVD-SS-04-01-TEST：Bug owner 条件路由与资产迁移

结论：本任务真实测试通过；影响：Bug 入口收敛的自动触发、保护语义和删除门禁已得到可重复验证；范围：本任务对应的 owner、route、消费者、资产或退役断言；非范围：后续最小任务与六域总体放行；变化：新增或执行确定性验证并记录结果；完成标准：命令返回成功且全部断言满足；术语说明：canonical owner 指承接原入口语义的唯一主入口；验证状态：PASS；图片资产决策：N/A + 原因 + 证据：本任务只处理文本、脚本和索引，无图片生成、编辑或引用。

## 验证结论

本任务的命令、断言和失败预期均已执行并通过。

## 完成标准

本任务的实现、真实测试、审查和验收证据均已落盘，且不存在 P0/P1 阻断。

## 执行环境

- 仓库根目录：`F:\luode-skills`。
- 环境：local 文件系统、Python UTF-8、PowerShell。
- 外部连接：`N/A + 原因 + 证据`：本任务只读写仓库内 Skill 资产，不连接业务数据库、缓存、消息队列、HTTP/RPC 或非 local 环境。

## 真实测试

```powershell
$env:PYTHONUTF8='1'
python -B -m py_compile doc/5-tests/2026-07-21_221037/six-domain-skill-streamlining/validate_cycle04_routes.py
python -B doc/5-tests/2026-07-21_221037/six-domain-skill-streamlining/validate_cycle04_routes.py --repo-root F:\luode-skills --manifest doc/5-tests/2026-07-21_221037/six-domain-skill-streamlining/mapping/domain-streamlining-manifest.yaml --migration-map doc/5-tests/2026-07-21_221037/six-domain-skill-streamlining/mapping/cycle04-bug-route-migration-map.yaml --phase pre-delete
```

结果：两条命令均退出码 `0`；route validator 返回 `candidate_count=5`、`retained_count=6`、`valid=true`、`errors=[]`。

## 结构断言

- `bug-intake-rules/SKILL.md` 保留单主入口，并以 `discovery-and-gap` 和 `runtime-diagnostics` 两个条件路由承接触发。
- `cycle04-bug-route-migration-map.yaml` 已列出每个 source 的原始全部资产、迁移资源和 route document。
- `validate_cycle04_routes.py` 验证 owner marker、正负 fixture、触发别名、保护语义、迁移资源、source 完整性和六个保留入口。
- 失败预期：缺 route marker、缺触发别名、缺迁移资源、嵌套反引号或 source 资产清单漂移时返回非零。

## 清理与回滚

- 清理：本任务未产生运行时诊断资产和业务数据。
- 回滚：依据 `cycle04-bug-route-migration-map.yaml`、manifest 的 `rollback_locator` 及 source 未删除状态，恢复 owner、route、映射与验证器。
- 停止：任一保护语义或触发别名不能由 canonical owner 定位时停止，不进入消费者迁移。
