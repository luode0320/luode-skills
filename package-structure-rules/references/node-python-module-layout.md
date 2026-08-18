# Node.js 与 Python 后端物理位置映射

Node.js 源码根为 `src/`；Python 源码根为 `src/<package>/`。两者的私有源码根直连业务域 `<domain>/`，业务相关逻辑通过 `router/<v?>/`、`controller/<v?>/`、`entity/<v?>/`、`service/<v?>/` 四类版本化目录完全隔离；未列出且不在禁止清单的其他目录允许存在，新增须用户确认，且不得作为规范目录的别名。项目关联工具统一放在根 `common/util/`，直接存放当前语言代码文件，不得创建子目录；业务域级通用目录为 `api/`、`base/`、`constant/`、`util/` 与单文件 `init.<ext>`（Node.js 为 `init.ts`、Python 为 `init.py`）。版本化目录 `router/<v?>/`、`controller/<v?>/`、`entity/<v?>/`、`service/<v?>/` 内各自按版本隔离，版本从 `v1` 递增，包名用 `v?router`、`v?controller`、`v?entity`、`v?service` 别名引用。未列出的其他目录允许存在，新增须用户确认。业务域之间禁止直接导入对方任何目录（无 `rpc/` 例外）。业务域 `util/` 保留为域私有辅助能力。

根 `database/`、`utils/`、`common/`、`global/`、`crontask/`、`async/`、`middleware/` 与源码根并列。`utils/` 自身不得直接存放文件；实现必须进入 `utils/<package>/` 或更深的真实技术子目录，且不得依赖项目其他包。禁止在源码根内重复创建配置、公共结构、SDK 或数据库目录。
