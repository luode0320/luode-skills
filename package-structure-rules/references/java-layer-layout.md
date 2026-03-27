# Java 分层样板

## 用途

用于 Java 项目中决定典型分层目录与依赖方向。

## 常见目录职责

- `controller`
  处理 HTTP 或 RPC 入口、参数绑定、响应返回。
- `service`
  承载业务流程、事务组织和核心业务规则。
- `repository` 或 `dao`
  承载持久化访问。
- `entity`
  承载持久化实体。
- `dto`
  承载请求响应对象、跨层传输对象。
- `config`
  承载框架配置、组件注册、环境配置。
- `exception`
  承载异常定义和异常映射。
- `mapper`
  承载 DTO 与实体、领域对象之间的映射逻辑。
- `util` 或 `utils`
  只放通用无状态小工具，不放业务流程。
- `constants`
  承载稳定常量和固定业务码值。

## 依赖方向

- `controller` -> `service`
- `service` -> `repository` / `dao`
- `repository` / `dao` -> `entity`
- `dto` 不应反向驱动整个业务层设计
- `config`、`exception`、`constants`、`util` 不应反向依赖 `controller`

## 特别提醒

- 不要把所有对象都塞进 `entity`，接口层对象应回到 `dto`。
- `service` 不要退化成纯转发层；如果只是转发，说明分层可能多余或职责未拆清。
- `util` 不承担领域语义明显的业务逻辑。
