# 测试数据构造规则

本文件定义 `project-release-test-rules` 在准备接口测试请求参数时，如何从可复用参数、上游接口、local 数据库 / 缓存、OpenAPI 示例、fixture 和明确规则中构造可追踪参数，避免用不存在的数据测试并接受失败为"符合预期"。

## 核心原则

- **真实可追踪优先**：测试参数必须优先来自已验证可复用样本、上游接口返回或 local 真实数据，确保请求的数据在业务中真实存在或有明确来源。
- **正常路径优先**：必须先用真实数据验证接口的正常（成功）响应，再验证异常路径。
- **禁止伪通过**：不得用不存在的数据测试查询接口，然后接受"record not found"或"空列表"为通过判定。

## 通用参数来源优先级（强制）

从高到低如下，必须按优先级依次尝试。任何必填参数无法直接确定时，不得直接手写猜测值。

1. **可复用参数**：先读取 `doc/5-tests/基线/reusable-params.yaml` 中状态为 `reusable` 且未过期的样本；P0 / P1、写接口和状态敏感接口必须先轻量复验。
2. **上游接口返回数据**：按 `dependency-graph.yaml` 与 `parameter-sources.yaml` 先调用 provider 接口，再通过 `response_path`、`selector`、`extract` 提取参数。
3. **数据库最近记录**：查询接口对应的 local 数据库表，按时间倒序取最近 5-10 条记录，从记录中提取请求参数字段。
4. **本地缓存数据**：从 local Redis / cache 中按已知 key 或扫描出的 key 读取候选值。
5. **OpenAPI 示例**：读取 `swag/` 中请求示例、example、schema default 或枚举值，只作为参数形状、字段格式和候选值参考。
6. **fixture 样本**：使用项目已维护的 fixture、mock 数据或测试样本文件。
7. **明确业务规则生成**：仅当规则已在接口基线或文档中明确时，按规则生成合理参数。
8. **不存在的测试数据**：仅用于验证接口错误处理和边界条件，不能作为通过判定的主依据。

## 参数解析协议（强制）

每个参数都必须产出可追溯来源，写入当轮 `artifacts/dependency-trace.json` 或 `artifacts/dependency-trace/<接口标识>.json`：

1. 先定位目标接口在 `interface-inventory.yaml` 中的 `参数来源`、`依赖接口` 和 `依赖失败策略`。
2. 对每个必填参数按 `parameter-sources.yaml` 的 `priority` 顺序解析。
3. 使用 `reusable_param` 时，必须检查 `status`、`ttl`、`last_verified_at`、`fail_count` 和脱敏/引用信息。
4. 使用 `upstream_api` 时，必须先执行 provider，保存 provider 请求和响应，再按提取规则选择候选值。
5. 使用 `local_database` 或 `local_cache` 时，只能连接 local 配置，不得读取 test / prod / staging。
6. 使用 `openapi_example` 时，必须记录来源 YAML 文件、operationId 和字段路径；P0 / P1、写接口和状态敏感接口仍必须用真实数据或轻量复验确认可用，不能只靠示例给 PASS。
7. 参数解析成功后，记录来源类型、来源接口或来源表、OpenAPI 文件、响应文件、提取路径、选择规则、脱敏值和真实值引用。
8. 参数解析失败时，记录失败阶段和失败类型；不得继续用空值或猜测值执行目标接口。

## 可复用参数持续更新（强制）

- 复验成功：更新 `last_verified_at`、`success_count`、`last_success_interface`，状态保持或提升为 `reusable`。
- 复验失败：更新 `fail_count`、`last_failed_at`、`failed_interface`、`failure_type`、`invalidation_reason`，并将状态转为 `stale`、`invalid` 或 `quarantined`。
- schema、请求字段、响应字段、鉴权或业务成功判定漂移：相关参数样本先转为 `stale`，本轮不得直接信任。
- 新解析且跑通的参数：先以 `candidate` 写入，至少记录来源证据；达到项目复验阈值后再升级为 `reusable`。
- 禁止保存明文 token、密码、手机号、身份证号、银行卡号、密钥和非 local 连接串。

## 数据源识别规则

通过项目自身的代码和配置识别数据源，不假定目录、业务实体或数据库类型：

1. 从 repository/DAO/ORM 查询、迁移脚本和实体模型中定位表、集合或 topic。
2. 从 local 配置解析数据库、缓存和消息系统连接引用，并记录配置文件路径与字段名。
3. 由 adapter 将数据源映射为 `source_type`、`source_ref`、`query`、`selector` 和脱敏证据。
4. 无法确认数据源时输出 `PARAM_UNRESOLVED`，不得使用项目外的默认表名或猜测字段。

## 查询规则

### MySQL 查询

