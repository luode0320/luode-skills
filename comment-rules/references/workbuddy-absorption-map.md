# 吸收裁决表（workbuddy-absorption-map）

> 归属：`comment-rules`。记录本 skill 的调整裁决与来源，来源可回指，每行含「整理去重」列。
> 本文件同时承载来源记录（原 `source-notes.md` 职责），避免为单条内部调整新建两个登记文件。

## 内部更新：结构化元数据已承载字段含义时不写行尾重复注释（2026-08-21）

**来源**：内部调整（无外部 skill）。用户在 EllipalFinance-go 项目截图指出 `database/model/db/coinsBrowserUrlDict.go` 的每个字段 tag 里已有 `comment:xxx`，行尾又跟了一遍 `// xxx`，明确要求"已经用 comment 说明了字段，就不需要在后面补充注释"。

**通道**：内部更新通道。**裁决结果**：合并 4 条 / 拒绝 1 条。

| 条目 | 本地现状 | 裁决 | 落点 | 整理去重 |
|------|---------|------|------|---------|
| 字段含义已由同一行结构化元数据（ORM `comment:` tag、schema `description`、IDL 字段说明）承载时，不写行尾重复注释；语义重复即删，不要求逐字相同 | `comment-placement.md` 第 5 条只要求"字段定义处必须写字段含义"，还鼓励在映射处重复补注释，**没有任何例外条款**，是当前重复注释的直接来源 | 合并（作为第 5 条的例外条款紧随其后） | `references/comment-placement.md` | 不新起小节，挂在原第 5 条下形成"规则 + 例外"，避免读者只读到其中一半 |
| 反向规则：元数据缺字段说明、只有行尾注释时，优先把说明补进元数据再删行尾 | 无 | 合并 | 同上 | 与上一条合并为同一组，共用"为什么"（`comment:` 会落进数据库列注释，是强载体；行尾 `//` 只有读该文件的人能看到） |
| 行尾注释仍应保留的边界：单位量纲、枚举取值、业务约束、字段间关系、历史兼容、为什么 | 无（原规则没有"写什么"的收敛，容易被理解成"一律删行尾注释"） | 合并 | 同上 + `references/comment-examples.md` 正例 | 正例用 `Enabled int8 ... // 1=启用 0=禁用` 一行同时演示"删重复"和"留补充"，不写两个样例 |
| schema 侧声明"注释说明"的载体是 `comment:` tag / DDL `COMMENT`，行尾 `//` 不算满足 | `database-schema-rules` 铁律 1 只写"注释说明等写清楚"，未指定载体，与本条存在冲突空间（schema 要求注释、comment 要求不重复） | 合并 | `database-schema-rules` 铁律 1 + `references/schema-boundaries.md` 必声明项第 6 条 | 采用「单一权威 + 引用」：schema 侧只声明载体归属，重复副本的治理规则写"归 `comment-rules`"，不复写判据 |
| 同步写进 `code-generation-style-rules` 通用风格契约 | 该 skill 已约定写码前加载反例库 active 条目 | **拒绝** | — | 拒绝理由同 2026-08-21 表名规则：会形成三处交叉冗余；本条经反例库 `STYLE-CASE-GO-005` 自动并入本轮风格契约 |

**同域冗余扫描（落盘后执行）**：范围 = `comment-rules`、`database-schema-rules`、`code-style-consistency-rules`、`code-generation-style-rules`。① 重复段落：0 处——判据唯一落在 `comment-placement.md`，schema 侧只声明载体并回指，反例库只放正反例；② 门控层叠：0 处——未新增门控，复用 `comment-rules` 既有位置分区；③ 散落产物：新增本登记文件 1 个（归档要求所需，已合并 source-notes 职责以免再多一个文件），无空模板与孤立文件；④ 引用链：`database-schema-rules` → `comment-rules` 位置分区、反例库 → `comment-rules`，均可达。结论 **PASS**。

**净增体积**：`comment-placement.md` +3 行、`comment-examples.md` +18 行（正例 8 + 反例 10）、`comment-rules/SKILL.md` +0 行（两处就地扩写）、`database-schema-rules` +0 行（两处就地扩写）、反例库 +25 行、本登记文件新增。项目侧 `PROJECT_STYLE.md` 为就地扩写既有条目。

**已删除源**：N/A（内部更新通道，无外部安装源）。

**关联**：同日的 [表名单一定义源](../../database-schema-rules/references/workbuddy-absorption-map.md) 裁决出自同一批用户截图反馈，两条规则都指向"同一事实只维护一处"。
