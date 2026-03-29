# Node / Python 模块样例

## 用途

用于 Node.js 和 Python 项目中判断 `router`、`controller`、`service`、`repository`、`model`、`utils`、`common`、`global`、`middleware`、`crontask` 等目录的职责边界和依赖方向。

## 常见目录职责

- `router`
  处理路由声明和入口绑定。默认优先使用 `router`；如果框架或项目已经稳定使用 `routes`，沿用现有基线，不要混用两套命名。
- `controller`
  处理请求输入输出、参数转换和响应组织。默认优先使用 `controller`；如果项目已经稳定使用 `handlers`，沿用基线，不要局部改名。
- `service`
  承载业务流程和业务组合逻辑。
- `repository`
  承载数据库或存储访问。
- `model`
  承载核心数据结构、ORM 模型、校验模型或序列化模型。只有在框架已经稳定使用 `schema` / `schemas` 时，才沿用对应命名。
- `middleware`
  承载鉴权、日志、追踪、上下文注入等横切逻辑。根目录默认作为命名空间，具体实现放 `middleware/<name>/`。
- `config`
  承载配置读取、环境装配和设置定义。
- `constants`
  承载稳定常量、状态码和配置键。
- `utils`
  承载无状态、跨模块复用的小工具。根目录默认作为命名空间，具体实现放 `utils/<name>/`。
- `common`
  承载和当前项目有关、但可在多个模块之间复用的公共支撑代码。根目录默认作为命名空间，具体实现放 `common/<name>/`。
- `global`
  承载已经初始化完成的共享实例或共享引用入口。根目录默认作为命名空间，具体实现放 `global/<name>/`。
- `crontask`
  承载定时任务入口、任务注册、调度装配和触发逻辑，不承载核心业务实现。

## 依赖方向

- 默认依赖方向为 `router` -> `controller` -> `service` -> `repository`。
- `model` 可以根据框架职责被入口层和数据层共享，但不要演变成万能目录。
- `middleware` 只做横切处理，不承载完整业务流程。
- `crontask` 可以依赖 `service` 或稳定公共支撑层完成任务编排，但不要把业务规则直接堆进定时任务入口层。
- `utils`、`common`、`global`、`config`、`constants` 不应反向依赖具体业务目录。

## 特别提醒

- 同一项目中不要同时混用多套近义命名，如一部分叫 `router`，另一部分叫 `routes`；一部分叫 `controller`，另一部分叫 `handlers`。
- 如果框架或团队已有稳定的复数命名基线，可以继续沿用，但不要半路切换成另一套。
- `utils`、`common`、`global`、`middleware` 根目录默认只放子目录，不直接堆实现文件（例如优先 `utils/time/format.py`、`middleware/auth/index.ts`）。
- Node / Python 不要机械照搬 Go 的根级私有层约束。像 `internal/`、根级 `global` / `middleware` / `crontask` 以及“禁止 `internal/middleware`”这类规则，只有项目本身已经明确采用同类私有层基线时才适用。
- Python 模块文件不要因为临时方便而散落在根目录，优先归入职责清晰的目录。
