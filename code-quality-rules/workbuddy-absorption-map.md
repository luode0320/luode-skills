# 吸收裁决表（workbuddy-absorption-map）

> 归属 owner：`code-quality-rules`（本表由 code-quality-rules 维护）。
>
> 本 skill 登记 2026-08-23 起针对本 skill 的内部更新与外部吸收。所有调整沿用 `skill-absorption-rules` 的三态裁决、整理去重与同域扫描要求；只增不减视为不合格。

## 2026-08-23：内部更新——删除纪律（remove 语义）

- **来源**：内部调整：`code-quality-rules`，调整诉求 = "删除代码/功能时必须彻底删除，禁止 xxxv2 备份版本，禁止记忆残留'禁止使用'描述"（用户痛点：agent 把删除执行成废弃）。
- **形态**：内部更新通道（无外部源可删）。
- **拆解原子条目数**：4 条。

| # | 内部诉求 | 本地现状 | 裁决 | 落点 / 理由 |
|---|---------|---------|------|------------|
| 1 | 删除代码/功能必须彻底（remove 语义） | 最小改动主线有"阻断顺手清理旧代码"约束（防多删），无"被要求删的要删干净"（防少删） | 合并 | `code-quality-rules/references/code-removal-discipline.md`（新建） |
| 2 | 禁止创建 xxxv2 备份版本 | 无任何 skill 覆盖 | 合并 | 并入 code-removal-discipline.md |
| 3 | 禁止在记忆写入"强制删除/禁止使用"残留描述 | `project-memory-rules` 生命周期有 active/deprecated/stale/conflicted/retired，但删除场景未明确 | 合并 | `project-memory-rules/SKILL.md` 写入规则补一条（引用 code-quality-rules 权威） |
| 4 | 删除需同步清引用、测试、配置、文档提及 | 无专门覆盖 | 合并 | 并入 code-removal-discipline.md「全链路清理清单」 |

- **落盘改动**：
  - 新增 `code-quality-rules/references/code-removal-discipline.md`（3,757 bytes）。
  - 修改 `code-quality-rules/SKILL.md` 最小改动主线核心约束补一条（最后一条）+ references 读取规则补一条。
  - 修改 `project-memory-rules/SKILL.md` 写入规则补一条（联动约束，引用 ../code-quality-rules/.../code-removal-discipline.md）。
- **整理去重**：N/A + 理由：本地最小改动主线已有"阻断顺手清理旧代码"约束，本轮新增"被要求删的删干净"是其互补面（一防多删、一防少删），未与既有约束形成重复段落；references 目录无其他删除相关 reference，无需清理。
- **同域扫描结论**：范围 = 编码域相邻 7 skill（code-generation-style-rules / code-change-finalization-gate-rules / code-context-resync-rules / code-quality-rules 自身 / requirement-change-rules / project-style-rules / artifact-storage-rules / project-memory-rules 自身）。执行 `references/source-notes.md` 同款精确扫描脚本（关键词：禁止创建/禁止备份/彻底移除/全链路清理/remove 语义/删除版本 等 9 个），结果：除本次新落盘的 `code-quality-rules/SKILL.md` 自身段落外，其他相邻 skill 0 命中。发现 0 处重复段落、0 处门控层叠、0 处散落产物；**PASS**。
- **净增体积**：+约 3,757 bytes（新文件）+ 约 280 bytes（两处 SKILL.md 小节）+ 约 220 bytes（project-memory-rules 写入规则一条），共约 +4,257 bytes；引用式接入，吸收即整理因本轮为零基线无存量可清，不构成膨胀。
- **棘轮验证**：
  - 3 个落盘文件 UTF-8 全部 PASS。
  - 引用链 PASS：`code-quality-rules/SKILL.md` → `references/code-removal-discipline.md` 存在；`project-memory-rules/SKILL.md` → `../code-quality-rules/references/code-removal-discipline.md` 可达。
  - 8 维评分（darwin-rubric）估计：与基线持平或略升（新规则覆盖一个原 0 分维度"删除完整性"，不破坏既有契约）；无回退。