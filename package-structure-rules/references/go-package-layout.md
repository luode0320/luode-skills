# Go 后端物理位置映射

## 二进制入口

独立 Go 后端的主入口文件直接放在项目根 `main.go`；其他二进制才放在 `cmd/<binary>/main.go`。前后端同仓时，后端入口统一放在 `backend/main.go` 或 `backend/cmd/<binary>/main.go`。`cmd/main.go`、同仓根 `main.go`、同仓根 `cmd/` 和 `backend/cmd/main.go` 都不属于入口 pattern。入口由项目维护者按实际 binary 创建，目录 `init` 不生成占位文件。

Go 私有源码根为 `internal/`，其下只使用 `router/`、`controller/`、`business/<domain>/`。项目关联工具统一放在根 `common/util/`，直接存放可依赖项目其他包的 Go 文件，不得创建子目录。业务域内使用 `api/`、`service/`、`entity/`、`base/`、`constant/`、`init/`、`crontask/`、`util/`、`rpc/`，其中业务域 `util/` 只承载本域私有辅助能力，`rpc/` 只直接存放面向其他业务域的 `func Operation(requestJSON string) string` 公开入口。

项目根 `utils/` 承载可独立复制的工具包与 SDK；其自身不得存放文件，所有实现必须位于 `utils/<package>/` 或更深的真实技术子目录，且不得依赖项目其他包。根 `database/` 承载持久化模型与 Repository；根 `common/request/`、`common/response/` 承载跨模块传输结构。不得再创建 `internal/service/`、`internal/entity/`、源码根 `util/`、`common/model/`、`common/sql/` 等旧位置。
