# ORM 自动迁移：存量表纳入的操作步骤、陷阱与等价性验证

## 用途

用于「把已经有数据的存量表纳入 ORM 启动期自动迁移」这一类改动。新表从零建出不难，难的是存量表——
线上结构与模型定义必然存在历史漂移，一旦让启动流程去"纠正"它，就是在共享库和生产库上执行未经评估的
结构变更。本文件给出边界、操作顺序、已实测的陷阱清单和验证矩阵。

只在涉及 ORM 自动迁移（AutoMigrate / Migrator / 等价机制）时读本文件。纯人工 DDL 上线读
`migration-safety-and-rollback.md`；新表设计读 `table-design-standards.md`。

## 铁律：自动迁移严格只做加法

**边界是「新表全自动，存量列只读」：**

| 对象 | 允许的动作 | 禁止的动作 |
|---|---|---|
| 表不存在 | 整表建出（列 + 索引 + 建表选项一次落地） | — |
| 表已存在、列缺失 | 补列（`AddColumn`） | — |
| 表已存在、列也存在 | **只读，什么都不做** | 改类型、改长度、改默认值、改可空、改注释、改字符集 |
| 索引缺失 | 幂等补建（先查后建） | 删索引、改索引定义 |
| 主键 | 不动 | 改主键 |

这条边界的完整表述见 `SKILL.md` 铁律 0.2。

## 铁律：不要用"全量对齐"型 API 管存量表

**禁止用 GORM `AutoMigrate` 这类"让库结构与模型完全一致"的 API 去处理存量表**，要用细粒度
Migrator 自己实现上面那张表的语义：

```go
migrator := db.Set("gorm:table_options", opts).Migrator()

// 表不存在：一次建全
if !migrator.HasTable(model) {
    return migrator.CreateTable(model)
}

// 表已存在：只补库里没有的列，已存在的列一律不碰
stmt := &gorm.Statement{DB: db, Table: tableName}
if err := stmt.ParseWithSpecialTableName(model, tableName); err != nil {
    return err
}
for _, field := range stmt.Schema.Fields {
    if field.DBName == "" || field.IgnoreMigration {
        continue
    }
    if migrator.HasColumn(model, field.DBName) {
        continue   // 关键：只判断「有没有」，不判断「一样不一样」
    }
    if err := migrator.AddColumn(model, field.DBName); err != nil {
        return err
    }
}
```

**为什么**：`AutoMigrate` 会为了让列定义与模型完全一致而生成 `MODIFY COLUMN`，触发条件包括长度、
精度、可空、默认值、**注释**等任一处不一致。真实事故：某环境 orderUser 只是两列缺 `COMMENT`，就让
每次启动都对这张 5.6 万行、38MB 的表执行两条 `MODIFY COLUMN` 只为补注释，耗时与等锁双双超过 DSN 的
`readTimeout=10s`，报 `invalid connection`；且因 ALTER 从未成功而每次启动重来一遍。

**加大 `readTimeout` 是错误答案**——那只是让这条 ALTER"成功"，锁表与 rebuild 的代价一分不少，
生产上照样跑。同样不可取的还有「只把当前这个环境的差异补齐」（只治一处，任何环境的任何漂移都会重现）
和「把大表移出迁移清单」（新环境又要人工建表，违背自动迁移的目的）。

## 失败是否阻断启动

分流口径见 `SKILL.md` 铁律 0（建库失败阻断；建表 / 补列 / 补索引失败只记错误不阻断），此处不重复。
两点本文件独有的补充：

- 错误日志要能直接定位到对象：**表名 + 列名/索引名 + 原始错误**，并在汇总行给出计数（新建 X 张、
  补列 Y 个、失败 Z 张）。
- 索引补建失败之所以也不阻断，是因为**索引缺失的症状是慢查询而非功能错误**，比建表失败隐蔽，
  值得靠日志与告警兜住而不是靠拒绝启动。

## 操作步骤

1. **清点现状**：列出待纳入的表、各表在目标环境的行数与数据量（`information_schema.TABLES`）。行数大的
   表要单独标注——它们是所有风险的集中点。
