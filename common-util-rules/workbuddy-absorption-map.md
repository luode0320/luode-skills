# 吸收裁决表（workbuddy-absorption-map）

> 归属 owner：`common-util-rules`（本表由 common-util-rules 维护）。
>
> 本 skill 登记 2026-09-11 起针对本 skill 的内部更新与外部吸收。所有调整沿用 `skill-absorption-rules` 的三态裁决、整理去重与同域扫描要求；只增不减视为不合格。

## 2026-09-11 内部更新：纯转换工具函数落点 + 公共工具索引文档契约

来源：用户会话提出——AI 辅助开发瓶颈已从"逻辑正确性"转向"代码质量"，其九维清单中第 8 维「纯转换工具函数的定义位置」与第 9 维「工具函数索引文档规范」在本 skill 内均无承接。经全仓基线侦察确认：`util-placement.md` 只有"可独立复制 → `utils/<pkg>` / 需项目依赖 → `common/util`"的二分，未点名"纯转换"判据；索引侧现有四层全是目录 / 类别级（`placement-catalog.yaml`、CLI `guide`、`directory-usage-routing.md`、`usage-recipes-go.md`），函数级索引为零。

用户裁决口径：① 索引形态 = **约定项目内索引契约**（不在规则仓新建平行索引文件）；② 纯转换函数 = **单独点名判据**。

| 来源 | 调整条目 | 本地现状 | 裁决 | 落点 / 理由 | 整理去重 |
| --- | --- | --- | --- | --- | --- |
| 用户需求（第 8 维） | 纯转换工具函数判据：确定性 / 无副作用 / 无 IO / 无项目依赖，全满足必进根 `utils/<pkg>/`；需项目依赖降级 `common/util/<函数>.<ext>` | `util-placement.md` 只有"可独立复制 vs 高关联"的二分，无"纯"的硬判据 | 合并 | `references/util-placement.md` 新增「纯转换工具函数的落点（点名判据）」小节 | 与既有二分合并为同一条落点链路（纯 → utils / 依赖 → common/util / 带业务语义 → 业务层），不新增平行条目 |
| 用户需求（第 9 维） | 项目内函数级公共工具索引的契约：落点、字段、更新时机、与既有索引层的边界 | 零基线；既有四层索引均为目录 / 类别级 | 合并 | `references/util-index-doc-contract.md`（新建） | 边界表显式声明不复制 `placement-catalog.yaml` / `guide` / `directory-usage-routing.md` / `usage-recipes-go.md` 的职责 |
| 强制接入 | 新增 / 修改导出工具函数后须同轮同步索引 | `复用红线` 只要求"新增前检索"，无"新增后登记" | 合并 | `SKILL.md` 复用红线 +1 条、默认执行流程 +1 步、references 读取规则 +1 条、description 补契约 | 作为复用红线的闭环另一半（检索 → 复用 → 登记），不改写既有红线 |

**净增/净减**：`util-index-doc-contract.md` +1 新文件；`util-placement.md` +1 小节 + 用途句改写；`SKILL.md` 复用红线 +1 条、默认执行流程 +1 步、references 读取规则 +1 条、description 补 1 句；无删除。

**同域冗余扫描**：范围 {common-util-rules 自身, package-structure-rules, code-quality-rules, architecture-doc-rules, artifact-storage-rules, naming-rules}。结论：
- `package-structure-rules` 的 `directory-usage-routing.md` 是**规则仓自用**目录级索引，`usage-recipes-go.md` 是规则仓自用类别级 recipe，均非本契约的项目侧副本；本契约在边界表显式声明，零逐字重复。
- `code-quality-rules` 的 `code-removal-discipline.md` 管删除纪律，本契约"删除函数先删索引行"只做引用，不复制正文。
- `architecture-doc-rules` / `artifact-storage-rules` 管 `doc/1-架构/` 主入口命名与序号，本契约只借用既定入口位置，不复制命名规则。
- 全仓关键词扫描（"公共工具索引 / util-index-doc-contract / 纯转换工具函数"）除本 skill 与工作日志外 0 命中。
- 发现 0 处逐字重复、0 处门控层叠、0 处散落产物；**PASS**。

**棘轮评分**：内部更新通道按最小回补执行（非外部吸收，不适用 8 维评分基线对比；改动为规则补齐，覆盖两个原 0 分维度"纯转换函数落点""函数级索引契约"，无回退）。

**源删除**：无（内部更新通道）。

**附带修复**：`package-structure-rules/references/directory-usage-routing.md` 第 19 行原将 `utils/decimal/` 行与 `utils/cache/redis/` 行挤在同一行（缺换行），Markdown 表格已破损，本轮拆回两行恢复。属"更新优化"顺手修复，登记见 `package-structure-rules/references/source-notes.md` 2026-09-11 段落。
