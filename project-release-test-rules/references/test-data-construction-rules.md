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

## 数据库表识别规则

通过以下途径识别接口对应的数据库表：

1. **repository 层代码**：查看 `app/exchange/repository/` 下与接口同名的 Repo 文件，确认对应的 model 和表名。
2. **entity model**：查看 `app/exchange/repository/model/` 下的 struct 定义，确认 `TableName()` 方法或 GORM 默认表名。
3. **SQL 脚本**：查看 `scripts/` 下的建表脚本，确认表名和字段。
4. **MongoDB 集合**：查看 `app/exchange/entities/mongo/` 下的 struct 定义和 `constant/mongo.go` 中的集合名常量。

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
6. **禁止把 OpenAPI 示例值当成真实业务数据直接判定接口通过**：示例只证明字段形状，不证明业务状态有效。

## 网络与代理配置检查

接口测试中如果出现外部服务连接超时、连接拒绝或无响应，必须先检查本地启动配置中是否需要代理。

### 代理配置位置

- 查看项目的本地配置文件（如 Go 项目的 `global/config/config_local*`、`.env.local`）中的 `httpConfig` 段。
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
3. 若需要代理，只能调整本地 `local` 配置并重启本地服务后重测；不得改动 `test` 环境配置来完成本地自动化测试。
4. 若代理地址本身不可达，标记为环境问题，不得判定为接口代码缺陷。

### 禁止行为

- 看到外部服务超时就直接判定接口不通过，不检查代理配置。
- 明明是代理未配置导致的网络问题，却判定为代码 bug 或接口逻辑错误。
- 代理配置存在但未验证代理可达性，直接重启服务后测试。
- 为了让本地自动化测试跑通，去修改 `config_test*` 或改用 `test` 环境数据库 / 服务。

## 例外条件

- 数据库完全无数据且无法插入测试数据时，可以记录"数据库无可用测试数据"并标记为待确认，但不能直接判定为通过。
- 接口依赖的外部服务（如 Polaris、第三方交易所 API）不可用时，可以记录为环境问题，但不能跳过接口测试。

## 写接口样本分级与矩阵（强制）

> 本节是`写入类接口`（createTransaction、createOrder、cancelOrder、refund 等）样本构造的唯一真相源；其他章节里关于写接口的说明与本节冲突时，以本节为准。

### 一、为什么不能只用 `historical_succeeded`（强制）

- 历史成功订单的参数组合，在当前时点不一定仍可成功下单：链上手续费会变、币对会进入维护、上游服务限流、用户地址被风控。
- 只用 `status=4`（已完成）订单回放时，会出现 4 类业务级失败（手续费不足、维护中、黑名单、超范围）。这些失败**不应当成接口不通过**，但也**不应当成接口通过**——它们是「数据时点已过期」的预期失败。
- 写接口测试结论必须基于样本矩阵，而不是单一历史成功记录。任何一个写接口的明细报告里没有"写接口样本分布"块，结论直接判无效。

### 二、4 级样本分级（强制）

写接口测试样本按下列 4 级分别采集，缺一类就视为矩阵缺失：

1. `historical_succeeded`
   - 来源：`orderUser` 等业务表，筛选 `status` 等于业务终态成功（默认 `status=4` 完成；其他业务终态成功码按本业务基线确定）。
   - 用途：验证相同参数组合在历史时点走通整条链路。
   - 注意：这是必要项，不充分项。哪怕全部 10 条都成功，也不能因此宣告接口通过。

2. `historical_failed_lifecycle`
   - 来源：同表，筛选历史上进入失败生命周期、`status` 落在 51/52/61-65/70/71 等业务失败终态集合的订单（具体码集合以本业务基线为准）。
   - 用途：验证相同参数组合在历史时点触发的是业务允许的失败路径（不是 5xx、不是空 msg、不是堆栈）。
   - 注意：用于反向验证业务失败路径的稳定性和错误信息质量，不用于正向验证下单成功。