- 只能使用本地 `local` 配置中的数据库连接（从 `global/config/config_local*`、`.env.local` 或等价本地配置获取地址、用户名、密码、库名）。
- 通过命令行 `mysql -h <host> -P <port> -u <user> -p<password> <dbname> -e "SQL"` 或 Python 脚本查询。
- 查询最近记录示例：`SELECT * FROM <table> ORDER BY <time_column> DESC LIMIT 5`
- 从记录中提取请求参数字段，如 `from_cType`、`from_shortName`、`to_cType`、`to_shortName`、`fromAddress`、`toAddress`、`fromAmount` 等。

### MongoDB 查询

- 使用 `mongosh` 或 Python pymongo 查询。
- 查询最近记录示例：`db.<collection>.find().sort({createdAt: -1}).limit(5)`

### Redis 查询

- 部分接口依赖 Redis 缓存数据（如币种列表、币价），可通过 `redis-cli` 查询对应 key。
- 缓存 key 格式参考 `PROJECT_MEMORY.md` 中的缓存键映射。

## 按接口类型的数据构造策略

### 查询、写入与事件入口

- 查询入口必须先从 provider、local 数据源或 fixture 得到真实存在的资源标识，再验证正常响应；空结果只能在契约明确允许时通过。
- 写入入口必须依据接口的 `side_effects`、`cleanup` 和风险等级执行；允许正常业务 DELETE/DML，但禁止破坏性数据库或基础设施操作。
- 事件、定时任务、消息消费者必须先准备与消息 schema 匹配的 local fixture，并验证 ack、重试、幂等和死信策略。
- 协议适配器必须把业务专属字段映射写入项目基线或 adapter 配置，不得修改本通用规则文件。

## 禁止行为

1. 禁止用不存在的资源标识验证正常路径并接受业务“未找到”为通过。
2. 禁止跳过写入口或消息入口的真实 local 调用；静态审查不能替代运行证据。
3. 禁止把 OpenAPI 示例值当成真实业务数据直接判定通过。
4. 禁止把环境阻断、参数未解析或适配器未知误报为接口失败或通过。

## 网络与代理配置检查

接口测试中如果出现外部服务连接超时、连接拒绝或无响应，必须先检查 local 启动配置中是否需要代理。

### 代理配置位置

- 查看项目的本地配置文件（如 Go 项目的 `global/config/config_local*`、`.env.local`）中的 `httpConfig` 段。
- 配置示例（字段名仅作适配器输入，不是通用默认值）：

```yaml
httpConfig:
    proxy: http://<local-proxy-host>:<port>
```

- 代理配置为空或被注释掉时，依赖外部服务的入口可能无法访问，导致超时或失败。
- 代理配置启用时，确保代理地址可达（先 `curl -x http://192.168.2.20:7897 https://httpbin.org/ip` 验证）。

### 什么时候检查代理

1. 接口返回外部服务超时或连接拒绝。
2. 接口在生产环境正常但测试环境失败，且两个环境网络策略不同。
3. 服务启动后初始化阶段出现大量外部连接失败日志。
4. 多个接口同时报网络相关错误，但本地数据库连接正常。

### 检查步骤

1. 读取当前 local 配置中由 adapter 声明的代理字段。
2. 若代理被注释或为空，评估该 local 依赖是否需要代理访问外部服务。
3. 若需要代理，只能调整本地 `local` 配置并重启本地服务后重测；不得改动 `test` 环境配置来完成本地自动化测试。
4. 若代理地址本身不可达，标记为环境问题，不得判定为接口代码缺陷。

### 禁止行为

- 看到外部服务超时就直接判定接口不通过，不检查代理配置。
- 明明是代理未配置导致的网络问题，却判定为代码 bug 或接口逻辑错误。
- 代理配置存在但未验证代理可达性，直接重启服务后测试。
- 为了让本地自动化测试跑通，去修改 `config_test*` 或改用 `test` 环境数据库 / 服务。

## 例外条件

- 数据库完全无数据且无法插入测试数据时，可以记录"数据库无可用测试数据"并标记为待确认，但不能直接判定为通过。
- 接口依赖的外部服务不可用时，可以记录为环境问题，但不能跳过接口测试；结论必须为 `BLOCKED` 或 `PENDING`。

## 写入入口样本矩阵（强制）

- 每个写入入口至少准备 `historical_valid`、`historical_rejected`、`current_valid`、`boundary` 四类样本；项目基线可声明不同类别，但必须给出来源和理由。
- P0 默认每类不少于 3 条、总数不少于 10 条；P1 可按风险降级，P2 记录最小代表样本。
- 每条样本记录来源引用、状态、幂等键、清理策略和是否产生外部副作用；重复参数组合只计一次。
- 允许的业务拒绝必须由项目基线声明；没有声明时统一为 `PENDING`，不得猜测为 `EXPECTED_FAIL`。
