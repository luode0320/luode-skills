# 吸收裁决表（workbuddy-absorption-map）

> 归属：`database-schema-rules`。记录外部 skill 精华的吸收裁决，来源可回指，每行含「整理去重」列。

## 执行中 gap 回补：存量表纳入 ORM 自动迁移（2026-08-21）

**来源**：内部实践（无外部 skill）。EllipalFinance-go 两轮真实执行——先把 15 张业务表以正式环境 DDL 为准
纳入自动迁移，随后 local 启动爆出 `orderUser` 每次迁移失败（`i/o timeout` + `invalid connection`）。
gap 判定：本 skill 有"自动初始化必须覆盖库/表/索引"的要求，但**完全没有**"存量表怎么纳入""ORM tag 有哪些
陷阱""怎么验证迁移不会动线上结构"的可执行内容，执行全程只能靠临时推导，且既有铁律 0 与实践冲突。

**通道**：执行中 gap 回补。**裁决结果**：合并 13 条 / 保留本地 2 条 / 拒绝 0 条 / 修正既有条款 1 条。

| 条目 | 本地现状 | 裁决 | 落点 | 整理去重 |
|------|---------|------|------|---------|
| 自动迁移边界＝新表全自动、存量列只读（建表+补缺列+补索引，已存在列一律不碰） | SKILL.md 只有"只做加法"一句，未定义边界，且实现层用 AutoMigrate 实际会 MODIFY | 合并 | SKILL.md 铁律 0.2 + `orm-auto-migration.md` 边界表 | 与铁律 0 合并表述，避免两处各说一半 |
| 禁止用 `AutoMigrate` 这类全量对齐 API 管存量表（为对齐注释就 MODIFY 大表 → 锁表/超时/每次启动重复） | 无 | 合并 | 同上 + 附可直接套用的 Migrator 代码骨架 | — |
| 迁移超时不得靠加大连接 `readTimeout` 掩盖；另否决"只补当前环境差异""大表移出清单" | 无 | 合并 | `orm-auto-migration.md` 未采用方案 | — |
| **既有铁律 0 修正**：初始化失败一律阻断启动 → 改为按场景分流（建库阻断；建表/补列/补索引不阻断） | 原文"任一环节失败都必须返回错误并阻断启动"，与实践冲突（单表问题会拖垮不相关业务） | 修正 | SKILL.md 铁律 0，并同步「进入后先做」第 4 条、「执行流程」第 6 条、通过/驳回标准 | **消除 4 处口径不一致**：原先阻断口径散落在 4 个小节，现统一指向铁律 0 |
| 真相源是数据库实际落地形态而非 DDL 文本（MySQL 8.0.19+ 丢整型显示宽度、`utf8`→`utf8mb3`） | 无 | 合并 | `orm-auto-migration.md` 落地形态差异表 | — |
| `type:int` 被提升为 `bigint`，须写 `int(11)`；列级字符集写进 `type`，跟随表默认的列不写 | 无 | 合并 | 同文件陷阱 1、2 | — |
| 会流转的状态列不能标 `primaryKey`（`Save` 用全主键拼 WHERE → 更新 0 行且不报错、状态静默丢失） | 无 | 合并 | 同文件陷阱 3 | — |
| 唯一索引建序随机 → `COLUMN_KEY` UNI/MUL → 1061，须幂等容错；调 tag 顺序无效 | SKILL.md 有"建索引须幂等"，但无此成因、也没说清为何 `HasIndex` 会误判 | 合并（补成因） | 同文件陷阱 5 | 不重复"须幂等"结论，只补成因与处理 |
| 索引要有独立显式补建步骤，并把声明/补建/失败数打进启动日志 | SKILL.md 已有同义要求 | **保留本地** | — | 不重复落盘 |
| `ON UPDATE CURRENT_TIMESTAMP` 并入 `type` 不写 `default` | **已有**（2026-08-21 上一轮已吸收，见本表下一节 + `schema-examples.md`） | **保留本地** | 新文件陷阱 4 只写一行指向 `schema-examples.md` | **避免了一处交叉重复**——查证后才发现已存在，未重抄 |
| 等价性验证按 `information_schema` 集合比（列/索引/表选项三组），不比建表语句文本 | 无 | 合并 | `orm-auto-migration.md` 比对方法 | — |
| 验证矩阵五段，其中**段 5 存量漂移环境**（用真实环境结构 dump 建副本，断言对存量列零变更） | 无 | 合并 | 同文件验证矩阵 | 本轮最高价值项：缺这段直接导致 bug 上线 |
| 四类假 PASS 陷阱（latin1 写坏中文注释、空快照两两相等、`mysqladmin ping` 命中临时 server、幂等判据数 DDL 语句） | 无 | 合并 | 同文件"会产出假结论的四个坑" | — |
| 存量表与铁律的适用边界（时间字段/毫秒戳/逻辑删除不补、金额列不改类型、老表如实保留 `utf8mb3`） | 铁律存在，但无存量表例外说明，导致执行时反复纠结要不要补列 | 合并 | `schema-boundaries.md` 新增「铁律的适用范围」+ `orm-auto-migration.md` 边界表 | 边界表放 orm 文件、原则句放 boundaries，互相引用不重复 |
| 新增 `TableName()` 对既有查询安全（`Table()` 优先级高于 `TableName()`） | 有表名铁律，缺这条结论 | 合并 | `orm-auto-migration.md` 操作步骤第 2 步 | 并入既有铁律的引用，不新开小节 |

