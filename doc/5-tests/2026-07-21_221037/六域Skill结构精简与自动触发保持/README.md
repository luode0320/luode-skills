---
schema_version: 1
doc_id: TEST-SS-20260721
doc_type: test
source_ids:
  - SRC-SKILL-STREAMLINE-20260721-001
  - REQ-SS-20260721
  - AC-SS-20260721
status: accepted
version: v1.1
template_version: 1
current_slice: CYCLE-SS-01 / TASK-SS-01-01 accepted
updated_at: 2026-07-21 22:10:37
reader_level: business_general
writing_style: plain_chinese
appendix_policy: preserve_existing_or_one_terminal_appendix
review_acceptance_gates:
  - stage: review
    applicability: applicable
    reason: 本测试任务新增迁移清单、资产基线、消费者索引和触发 fixtures。
    basis: CYCLE-SS-01 / TASK-SS-01-01。
    required_by_source: true
    required_now: true
    completed_validation:
      - EVD-SS-01-TEST
      - EVD-SS-01-REVIEW
    substitute_validation: []
    manual_follow_up: N/A
    pass_standard: 清单、哈希、路径边界和 fixture 契约无 P0/P1。
  - stage: acceptance
    applicability: applicable
    reason: 本任务必须验证后续 Skill 迁移的基线入口。
    basis: TASK-SS-01-01。
    required_by_source: true
    required_now: true
    completed_validation:
      - EVD-SS-01-TEST
      - EVD-SS-01-ACCEPT
    substitute_validation: []
    manual_follow_up: 真实迁移完成后重新执行 post-delete 验收。
    pass_standard: baseline 验证器返回 valid=true 且无错误。
  - stage: third_party
    applicability: not_applicable
    reason: 只读取本地仓库文件和 Python 标准库。
    basis: 不连接外部业务服务。
    required_by_source: false
    required_now: false
    completed_validation: []
    substitute_validation: []
    manual_follow_up: N/A
    pass_standard: N/A
---
# 六域 Skill 结构精简与自动触发保持基线验证说明

结论：本测试冻结六域 36 个 Skill、11 个拟退役候选、资产哈希、活跃消费者和触发样本；影响：后续每个周期都使用该基线判断迁移是否完整；范围：迁移清单、资产索引、消费者索引、触发 fixtures 和验证器；非范围：本任务不修改 Skill 资产、不删除旧目录、不刷新字典；变化：把迁移前事实转成可复核机器输入；完成标准：基线验证器通过且所有候选字段、路径和哈希完整；术语说明：基线指迁移前磁盘事实，消费者指引用或依赖 Skill 名称的活跃文件；验证状态：实现、真实测试、审查和验收均已完成。；图片资产决策：N/A + 原因 + 证据：本任务不生成、不编辑、不引用图片。

## 文档信息

| 字段 | 内容 |
| --- | --- |
| 测试任务 | `CYCLE-SS-01 / TASK-SS-01-01` |
| 测试根目录 | `doc/5-tests/2026-07-21_221037/` |
| 中文说明目录 | `六域Skill结构精简与自动触发保持/` |
| ASCII 资产目录 | `six-domain-skill-streamlining/` |
| 执行环境 | `F:\luode-skills`、Python UTF-8、PowerShell 7 |
| 数据来源 | 当前仓库 36 个目标 Skill、当前活跃消费者和迁移计划 manifest |
| 图片资产决策 | `N/A + 原因 + 证据`：只验证文本、YAML、JSON、Python、PowerShell 和文档结构，不涉及图片资产。 |

## 结论

本测试任务已完成迁移前基线冻结；基线通过不代表任何 Skill 已完成合并或删除。

## 测试目标

- 冻结六域 36 个 Skill 的分类、动作、目标 owner 和触发契约。
- 冻结每个 Skill 的文本资产文件、字节数和 SHA-256。
- 冻结历史归档之外的活跃消费者索引。
- 为后续删除前、删除后和负向触发验证提供固定样本。

## 测试环境与边界

- 只使用 `F:\luode-skills` local 仓库文件。
- 不连接数据库、缓存、消息队列、HTTP/RPC、第三方业务服务或生产环境。
- `.codex/config.toml` 不进入 manifest、write set 或资产迁移范围。
- Obsidian vault 不参与本测试，vault 状态阻断不影响本地基线测试。

