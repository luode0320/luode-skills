# 接口测试报告输出格式

本文件定义测试报告的标准化输出格式，**强制要求接口测试明细不得使用 Markdown 表格，必须使用块状格式**，请求参数和简要响应必须是格式化的 JSON 字符串。

## 报告整体结构

测试报告分为四部分：

1. 测试概览（主 `README.md` 中展示）
2. 基线扫描、双索引同步与对账摘要（主 `README.md` 中展示）
3. 接口测试明细（ASCII 镜像目录的 `interface-test-results.md` 中展示）
4. 门禁结论（主 `README.md` 中展示）

---

## 第一部分：测试概览格式（主 README.md）

```text
# 上线前项目接口测试报告

## 基本信息
- 测试时间：YYYY-MM-DD HH:MM:SS
- 测试范围：本次上线改动模块
- 测试环境：local 本地环境
- 接口总数：N
- 必测接口数：N
- 通过接口数：N
- 不通过接口数：N
- 待确认接口数：N
- 跳过接口数：N

## 风险等级统计
- P0 级接口：总数 N，通过 N，不通过 N，待确认 N，跳过 N
- P1 级接口：总数 N，通过 N，不通过 N，待确认 N，跳过 N
- P2 级接口：总数 N，通过 N，不通过 N，待确认 N，跳过 N
```

---

## 第二部分：基线扫描与对账摘要（主 README.md）

```text
## 接口基线扫描摘要
- 扫描模式：全量建基线 / 增量扫描
- 扫描时间：YYYY-MM-DD HH:MM:SS
- 扫描来源：route、controller、swagger、test、doc
- 新增接口数：N
- 删除接口数：N
- 变更接口数：N
- 待确认接口数：N

## 对账结果
1. 新增接口：POST /api/order/create，来源 backend/router/order.go:42
2. 变更接口：GET /api/order/detail/{id}，变更项：鉴权要求、响应结构摘要
3. 待确认接口：POST /api/pay，待确认项：业务成功判定

## 接口契约双索引同步摘要
- 当前代码扫描接口数：N
- swag manifest 接口数：N
- interface inventory 接口数：N
- 缺失 manifest：是 / 否
- 缺失 inventory：是 / 否
- 是否需要双刷新：是 / 否
- schema 漂移接口数：N
- 受影响可复用参数数：N
- 同步报告：ascii-artifacts/interface-sync-report.yaml
```

---

## 第三部分：接口测试明细格式（强制，不得使用 Markdown 表格）

每个接口独立一个块，字段顺序固定，格式如下：

```text
【接口 1】
接口            POST /api/order/create
接口名称        创建订单
接口标识        order_create_POST
请求参数        {"userId":"***","amount":"100","currency":"USDT","remark":"测试订单"}
参数来源        reusable_param:order_create_candidate_20260702
依赖追踪        artifacts/dependency-trace/order_create_POST.json
简要响应        {"httpStatus":200,"code":0,"message":"success","data":{"orderId":"ord_123456***","status":"pending","amount":"100"}}
Agent 判定      通过
阻断分类        无
判定理由        HTTP 状态码 200，业务 code=0，返回有效 orderId，订单状态为 pending，符合创建订单预期
风险等级        P0
发现来源        route,swagger
是否阻断上线    否

【接口 2】
接口            GET /api/order/detail/{id}
接口名称        查询订单详情
接口标识        order_detail_GET
请求参数        {"id":"ord_123456***","Authorization":"***"}
参数来源        upstream_api:order_create_POST -> $.data.orderId
依赖追踪        artifacts/dependency-trace/order_detail_GET.json
简要响应        {"httpStatus":200,"code":0,"data":{"orderId":"ord_123456***","status":"pending","amount":"100","userId":"***"}}
Agent 判定      通过
阻断分类        无
判定理由        HTTP 状态码 200，业务 code=0，返回订单信息和创建接口一致，符合预期
风险等级        P0
发现来源        controller,test
是否阻断上线    否
```

