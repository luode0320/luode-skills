---
schema_version: 1
doc_id: TEST-SS-REQUIREMENT-20260721
doc_type: test
source_ids:
  - SRC-SKILL-STREAMLINE-20260721-001
  - REQ-SS-20260721
  - AC-SS-20260721
  - CYCLE-SS-02
status: accepted
version: v1.0
template_version: 1
current_slice: TASK-SS-02-02 accepted
updated_at: 2026-07-21 23:59:59
reader_level: business_general
writing_style: plain_chinese
appendix_policy: preserve_existing_or_one_terminal_appendix
review_acceptance_gates:
  - stage: review
    applicability: applicable
    reason: 本测试任务新增需求域 owner route、消费者索引和定向验证脚本。
    basis: TASK-SS-02-01、TASK-SS-02-02 已完成实现与真实测试。
    required_by_source: true
    required_now: true
    completed_validation:
      - EVD-SS-02-01-REVIEW
      - EVD-SS-02-02-REVIEW
    substitute_validation: []
    manual_follow_up: 旧目录删除前再次复核 consumer 与 route。
    pass_standard: owner、route、消费者和历史保护无 P0/P1。
  - stage: acceptance
    applicability: applicable
    reason: 本测试任务必须证明 discovery 入口迁移后正例、负例和回滚边界成立。
    basis: TASK-SS-02-01、TASK-SS-02-02。
    required_by_source: true
    required_now: true
    completed_validation:
      - EVD-SS-02-01-ACCEPT
      - EVD-SS-02-02-ACCEPT
    substitute_validation: []
    manual_follow_up: TASK-SS-02-03 完成后重跑 post-delete。
    pass_standard: 定向 route validator、consumer validator 和预期负向均符合退出码标准。
  - stage: third_party
    applicability: not_applicable
    reason: 只读取本地仓库规则资产，不连接外部业务服务。
    basis: 测试范围不含数据库、缓存、消息队列或 HTTP/RPC。
    required_by_source: false
    required_now: false
    completed_validation: []
    substitute_validation: []
    manual_follow_up: N/A
    pass_standard: N/A
---
# 需求域入口收敛测试说明

结论：需求域入口与活跃引用迁移已完成实现、真实测试、审查和验收；影响：discovery 已迁移到唯一需求主入口的 `initial-discovery` 条件路由，live consumer 已更新；范围：owner、迁移 references、agent prompt、模板注册、项目规则、项目记忆、active-consumers 和定向验证；非范围：gap-routing 合并、旧目录删除、post-delete 和最终全链路收口；变化：由两个同生命周期入口收敛为一个主入口加条件路由；完成标准：route/consumer 正向通过，污染样本负向失败，历史归档不被改写；术语说明：live consumer 是当前会继续驱动自动触发或文档路由的非历史文件；验证状态：PASS；图片资产决策：N/A + 原因 + 证据：本任务只验证文本和机器索引，不生成或引用图片。

## 测试目标

- 证明 `initial-discovery` route 已由 `requirement-intake-rules` 唯一 owner 承接。
- 证明 discovery 的先侦察、local 安全、证据、记忆回写、输出和停止边界未丢失。
- 证明 9 个 live consumer 已从旧入口迁移，历史和 `.tmp` 快照不被误改。
- 证明旧入口污染样本会被负向验证拒绝。

## 执行环境与边界

- 仓库根目录：`F:\luode-skills`。
- 只使用 local 文件系统和 Python 标准库 / PyYAML。
- 不连接数据库、缓存、消息队列、HTTP/RPC、外部服务或 Obsidian vault。
- `.codex/config.toml`、Git 历史、历史归档和 `.tmp/skill-governance/` 不是本测试的写集。

## 测试矩阵

| TEST | 输入样本 | 执行命令 | 通过标准 | 失败预期 |
| --- | --- | --- | --- | --- |
| `TEST-SS-02-01-ROUTE` | owner、source、route refs、discovery fixtures | `python -B doc/5-tests/2026-07-21_221037/six-domain-skill-streamlining/validate_requirement_route_migration.py --repo-root F:\luode-skills --fixtures doc/5-tests/2026-07-21_221037/six-domain-skill-streamlining/fixtures/trigger-cases.yaml` | `valid=true`、退出码 `0`。 | 缺 route、保护语义、reference 或 source 时退出码非零。 |
| `TEST-SS-02-02-CONSUMER` | active-consumers、9 个 live 文件 | `python -B doc/5-tests/2026-07-21_221037/six-domain-skill-streamlining/validate_requirement_consumers.py --repo-root F:\luode-skills --index doc/5-tests/2026-07-21_221037/six-domain-skill-streamlining/inventory/active-consumers.json` | `valid=true`、退出码 `0`。 | 缺文件、旧入口残留、集合漂移时退出码非零。 |
| `TEST-SS-02-NEGATIVE` | 临时污染的 consumer index | 同 consumer validator，输入 `.tmp-consumers-negative.json`。 | 预期退出码 `1`，识别旧入口和 write set 污染。 | 错误返回 `0` 或未指出污染。 |
| `TEST-SS-02-MANIFEST` | manifest、资产 inventory、触发 fixtures | `python -B validate_domain_streamlining.py --phase baseline` 与 `--phase trigger`。 | 两个阶段均 `valid=true`。 | candidate、owner、hash 或 fixture 失败。 |

## 清理与回滚

- 清理：删除负向临时 index；测试使用 `python -B`，不保留 `.pyc`。
- 回滚：恢复 owner、live consumer、active-consumers、manifest 和项目记忆/风格变更；旧 source 只在删除任务获得完整 pre-delete/post-delete 通过后处理。
- 停止：任一 route、consumer、历史保护或负向断言失败，停止进入删除任务。

## 证据与追踪

| 来源 | REQ/RULE | AC | TASK | TEST | EVIDENCE |
| --- | --- | --- | --- | --- | --- |
| `SRC-SKILL-STREAMLINE-20260721-001` | `RULE-SS-TRIGGER-001`、`RULE-SS-USER-HABIT-001`、`RULE-SS-AUTH-001`、`RULE-SS-SAFETY-001` | `AC-SS-006` | `TASK-SS-02-01` | `TEST-SS-02-01-ROUTE` | `EVD-SS-02-01-TEST`、`EVD-SS-02-01-REVIEW`、`EVD-SS-02-01-ACCEPT` |
| `SRC-SKILL-STREAMLINE-20260721-001` | `RULE-SS-TRIGGER-001`、`RULE-SS-OUTPUT-001`、`RULE-SS-STOP-001` | `AC-SS-006` | `TASK-SS-02-02` | `TEST-SS-02-02-CONSUMER`、`TEST-SS-02-NEGATIVE` | `EVD-SS-02-02-TEST`、`EVD-SS-02-02-REVIEW`、`EVD-SS-02-02-ACCEPT` |

## 验收结论

PASS。当前测试文档只放行进入 `TASK-SS-02-03`，不放行旧目录删除或全链路 post-delete。