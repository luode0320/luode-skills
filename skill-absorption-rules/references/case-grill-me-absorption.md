# Case Study：grill-me 吸收（2026-08-18）

> 归属 owner：`skill-absorption-rules`。本文件是"外部 skill 精华吸收"的完整参考样例，下次吸收任何 skill 时对照本案例的流程与产物形态执行。

## 来源

- 外部 skill：`softspark-ai-toolkit-grill-me`（LobeHub，v1.0.1）
- 定位：深度追问式方案审查，逐层拆解设计决策直到达成共识
- 获取方式：WebSearch 找到 3 个镜像源（LobeHub / Gitea / SkillsMP），WebFetch 抓取原文 SKILL.md 与规则

## 精华拆解（原子规则 9 条）

1. 对抗式审查：目的不是通过，是找出漏洞
2. 一次只问一个问题
3. 每个问题附推荐答案（供确认）
4. 决策树逐层拆解：先核心依赖后细节分支
5. 能从代码库查证就不问用户
6. 不满足于模糊答案
7. 挑战假设，不只表面决策
8. 魔鬼代言人（Devil's Advocate）反方批评
9. 直到达成共识

## 三态裁决

| # | 外部精华 | 本地现状 | 裁决 | 落点 / 理由 |
| --- | --- | --- | --- | --- |
| 1 | 对抗式审查 | 缺口路由偏"识别缺失"，无对抗姿态 | 合并 | `requirement-intake-rules/references/adversarial-gap-interview.md` |
| 2 | 一次只问一个问题 | gap-routing 已有同义规则 | 保留本地 | `requirement-intake-rules/references/gap-routing.md` |
| 3 | 每问附推荐答案 | 本地只列待确认项 | 合并 | `adversarial-gap-interview.md` |
| 4 | 决策树依赖优先 | 有建议确认顺序，非显式依赖树 | 合并 | `adversarial-gap-interview.md` |
| 5 | 能查证就不问 | initial-discovery 完整路由更强 | 保留本地 | `initial-discovery-route.md` |
| 6 | 不满足模糊答案 | 极致完整性标准更强 | 保留本地 | `extreme-completeness-standard.md` |
| 7 | 挑战假设 | 本地无显式反方批评 | 合并 | `adversarial-gap-interview.md` + `implementation-planning-rules/references/plan-devils-advocate-review.md` |
| 8 | 魔鬼代言人 | 本地无对抗姿态 | 合并 | 同上（双域落点） |
| 9 | 直到共识 | 确认后回填主文档 | 保留本地 | `gap-routing.md` |

**拒绝项**：破冰寒暄（"最喜欢的电影"式开场）——与本地工程化文档体系不兼容，为吸收而吸收。

## 落点与简化

- 需求域：新增 `adversarial-gap-interview.md`（对抗式缺口追问：推荐答案 + 魔鬼代言人 + 依赖优先）；SKILL.md 与 gap-routing.md 引用挂接。
- 实施域：新增 `plan-devils-advocate-review.md`（方案反方批判 7 维）；`plan-review-checklist.md` 新增"反方批判检查"节；SKILL.md 引用 + source-notes.md 记录来源。
- 简化：gap-routing.md 原"进入后先做什么"(8条)+"默认执行流程"(13条) 重叠约 40%，合并为"执行流程"11 条，语义零丢失；顺手修掉 `implementation-planning-rules` 重复列举笔误。
- 登记：`implementation-planning-rules/references/workbuddy-absorption-map.md` 新增 7 行裁决（3 合并 / 4 保留本地）。

## 验证

- 8 个文件全部 UTF-8 干净，无乱码迹象。
- 引用链 9 项全 PASS（SKILL.md → reference、reference → reference 双向可达）。
- 无断链：无其他文件引用被合并的章节名（"进入后先做什么"/"默认执行流程"）。
- 本次未跑 8 维评分（吸收发生在 darwin-rubric 建立之前）；后续吸收必须补跑棘轮验证。

## 关键约定（沉淀为本 skill 的规则）

- 推荐答案只作"供确认建议"，不得写成已确认结论；与"禁止 Agent 猜测"兼容。
- 反方批评只针对方案不针对人，≤3 条按严重度排序，避免无限抬杠。
- 先核心依赖后细节分支；依赖未定的下游缺口保持 `blocked`。
- 吸收时"不是一直加"：发现本地可简化处顺带合并，净增内容最小化。
