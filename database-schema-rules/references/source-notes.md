# 来源记录（source-notes）

> 归属：`database-schema-rules`。记录外部吸收来源与落点，保证可追溯。

## 执行中 gap 回补：存量表纳入 ORM 自动迁移（2026-08-21）

- **来源名称**：内部实践 —— EllipalFinance-go 项目连续两轮真实执行，无外部 skill / URL
- **来源形态**：
  1. 第一轮：把 15 张业务表以正式环境 DDL 为准校准 tag 并全部纳入自动迁移；期间用一次性探针实测
     GORM 1.25.9 + driver mysql 1.8.1 + MySQL 8.0.46 的 tag→DDL 映射（整型宽度、列级字符集、复合主键、
     索引注释、时间默认值），ALTER 条数迭代 252 → 8 → 0
  2. 第二轮：local 启动爆出 `orderUser` 每次迁移失败（`read tcp ... i/o timeout` + `invalid connection`），
     定位为 `AutoMigrate` 为对齐两列缺失的 `COMMENT` 而对 5.6 万行/38.6MB 表反复 `MODIFY COLUMN`
- **gap 判定**：本 skill 原有"自动初始化必须覆盖库/表/索引"的要求，但没有任何"存量表如何纳入""ORM tag
  有哪些陷阱""如何验证迁移不动线上结构"的可执行内容；且原铁律 0 的"失败一律阻断启动"与实践冲突。执行
  全程只能临时推导，属于未来会重复命中的稳定场景，符合 gap 回补条件
- **吸收日期**：2026-08-21
- **落点**：
  - `references/orm-auto-migration.md`（新建，本轮主落点：边界 / 失败分流 / 7 步操作 / 落地形态差异 /
    6 条陷阱 / 五段验证矩阵 / 四类假 PASS 陷阱 / 存量表铁律边界 / 检查清单）
  - `SKILL.md`（铁律 0 修正为场景分流；新增铁律 0.2 只做加法；触发信号 +2；暂停确认 +2；
    通过/驳回标准同步；references 读取规则 +1；并收敛三处铁律重抄）
  - `references/schema-boundaries.md`（新增「铁律的适用范围：新建表强制，存量表不据此改」；两份检查清单合并）
  - `references/migration-safety-and-rollback.md`（加指向新文件的引用，划清人工 DDL 与 ORM 自动迁移的边界）
- **裁决依据**：ORM 自动迁移与人工 DDL 上线是两个不同场景（前者由重启触发、无人值守、面向全部环境），
  原有 references 只覆盖后者。陷阱清单全部为实测结论而非文档推断，故独立成文件并在相邻 reference 留引用；
  已存在的 `ON UPDATE` 规则查证后判为保留本地，新文件只留一行指向，避免交叉重复
- **验证证据**：五段等价性验证全部 PASS（含用真实 local 结构 dump 的段 5，断言对存量列零变更）；
  修复后在真实 local 库闭环 2 秒完成、0 改列语句、无超时

## 内部调整：GORM tag 的 ON UPDATE 写法（2026-08-21）

- **来源名称**：内部调整 —— `database-schema-rules`，新增「GORM tag 时间字段写法（AutoMigrate 幂等性）」规则
- **来源形态**：用户基于 GORM 源码（`gorm.io/gorm` v1.25+ / `gorm.io/driver/mysql` v1.5+ 的 `MigrateColumn` 默认值比对逻辑）验证的经验结论；无外部 skill / URL
- **调整诉求**：不要写成把 `ON UPDATE CURRENT_TIMESTAMP` 放进 `default:` 标签的写法（写法 A 迁移不幂等）；需要 DB 层兜底时放 `type:`，或依赖 autoUpdateTime 不写 DB 层 ON UPDATE
- **吸收日期**：2026-08-21
- **落点**：
  - `SKILL.md`（「进入后先做什么」的 GORM tag ON UPDATE 检查点；按小节名 + 规则名引用，不写条号——
    条号会随后续收敛失效）
  - `references/schema-examples.md`（新增「GORM tag 写法（AutoMigrate 幂等性）」小节：正例 9 + 反例 13）
- **裁决依据**：纯 SQL DDL 中 DEFAULT 与 ON UPDATE 顺序无关，但 GORM tag 位置影响 `MigrateColumn` 比对 → 位置敏感，需独立成条；知识库 `工程实践/数据库表设计规范.md` 同步补一笔
- **状态**：已落盘，无外部源需删除。

## 内部调整：表名单一定义源（2026-08-21）

- **来源名称**：内部调整 —— `database-schema-rules`，新增「表名单一定义源」铁律
- **来源形态**：用户在 EllipalFinance-go 项目的截图 + 文字诉求（model 已有 `TableName()`，repository 仍硬编码同一表名字面量）
- **调整诉求**：表名唯一定义在 model，repository / 访问层直接引用，不重复写字符串
- **吸收日期**：2026-08-21
- **落点**：
  - `SKILL.md`（新增铁律 1.2，同步 description、进入后先做、权责边界、暂停确认、通过/驳回）
  - `references/schema-boundaries.md`（新增「铁律：表名单一定义源」判定标准 + 正反例 + 例外 + 检查清单项）
  - 跨 skill：`database-query-rules`（访问层引用检查，引用本 skill 为定义权威）、`code-style-consistency-rules/references/user-style-feedback-library.md`（STYLE-CASE-GO-004）
- **裁决依据**：表名是 schema 属性，定义权威归本 skill；访问层引用属 query 域。拒绝在 `code-generation-style-rules` 重复落条，避免三处交叉冗余。
- **状态**：已落盘，无外部源需删除。

## design-db__skillhub（2026-08-19 吸收）

- **来源名称**：design-db（[PRD2PLAN] 数据库表结构设计规范）
- **来源形态**：skillhub 市场安装包（`C:\Users\luode\.workbuddy\skills\design-db__skillhub`，9KB 单文件 SKILL.md）
- **来源版本**：无显式版本号；安装时间 2026-08-19 22:36
- **来源 URL**：skillhub 本地安装，无外部 URL 可回指（`_skillhub_meta.json` 记录市场元数据）
- **吸收日期**：2026-08-19
- **落点**：
  - `references/table-design-standards.md`（新增，主落点）
  - `SKILL.md`（新增铁律 6：禁止物理外键，逻辑外键列必须建索引；references 读取规则更新）
- **裁决依据**：用户个人规则「禁止外键」纳入为铁律 6；金额类型按本地铁律 2（强制字符串）改写外部 DECIMAL 建议。
- **状态**：已吸收，源 skill 已删除。
