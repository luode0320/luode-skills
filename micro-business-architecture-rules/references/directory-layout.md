# 微业务目录布局

## 用途

本文件只说明微业务之间的隔离边界与版本目录语义。业务域内的实际层次、语言源码根与文件扩展名由 `package-structure-rules` 唯一决定；这里不再定义根 `contract/` 或竞争目录树。

## 统一目录形态

```text
<source-root>/
└── <domain>/
    ├── init.<ext>          # [条件·提交] 域初始化入口文件；全量注册本域所有版本路由，/v1、/v2 前缀区分
    ├── api/                # [条件·提交] 域内 API 调用
    ├── base/               # [条件·提交] 业务基础结构
    ├── constant/           # [条件·提交] 域常量
    ├── util/               # [条件·提交] 域私有辅助；不属于根 utils/ 或 common/util/
    ├── router/             # [条件·提交] 路由装配目录；版本目录承载随版本变化的路由注册
    │   └── <v?>/           # [必需·提交] 版本管理，从 v1 起递增；包名用 v?router 别名引用
    ├── controller/         # [条件·提交] 输入与响应映射目录；版本目录承载随版本变化的转换逻辑
    │   └── <v?>/           # [必需·提交] 版本管理，从 v1 起递增；包名用 v?controller 别名引用
    ├── entity/             # [条件·提交] 领域实体目录；不同版本的实体会变化
    │   └── <v?>/           # [必需·提交] 版本管理，从 v1 起递增；包名用 v?entity 别名引用
    └── service/            # [必需·提交] 业务流程目录；版本目录承载随版本变化的业务流程
        └── <v?>/           # [必需·提交] 版本管理，从 v1 起递增；包名用 v?service 别名引用
```

- 业务域直连源码根，业务相关逻辑完全通过各版本目录 `<v?>` 隔离，其余为跨版本通用业务逻辑。版本目录挂在 `router/<v?>/`、`controller/<v?>/`、`entity/<v?>/`、`service/<v?>/` 各自之下。
- `<v?>` 解析为 `v[0-9]+`，`v1` 起；`scaffold` 默认创建 `v1`，新增版本时 `v2`、`v3` 递增，不自动迁移旧目录。
- 域级入口为单文件 `init.<ext>`（`<ext>` 为语言扩展名，如 Go 的 `init.go`），不再建立 `init/` 目录。
- Go、Java、Node.js、Python 的 `<source-root>` 物理位置由 `package-structure-rules` 唯一定义（Go=internal/、Java=src/main/java/<包>、Node=src/、Python=src/<包>）。

> 域级通用目录与版本目录是统一规范子目录，允许其他域私有目录存在，新增须用户确认，且不得代替规范目录职责。

## 依赖方向

| 起点 | 终点 | 结论 | 原因 |
|---|---|---|---|
| `<domain>/A` | 根 `common/` 五类目录 | 允许 | 稳定公共请求、响应、常量、错误与校验结构。 |
| `<domain>/A` | 根 `global/` 的非业务运行引用 | 条件允许 | 仅配置、日志、数据库连接和技术客户端等已装配能力。 |
| `<domain>/A` | `<domain>/B` 的任何目录 | 禁止 | 业务域之间禁止直连，共享结构仅走根 `common/` 与 `global/`。 |
| `global/` | 任意 `<domain>/*` | 禁止 | 全局引用层不能成为业务状态或业务数据的隐式通道。 |

## Go 例子

```text
internal/
├── orders/
│   ├── init.go            # 全量注册 orders 域 v1、v2 路由
│   ├── api/
│   ├── constant/
│   ├── router/
│   │   ├── v1/
│   │   └── v2/
│   ├── controller/
│   │   ├── v1/
│   │   └── v2/
│   ├── entity/
│   │   ├── v1/
│   │   └── v2/
│   └── service/
│       ├── v1/
│       └── v2/
└── users/
    ├── init.go
    ├── router/
    │   └── v1/
    ├── controller/
    │   └── v1/
    ├── entity/
    │   └── v1/
    └── service/
        └── v1/
```

`orders` 不能导入 `users` 的任何目录（含 `router/v1/`、`controller/v1/` 等所有版本目录内容）；跨域共享结构只能走根 `common/` 与 `global/`。`orders/init.go` 全量注册 `orders` 域的 `v1`、`v2` 路由，`/v1`、`/v2` 前缀区分，多版本并存对外。包名使用 `v1router`、`v2router`、`v1controller`、`v2controller`、`v1entity`、`v2entity`、`v1service`、`v2service` 别名引用区分版本。
