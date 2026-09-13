# 契约测试方法论 — test-contract

> 归属 owner：`apifox`。本模块提供契约测试的方法论与 apifox 落地方式，防止前后端 / 跨团队契约漂移。吸收来源：API测试自动化专家版（ContractTester / contract_guide.md）方法论，转换为 apifox 可执行检查项。与 `modules/test-case-generation.md` 的关系：后者负责"设计用例"，本模块负责"用接口定义约束请求/响应结构"；与 `modules/import-export.md` 的关系：spec 导入导出负责保持契约同步。

## 何时加载

- 用户要求"契约测试""Schema 验证""防接口漂移"
- 接口变更后需要验证响应结构是否符合接口定义
- 前后端并行开发，需要以 OpenAPI/Schema 为契约基准
- 上线前门禁的契约部分

## 核心概念

| 概念 | 说明 |
|------|------|
| 契约测试 | 用接口定义（OpenAPI/JSON Schema）约束请求/响应结构，防止实现与文档漂移 |
| Schema 校验 | 响应字段存在性、类型、必填、枚举、格式（email/uuid/date-time） |
| 变化检测 | 对比新旧 spec，识别新增/移除/变更的端点与字段 |
| 契约用例 | 每个接口的"结构断言"用例，变更后重跑即暴露漂移 |

## 契约测试三能力（方法论）

### 1. 端点存在性校验

- 每个接口必须有 spec 定义：`method + path` 在 OpenAPI `paths` 中存在
- 接口上线但 spec 缺失 → 契约缺口（对照 `import-export.md` 质量指标：`schemas` 覆盖、`emptyObjectBodies` 风险）

### 2. 响应 Schema 校验

按响应 schema 逐字段校验，而非只看状态码：

| 校验项 | 检查内容 |
|--------|----------|
| 字段存在性 | 文档声明字段必须返回 |
| 字段类型 | 与 schema `type` 一致（string/integer/object/array） |
| 必填字段 | `required` 清单逐一非空 |
| 枚举约束 | 值必须落在 `enum` 内 |
| 格式约束 | `format: email/date-time/uuid` 合法 |
| 数组结构 | 元素类型、空数组场景 |

### 3. Schema 变化检测

- 对比新旧 spec：新增端点、移除端点、字段增删、类型变更、必填变更
- 变化点映射为受影响用例：变更字段的接口重跑契约用例
- 变更未同步 spec = 契约漂移，契约用例失败即暴露

## apifox 落地映射（强制）

- 契约为每个接口建立**结构断言用例**：断言 `httpCode` + `responseJson` 关键字段非空/类型（断言字段规则见 `modules/test-case.md`）
- 请求体结构校验：对照 endpoint schema 的 `required` 与 `type` 构造（见 `modules/test-case-generation.md` 的 schema 驱动数据构造）
- spec 同步：接口变更后经 `modules/import-export.md` 重新导入 spec，再重跑契约用例
- 跨团队共享：apifox 项目即共享契约库，契约用例失败 → 先查是 spec 过期还是实现偏差
- **环境红线不变**：契约用例运行 environment 只允许 local（`test-strategy-rules` 接口测试执行通道）

## 契约用例设计示例（结构断言）

```json
{
  "type": "assertion",
  "data": {
    "name": "响应含 data.id 且为数字",
    "subject": "responseJson",
    "comparison": "equal",
    "value": "{{expectedId}}",
    "path": "$.data.id"
  },
  "defaultEnable": true,
  "enable": true
}
```

配合自定义脚本兜底类型校验（见 `test-case.md` 断言规则：常规校验用 assertion，复杂类型用 customScript）。

## 契约测试专项维度（吸收自 api-contract-test-skill，2026-09-01）

> 吸收来源：Mohammad-Albaba/api-contract-test-skill（MIT，2026-09-01 外部吸收通道），改写为通用形态、不绑定任何 agent。除基础三能力外，契约测试还须覆盖以下 7 个专项维度，防止"接口能通但契约/安全/一致性早已漂移"。

### 契约 7 专项维度

