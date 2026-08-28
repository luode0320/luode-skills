# Case study：调试用例与测试用例是两套资源（2026-08-24 gap 回补）

> 归属 owner：`apifox`。本案例记录一次**由错误论断导致的假通过**，以及五步取证如何定位 CLI 的真实能力边界。供下次遇到"CLI 说成功但客户端看不到"类问题时对照。

> **续篇（2026-08-26）**：本篇第五节结论「调试用例事后完全无法用 CLI 补」被**部分推翻**——原生格式 match-name 重导可批量更新 DEBUG_CASE 的 `preProcessors`。完整证据链见文末「八、续篇：DEBUG_CASE 处理器可经原生重导写入（2026-08-26）」。
>
> **续篇2（2026-08-26）**：接口节点本身的 `api.preProcessors` 也可经同一通道批量写入，但**接口层脚本会级联执行到所有下级用例**——豁免用例必须用「清除鉴权头」脚本抵消（`inheritPreProcessors` 落库但 CLI 引擎不读）。见文末「九、续篇2」。完整三层矩阵：接口层 66/66 + DEBUG_CASE 66/66 + TEST_CASE 72/72 全带脚本。

## 一、现象

EllipalFinance-go 项目为 5 个活动曝光管理接口（`/api/swap/v2/admin/activity/*`）建了 21 个 test-case，跑出 88 断言 0 失败，且按当时的参数完整性闸门取证：必填字段零缺失、T-1 格式化全通过。

用户随后截图：客户端「接口管理」里点开 `新增或编辑活动曝光配置` → 用例「成功」→ Body(JSON) **完全空白**，并问"是 apifox 的 skill 还不够完善吗"。

## 二、根因：skill 的论断与实测相反

本 skill `modules/test-case.md` 当时写着：

> 接口树里接口下方的"成功/失败"等子项 = 接口用例
> 不存在"把测试用例复制到调试用例"这个操作——接口用例本身即带完整参数的调试例子

agent 据此认为"建完 test-case 接口树下就有带参例子"，于是参数完整性闸门**只查了 `test-case` 一路**，得出全通过。而用户看到的是另一套资源。

**这是假通过的典型成因：验收口径覆盖不全，且 skill 明文背书了错误口径。**

## 三、五步取证（每步都推翻一个可能的解法）

| 步 | 验证 | 结果 |
|---|---|---|
| 1 | `test-case list --endpoint 505838489` 是否含那个「成功」 | ❌ 只返回 7 个自建用例，body 均 103~510 字节非空；「成功」不在列表 |
| 2 | `export --format apifox` 看它到底是什么 | 它在 `api.cases[0]`，`type=DEBUG_CASE`，`categoryId=0`，`requestBody.data=""` |
| 3 | `endpoint get` 能否读到 `cases` | ❌ 返回的 39 个顶层键里没有 `cases` |
| 4 | `endpoint-update` schema 是否接受 `cases` | ❌ schema 里既无 `cases` 也无 `DEBUG_CASE` |
| 5 | `endpoint update` 写 `requestBody.example` | ❌ 5/5 报 `success: true`，但回读 example 长度全为 0（假成功） |

结论：**CLI 完全写不到调试用例**，只能在 `import` 时经 example 灌入。

## 四、决定性实验：example 该放哪一层

前四步只证明了"写不进去"，没解决"怎么才能有"。于是导入一个**临时探针接口**（带 example，验完即删）：

```yaml
content:
  application/json:
    schema: {...}
    example:            # MediaType 层级
      activityId: probe_demo_001
      type: 1
```

探针的 `DEBUG_CASE` **自带 69 字节 body** → 证明 example 是唯一入口。

但第一次给正式接口补 example 时放进了 `schema.example`，删接口重导后验收 **0/5 仍为空**；改到 MediaType 层级重导，**5/5 生效**。

> **OpenAPI 里 `MediaType.example` 与 `Schema.example` 都合法，apifox 生成调试用例 body 时只认前者。** 这一条是本案例最容易踩且最难自查的点——放错位置不报错、不告警，只是静默没有。

## 五、修复代价（为什么要在导入前就写对）

已存在接口没有第三条路：

