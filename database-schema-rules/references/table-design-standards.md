# 表设计规范（命名 / 类型 / 索引 / 约束 / 关系 / 迁移）

## 用途

用于新表设计、表结构评审时对照统一的表设计标准。与 `schema-boundaries.md`（DDL 完整性与边界）、`schema-examples.md`（正反例）互补：本文件定义**规则本身**，两个相邻文件提供**落地示例与正反例**，引用时不再重复全文。

## 一、命名约定

### 表命名

- 小写 + 下划线：`users`、`order_items`。
- 复数名词表示集合：`orders`、`projects`、`attachments`。
- 关联表：`{表A}_{表B}`（按字母序）：`role_user`、`project_tag`。
- 可按模块加前缀：`{module}_xxx`（如 `biz_orders`、`sys_config`），项目内统一即可。
- **禁止**：中文字段名、大小写混用、`table1` 类无意义命名。

### 列命名

- 小写 + 下划线：`user_name`、`created_at`。
- 主键统一 `id`（自增 BIGINT 或 UUID 字符串），不另起 `table_id` 等别名。
- 外键（逻辑外键）：`{表名单数}_id`：`user_id` → `users.id`。
- 布尔标记：`is_xxx`：`is_active`、`is_deleted`。
- 时间：`xxx_at`：`created_at`、`approved_at`。
- 金额：`xxx_amount`，类型按本地红线强制字符串（见 `schema-boundaries.md` 铁律 2）。

### 索引命名

| 类型 | 格式 | 示例 |
|------|------|------|
| 普通索引 | `idx_{表}_{列}` | `idx_orders_status` |
| 组合索引 | `idx_{表}_{列1}_{列2}` | `idx_orders_user_status` |
| 唯一索引 | `uk_{表}_{列}` | `uk_users_email` |

## 二、必备字段与审计字段选型

### 每张业务表必含（本地铁律，详见 `schema-boundaries.md`）

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | BIGINT / UUID | 主键 |
| `created_at` | DATETIME 默认 CURRENT_TIMESTAMP | 创建时间 |
| `updated_at` | DATETIME 默认 CURRENT_TIMESTAMP ON UPDATE | 更新时间 |
| `created_at_ts` | BIGINT / VARCHAR | 冗余毫秒级时间戳（铁律 4） |
| `is_deleted` | TINYINT 默认 0 | 逻辑删除（铁律 5） |

### 审计字段选型（新表新增）

| 风格 | 适用场景 |
|------|----------|
| `created_at` + `created_by` + `updated_at` + `updated_by` | 新项目首选，语义直观 |
| `create_time` + `creator` + `modify_time` + `modifier` | 中文团队常见风格 |
| `gmt_create` + `gmt_modified` | 阿里系风格 |

**规则**：一个项目内只能选一种，禁止混用。审计字段名从项目现有约定中提取，新项目自由选择。

## 三、数据类型选型

> 金额字段**不适用**下方 DECIMAL 建议，按本地铁律 2 强制 VARCHAR/CHAR 字符串（见 `schema-boundaries.md`），避免精度问题。

| 场景 | 推荐类型 | 反例 |
|------|----------|------|
| 主键、数量 | `BIGINT` | 用 `INT` 存超 21 亿的值 |
| 短文本（≤255） | `VARCHAR(n)`，给具体长度 | `VARCHAR(255)` 不给原因 |
| 长文本 | `TEXT` / `MEDIUMTEXT` | 用 `VARCHAR(10000)` |
| 布尔/开关/状态 | `TINYINT` + COMMENT 注释 | `ENUM` 类型（扩展需 ALTER TABLE） |
| JSON 数据 | `JSON` 类型 | 用 TEXT 存 JSON |
| 金额 | 强制字符串（本地红线） | `FLOAT` / `DOUBLE` / `DECIMAL`（精度丢失） |
| 日期时间 | `DATETIME` | `TIMESTAMP`（2038 问题） |
| 日期（无时间） | `DATE` | 用 DATETIME 存纯日期 |
| 百分比 | `DECIMAL(5,2)` | `FLOAT` |
| 文件大小 | `BIGINT`（字节） | `VARCHAR` |

### CHAR vs VARCHAR

- `CHAR` 仅用于固定长度值（如 MD5: `CHAR(32)`、手机号、身份证号）。
- 其余一律 `VARCHAR`。

## 四、索引设计

### 必须建索引的场景

- WHERE 条件列。
- JOIN 的 ON 列（逻辑外键列）。
- ORDER BY 列。
- GROUP BY 列。
- 唯一业务键（UNIQUE 约束天然是索引）。

### 组合索引原则

1. 等值条件在前，范围条件在后。
2. 区分度高的列在前。
3. 最左前缀匹配。

```sql
-- 查询: WHERE user_id = ? AND status = ? ORDER BY created_at
CREATE INDEX `idx_orders_user_status_created` ON `orders` (`user_id`, `status`, `created_at`);
```

### 索引禁忌

- 不要为每个列单独建索引（浪费空间、拖慢写入）。
- 不要在低基数列（如性别、type≤3）上建单列索引。
- 不要对大字段建索引（TEXT、长 VARCHAR）。
- 组合索引建议不超过 5 列。

### 覆盖索引

查询只需索引中的列时，避免回表：

```sql
CREATE INDEX `idx_orders_user_status_id_amount` ON `orders` (`user_id`, `status`, `id`, `amount`);
```

## 五、约束

### 必须声明

- `NOT NULL`：业务必填字段。
- `DEFAULT`：有默认值的字段（避免 NULL 带来的判断负担）。
- `UNIQUE`：业务唯一键。
- `PRIMARY KEY`：每表必须有主键。

### 外键红线（个人规则，强制）