2. **确认模型侧前提**：每张表都要有显式表名方法（见 `schema-boundaries.md` 的表名单一定义源）。给已有
   访问代码的模型新增 `TableName()` 是安全的：访问路径若已显式 `Table(...)`，ORM 中 `Table()` 的优先级
   高于 `TableName()`，行为不变。
3. **建立结构真相源**：拿目标环境的真实 DDL 在本机容器里建一个基线库，导出结构快照。**真相源是数据库
   里的实际落地形态，不是 DDL 文本字面**——见下节"落地形态差异"。
4. **探针实测 tag→DDL 映射**：写一个一次性探针，把本次会用到的各类字段（整型、无符号、带标度浮点、
   列级字符集、复合主键、索引注释、时间默认值）各建一列，跑完 `SHOW CREATE TABLE` 看真实输出，再据此
   写模型 tag。**不要凭文档猜**，见下节陷阱清单。
5. **逐表写 tag 并登记清单**：建表选项（ENGINE / CHARSET / ROW_FORMAT / COMMENT）按表单独给，逐字对齐
   目标环境。字段顺序也按目标环境排，便于后续结构比对。
6. **迭代到零变更**：在基线库上反复跑迁移，直到"零 DDL、结构一字不变"。每一条残留的 DDL 都要查清成因，
   不允许"看起来没坏就放过"。
7. **跑完整验证矩阵**：见下节。改动任何模型 tag 后都要重跑。

## 落地形态差异：真相源不是 DDL 文本

同一份 DDL 文本在不同 MySQL 版本里落地形态不同，按字面写 tag 会与实际不符而触发 ALTER：

| DDL 文本 | MySQL 8 实际存储 | 说明 |
|---|---|---|
| `int(11)` / `int(4)` / `tinyint(3)` / `bigint(20)` | `int` / `int` / `tinyint` / `bigint` | 8.0.19 起丢弃整型显示宽度 |
| `tinyint(1)` | `tinyint(1)` | 保留，有 boolean 语义 |
| `CHARSET=utf8` | `utf8mb3` | `utf8` 是 `utf8mb3` 的别名 |
| `double(20,8)` / `decimal(6,4)` | 原样 | 浮点与定点的精度标度保留 |

所以第 3 步要取 `SHOW CREATE TABLE` / `information_schema` 的真实输出作为校准依据。

## 陷阱清单（均为实测结论，GORM 1.25 + driver mysql 1.8 + MySQL 8.0）

### 1. `type:int` 会被提升成 `bigint`

tag 写 `type:int` 落地是 `bigint`（命中 ORM 抽象 DataType 后按 Go `int` 宽度映射）。写带显示宽度的
`type:int(11)` 才透传成 `int`。带修饰的 `type:int unsigned` 也能正常透传。
**统一用带宽度写法**（`int(11)`、`tinyint(3)`、`bigint(20)`），MySQL 8 会归一化，结果与目标环境一致。

其他类型均可原样落地：`bigint unsigned`、`tinyint(1)`、`double(20,8)`、`float(10,4)`、`float unsigned`、
`decimal(3,2) unsigned`、`longtext`、`json`。

### 2. 列级字符集要写进 `type`

表是 `utf8mb3` 而个别列是 `latin1` 或 `utf8mb4` 时，必须显式声明，否则会被判为需要 ALTER：

```go
Network string `gorm:"column:network;type:varchar(32) CHARACTER SET latin1 COLLATE latin1_swedish_ci;not null"`
```

反过来，**跟随表默认字符集的列不要写** `charset` / `collate` —— 写了同样会造成不一致（尤其是写了
`utf8mb4_general_ci` 而表实际是 `utf8mb4_0900_ai_ci`）。

### 3. 复合主键的第二列若会变更，ORM 上不能标 `primaryKey`

ORM 的 `Save` 会用**全部主键**拼 `UPDATE` 的 `WHERE`，且不更新主键列本身。若线上主键是 `(id,status)`
而 `status` 是会流转的业务状态，把 `status` 也标成 `primaryKey` 会让状态更新生成
`WHERE id = ? AND status = <新状态>`，匹配不到旧状态行——**更新 0 行、不报错、状态静默丢失**。

