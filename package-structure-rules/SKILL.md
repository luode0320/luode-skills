---
name: package-structure-rules
description: 用于判断前后端同仓、独立后端、独立前端项目中新增或修改目录、包、模块、数据库资产、静态数据、配置、公共结构、工具包、第三方 SDK、中间件、定时任务、异步任务与源码层的唯一位置、职责和依赖方向；目录查询、渲染、初始化和检查统一由本 Skill 的 Catalog 负责。
---

# 代码位置目录规则 V2

本 Skill 是代码位置、查找和引用的唯一 Owner。它只保留三类项目：前后端同仓、独立后端、独立前端。

## 唯一事实源

- 人工可读目录树：`references/project-layout-v2.md`。
- 机器可读目录事实：`references/placement-catalog.yaml`。
- 目录查询与检查入口：`scripts/placement_catalog.py`。
- 查找、复用、引用与依赖方向：`references/lookup-and-reference-contract.md`。
- 配置、数据库、后端工具包、前端目录分别由对应 reference 细化。

当人工文档与 Catalog 不一致时，停止新增目录；先修复两者一致性，再继续生成或引用代码。

## 核心边界

1. 同仓根仅保存工作区资产、`integration/` 和 `doc/`；后端、前端业务资产分别留在其独立项目中。
2. 后端根级唯一位置：`config/`、`database/`、`utils/`、`common/`、`global/`、`crontask/`、`async/`、`middleware/`；不建立根 `data/`。
3. 前后端同仓、独立后端、独立前端的项目根均固定提交 `AGENTS.md`、`CLAUDE.md`、`PROJECT_CURRENT.md`、`PROJECT_MEMORY.md`、`PROJECT_HISTORY.md`；`PROJECT_STYLE.md` 仅在确有长期风格时创建并提交。`AGENTS.md` 与 `CLAUDE.md` 正文必须一致，分别供 Codex 与 Claude Code 读取；目录规则只负责其位置、初始化、查询和只读一致性检查，具体正文结构由项目规则、项目记忆与项目风格 Owner 管理。
4. 后端根 `utils/` 承载可独立复制的技术工具包与 SDK；根目录只允许工具包子目录，不得直接存放文件，也不得依赖项目其他包。IP 地址提取、标准化与归属查询只进入 `utils/ip/`；服务注册发现只允许 `utils/discovery/polaris/`、`utils/discovery/nacos/`。
5. 后端 `common/` 只允许 `request/`、`response/`、`constant/`、`error/`、`validation/`。
6. 后端语言源码根只承载 `router/`、`controller/`、`util/`、`business/<domain>/`；源码根 `util/` 直接存放可依赖项目其他包的高关联工具函数，禁止建立子目录。业务域内部只使用 `api/`、`service/`、`entity/`、`base/`、`constant/`、`init/`、`crontask/`、`util/`、`rpc/`；其中 `rpc/` 是其他微业务唯一可导入的 JSON 字符串公开通信入口，业务域 `util/` 保留为域私有辅助能力。
7. `database/connection/` 是关系型数据库、Redis、Mongo 等数据存储服务的连接、连接池与客户端初始化源码入口；`database/model/` 只允许 `db/`、`redis/`、`mongo/` 子目录。`database/migration/` 是自动迁移生产源码；独立 SQL 只进入 `database/sql/ddl/`、`database/sql/index/` 或 `database/sql/field/{create,update,delete}/`，每个叶子目录只直接存放 `.sql` 文件。
8. 不建立根 `protocol/`、项目级 `schema/`、业务源码内独立 `tests/`、`infrastructure/`、`third_party/`、`supply-chain/`、`coverage/`；仓库根 `test/` 是唯一活动测试代码根，不属于生产包结构。
9. Swag 内部目录与 YAML 规则只引用 `swag-openapi-maintainer-rules`。

## 使用方式

先查询，再创建或引用：

