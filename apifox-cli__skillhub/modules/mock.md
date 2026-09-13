# Mock 期望管理 — mock expectation

> 本模块覆盖 Mock 期望的创建、查询、更新、删除，以及**在测试流程中自动的 Mock 同步与对齐**。已从 SKILL.md 继承：写入标准流程（cli-schema get → validate → write）、分支参数规则。

## 何时加载

- 创建/更新/查询/删除 Mock 期望
- 接口测试前检查 Mock 覆盖度
- 接口测试中同步更新 Mock 数据
- 接口 schema/用例变更后检查 Mock 是否仍有效
- 排查"接口返回 404 或异常响应"（Mock 未配置 / Mock 条件不匹配）

## 核心概念

| 概念 | CLI 资源 | 说明 |
|------|----------|------|
| Mock 期望（expectation） | `mock` | 一个接口的 Mock 响应规则，含匹配条件和响应定义 |
| 条件（conditions） | `mock create` 的 `conditions` 数组 | 按请求参数匹配的规则，命中哪个条件就返回哪个响应 |
| 响应（response） | `mock create` 的 `response` 对象 | 返回的 HTTP 状态码/延迟/头/body |
| 智能 Mock | apifox 内置（非 CLI 管理） | 基于 schema 自动生成的 Mock，CLI 创建的是固定期望 |

## 命令入口

```bash
apifox mock --help
apifox mock list --help
apifox mock get --help
apifox mock create --help
apifox mock update --help
apifox mock delete --help
```

## Mock 期望结构（CLI 事实）

```json
{
  "name": "Mock 期望名称（必填，max 255）",
  "apiDetailId": 12345,
  "conditions": [
    {
      "name": "参数名",
      "value": "期望值",
      "location": "query|path|header|cookie|body|auth|advancedSettings|preProcessors|postProcessors",
      "comparison": "equal|notEqual|exists|notExist|isBelow|isAtMost|isAbove|isAtLeast|match|include|notInclude",
      "enable": true
    }
  ],
  "ipCondition": {
    "enable": true,
    "value": "192.168.1.1"
  },
  "response": {
    "code": 200,
    "delay": 0,
    "headers": [
      { "key": "Content-Type", "value": "application/json" }
    ],
    "bodyType": "json",
    "bodyData": "{\n  \"code\": 0,\n  \"data\": {}\n}",
    "disableMockJs": false,
    "disableTemplating": false
  }
}
```

### 关键字段说明

- **`conditions`**：可选。为空数组时匹配所有请求（兜底 Mock）。条件之间是 **AND 关系**，全部命中才返回对应响应。
- **`location`**：参数位置，支持 `query` / `path` / `header` / `cookie` / `body` / `auth` / `advancedSettings` / `preProcessors` / `postProcessors`。
- **`comparison`**：比较方式，常用 `equal`（精确匹配）、`exists`（存在就行）、`match`（正则）、`include`（包含）。
- **`response.bodyData`**：响应 body 内容。`bodyType=json` 时必须是 JSON 字符串（bodyData 本身是字符串，JSON 内容需用 `\n` 转义多行）。
- **`disableMockJs` / `disableTemplating`**：禁用智能 Mock JS 和模板引擎，固定返回 bodyData 内容。

### 多条 Mock 期望的匹配顺序

一个接口可以有多个 Mock 期望，Apifox 按**创建顺序**（或手动排序）依次匹配：先匹配条件的先返回。**最具体的条件应放在最前面**，一个兜底期望（无条件的）放最后。

## Mock 在测试流程中的职责（核心）

> **Mock 不是一次配置永久有效的——接口 schema 变了、用例数据变了、接口新增了，Mock 就应该跟着变，否则接口测试要么返回 404（无 Mock），要么返回过时的假数据（误导）。**

### 两条铁律

1. **Mock 不是测试的替代品**——接口级测试应连接真实被测服务，Mock 仅用于：
   - 前端/对接方**独立开发**时（后端接口尚未就绪）
   - 依赖服务**不可用**时的局部隔离测试
   - 特定**异常场景**（如超时、500 错误）的模拟
2. **Mock 数据必须与真实接口行为一致**——当接口已经完成开发、测试用例已跑通时，Mock 的响应数据必须与真实响应对齐（规则 T-2 已规定 Mock 示例不能为空壳，本模块补的是"同步"），否则 Mock 会成为致命误导源。

