# 调试用例（接口用例）专项 — debug-case

> 归属 owner：`apifox`。本模块是**接口树下的调试用例（`api.cases[]`，`type=DEBUG_CASE`）的唯一权威**，覆盖它的覆盖度铁律、创建/维护/批量工具链、字段规范与失败排查。吸收来源：skill-absorption-rules 外部吸收通道（2026-09-01，源3 buer2233/ai-api-test-skill 方法论层），改写为通用形态、不绑定任何 agent。与 `modules/test-case.md` 的边界：后者负责**自动化测试用例（`apiTestCaseCollection`）** 的命令操作细节（categoryId、处理器、断言字段、T-1/T-2/T-3 规则）；本模块只负责**接口树下的调试用例（DEBUG_CASE）**，两者是两套资源，字段与操作路径不同，禁止混用。

## 何时加载

- 用户要求"调试用例""接口用例""接口树下用例""点开接口下面的成功/失败""DEBUG_CASE"
- 接口树下的用例 body 为空、点开只有空壳、没有请求示例（对照 `test-case.md` 规则 T-3）
- 需要给已存在接口批量补调试用例的请求示例或前后置脚本
- 排查接口用例调试失败（鉴权不过、body 空、脚本未执行）
- 与 `test-case.md` 的触发区分：涉及"自动化测试菜单 / `apiTestCaseCollection` / 处理器断言字段"→ 走 `test-case.md`；涉及"接口树下 DEBUG_CASE"→ 走本模块

## 与 test-case.md 的边界（强制）

| 维度 | 本模块（debug-case） | test-case.md |
|------|---------------------|--------------|
| 资源对象 | 接口树下调试用例 `api.cases[]`，`type=DEBUG_CASE`，`categoryId=0` | 自动化测试用例 `apiTestCaseCollection`，可归类正向/负向/边界/安全 |
| CLI 写入 | body（`requestBody.data`）不可经 CLI 直接写，仅 import 时经 MediaType 层级 example 生成；处理器可经 match-name 重导写入 | CLI 可 create/update/test-case 直接读写 |
| 典型症状 | 客户端接口树点开"成功" body 空白、只有空壳 | 自动化测试菜单里用例缺失/参数不全 |
| 关联参考 | `references/case-debug-case-vs-test-case.md`（第八/九节：批量通道 + ordering 归零副作用 + 豁免清单 + 接口层级联） | 规则 T-1/T-2/T-3、双重闸门 A7 |

## 引用 case study（必读）

本模块的字段事实与批量通道全部来自实测案例，改动前先读 `references/case-debug-case-vs-test-case.md`：

- **第八节（2026-08-26）**：DEBUG_CASE 处理器可经「导出 → 改 JSON → match-name 重导」批量写入；副作用仅 `ordering` 归零；豁免用例（缺凭据负向/错误签名安全性）不能注入签名脚本。
- **第九节（2026-08-26）**：接口节点 `api.preProcessors` 与用例层共用同一通道；接口层脚本会级联执行到所有下级用例，豁免用例必须用「清除鉴权头」脚本抵消；`inheritPreProcessors` 落库但 CLI 引擎不读。
- 第五节：`endpoint update` 写 `requestBody.example` 是假成功（回读长度 0）；example 唯一有效层级是 MediaType 层级（`content."application/json".example`），放错位置静默不生效。

## 覆盖度铁律（强制，最高优先级）

> 接口树下的调试用例（DEBUG_CASE）与自动化测试用例是**两套资源**，覆盖度要**分别**满足，不能拿自动化用例的覆盖顶替调试用例（反之亦然）。本铁律针对 DEBUG_CASE，自动化用例的覆盖度铁律（正/负/边界三类）见 `modules/test-case-generation.md` 规则 B。

### 铁律：每个有 body 接口 ≥ 1 非空 DEBUG_CASE

