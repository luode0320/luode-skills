# 测试数据构造规则

本文件定义 `project-release-test-rules` 在准备接口测试请求参数时，如何从本地数据库获取真实数据构造合理的请求参数，避免用不存在的数据测试并接受失败为"符合预期"。

## 核心原则

- **真实数据优先**：测试参数必须优先从数据库最近记录构造，确保请求的数据在业务中真实存在。
- **正常路径优先**：必须先用真实数据验证接口的正常（成功）响应，再验证异常路径。
- **禁止伪通过**：不得用不存在的数据测试查询接口，然后接受"record not found"或"空列表"为通过判定。

## 数据来源优先级

从高到低如下，必须按优先级依次尝试：

1. **数据库最近记录**：查询接口对应的数据库表，按时间倒序取最近 5-10 条记录，从记录中提取请求参数字段。
2. **接口列表返回数据**：先调用列表类接口（如 getFromPairList、getToPairList、getMainPairList）获取可用数据，再用于构造后续接口的请求参数。
3. **手动构造合理参数**：当数据库和列表接口均无法获取时，根据接口文档和业务规则手动构造合理参数。
4. **不存在的测试数据**：仅用于验证接口的错误处理和边界条件，不能作为通过判定的主依据。

## 数据库表识别规则

通过以下途径识别接口对应的数据库表：

1. **repository 层代码**：查看 `app/exchange/repository/` 下与接口同名的 Repo 文件，确认对应的 model 和表名。
2. **entity model**：查看 `app/exchange/repository/model/` 下的 struct 定义，确认 `TableName()` 方法或 GORM 默认表名。
3. **SQL 脚本**：查看 `scripts/` 下的建表脚本，确认表名和字段。
4. **MongoDB 集合**：查看 `app/exchange/entities/mongo/` 下的 struct 定义和 `constant/mongo.go` 中的集合名常量。

## 查询规则

### MySQL 查询

- 使用测试环境配置的数据库连接（从 `global/config/config_<env>_yaml.go` 获取地址、用户名、密码、库名）。
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

### 查询类接口（getHistory、getExchangeOrderStatus 等）

- 查询对应的 `orderUser` 表，取最近 5 条订单记录。
- 从记录中提取 `orderID`、`address`、`business`、`business_direction` 等字段构造请求参数。
- 必须用真实存在的订单ID或地址测试，验证正常返回数据。

### 报价类接口（getRateAndRange、getRange 等）

- 先调用 `getFromPairList` 获取可用兑出币种列表。
- 用第一个兑出币种调用 `getToPairList` 获取可用兑入币种列表。
- 用第一对可用币对构造报价请求参数。
- 如果某币对返回"维护中"，换用其他可用币对，不直接判定为失败。

### 写入类接口（createTransaction 等）

- 查询 `orderUser` 表最近成功的订单记录，获取有效的 `from`/`to` 币种、`fromAddress`/`toAddress`、`fromAmount`。
- 用真实参数组合构造下单请求，验证订单创建成功。
- 测试后必须清理创建的测试订单（删除或标记为测试数据）。
- 如果下单会触发真实交易，需使用低价值测试币对并评估风险。

### 风控类接口（checkIsBlacklisted 等）

- 查询 `orderUser` 表取真实的 `fromAddress` 和 `toAddress`。
- 用真实地址测试正常路径（应返回安全）。
- 再用明显无效地址（如零地址）测试异常路径（应返回风险）。

## 禁止行为

1. **禁止用不存在的订单ID测试查询接口并接受"record not found"为通过**：必须用真实订单ID验证正常返回。
2. **禁止用零地址测试风控接口并接受"风险地址"为通过**：必须用真实地址验证正常路径（安全）。
3. **禁止用不存在的币对测试报价接口并接受"不支持"为通过**：必须用可用币对验证正常报价。
4. **禁止跳过写入接口的实际调用**：写入接口（如 createTransaction）必须用真实参数执行实际调用，不能仅做代码审查就判定为通过。
5. **禁止用空列表作为查询接口的唯一测试结果**：如果列表为空，必须检查数据库是否有数据，有数据则用真实数据重测。

## 网络与代理配置检查

接口测试中如果出现外部服务连接超时、连接拒绝或无响应，必须先检查本地启动配置中是否需要代理。

### 代理配置位置

- 查看项目的环境配置文件（如 Go 项目的 `global/config/config_<env>_yaml.go`）中的 `httpConfig` 段。
- 配置示例：

```yaml
httpConfig:
    proxy: http://192.168.2.20:7897
```

- 代理配置为空或被注释掉时，部分依赖外网的服务（如第三方交易所 API、外部风控接口、币价数据源）可能无法访问，导致接口超时或失败。
- 代理配置启用时，确保代理地址可达（先 `curl -x http://192.168.2.20:7897 https://httpbin.org/ip` 验证）。

### 什么时候检查代理

1. 接口返回外部服务超时错误（如 Polaris timeout、第三方 API connection refused）。
2. 接口在生产环境正常但测试环境失败，且两个环境网络策略不同。
3. 服务启动后初始化阶段出现大量外部连接失败日志。
4. 多个接口同时报网络相关错误，但本地数据库连接正常。

### 检查步骤

1. 读取当前环境配置中的 `httpConfig.proxy` 字段。
2. 若代理被注释或为空，评估该环境是否需要代理访问外网服务。
3. 若需要代理，取消注释并填入可用代理地址，重启服务后重测。
4. 若代理地址本身不可达，标记为环境问题，不得判定为接口代码缺陷。

### 禁止行为

- 看到外部服务超时就直接判定接口不通过，不检查代理配置。
- 明明是代理未配置导致的网络问题，却判定为代码 bug 或接口逻辑错误。
- 代理配置存在但未验证代理可达性，直接重启服务后测试。

## 例外条件

- 数据库完全无数据且无法插入测试数据时，可以记录"数据库无可用测试数据"并标记为待确认，但不能直接判定为通过。
- 接口依赖的外部服务（如 Polaris、第三方交易所 API）不可用时，可以记录为环境问题，但不能跳过接口测试。