**同域冗余扫描（落盘后执行，由独立子 agent 只读审计）**

范围：`database-schema-rules` 自身全部 references、`database-query-rules`、`test-strategy-rules`、
`test-program-rules`、`code-style-consistency-rules`、`execution-failure-learning-rules`、`golang-patterns`。

① **重复段落：发现 5 处，清理 5 处**

| 冗余位置 | 收敛到的单一权威 | 处理 |
|---|---|---|
| 失败分流表 + 理由，在 `SKILL.md` 铁律 0 与 `orm-auto-migration.md`「失败是否阻断启动」逐字重复 | `SKILL.md` 铁律 0 | orm 文件删表格与理由，只留两点独有增量（日志字段粒度、索引缺失症状是慢查询） |
| 「不要依赖建表 API 补齐索引」两处都写了，**与本表裁决"保留本地/不重复落盘"自相矛盾** | `SKILL.md` 索引幂等检查项 | orm 文件陷阱 6 删否定句，只留 `ParseIndexes→HasIndex→CreateIndex` 落地方式与日志可观测性 |
| 「存量列该不该改…不由一次服务重启决定」在 3 个文件近逐字 | `SKILL.md` 铁律 0.2（`migration-safety-and-rollback.md` 那句是刻意的跨场景锚点，保留） | 删 `orm-auto-migration.md` 的复述，改为指向铁律 0.2 |
| 「按目标环境如实保留，而不是遗漏」在 `schema-boundaries.md` 与 `orm-auto-migration.md` 逐字重复 | `schema-boundaries.md`「铁律的适用范围」 | orm 文件删该句，只留「新表一律按铁律执行」 |
| `SKILL.md` 的 ON UPDATE 检查点复述了 `schema-examples.md:301/310` 已有的完整机理 | `schema-examples.md` GORM tag 小节 | `SKILL.md` 压成「结论 + 指针」 |

② **门控层叠 / 多套术语：发现 3 处，清理 3 处**

- `table-design-standards.md` 的小节标题也叫「铁律」，但条目是另一套措辞、无编号、不回指 `SKILL.md` 的
  编号铁律 → 标题改为「迁移管理要点」，加一句「口径以 `SKILL.md` 编号铁律为准，『铁律』一词专指该编号
  体系」，并补上指向 `orm-auto-migration.md` 的入口（原先只指向人工 DDL 的 migration-safety）。
- 同一组铁律在 `schema-boundaries.md` 与 `orm-auto-migration.md` 用了两套自然语言别名、顺序还不同
  → 两处统一改为编号引用（铁律 1~5）。
- `SKILL.md`「默认执行流程」第 6-9 条是对铁律 0/0.1/0.2 与「进入后先做」的第三次重抄 → **整块删除**，
  该节回归「读哪些 reference + 输出什么」的单一职责，并加一条引导说明去哪看那些要求。

③ **散落产物：本轮引入 0 处**。`source-notes.md` 与 `workbuddy-absorption-map.md` 不被 SKILL.md 引用属
`skill-absorption-rules` 的登记约定，正常。扫描另发现 3 个**本轮之前就存在**的孤立文件（
`test-strategy-rules/references/doc-minimums.md`、`test-program-rules/references/mock-factory-pattern.md`
与 `test-program-rules/references/runtime-mock-pattern.md`），不由本次吸收引入且属其他 skill 的域，
按「单一可编辑资产」原则本轮不动，登记备查。

