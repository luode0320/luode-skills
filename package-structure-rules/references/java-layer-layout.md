# Java 分层样例

## 用途

用于 Java 项目中判断典型分层目录、公共支撑目录和依赖方向。

## 常见目录职责

- `controller`
  处理 HTTP 或 RPC 入口、参数绑定和响应返回。
- `service`
  承载业务流程、事务组织和核心业务规则。
- `repository` 或 `dao`
  承载持久化访问。
- `entity`
  承载持久化实体。
- `dto`
  承载请求响应对象和跨层传递对象。
- `config`
  承载框架配置、组件注册和环境装配。
- `exception`
  承载异常定义和异常映射。
- `mapper`
  承载 DTO 与实体之间的映射逻辑。
- `utils`
  只放通用、无状态、可复用的小工具。
- `constants`
  承载稳定常量和固定业务码值。
- `common`
  承载和当前项目有关、但可在多个模块复用的公共支撑代码。
- `global`
  承载已经初始化完成的共享实例或共享引用入口。
- `crontask`
  承载定时任务入口、任务注册和调度装配，不承载核心业务实现。

## 依赖方向

- `controller` -> `service`
- `service` -> `repository` / `dao`
- `repository` / `dao` -> `entity`
- `crontask` 可以依赖 `service` 或稳定公共支撑层完成任务编排，但不要把业务规则直接堆进定时任务入口层。
- `config`、`exception`、`constants`、`utils`、`common`、`global` 不应反向依赖 `controller`

## 特别提醒

- 不要把所有对象都塞进 `entity`，接口层对象应回到 `dto`。
- `service` 不要退化成纯转发层；如果只是转发，说明分层可能多余或职责未拆清。
- `utils` 不承载领域语义明显的业务逻辑。
- Java 不要机械照搬 Go 的目录规则。像根目录 `main.go`、`internal/`、以及根级 `global` / `middleware` / `crontask` 的硬约束，是 Go 包结构约定；Java 应优先遵循包名、模块边界和框架装配方式。