- **禁止物理外键约束（`FOREIGN KEY`）**，一律使用逻辑外键：在应用/代码层保证引用完整性，通过外键列 + 索引实现关联。
- 逻辑外键列**必须建索引**。
- 理由：物理外键约束影响写入性能、增加迁移耦合，高并发与分库分表场景不可用。

### CHECK 约束

```sql
-- 限制枚举范围
`status` TINYINT NOT NULL CHECK (status IN (0,1,2,3,4))
-- 限制数值范围
`age` INT CHECK (age > 0 AND age <= 150)
```

## 六、表设计（范式与拆分）

- 默认遵循 3NF：消除冗余、依赖传递。
- 有意识地反范式：高频查询 JOIN 过多时，冗余一两个字段。
- **反范式必须有注释说明原因**。

### 纵向拆分

大表 → 热门字段（高频查询）+ 冷门字段（低频），1:1 JOIN 或独立表。

### 横向拆分 / 分区

- 日志类、时序数据：按时间分区。
- 多租户：按 `tenant_id` 分区。
- 超大数据量：分表（按时间或 ID hash）。

## 七、关系映射

| 关系 | 实现 | 示例 |
|------|------|------|
| 1:1 | FK + UNIQUE 或同表 | `user_profile.user_id` UNIQUE → `users.id` |
| 1:N | FK 在多方 | `orders.user_id` → `users.id` |
| N:M | 中间关联表 | `role_user(role_id, user_id)` |
| 树形 | `parent_id` + 物化路径 `path` | `parent_id=0, path="/1/3/7"` |
| 版本化 | `version` + 复合主键 | `PRIMARY KEY (doc_id, version)` |

### 关联表规则

- 关联表必须包含两方逻辑外键列 + 关系属性（如有）。
- 主键：两 FK 的联合主键，或独立 `id`。
- 必须带 `created_at`。

```sql
CREATE TABLE `role_user` (
  `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `role_id` BIGINT NOT NULL COMMENT '角色ID',
  `user_id` BIGINT NOT NULL COMMENT '用户ID',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_role_user` (`role_id`, `user_id`),
  KEY `idx_role_user_user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='角色用户关联表';
```

## 八、软删除

- 本地红线为标记位：`is_deleted TINYINT NOT NULL DEFAULT 0`，1=删除，非 1=正常（见 `schema-boundaries.md` 铁律 5），**所有查询必须带 `is_deleted = 0` 条件**。
- 唯一约束需包含 `is_deleted`：`UNIQUE (email, is_deleted)`，避免删除后无法复用唯一键。
- ORM 自动过滤：多数 ORM 支持逻辑删除自动过滤（如 MyBatis-Plus `@TableLogic`、GORM `gorm.DeletedAt`）；手写 SQL 必须手动加条件。
- 查询视图用 `CREATE VIEW active_users AS SELECT ... WHERE is_deleted = 0`。

## 九、迁移管理

### 文件命名

```
V1.0.0__init_schema.sql
V1.0.1__add_user_phone.sql
V1.0.2__create_report_tables.sql
```

### 铁律

- 所有 DDL 进版本控制。
- 迁移前向兼容：新加字段给 `DEFAULT`，不删旧字段。
- 破坏性变更多步走：`add column` → 代码适配 → `drop column`（分版本）。
- 生产禁删表、删列、改名（除非确认无依赖）。
- 迁移安全与回滚细则见 `migration-safety-and-rollback.md`（双写、灰度、不可逆点声明等）。

## 十、常见设计模式（低优先参考）

### 配置驱动表

```sql
CREATE TABLE `config_type` (
  `id` BIGINT PRIMARY KEY,
  `type_code` VARCHAR(32) NOT NULL COMMENT '类型编码',
  `name` VARCHAR(100) COMMENT '名称',
  `enabled` TINYINT DEFAULT 1 COMMENT '是否启用',
  UNIQUE KEY `uk_type_code` (`type_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='配置类型表';
```

### 多对多 + 额外属性

```sql
CREATE TABLE `entity_relation` (
  `id` BIGINT PRIMARY KEY,
  `entity_a_id` BIGINT NOT NULL COMMENT '实体A',
  `entity_b_id` BIGINT NOT NULL COMMENT '实体B',
  `sort_order` INT DEFAULT 1 COMMENT '排序',
  `is_active` TINYINT DEFAULT 1 COMMENT '状态',
  UNIQUE KEY `uk_entity_relation` (`entity_a_id`, `entity_b_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='实体关联表';
```

### 审计日志表

```sql
CREATE TABLE `audit_log` (
  `id` BIGINT PRIMARY KEY,
  `table_name` VARCHAR(64) NOT NULL COMMENT '表名',
  `record_id` BIGINT NOT NULL COMMENT '记录ID',
  `action` VARCHAR(16) NOT NULL COMMENT '动作：INSERT/UPDATE/DELETE',
  `changed_by` BIGINT COMMENT '操作人',
  `changed_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '操作时间',
  `old_value` JSON COMMENT '旧值',
  `new_value` JSON COMMENT '新值',
  KEY `idx_audit_log_table_record` (`table_name`, `record_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='审计日志表';
```

## 严禁清单（评审快速否决项）

- 没有主键。
- `SELECT *`（生产查询）。
- `ENUM` 类型。
- `VARCHAR` 不给长度。
- 逻辑外键列无索引。
- **物理外键约束（`FOREIGN KEY`）**。
- 金额用 `FLOAT` / `DOUBLE` / `DECIMAL`（本地红线要求字符串）。
- 低基数列建单独索引。
- 生产中直接删表/删列/改名。
- NULL 满天飞导致 `WHERE` 条件遗漏 `IS NULL`。
- 一张表超过 50 列不拆分。
- 组合索引超过 5 列。
