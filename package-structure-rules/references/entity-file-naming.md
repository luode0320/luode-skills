# 领域实体文件粒度与命名规则

本文件是 `backend.entity`（`<source-root>/<domain>/entity/<v?>/`）内部**文件如何切分、如何命名**的唯一细则来源。目录本身的位置、版本化和包名别名仍以 `placement-catalog.yaml` 与 `project-layout-v2.md` 为准。

## 粒度：一个接口一个文件

`entity/<v?>/` 内**一个接口一个文件，请求与响应各自独立成文件**。

- 禁止把整个版本的请求结构聚合成 `request.<ext>`、响应结构聚合成 `response.<ext>`。聚合文件随接口增长会变成几百行的杂物文件，改一个接口要在长文件里翻找，定位成本高；文件级 diff 也无法反映"改了哪个接口"。
- 禁止按"层"或"类型"聚合（如 `dto.<ext>`、`vo.<ext>`、`types.<ext>`、`models.<ext>`）。这类命名不携带接口信息，等价于聚合文件。
- 一个文件内可以有多个结构，但它们必须属于**同一个接口**（见下节响应树）。

## 命名：req / resp 前缀 + 接口名

文件名由 `req` / `resp` 前缀加接口名构成，接口名取该接口的业务动作名（通常与路由末段或 controller 方法同名），不带版本号（版本已由所在目录表达）。

各语言的大小写形态受语言自身约束，按下表落地：

| 语言 | 请求文件 | 响应文件 | 形态约束来源 |
|---|---|---|---|
| Go | `req<Interface>.go` | `resp<Interface>.go` | 首字母小写驼峰，跟随 Go 社区文件名惯例 |
| TypeScript / JavaScript | `req<Interface>.ts` | `resp<Interface>.ts` | 首字母小写驼峰 |
| Java | `Req<Interface>.java` | `Resp<Interface>.java` | PascalCase，public 类名必须与文件名一致 |
| Python | `req_<interface>.py` | `resp_<interface>.py` | snake_case，跟随 PEP 8 模块命名 |

Go 示例：

```text
internal/<domain>/entity/v1/
├── reqGetMainPairs.go
├── reqGetToPairs.go
├── reqUpdateOrderUserStatus.go
├── respGetRange.go
└── respGetSupportSwitch.go
```

结构体（类）名本身沿用 `Req<Interface>` / `Resp<Interface>` 的导出命名，与文件名对应。**已有项目中先前采用后缀式命名的结构（如 `GetFromPairsPageResp`）不因本规则强制改名**：文件名按 `resp<Interface>` 规则命名即可（`respGetFromPairsPage.go`），类型改名属独立的重命名议题，需单独确认，避免为纯命名统一而扩大 diff。

## 同一接口的响应树留在一个文件

若某接口的响应由一个顶层结构加若干**只被它内嵌引用**的子结构组成，这些子结构与顶层结构放在同一个响应文件内，不再各自拆分。

判断依据是"是否服务于同一个接口"，不是"结构数量"。把只有几个字段的内嵌子结构拆成独立文件，会让读一个响应需要跳多个文件，与本规则要解决的定位问题相反。

例如活动曝光接口的响应树 `RespActivityExposure` 内嵌 `RespActivityGift` / `RespActivityPopup` / `RespActivityJump`，四者同处 `respActivityExposure.<ext>`。

若某子结构被**两个以上接口**共用，它已不属于单个接口，按下节转出。

## 跨接口与跨版本共享结构的出口

`entity/<v?>/` 只放版本专属结构。判断依据是**真实引用面**，不是名字：

- 只被本版本的 router / controller / service 引用 → 留在 `entity/<v?>/`。
- 被同版本内多个接口共用 → 仍在 `entity/<v?>/`，用能表达其语义的文件名（不套 `req`/`resp` 前缀），例如共享的分页条件、共享的币种视图。
- 被跨版本包（其他版本目录、领域通用包、根 `utils/`、根 `middleware/`）引用 → 必须放根 `common/request`、`common/response` 或 `common/dto`。把它下沉到 `entity/<v?>/` 会让跨版本包反向依赖具体版本目录。

迁移既有聚合文件前，先统计每个结构的真实使用方再分类；只按名字前缀猜测归属会漏掉公共包的引用，编译期才暴露。

## 合法与非法示例

合法：

- `internal/order/entity/v1/reqCreateOrder.go`、`internal/order/entity/v1/respCreateOrder.go`
- `internal/order/entity/v2/respActivityExposure.go`（含该接口的响应树共 4 个结构）
- `internal/order/entity/v1/respGetFromPairsPage.go`（类型名沿用既有 `GetFromPairsPageResp`）
- `src/main/java/<base>/order/entity/v1/ReqCreateOrder.java`

非法：

- `entity/v1/request.go`、`entity/v1/response.go`：聚合文件，难定位。
- `entity/v1/dto.go`、`entity/v1/types.go`、`entity/v1/models.go`：按类型聚合，文件名不携带接口信息。
- `entity/v1/reqV1CreateOrder.go`：版本号已由目录表达，文件名不再重复。
- `entity/v1/req_get_main_pairs.go`（Go 项目）：Go 侧应为小驼峰 `reqGetMainPairs.go`。
- `entity/v1/respActivityGift.go`：把只被 `RespActivityExposure` 内嵌的子结构单独拆出。
- `entity/v1/reqCommonParam.go` 承载被 middleware 与多版本共用的公共请求头：应放根 `common/request`。

## 与相邻规则的边界

- 目录位置、版本目录、包名别名：`placement-catalog.yaml` 的 `backend.entity` 与 `project-layout-v2.md`。
- 根 `common/request`、`common/response` 的职责：`project-layout-v2.md` 与 Catalog 对应条目。
- 具体语言的包声明与目录内组织惯例：`go-package-layout.md`、`java-layer-layout.md`、`node-python-module-layout.md`。
- 符号命名（结构体、字段）本身不由本文件管辖，交 `naming-rules`。