④ **引用链**：`SKILL.md` 引用的 5 个 reference 全部存在可达；`orm-auto-migration.md` 内部引用的 4 个
文件全部可达；跨 skill 引用 `code-style-consistency-rules/references/user-style-feedback-library.md`
目标存在。修复了扫描发现的 **1 处悬空指针**（本节原写"见本节末尾扫描结论"但无该子节，现已填入）与
**4 处失效条号引用**（本轮把「进入后先做」16 条收敛为 10 条，导致旧登记里的"第 16 条""第 15 条"全部
错位）——登记文件统一改为「按小节名 + 规则名」引用，不再写条号。

⑤ **跨 skill 规则冲突：发现 1 处，已修（本次最重要的一条）**。`orm-auto-migration.md` 段 5 原写"凡是能
拿到 dump 的环境（local / 预发 / 生产副本）都要跑"并给出 `mysqldump` 直连命令，字面上会要求 Agent 直连
`pre` / `prod` 配置声明的库，**撞 `test-strategy-rules` 的本地环境红线**。已在 schema 侧收紧（红线权威留
在 `test-strategy-rules`，不在此另开口子）：Agent 只允许直连 local 导 dump，非 local 环境的 dump 必须由
人工/运维离线导出后作为文件提供，Agent 只消费文件；拿不到就用 local 跑并写明未覆盖环境，不得以此跳过段 5。

⑥ **确认无冗余**：`database-query-rules`（已采用「权威在 schema 侧、query 侧只查引用」模式）、
`test-strategy-rules` / `test-program-rules`（验证矩阵与假 PASS 陷阱关键词全树零命中）、
`code-style-consistency-rules`（反例库只承载正反例并回指权威）、`execution-failure-learning-rules`、
`golang-patterns` 均与新增内容零重复。

**遗留建议（不在本轮改，属其他 skill 的可编辑资产）**：`orm-auto-migration.md` 陷阱 3 的「`Save` 用全部
主键拼 `WHERE`」是 query 域语义，`database-query-rules` 的 `Save` 规则处目前无回链，建议后续补一行指针
（定义仍留 schema 侧）。

**扫描结论：PASS**（发现 9 处可清理项 + 1 处红线冲突，全部在本闭环内收敛）。

**整理去重（本轮存量整理）**：
1. **SKILL.md 三处铁律重抄收敛**——原「进入后先做什么」第 5-11 项、「默认执行流程」第 8-14 项都把铁律 1~6
   逐条重抄了一遍（与「Skill 作用与适用场景」的铁律正文三重重复）。现收敛为各一条"逐条核对铁律 1~6，
   判定细则见 `schema-boundaries.md`"，「进入后先做」16 条 → 10 条，「执行流程」16 条 → 11 条。
2. **阻断口径统一**——原阻断要求散落在铁律 0、进入后先做第 3 条、执行流程第 5 条、通过/驳回标准共 4 处，
   且措辞不一。现统一由铁律 0 定义，其余 3 处改为引用它。
3. **`schema-boundaries.md` 两份检查清单合并**——原「检查清单」与「检查清单（通用）」的变更性质检查项重叠，
   合并为「变更性质检查」一节并补一条存量表判据。

**净增体积（收口时按磁盘实测，非中间态）**：

| 文件 | 吸收前 | 收口后 | 说明 |
|---|---|---|---|
| `SKILL.md` | 137 行 / 16819 字节 | **131 行** / 18731 字节 | 行数 −6（收敛三处重抄 + 删掉「执行流程」6-9 整块）；字节 +1912，来自铁律 0 分流定义、铁律 0.2 边界定义与铁律 3 口径收口——用"一处完整定义"换掉"多处半句重抄" |
| `references/orm-auto-migration.md` | 无 | **245 行** / 15198 字节 | 新增，本轮全部新知识的集中落点 |
| `references/schema-boundaries.md` | 209 行 | **251 行** | 新增外键铁律小节（补委派断链）、铁律适用范围、`updated_at` 口径收口；两份检查清单合并 |
| `references/table-design-standards.md` | 263 行 | **267 行** | 「铁律」小节改名「迁移管理要点」+ 口径回指 + 补新文件入口 |
| `references/migration-safety-and-rollback.md` | 25 行 | **29 行** | 加指向新文件的场景分界 |
| `references/schema-examples.md` | 310 行 | **312 行** | 补一句说明与铁律 0.2 的关系（为何反例 13 仍须遵守） |