1. **删接口重导**：`endpoint delete` → 带 example `import` → 重绑 securityScheme → **重建全部测试用例**（endpointId 变，21 个 caseId 全部失效）→ 重跑回归。本次实际执行了**两轮**（第一轮因 example 放错层级白做）。
2. **用户客户端点「自动生成」**：零风险但需人工逐接口点击。

所以规则 T-3 把关口前移到"写 OpenAPI 时"，而不是"发现问题后再补"。

## 六、沉淀

- `modules/test-case.md`：重写「两类用例是两套资源」节（纠错）+ 新增规则 T-3 + 纠正 T-2 修复路径 + 不可违反规则第 5/6 条
- `modules/project-onboarding-checklist.md`：硬动作 A12
- `modules/api-sync-to-apifox.md`：不可违反规则第 10 条
- 净增约 62 行，其中约 12 行为替换原错误论断

## 七、可迁移的教训

1. **"CLI 报 success" 不等于落库**——本 skill 已知两个假成功字段（`endpoint update` 的 `requestBody.example`、`environment update` 的 `variables`），写完都必须回读确认。遇到新字段默认怀疑。
2. **一个概念对应几套资源，要先用 `export --format apifox` 看原生结构**，不要凭客户端 UI 的层级关系推断 CLI 资源模型。
3. **skill 里的论断也会错**——当实测与 skill 冲突时以实测为准，并回头修 skill（本 skill「CLI 事实优先」原则）。这次若不修，下个项目会原样再踩一遍。
4. **验收口径要覆盖交付物的全部可见面**：用户看的是客户端接口树，agent 查的是 CLI 列表，两者不重合就会出现"我说全绿、你说是空的"。

## 八、续篇：DEBUG_CASE 处理器可经原生重导写入（2026-08-26）

> 本篇第五节曾断言「调试用例事后完全无法用 CLI 补」。**该结论对 body（`requestBody.data`）仍成立，但对 preProcessors/postProcessors 已被推翻**。以下为完整证据链。

### 背景与现象

兑换项目（8735371）自动化测试用例（TEST_CASE）有鉴权前置脚本，但接口树下的调试用例（DEBUG_CASE）**66 个全部没有前置脚本**——用户用接口用例调试时鉴权无法通过。全量导出核验：`api.cases[]` 混合 66 DEBUG_CASE（categoryId=0，全部无 preProcessors）+ 72 TEST_CASE（仅 21 个带 AUTHV2 脚本）。

### 通道验证（沙盒，三步）

| 步 | 操作 | 结果 |
|---|---|---|
| 1 | 全量导出 → 改 1 个 DEBUG_CASE 的 `preProcessors` 为标记脚本 → match-name 重导 | 首轮 createCount=66（新项目导入）；二轮 **updateCount=66**（已存在接口走 update 语义） |
| 2 | 回读验证 `preProcessors` 是否落库 | `[{"type":"customScript","data":"console.log(\"SANDBOX_TEST_MARKER\");","defaultEnable":true,"enable":true}]` —— **真实落库** |
| 3 | 对比重导前后接口契约字段 | name/path/method/folderId/tags/securityScheme/requestBody/responses/parameters **全部 SAME**；唯一副作用 `ordering` 归零（仅显示排序） |

### 真实项目应用（一次导入完成双通道）

- 注入源：从现有 v2 TEST_CASE 提取 AUTHV2 签名脚本全文；v1 脚本按 `Authorization = md5(RequestURI + body原文 + authSecret)` 构造（v1 密钥对应 `x-api-key` 头选 H5/APP 密钥）
- 结果：**endpointCase updateCount=138**（66 DEBUG_CASE + 72 TEST_CASE 全命中，含 9 个刻意保持无脚本的用例——7 个「缺凭据」负向 + 2 个「错误/无签名」安全性用例，注入脚本会破坏其拒绝语义，必须豁免）
- 回读验证：DEBUG_CASE 66/66 带脚本（v1=58 authSecret、v2=8 v2ApiSecret，脚本类型零错误）；TEST_CASE 63/72 带脚本；接口契约字段回读与注入源一致
- 环境变量：v1 用例依赖 `authSecret`，经开放 API 代填写入开发环境（隔离档，密钥低敏），`environment update` 整体覆盖语义下 payload 需含全部既有变量（v2ApiSecret 等），写后回读核对

