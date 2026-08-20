# 接口测试用例 — test-case / test-data

> 本模块覆盖接口测试用例和测试数据集管理。已从 SKILL.md 继承：写入标准流程、分支参数规则。

## 何时加载

- 创建/更新/删除/查看接口下的测试用例
- 管理测试步骤、断言、提取变量、前后置处理器
- 管理测试数据集（test-data）
- 排查"测试步骤无法展示""断言不生效""提取变量为空"
- 按 caseId、endpointId、categoryId 运行测试用例

## 不应使用

- 多接口流程编排 → 加载 `modules/test-scenario.md`
- 运行套件/CI → 加载 `modules/test-automation.md`
- 只改接口定义 → 加载 `modules/api-design.md`

## 核心概念

| 概念 | CLI 资源 | 说明 |
|------|----------|------|
| 接口测试用例 | `test-case` | 绑定接口 endpoint 的测试数据与步骤 |
| 测试分类 | `test-case category` | 创建 case 前用于获取有效 `categoryId` |
| 测试数据集 | `test-data` | 可供迭代运行的数据 |
| 接口定义 | `endpoint` | case 的依赖对象，不等同 case |

## 命令入口

```bash
apifox test-case --help
apifox test-data --help
```

具体参数以当前 CLI help 为准。

## 创建测试用例标准流程

> 收口目标：在 apifox「自动化测试」菜单的 正向 / 负向 / 边界值 / 安全性 / 其他 分类下，每接口在「正向/负向/边界值」三个分类下都有用例，且正向上覆盖业务参数（非仅分页），POST 等非 GET 接口有完整覆盖。详见 `modules/test-case-generation.md` 的「覆盖度铁律」。

0. **创建前自检覆盖度（强制）**：先用 `test-case list --endpoint <endpointId>` 拉取当前接口下已有用例，按 正向 / 负向 / 边界值 三维列出缺口（POST/PUT/PATCH/DELETE 接口必须有 0→完整 的覆盖推进），缺口先呈现给用户确认后再继续
1. 确认项目和分支（参见 `modules/ai-team-project.md` 的「首轮必须指明 → 持久化」规则）
2. 定位 endpoint：`apifox endpoint list/get`
3. **必须执行** `apifox test-case category --project <projectId>` 获取有效 `categoryId`
4. 如有类似 case，先 `test-case list --endpoint <endpointId>` 再 `get` 一个作为模板
5. 获取 `test-case-create` schema 并校验
6. 构造完整 JSON（不要只写空壳 name/endpointId）
7. 创建后立即 `test-case get <caseId>` 确认后端保存结构
8. 运行一次确认 requestBody、处理器、断言和脚本在 runner 中生效

> `categoryId` 是前端展示测试用例的**关键必填字段**。无效 `categoryId` 可能导致 CLI 能看到但客户端不可见。

## 更新测试用例

更新时必须先 `get` 原结构并基于完整结构修改，`update` 不是 JSON Patch，会整体覆盖。`test-case-update` schema 已包含 processor/assertion/extractor 的枚举值说明，不要凭经验猜字段名。

## 处理器结构

> 处理器分两类：**preProcessors（前置，请求发出前执行）** 与 **postProcessors（后置，响应返回后执行）**。前置处理器用于鉴权自动续期、动态签名、动态参数准备；后置处理器用于断言、提取变量。鉴权自动化的完整方案（登录用例 extractor / 前置脚本自动重登 / JWT 构造）见 `modules/test-auth.md`。

```json
{
  "requestBody": {
    "type": "application/json",
    "data": "{\n  \"name\": \"Demo\"\n}"
  },
  "preProcessors": [
    {
      "id": "preProcessors.0.customScript",
      "type": "customScript",
      "data": "// 请求前脚本：如 token 过期自动重登（模板见 modules/test-auth.md 方案 B）",
      "defaultEnable": true,
      "enable": true
    }
  ],
  "postProcessors": [
    {
      "id": "postProcessors.0.customScript",
      "type": "customScript",
      "data": "pm.test('返回 ID', function () {\n  var body = pm.response.json();\n  pm.expect(body.data.id).to.exist;\n});",
      "defaultEnable": true,
      "enable": true
    },
    {
      "id": "postProcessors.1.extractor",
      "type": "extractor",
      "data": {
        "variableName": "token",
        "variableType": "globals",
        "shareScope": "PROJECT",
        "subject": "responseJson",
        "expression": "$.data.token"
      },
      "defaultEnable": true,
      "enable": true
    }
  ]
}
```

规则：
- `requestBody.data` 必须是字符串，不要把 JSON Body 写成对象
- 处理器使用扁平结构 `{ id, type, data, defaultEnable, enable }`
- 处理器建议带稳定 `id`（preProcessor 用 `preProcessors.N.*`，postProcessor 用 `postProcessors.N.*`）
- `shareScope` 优先 `PROJECT`，不要默认 `TEAM`
- 多行内容用 `\n` 预格式化
- **`update` 是整体覆盖**：更新时保留原有 preProcessors + postProcessors，不要只带新增的处理器

## 断言规则

常规校验优先用可视化 `assertion`，自定义脚本只做兜底：
- HTTP 状态码用 `httpCode`，不要用 `responseCode`
- JSON 字段用 `responseJson`，不要用 `responseBody`
- 全文包含用 `responseText` + `include`
- 比较符用 `equal`，不要用 `equals`

