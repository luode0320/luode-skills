# 吸收裁决登记（workbuddy-absorption-map）

> 归属：`requirement-intake-rules`。本文件登记本 skill 的历史外部吸收裁决，供回指与防重复吸收。每次吸收在此追加一行；来源 URL / 仓库 / 版本必须可回指。

## 吸收记录

| 日期 | 外部来源 | 版本 | 原子条目数 | 合并 | 保留本地 | 拒绝 | 整理去重 | 同域扫描 | 落点 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-09-05 | `@clawhub_je44/need`（skillhub 市场，本地源 `need__skillhub/` 已删除） | 0.1.4 | 8 | 2（N3b 范围优先级缺失、N3c 受众/角色缺失） | 6（N1/N2/N3a/N4/N5/N6，本地更强） | 0 | 目标文件 `missing-info-checklist.md` 为清单体、逐条独立无冗余段，无伴生删减（N/A + 文件本身精简） | 扫描范围：requirement-intake-rules / bug-intake-rules 同域；发现 0 处交叉冗余；清理 0 处；PASS | `references/missing-info-checklist.md`「常见缺失项」+2 行（净增 +2 行，约 +120 字节） |

## 裁决细节（2026-09-05，need）

need 的核心追问机制（想法模糊时先判断缺什么 → 只追问 3-7 个关键问题 → 补目标/场景/输入输出/成功标准/约束 → 信息足才出方案 → 短/直接/结构化/不乱补设定）在本地已有更强覆盖，逐条裁决：

- 保留本地：N1 触发判定 → `gap-routing`（需求）/ `bug-intake-rules#discovery-and-gap`（Bug）；N2 问题数量与组织 → 本地"一次一个真实缺口 + 推荐答案 + 魔鬼代言人"（`adversarial-gap-interview.md`）更严格；N3a 补齐维度主体 → `missing-info-checklist.md` 已列 12+ 项；N4 信息组织 → `initial-discovery-output-template.md` + gap 临时缺口文档（本地有落盘机制且更强）；N5 时机门控 → 缺口未清零不进规划/编码 + 质量门 90 分 + P0/P1 blocked；N6 输出纪律 → AGENTS.md 禁止脑补结论红线 + `plain-language-document-contract`。
- 合并：N3b「范围优先级缺失：must-have vs nice-to-have」与 N3c「受众/角色缺失」为本地缺失信息清单未显式列出的维度，补入 `missing-info-checklist.md`「常见缺失项」。
- 拒绝：无。