登记文件（`source-notes.md` +27 行、本表 +98 行）不计入规则内容，属流程要求的可追溯记录。

引用链自检：SKILL.md 引用的 5 个 reference 全部存在可达；`orm-auto-migration.md` 内部 4 处引用可达；
跨 skill 引用目标存在。

**独立评分（棘轮验证）**：由独立子 agent 按 `skill-absorption-rules/references/darwin-rubric.md` 的 8 维
标准评分，**86.0 分 vs 基线 64.0 分**，净增 +22，远超 1 分早停阈值 → **保留本次吸收**。

- 提升最大的两维：实测表现（权重 25，6→9，场景 A/B 从"完全无法处理、且原铁律 0 会给出错误指导"变为
  "一步定位根因 + 显式否决错误答案 + 有可执行验证矩阵"）、边界条件覆盖（5→9，原铁律 0 的"一律阻断"
  本身是错误边界）。
- 唯一未净进步的维度：资源整合度（7→7），扣分即下面两处退化。
- **评分指出的两处本次引入的退化，已在同一闭环内修掉**：① 铁律 6（禁物理外键）的委派断链——SKILL.md
  说细则见 `schema-boundaries.md`，但该文件原本没有外键小节（细则在 `table-design-standards.md`），
  现已在 `schema-boundaries.md` 补齐外键铁律小节 + 检查清单项，委派成立；② "不得依赖建表 API 补齐索引"
  这句反模式警告在删「执行流程」整块时丢失，现已回填进「进入后先做」的索引检查项（该警告适用于所有
  自动建索引场景，不该只挂在按条件读取的存量表文件里）。
- 评分另指出的非阻断项也已处理：登记表的陈旧条号引用（4 处）与体积数字已按磁盘实测校正；
  `updated_at` 的"DB 层 vs ORM 层维护"口径张力已在铁律 3 与 `schema-boundaries.md` 收口为
  "必须自动维护、实现方二选一、项目内统一"。

**流程教训**：本轮在同域扫描与独立评分**尚在运行时**就开始按扫描结论改文件，导致评分 agent 读到了三个
互不相同的中间态快照，它在报告里明确指出"评分对象被并发修改两次、数字对不上"。下次应先让只读审计全部
回收、再统一落修改，或修改后重新评分；登记表的体积数字必须在收口时按磁盘复测一次，不能沿用中间态。

**已删除源**：N/A（内部实践，无外部安装源）。

## 内部更新：GORM tag 的 ON UPDATE 写法（2026-08-21）

**来源**：内部调整（无外部 skill）。用户基于 GORM 源码（`gorm.io/gorm` v1.25+ / `gorm.io/driver/mysql` v1.5+）验证得出的经验结论，要求固化到 skill：**不要写成把 `ON UPDATE CURRENT_TIMESTAMP` 放进 `default:` 标签的写法**。

**通道**：内部更新通道。**裁决结果**：合并 3 条 / 保留本地 0 条 / 拒绝 0 条。

| 条目 | 本地现状 | 裁决 | 落点 | 整理去重 |
|------|---------|------|------|---------|
| 禁止把 `ON UPDATE CURRENT_TIMESTAMP` 放进 GORM tag 的 `default:`（写法 A）：`MigrateColumn` 用 DB 报告值 `column_default`（只存 CURRENT_TIMESTAMP，ON UPDATE 在 EXTRA、驱动不比对）与 `field.DefaultValue`（含 ON UPDATE）比对永不相等 → 每次 AutoMigrate 重复 ALTER，迁移不幂等 | 本地 references 的 `updated_at` 全部是纯 SQL DDL 视角（顺序无关），无 GORM tag 写法规则 | 合并 | `references/schema-examples.md` 新增「GORM tag 写法（AutoMigrate 幂等性）」小节（反例 13）+ `SKILL.md`「进入后先做什么」的 GORM tag ON UPDATE 检查点 | 用一句话区分「纯 SQL 顺序无关 / GORM tag 位置敏感」两个视角，避免与现有正例 3、反例 3 产生表面矛盾；未在九个小节逐条复写（遵循本 skill 上次「表名单一定义源」吸收先例，只落必要位点） |
| 需要 DB 层兜底时用写法 B：`type:timestamp ON UPDATE CURRENT_TIMESTAMP;not null;default:CURRENT_TIMESTAMP`，比对通过、幂等 | 同上 | 合并 | 同上（正例 9 第二种） | 同上 |
| UpdatedAt 字段 GORM 默认 autoUpdateTime 应用层自动维护，DB 层 ON UPDATE 通常冗余，最干净写法 `column:updated_at;type:timestamp;not null;default:CURRENT_TIMESTAMP;comment:更新时间` | 铁律 3 只说「由数据库自动管理」，未区分 ORM 应用层维护场景 | 合并 | 同上（正例 9 第一种） | 澄清口径：非 ORM 项目 DB 层 ON UPDATE 保留；GORM 项目由 autoUpdateTime 接管，DB 层 ON UPDATE 可选，铁律 3 正文不动 |

