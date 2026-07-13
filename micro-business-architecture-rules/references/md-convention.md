# 微业务 md 规范

本文件定义微业务架构下的统一 md 文档规范，目标是让 AI 只读单个业务包的上下文即可分析其实现逻辑，无需扫描全仓。

统一 md 规范定义三类文档：每业务包 README、全局业务包索引、公共接口契约清单。三类文档都落在代码目录，不落 `doc/`；路径与命名统一遵循 `artifact-storage-rules`，本文件不自定义路径。

- 分层落点（handler/logic/store 等层内规则）交给 `package-structure-rules`。
- 隔离与通信契约见 `references/isolation-and-communication.md`。
- 本文件只负责三类 md 文档的字段、落点、维护规则与「AI 只读单业务上下文」的落地机制。

## 三类 md 文档总览

| 文档类型 | 落点 | 数量 | 模板 | 职责 |
|---|---|---|---|---|
| 每业务包 README | `internal/business/<域>/README.md` | 每业务包一份 | `templates/business-readme-template.md` | 描述单个业务包的职责、边界、结构、接口与关键链路 |
| 全局业务包索引 | `internal/business/README.md` | 全仓一份 | `templates/business-index-template.md` | 汇总全部业务包清单，作为 AI 的定位入口 |
| 公共接口契约清单 | `internal/contract/README.md` | 全仓一份 | `templates/business-index-template.md` | 汇总全部跨业务接口的暴露方 / 实现方 / 调用方 / 用途 |

## 一、每业务包 README

- 落点：`internal/business/<域>/README.md`（每个业务包各自一份）。
- 模板：`templates/business-readme-template.md`。
- 定位：单业务上下文的核心入口，AI 读它即可掌握该业务对外契约与内部结构。

字段清单（顺序固定，字段名严格一致）：

| 字段 | 内容要求 |
|---|---|
| 业务职责 | 用一段话说明本业务包负责什么，覆盖哪些核心能力 |
| 边界（本包做什么 / 不做什么） | 分「本包做什么」与「本包不做什么」两组，明确职责边界与不承担的部分 |
| 目录结构 | 列出本业务包内部子目录（handler/logic/model/store 等）及各自职责 |
| 对外接口（引用 `contract/<self>`） | 列出本业务在公共接口包中对外暴露的接口，引用 `contract/<self>` 下的契约；无对外接口时写 `N/A + 原因` |
| 依赖的其他业务接口（引用 `contract/<other>`） | 列出本业务调用的其他业务接口，引用 `contract/<other>`；无跨业务依赖时写 `N/A + 原因` |
| 私有数据模型入口 | 指向本业务私有数据结构 / 存储模型的入口位置（如 `model/`、`store/`） |
| 关键链路 | 描述本业务 1-3 条主链路（入口 → 逻辑 → 存储 / 跨业务调用），供 AI 快速理解实现走向 |

> 「对外接口」与「依赖的其他业务接口」必须引用 `contract/` 下的接口，不得直接引用其他业务包内部路径；这是隔离规则在文档层的体现。

## 二、全局业务包索引

- 落点：`internal/business/README.md`（全仓唯一一份）。
- 模板：`templates/business-index-template.md`。
- 定位：AI 进入仓库的第一定位入口——先读它锁定目标业务包，再深入该包 README + 代码。

字段清单（字段名严格一致）：

| 字段 | 内容要求 |
|---|---|
| 业务包清单 | 列出全部业务包（`internal/business/<域>/`） |
| 每个业务一句话职责 | 每个业务包配一句话职责概述 |
| 状态（活跃 / 冻结） | 标注每个业务包状态：`活跃` 或 `冻结` |
| 指向各业务包 README 的链接 | 每个业务包给出指向其 `README.md` 的相对链接，供 AI 直接跳转 |

推荐用一张表呈现，例如：

```markdown
| 业务包 | 一句话职责 | 状态 | README |
|---|---|---|---|
| order | 负责订单创建、查询与状态流转 | 活跃 | [order/README.md](./order/README.md) |
| user  | 负责用户资料与身份查询         | 活跃 | [user/README.md](./user/README.md) |
```

