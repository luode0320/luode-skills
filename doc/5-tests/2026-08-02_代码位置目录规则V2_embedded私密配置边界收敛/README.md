---
schema_version: 1
doc_id: "TEST-PSR-CONFIG-SECRET-001"
doc_type: "test"
source_ids: ["REQ-PSR-CONFIG-SECRET-001", "CYCLE-PSR-19-001"]
status: accepted
version: "v1.0"
current_slice: "CYCLE-19 embedded 私密配置边界测试"
updated_at: "2026-08-02"
template_version: 1
reader_level: business_general
writing_style: plain_chinese
appendix_policy: preserve_existing_or_one_terminal_appendix
---

# embedded 私密配置边界测试证据

结论：本轮验证两类后端 embedded 允许源码内私密配置，源码优先且默认不依赖环境变量；YAML 仍禁止秘密原值。影响：仅验证目录规则的机器元数据和文档契约，不执行具体后端加载器。范围：配置专项测试、Catalog/Schema 解析和脱敏文字断言。非范围：真实密钥、外部服务和 Git 历史。变化：新增三项策略字段断言。完成标准：专项测试和根测试通过。术语说明：embedded 是源码内 YAML 字符串配置。验证状态：配置专项、package-structure-rules 回归和根 `test/` 子目录回归均通过。

## 文档信息

| 字段 | 内容 |
|---|---|
| 文档 ID | `TEST-PSR-CONFIG-SECRET-001` |
| 关联需求/周期 | `REQ-PSR-CONFIG-SECRET-001` / `CYCLE-PSR-19-001` |
| 测试代码 | `test/package-structure-rules/configuration_layout_test.py` |
| 环境边界 | 仅本地 Python、临时目录和仓库文件 |

## 完成标准

配置策略断言、根测试子目录回归、脱敏扫描和文档 profile 全部通过；测试不读取真实密钥，不连接外部服务，不写入 Git 历史。

## 测试入口与样本

| 测试 ID | 命令 | 样本/断言 | 结果 |
|---|---|---|---|
| `TEST-PSR-CONFIG-SECRET-001` | `python -X utf8 test/package-structure-rules/configuration_layout_test.py` | backend/fullstack 四类 query、策略字段和 reference 文本 | `7/7 PASS` |
| `TEST-PSR-CONFIG-SECRET-002` | 同上 | YAML `forbid_plain_secret`、embedded `allow_plain_secret` | `7/7 PASS` |
| `TEST-PSR-CONFIG-SECRET-003` | `python -X utf8 -m unittest discover -s test/package-structure-rules -p '*_test.py'` | 配置目录正负 fixture、策略和 init 回归 | `16/16 PASS` |
| `TEST-PSR-CONFIG-SECRET-004` | 按根 `test/` 子目录逐项 discover | 既有治理、资产、任务计划和浏览器规则回归 | `212/212 PASS` |

## 安全与环境边界

- 所有 fixture 使用脱敏占位文本，不读取或写入真实 API key、密码、token、私钥或连接串。
- 测试仅使用本地 Python、仓库文件和临时目录，不连接数据库、缓存、HTTP/RPC 上游或非 local 环境。
- 输出、报告和本 README 不包含任何秘密原值。

## 清理、回滚与证据

- `TemporaryDirectory` 自动清理临时 fixture；不保留缓存、投影或运行输出。
- 失败时只回滚本轮测试文档和策略断言，不触碰既有 CYCLE-17/CYCLE-18 文件。
- 图片资产决策：N/A + 原因：无视觉验收；Mermaid 图已在 CYCLE-19 文档表达流程。

## 追踪入口

`REQ-PSR-CONFIG-SECRET-001` -> `CYCLE-PSR-19-001` -> `TASK-19-03/04` -> `TEST-PSR-CONFIG-SECRET-001..004`。
