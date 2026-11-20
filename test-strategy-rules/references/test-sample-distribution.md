# 测试样本分布优先（强制）

> 本节是测试策略中"测什么、用什么样本测"的强制规则，是对上文"测试隔离红线"的补充。任何测试策略、测试大纲、测试摘要，都必须显式回答"测试样本分布"问题。

### 一、为什么必须是真实分布

- 读接口（getHistory、getRateAndRange 等）必须用真实数据验证正常返回，禁止仅用不存在的数据测试并接受失败为"符合预期"。
- 写接口（createTransaction、createOrder 等）必须用 4 级样本矩阵（`historical_succeeded` / `historical_failed_lifecycle` / `historical_inflight` / `current_listing_available`）验证，样本定义见本文件下文"三、写接口样本分布"，数据来源优先级与判定规则见 `apifox-cli__skillhub/modules/test-data-and-judgement.md`。
- 任何"用伪造数据测试 + 接受失败为符合预期"的策略，必须直接驳回。

### 二、读接口样本分布

- 必须从数据库最近 5-10 条记录中提取请求参数。
- 至少覆盖 2 个业务场景或 2 个查询维度。
- 数据库无数据时，必须先尝试插入测试数据（按本地 `local` 配置连接）；完全无法插入时记录为待确认，不得直接判定为通过。

### 三、写接口样本分布（4 级样本矩阵，独立内嵌）

> 原 `project-interface-release-execution-rules/references/test-data-construction-rules.md` 的数据来源优先级与响应判定规则已并入 `apifox-cli__skillhub/modules/test-data-and-judgement.md`；本节的 4 级样本定义保持不变。

- 写接口策略必须显式回答 4 类样本如何获取：
  - `historical_succeeded`：`orderUser` 等业务表中 `status=4`（或其他业务终态成功码）的最近 N 条。
  - `historical_failed_lifecycle`：业务表上 51/52/61-65/70/71 等业务失败终态集合的最近 N 条。
  - `historical_inflight`：业务表上 1/2/22/50 等在途区间的最近 N 条。
  - `current_listing_available`：`getFromPairList` / `getToPairList` / `getMainPairList` 当前可用币对。
- 每一类样本数 N 默认 5，不得低于 3；总样本数不得少于 10。
- 至少覆盖 2 个通道/链/币种。

### 四、与其他测试类型的关系

- 接口测试是验证"接口在真实分布下是否按预期工作"的主要手段，不能用单元测试或代码审查代替。
- 联调测试中遇到写接口时，同样适用 4 级样本矩阵。
- 回归测试中遇到写接口时，至少保证 `historical_succeeded` + `current_listing_available` 2 类样本。