处理：模型只声明 `id`。自动迁移不修改已存在表的主键，所以少声明这一列对线上无影响；只有全新环境建出
的主键会退化为 `(id)`，需完全一致时以人工 DDL 为准。这类刻意偏离必须在模型注释里写明原因。

### 4. `ON UPDATE CURRENT_TIMESTAMP` 的写法

必须并入 `type`，不能写进 `default`。成因与正反例见 `schema-examples.md` 的 GORM tag 小节，本文件不
重复。

### 5. 唯一索引创建顺序随机，会报 `Duplicate key name`

一个列同时挂"单列唯一索引"和"复合唯一索引首列"时（例如 `order_id` 既有 `uk_order_id` 又是
`uk_order_ext(order_id, ext_id)` 的首列），建表时索引创建顺序来自 map 遍历，**是随机的**：

| 先建的索引 | 该列 `COLUMN_KEY` | 后续 `HasIndex` 判断 |
|---|---|---|
| 单列唯一索引 | `UNI` | 正确，no-op |
| 复合唯一索引 | `MUL` | **误判为不存在**，重复创建 → MySQL 1061 |

调整 tag 顺序**不能**消除随机性。处理：在 `CreateIndex` 的错误分支里按错误码 1061 幂等跳过（此时索引
确实已存在、结构正确）。目标环境的表若由人工 DDL 建出且单列索引在前，`COLUMN_KEY` 是 `UNI`，线上不受
影响，只有全新环境自建的表会遇到。

### 6. 索引要有独立的显式补建步骤

「不依赖建表 API 补齐存量表索引」这一条的权威在 `SKILL.md`（进入后先做的索引幂等检查项）。落地方式是
单独走一遍 `ParseIndexes → HasIndex → CreateIndex`，并把「模型上声明了几个索引 / 补建了几个 / 失败几个」
打进启动日志——把此前完全隐式的"模型到底声明了多少索引"变成可观测信息。

## 等价性验证矩阵

改动任何模型 tag 后必须重跑。五段缺一不可：

| 段 | 做什么 | 判据 |
|---|---|---|
| 1 正向 no-op | 用目标环境真实 DDL 建基线库，跑迁移 | 零 DDL 且结构一字不变 |
| 2 反向等价建表 | 空库跑迁移，与基线做语义级集合比对 | 列 / 索引 / 表选项集合一致（刻意偏离项显式列出并说明） |
| 3 二次启动幂等 | 自建库上再跑一次 | 无 error 且结构不变 |
| 4 随机性稳定 | 多轮重建空库各跑两次 | 全程无 error，且覆盖到索引建序的各个随机分支 |
| 5 **存量漂移环境** | 用**真实环境**的结构 dump 建副本再跑 | **对存量列零变更** |

### 段 5 是最容易漏、也最重要的一段

只验证"按标准 DDL 建出的结构"会给出一切正常的假象：那上面确实零 DDL。但真实环境的存量结构本就有历史
漂移，**漂移环境才是会出问题的那个**。真实教训：只验了标准结构就判定安全，上线后每次启动都在大表上
ALTER 并超时。凡是能拿到结构 dump 的环境都要跑一遍段 5。

**环境边界（红线，不得绕开）**：Agent 只允许直连 local 配置声明的库去导出 dump。`test` / `pre` /
`staging` / `prod` 等非 local 环境的结构 dump **必须由人工或运维离线导出后作为文件提供**，Agent 只消费
dump 文件本身，不得直连这些环境——本地环境红线的权威在 `test-strategy-rules`，本文件不另开口子。拿不到
非 local 的 dump 时，就用 local 的 dump 跑段 5 并在结论里写明"未覆盖的环境"，不要用"连不上"当作跳过
段 5 的理由。

导出结构（只读、不含数据；**仅对 local 执行**，非 local 由人工离线导出）：

```bash
mysqldump --no-data --skip-add-drop-table --skip-comments \
  --default-character-set=utf8mb4 -h <host> -P <port> -u <user> -p<pw> <db> > /tmp/env_schema.sql
```

### 比对方法：按 information_schema 集合比，不比建表语句文本

查三组、各自排序后 diff：

