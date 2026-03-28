# 结构变更边界

## 用途

用于区分数据库结构变更、数据变更和查询实现，避免一个迁移包办所有事情。

## 铁律：DDL 定义必须完整

**数据库的字段必须要定义以下内容，不要遗漏，否则会导致自动创建表出现不可控的因素：**

1. **数据类型** - 明确每个字段的数据类型（INT、VARCHAR、TEXT、DATETIME、DECIMAL 等）
2. **默认值** - 明确每个字段的默认值（如果有）
3. **是否需要索引** - 明确哪些字段需要索引、哪些需要唯一索引、哪些不需要索引
4. **CHARSET=utf8mb4** - 明确指定字符集为 utf8mb4
5. **ENGINE=InnoDB** - 明确指定存储引擎为 InnoDB
6. **注释说明** - 为每个字段和表添加清晰的注释说明

## 铁律：金额字段强制使用字符串

**所有金额相关的字段必须强制使用 VARCHAR 或 CHAR 字符串类型，避免任何出现精度问题的情况。**

- ❌ 禁止使用：DECIMAL、DOUBLE、FLOAT、INT 等数值类型
- ✅ 必须使用：VARCHAR、CHAR 等字符串类型
- 示例：`amount` VARCHAR(32) NOT NULL DEFAULT '0.00' COMMENT '订单金额'

## 铁律：创建时间和更新时间规范

**所有表必须包含 created_at 和 updated_at 字段，定义如下：**

```sql
`created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
`updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
```

- `created_at` - 创建时间，默认值为 CURRENT_TIMESTAMP，由数据库自动设置
- `updated_at` - 更新时间，默认值为 CURRENT_TIMESTAMP，并且在更新时自动更新为当前时间，由数据库本身控制

## 铁律：冗余毫秒级时间戳

**为了避免数据库的时区问题影响不同的时间格式，必须冗余一个毫秒级时间戳的创建时间字段。**

字段名建议：`created_at_ts` 或 `created_timestamp`

类型建议：`BIGINT` 或 `VARCHAR(64)`

示例：

```sql
`created_at_ts` BIGINT NOT NULL DEFAULT 0 COMMENT '创建时间毫秒级时间戳',
```

或：

```sql
`created_at_ts` VARCHAR(64) NOT NULL DEFAULT '' COMMENT '创建时间毫秒级时间戳',
```

- 此字段在应用层设置，不由数据库自动维护
- 用于避免不同时区、不同数据库时间格式带来的问题

## 铁律：逻辑删除字段

**所有表必须包含逻辑删除字段，1 的状态标识删除，不是 1 代表正常非删除状态，默认 0=非删除。**

字段名建议：`is_deleted` 或 `deleted`

类型建议：`TINYINT` 或 `SMALLINT`

定义：
```sql
`is_deleted` TINYINT NOT NULL DEFAULT 0 COMMENT '是否删除：0-非删除，1-删除',
```

或：
```sql
`deleted` TINYINT NOT NULL DEFAULT 0 COMMENT '是否删除：0-非删除，1-删除',
```

- `is_deleted` / `deleted` - 逻辑删除标识
- 默认值：0（非删除）
- 删除状态：1（已删除）
- 非删除状态：不是 1 的值都代表正常非删除状态
- 所有查询必须添加 `is_deleted = 0` 或 `deleted = 0` 条件

## 属于 schema 域

- 新增、修改、删除表
- 新增、修改、删除字段
- 索引、唯一约束、外键、主键和 DDL 定义
- ORM 实体结构与数据库 schema 的映射边界

## 不属于 schema 域

- SQL 查询实现、分页、事务、锁、批量 CRUD
- 一次性数据修复脚本和业务补偿逻辑
- 通过默认值偷偷改变业务规则
- 环境配置、连接信息和运行时数据库开关

## 检查表定义完整性

### 创建表的完整 DDL 示例

```sql
CREATE TABLE `orders` (
  `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `order_no` VARCHAR(64) NOT NULL COMMENT '订单号',
  `user_id` BIGINT NOT NULL COMMENT '用户ID',
  `status` TINYINT NOT NULL DEFAULT 0 COMMENT '订单状态：0-待支付，1-已支付，2-已取消',
  `amount` VARCHAR(32) NOT NULL DEFAULT '0.00' COMMENT '订单金额',
  `discount_amount` VARCHAR(32) NOT NULL DEFAULT '0.00' COMMENT '优惠金额',
  `pay_amount` VARCHAR(32) NOT NULL DEFAULT '0.00' COMMENT '实付金额',
  `remark` VARCHAR(255) NULL DEFAULT '' COMMENT '备注',
  `is_deleted` TINYINT NOT NULL DEFAULT 0 COMMENT '是否删除：0-非删除，1-删除',
  `created_at_ts` BIGINT NOT NULL DEFAULT 0 COMMENT '创建时间毫秒级时间戳',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_order_no` (`order_no`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_status` (`status`),
  KEY `idx_is_deleted` (`is_deleted`),
  KEY `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='订单表';
```

### 检查清单

- [ ] 每个字段都有明确的数据类型
- [ ] 每个字段都有明确的默认值（如果适用）
- [ ] 明确指定了哪些字段需要索引
- [ ] 明确指定了 CHARSET=utf8mb4
- [ ] 明确指定了 ENGINE=InnoDB
- [ ] 每个字段都有注释说明
- [ ] 表本身有注释说明
- [ ] 主键、唯一索引、普通索引都有明确的命名和定义
- [ ] 所有金额字段使用 VARCHAR 或 CHAR 字符串类型（不使用 DECIMAL、DOUBLE、FLOAT、INT）
- [ ] 包含 created_at 字段：DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
- [ ] 包含 updated_at 字段：DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
- [ ] 包含 created_at_ts（或 created_timestamp）字段作为冗余毫秒级时间戳
- [ ] 包含 is_deleted（或 deleted）字段：TINYINT NOT NULL DEFAULT 0，1 表示删除，0 表示非删除
- [ ] 为 is_deleted（或 deleted）字段添加索引

## 检查清单（通用）

- 当前变更是否真的是结构定义
- 是否混入了数据修复或查询实现
- 是否改变了现有字段语义、空值语义或默认值语义
- 是否需要拆成多步迁移而不是一步到位
