# 数据访问层边界

## 用途

用于区分 SQL、Repository、DAO、Mapper、QueryBuilder 和业务层的职责。

## 属于 query 域

- SQL 查询与写入实现
- Repository / DAO / Mapper / QueryBuilder 的访问封装
- 分页、排序、过滤、批量 CRUD 的访问细节
- 事务入口、锁选择和访问层错误边界

## 不属于 query 域

- 表结构、字段设计、DDL、迁移
- 缓存 key、缓存读写和缓存失效策略
- 复杂业务编排、权限规则、领域规则判断
- 环境连接信息和配置分层

## 检查清单

- 当前逻辑是否真的是数据访问职责
- 当前访问层是否泄露了业务语义
- 当前分页、过滤、排序是否稳定可解释
- 当前问题是否应回流 schema 或缓存层
