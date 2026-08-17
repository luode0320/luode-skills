---
name: skill-absorption-rules
description: 当用户表达吸收、借鉴、融合、优化外部 skill（如"吸收某个skill的精华""这个skill能不能吸收到我们skill""借鉴XX skill的思路""把XX skill的精华融进我们的skill""优化我们的skill，让skill更强大"），或主动引入外部种子（市场、GitHub、LobeHub、coze、SkillsMP 等来源的 SKILL.md、README、指南）用于改进自有 skill 体系时触发。负责把外部 skill 拆成原子精华、逐条对照本地现状裁决（保留本地/合并/拒绝）、给出落点与简化建议、按 8 维评分与棘轮机制验证改进是否真实成立，并登记吸收裁决表与来源记录；它是外部精华进入自有 skill 体系的唯一总入口。若外部精华已经在本地更强或重复命中，裁决为保留本地并记录理由，不重复吸收。不要用它代替 skill-evolution-rules（内部 gap 演进）、skill-audit-rules（多 skill 职责审计）或具体业务实现。
---

# 外部 Skill 精华吸收规则

只在"用户想把外部 skill 的精华改进我们自己的 skill 体系"时使用这个 skill。
如果当前问题是已有 skill 执行中暴露 gap、需要回补自身，那是 `skill-evolution-rules`；如果是多个 skill 职责重叠、需要审计边界，那是 `skill-audit-rules`；本 skill 只负责"外部种子 -> 吸收裁决 -> 落点 -> 验证 -> 登记"的完整吸收闭环。

## 设计内核（吸收自 darwin-skill 的 5 条核心原则）

> 来源：`alchaincyf/darwin-skill`（GitHub），核心机制受 Karpathy autoresearch 启发：只保留可测量的改进，其余全部回滚。

1. **单一可编辑资产**：每次吸收只改一个 SKILL.md / reference，变量可控、改进可归因；禁止一次吸收同时改多个 skill 再统一验证。
2. **双重评估**：结构评分（静态分析 SKILL.md 写得是否规范）+ 效果验证（跑真实场景看输出是否符合宣称），不只看写得漂不漂亮。
3. **棘轮机制**：分数只能升不能降；吸收后评分低于吸收前基线时自动回滚，不留局部退化。
4. **独立评分**：评分用独立子 agent 执行，避免"自己改自己评"的偏差；关键吸收至少一次独立评分。
5. **人在回路**：每个 skill 吸收完成后暂停，展示 diff 与评分变化，等用户确认再进入下一个 skill / 下一轮。

## Skill 作用与适用场景

- 把用户发现的外部 skill（grill-me、darwin-skill 等任何来源）拆成原子规则，逐条对照本地现状。
- 对每条外部精华做出三态裁决：`保留本地`（本地已有且更强）、`合并`（本地缺失或更弱，值得吸收）、`拒绝`（与本地红线/工作流冲突或为吸收而吸收）。
- 输出吸收落点：哪个 SKILL.md / reference 新增或修改，为什么要放那里，不新增同类 skill 目录（遵循吸收原则：不复制外部整套工作流、不引入外部目录结构）。
- 吸收时顺带检查现有文件是否可简化：合并重复段落、消除冗余引用，净增内容最小化（"不是一直加，吸收后发现可简化也优化简化"）。
- 吸收完成后按 8 维评分跑棘轮验证：新分必须严格高于吸收前基线才保留，否则回滚。
- 更新吸收裁决表（`workbuddy-absorption-map.md` 或本 skill 的裁决记录）与来源记录（`source-notes.md`），保证可追溯。

## 自动触发信号

- 用户说"吸收 / 借鉴 / 融合 / 消化 / 采纳 某个 skill（的精华）到我们的 skill"。
- 用户说"我们发现了这个 skill，能不能吸收""这个 skill 怎么样，值不值得吸收""把 XX skill 的思路用起来"。
- 用户提供外部 skill 的 URL、GitHub 仓库、市场页面、SKILL.md 内容、README 或描述，并要求改进自有 skill 体系。
- 用户说"优化我们的 skill，让它更强大""持续迭代我们的 skill""把外部精华沉淀成规则"。
- 用户说"把 XX skill 的精华总结成/沉淀成我们的 skill"（含将本次吸收经验固化为新 skill 的意图）。
- 当前会话已命中 `skill-evolution-rules` 但根因是"外部有更好种子"，回落到本 skill 走吸收流程。

## 进入后先做什么

