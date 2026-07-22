---
schema_version: 1
doc_id: TEST-SS-REQUIREMENT-DELETE-20260721
doc_type: test
source_ids:
  - SRC-SKILL-STREAMLINE-20260721-001
  - REQ-SS-20260721
  - AC-SS-20260721
  - CYCLE-SS-02
status: accepted
version: v1.0
template_version: 1
current_slice: TASK-SS-02-03 accepted
updated_at: 2026-07-21 23:59:59
reader_level: business_general
writing_style: plain_chinese
appendix_policy: preserve_existing_or_one_terminal_appendix
review_acceptance_gates:
  - stage: review
    applicability: applicable
    reason: 本任务执行了当前候选的删除、字典再生和增量 post-delete 验证。
    basis: TASK-SS-02-03 已完成实现与真实测试。
    required_by_source: true
    required_now: true
    completed_validation:
      - EVD-SS-02-03-REVIEW
    substitute_validation: []
    manual_follow_up: 全部候选删除前继续执行全局 gate。
    pass_standard: 当前候选删除边界、回滚和 post-delete 无 P0/P1。
  - stage: acceptance
    applicability: applicable
    reason: 旧入口删除必须以 scoped pre-delete/post-delete 证据放行。
    basis: TASK-SS-02-03。
    required_by_source: true
    required_now: true
    completed_validation:
      - EVD-SS-02-03-ACCEPT
    substitute_validation: []
    manual_follow_up: N/A
    pass_standard: 当前候选 source 消失、owner/route/字典和回滚均通过。
  - stage: third_party
    applicability: not_applicable
    reason: 只操作本地仓库资产。
    basis: 不连接外部服务。
    required_by_source: false
    required_now: false
    completed_validation: []
    substitute_validation: []
    manual_follow_up: N/A
    pass_standard: N/A
---
# 需求域 discovery 旧入口删除测试说明

结论：当前候选已完成删除前承接、真实删除、字典再生和 scoped post-delete 验证；影响：需求域不再保留 discovery 竞争入口；范围：单候选 source、owner、live consumer、资产状态、manifest、字典和增量验证器；非范围：gap-routing、其他退役候选、全局六域最终收口；变化：验证器支持按 source 增量执行删除门禁，并区分冻结资产记录与当前磁盘资产；完成标准：当前 source 不存在、owner route 可定位、字典无旧入口、post-delete 为 `valid=true`；术语说明：scoped gate 是只验证已完成迁移候选的增量删除闸门；验证状态：PASS；图片资产决策：N/A + 原因 + 证据：本任务不生成或引用图片。

## 测试目标

- 证明当前候选在删除前已完整承接。
- 证明物理删除只影响当前 source 目录。
- 证明字典、active consumer、owner route 和资产 retired 状态保持一致。
- 证明未迁移候选不会被本任务误报为已完成。

## 测试环境与边界

- 只使用 `F:\luode-skills` local 文件系统。
- 不连接数据库、缓存、消息队列、HTTP/RPC 或外部服务。
- 不执行 Git 历史写入；不修改 `.codex/config.toml`；不回写历史归档。

## 测试矩阵

| TEST | 输入样本 | 执行命令 | 通过标准 | 失败预期 |
| --- | --- | --- | --- | --- |
| `TEST-SS-02-03-PRE` | discovery candidate、owner、manifest、route fixtures | `pwsh ...run_domain_trigger_cases.ps1 -Phase pre-delete -OnlySource requirement-discovery-rules` | `valid=true`、退出码 `0`。 | owner route、consumer、asset、source 任一缺失即非零。 |
| `TEST-SS-02-03-DELETE` | 已通过 pre-delete 的 source 目录 | 工作区内受保护 Python 删除命令。 | 仅当前 source 目录消失。 | 路径越界、source 不存在或删除范围扩大时停止。 |
| `TEST-SS-02-03-DICTIONARY` | 当前 Skill 字典生成器 | `python -B skill-dictionary/generate_dictionary.py` | 退出码 `0`，字典无旧入口。 | 旧入口残留或生成器失败。 |
| `TEST-SS-02-03-POST` | deleted source、retired asset record、owner route | `pwsh ...run_domain_trigger_cases.ps1 -Phase post-delete -OnlySource requirement-discovery-rules` | `valid=true`、退出码 `0`。 | source 残留、旧入口断链、生命周期字段非法时非零。 |

## 清理与回滚

- 清理：删除测试期间生成的 `__pycache__`；保留 migration map、manifest、inventory、evidence 和 generator 结果。
- 回滚：按 baseline commit 恢复 source 目录，再恢复 owner refs、consumer index、manifest、asset retired 状态、字典和验证器变更。
- 停止：当前候选 post-delete 失败、字典旧 token 残留、回滚 locator 缺失或发现其他候选被误改时停止。

## 证据与追踪

| 来源 | REQ/RULE | AC | TASK | TEST | EVIDENCE |
| --- | --- | --- | --- | --- | --- |
| `SRC-SKILL-STREAMLINE-20260721-001` | `RULE-SS-TRIGGER-001`、`RULE-SS-AUTH-001`、`RULE-SS-STOP-001` | `AC-SS-006` | `TASK-SS-02-03` | `TEST-SS-02-03-PRE`、`TEST-SS-02-03-POST` | `EVD-SS-02-03-TEST`、`EVD-SS-02-03-REVIEW`、`EVD-SS-02-03-ACCEPT` |

## 验收结论

PASS。当前测试文档只证明 discovery 候选删除完成，不替代其他候选或 CYCLE-SS-06 全局验收。