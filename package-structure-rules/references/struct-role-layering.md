# 结构体角色与落点总谱（按语言生态）

本文件是“结构体 / 类型按类型与作用划分”的统一入口：判定一个结构属于哪个角色、落在哪个位置、注释写到什么颗粒度。

落点以 `placement-catalog.yaml` 与 `project-layout-v2.md` 为唯一事实源；`entity/<v?>/` 内的文件切分与 `req` / `resp` 命名见 `entity-file-naming.md`；符号命名见 `naming-rules`；注释语言与写法见 `comment-rules`。本文件只做角色映射与语言差异，不复制上述细则。

## 一、角色谱系与落点（语言无关）

| 角色 | 作用 | 引用面 | 落点 |
|---|---|---|---|
| 持久化模型 | 与表 / 集合一一对应 | 仅数据访问层 | `database/model/db/`、`database/model/redis/`、`database/model/mongo/` |
| 领域实体 | 跨业务域共享的核心业务模型 | 多业务域 | 根 `common/entity/` |
| 接口请求 / 响应 | 单个接口的入参 / 出参 | 单接口 | `<domain>/entity/<v?>/` 的 `req*` / `resp*` |
| 公共传输结构 | 多接口或跨版本共享的入参出参 | 多接口、跨版本 | `common/request/`、`common/response/`、`common/dto/` |
| 配置结构 | 配置文件的映射结构 | 配置加载层 | 后端 `config/model.<ext>` |
| 函数参数结构 | 收敛函数签名 | 单函数及其调用链 | 与函数同包（见 `code-quality-rules` 的 `function-signature-rules.md`） |
| 内部临时结构 | 包内中间计算、不外传 | 单包 | 就近定义在所属包，**不得**进入 `entity/` 与 `common/` |

判定顺序（引用面从小到大，命中即停）：

1. 只在一个包内使用 → 内部临时结构，就近定义，不新建跨包文件。
2. 只服务一个接口 → 接口请求 / 响应，落 `entity/<v?>/`。
3. 被多个接口或跨版本引用 → 公共传输结构，落 `common/` 对应目录。
4. 跨业务域共享的业务模型 → 领域实体，落 `common/entity/`。
5. 对应存储表或集合 → 持久化模型，落 `database/model/` 对应子目录。

## 二、按语言生态的差异

### Go

- 角色载体为 `struct`，**用导出性表达外传边界**：跨包可见用导出名（`RespCreateOrder`），包内临时结构用小写（`orderParams`）。
- 内部临时结构不新建文件，直接写在所属包内。
- 公共实体与公共传输结构必须是导出结构。

### Java

- 角色载体为 `class` 或 `record`；public 类名必须与文件名一致（JVM 约束）。
- 项目已有 PO / DTO / VO / BO 分层约定时沿用既有约定，不强制改名；无既有约定时按本谱系命名（`XxxEntity` / `XxxDto` / `XxxReq` / `XxxResp`）。
- 内部临时结构用包私有或嵌套静态类，不新建文件。

### TypeScript / JavaScript

- 角色载体为 `interface`、`type` 或 `class`；结构化数据统一用 `interface`，`type` 只用于联合类型与工具类型。
- 前端与后端共享的类型契约放 `common/` 对应目录，不在组件或页面目录里重复定义。

### Python

- 角色载体为 `dataclass` 或 Pydantic `BaseModel`；带校验的输入模型用 Pydantic，内部临时结构用 `dataclass` 或 `NamedTuple`。
- 命名走 snake_case，与模块命名一致。

## 三、注释要求（按角色）

- 所有角色：结构体顶部写一句话用途，说明它代表什么业务对象；语言与写法服从 `comment-rules`。
- 持久化模型：字段注释只写用途，**不在代码里重复数据库 `COMMENT` 全文**。
- 接口请求 / 响应：只对语义不自明的字段补一句，不写“对应前端某字段”这类冗余说明。
- 内部临时结构：结构体一句用途即可，字段通常不写注释。
- 跨业务域共享实体与公共传输结构：必须写全用途，并为每个导出字段写用途。

## 四、禁止

- 把内部临时结构放进 `entity/` 或 `common/`。
- 同一业务模型在多处重复定义，应按最大引用面选唯一落点。
- 用 `data`、`info`、`types`、`models` 这类聚合名承载结构体。
- 为“未来可能复用”提前把临时结构提升为公共结构（属 `code-quality-rules` 主线 1 反对项）。

## 五、与相邻规则的边界

- 目录位置与版本化：`placement-catalog.yaml`、`project-layout-v2.md`。
- `entity/<v?>/` 内文件切分与 `req` / `resp` 命名：`entity-file-naming.md`。
- 各语言完整目录映射：`go-package-layout.md`、`java-layer-layout.md`、`node-python-module-layout.md`。
- 符号命名：`naming-rules`；注释语言与颗粒度：`comment-rules`。
- 函数参数结构：`code-quality-rules` 的 `function-signature-rules.md`。
