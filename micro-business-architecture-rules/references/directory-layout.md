# 微业务目录布局

## 用途

本文件只说明微业务之间的隔离与公开通信面。业务域内的实际层次、语言源码根与文件扩展名由 `package-structure-rules` 唯一决定；这里不再定义根 `contract/` 或竞争目录树。

## 统一目录形态

```text
<source-root>/
└── business/
    └── <domain>/
        ├── api/              # 域私有 API 调用与适配
        ├── service/          # 域私有业务流程
        ├── entity/           # 域私有领域实体
        ├── base/             # 域私有基础结构
        ├── constant/         # 域私有常量
        ├── init/             # 域私有初始化
        ├── crontask/         # 域私有定时任务实现
        ├── util/             # 域私有辅助
        └── rpc/              # [条件·提交] 跨域公开 JSON 字符串函数，文件直接落盘
            └── <operation>.<ext>
```

- `rpc/` 仅在存在真实跨业务调用时创建；不得创建字面量 `<domain>` 或 `<operation>` 目录、文件。
- `rpc/` 不建立子目录；只直接放当前语言的公开函数实现。
- Go、Java、Node.js、Python 的 `<source-root>` 物理位置和 `init` 参数由 `placement_catalog.py query --artifact business-rpc` 返回。
- 根 `contract/` 不再是微业务通信目录，也不应作为迁移兼容层继续创建。

## 依赖方向

| 起点 | 终点 | 结论 | 原因 |
|---|---|---|---|
| `business/A` | `business/B/rpc` | 允许 | B 对外公开的 JSON 字符串通信入口。 |
| `business/A` | 根 `common/` 五类目录 | 允许 | 稳定公共请求、响应、常量、错误与校验结构。 |
| `business/A` | 根 `global/` 的非业务运行引用 | 条件允许 | 仅配置、日志、数据库连接和技术客户端等已装配能力。 |
| `business/A` | `business/B/{api,service,entity,base,constant,init,crontask,util}` | 禁止 | 目标业务私有实现，必须改走 B 的 `rpc/`。 |
| `global/` | 任意 `business/*` | 禁止 | 全局引用层不能成为业务状态或业务数据的隐式通道。 |

## Go 例子

```text
internal/business/
├── orders/
│   ├── service/
│   └── rpc/
└── users/
    ├── service/
    ├── entity/
    └── rpc/
        └── get_profile.go
```

`orders` 只能导入 `internal/business/users/rpc`；它不能导入 `users/service` 或 `users/entity`。`users/rpc/get_profile.go` 自行调用 `users` 域的 `service/`，并把结果封装为 JSON 响应字符串。