1. 先拿到外部 skill 的**原始内容**：优先用 WebFetch 抓取源页面 / 原文，拿不到全文就用 WebSearch 找镜像，再不行让用户贴原文；禁止凭印象"重建"外部 skill 内容。
2. 把外部 skill 拆成**原子规则条目**（每条一句话，可独立判定），写进临时清单，不带着模糊印象做裁决。
3. 对每条对照本地现状：先读目标域 SKILL.md 与其 references，确认本地是否已有同义或更强规则；能查证就不要凭记忆。
4. 产出三态裁决表，明确每条的去留理由，不写"感觉不错"这种无法验证的理由。
5. 给出落点与简化建议后，先与用户确认裁决表，再动手改文件；涉及多 skill 时一次只推进一个。
6. 动手后按 8 维评分跑棘轮验证，向用户展示 diff 与分数变化，等确认再收口。

## 默认执行流程

1. 先读 `references/absorption-decision-matrix.md`，按三态裁决标准逐条判定外部精华。
2. 读取目标域现有 SKILL.md 与 references，确认本地现状；必要时读 `../artifact-storage-rules/references/path-map.yaml` 与 `../artifact-storage-rules/references/update-policy.md` 确认文档落点。
3. 输出吸收裁决表（来源 / 精华 / 本地现状 / 裁决 / 落点），提交用户确认；未确认不落盘。
4. 用户确认后按"单一可编辑资产"原则逐 skill 落盘：新增或修改 reference，同步更新 SKILL.md 的 References 引用；顺带合并目标文件中可简化的重复段落（语义零丢失）。
5. 每个 skill 吸收完成后，先跑结构评分（读 `references/darwin-rubric.md` 的 8 维标准），再用 2-3 个真实场景 prompt 做效果验证；需要独立评分时派子 agent 执行（`parallel-task-dispatch-rules` 协调）。
6. 新分 > 吸收前基线则保留；否则按棘轮机制回滚该次改动（git revert 或恢复文件），并向用户说明回滚原因。
7. 单轮涨幅 < 1 分时自动早停，避免凑分堆冗余；停止本轮吸收，记录"该外部精华与本地位基本持平"。
8. 全部完成后更新吸收裁决表与来源记录，检查文件 UTF-8、引用链一致、无断链；输出收口说明（吸收了什么 / 拒绝了什么 / 简化了什么 / 分数变化）。

## 权责边界与不负责事项

- 只负责外部精华的吸收闭环，不负责内部 gap 演进（`skill-evolution-rules`）、多 skill 职责审计（`skill-audit-rules`）、命中总控（`skill-hit-check-rules`）。
- 不复制外部 skill 的整套工作流、目录结构、`.codebuddy/specs/` 等专属形态；只吸收原子规则。
- 不因为"发现了新 skill"就默认新增独立 skill 目录；优先补现有 skill 的 reference。
- 不把一次性低频特性或与本地红线冲突的内容硬塞进吸收范围。
- 不代替需求、Bug、编码、测试等业务域的执行。

## 需要暂停并确认的条件

- 外部 skill 原文不可得，只能凭印象转述。
- 裁决结果会牵动多个域 / 多个 skill 的大范围改动。
- 吸收目标与现有 skill 职责高度重叠，无法判断该补哪个。
- 用户希望新增独立 skill，但本地已有能力承接。
- 吸收后评分低于基线，需要回滚但改动已跨多个文件。

## 执行通过 / 驳回标准

- 通过：能说清外部 skill 拆成了哪些原子规则、每条三态裁决及理由、落点文件、简化点、8 维评分前后对比，并完成登记与验证。
- 驳回：没有拿到原文就凭印象吸收、裁决表只有"不错/有用"没有理由、吸收后未跑棘轮验证、只增不减导致文件膨胀、或把外部整套工作流原样复制进来。

## 执行结果归档要求

- 吸收裁决表：登记到目标 skill 的 `workbuddy-absorption-map.md`（已有则追加行）；来源 URL / 仓库 / 版本必须可回指。
- 来源记录：目标 skill 的 `references/source-notes.md` 追加吸收来源与落点。
- 案例沉淀：重要吸收完成后，在 `references/case-<skill名>-absorption.md` 留一份 case study，供下次吸收对照。
- 文件校验：新增与修改文件必须 UTF-8、中文无乱码、references 引用可达、无断链；必要时跑 `artifact-delivery-gate-rules` 的文档校验脚本。
- 工作日志：吸收完成后在 `.workbuddy/memory/` 当日日志追加一行摘要。

## references 读取规则

- 默认先读 `references/absorption-decision-matrix.md`（三态裁决标准与反例）。
- 只有做评分验证时再读 `references/darwin-rubric.md`（8 维评分：结构 60 + 实测 40）。
- 只有参考历史吸收案例时再读 `references/case-grill-me-absorption.md`（本次 grill-me 吸收全过程样例）。
- 需要确认文档落点与更新策略时，再读 `../artifact-storage-rules/references/path-map.yaml` 与 `../artifact-storage-rules/references/update-policy.md`。