- **列**：表名 / 列名 / `COLUMN_TYPE` / 可空 / 默认值 / 字符集 / 排序规则 / `EXTRA` / 注释
- **索引**：表名 / 索引名 / 唯一性 / `SEQ_IN_INDEX` / 列名
- **表选项**：引擎 / `TABLE_COLLATION` / 注释 / `ROW_FORMAT`

**为什么不用 `SHOW CREATE TABLE` 文本比**：人工 DDL 里的 `USING BTREE`（ORM 不写）、以及索引与列的
排列顺序都不影响行为，却会产生几十行 diff 噪声把真实差异淹没。集合比对天然顺序无关。

## 会产出"假结论"的四个坑

验证脚本本身出错比没验证更危险——它会给出一个可信的 PASS。以下四个都实际踩过：

1. **客户端默认 `latin1` 写坏中文注释**：容器内 mysql 客户端默认字符集是 `latin1`，导入含中文注释的
   DDL 会双重编码写坏注释，随后 ORM 拿正确中文比对 mojibake，判定每一列都要改——曾据此产出「252 条
   ALTER」的假警报。导入与读取一律显式 `--default-character-set=utf8mb4`。要判断存储是否真坏了，查
   `HEX(COLUMN_COMMENT)` 并用两种读法交叉验证。
2. **空快照两两相等**：环境没起来（容器端口占用、库没导入）时脚本继续跑，各段拿到的都是空结果，diff
   相等于是报「完全一致」。每一段都要先校验前置条件（容器起没起、副本导了几张表、查询结果非空），
   环境异常直接判失败退出。
3. **容器就绪判据用 `mysqladmin ping`**：MySQL 官方镜像会先用临时 server 做初始化再 shutdown 重启正式
   server，`ping` 在初始化阶段就会成功而 root 密码尚未生效，之后连接就断（`driver: bad connection`）。
   判据要用「能用目标账号真正执行一条 SQL」，且要求连续多次成功。
4. **幂等判据数「有没有 DDL 语句」**：有些语句发出来就注定失败并被幂等逻辑吞掉（如上面的 1061）。
   判据应是「无 error + 结构不变」，而不是「日志里没有 DDL」。

## 存量表与本 skill 铁律的适用边界

铁律 1~5 是**新建表的强制要求**。存量表纳入自动迁移时按以下边界执行，不得据此去改存量表：

| 铁律 | 存量表处理 | 原因 |
|---|---|---|
| 铁律 3 / 4 / 5（时间字段 / 毫秒戳 / 逻辑删除） | 缺就缺着，**不补** | 补列就是对线上大表执行 DDL；是否要补属结构变更决策，走人工 DDL |
| 铁律 2（金额用字符串） | 存量的 `decimal` / `double` 保留 | 改类型要 rebuild 全表，且可能损失精度，必须业务确认 |
| 铁律 1（含 `CHARSET=utf8mb4`） | 老表的建表选项如实保留 `utf8mb3` | 建表选项只在首次建表生效，对存量表零影响；写 `utf8mb4` 反而让新环境与目标环境列字符集不一致，破坏等价性 |

偏离必须写明原因（口径见 `schema-boundaries.md` 的「铁律的适用范围」）。新表一律按铁律执行，不受本节影响。

## 检查清单

- [ ] 迁移实现是「建表 + 补缺列 + 补索引」，没有任何路径会改动已存在的列
- [ ] 建库失败阻断启动；建表 / 补列 / 补索引失败只记错误并计入汇总
- [ ] 模型 tag 按目标环境的**实际落地形态**校准（不是 DDL 文本字面）
- [ ] 整型 tag 用带显示宽度写法，列级字符集只在与表默认不同时显式声明
- [ ] 会流转的状态列没有被标成 `primaryKey`
- [ ] 索引有独立的幂等补建步骤，且对 1061 做了容错
- [ ] 五段验证全部通过，其中**段 5 用了真实环境的结构 dump**
- [ ] 比对走 `information_schema` 集合，不是建表语句文本
- [ ] 验证脚本对「环境未就绪 / 副本为空」直接判失败，不会输出假 PASS
- [ ] 与铁律的偏离项都在注释与文档里写明原因