### 接口明细格式强制规则

1. 每个接口必须以 `【接口 N】` 开头，`N` 为数字，从 1 开始递增。
2. 字段顺序固定：接口、接口名称、接口标识、请求参数、参数来源、依赖追踪、简要响应、Agent 判定、阻断分类、判定理由、风险等级、发现来源、是否阻断上线。
3. 请求参数和简要响应必须是合法的 JSON 字符串，可包含必要的转义和脱敏。
4. Agent 判定只能是 `通过`、`不通过`、`待确认` 三种值；写接口可使用 `PASS`、`EXPECTED_FAIL`、`UNEXPECTED_FAIL`、`PENDING`。
5. 阻断分类只能是 `无`、`BLOCKED_BY_DEPENDENCY`、`PARAM_UNRESOLVED`、`ENV_BLOCKED`、`BASELINE_STALE`。
6. 是否阻断上线只能是 `是` 或 `否`。
7. 禁止使用任何形式的 Markdown 表格、HTML 表格输出接口明细。
8. 禁止合并多个接口到同一个块中，每个接口独立成块。
9. 超过 3 个字段的 JSON 可以适当换行，保持可读性。
10. 依赖追踪必须指向真实落盘文件；没有依赖时写 `无`。

### 简要响应内容强制规则

`简要响应` 用于让人工快速识别接口实际返回了什么业务内容，不能退化成只展示判定结果的占位 JSON。

1. `简要响应` 必须是合法 JSON 字符串，且必须包含 `httpCode` 或 `httpStatus`、业务状态字段（如 `status` / `code`）、`msg` 或等价消息字段，以及一段裁剪后的业务响应内容。
2. 禁止只输出无业务信息的占位响应，例如：
   - `{"httpCode":200,"verdict":"PASS"}`
   - `{"status":true}`
   - `{"code":0}`
3. 成功响应必须展示部分正常业务数据：
   - 如果 `data` 是对象，保留 3-8 个由接口 schema 标记为关键的字段，例如资源标识、状态、数量、时间、分页和计数等。
   - 如果 `data` 是数组，保留 `count` 和前 1-3 条脱敏样本；样本只保留关键字段，禁止整段大数组塞入报告。
   - 如果 `data` 是字符串、数字或布尔值，直接展示 `data` 值。
4. 失败或待确认响应必须展示 `httpCode` / 业务状态字段 / `msg` / `errorType`（如有）/ 错误摘要；错误摘要保留能判断原因的关键片段。
5. `简要响应` 必须脱敏：地址、订单号、txHash、userId、token、手机号、身份证号、银行卡号、密钥等字段只保留前后少量字符或用 `***` 代替。
6. `简要响应` 建议控制在 300-800 字符；超过长度时按字段优先级裁剪，但裁剪后仍必须是合法 JSON，不能用 `...` 破坏 JSON 结构。
7. 完整响应必须继续落盘到 `artifacts/raw-response/`；`简要响应` 只放足够人工识别接口行为的摘要内容。
8. 报告生成脚本必须从完整响应中构造 `dataPreview` 或等价字段，优先包含业务主键、状态、数量、列表前几条样本；不得直接用 `verdict` 替代响应内容。

---

## 第四部分：门禁结论（主 README.md 中展示）

```text
## 最终门禁结论
### 结论等级：PASS / FAIL / PARTIAL

#### PASS（允许上线）
所有必测 P0 接口全部通过，无阻断级问题，允许上线。

#### FAIL（阻断上线）
存在任一 P0 接口不通过/待确认/跳过，或者存在多个 P1 接口不通过，阻断上线，修复后重测。

#### PARTIAL（风险上线/需要人工确认）
无 P0 接口不通过，但存在 P1 接口不通过或待确认，或者存在 P2 级大面积失败，需要人工评估风险后决定是否上线，必须明确说明风险和影响范围。

### 阻断项列表
1. 接口 POST /api/order/create P0，不通过，原因：返回 code=500，内部错误
2. 接口 POST /api/pay P0，待确认，原因：业务返回码 1001 含义未知

### 风险项列表
1. 10 个 P2 接口查询超时，不影响核心流程，可后续修复
```

