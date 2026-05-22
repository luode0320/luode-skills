# 项目专属 Skill 拆分边界

## 目标

把项目经验沉淀为“可触发、可执行、可复用”的小 skill 集合。

## 拆分原则

- 一类主题一个 skill，避免大而全。
- 优先按“代码位点 + 业务能力 + 工具包”拆分。
- 每个 skill 只回答一个核心问题：什么时候触发、解决什么。

## 推荐主题

- `code-style-rules`：项目代码风格、目录约束、常见禁用写法。
- `enum-static-usage-rules`：静态属性枚举与常量映射约束。
- `string-number-conversion-rules`：字符串与数字转换工具包约定。
- `time-conversion-rules`：时间格式、时区、时间戳互转约定。
- `goroutine-usage-rules`：协程创建、回收、错误处理约定。
- `http-package-rules`：HTTP 请求、超时、重试、错误处理约定。
- `api-writing-rules`：接口路径、请求响应结构、幂等与版本约定。
- `database-query-rules-project`：项目特有 SQL/ORM 查询约束。
- `mongo-usage-rules`：Mongo 集合访问和索引约定。
- `redis-usage-rules`：缓存 key 设计、过期策略、并发保护。
- `polaris-config-rules`：北极星配置读取、隔离与降级约定。

## 最小交付

每个子 skill 至少包括：

- `SKILL.md` frontmatter：`name`、`description`
- 主体：触发信号、默认流程、边界、通过标准

