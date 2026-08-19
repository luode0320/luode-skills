# 来源记录（source-notes）

> 归属：`database-schema-rules`。记录外部吸收来源与落点，保证可追溯。

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