- **判定对象**：接口树下的调试用例 `api.cases[]` 且 `type=DEBUG_CASE`。用户/client 看到的是客户端接口树里接口下方的「成功 / 失败」等子项。
- **判定标准**：有 `requestBody` 的接口，其 DEBUG_CASE 的 `requestBody.data` 必须**非空**（≥ 1 个真实请求体，不能是 `""` 或空壳）。参考值：实测 `api.cases[0].requestBody.data=""` 即为空壳；带参例子实测 69 字节以上。
- **例外**：header-only 接口（schema 无必填 + 维度全在请求头）允许 `{}` 空 body——这是真实契约，不是空壳（与 `test-case.md` 的 header-only 例外同口径）。
- **不达标处理**：空壳 DEBUG_CASE 视为覆盖缺口，按下方「批量工具链」补齐后再验收；缺口不消不得宣称接口用例完成。
- **项目落地**：本铁律同步为 onboarding-checklist 硬动作 A13（节点 2「调试用例请求示例」家族，见 `modules/project-onboarding-checklist.md`）。

## 创建/维护/批量工具链

### 1. 新建接口：写 OpenAPI 时就把 example 放对层（唯一可靠入口）

- `requestBody.data` **不可经 CLI 直接写**（`endpoint update` 写 `requestBody.example` 是假成功：回读长度仍为 0）。
- 唯一入口是 `import` 时经 MediaType 层级 example 生成：

```yaml
content:
  application/json:
    schema: {...}
    example:            # MediaType 层级（不是 schema.example！）
      activityId: probe_demo_001
      type: 1
```

- **只认 MediaType 层级**：`Schema.example` 与 `MediaType.example` 都合法，但 apifox 生成 DEBUG_CASE body 只认后者。放错位置**不报错、不告警，静默没有**——这是最易踩的点。
- 接口已存在且 body 为空时，没有第三条路：删接口重导（会重建全部测试用例，endpointId 变）或用户客户端点「自动生成」。所以把关口前移到「写 OpenAPI 时」。

### 2. 存量接口：match-name 重导批量补处理器（唯一自动化通道）

body 不可事后补，但 **preProcessors / postProcessors 可批量写入**：

```bash
apifox export --project <id> --format apifox --output export.json
apifox import --project <id> --format apifox --file inject.json --module-import-mode match-name
# 模块同名冲突时显式映射
apifox import --project <id> --format apifox --file inject.json --module-import-mode match-name --module-map "source:<源模块Id>=<目标模块Id>"
# 回读验证（必须，确认落库）
apifox export --project <id> --format apifox --output verify.json
```

要点：

- **读输出尾部不看头部**：`import` 的 updateCount 才是真实命中数；`endpointCase` 命中即使 `updateCount=0` 也会更新用例。
- **接口层与用例层共用同通道**：match-name 重导同时写 `api.preProcessors` 与 `cases[].preProcessors`，一次导入全部生效。
- **豁免清单必须显式维护**：负向「缺凭据」与安全性「错误签名」类用例**不能**注入签名脚本（脚本会生成合法签名导致用例失效）。注入脚本时按用例名/断言语义人工判定豁免，不可无脑全量。
- **接口层脚本会级联到所有下级用例**：给接口层加脚本 = 给所有无脚本用例加脚本。豁免用例必须加「清除鉴权头」脚本抵消（见 case study 第九节），否则负向/安全性用例被级联注入破坏。
- **脚本模板从项目内已有用例提取**，不手写；脚本内密钥一律 `pm.environment.get()` 运行时取，禁止写死。
- **`inheritPreProcessors` 落库不等于生效**：CLI run 引擎不读该字段，自动化场景用「清除脚本」抵消继承。

### 3. 校验空壳与豁免

- 回读校验：`apifox export --format apifox` 后检查 `api.cases[]` 每项的 `requestBody.data` 非空（`requestBody.data=""` 即空壳）。
- 豁免校验：注入/级联脚本前后各过一遍豁免清单，确认负向/安全性用例保持「应被拒」语义。
- 验收口径覆盖**用户可见的全部面**：agent 查 CLI 列表 ≠ 客户端接口树。两者都要验，否则会出现「我说全绿、你说是空的」的假通过（case study 教训 4）。

