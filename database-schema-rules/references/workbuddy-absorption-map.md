# 吸收裁决表（workbuddy-absorption-map）

> 归属：`database-schema-rules`。记录外部 skill 精华的吸收裁决，来源可回指，每行含「整理去重」列。

## design-db__skillhub（2026-08-19）

**来源**：本地安装 `C:\Users\luode\.workbuddy\skills\design-db__skillhub`（skillhub 安装，9KB SKILL.md，无 references）。数据库表结构设计规范，PRD2PLAN 体系。

**裁决结果**：合并 ≈20 条 / 保留本地 2 条 / 部分合并 2 条。

| 外部精华 | 裁决 | 落点 | 整理去重 |
|---------|------|------|---------|
| 表/列/索引命名约定（小写+下划线、复数表名、`idx_`/`uk_` 前缀） | 合并 | `references/table-design-standards.md` 一、命名约定 | 本地此前无命名规范，纯新增 |
| 必备字段 + 审计字段三风格选型（at/by、time/creator、gmt_create） | 部分合并 | 同上一、二；created_at/updated_at 本地铁律 3 更强，仅补审计选型 | 复用本地铁律，不重复 created_at/updated_at 定义 |
| 数据类型选型表（BIGINT/VARCHAR/TEXT/JSON/DATETIME/DATE/CHAR） | 合并 | 同上三、数据类型选型 | 金额 DECIMAL(18,2) 拒绝（本地铁律 2 强制字符串），表中改为本地红线 |
| 索引设计（必建场景/组合索引/覆盖索引/禁忌） | 合并 | 同上四、索引设计 | 与 `schema-examples.md` 正例 6 交叉引用，不重复示例 |
| 约束设计（NOT NULL/DEFAULT/UNIQUE/CHECK） | 部分合并 | 同上五、约束 | 必声明项与本地检查清单重叠，仅补 CHECK 示例 |
| 外键策略（物理/逻辑二选一） | 拒绝（物理外键）+ 合并（逻辑外键） | 同上五 + SKILL.md 新增铁律 6 | 按用户个人规则「禁止外键」改为红线：禁止物理外键，逻辑外键列必须建索引 |
| 表设计（3NF/反范式/纵向横向拆分） | 合并 | 同上六 | 纯新增 |
| 关系映射（1:1/1:N/N:M/树形/版本化 + 关联表规则） | 合并 | 同上七 | 纯新增 |
| 软删除选型（is_deleted/deleted_at/ORM 过滤/唯一约束含 is_deleted） | 部分合并 | 同上八 | 本地铁律 5 强制 is_deleted 更强；补 ORM 自动过滤与唯一约束细节 |
| 迁移文件命名 `V{版本}__{描述}.sql` | 合并 | 同上九 | 迁移安全细则复用 `migration-safety-and-rollback.md`，不重复 |
| 常见设计模式（配置驱动表/多对多+属性/审计日志表） | 合并 | 同上十 | 低优先参考，简表收录 |
| 严禁清单 | 合并（本地化改写） | 同上「严禁清单」 | 剔除与本地冲突项（金额数值类型改为本地字符串红线），新增物理外键禁止项 |

**整理去重统计**：本地 `database-schema-rules` 此前无命名/类型/索引/关系规范，本次净增 1 个 reference（约 230 行）；通过与 `schema-boundaries.md`、`schema-examples.md`、`migration-safety-and-rollback.md` 交叉引用，避免重复示例，SKILL.md 仅新增铁律 6 及相应读取规则。

**已删除源**：`C:\Users\luode\.workbuddy\skills\design-db__skillhub`（吸收完成后删除）。
