# 微业务隔离与引用边界

## 规则定位

本文件拥有跨业务导入隔离的解释与检查流程；`package-structure-rules` 拥有目录的物理位置、允许扩展名和 Catalog 查询。两者对同一规则不重复定义。

## 允许与禁止的导入

业务域之间禁止直接导入对方任何目录（无 `rpc/` 例外）。跨域共享结构仅走根 `common/`（request/response/constant/error/validation）与 `global/` 非业务运行引用。

| 导入路径 | 结论 | 修复方式 |
|---|---|---|
| `.../common/request`、`.../common/response` 等五类目录 | 允许 | 使用稳定公共结构。 |
| `.../global/` 的非业务运行引用 | 条件允许 | 仅配置、日志、数据库连接和技术客户端。 |
| `.../internal/users/service/v1` | 禁止 | 业务域私有层，跨域共享结构下沉到根 `common/`。 |
| `.../internal/users/entity/v1` | 禁止 | 业务域私有实体，跨域共享 DTO 下沉到根 `common/`。 |
| `.../internal/users/util` | 禁止 | 业务域私有辅助，跨域能力收敛到根 `common/util/`。 |
| `.../internal/users` 的任何子路径 | 禁止 | 业务域之间禁止直连，无例外。 |

`scripts/micro_business.py check` 是确定性门禁：扫描 Go import，对任何指向另一真实业务域的 import 一律报违规。它必须在 CodeGraph 审查前通过。

## 版本目录语义

1. 业务相关逻辑完全通过各版本目录 `<v?>` 隔离，`v1` 起递增；版本目录挂在 `router/<v?>/`、`controller/<v?>/`、`entity/<v?>/`、`service/<v?>/` 各自之下。
2. 域级通用目录（`api/`、`base/`、`constant/`、`util/`）跨版本共享，不随版本演进。
3. 版本目录内（`router/<v?>/`、`controller/<v?>/`、`entity/<v?>/`、`service/<v?>/`）承载随版本变化的业务实现，包名用 `v?router`、`v?controller`、`v?entity`、`v?service` 别名引用。
4. 域级单文件 `init.<ext>` 全量注册本域所有版本路由，`/v1`、`/v2` 前缀区分；旧版本不因新版本诞生而下线。

## CodeGraph 审查闸门

目的：以实际导入节点证明确定性门禁没有漏判，并让审查者定位违规来源文件和行号。

1. 在包含 fixture 或目标项目的根执行 `codegraph sync <root>`。
2. 对每个目标域执行 `codegraph query -p <root> --kind import --limit 1000 --json "<module>/internal/<target>"`。
3. 违规证据必须显示调用文件导入目标域任何子路径（含版本目录、域级目录）；真实测试失败，且不得以 `6-review` 覆盖该行为问题。
4. CodeGraph 只提供可追溯的导入证据；允许路径的确定性裁决仍由 `micro_business.py check` 负责。

## 公共例外和 global 边界

- 可直接跨域使用的公共结构仅为根 `common/request`、`response`、`constant`、`error`、`validation`。
- `global/` 只暴露配置、日志、数据库连接、技术客户端等已装配的非业务运行引用。
- `global/` 不保存、传递或缓存任何业务实体、业务列表、业务状态和可变业务缓存；这些数据不能绕过 `common/` 流通。
