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
6. **注释说明** - 为每个字段和表添加清晰的注释说明。载体是 ORM 的 `comment:` tag 与 DDL 的 `COMMENT`（会真正落进数据库列注释，DBA、SQL 客户端和其他语言的调用方都能看到）；模型字段行尾的 `//` 注释不算满足本项，也不要拿它重抄 `comment:` 的内容——重复副本的治理规则见 `comment-rules` 的位置分区

## 铁律：SQL 标识符统一反引号

**SQL 中的表名、字段名、索引名统一使用反引号包裹，避免关键字冲突和风格漂移。**

- ✅ 推荐：`` `enabled` TINYINT(1) NOT NULL DEFAULT 1 COMMENT '是否启用' ``
- ❌ 不推荐：`enabled TINYINT(1) NOT NULL DEFAULT 1 COMMENT '是否启用'`

说明：

- 反引号规范不仅用于字段名，也用于表名、主键名、普通索引名、唯一索引名。
- 即使当前名称不与关键字冲突，也保持统一反引号风格，减少后续迁移风险。

## 铁律：表名单一定义源

**表名字面量在整个仓库只允许出现在两处：该表的模型文件、DDL / 迁移脚本。其余任何位置要用表名，一律引用模型暴露的表名方法。**

判定标准：

- 每个表模型都必须显式实现返回表名的方法（Go GORM 的 `TableName()`、其他 ORM 的等价 `table` 元数据），不允许依赖 ORM 的结构体名推导或自动复数化。
- 仓储层 / DAO / QueryBuilder 的表名成员、`.Table(...)` 调用、迁移登记清单、初始化脚本、测试构造数据，都必须引用模型的表名方法。
- 同一个表名字符串在模型之外出现第二次，即判定为违规，无论它拼写是否正确。

正例（Go + GORM）：

```go
// model 层：表名的唯一定义源
func (ExchangeFreeGasControl) TableName() string {
    return "exchange_free_gas_control"
}

// repository 层：引用模型表名，不重写字面量
func NewExchangeFreeGasControlRepo() *ExchangeFreeGasControlRepo {
    return &ExchangeFreeGasControlRepo{
        db:        connection.GetDB(),
        tableName: model.ExchangeFreeGasControl{}.TableName(),
    }
}
```

反例（禁止）：

```go
// repository 层重复硬编码表名，与 model 形成两个真相源
func NewCoinsBrowserUrlDictRepo() *CoinsBrowserUrlDictRepo {
    return &CoinsBrowserUrlDictRepo{
        db:        connection.GetDB(),
        tableName: "coins_browser_url_dict", // ❌ 表名字面量重复出现
    }
}
```

为什么：表名字面量重复即两个真相源。改表名（重命名、加前缀、分库分表换表名）时编译器不会报错，漏改的调用点在运行时才炸；且拼写错误只能靠跑到那条链路才发现。收敛到模型方法后，改表名只改一处，所有引用点自动跟随。

例外（必须显式说明理由）：

- DDL / 迁移脚本里的 `CREATE TABLE`、`ALTER TABLE` 本身就是表名定义源，不受本条约束。
- 跨库查询、`information_schema` 元数据查询、动态分表按规则拼接表名时，允许以模型表名方法为基串再拼后缀，但基串仍不得写字面量。
- 表模型尚未建立的一次性排查脚本可以直接写表名，但不得进入生产代码路径。

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

上面是**数据库层自动维护**的写法，适用于非 ORM 项目。ORM 项目也可以改由 ORM 自动维护（如 GORM 的
`autoCreateTime` / `autoUpdateTime`），此时 DB 层的 `ON UPDATE` 可以不写——铁律 3 要求的是"必须自动
维护、不许业务代码逐处手写"，不是"必须由数据库维护"。两种方式在同一项目内要统一，别一半一半。
GORM 的 tag 写法与 `ON UPDATE` 的位置陷阱见 `schema-examples.md` 的 GORM tag 小节。

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

## 铁律：禁止物理外键，一律逻辑外键

**禁止 `FOREIGN KEY` 约束；表间关系用逻辑外键表达，且外键列必须建索引。**

判定要点：

- DDL 里出现 `FOREIGN KEY` / `REFERENCES` / `ON DELETE CASCADE` 即违规，无论是建表时写的还是后续 `ALTER` 加的。
- 逻辑外键列（`user_id`、`order_id` 这类）**必须有索引**——没有索引的逻辑外键会让关联查询全表扫描，
  是比缺约束更现实的问题。
- ORM 侧不要声明会自动建物理外键的关联（GORM 需显式关闭 `DisableForeignKeyConstraintWhenMigrating`
  或不声明 `constraint` 标签），否则自动迁移会把物理外键建出来。

```sql
-- ✅ 逻辑外键 + 索引
`user_id` BIGINT NOT NULL COMMENT '用户ID',
KEY `idx_user_id` (`user_id`)

-- ❌ 物理外键
CONSTRAINT `fk_order_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
```

为什么：物理外键把关联校验压在数据库层，分库分表、批量导数、灰度双写、删档回滚时都会被约束挡住；
级联删除还会造成难以预期的连锁删除。关系完整性由应用层保证，数据库只负责存储与索引。

关系建模、级联策略与更详细的设计取舍见 `table-design-standards.md`。

## 铁律的适用范围：新建表强制，存量表不据此改

上面这些铁律（`SKILL.md` 的铁律 1~5）都是**新建表的强制要求**。遇到已经有数据的存量表不符合铁律时，
**不得据此去改存量表**——补列、改类型都是对线上表执行 DDL，属于需要人工评估的结构变更决策，不能由
"对齐规范"或一次服务重启顺手完成。

这类偏离必须在模型注释与迁移说明里写明是"按目标环境如实保留"，而不是遗漏。存量表纳入 ORM 自动迁移时
的逐条边界（含金额列改类型的精度风险、老表字符集为何如实保留）见 `orm-auto-migration.md` 的
「存量表与本 skill 铁律的适用边界」。

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
- [ ] 表名、字段名、索引名统一使用反引号包裹（例如 `enabled`）
- [ ] 表模型显式实现了表名方法，且表名字面量只出现在模型文件与 DDL / 迁移脚本
- [ ] 每个字段都有注释说明
- [ ] 表本身有注释说明
- [ ] 主键、唯一索引、普通索引都有明确的命名和定义
- [ ] 所有金额字段使用 VARCHAR 或 CHAR 字符串类型（不使用 DECIMAL、DOUBLE、FLOAT、INT）
- [ ] 包含 created_at 字段：DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
- [ ] 包含 updated_at 字段：DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
- [ ] 包含 created_at_ts（或 created_timestamp）字段作为冗余毫秒级时间戳
- [ ] 包含 is_deleted（或 deleted）字段：TINYINT NOT NULL DEFAULT 0，1 表示删除，0 表示非删除
- [ ] 为 is_deleted（或 deleted）字段添加索引
- [ ] 没有物理外键约束（`FOREIGN KEY` / `REFERENCES`），且每个逻辑外键列都建了索引

### 变更性质检查（所有结构变更都要过）

- [ ] 当前变更真的是结构定义，没有混入数据修复或查询实现
- [ ] 没有改变现有字段语义、空值语义或默认值语义
- [ ] 判断过是否需要拆成多步迁移而不是一步到位
- [ ] 若目标表已有数据，确认本次变更不会由启动流程自动施加（见「铁律的适用范围」）