**同域冗余扫描（落盘后执行）**：范围 = `database-schema-rules`、`database-query-rules`、`golang-patterns`、`code-style-consistency-rules`、`comment-rules`。① 重复段落：0 处——grep 全仓 `ON UPDATE`/`AutoMigrate`/`autoUpdateTime` 命中仅 database-schema-rules 自身文件与 comment 类 tag 示例，无同义规则；② 门控层叠：0 处——未新增独立门控，复用既有检查点小节；③ 散落产物：0 处——未新建文件，全部追加进既有 reference；④ 引用链：SKILL.md「进入后先做什么」的 ON UPDATE 检查点 → `references/schema-examples.md` 的 GORM tag 小节，可达。结论 **PASS**。

**净增体积**：`SKILL.md` +1 行、`schema-examples.md` +26 行；无删除项（目标小节为纯新增视角，与既有纯 SQL 视角无同义重复可清）。

**已删除源**：N/A（内部更新通道，无外部安装源）。

## 内部更新：表名单一定义源（2026-08-21）

**来源**：内部调整（无外部 skill）。用户在 EllipalFinance-go 项目截图指出 model 的 `TableName()` 与 repository 的 `tableName: "coins_browser_url_dict"` 是同一表名的两个真相源，要求"model 自带表名，repository 直接引用"。

**通道**：内部更新通道。**裁决结果**：合并 4 条 / 拒绝 1 条。

| 条目 | 本地现状 | 裁决 | 落点 | 整理去重 |
|------|---------|------|------|---------|
| 表名字面量只允许存在于模型文件与 DDL / 迁移脚本；模型必须显式实现表名方法 | 本地只有反引号规范与命名约定，无表名来源规则 | 合并 | `SKILL.md` 铁律 1.2 + description + 「进入后先做什么」的铁律核对项 + 权责边界 + 暂停确认 + 通过/驳回 | 只落 6 处必要位点，未按该 skill 既有习惯在九个小节逐条复写，避免制造新的重复段落 |
| 判定标准 + 正反例 + 三类例外（DDL、动态分表基串、一次性排查脚本） | 无 | 合并 | `references/schema-boundaries.md` 新增「铁律：表名单一定义源」+ 检查清单 1 项 | 正例直接引用项目真实代码，不另造样例；与 `schema-examples.md` 不重复 |
| 访问层必须引用模型表名方法，禁止硬编码 | `database-query-rules` 有邻近的「显式 Model(&X{})」规则，无表名来源规则 | 合并 | `database-query-rules` description + Skill 作用 + 触发信号 + 进入后先做 6 + 权责边界 + 通过/驳回 | 采用「单一权威 + 引用」：定义细则不复写，只写"权威在 database-schema-rules 铁律 1.2"，本 skill 仅检查引用是否正确 |
| 用户否定写法入全局风格反例库 | 反例库 3 条 active，无本条 | 合并 | `code-style-consistency-rules/references/user-style-feedback-library.md` STYLE-CASE-GO-004 | 只放正反例供写码前规避，规则依据回指 schema/query 两个 owner，不第三次定义规则 |
| 同步写进 `code-generation-style-rules` 通用风格契约 | 该 skill 已约定写码前加载反例库 active 条目与 `PROJECT_STYLE.md` | **拒绝** | — | 拒绝理由：会与 `database-*`、反例库形成三处交叉冗余；本条经反例库自动并入本轮风格契约，无需重复落条 |

