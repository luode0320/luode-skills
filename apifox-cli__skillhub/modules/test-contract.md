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

## 契约测试检查清单

- [ ] 每个接口有 spec 定义（method+path 存在）
- [ ] 响应关键字段全部有结构断言
- [ ] 必填字段、枚举、格式约束已覆盖
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
