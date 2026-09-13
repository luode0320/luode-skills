# 公共工具索引文档契约

## 用途

本文件规定「项目内的公共工具索引文档」放在哪、写什么、何时更新，用来支撑 `common-util-rules` 的复用红线：新增任何工具方法前必须先全仓检索已有实现。索引是这个检索的可信入口，索引失真等同于复用红线失效。

本文件只定义索引文档的契约；复用资格、7 天冻结、放置判据仍以 `SKILL.md` 与 `util-placement.md` 为准。

## 一、落点（唯一，且必须 Catalog 合法）

- 唯一落点：`doc/1-架构/3-模块职责.md` 的 `## 公共工具索引` 小节。
- 内容过长时**只加小节层级**（如 `### utils/time`），不拆文件、不新增主入口。
- 禁止写成 `utils/<pkg>/README.md`：`utils/<pkg>` 在 `placement-catalog.yaml` 中的 `allowed_extensions` 只含源码扩展名（`.go` / `.java` / `.ts` / `.js` / `.py`），`.md` 不在其列，写入即破坏放置契约。
- 禁止在 `doc/` 下新建索引专用子目录或新序号文件：`doc/` 子目录已由 Catalog 固定，`doc/1-架构/` 的 `1-4` 主入口与 `5+` 业务链路序号已由 `artifact-storage-rules` 固定，新增需改 Catalog。
- 入口归属：索引小节的位置由本契约约定，`doc/1-架构/3-模块职责.md` 的文档结构仍由 `architecture-doc-rules` 与 `artifact-storage-rules` 管理。

## 二、索引字段（固定表格）

每个**导出**工具函数一行，字段固定，缺必填项即视为索引不完整：

| 字段 | 含义 | 必填 |
|---|---|---|
| 函数名 | 导出函数 / 方法名（不含包前缀） | 是 |
| 签名 | 参数与返回的一句话形态 | 是 |
| 一句话用途 | 脱离当前业务上下文仍然成立的作用 | 是 |
| 所属包 | `utils/<pkg>/` 或 `common/util/<函数>.<ext>` | 是 |
| 纯函数 | 是否满足确定性 / 无副作用 / 无 IO / 无项目依赖（是 / 否） | 是 |
| 首次引入 | 日期 + `DEC-*` / `TASK-*` 追溯锚点；无则写「首次提交」 | 否 |
| recipe 锚点 | 规则仓 recipe 定位（如 `usage-recipes-go.md#time`）；无则写「暂无」 | 否 |

包级条目：每个 `utils/<pkg>/` 先写一行包级说明（技术主题 + 用途），再列其函数行。

## 三、更新时机（强制）

- **新增**工具函数：同一轮改动内必须补索引行，未补视为该交付未完成，会被 `code-change-finalization-gate-rules` 拦截。
- **修改**签名、用途或所属包：同步修改索引行，不允许只改代码。
- **删除**工具函数：先删索引行与所有引用，再删实现（配合 `code-quality-rules` 的 `code-removal-discipline.md`）。
- **首次引入**新的 `utils/<pkg>/` 包：先补包级说明，再列函数行。
- 索引与代码不一致时以代码为准，且必须**当轮**修复索引；不允许留下"待补"状态。

## 四、与既有索引层的边界（不重复）

| 层 | 载体 | 粒度 | 与本契约的关系 |
|---|---|---|---|
| 机器放置事实 | `placement-catalog.yaml` | 目录 / 文件模式 | 本契约不复制；落点合法性以它为准 |
| CLI 目录查询 | `guide --category --language` | 目录 | 本契约不是查询入口 |
| 规则仓目录用法索引 | `package-structure-rules/references/directory-usage-routing.md` | 目录 | 规则仓自用，不是本契约的项目侧副本 |
| 规则仓 recipe 正文 | `package-structure-rules/references/usage-recipes-go.md` | 类别 / 用法 | 本契约只引用其锚点，不复制用法正文 |

本契约补的是**函数级**这一层：上位三层全是目录 / 类别级，无法回答"这个函数存在吗、放在哪个包、是不是纯函数"。

## 五、禁止

- 用 `data`、`info`、`util-all`、`工具大全` 这类聚合名承载索引。
- 把索引写成代码注释、`README` 或注释块的替代品（`utils/` 不放 `.md`）。
- 把未导出（包内私有）函数列入索引——索引只服务跨包复用。
- 索引只增不删，或长期停留在"待补"状态。
- 为一个函数同时维护两份索引（本契约与已知复用点冲突时，以本契约为唯一索引）。

## 六、与相邻规则的边界

- 复用红线、7 天冻结、复用检索：`common-util-rules/SKILL.md`。
- 放置判据（纯转换函数 → `utils/<pkg>/`；需项目依赖 → `common/util/`）：`util-placement.md`。
- 架构文档主入口与命名：`architecture-doc-rules`、`artifact-storage-rules`。
- 删除纪律：`code-quality-rules` 的 `code-removal-discipline.md`。
- 目录落点合法性：`package-structure-rules` 的 `placement-catalog.yaml`。
