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

## 2026-08-23：外部吸收——cd-debug（调试排错特工）

- **来源**：外部吸收通道，skillhub 市场 `cd-debug__skillhub`（调试排错特工 v1.0.0，作者 smart，2026-08-23 安装）。
- **吸收诉求**：吸收其「定位报错根因，给最小改动的修复方案」中的**最小改动部分规则**。
- **拆解原子条目数**：7 条。

| # | 外部精华 | 本地现状 | 裁决 | 落点 / 理由 |
|---|---------|---------|------|------------|
| 1 | 定位报错根因，给最小改动的修复方案（核心承诺） | `bug-root-cause-rules`（根因定位）+ `bug-fix-proposal-rules`「根因修复优先（反打补丁式修复）」+ 本 skill minimal-change 三件套 | 保留本地 | 本地覆盖更全更具体、经真实场景验证 |
| 2 | 最小改动 = 不引入无关改动 ≠ 表层贴补丁；根因必需改动不算越界；较大重构提方案等确认 | `bug-fix-proposal-rules`「与最小改动的协调」小节逐字等价；`minimal-change-general.md` 允许/应排除改动清单更细 | 保留本地 | 本地更强 |
| 3 | 生成代码须人工审查后上线；不自动执行破坏性操作 | `code-change-finalization-gate-rules` + `git-collaboration-rules` + `skill-execution-compliance-gate-rules` | 保留本地 | 本地为可执行门控，非一句话声明 |
| 4 | 结构化交付卡（需求/方案/代码/测试/说明） | `artifact-delivery-gate-rules`（validate 脚本）+ `code-change-finalization-gate-rules` | 保留本地 | 本地有机器校验，更强 |
| 5 | 万能触发词（写代码/写个脚本/帮我实现/debug 等） | 本地按域细分触发（bug-intake / requirement-intake / code-generation-style 各司其职）+ `skill-hit-check-rules` 强制总控 | 拒绝 | 与本地触发体系冲突，抢触发降精度 |
| 6 | Pay Skill 付费升级规划（专业版/计费通道） | 本地为开源规则体系 | 拒绝 | 商业形态不迁移 |
| 7 | 免责声明（辅助性结果、人工复核） | `artifact-delivery-gate-rules` 已有人工复核红线 | 保留本地 | 本地已覆盖 |

- **落盘改动**：无（0 条合并，本地已全覆盖且更强；按棘轮原则不因"为吸收而吸收"新增内容）。
- **整理去重**：N/A + 理由：无合并条目，目标文件无新增内容，无存量可清。
- **同域扫描结论**：范围 = 编码/Bug 域相邻 skill（bug-fix-proposal-rules / bug-root-cause-rules / code-quality-rules 自身 / code-change-finalization-gate-rules / artifact-delivery-gate-rules / skill-execution-compliance-gate-rules / git-collaboration-rules）。7 条外部精华逐一对照，0 条触发新增落盘，无新增重复段落、无门控层叠、无散落产物；**PASS**。
- **净增体积**：0 bytes（无落盘改动）；仅登记文件追加。
- **棘轮验证**：无代码改动，8 维评分与基线持平，无回退风险。
- **源删除**：已删除用户级 `C:\Users\luode\.workbuddy\skills\cd-debug__skillhub\` 与工作区 `D:\谷歌云盘\luode-skills\cd-debug__skillhub\` 两份安装源（删除前 md5 指纹一致，SKILL.md 全文已留档于本裁决表上下文）。