# 结构变更正反例

## 正例

### 正例 1：完整的 DDL 定义（包含所有必需内容）

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
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `created_at_ts` BIGINT NOT NULL DEFAULT 0 COMMENT '创建时间毫秒级时间戳',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_order_no` (`order_no`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_status` (`status`),
  KEY `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='订单表';
```

✅ 优点：
- 每个字段都有明确的数据类型
- 每个字段都有默认值（如果适用）
- **金额字段使用 VARCHAR 字符串类型**，避免精度问题
- **包含 created_at 和 updated_at 字段**，由数据库自动管理
- **包含 created_at_ts 冗余毫秒级时间戳**，避免时区问题
- 明确指定了索引（主键、唯一索引、普通索引）
- 明确指定了 ENGINE=InnoDB
- 明确指定了 CHARSET=utf8mb4
- 每个字段都有注释说明
- 表本身有注释说明

### 正例 2：金额字段使用字符串类型

```sql
-- ✅ 正确：金额字段使用 VARCHAR
`amount` VARCHAR(32) NOT NULL DEFAULT '0.00' COMMENT '订单金额',
`discount_amount` VARCHAR(32) NOT NULL DEFAULT '0.00' COMMENT '优惠金额',
`pay_amount` VARCHAR(32) NOT NULL DEFAULT '0.00' COMMENT '实付金额',
```

### 正例 3：创建时间和更新时间规范

```sql
-- ✅ 正确：创建时间和更新时间由数据库自动管理
`created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
`updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
```

### 正例 4：冗余毫秒级时间戳

```sql
-- ✅ 正确：冗余毫秒级时间戳，避免时区问题
`created_at_ts` BIGINT NOT NULL DEFAULT 0 COMMENT '创建时间毫秒级时间戳',
```

或使用 VARCHAR：

```sql
-- ✅ 正确：也可以使用 VARCHAR 类型
`created_at_ts` VARCHAR(64) NOT NULL DEFAULT '' COMMENT '创建时间毫秒级时间戳',
```

### 正例 5：新增可空字段，先上线兼容代码，再逐步回填，再改为非空

```sql
-- 第一步：新增可空字段
ALTER TABLE `orders` ADD COLUMN `pay_time` DATETIME NULL DEFAULT NULL COMMENT '支付时间' AFTER `status`;

-- 第二步：逐步回填历史数据
-- ... (数据回填脚本)

-- 第三步：改为非空
ALTER TABLE `orders` MODIFY COLUMN `pay_time` DATETIME NOT NULL COMMENT '支付时间';
```

### 正例 6：新增索引前先确认查询场景和写入影响，不把所有字段都机械加索引

```sql
-- 只给经常查询的字段加索引
CREATE INDEX `idx_user_id` ON `orders` (`user_id`);
CREATE INDEX `idx_status_created_at` ON `orders` (`status`, `created_at`);

-- 不给不常查询的字段加索引
-- 避免：CREATE INDEX `idx_remark` ON `orders` (`remark`);
```

### 正例 7：删除旧字段前先确认没有旧代码、旧接口和旧任务仍在依赖

```sql
-- 第一步：确认旧字段已无依赖
-- ... (检查代码、接口、任务)

-- 第二步：先标记为废弃（可选）
-- ALTER TABLE `orders` MODIFY COLUMN `old_field` VARCHAR(255) NULL DEFAULT NULL COMMENT '已废弃，请勿使用';

-- 第三步：确认安全后删除
ALTER TABLE `orders` DROP COLUMN `old_field`;
```

### 正例 8：把结构变更迁移和数据修复迁移分成独立步骤

```sql
-- 迁移1：结构变更
ALTER TABLE `orders` ADD COLUMN `discount_amount` VARCHAR(32) NOT NULL DEFAULT '0.00' COMMENT '优惠金额' AFTER `amount`;

-- 迁移2：数据修复
UPDATE `orders` SET `discount_amount` = '0.00' WHERE `discount_amount` = '';
```

## 反例

### 反例 1：金额字段使用数值类型（会导致精度问题）

```sql
-- ❌ 错误：金额字段使用 DECIMAL
`amount` DECIMAL(10, 2) NOT NULL DEFAULT 0.00 COMMENT '订单金额',
```

```sql
-- ❌ 错误：金额字段使用 DOUBLE
`amount` DOUBLE NOT NULL DEFAULT 0.00 COMMENT '订单金额',
```

```sql
-- ❌ 错误：金额字段使用 FLOAT
`amount` FLOAT NOT NULL DEFAULT 0.00 COMMENT '订单金额',
```

