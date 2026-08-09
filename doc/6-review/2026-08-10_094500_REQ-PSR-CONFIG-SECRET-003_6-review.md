---
schema_version: 1
template_version: 1
doc_id: "STYLE-PSR-CONFIG-SECRET-20260810"
doc_type: style_regression
source_ids: ["REQ-PSR-CONFIG-SECRET-003", "TEST-PSR-CONFIG-SECRET-20260810"]
status: accepted
version: "v1.0"
current_slice: "completed"
updated_at: "2026-08-10"
reader_level: business_general
writing_style: plain_chinese
appendix_policy: preserve_existing_or_one_terminal_appendix
---

# 跨 Skill 凭据默认代码持久化与来源优先级统一：6-review

结论：本轮已完成九个 Skill 凭据口径改动的格式、编码、命名、目录归位、注释和可读性回归。影响：九个 Skill 的 SKILL.md/references/scripts 表达一致。范围：规则资产、契约测试与文档证据。非范围：业务正确性、真实密钥、外部服务和发布放行。变化：九个 Skill 的旧凭据口径已统一为"项目代码/配置默认，环境变量仅作运行时覆盖，禁止过程性输出回显"。完成标准：真实测试先通过且本记录为 `STYLE: PASS`。术语说明：STYLE 只表示格式、位置、写法和可读性回归结果。验证状态：已通过。

## 文档信息

| 字段 | 内容 |
|---|---|
| 关联测试 | `TEST-PSR-CONFIG-SECRET-011..014` |
| 风格结果 | `STYLE: PASS` |
| 检查对象 | 九个 Skill 的 SKILL.md/references/scripts、契约测试、文档证据 |

## 检查清单

- UTF-8、换行、命名、目录归位与尾随空白：已通过 `git diff --check` 复核。
- 九个 Skill 的 SKILL.md 均无旧口径残留，来源优先级统一，禁止过程性输出回显保留。
- 契约测试文件归入 `test/credential-policy/`，文档归入对应 `doc/` 子目录。

## 问题与修复

- 修复：godot-project-bootstrap-rules/SKILL.md 旧口径"不得明文写真实 OPENAI_API_KEY" 改为允许明文写入，禁止过程性输出回显。
- 修复：project-rule-file-bootstrap-rules/SKILL.md 旧口径"不得写入真实密钥" 改为允许写入。
- 修复：imagegen/SKILL.md 旧口径"案例中禁止写入 API key" 改为允许写入。
- 修复：mcp-installation-rules/SKILL.md 旧口径"必须留空由用户自行填写" 改为项目代码/配置默认。
- 修复：authenticated-url-routing-rules/SKILL.md 旧口径"只从本机环境变量读取" 改为项目代码/配置默认。
- 修复：browser-use-cloud-rules/SKILL.md 旧口径"只从本机环境变量读取" 改为项目代码/配置默认。
- 修复：三个 TAPD SKILL.md 的 description 旧口径"提示用户配置 env" 改为项目代码/配置或环境变量。

## 真实测试前置证据

```bash
py.exe -3 -X utf8 -B test/credential-policy/credential_policy_contract_test.py -v
# 结果：3/3 OK + 1 skipped
```

## 检查范围

- 九个 Skill 的 SKILL.md 正文：中文表达、UTF-8 编码、无旧口径残留
- 参考文件（references/scripts）：来源优先级统一
- 契约测试文件：`test/credential-policy/credential_policy_contract_test.py`
- 文档证据：`doc/` 下需求、实施总览、实施周期、测试 README 和 6-review 记录

## 6-review 结论

所有检查项通过，最终放行。
STYLE: PASS

## 图片资产决策

图片资产决策：N/A + 原因：纯规则与文档变更，无视觉产物 + 证据：需求与实施周期文档 Mermaid 图。