### 关键命令（可直接复用）

```bash
# 导出 → 注入脚本 → match-name 重导
apifox export --project <id> --format apifox --output export.json
apifox import --project <id> --format apifox --file inject.json --module-import-mode match-name
# 模块同名冲突时显式映射（目标有多个同名模块时必需）
apifox import --project <id> --format apifox --file inject.json --module-import-mode match-name --module-map "source:<源模块Id>=<目标模块Id>"
# 回读验证（必须，确认落库）
apifox export --project <id> --format apifox --output verify.json
```

### 可迁移要点

1. **原生格式 match-name 重导是"已存在接口批量改用例"的唯一自动化通道**：不删接口、不动 ID、不重建用例，契约字段全保留。副作用仅 `ordering` 归零。
2. **豁免清单必须显式维护**：负向「缺凭据」与安全性「错误签名」类用例**不能**注入签名脚本——脚本会生成合法签名导致用例失效。注入脚本时按用例名/断言语义人工判定豁免，不可无脑全量。
3. **脚本模板提取自真实用例**：优先从项目内已有同类用例提取脚本全文（含环境变量缺失时的 console.log 提示逻辑），不要从零手写。
4. **v1/v2 双签名并存**：同一项目可能 v1（`authSecret` + `x-api-key` 选密钥）+ v2（`v2ApiSecret`）双通道，注入脚本按接口 securityScheme 分发，脚本内密钥一律 `pm.environment.get()` 运行时取，禁止写死。
5. **假成功清单再扩一条**：`import` 的 updateCount 才是真实命中数——`updateCount=0` 只说明 match-name 没匹配上接口定义，但 **endpointCase 命中仍会把用例更新进去**，要看完整输出尾部而不是头部。

## 九、续篇2：接口节点本身的 preProcessors 也可批量写入，但会级联到用例（2026-08-26）

> 第八节补的是 `api.cases[]`（接口用例）层。用户随后发现**接口节点本身**（客户端「接口编辑 → 前置操作」页签）仍是空——直接调试接口（不选用例）时鉴权脚本不执行。本轮把接口层也补上，并踩出一个**必须知道的大坑：接口层脚本会级联执行到所有下级用例**。

### 现象

截图：接口编辑视图「前置操作(1)」页签无内容（空占位）；接口用例编辑视图「前置操作(1)」有内容（上轮已注入）。全量导出核验：66 个接口的 `api.preProcessors` 全部为 `[]`。

### 注入通道（与第八节同一通道，字段位置不同）

- 修改位置：`api.preProcessors`（接口节点字段，与 `api.cases[]` 平级，不在 cases 内）
- 脚本模板：与对应用例层完全一致（v1=58 用 `authSecret`、v2=8 用 `v2ApiSecret`）——两处共用同一模板。**`pm.request.headers.add` 对同名 key 是「追加」而非「覆盖」**：接口层脚本先执行注入第一个同名头，用例层脚本后执行 add 会追加第二个同名头，而服务端 `c.GetHeader` 只取**第一个**——若两层算出的值不同（用例层 body 已就绪、接口层 body 未就绪时签名必然不同），最终生效的是接口层的旧值，验签失败。**因此用例层签名脚本必须「先 remove 再 add」完全接管请求头**（见下方修复段）
- 重导：`endpointCase updateCount=138` 同一次命中；回读 66/66 接口层脚本落库

### ⚠️ 关键副作用：接口层脚本被所有下级用例级联执行

Apifox 继承机制：**用例默认继承接口的前后置操作**（官方文档：「单个接口/接口用例默认继承父级的前/后置操作，可关闭继承」）。给接口层加脚本后：

- 正常用例（自带签名脚本）：接口层脚本先执行注入 → 用例层脚本后执行**接管**（脚本开头先 `headers.remove` 再 `headers.add`，保证请求头唯一且按用例层语义）→ 无影响，PASS。**注意：若不先 remove，headers.add 追加语义会让两个同名头共存、服务端取第一个，用例层签名被接口层旧值污染，表现为「验签失败」而非「追加成功」**
- **豁免用例（缺凭据负向/安全性，刻意无脚本）**：接口层脚本注入合法签名 → 请求带凭据 → 服务端放行 → 「应被拒」断言 FAIL

