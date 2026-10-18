---
schema_version: 1
doc_id: REVIEW-IMAGEGEN-CONCURRENCY-001
doc_type: style_regression
template_version: 1
source_ids:
  - SRC-IMAGEGEN-CONCURRENCY-001
version: 1
current_slice: 并发生图核验与技能规则更新
updated_at: 2026-10-19
status: accepted
unresolved_decisions: 0
reader_level: business_general
writing_style: plain_chinese
appendix_policy: preserve_existing_or_one_terminal_appendix
---

# 6-review 风格回归：imagegen 并发生图默认化

结论：本轮通过风格回归，`STYLE: PASS`；影响：仅 `imagegen` 技能规则与字典产物；范围：`imagegen/SKILL.md`、`skill-dictionary/data.js`、`字典.md`；非范围：脚本逻辑、配置、其他 skill；变化：多图默认并发、内置通道明确标注不并发；完成标准：结构校验、真实并发测试、知识库校验全部通过；术语说明：内置通道指宿主 `ImageGen` 工具；验证状态：已执行并通过。

## 1. 文档信息

- 对应任务：验证 imagegen 是否支持并发生图，并按结论调整规则。
- 检查时间：2026-10-19
- 检查范围：本轮全部规则改动与生成产物

## 2. 检查范围

| 文件 | 改动性质 | 是否代码 |
| --- | --- | --- |
| `imagegen/SKILL.md` | 判定思路、工作流、并发生图章节 | 否（规则文档） |
| `skill-dictionary/data.js` / `字典.md` | 字典重生成 | 否（生成物） |
| `PROJECT_CURRENT.md` | 任务投影与当前状态 | 否（项目状态） |

脚本 `imagegen/scripts/image_gen.py` 本轮未改动，仅阅读核验。

## 3. 真实测试前置证据

- `generate-batch --concurrency 1`：3 张 78.3s。
- `generate-batch --concurrency 3`：3 张 33.1s，无 429。
- `generate-batch --concurrency 5`：5 张 36.5s，无 429。
- 内置通道同轮 3 次调用：完成时间戳间隔约 11s，串行。
- 产物校验：11 张 PNG，1254×1254 RGB，sha256 互不相同。

## 4. 交付残留自查（6 维）

| 维度 | 结论 | 证据 |
| --- | --- | --- |
| 维度 1 需求覆盖对账 | 通过 | 用户诉求「核验并发是否支持→支持则改为默认并发」→ 落点 `imagegen/SKILL.md` 判定思路 #2/#3、工作流 4.1、并发批量通道章节；实测数据表在 §「已验证事实」 |
| 维度 2 影响面 / 消费方对账 | 通过 | `grep -rn "generate-batch\|--concurrency"` 全仓扫描，除 SKILL.md 与脚本本体外零命中，无其他消费方需同步 |
| 维度 3 残留物清扫 | 通过 | `git status --porcelain` 逐项归类：临时 b64/contact sheet/jobs.jsonl 已删除；测试产物保留在 `images/concurrency-test/parallel5/` 与 `vibe_images/`（未跟踪，供用户核验，不属交付资产） |
| 维度 4 文档与引用一致性 | 通过 | 新增章节已被字典收录（`sections` 含「并发批量通道（OpenAI 兼容端点，默认多图路径）」）；知识库新笔记已挂 MOC，`dead_link_count: 0` |
| 维度 5 口径一致性 | 通过 | 并发默认值 5、上限 25、失败上限 3 在 SKILL.md 参数表与脚本 `DEFAULT_CONCURRENCY=5` / 校验区间 `1–25` / `--max-attempts 3` 三处一致；耗时数字在 SKILL.md 与知识库笔记一致 |
| 维度 6 验证有效性反审 | 通过 | 耗时来自真实 wall clock 而非退出码；哈希互不相同排除复制产物；并发与串行用同一 JSONL、同一参数对照；内置通道结论来自完成时间戳间隔而非「调用成功」 |

## 5. 风格检查

- 修改沿用原文件既有中文小节风格与 Markdown 表格结构，无批量重排。
- 新增内容无未使用引用、无临时调试段落、无占位符。
- 数字与命令均可在脚本中找到对应实现（`DEFAULT_CONCURRENCY`、`--concurrency`、`--max-attempts`、`--fail-fast`）。

`STYLE: PASS`
