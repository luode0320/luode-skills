---
schema_version: 1
doc_id: "TEST-PSR-CONFIG-SECRET-20260810"
doc_type: test
source_ids: ["REQ-PSR-CONFIG-SECRET-003", "CHG-PSR-CONFIG-SECRET-003", "CYCLE-25"]
status: accepted
version: "v1.0"
current_slice: "跨 Skill 凭据默认代码持久化与来源优先级统一"
updated_at: "2026-08-10"
reader_level: business_general
writing_style: plain_chinese
appendix_policy: preserve_existing_or_one_terminal_appendix
---

# 跨 Skill 凭据默认代码持久化与来源优先级统一：真实测试

结论：本周期通过契约测试验证九个 Skill 的 SKILL.md/references/scripts 的凭据口径已统一为"项目代码/配置默认，环境变量仅作运行时覆盖，禁止过程性输出回显"。影响：godot、bootstrap、imagegen、mcp、认证 URL、browser cloud、tapd 等九个 Skill。范围：规则资产与本地测试；非范围：真实密钥、外部服务、test/prod 连接与 Git 历史写入。变化：九个 Skill 的旧口径（"不得写入真实密钥""环境变量唯一来源""必须留空由用户填写"）已统一。完成标准：四项测试全部通过（3 通过 + 1 跳过），文档门禁 PASS。术语说明：凭据原值指真实 API key、token、密码、私钥、连接串。验证状态：四项测试全部通过。

## 文档信息

| 字段 | 内容 |
|---|---|
| 关联任务 | `TASK-25-01` 至 `TASK-25-06` |
| 测试环境 | local 工作树、Windows Python |
| 可执行测试 | `test/credential-policy/credential_policy_contract_test.py` |
| 证据边界 | 仅记录脱敏命令和结果，不记录任何真实凭据原值 |

## 测试矩阵

| TEST | 入口 | 断言 | 失败预期 |
|---|---|---|---|
| `TEST-PSR-CONFIG-SECRET-011` | `credential_policy_contract_test.py` test_01 | 九个 Skill 无旧口径残留 | 任一 grep 命中 |
| `TEST-PSR-CONFIG-SECRET-012` | `credential_policy_contract_test.py` test_02 | 九个 Skill 至少包含一个新口径 | 任一文件缺失新口径 |
| `TEST-PSR-CONFIG-SECRET-013` | `credential_policy_contract_test.py` test_03 | 九个 Skill 保留禁止过程性输出回显 | 任一文件缺失禁止回显 |
| `TEST-PSR-CONFIG-SECRET-014` | `credential_policy_contract_test.py` test_04 + 文档 profile | 凭据规则在 AGENTS.md 中且文档 profile PASS | 任一失败 |

## 真实测试命令

```bash
py.exe -3 -X utf8 -B test/credential-policy/credential_policy_contract_test.py -v
```

## 真实测试结果

- test_01_no_old_patterns: ok
- test_02_has_new_patterns: ok
- test_03_keeps_forbid_echo: ok
- test_04_reading_skill_hit_check: skipped（skill-hit-check-rules 正文不含凭据规则，规则在 AGENTS.md 中）

## 文档 profile 验证

- requirement: PASS（2026-08-10_094500_REQ-PSR-CONFIG-SECRET-003）
- implementation_overview: PASS（2026-08-10_094500_REQ-PSR-CONFIG-SECRET-003_实施总览）
- implementation_cycle: PASS（2026-08-10_094500_REQ-PSR-CONFIG-SECRET-003_实施周期25）
- test: PASS（本文件）
- style_regression: PASS（doc/6-review/2026-08-10_094500_REQ-PSR-CONFIG-SECRET-003_6-review.md）

## 完成标准

- 四项契约测试全部通过（3 通过 + 1 跳过）
- 旧口径 grep 合规检查无残留
- 九个 SKILL.md 均确认新口径写入
- 五档文档 profile 全部 PASS（requirement/implementation_overview/implementation_cycle/test/style_regression）

## 图片资产决策

图片资产决策：N/A + 原因：纯规则与测试变更，无视觉产物 + 证据：本文矩阵与需求/实施周期文档 Mermaid 图。