```sql
-- ❌ 错误：金额字段使用 INT
`amount` INT NOT NULL DEFAULT 0 COMMENT '订单金额',
```

❌ 问题：金额字段使用数值类型可能导致精度问题，必须使用 VARCHAR 或 CHAR 字符串类型。

### 反例 2：缺少 created_at 和 updated_at 字段

```sql
CREATE TABLE `orders` (
  `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `order_no` VARCHAR(64) NOT NULL COMMENT '订单号',
  ...
  -- ❌ 错误：缺少 created_at 字段
  -- ❌ 错误：缺少 updated_at 字段
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='订单表';
```

### 反例 3：created_at 和 updated_at 定义不正确

```sql
-- ❌ 错误：created_at 没有 DEFAULT CURRENT_TIMESTAMP
`created_at` DATETIME NOT NULL COMMENT '创建时间',

-- ❌ 错误：updated_at 没有 ON UPDATE CURRENT_TIMESTAMP
`updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
```

### 反例 4：缺少冗余毫秒级时间戳

```sql
CREATE TABLE `orders` (
  ...
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  -- ❌ 错误：缺少 created_at_ts 冗余毫秒级时间戳字段
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='订单表';
```

❌ 问题：缺少冗余毫秒级时间戳，可能导致数据库时区问题影响不同的时间格式。

### 反例 5：DDL 定义缺少必要内容

```sql
CREATE TABLE `orders` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `order_no` VARCHAR(64) NOT NULL,
  `user_id` BIGINT NOT NULL,
  `status` TINYINT NOT NULL DEFAULT 0,
  `amount` DECIMAL(10, 2) NOT NULL,
  `remark` VARCHAR(255),
  `created_at` DATETIME,
  `updated_at` DATETIME,
  PRIMARY KEY (`id`)
);
```

❌ 问题：
- 金额字段使用 DECIMAL 数值类型（会导致精度问题）
- 缺少冗余毫秒级时间戳 created_at_ts
- 缺少字段注释
- 缺少表注释
- 缺少索引定义（除了主键）
- 缺少 ENGINE=InnoDB
- 缺少 CHARSET=utf8mb4
- 部分字段缺少默认值
- created_at 和 updated_at 定义不正确
- 会导致自动创建表出现不可控的因素

### 反例 6：缺少 CHARSET=utf8mb4

```sql
CREATE TABLE `orders` (
  ...
) ENGINE=InnoDB COMMENT='订单表';
```

❌ 问题：缺少 CHARSET=utf8mb4，可能导致字符集不统一，出现乱码或存储问题。

### 反例 7：缺少 ENGINE=InnoDB

```sql
CREATE TABLE `orders` (
  ...
) DEFAULT CHARSET=utf8mb4 COMMENT='订单表';
```

❌ 问题：缺少 ENGINE=InnoDB，可能使用默认的存储引擎，导致事务、外键等功能不可用。

### 反例 8：在同一条迁移里同时删列、回填、改语义、改查询逻辑

```sql
-- 不推荐：一条迁移做太多事情
ALTER TABLE `orders`
  DROP COLUMN `old_field`,
  ADD COLUMN `new_field` VARCHAR(255) NOT NULL DEFAULT '',
  MODIFY COLUMN `status` TINYINT NOT NULL DEFAULT 1;

UPDATE `orders` SET `new_field` = `old_field` WHERE `old_field` IS NOT NULL;
```

❌ 问题：职责混杂，风险高，回滚困难。

### 反例 9：直接把高频表字段从宽类型改成窄类型，却没有兼容或回滚说明

```sql
-- 不推荐：直接改窄类型
ALTER TABLE `orders` MODIFY COLUMN `order_no` VARCHAR(32) NOT NULL COMMENT '订单号';
```

❌ 问题：没有兼容方案，可能导致数据截断，回滚方案不清。

### 反例 10：给关键字段加危险默认值，只为了绕过现有脏数据

```sql
-- 不推荐：危险的默认值
ALTER TABLE `orders` MODIFY COLUMN `status` TINYINT NOT NULL DEFAULT 1 COMMENT '订单状态';
```

❌ 问题：通过默认值偷偷改变业务规则，可能导致数据错误。

### 反例 11：查询慢就直接改 schema，但没有确认瓶颈到底在结构还是查询实现

```sql
-- 不推荐：盲目加索引
CREATE INDEX `idx_everything` ON `orders` (`user_id`, `status`, `amount`, `created_at`);
```

❌ 问题：没有分析查询瓶颈，盲目加索引可能导致写入性能下降。
