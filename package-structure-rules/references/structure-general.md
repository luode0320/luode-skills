# 跨语言结构总则

代码位置以 `placement-catalog.yaml` 为唯一机器事实源；三类完整目录树见 `project-layout-v2.md`。前后端同仓、独立后端和独立前端的项目根都必须直接保存并提交 `Dockerfile`；同仓根只拥有工作区资产，独立后端与独立前端分别拥有自己的业务目录。
后端根级 `database/`、`utils/`、`common/`、`global/`、`crontask/`、`cachetask/`、`async/`、`middleware/` 不进入语言源码根。其中根 `utils/` 只包含可独立复制的工具包子目录，不得直接存放文件，也不得依赖项目其他包；`common/util/` 直接存放可依赖项目其他包的高关联工具函数，禁止建立子目录。源码根直连业务域 `<domain>/`，业务相关逻辑通过 `router/<v?>/`、`controller/<v?>/`、`entity/<v?>/`、`service/<v?>/` 四类版本化目录完全隔离，包名用 `v?router`、`v?controller`、`v?entity`、`v?service` 别名引用；未列出且不在禁止清单的其他目录允许存在，新增须用户确认，且不得作为规范目录的别名。不再建立源码根 `util/`。二进制入口是独立后端根 `main.<ext>`、独立后端额外入口 `cmd/<binary>/main.<ext>`，或同仓后端前缀 `backend/main.<ext>`、`backend/cmd/<binary>/main.<ext>`；`cmd/main.<ext>` 不属于额外入口。业务域 `<domain>/util/` 仍是域私有辅助能力；业务域之间禁止直接导入对方任何目录（无 `rpc/` 例外），跨域共享结构仅走根 `common/` 与 `global/` 非业务运行引用。三类项目根均固定保存同内容的 `AGENTS.md` 与 `CLAUDE.md`，以及 `PROJECT_CURRENT.md`、`PROJECT_MEMORY.md`、`PROJECT_HISTORY.md`，并按需保存 `PROJECT_STYLE.md`；这些文件不进入源码根。`AGENTS.md` 供 Codex，`CLAUDE.md` 供 Claude Code，二者不得独立演化。禁止后端项目根 `util/` 工具包目录、源码根 `util/`、根 `contract/`、根 `protocol/`、项目级 `schema/` 和 `infrastructure/`。
目录新增、迁移或职责调整后，必须更新项目真实目录树 `doc/1-架构/2-目录树.md`。

## 代码分解与目录内聚规则（强制）

阈值与合法例外唯一见 `AGENTS.md` 的「代码分解与目录内聚规则（强制）」，本节不重复数字。本文件只补目录侧增量：

1. **拆分后的落点**：同级 diamond 文件留在原业务目录内；判定为两种及以上业务时必须拆到不同规范目录，具体落在哪一个以 `placement-catalog.yaml` 为准。
2. **目录单一职责的判据**：一个目录只处理一个业务或一个处理阶段；同一业务的多阶段拆为同级文件，不得在单文件内混杂不同业务或处理切面。
3. **不留兼容壳**：拆分后旧文件不得保留转发桩、别名导出或空壳目录。