| # | 维度 | 检查内容 | apifox 落地 |
|---|------|----------|------------|
| 1 | Schema 一致性 | 响应字段名/类型/必填与 spec 完全一致，无多余字段、无类型漂移 | 结构断言逐字段；`responseJson` + path 断言关键字段 |
| 2 | 状态码错误契约 | 每种错误码（400/401/403/404/409/422/500）的响应体结构与 spec 声明的错误 schema 一致 | 为每个声明的错误码建用例，断言 `httpCode` + 错误结构 |
| 3 | IDOR/BOLA 越权 | 用户 A 用自己的 token 访问/修改用户 B 的资源（水平越权）；普通用户访问管理员资源（垂直越权） | 建「资源归属」用例：token 属于 A，目标资源 id 属于 B，断言 403/404（不应 200） |
| 4 | 幂等与副作用 | 同请求重复执行结果一致（幂等）；创建/更新请求不得产生未声明副作用 | 同请求发两次断言幂等；对照 spec 检查副作用声明 |
| 5 | 分页越界 | page 超界/负值/超大量、pageSize 越界、排序字段非法 | 建边界用例：page=0/-1/超大、pageSize=0/超大 |
| 6 | 输入边界 | 必填缺失、超长、非法枚举、非法格式、空数组 | 对照 schema `required`/`enum`/`format`/`maxLength` 建负向用例 |
| 7 | 版本漂移 | spec 版本变更未同步实现、字段增删/类型变更未覆盖 | 对比新旧 spec（变化检测），变更接口重跑契约用例 |

### 四态判定（pass / drift / break）

> 契约用例结果不是简单的"通过/失败"，而是四态。区分后才知道下一步动作。

| 状态 | 含义 | 判定 | 下一步 |
|------|------|------|--------|
| `pass` | 契约一致 | 断言全通过，响应与 spec 匹配 | 无需动作 |
| `drift` | 契约漂移（实现变了但 spec 没更新） | 响应结构与当前 spec 不符，但可能是 spec 过期 | 先核对新旧 spec，再决定更新 spec 还是修实现 |
| `break` | 契约断裂（实现不符合任何已声明契约） | 响应与 spec 不符且 spec 是当前权威 | 阻断发布，修实现或修 spec 后重跑 |
| 未知/存疑 | 无法判定 | 响应/断言口径存疑 | 先回 `testing-pitfalls.md` 排查断言口径再判定 |

### 基线只作比较不作证明

- **基线（baseline）是"变更检测的参照"，不是"实现正确的证明"**：基线契约用例通过 ≠ 接口符合最终契约，只说明"相对上次没有新增漂移"。
- 用基线的方式：变更前后各跑一次，对比差异定位漂移；不能把"基线通过"当验收依据。
- 基线需随 spec 变更显式更新；基线过期会让 `drift` 误判为 `pass`。

### evidence 规则（契约证据留痕）

- 每次契约测试运行记录：spec 版本（或 spec 快照标识）、被测接口清单、四态判定结果、漂移/断裂点（字段级）。
- 失败/漂移必须有证据：`apifox` runner 报告（断言数/失败数两列，见 `testing-pitfalls.md` 陷阱 12-1）+ 响应样例。
- 证据落点：测试主文档或项目 `PROJECT_TEST.md` 契约节，供下次对比与上线门禁引用。

### 与 test-auth.md 的边界

- 本维度只做**资源归属与越权结果的契约判定**（断言 403/404 的响应结构）；token 获取/续期/签名构造/免签分支等鉴权机制本身见 `modules/test-auth.md`。
- 幂等只做**重复请求结果一致性**断言；前置数据构造与 fixture 环境变量见 `modules/test-data-and-judgement.md` / `modules/environment.md`。

## 契约测试检查清单

- [ ] 每个接口有 spec 定义（method+path 存在）
- [ ] 响应关键字段全部有结构断言
- [ ] 必填字段、枚举、格式约束已覆盖
- [ ] 7 专项维度按风险覆盖（越权/幂等/分页/输入边界/版本漂移至少抽查）
- [ ] 四态判定（pass/drift/break）已区分，drift/break 有证据留痕
- [ ] 基线只作比较不作证明，spec 变更后基线显式更新
- [ ] spec 变更后重跑全部契约用例
- [ ] 失败时区分"spec 过期"与"实现偏差"
- [ ] 契约用例已在 apifox 真实运行通过

## 常见恢复

| 现象 | 处理 |
|------|------|
| 契约用例失败但接口正常 | 先查 spec 是否过期（`import-export.md` 重新导入） |
| 字段类型断言不生效 | 检查 assertion 的 subject/path 是否命中真实响应路径 |
| 契约用例过多 | 按"每接口 ≥1 结构断言 + 关键字段"校准，避免重复断言同字段 |
| schema 是空对象 | 回 `import-export.md` 处理 `emptyObjectBodies` 风险后再建契约用例 |
