# 测试用例生成方法论（吸收自 API 测试类 skill）

> 归属 owner：`apifox`。本模块用于从接口定义（OpenAPI/Swagger/现有 endpoint）**系统化生成完善测试用例**，并在 apifox 中真实创建、运行、通过。吸收来源：API测试自动化专家版 / API接口测试管理器 / 测试用例生成器（SkillHub 生态）的方法论精华；落地为 apifox CLI 可执行流程。与 `modules/test-case.md` 的关系：后者负责 apifox 命令操作细节（categoryId、处理器、断言字段），本模块负责"测什么、怎么设计用例"的方法论，两者配合使用。

## 何时加载

- 用户要求"为接口/项目补全测试用例""生成测试用例""完善测试""测登录/注册/CRUD""补边界值用例"
- 已导入 OpenAPI 或已有 endpoint，需要把接口定义转化为完整测试覆盖
- 需要从需求文档/API 规范生成结构化测试用例
- 目标：**让 apifox 有完整接口 + 完整测试用例，且真实测试通过**（供同事对接）

---

## ⚡ 默认菜单与覆盖度铁律（强制，最高优先级）

### 规则 A：默认入口是「自动化测试」菜单

- 用户在 apifox 客户端看到的用例分类菜单有：**正向 / 负向 / 边界值 / 安全性 / 其他**
- "自动化测试"是指 apifox 项目侧用于跑用例的环境/套件入口，不要误以为是"自动化生成"
- 本 skill 生成的用例**默认归类**遵循上述五类（其中"安全性"对应鉴权/权限相关用例）
- 用户提到的"自动化测试"默认指这套菜单下的用例运行与管理；用例运行入口见 `modules/test-automation.md`

### 规则 B：覆盖度铁律 — 每个接口必须有 正向 + 负向 + 边界值 三类

> **现状问题（用户已指明）**：当前项目很多接口只有 1 个正向用例，且这个正向用例只测了分页参数（pageSize/pageIndex），其他 Query/Body 参数没有任何用例。POST 接口则完全没有用例。
>
> 这种现状**视为严重覆盖缺口**，必须主动补全。新生成的用例集必须满足：

| 维度 | 最低要求 | 不达标处理 |
|------|----------|-----------|
| 正向 | 每个接口 ≥ 1 个，覆盖**全部主要参数**（不是仅分页） | 缺则补 |
| 负向 | 每个接口 ≥ 1 个，覆盖必填缺失/参数错误/无权限/不存在 等 | 缺则补 |
| 边界值 | 每个有界字段 ≥ 1 个边界用例（min / max / 空 / 超长 / 0 / 负数） | 缺则补 |
| 安全性（可选） | 有 securityScheme 时强制（无 Token / 过期 / 权限不足） | 有鉴权接口必加 |

> **项目落地**：本规则同步写入项目根 `PROJECT_TEST.md` 的「测试覆盖度铁律」节（模板见 `references/project-test-md-template.md`），保证无 skill 环境（纯 Codex/Claude）也能读到该规则。

### 规则 C：POST 接口铁律 — 任何方法 ≠ GET 都必须有完整用例

- 现状截图证据：POST 请求普遍没有任何用例
- 任何 `POST / PUT / PATCH / DELETE` 接口**禁止**只为空，必须补齐至少 正向 + 负向 + 边界值 三类，且正向上必须覆盖完整 requestBody（不是只测一个空对象）
- 创建类接口（POST）的负向用例重点：缺失必填字段 / 字段类型错误 / 字段超长 / 唯一键冲突 / 业务校验失败

### 规则 D：补全前先评估覆盖缺口，再生成

- 进入"补全/完善测试"任务时，**第一步不是直接 create**，而是先列出覆盖矩阵：

  | 接口 | 方法 | 现有 正向 | 现有 负向 | 现有 边界值 | 计划补 |
  |------|------|-----------|-----------|-------------|--------|
  | /api/v1/exchangeOrder (GET) | GET | 1（仅分页） | 0 | 0 | +2 负向 +3 边界值 + 扩参数正向 |
  | /api/v1/exchangeOrder (POST) | POST | 0 | 0 | 0 | +1 正向（完整 body） +3 负向 +2 边界值 |

- 让用户看到缺口，再开干；用户同意后逐个创建
- 用户没看到缺口就直接创建，容易后续返工

### 规则 E：扩"正向"用例必须包含**非分页参数**

- 「正向」用例不等同于「分页正向」；任何有 Query/Body 参数的接口，正向用例集必须覆盖关键业务参数的全部组合（不只是 page=1&size=10）
- 判定准则：用户能用正向用例看到接口在"正确业务输入"下的真实响应 → 才是合格正向