### 何时需要创建/更新 Mock（自动触发）

以下场景 agent 应在完成主任务后**自动检查 Mock 状态并同步更新**，无需用户额外指示：

| 触发场景 | 动作 | 检查方法 |
|----------|------|----------|
| **接口创建/导入后** | 检查该接口是否有 Mock 期望，无则按 schema 创建兜底 Mock | `mock list --http-api-id <id>` |
| **接口测试用例创建/跑通后** | 用真实响应数据更新 Mock 的 `response.bodyData`，保持 Mock 与真实行为一致 | `mock get <mockId>` 对比真实响应 |
| **接口 schema 变更后**（新增/删除字段、类型变更） | 检查已有的 Mock 响应 bodyData 是否仍匹配最新 schema，不匹配则更新 | `endpoint get <id>` 对比 schema 字段 |
| **用例参数模式变更后** | 更新 Mock 的 `conditions` 匹配条件，确保新参数模式也能命中 Mock | 导出对比用例参数分布 |
| **测试返回 404 或异常** | 先检查 Mock 是否缺失（Mock 未配置是常见原因），缺则创建 | 排查步骤见 `testing-pitfalls.md` |

### Mock 同步时机：测试流程中的三个节点

> **分别在测试前、测试中、测试后检查 Mock 状态，确保 Mock 始终反映真实接口行为。**

#### 节点 M1：测试前 — Mock 覆盖度检查（强制）

**触发时机**：准备运行接口测试前，或创建新接口的测试用例前。

**执行步骤**：

1. 列出目标接口的 Mock 期望：`apifox mock list --project <projectId> --http-api-id <endpointId> --branch <branch>`
2. 检查覆盖度：
   - 接口有 Mock → 检查 `response.bodyData` 是否为空壳或过时（对比 schema 字段）
   - 接口无 Mock → 按当前 schema 创建兜底 Mock（无条件的，匹配所有请求）
3. **通过标准**：每个有用例的接口至少有一个非空 Mock 期望（bodyData 含全部必填响应字段，schema 字段对齐）
4. **不通过则阻断**：无 Mock 或 Mock 空壳 → 必须先创建/更新 Mock 再运行测试，不要等接口返回 404 再排查

#### 节点 M2：测试中 — Mock 与真实响应自动对齐（强制）

**触发时机**：接口测试用例跑通（成功响应）后，立即用真实响应数据更新 Mock。

**核心逻辑**：Mock 的价值在于"模拟真实接口行为"，因此在**测试用例首次跑通后**，agent 应自动将 Mock 的 `response.bodyData` 更新为刚刚实测到的真实响应——测试通过证明接口是通的，真实响应就是 Mock 该返回的数据。

**为什么不是即时同步而是"首次跑通后"**：
- 创建接口/导入 swag 时即创建 Mock（节点 M1），此时用 schema 自动生成示例数据作为初始 Mock
- 第一次跑通测试用例后，用真实响应更新 Mock（节点 M2），确保 Mock 数据从"形状正确"升级为"内容真实"
- 后续接口变更时再回到节点 M1 检查

**执行步骤**：

1. 测试用例跑通（HTTP 200 + 业务码正确 + 结构完整）后，记录真实响应 body
2. 查询该接口的 Mock 期望：`mock list --http-api-id <endpointId>`，取第一个
3. 对比 Mock 的 `response.bodyData` 与真实响应 body：
   - **一致** → 跳过，Mock 已对齐
   - **不一致且 Mock 明显过时**（空壳 `{}`、字段明显缺失、值与真实响应不同）→ 更新 Mock 响应
   - **不一致但 Mock 是特意构造的异常场景**（如特意返回 500 用于测异常路径）→ 不做覆盖，保持原 Mock
4. 更新时遵循写入标准流程：`mock get <mockId>` 获取完整结构 → 改 `response.bodyData` → `cli-schema validate mock-update` → `mock update`

**同步规则**：

| 真实响应特征 | Mock 同步动作 |
|-------------|--------------|
| 200 成功，body 含完整业务数据 | 用真实 body 替换 Mock 的 `bodyData` |
| 401/403（环境变量缺失导致） | **不同步**——这是环境问题，不是接口真实行为 |
| 500（业务数据不足导致） | **不同步**——这是用例数据问题，不是接口真实行为 |
| 接口返回 404（Mock 缺失导致） | 按 schema 先创建兜底 Mock，再重跑测试 |
| 4xx/5xx 是接口的**正常业务逻辑**（如查不存在的记录） | 可同步，但标注为异常场景 Mock |

