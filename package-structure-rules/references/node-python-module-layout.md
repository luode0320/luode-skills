# Node.js 与 Python 后端物理位置映射

Node.js 源码根为 `src/`；Python 源码根为 `src/<package>/`。两者的私有源码根只使用 `router/`、`controller/`、`util/`、`business/<domain>/`。`src/util/` 与 `src/<package>/util/` 分别直接存放可依赖项目其他包的高关联工具函数，均不得创建子目录；业务域内部使用 V2 固定九类子目录，业务域 `util/` 保留为域私有辅助能力，`rpc/` 直接存放 `string -> string` 的 JSON 跨域公开函数。

根 `database/`、`utils/`、`common/`、`global/`、`corntask/`、`async/`、`middleware/` 与源码根并列。`utils/` 自身不得直接存放文件；实现必须进入 `utils/<package>/` 或更深的真实技术子目录，且不得依赖项目其他包。禁止在源码根内重复创建配置、公共结构、SDK 或数据库目录。