## 格式校验规则

报告必须满足以下所有要求才视为合格：

1. 接口明细未使用 Markdown 表格。
2. 所有请求参数和简要响应都是合法 JSON 字符串。
3. Agent 判定只有三种合法值。
4. 所有 P0 接口都有测试结果，无遗漏。
5. 门禁结论明确，理由充分。
6. 所有接口的判定理由都明确具体，无模糊描述。
7. README 中必须包含基线扫描、双索引同步与对账摘要，不能只保留测试结果。
8. 每个依赖接口或参数解析失败必须有阻断分类，不能混入目标接口“不通过”。

## 参数复用与失效摘要（主 README.md）

每次上线测试主 README 必须包含参数基线变更摘要：

```text
## 参数复用与失效摘要
- 本轮复用参数数：N
- 复验成功参数数：N
- 新增 candidate 参数数：N
- 标记 stale 参数数：N
- 标记 invalid 参数数：N
- 标记 quarantined 参数数：N
- 主要失效类型：expired / schema_changed / state_changed / ...
```

## 写接口样本分布块（强制）

> 本节定义写接口（createTransaction、createOrder、cancelOrder、refund 等）明细报告必须附带的"写接口样本分布"块格式。`test-data-construction-rules.md` 中规定 4 类样本必须全部出现，本节定义其呈现格式。

### 一、什么时候必须带写接口样本分布块

- 任何写接口的接口明细块中，`Agent 判定` 字段如果是 `PASS` / `EXPECTED_FAIL` / `UNEXPECTED_FAIL` / `PENDING` 四类之一，必须紧随其后附带「写接口样本分布」块。
- 缺少"写接口样本分布"块的上线测试报告，视为报告不合格，需要补齐后重新提交。
- 读接口（getHistory、getRateAndRange 等）的明细块不需要附带本块。

### 二、块格式（强制，不得使用 Markdown 表格）

接口明细块中紧跟 `判定理由` 字段后插入以下块（顺序与字段名固定）：

```text
【写接口样本分布】
接口标识        order_create_POST
样本总数        N
PASS 数量       N1
EXPECTED_FAIL   N2（其中 手续费不足 K1 / 维护中 K2 / 黑名单 K3 / 超范围 K4 / 上游业务级拒绝 K5）
UNEXPECTED_FAIL N3
PENDING         N4
样本来源分布
  historical_succeeded         数量 / 占比
  historical_failed_lifecycle  数量 / 占比
  historical_inflight         数量 / 占比
  current_listing_available    数量 / 占比
通道/链/币种分布
  <通道A>   数量
  <通道B>   数量
  ...
矩阵完整性     完整 / 缺失 <类别>
```

### 三、字段说明

- `样本总数`：所有 4 类样本加起来的条数，必须 ≥10。
- `EXPECTED_FAIL` 行的 `K1..K5` 是子分类计数，5 个子分类对应 5 类业务允许失败（手续费不足 / 维护中 / 黑名单 / 超范围 / 上游业务级拒绝）。
- `样本来源分布` 必须显式标注 4 类样本各自的数量与占比，缺一类记为 0。
- `通道/链/币种分布` 至少列出实际命中的通道；少于 2 个通道时必须显式标注"覆盖度不足"。
- `矩阵完整性` 字段值必须是 `完整` 或 `缺失 <类别>`，缺失类别只能是 4 类样本之一。

### 四、判定理由补充

- 写接口的 `判定理由` 字段必须显式说明 EXPECTED_FAIL 命中的是哪个子分类。
- 4 类样本缺失时，`判定理由` 字段必须说明缺失原因（数据库无数据 / 列表接口不可用 / 上游业务变化 / 其他）。
- `矩阵完整性` 与 `判定理由` 必须保持一致；不一致视为报告伪造。