#### 节点 M3：测试后 — Mock 质量审计（推荐）

**触发时机**：项目收口/上线前，或定期质量审计时。

**检查项**：
1. 有接口用例但无 Mock 的接口数 → 补创建兜底 Mock
2. Mock bodyData 与 schema 字段不匹配的接口数 → 按 schema 对齐
3. Mock bodyData 为空壳 `{}` 的接口数 → 补真实数据

## 兜底 Mock 创建（强制）

> 每个有测试用例的接口都应该有**至少一个无条件兜底 Mock**，确保前端/对接方在接口未就绪时也能拿到合理响应。

**兜底 Mock 标准**：

```json
{
  "name": "兜底-<接口摘要>",
  "apiDetailId": <endpointId>,
  "conditions": [],
  "response": {
    "code": 200,
    "delay": 0,
    "headers": [{ "key": "Content-Type", "value": "application/json" }],
    "bodyType": "json",
    "bodyData": "<pretty-print JSON 含全部必填响应字段>"
  }
}
```

- `conditions` 为空数组 → 匹配所有请求（兜底）
- `bodyData` 必须包含接口 schema 中的**全部必填响应字段**，且数据合理（ID 非空、时间格式正确、枚举值合法）
- `bodyData` 的 JSON 格式化规则同 `test-case.md` 规则 T-1（pretty-print，2 空格缩进）

### Schema 驱动 Mock 数据生成规则（强制）

> 吸收自 `z-dev-unit-mock`（单元测试Mock生成器）的核心方法论：**输入 schema 字段定义 → 输出可用的 Mock 数据**。避免生成空壳 `{}` 或肉眼可见的占位符（如全是 `"string"`、`123`）。

以下表按字段类型定义 Mock 数据值，agent 创建兜底 Mock 时按此规则自动生成 `bodyData`：

| 字段类型 | 正向 Mock 值（真实感） | 说明 |
|---------|----------------------|------|
| `string`（无约束） | `"示例文本"`（中文）/ `"sample-name"`（英文标识） | 优先从字段名/description 推断语义，如 `name`→`"测试策略"`、`email`→`"test@example.com"`；字段名含 `url`→`"https://api.example.com/resource/1"` |
| `string` + `enum` | 取枚举第一个合法值 | 如 `["pending","active","disabled"]` → `"pending"` |
| `string` + `format: date` | `"2026-09-08"` | 当前日期，格式 `YYYY-MM-DD` |
| `string` + `format: date-time` | `"2026-09-08T10:00:00Z"` | 当前时间 ISO 8601 |
| `string` + `format: email` | `"admin@example.com"` | 标准邮箱格式 |
| `string` + `format: uri` / `url` | `"https://api.example.com/v1/resource"` | 可访问的 URL 示例 |
| `string` + `format: ipv4` | `"192.168.1.1"` | 内网地址 |
| `string` + `format: uuid` | `"a1b2c3d4-e5f6-7890-abcd-ef1234567890"` | 标准 UUID v4 格式 |
| `integer`（无约束） | `1` | 正数，从 1 开始递增 |
| `integer` + `minimum` | `minimum` 值 | 如 `minimum=0` → `0`；`minimum=1` → `1` |
| `integer` + `enum` | 取枚举第一个合法值 | 如 `[1,2,3]` → `1` |
| `number`（浮点） | `1.0` | 精度 1-2 位小数 |
| `number` + `minimum` | `minimum` 值 | 如 `minimum=0` → `0.0` |
| `boolean` | `true` | 正向业务场景用 true |
| `array` | `[]` 空数组或 `[{...}]` 含一个元素 | 兜底用非空数组，元素按子 schema 规则生成 |
| `array` + `minItems` | 按 `minItems` 生成对应数量的元素 | 如 `minItems=1` → `[{...}]` |
| `object` | `{}` 或 `{...}` 含全部必填字段 | 按子字段逐层展开 |
| `object` 无必填 | `{}` | 可空对象，不强制生成内部字段 |
| `null` 可空 | `null` 或不生成该字段 | 按字段是否 required 决定 |
| `$ref` 引用类型 | 按被引用的 schema 定义生成 | 递归展开，防循环引用（maxDepth=3） |

**语义推断优先**（字段名驱动的值选择）：

