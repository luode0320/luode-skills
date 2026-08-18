# 测试用例生成方法论（吸收自 API 测试类 skill）

> 归属 owner：`apifox`。本模块用于从接口定义（OpenAPI/Swagger/现有 endpoint）**系统化生成完善测试用例**，并在 apifox 中真实创建、运行、通过。吸收来源：API测试自动化专家版 / API接口测试管理器 / 测试用例生成器（SkillHub 生态）的方法论精华；落地为 apifox CLI 可执行流程。与 `modules/test-case.md` 的关系：后者负责 apifox 命令操作细节（categoryId、处理器、断言字段），本模块负责"测什么、怎么设计用例"的方法论，两者配合使用。

## 何时加载

- 用户要求"为接口/项目补全测试用例""生成测试用例""完善测试""测登录/注册/CRUD"
- 已导入 OpenAPI 或已有 endpoint，需要把接口定义转化为完整测试覆盖
- 需要从需求文档/API 规范生成结构化测试用例
- 目标：**让 apifox 有完整接口 + 完整测试用例，且真实测试通过**（供同事对接）

## 核心流程：OpenAPI/接口定义 → 三类用例 → apifox 落地

### Step 1: 获取接口定义（完善接口信息）

- 已有 spec：`apifox import --project <projectId> --format openapi --file <spec>`（详见 `modules/import-export.md`，导入前必须跑质量指标）
- 无 spec：`apifox endpoint list/get` 拉取现有接口，确认 method/path/params/requestBody/schema
- 不完整时：先按 `modules/import-export.md` 的质量指标判断（paths/operations/schemas/withBody/emptyObjectBodies），缺什么补什么
- 接口信息完善是测试用例的前提：**schema 不完整 → 测试用例必然不完整**

### Step 2: 按三类意图生成用例（核心）

每个接口至少覆盖三类用例，缺一类视为覆盖缺口：

| 意图 | 目标 | 用例设计 |
|------|------|----------|
| **正向（正常请求）** | 验证功能正确 | 用 schema 合法值，断言 2xx + 关键响应字段 |
| **异常（参数错误/鉴权失败）** | 验证错误处理 | 缺失必填、类型错误、无效枚举、未授权、未找到，断言 400/401/403/404 + 错误结构 |
| **边界（最小/最大/空/超长）** | 验证边界约束 | min/max、minLength/maxLength、空字符串、超长字符串、null、0、负数、空数组 |

**schema 驱动数据构造规则**（根据字段定义推断测试数据）：

| schema 字段 | 正向值 | 边界值 | 异常值 |
|-------------|--------|--------|--------|
| `required` | 全填 | 逐个缺失必填字段 | 缺一个必填 → 400 |
| `type: string` + `minLength/maxLength` | 合法长度 | 恰好 min/max、空串 | 超 maxLength、非字符串 |
| `type: integer` + `minimum/maximum` | 区间内 | 恰好 min/max、0、负数 | 超区间、非数字、字符串数字 |
| `enum` | 每个枚举值 | 边界枚举 | 枚举外值 |
| `format: email/date-time/uuid` | 合法格式 | 边界格式 | 格式错误 |
| `example` | 用 example | 按约束变体 | 偏离 example |
| 数组 | 1-2 个元素 | 空数组、单元素 | 超长数组、非数组 |
| 对象嵌套 | 合法嵌套 | 空对象 | 缺嵌套必填、类型错误 |

**认证场景**（有 securityScheme 时强制）：无 Token / Token 过期 / 权限不足 / 正确 Token。

**交叉与状态**：组合参数（两个字段联合约束）、分页场景（page/limit 边界、分页切换保筛选）、CRUD 流程依赖（先创建拿到 id → 查询/更新/删除）。

### Step 3: 生成断言模板（按响应 schema）

从 `responses` 各状态码 schema 生成断言：

| 断言对象 | apifox assertion 映射 |
|----------|----------------------|
| HTTP 状态码 | `httpCode` + `equal` |
| 响应头存在/值 | `responseHeader` |
| JSON 字段存在/值 | `responseJson` + path（如 `$.data.id`） |
| JSON Schema 结构 | 关键字段非空 + 类型断言 |
| 数值精度/时间戳格式 | `responseJson` + 自定义脚本兜底 |

> 断言字段命名遵循 `modules/test-case.md` 的断言规则：`httpCode`/`responseJson`/`responseText`，比较符用 `equal`。

### Step 4: apifox 落地（真实创建）

按 `modules/test-case.md` 的标准流程逐个创建：
1. `apifox test-case category --project <projectId>` 获取 `categoryId`
2. 建议按接口/模块建测试分类，正向/异常/边界用例分到同一接口下
3. `cli-schema get test-case-create` → 构造完整 JSON（含 requestBody、postProcessors、assertion）→ `cli-schema validate` → `create`
4. 创建后 `test-case get` 确认保存结构，再 `test-case run <caseId>` 运行

### Step 5: 真实测试通过（收口目标）

- 每个用例必须真实运行：`apifox run --test-case <caseId> --environment <env>` 或 `test-case run`
- 断言失败 → 检查是接口定义问题、环境问题还是用例问题；修到真实通过
- **"在 apifox 测试通过" = 用例在 apifox runner 中真实执行并全绿**，不是写完就收口
- 多接口编排 → `modules/test-scenario.md`；多用例回归 → `modules/test-automation.md`（test-suite + CI）

## 测试点分析（覆盖维度清单）

生成用例前按以下维度自查覆盖度，缺失维度补用例：

- **功能**：每个 operation 至少一个正向用例
- **异常**：每个 operation 的 4xx/5xx 分支
- **边界**：每个字段的 min/max/空/超长
- **认证**：无 Token/过期/权限不足/正确 Token
- **分页**：page/limit 边界、筛选保留
- **依赖**：CRUD 顺序、跨接口数据流（提取变量传递）
- **状态**：业务状态流转（创建→处理→完成）
- **并发/性能**：见下

## 性能测试（映射到 apifox）

apifox 通过 runner + 定时任务支撑性能类验证：

- 用例设计：关键接口的重复执行、多迭代（`apifox run --iteration`）
- 断言：响应时间阈值（自定义脚本断言 `pm.response.responseTime`）
- 回归：`test-suite` 定时执行（`scheduled-task`），对响应时间回归敏感
- 不做 JMeter 级压测，但覆盖"响应时间回归 + 高频调用稳定性"

## 契约测试（映射到 apifox）

契约测试 = 用接口定义约束请求/响应结构，防止前后端/跨团队漂移：

- apifox 中实践：为每个接口建立"结构断言"用例（响应 JSON Schema 关键字段 + 类型）
- 配合 `modules/import-export.md` 的 spec 质量指标：`schemas` 覆盖、`emptyObjectBodies` 风险
- 接口变更后重跑契约用例：字段缺失/类型变化 → 用例失败 → 暴露契约漂移
- 跨团队：apifox 项目即共享契约库，`import/export` 保持 spec 与实现同步

## 常见恢复

| 现象 | 处理 |
|------|------|
| 生成的用例太多/太少 | 按"每接口 ≥3 类用例"校准，检查 schema 是否完整 |
| 用例运行失败但接口正常 | 检查环境/变量/前置数据，`test-case get` 看真实保存结构 |
| 断言不生效 | 对照 `modules/test-case.md` 断言规则检查字段命名 |
| 数据依赖（先建后查） | 用 extractor 提取变量（shareScope=PROJECT）+ test-scenario 编排 |
| 接口信息不完整 | 先回 `modules/import-export.md` 补 spec，再生成用例 |
