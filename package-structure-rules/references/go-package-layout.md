# Go 后端物理位置映射

## 二进制入口

独立 Go 后端的主入口文件直接放在项目根 `main.go`；其他二进制才放在 `cmd/<binary>/main.go`。前后端同仓时，后端入口统一放在 `backend/main.go` 或 `backend/cmd/<binary>/main.go`。`cmd/main.go`、同仓根 `main.go`、同仓根 `cmd/` 和 `backend/cmd/main.go` 都不属于入口 pattern。入口由项目维护者按实际 binary 创建，目录 `init` 不生成占位文件。

Go 私有源码根为 `internal/`，其下直连业务域 `<domain>/`，业务相关逻辑通过 `router/<v?>/`、`controller/<v?>/`、`entity/<v?>/`、`service/<v?>/` 四类版本化目录完全隔离，其余为跨版本通用业务逻辑；未列出且不在禁止清单的其他目录允许存在，新增须用户确认，且不得作为规范目录的别名。项目关联工具统一放在根 `common/util/`，直接存放可依赖项目其他包的 Go 文件，不得创建子目录。业务域级通用目录为 `api/`、`base/`、`constant/`、`util/` 与单文件 `init.go`（域初始化入口，全量注册本域所有版本路由，`/v1`、`/v2` 前缀区分）。版本化目录 `router/<v?>/`、`controller/<v?>/`、`entity/<v?>/`、`service/<v?>/` 内各自按版本隔离，版本从 `v1` 递增；包名用 `v?router`、`v?controller`、`v?entity`、`v?service` 别名引用。业务域之间禁止直接导入对方任何目录（无 `rpc/` 例外），跨域共享结构仅走根 `common/` 与 `global/` 非业务运行引用。

项目根 `utils/` 承载可独立复制的工具包与 SDK；其自身不得存放文件，所有实现必须位于 `utils/<package>/` 或更深的真实技术子目录，且不得依赖项目其他包。根 `database/` 承载持久化模型与 Repository；根 `common/request/`、`common/response/` 承载跨模块传输结构。不得再创建 `internal/service/`、`internal/entity/`、源码根 `util/`、`common/model/`、`common/sql/` 等旧位置。
