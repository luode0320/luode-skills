# Go 后端物理位置映射

Go 私有源码根为 `internal/`，其下只使用 `router/`、`controller/`、`util/`、`business/<domain>/`。`internal/util/` 直接存放可依赖项目其他包的高关联工具函数；不得创建其子目录。业务域内使用 `api/`、`service/`、`entity/`、`base/`、`constant/`、`init/`、`corntask/`、`util/`、`rpc/`，其中业务域 `util/` 只承载本域私有辅助能力，`rpc/` 只直接存放面向其他业务域的 `func Operation(requestJSON string) string` 公开入口。

项目根 `utils/` 承载可独立复制的工具包与 SDK；其自身不得存放文件，所有实现必须位于 `utils/<package>/` 或更深的真实技术子目录，且不得依赖项目其他包。根 `database/` 承载持久化模型与 Repository；根 `common/request/`、`common/response/` 承载跨模块传输结构。不得再创建 `internal/service/`、`internal/entity/`、根 `util/`、`common/model/`、`common/sql/` 等旧位置。