**同域冗余扫描（落盘后执行）**：范围 = `database-schema-rules`、`database-query-rules`、`code-style-consistency-rules`、`code-generation-style-rules`。① 重复段落：0 处——定义细则唯一落在 schema 的 `schema-boundaries.md`，query 侧只写引用检查，反例库只写正反例；② 门控层叠：0 处——未新增独立门控，复用两 skill 既有的通过/驳回小节；③ 散落产物：0 处——未新建文件，全部追加进既有 reference；④ 引用链：`database-query-rules` → `database-schema-rules 铁律 1.2`、反例库 → 两个 owner，均可达。结论 **PASS**。

**净增体积**：`database-schema-rules/SKILL.md` +6 行、`schema-boundaries.md` +52 行、`database-query-rules/SKILL.md` +5 行（含 1 行编号修正）、反例库 +29 行。拒绝 1 条避免了第三份冗余定义；项目侧 `PROJECT_STYLE.md` 为**就地修正既有反例样例**，净增 0 行正文。

**已删除源**：N/A（内部更新通道，无外部安装源）。

## design-db__skillhub（2026-08-19）

**来源**：本地安装 `C:\Users\luode\.workbuddy\skills\design-db__skillhub`（skillhub 安装，9KB SKILL.md，无 references）。数据库表结构设计规范，PRD2PLAN 体系。

**裁决结果**：合并 ≈20 条 / 保留本地 2 条 / 部分合并 2 条。

| 外部精华 | 裁决 | 落点 | 整理去重 |
|---------|------|------|---------|
| 表/列/索引命名约定（小写+下划线、复数表名、`idx_`/`uk_` 前缀） | 合并 | `references/table-design-standards.md` 一、命名约定 | 本地此前无命名规范，纯新增 |
| 必备字段 + 审计字段三风格选型（at/by、time/creator、gmt_create） | 部分合并 | 同上一、二；created_at/updated_at 本地铁律 3 更强，仅补审计选型 | 复用本地铁律，不重复 created_at/updated_at 定义 |
| 数据类型选型表（BIGINT/VARCHAR/TEXT/JSON/DATETIME/DATE/CHAR） | 合并 | 同上三、数据类型选型 | 金额 DECIMAL(18,2) 拒绝（本地铁律 2 强制字符串），表中改为本地红线 |
| 索引设计（必建场景/组合索引/覆盖索引/禁忌） | 合并 | 同上四、索引设计 | 与 `schema-examples.md` 正例 6 交叉引用，不重复示例 |
| 约束设计（NOT NULL/DEFAULT/UNIQUE/CHECK） | 部分合并 | 同上五、约束 | 必声明项与本地检查清单重叠，仅补 CHECK 示例 |
| 外键策略（物理/逻辑二选一） | 拒绝（物理外键）+ 合并（逻辑外键） | 同上五 + SKILL.md 新增铁律 6 | 按用户个人规则「禁止外键」改为红线：禁止物理外键，逻辑外键列必须建索引 |
| 表设计（3NF/反范式/纵向横向拆分） | 合并 | 同上六 | 纯新增 |
| 关系映射（1:1/1:N/N:M/树形/版本化 + 关联表规则） | 合并 | 同上七 | 纯新增 |
| 软删除选型（is_deleted/deleted_at/ORM 过滤/唯一约束含 is_deleted） | 部分合并 | 同上八 | 本地铁律 5 强制 is_deleted 更强；补 ORM 自动过滤与唯一约束细节 |
| 迁移文件命名 `V{版本}__{描述}.sql` | 合并 | 同上九 | 迁移安全细则复用 `migration-safety-and-rollback.md`，不重复 |
| 常见设计模式（配置驱动表/多对多+属性/审计日志表） | 合并 | 同上十 | 低优先参考，简表收录 |
| 严禁清单 | 合并（本地化改写） | 同上「严禁清单」 | 剔除与本地冲突项（金额数值类型改为本地字符串红线），新增物理外键禁止项 |

**整理去重统计**：本地 `database-schema-rules` 此前无命名/类型/索引/关系规范，本次净增 1 个 reference（约 230 行）；通过与 `schema-boundaries.md`、`schema-examples.md`、`migration-safety-and-rollback.md` 交叉引用，避免重复示例，SKILL.md 仅新增铁律 6 及相应读取规则。

**已删除源**：`C:\Users\luode\.workbuddy\skills\design-db__skillhub`（吸收完成后删除）。