## 字段规范

| 字段 | 规范值 / 说明 |
|------|--------------|
| `type` | `DEBUG_CASE`（接口树下调试用例） |
| `categoryId` | `0`（DEBUG_CASE 固定为 0，与自动化用例的 categoryId 分类不同） |
| `requestBody.data` | 请求体 JSON 文本，必须非空（覆盖度铁律判定字段）；不可经 CLI 直接写，import 时经 MediaType 层级 example 生成 |
| `preProcessors` / `postProcessors` | 处理器脚本数组；可经 match-name 重导批量写入；结构 `[{"type":"customScript","data":"...","defaultEnable":true,"enable":true}]` |
| `ordering` | **重导唯一副作用：归零**（仅影响显示排序，不影响契约字段）。重导前后对比 name/path/method/folderId/tags/securityScheme/requestBody/responses/parameters 应全部 SAME |

- **签名脚本强制前缀**：接口层与用例层脚本共存时，`pm.request.headers.add` 对同名 key 是「追加」而非「覆盖」，服务端 `c.GetHeader` 取第一个——用例层脚本必须先 `headers.remove` 再 `add` 完全接管请求头，否则被接口层旧值污染（case study 第九节教训 4）。
- **fixture 重跑会让签名密钥漂移**：`partner_fixture.py` 类每次运行重生成 `api_secret`，环境变量 `v2ApiSecret`/`v2ApiKey` 不会跟着变——重跑 fixture 后必须重写环境变量（`environment update` 整体覆盖，payload 带全量变量）。判定：手动用库当前凭据请求成功、用例失败 → 环境变量漂移。

## 失败排查 8 级

> 吸收自 buer2233/ai-api-test-skill 方法论层（2026-09-01，改写为通用形态；脚本层不吸收）。接口用例失败时**按级逐层排查，不要跳级**；每级先给出根因候选再验证，避免凭印象改。

| 级 | 检查 | 根因候选 | 验证动作 |
|----|------|----------|----------|
| 1 | 请求体是否为空壳 | `requestBody.data=""`（覆盖度铁律缺口） | `apifox export --format apifox` 回读 `api.cases[].requestBody.data`；空则按「创建/维护工具链」补 example |
| 2 | 字段是否放对层 | example 放进了 `schema.example` 而非 MediaType 层级 | 对照 case study 第四节：`content."application/json".example`；放错层静默不生效 |
| 3 | 处理器/脚本是否落库 | 重导后 `preProcessors` 未写入 | 回读验证 `[{"type":"customScript",...}]`；`import` 看输出尾部 `endpointCase updateCount` |
| 4 | 接口层脚本是否级联污染 | 接口层 `api.preProcessors` 注入合法签名，豁免用例被破坏 | 检查豁免用例是否缺「清除鉴权头」脚本（case study 第九节） |
| 5 | 签名接管前缀是否缺失 | 用例层脚本只 `headers.add` 未 `remove`，被接口层旧值污染 | 确认脚本开头先 `headers.remove` 再 `add`（case study 教训 4） |
| 6 | 环境变量是否漂移 | fixture 重跑后 `v2ApiSecret`/`v2ApiKey` 未同步 | 手动用库当前凭据请求成功、用例失败 → 重写环境变量（`environment update` 整体覆盖） |
| 7 | 断言口径是否正确 | 用了 `responseCode`/`responseBody`/`equals`，或只断言 2xx | 断言 subject 用 `httpCode`/`responseJson`，comparison 用 `equal`，补结构断言（见 `testing-pitfalls.md` 二、断言陷阱） |
| 8 | 验收口径是否覆盖全 | 只查 CLI 列表没查客户端接口树，或 grep `√`/`×` 漏计失败 | 客户端接口树 + CLI 双验；runner 统计解析报告表格「断言数/失败数」两列，不用 `×` 计数（`testing-pitfalls.md` 陷阱 12-1） |