```bash
python package-structure-rules/scripts/placement_catalog.py query --artifact utils --category discovery --technology polaris
python package-structure-rules/scripts/placement_catalog.py query --artifact utils --category ip
python package-structure-rules/scripts/placement_catalog.py query --artifact source-util --language go
python package-structure-rules/scripts/placement_catalog.py query --artifact business-rpc
python package-structure-rules/scripts/placement_catalog.py query --artifact project-governance --category agents
python package-structure-rules/scripts/placement_catalog.py query --project-kind frontend --artifact project-governance --category claude
python package-structure-rules/scripts/placement_catalog.py query --artifact database-migration --category field --operation create
python package-structure-rules/scripts/placement_catalog.py render --all
python package-structure-rules/scripts/placement_catalog.py check --root <项目根目录> --project-kind backend --language go --policy strict
python package-structure-rules/scripts/placement_catalog.py check --root <旧项目根目录> --project-kind backend --language go --policy adoption --adoption-manifest doc/1-架构/3-目录规则收敛清单.yaml
```

`check` 始终只读；后端 `strict` 必须同时传入 `--project-kind backend` 与 `--language`，以准确识别源码根 `util/`。当 `AGENTS.md` 与 `CLAUDE.md` 同时存在时，strict 必须拒绝正文不一致；旧项目缺失其中之一时不因此自动迁移。`init` 创建必需目录和必需根文件，并仅在 `--enable backend.root.project-style` 时创建条件 `PROJECT_STYLE.md`；它不移动、不删除、不重命名用户文件，也不代替对应 Owner 填充文件正文。

创建业务域 `rpc/` 时，`init` 必须显式传入 `--enable backend.business-rpc --domain <domain> --language <language>`；Java 另传 `--base-package <base-package>`。调用方只可导入目标域 `rpc/` 的公开函数，参数和返回值均为 JSON 字符串；返回值遵循根 `common/response.Response` 的 `code`、`status`、`message`、`data` 语义。

## 旧项目渐进采纳

旧项目不自动迁移目录。项目人工维护的收敛清单固定为 `doc/1-架构/3-目录规则收敛清单.yaml`：

- `adopted_paths` 仅登记可由 V2 Catalog 唯一匹配的规范路径；该路径后续扩展仍必须遵守匹配的 Catalog 目录、内容类型和子目录约束。
- `legacy_source_roots` 登记已冻结的遗留源码根及其当时已有目录和文件；其中内容只能维护，禁止新增源码文件或源码目录。
- 收敛清单使用 UTF-8 YAML；本机具备 PyYAML 时接受普通缩进 YAML，缺少该库时仅可使用 JSON 兼容 YAML。
- 名称或职责相似的遗留目录不得自动推断为可沿用；必须人工登记为 `legacy_source_roots` 后才可继续维护。
- 新业务、新模块和可独立演进的新逻辑必须进入 V2 Catalog 唯一位置，不得在 `legacy_source_roots` 内新增实现。
- `strict` 与 `legacy` 策略保持原有语义；`adoption` 策略依据收敛清单核验渐进采纳边界。`check`、`init`、`render` 均不得创建、修改或补全收敛清单。

## 相邻 Skill 边界

- `swag-openapi-maintainer-rules`：拥有 Swag/OpenAPI 内部文件规则。
- `architecture-doc-rules`：拥有项目真实目录树文档；目录新增、删除、迁移后必须更新 `doc/1-架构/2-目录树.md`。
- `code-snippet-location-rules`：拥有用户仅提供代码片段时的真实文件定位流程。
- `codegraph-analysis-rules`：拥有符号、调用链与影响面分析。
- `common-util-rules`：拥有公共复用资格；实际物理路径仍以本 Skill Catalog 为准。

## 通过标准

- 同一项目类型、代码类型、能力、技术与操作只返回一个规范位置。
- Catalog、目录树、CLI 和测试 fixture 对相同规则给出一致结论。
- 禁止路径、源码与 SQL 混放、非法子目录在 strict 策略下稳定失败。
- 目录规则变更后，更新真实项目目录树文档与相邻 Skill 引用，不复制竞争 Owner。