| 字段名关键词 | 推断的 Mock 值 |
|-------------|---------------|
| `name` / `title` / `nickname` | `"测试名称"` / `"测试标题"` |
| `description` / `desc` / `remark` / `note` | `"这是测试描述"` |
| `status` / `state` / `phase` | 枚举取第一个；无枚举时 `1` 或 `"active"` |
| `type` / `category` / `kind` / `classify` | 枚举取第一个；无枚举时 `"default"` 或 `1` |
| `id` / `pk` / `primaryKey` | `1`（整数）或 `"ID_001"`（字符串） |
| `createdAt` / `updatedAt` / `deletedAt` / `createTime` / `updateTime` | `"2026-09-08T10:00:00Z"` |
| `createdBy` / `updatedBy` / `creator` / `operator` | `"admin"` 或 `1` |
| `email` / `mail` | `"admin@example.com"` |
| `phone` / `mobile` / `tel` | `"13800138000"` |
| `url` / `link` / `href` | `"https://api.example.com/resource/1"` |
| `avatar` / `icon` / `image` / `photo` | `"https://api.example.com/static/default.png"` |
| `address` / `location` | `"中国广东省深圳市南山区"` |
| `code` / `errorCode` / `errCode` | `0`（成功时）或 `"SUCCESS"` |
| `message` / `msg` / `errorMsg` | `"操作成功"` / `"success"` |
| `count` / `total` / `size` | `10` |
| `page` / `pageNum` / `offset` | `1` |
| `pageSize` / `limit` / `perPage` | `10` |
| `sort` / `orderBy` / `order` | `"desc"` 或 `"createdAt"` |
| `enabled` / `isEnabled` / `active` / `isActive` | `true` |
| `deleted` / `isDeleted` | `false` |
| `version` / `revision` | `1` |

**生成策略**：
- 接口 schema 中**`required` 数组里的字段**必须全部出现在 bodyData 中
- 非必填字段：可选加入，建议至少覆盖 60% 的非必填字段让 Mock 更真实
- 嵌套对象逐层展开，**最大深度 3 层**（避免嵌套过深导致 JSON 臃肿）
- 数组元素：生成 1 个示例元素（除非 `minItems` 指定更大值）
- 生成后执行 `pretty_jsonb` 格式化（同 `test-case.md` 规则 T-1）

**适用场景**：
- 接口创建/导入后首次创建兜底 Mock（M1 节点）
- 接口新增字段后同步更新 Mock（schema 变更）
- 测试用例尚未跑通时的初始 Mock 数据（M2 节点跑通后会被真实数据覆盖）

## 带条件 Mock 创建（可选）

需要模拟不同参数返回不同响应时，创建带条件的 Mock 期望：

```json
{
  "name": "按名称查询-存在",
  "apiDetailId": <endpointId>,
  "conditions": [
    {
      "name": "name",
      "value": "已存在名称",
      "location": "query",
      "comparison": "equal",
      "enable": true
    }
  ],
  "response": {
    "code": 200,
    "delay": 0,
    "headers": [{ "key": "Content-Type", "value": "application/json" }],
    "bodyType": "json",
    "bodyData": "{\n  \"code\": 0,\n  \"data\": {\n    \"id\": 1,\n    \"name\": \"已存在名称\",\n    \"status\": 1\n  }\n}"
  }
}
```

**设计原则**：
- 条件从**具体到通用**排列（最具体的条件先匹配）
- 条件值从**测试用例的真实参数**中提取，不要凭空编造
- 异常场景（404/500/超时）的 Mock 单独创建，用条件区分

## 写入标准流程（强制）

> 与 SKILL.md 的「写入标准流程」一致，逐步执行，不跳步。

```bash
# 1. 获取 schema（create 或 update）
apifox cli-schema get mock-create
apifox cli-schema get mock-update

# 2. 构造 JSON 文件
# 3. 校验
apifox cli-schema validate mock-create --file <path>
apifox cli-schema validate mock-update --file <path>

# 4. 写入
apifox mock create --project <projectId> --file <path>
apifox mock update <mockId> --project <projectId> --file <path>

# 5. 回读确认（写入后立即校验）
apifox mock get <mockId> --project <projectId>
```

**update 注意事项（与 SKILL.md 一致）**：update 不是 JSON Patch，是整体覆盖。修改数组/嵌套对象前先 `mock get` 拉完整结构，在完整结构上修改后再 update。

