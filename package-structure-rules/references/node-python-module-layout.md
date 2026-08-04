# Node.js 与 Python 后端物理位置映射

Node.js 源码根为 `src/`；Python 源码根为 `src/<package>/`。两者的私有源码根只使用 `router/`、`controller/`、`business/<domain>/`。项目关联工具统一放在根 `common/util/`，直接存放当前语言代码文件，不得创建子目录；业务域内部使用 V2 固定九类子目录，业务域 `util/` 保留为域私有辅助能力，`rpc/` 直接存放 `string -> string` 的 JSON 跨域公开函数。

根 `database/`、`utils/`、`common/`、`global/`、`crontask/`、`async/`、`middleware/` 与源码根并列。`utils/` 自身不得直接存放文件；实现必须进入 `utils/<package>/` 或更深的真实技术子目录，且不得依赖项目其他包。禁止在源码根内重复创建配置、公共结构、SDK 或数据库目录。