## 三、公共接口契约清单

- 落点：`internal/contract/README.md`（全仓唯一一份）。
- 模板：`templates/business-index-template.md`。
- 定位：跨业务通信的全局视图，AI 读它即可掌握业务之间「谁暴露、谁实现、谁调用」的接口关系。

字段清单（每条接口一行，字段名严格一致）：

| 字段 | 内容要求 |
|---|---|
| 暴露方业务 | 在 `contract/<name>` 声明该接口的业务 |
| 实现方 | 实现该接口的业务包（通常与暴露方一致） |
| 调用方业务 | 通过该接口发起跨业务调用的业务 |
| 用途 | 该接口解决的跨业务能力 / 场景 |

推荐用一张表呈现，例如：

```markdown
| 接口 | 暴露方业务 | 实现方 | 调用方业务 | 用途 |
|---|---|---|---|---|
| contract/user.Reader | user | user | order | order 展示订单时查询用户名 |
```

> 只有存在真实跨业务调用点的接口才登记；不得为「以后可能用」预建接口后登记空行（服从 `references/isolation-and-communication.md` 的接口按需原则与 `code-readability-rules`）。

## 落点映射

三类 md 全部落在代码目录，不落 `doc/`：

| 文档 | 落点（代码目录） | 是否落 doc/ |
|---|---|---|
| 每业务包 README | `internal/business/<域>/README.md` | 否 |
| 全局业务包索引 | `internal/business/README.md` | 否 |
| 公共接口契约清单 | `internal/contract/README.md` | 否 |

弱回写（可选，非强制）：

- 微业务采用决策与业务清单入口可弱回写到 `doc/1-架构/3-模块职责.md`（联动 `architecture-doc-rules`）与根目录 `项目设计.md`。
- 弱回写的路径一律遵循 `artifact-storage-rules`，不自定义；`doc/` 侧只做结构结论的摘要与指向，真实、权威、最新的业务/接口信息始终以代码目录内的三类 md 为准。
- 代码目录内的三类 md 与 `doc/` 弱回写内容冲突时，以代码目录内的 md 为准。

## 为什么这样设计（AI 只读单业务上下文的落地机制）

- 全局业务包索引（`internal/business/README.md`）让 AI 先一步定位到目标业务包，而不必扫描全仓源码。
- 定位后，AI 只需读「目标业务包 README + 该包代码」即可完成该业务的分析与实现；跨业务依赖通过 README 中引用的 `contract/<other>` 接口即可理解，无需读入其他业务包的内部实现。
- 公共接口契约清单（`internal/contract/README.md`）提供跨业务关系的全局视图，让 AI 在需要跟踪跨业务调用时，仍能只沿接口边界扩展上下文，而非把相关业务包全量读入。
- 三类文档配合业务包横向零依赖的隔离规则，共同构成「AI 只读单业务上下文即可分析实现」的落地机制：文档负责定位与契约可读，隔离规则负责保证单业务上下文自包含。

## 维护规则

三类 md 是隔离架构可读性的组成部分，维护缺任一视为未收口：

- 新增业务包：必须同时更新全局业务包索引（`internal/business/README.md`），补上该业务包的清单行、一句话职责、状态与 README 链接；并为该业务包创建自己的 `README.md`。
- 新增跨业务接口：必须同时更新公共接口契约清单（`internal/contract/README.md`），补上暴露方 / 实现方 / 调用方 / 用途；相关业务包 README 的「对外接口」与「依赖的其他业务接口」字段同步更新。
- 业务包冻结 / 下线：在全局业务包索引中把状态改为 `冻结`，不删除历史行。
- 缺任一同步更新（新业务包漏登索引、新接口漏登契约清单、README 接口字段与契约清单不一致）均视为未收口，必须补齐后才能结束当前改动。
- 所有 md 新增或修改一律 UTF-8 落盘，中文正文，纯 Markdown，写入后回读确认无乱码。