```json
{
  "type": "assertion",
  "data": {
    "name": "HTTP 状态码为 200",
    "subject": "httpCode",
    "comparison": "equal",
    "value": "200",
    "path": ""
  },
  "defaultEnable": true,
  "enable": true
}
```

## 断言顺序（强制）

> 吸收自 API测试自动化专家版。每个用例的断言按固定顺序编写，避免"表面通过"：

1. **先查状态码**：`httpCode` + `equal`（先确认 HTTP 层正确）
2. **再查业务码**：`responseJson` + `$.code`（业务层是否正确）
3. **后查关键字段**：`responseJson` + path 断言关键响应字段非空/值正确

禁止只断言 2xx 不校验响应结构，也禁止把错误路径断言成"符合预期"。

## 断言速查（16 种映射）

> 吸收自 API测试自动化专家版 Assertions 分类，映射到 apifox assertion 字段。

| 断言意图 | apifox 落地 |
|----------|-------------|
| HTTP 状态码 | `httpCode` + `equal` + value（支持多值 `[200, 201]`） |
| 任意 2xx | 自定义脚本断言（pm.response.code 2xx） |
| JSON 字段存在 | `responseJson` + path + `notNull` 或 `include` |
| JSON 字段值 | `responseJson` + path + `equal` |
| JSON 嵌套路径 | `responseJson` + `$.data.items[0].id` |
| JSON Schema 结构 | 自定义脚本 + 关键字段类型断言兜底 |
| 响应全文包含 | `responseText` + `include` |
| Header 存在/值 | `responseHeader` + 名称 + `equal/include` |
| Content-Type | `responseHeader` + `Content-Type` + `equal` |
| 响应时间阈值 | 自定义脚本（pm.response.responseTime） |
| 字段非空 | `responseJson` + path + 自定义脚本断言非空 |
| 数组长度 | 自定义脚本（pm.expect(body.data.items.length)） |
| 字段类型 | 自定义脚本（typeof） |
| 数值大小比较 | 自定义脚本（pm.expect(Number(...)).to.be.above/below） |
| 枚举值校验 | `responseJson` + path + `equal` 逐一断言 |
| 错误结构校验 | `httpCode` 4xx + `responseJson` + `$.code` 非空 |

> 规则：常规校验优先用可视化 `assertion`（上表前 6 行），复杂校验用自定义脚本兜底（`pm.test` / `pm.expect`）。

## 字段风险提醒

- 不要把 `test-scenario` 的步骤结构写进 `test-case`
- 不要只写 case 名称和 endpointId（空壳）
- 不要使用未验证的 `categoryId`
- 不要凭经验猜 processor/assertion/extractor 的字段名
- test-case 不支持跨步骤数据传递，需要时加载 `test-scenario`

## 数据清理机制（写接口用例，强制）

> 方法论见 `modules/test-case-generation.md`「规则 F：写接口测试数据清理铁律」，本节只给 CLI 落地写法。

- **POST 用例清理**：在 `postProcessors` 加 `extractor` 提取新建资源主键（`shareScope=PROJECT`），随后用 `test-scenario` 把"创建 case → 断言 case → 删除 case（复用 {{提取的id}}）"编成一条场景；单独跑创建 case 时不清理，必须跑场景才算完整闭环。
- **PUT/PATCH 用例清理**：优先对 fixture（专用测试记录，不服务真实业务）操作；若必须改共享数据，在同一 case 的 `postProcessors` 末尾加一个还原请求（自定义脚本里发起还原调用，或场景里追加还原步骤）。
- **DELETE 用例清理**：本身即清理动作，但前置必须是"本场景创建的数据"，不要对已有业务数据跑删除用例；场景第一步用创建 case 的 extractor 产出 id，最后一步才是 delete case。
- **无删除接口的资源**：在 `PROJECT_TEST.md`「遗留测试数据」登记，不要跳过清理环节就直接收口。

## 运行规则

- `test-case run <caseId>` — 单个 case
- `test-case run --endpoint <endpointId>` — 按接口运行
- `--category <categoryId>` 必须和 `--endpoint <endpointId>` 一起使用
- `apifox run --test-case <caseId>` 只支持 caseId
- 建议显式指定 `--environment <开发环境Id>`
- **运行前环境变量就绪检查（强制）**：用例依赖鉴权/登录/签名时，先核对开发环境变量是否齐备（对照 `PROJECT_TEST.md`「环境变量登记」表）；401/403/签名错误/token 无效 → 先查环境变量缺失/过期，再查接口——不要算成接口失败（详见 `modules/environment.md`「开发环境环境变量（强制）」节）

## 常见恢复

| 现象 | 处理 |
|------|------|
| 测试步骤不展示 | `test-case get` 看真实保存结构 |
| 断言不生效 | 对比现有成功 case 模板，检查 assertion 字段 |
| 提取变量为空 | 检查 extractor 层级、变量名、响应路径和执行报告 |
| endpoint 下找不到 case | 检查 `--branch` 和 `--endpoint` |
| 401/403/签名错误/token 无效 | 先核对开发环境变量（鉴权签名/登录账号/token）是否缺失或过期，对照 `PROJECT_TEST.md`「环境变量登记」表，再查接口 |
| 登录后 token 没生效 | 检查登录用例 extractor（`shareScope=PROJECT`）与后续用例环境变量引用 {{token}} |