## 异常场景 Mock 设计（可选）

> 吸收自 `kunlun-cn-api-mock`（API Mock 与联调助手）的工程实践方法论。正常响应的 Mock 是基础，但联调中真正拖慢进度的往往是"依赖服务不可用""接口超时""限流"等异常场景的 Mock 缺失。

以下场景应该在兜底 Mock 之外，**单独创建带条件的 Mock 期望**用于模拟异常：

| 异常场景 | Mock 行为 | 典型响应 | 联调用途 |
|----------|-----------|---------|---------|
| 接口超时 | `delay: 15000`（15 秒延迟） | 200，但前端感知超时 | 前端验证超时重试/loading 超时样式 |
| 服务端错误 | 返回 500 | `{"code":500,"msg":"Internal Server Error"}` | 前端验证 500 降级页面 |
| 请求被限流 | 返回 429 | `{"code":429,"msg":"Too Many Requests"}` | 前端验证限流提示和重试策略 |
| 数据不存在 | 返回 404 | `{"code":404,"msg":"资源不存在"}` | 前端验证空态/缺省页 |
| 参数校验失败 | 返回 400 | `{"code":400,"msg":"参数 xxx 不合法"}` | 前端验证表单错误提示 |
| 无权限 | 返回 403 | `{"code":403,"msg":"无操作权限"}` | 前端验证权限提示和跳转 |
| 服务降级 | 返回 503 | `{"code":503,"msg":"服务暂不可用，请稍后重试"}` | 前端验证降级页面 |

**设计原则**：
- 异常 Mock 应该**通过条件区分**（如特定 `userId=0` 触发 500，而非覆盖所有请求），避免影响正常接口调试
- 异常 Mock 的 `delay` 值要合理（超时 = 前端超时时间 × 1.5，限流按实际阈值）
- 异常 Mock 创建后要在联调清单中标注"已就绪"，让前端知道哪些异常场景已可验证
- 接口上线后，异常 Mock 可以保留但**应标记为 disabled**，仅在需要时手动启用

## 契约先行原则（强制）

> 吸收自 `kunlun-cn-api-mock`（API Mock 与联调助手）的核心方法论：**在创建 Mock 之前，先保证接口契约（请求/响应 schema）已固化**。Mock 是契约的"实例化"，不是独立于接口的随意数据。

**契约先行的含义**：
- 创建 Mock 前，先确认接口的 `method + path`、请求参数、响应 schema 已与代码侧契约对齐（遵循 `api-sync-to-apifox.md` 的契约校验规则）
- 若接口 schema 尚未确定（仍在开发阶段），Mock 的 `bodyData` 应标注 `"// TODO: schema 待定"` 注释，并标记为**临时 Mock**，待 schema 确认后更新
- 契约未固化即创建 Mock → Mock 数据与真实接口形状不一致 → 前端按 Mock 开发 → 联调时发现不匹配 → 返工

**契约固化的三种状态与 Mock 策略**：

| 契约状态 | 定义 | Mock 策略 |
|---------|------|----------|
| ✅ 已确定 | schema 已与代码侧对齐，字段、类型、约束已完成 | 创建完整 Mock（含全部必填字段、语义推断值） |
| ⏳ 草稿中 | schema 存在但未与代码侧对齐，部分字段可能变更 | 创建**临时 Mock**，bodyData 标注 `// TODO`，schema 确认后必须更新 |
| ❌ 未定义 | 接口仅有 method+path，无响应 schema | **不创建 Mock**，先引导用户完成响应定义（`apifox endpoint update` 补 schema） |

**CLI 检查方法**：
```bash
# 获取接口 schema 检查响应定义是否完整
apifox endpoint get <endpointId> | jq '.response'  # 检查 response 是否有内容
# 若 response 为空 → 契约未定义，先补 schema 再创建 Mock
```

### 临时 Mock 的管理

临时 Mock 是契约未完全确定时创建的过渡性 Mock，需要特殊管理：
- 命名前缀：`[TEMP] 兜底-<接口摘要>`（区别于正式 Mock）
- 条件：与正式兜底 Mock 一致，conditions 为空数组
- 生命周期：一旦契约确认（接口 schema 与代码对齐），必须更新临时 Mock 为正式 Mock
- 过期清理：契约确认后仍残留的 `[TEMP]` 前缀 Mock → 视为未对齐，阻断联调