实测：注入接口层脚本后，全量回归从 72/72 跌到 **61/72**（9 个豁免用例全挂）。

### 修复：豁免用例加「清除鉴权头」脚本

给 9 个豁免 TEST_CASE 各加一个清除脚本（用例层 preProcessors）：

```js
// 豁免用例：清除接口层注入的鉴权头，保持「无凭据/错误凭据-应被拒」语义
var headers = pm.request.headers;
var names = ['x-api-key', 'X-Api-Key', 'authorization', 'Authorization'];
for (var i = names.length - 1; i >= 0; i--) {
    headers.remove(names[i]);
}
```

执行顺序：接口层脚本先注入 → 用例层脚本后清除 → 请求保持无凭据 → 服务端按预期拒绝。**实测 9/9 豁免用例恢复 PASS，全量回归回到 72/72。**

### ❌ 尝试过但不可行的方案：inheritPreProcessors

- `test-case update` 写 `inheritPreProcessors: {"enable": false}` → **落库成功**（test-case get 回读确认），但 **CLI 执行引擎不读该字段** → 用例仍被接口层脚本注入签名 → FAIL
- 结论：**CLI run 无法靠 inheritPreProcessors 关闭继承**；「清除脚本」是唯一可靠通道（客户端 UI 关闭继承另说，CLI 自动化必须用清除脚本）

### 三层最终矩阵（本次任务完成态）

| 层 | 覆盖 | 脚本 |
|---|---|---|
| 接口层 `api.preProcessors` | 66/66 | v1=58 authSecret、v2=8 v2ApiSecret（签名） |
| 接口用例 DEBUG_CASE | 66/66 | 同上（签名） |
| 自动化用例 TEST_CASE | 72/72 | 42 v1 签名 + 21 v2 签名 + **9 豁免清除脚本** |

任何一层单独调试（接口直发/用例直发）鉴权都能通过，豁免用例仍验证拒绝行为。

### 可迁移要点（增量）

1. **接口层与用例层共用同通道、同模板**：match-name 重导同时写 `api.preProcessors` 与 `cases[].preProcessors`，一次导入全部生效。
2. **给接口层加脚本 = 给所有无脚本用例加脚本**：必须同步检查豁免用例，否则负向/安全性用例被级联注入破坏。豁免清单要在「用例层注入」和「接口层注入」两个动作里各过一遍。
3. **`inheritPreProcessors` 落库不等于生效**：CLI run 引擎不读它，自动化场景用「清除脚本」抵消继承，别浪费时间调这个字段。
4. **`pm.request.headers.add` 对同名 key 是追加（不是覆盖），服务端 `c.GetHeader` 取第一个头**：接口层与用例层脚本共存时，用例层脚本**必须先 `headers.remove` 再 `add`** 才能完全接管请求头——只 add 会把第二个同名头追加在后面，服务端读到的仍是接口层的旧值。这个「先清除再注入」接管前缀是签名脚本的强制组成部分，不是可选项。实测证据：63 个签名脚本插入接管前缀后，负向用例 407432230（正确身份但签名错误-应被拒）从 FAIL 恢复 PASS；豁免用例的清除脚本同理（remove 保证无凭据语义）。
5. **fixture 重跑会让环境变量里的签名密钥漂移（2026-08-26 新增坑）**：`partner_fixture.py` 每次运行都用 `secrets.token_hex(32)` 重新生成合作方 `api_secret`，`api_key = sha256(api_secret)` 同步轮换——**环境变量 `v2ApiSecret`/`v2ApiKey` 不会跟着变**。症状极具迷惑性：鉴权通过（身份合法）、但按订单归属校验的接口（如 /status 查单）返回 `order not found`，因为用例身份（旧 key）≠ 订单归属（新 key）。修复：重跑 fixture 后必须重写环境变量（`environment update` 整体覆盖，payload 需带全量 3 变量 `v2ApiSecret`/`v2ApiKey`/`authSecret`）。判定方法：手动用库里当前 `test_partner_a` 凭据请求成功、而用例失败 → 就是环境变量漂移。