3. `historical_inflight`
   - 来源：同表，筛选 `status` 落在 1/2/22/50 等"在途"区间的订单。
   - 用途：捕获「曾经下单但当前仍未终态」的样本，验证接口对长生命周期订单的查询/回调/状态轮询兼容。
   - 注意：在途订单的链上/上游状态可能已变更，复用其入参时只能用于"曾经走通"的对照，不能作为新下单成功依据。

4. `current_listing_available`
   - 来源：调用 `getFromPairList` / `getToPairList` / `getMainPairList`（或本业务等价列表接口）当前时点返回的可用币对。
   - 用途：使用当前真实可用币对构造下单参数，验证接口对当前业务态的可用性。
   - 注意：列表接口本身若不可用，需先排查上游服务、代理配置、数据新鲜度，再决定是否继续。

### 三、矩阵要求（强制）

- 每一类样本**至少 N 条**（默认 N=5，N 不得低于 3）。
- 总样本数不得少于 10 条；样本必须覆盖**至少 2 个通道/链/币种**，避免单一通道假阳性。
- 样本数量、来源、通道分布、币种分布必须写入明细报告的「写接口样本分布」块。
- 同一参数组合（同一 `from_cType`+`to_cType`+`fromAddress`+`toAddress`+`fromAmount`）不得重复计为多条样本；重复使用视为 1 条。

### 四、判定分类（写接口专用）

针对写接口的判定，由 `agent-response-judgement.md` 的通用 3 类扩展为 4 类：

- `PASS`：HTTP 2xx 且业务码符合创建/修改类成功语义，资源/订单/记录创建成功，状态正确。
- `EXPECTED_FAIL`：HTTP 4xx 或业务失败码落在业务允许集合内，且错误信息明确属于以下任一类：
  - 矿工费/手续费预留不足（`insufficient fee` / `gas underpriced` / 等价错误信息）
  - 币对/币种维护中（`Token under maintenance` / `Pair suspended` / 等价错误信息）
  - 地址被风控/黑名单（`address blocked` / `blacklisted` / 等价错误信息）
  - 数量/限额/范围超限（`amount out of range` / `limit exceeded` / 等价错误信息）
  - 上游服务明确业务级拒绝（HTTP 4xx + 业务码在白名单内）
- `UNEXPECTED_FAIL`：5xx、空 msg、堆栈、字段缺失、状态不符、敏感信息泄露等真异常。
- `PENDING`：缺少判定依据，需要人工或下一轮测试补齐。

### 五、矩阵结论与门禁（与 `execution-gate.md` 联动）

- P0 写接口：4 类样本必须全部出现；缺失任一类视为矩阵缺失，不给出 PASS/FAIL 结论，直接判 `PENDING`，并报告缺失类别。
- P0 写接口：`EXPECTED_FAIL` 比例 ≥60% 且 `UNEXPECTED_FAIL=0` 时，可走 PARTIAL 结论。
- P0 写接口：连续 3 轮出现同一 `EXPECTED_FAIL` 类别占比 ≥80% 时，升级为人工阻断（`PENDING` + 阻断说明），不进入 PARTIAL。
- P1 写接口：4 类样本可降级为 2 类（`historical_succeeded` + `current_listing_available`），判定规则同上。

### 六、与既有规则的兼容

- 本节不取代 `test-data-construction-rules.md` 其他章节的"真实数据优先"原则，反而是它的强化版：写接口必须按矩阵多级采样，不能只采一类。
- 本节不取代 `agent-response-judgement.md` 通用判定，只在写接口场景中追加 `EXPECTED_FAIL` / `UNEXPECTED_FAIL` 两类。
- 本节不取代 `execution-gate.md` 的 P0/P1/P2 分级与 `PARTIAL` 既有条件，只在写接口场景下放宽 `EXPECTED_FAIL` 计入 PARTIAL 准入。
- 本节不取代 `test-strategy-rules` 和 `functional-validation-rules` 的"真实分布优先"思路，但要求写接口必须把这一思路落到具体矩阵。
