# 吸收裁决表

> 本文件记录 `skill-execution-compliance-gate-rules` 的 Skill 吸收历史。来源包括外部市场 Skill、内部调整、执行中 gap 回补。

| 日期 | 来源 | 条目 | 本地现状 | 裁决 | 落点 | 整理去重（含同域清理） | 环境依赖 | agent 通用性 |
|---|---|---|---|---|---|---|---|---|
| 2026-09-12 | 内部调整（用户会话） | 收口前遗留在影响面 / 需求覆盖 / 计划外残留三处无覆盖，需一次以真实变更集为输入的横切自查 | 无对应机制；现有 5 个收口 gate 均为单维度消费型对账，只校验「是否执行」 | 合并 | `references/delivery-residue-self-check.md`（新建）；`SKILL.md` 承载条目；`code-change-finalization-gate-rules/SKILL.md` 消费条目（维度 2 / 3 / 6） | 无（新文件零存量冗余）；与 `applicability-and-gap-check.md` 划清正反推导边界，避免门控层叠；同域扫描结论见 `references/source-notes.md` | `N/A + 理由：纯规则文本，不依赖环境变量 / hook / 依赖安装 / 路径引用` | 通用 |