---

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
| **正向（正常请求）** | 验证功能正确 | 用 schema 合法值，断言 2xx + 关键响应字段；**正向必须覆盖全部关键参数，不能只测分页** |
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

从 `responses` 各状态码 schema 生成断言。**断言字段命名与映射速查不在此重复**，统一遵循 `modules/test-case.md` 的「断言速查（16 种映射）」与「断言顺序（强制）」：`httpCode` / `responseJson` / `responseText`，比较符用 `equal`，先状态码 → 再业务码 → 后关键字段。此处只补充生成时的覆盖原则：

- 每个状态码至少对应 1 条断言（2xx 断业务码 + 关键字段，4xx/5xx 断错误结构非空）
- 响应体有 schema 时，对 `required` 字段逐个断言存在/非空
- 时间戳/数值精度等无法用可视化断言覆盖的，用自定义脚本兜底

### Step 4: apifox 落地（真实创建）

按 `modules/test-case.md` 的标准流程逐个创建：

1. `apifox test-case category --project <projectId>` 获取 `categoryId`
2. 建议按接口/模块建测试分类，正向/异常/边界用例分到同一接口下
3. `cli-schema get test-case-create` → 构造完整 JSON（含 requestBody、postProcessors、assertion）→ `cli-schema validate` → `create`
4. 创建后 `test-case get` 确认保存结构，再 `test-case run <caseId>` 运行

> ⚠️ Step 4 创建前必须先对照规则 B 的覆盖度铁律自检：当前接口的正/负/边界覆盖是否满足最低要求？POST 接口是否有完整用例？正向用例是否覆盖了非分页参数？**任一不满足则继续补，不要在缺口存在时宣称"用例已建好"。**

### Step 5: 真实测试通过（收口目标）

- 每个用例必须真实运行：`apifox run --test-case <caseId> --environment <env>` 或 `test-case run`
- 断言失败 → 检查是接口定义问题、环境问题还是用例问题；修到真实通过
- **"在 apifox 测试通过" = 用例在 apifox runner 中真实执行并全绿**，不是写完就收口
- **"覆盖达标" = 该接口在「自动化测试」菜单中能看到 正向 / 负向 / 边界值 三个分类下都有用例，且 POST 等非 GET 接口有完整覆盖**（校验基准：项目根 `PROJECT_TEST.md` 的「测试覆盖度铁律」节）
- 多接口编排 → `modules/test-scenario.md`；多用例回归 → `modules/test-automation.md`（test-suite + CI）

---

## 测试点分析（覆盖维度清单）

生成用例前按以下维度自查覆盖度，缺失维度补用例：

- **功能**：每个 operation 至少一个正向用例（**正向必须覆盖业务参数，不只是分页**）
- **异常**：每个 operation 的 4xx/5xx 分支
- **边界**：每个字段的 min/max/空/超长
- **认证**：无 Token/过期/权限不足/正确 Token
- **分页**：page/limit 边界、筛选保留（分页只是参数之一，不是接口的全部）
- **依赖**：CRUD 顺序、跨接口数据流（提取变量传递）
- **状态**：业务状态流转（创建→处理→完成）
- **方法全覆盖**：POST/PUT/PATCH/DELETE 必须有完整用例（≥ 正向 + 负向 + 边界值）
- **并发/性能**：见下

---

## 性能与契约测试

> 深度方法论已拆分至独立模块，此处仅保留映射指引，不再重复：
> - 性能测试（负载/压力/峰值/延迟、P50-P99 指标、apifox 落地）→ `modules/test-performance.md`
> - 契约测试（Schema 校验、变化检测、结构断言用例）→ `modules/test-contract.md`
> - 用例生成前如需陷阱自查/失败排查 → `modules/testing-pitfalls.md`

## 常见恢复

| 现象 | 处理 |
|------|------|
| 用户报"apifox 用例太少/全是正向" | 直接套规则 B/C/D：先列出覆盖矩阵让用户确认缺口，再补三类 |
| 生成的用例太多/太少 | 按"每接口 ≥3 类用例"校准，检查 schema 是否完整 |
| 用例运行失败但接口正常 | 检查环境/变量/前置数据，`test-case get` 看真实保存结构 |
| 断言不生效 | 对照 `modules/test-case.md` 断言规则检查字段命名 |
| 数据依赖（先建后查） | 用 extractor 提取变量（shareScope=PROJECT）+ test-scenario 编排 |
| 接口信息不完整 | 先回 `modules/import-export.md` 补 spec，再生成用例 |
