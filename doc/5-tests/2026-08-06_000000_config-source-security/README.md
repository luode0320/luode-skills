---
schema_version: 1
doc_id: "TEST-PSR-CONFIG-SECURITY-20260806"
doc_type: test
source_ids: ["REQ-PSR-CONFIG-SOURCE-001", "CYCLE-PSR-23"]
status: accepted
version: "v1.0"
current_slice: "configuration-source-security"
updated_at: "2026-08-06 00:00:00"
reader_level: business_general
writing_style: plain_chinese
appendix_policy: preserve_existing_or_one_terminal_appendix
---

# 配置来源安全边界真实测试

结论：本轮已验证配置目录规则将 `embedded/` 固定为同一环境的主来源，并将 `yaml/` 固定为缺失时的回退来源；影响：Catalog、Schema、reference、Skill 与活动测试对来源优先级和秘密边界保持一致；范围：`package-structure-rules` 配置 Catalog、Schema、reference、SKILL 与契约测试；非范围：真实业务 loader 运行、外部服务和非 local 环境；变化：YAML 策略改为 `embedded_source_fallback`，embedded 策略保留 `embedded_source_primary`；完成标准：配置专项和目录回归通过，JSON、差异和风格检查通过；术语说明：主来源表示优先读取，回退来源表示主来源缺失时才读取；验证状态：已通过。

## 文档信息

| 字段 | 内容 |
| --- | --- |
| 关联任务 | `TASK-PSR-CONFIG-SECURITY-01` |
| 测试环境 | local 工作树、Windows Python、临时目录 |
| 可执行测试 | `test/package-structure-rules/configuration_layout_test.py` |
| 证据边界 | 仅记录脱敏命令和结果，不记录任何秘密原值 |

## 测试矩阵

| TEST | 入口 | 断言 | 失败预期 |
| --- | --- | --- | --- |
| `TEST-PSR-CONFIG-SECURITY-01` | 配置专项 | 11 个配置查询、命名、秘密策略和 loader 来源断言全部通过 | 任一 source policy、loader 优先级或边界断言不一致即失败 |
| `TEST-PSR-CONFIG-SECURITY-02` | `test/package-structure-rules` 四文件回归 | 26 个既有目录、入口、配置和 adoption 行为断言全部通过 | 任一兼容行为回退即失败 |
| `TEST-PSR-CONFIG-SECURITY-03` | JSON、差异和文档风格检查 | Catalog/Schema 可解析，`git diff --check` 无错误，6-review 为 `STYLE: PASS` | 语法、格式或风格不一致即失败 |

## 真实测试命令

```powershell
python -X utf8 -m unittest discover -s test/package-structure-rules -p configuration_layout_test.py -v
python -X utf8 -m unittest discover -s test/package-structure-rules -p "*_test.py" -v
python -X utf8 -c "import json; json.load(open('package-structure-rules/references/placement-catalog.yaml', encoding='utf-8')); json.load(open('package-structure-rules/references/placement-catalog.schema.json', encoding='utf-8')); print('JSON:PASS')"
git diff --check
python -X utf8 -B artifact-delivery-gate-rules/scripts/validate_engineering_docs.py --profile test --doc doc/5-tests/2026-08-06_000000_config-source-security/README.md --root F:\luode-skills --strict
python -X utf8 -B artifact-delivery-gate-rules/scripts/validate_engineering_docs.py --profile style_regression --doc doc/6-review/2026-08-06_000000_PSR-CONFIG-SECURITY_6-review.md --root F:\luode-skills --strict
```

## 本轮实测结果

| TEST | 状态 | 证据 |
| --- | --- | --- |
| `TEST-PSR-CONFIG-SECURITY-01` | 配置专项 `11/11` 通过 | `EVD-PSR-CONFIG-SECURITY-01` |
| `TEST-PSR-CONFIG-SECURITY-02` | 四文件目录回归 `26/26` 通过 | `EVD-PSR-CONFIG-SECURITY-02` |
| `TEST-PSR-CONFIG-SECURITY-03` | JSON 解析通过，`git diff --check` 通过，6-review `STYLE: PASS` | `EVD-PSR-CONFIG-SECURITY-03` |

## 验证结论

三项测试均达到完成标准；未发现来源优先级、秘密策略、目录位置或既有 strict/adoption 行为回归。

## 测试边界

- 本轮只使用 local 工作树和临时目录，不连接数据库、缓存、消息队列、HTTP/RPC 上游或 test/prod 环境。
- 技能仓库根目录直接执行 strict 不作为本轮证据：该根目录缺少业务项目必需 `Dockerfile`，且 `CLAUDE.md` 与 `AGENTS.md` 的基线不一致；临时 fixture 的 strict/adoption 负向断言已由 `26/26` 回归覆盖。
- 本轮不写入任何 API key、token、密码、私钥、连接串或其它秘密原值。
- 图片资产决策：N/A + 原因：本任务只验证文本规则、Catalog、Schema 和测试脚本，无界面或视觉产物 + 证据：上述测试矩阵。

## 追踪附录

| 规则变化 | TEST | 风格证据 |
| --- | --- | --- |
| `embedded/` 主来源、`yaml/` 回退来源 | `TEST-PSR-CONFIG-SECURITY-01` | `EVD-PSR-CONFIG-SECURITY-03` |
| YAML 禁止秘密原值、embedded 允许源码私密值 | `TEST-PSR-CONFIG-SECURITY-01..02` | `EVD-PSR-CONFIG-SECURITY-01..03` |