## 联调清单（推荐）

> 吸收自 `kunlun-cn-api-mock`（API Mock 与联调助手）的"联调清单"理念。当后端接口 Mock 已就绪、准备交付前端/其他消费者联调时，按以下清单逐项确认。

### 联调前检查清单

| # | 检查项 | 检查方法 | 通过标准 |
|---|--------|---------|---------|
| 1 | 接口已创建 | `apifox endpoint list` | method+path 存在，且有响应 schema |
| 2 | 兜底 Mock 已创建 | `apifox mock list --http-api-id <id>` | 至少 1 个 Mock 期望，且非空壳 |
| 3 | Mock bodyData 含全部必填字段 | `mock get <id>` 对比 schema | Mock 响应字段与 schema required 对齐 |
| 4 | Mock 数据语义合理 | 人工查看 bodyData | 不是 `{}` 空壳或全是 `123`/"string" |
| 5 | 异常场景 Mock 已就绪 | `mock list` 检查异常场景 | 至少 500 超时两个常用异常 Mock 已创建（可选但推荐） |
| 6 | Mock 响应状态码覆盖完整 | 对比接口 schema 的所有 response code | 200 必须有，4xx/5xx 按需 |
| 7 | 带条件 Mock 的匹配条件可用 | 用条件值测试 Mock 命中 | 条件值来自测试用例真实参数，非凭空编造 |
| 8 | 契约是否已确定 | `endpoint get` 检查响应 schema | 非 `[TEMP]` 状态，schema 已与代码对齐 |

### 联调中发现问题时的排错清单

| 现象 | 可能原因 | 检查步骤 |
|------|---------|---------|
| 前端请求返回 404 | Mock 未创建 / 条件不匹配 | `mock list` 检查是否有 Mock；条件值是否匹配请求参数 |
| 前端收到 `{}` 空响应 | Mock bodyData 为空壳 | `mock get` 检查 bodyData，按 schema 补全数据 |
| 响应字段与预期不一致 | Mock 数据过时 / schema 变更后未同步 | 对比 `endpoint get` schema 与 Mock bodyData |
| 异常场景无法触发 | 异常 Mock 未创建 / 条件不匹配 | `mock list` 检查异常场景 Mock 是否存在 |
| 延迟响应不符预期 | Mock 的 delay 值不合理 | `mock get` 检查 delay 值，按前端超时时间调整 |

## 不可违反规则

1. **每个有测试用例的接口必须有兜底 Mock**：无 Mock 即运行测试，接口测试可能返回 404（Mock 未配置导致），先创建 Mock 再测
2. **Mock 不允许空壳**：`bodyData` 为 `{}` 空壳或字段少于 schema 必填字段 → 判定为无效 Mock，必须补全真实数据。此规则与 `test-case.md` 规则 T-2 一致
3. **Mock 数据必须与真实响应对齐**：用例跑通后，Mock 的 `bodyData` 应与真实响应一致；不一致时同步更新
4. **写入必须预热 + 回读**：Mock 创建/更新后，先 `mock get` 回读确认落库，再宣称已就绪（与 `environment.md` 的环境变量假成功为同一类陷阱）
5. **Mock 是测试配套，不是测试替代**：接口级测试以真实被测服务为准，Mock 仅用于前端开发/依赖隔离/异常模拟；Mock 全绿 ≠ 接口真通
6. **Mock 条件用例参数来源**：创建带条件 Mock 时，条件值从测试用例的真实参数提取，不凭空编造不可能匹配的条件
7. **测试前检查 Mock 覆盖度，测试后同步 Mock 数据**（节点 M1/M2/M3）：agent 在测试流程中必须自动执行，无需用户额外指示

## 关联文档

- `modules/test-case.md` 规则 T-2 — Mock 200 响应示例真实性（判定标准与修复路径）
- `modules/project-onboarding-checklist.md` 节点 2 → A6 — Mock 200 响应示例真实性（硬动作级）
- `modules/project-onboarding-checklist.md` 新增节点 M1/M2/M3 — Mock 自动同步（硬动作级）
- `modules/testing-pitfalls.md` — 排查"接口返回 404"时先查 Mock 是否缺失
- `modules/environment.md` — 环境变量影响 Mock 行为（如 baseUrl 不对导致 Mock 服务不可达）
- `modules/api-design.md` — 接口 schema 变更后触发的 Mock 同步检查