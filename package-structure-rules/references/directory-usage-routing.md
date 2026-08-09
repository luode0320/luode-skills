# 目录用法索引

本文档是 `package-structure-rules` Catalog 的用法索引，用于从目录出发快速定位关联 skill 和 recipe 示例。文档不替代各专业 skill 的具体编码规则，只做索引和转发。

## 用法查询流程

1. 优先使用 CLI 查询：`python placement_catalog.py guide --category <category> --language go`
2. 文档手动查询回退：按下方分类表查找目录、关联 skill 和 recipe

## 目录 -> 关联 skill 映射

### `utils/` 工具包

| 目录 | 关联 skill | recipe 索引 |
| --- | --- | --- |
| `utils/time/` | `time-util-rules`、`common-util-rules` | `usage-recipes-go.md#time` |
| `utils/convert/` | `common-util-rules` | `usage-recipes-go.md#convert` |

| `utils/decimal/` | `common-util-rules`、`database-query-rules`、`database-schema-rules` | `usage-recipes-go.md#decimal` || `utils/cache/redis/` | `common-util-rules` | `usage-recipes-go.md#cache-redis` |
| `utils/cache/mongo/` | `common-util-rules` | 暂无 |
| `utils/http/` | `common-util-rules` | `usage-recipes-go.md#http` |
| `utils/async/` | `common-util-rules` | 暂无 |
| `utils/json/` | `common-util-rules` | `usage-recipes-go.md#json` |
| `utils/log/` | `common-util-rules` | `usage-recipes-go.md#log` |
| `utils/ip/` | `common-util-rules` | 暂无 |
| `utils/cron/` | `common-util-rules` | 暂无 |
| `utils/discovery/polaris/` | `common-util-rules` | 暂无 |
| `utils/discovery/nacos/` | `common-util-rules` | 暂无 |
| `utils/mq/*/` | `common-util-rules` | 暂无 |
| `utils/search/*/` | `common-util-rules` | 暂无 |
| `utils/storage/*/` | `common-util-rules` | 暂无 |
| `utils/rpc/*/` | `common-util-rules` | 暂无 |
| `utils/api/*/` | `common-util-rules` | 暂无 |
| `utils/auth/*/` | `common-util-rules` | 暂无 |
| `utils/secret/*/` | `common-util-rules` | 暂无 |
| `utils/notification/*/` | `common-util-rules` | 暂无 |
| `utils/payment/*/` | `common-util-rules` | 暂无 |
| `utils/protobuf/` | `common-util-rules` | 暂无 |

### `common/` 公共结构

| 目录 | 关联 skill | recipe 索引 |
| --- | --- | --- |
| `common/request/` | `package-structure-rules` | 暂无 |
| `common/response/` | `package-structure-rules` | 暂无 |
| `common/constant/` | `common-util-rules` | 暂无 |
| `common/error/` | `error-handling-rules` | 暂无 |
| `common/validation/` | `package-structure-rules` | 暂无 |
| `common/util/` | `common-util-rules`、`package-structure-rules` | 暂无 |

### `database/` 数据存储

| 目录 | 关联 skill | recipe 索引 |
| --- | --- | --- |
| `database/connection/` | `database-query-rules` | 暂无 |
| `database/model/db/` | `database-schema-rules` | 暂无 |
| `database/model/redis/` | `database-schema-rules` | 暂无 |
| `database/model/mongo/` | `database-schema-rules` | 暂无 |
| `database/repository/` | `database-query-rules` | 暂无 |
| `database/migration/` | `database-schema-rules` | 暂无 |
| `database/sql/ddl/` | `database-schema-rules` | 暂无 |

## 持续扩展示例

新增 recipe 的流程：

1. 在 `usage-recipes-go.md` 中新增 recipe 小节（使用 `## <category>` 标题）
2. 更新 Catalog 中对应条目的 `usage_recipes` 字段
3. 更新本索引文档的 recipe 索引表
4. 更新 `backend-util-layout.md` 的 Catalog ID 标注（如需要）

新增 recipe 的准入条件：

- 该工具包目录已稳定存在（非推测性）
- 已有至少 1 个真实项目的使用经验
- 关联 skill 的编码规则已明确