## 测试用例与断言

| TEST | 输入样本 | 执行命令 | 通过标准 | 失败预期 |
| --- | --- | --- | --- | --- |
| `TEST-SS-001` | manifest、资产索引、消费者索引 | `python -X utf8 doc/5-tests/2026-07-21_221037/six-domainSkilldoc/5-tests/2026-07-21_221037/six-domain-skill-streamlining/validate_domain_streamlining.py --phase baseline` | 36 个候选、11 个退役候选、资产哈希、路径和回滚字段均通过。 | 缺字段、目标不存在、哈希漂移、路径越界时非零退出。 |
| `TEST-SS-001-PYCOMPILE` | Python 验证器 | `python -X utf8 -m py_compile doc/5-tests/2026-07-21_221037/six-domain-skill-streamlining/validate_domain_streamlining.py` | 编译退出码为 0。 | 语法错误时非零退出。 |
| `TEST-SS-001-PS` | PowerShell wrapper | `pwsh -NoProfile -File doc/5-tests/2026-07-21_221037/six-domain-skill-streamlining/run_domain_trigger_cases.ps1 -Phase baseline` | wrapper 转发成功且返回 valid=true。 | validator 失败时 wrapper 非零退出。 |
| `TEST-SS-001-NEGATIVE` | 越界路径和非法阶段 | validator 的参数校验分支。 | 越界路径、非法阶段和缺失 manifest 被阻断。 | 误接受越界路径或非法参数。 |

## 完成标准

- manifest 记录 36 条候选，`summary.unmapped=0`。
- 11 条 `merge_retire` 均有目标 owner、路由、保护语义、消费者索引、资产索引和回滚定位。
- 资产索引中的文件数量、字节数和 SHA-256 与当前磁盘一致。
- 消费者索引中的每个文件当前存在且位于仓库根目录内。
- Python、PowerShell 和文档 profile 均通过。

## 怎样算完成

只有上述全部条件同时满足，`TASK-SS-01-01` 才能标记为 `done`；本任务不得把基线通过解释为迁移、删除或字典刷新已完成。

## 通过标准

`TEST-SS-001`、`TEST-SS-001-PYCOMPILE`、`TEST-SS-001-PS` 均返回成功；所有负向样本均按预期拒绝；没有 P0/P1 失败。

## 验收结论

PASS。迁移前 manifest、资产索引、活跃消费者索引和 72 条触发样本已冻结，验证器返回 `valid=true`。

## 验证结论

PASS。Python 编译、baseline validator 和 PowerShell wrapper 均通过；本任务仅证明基线契约，不证明后续 Skill 迁移结果。

## 审查结论

PASS。审查确认测试资产路径、UTF-8 写入、仓库边界、`.codex/config.toml` 排除、失败出口和回滚定位均已明确；未发现 P0/P1。

## 执行附录

- manifest：`six-domain-skill-streamlining/mapping/domain-streamlining-manifest.yaml`。
- 资产索引：`six-domain-skill-streamlining/inventory/domain-asset-inventory.json`。
- 消费者索引：`six-domain-skill-streamlining/inventory/active-consumers.json`。
- 触发样本：`six-domain-skill-streamlining/fixtures/trigger-cases.yaml`。
- 验证入口：`six-domain-skill-streamlining/validate_domain_streamlining.py`。
- wrapper：`six-domain-skill-streamlining/run_domain_trigger_cases.ps1`。
- 清理：删除 `__pycache__` 和临时输出，保留正式 manifest、索引、fixtures、脚本、证据和 README。
- 回滚：只删除本任务新增测试资产，恢复到周期 01 文档基线，不删除任何真实 Skill。

## 追踪附录

| 来源 | 需求/规则 | 验收 | 周期 | 任务 | 测试 | 证据 |
| --- | --- | --- | --- | --- | --- | --- |
| `SRC-SKILL-STREAMLINE-20260721-001` | `REQ-SS-001`、`RULE-SS-001` | `AC-SS-001` | `CYCLE-SS-01` | `TASK-SS-01-01` | `TEST-SS-001` | `EVD-SS-01-TEST`、`EVD-SS-01-REVIEW`、`EVD-SS-01-ACCEPT` |
