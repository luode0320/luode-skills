# 环境与 Mock — environment / variables / mock / database-connection

> 本模块覆盖环境配置、变量管理、Mock 规则及数据库连接。已从 SKILL.md 继承：写入标准流程、分支参数规则。

## 何时加载

- 创建/更新/查询/删除环境
- 管理环境变量、全局变量
- 配置 Mock 规则/期望/智能 Mock
- 配置数据库连接

## 命令入口

```bash
apifox environment --help
apifox variables --help
apifox mock --help
apifox database-connection --help
```

具体参数以当前 CLI help 为准。

## 环境管理

```bash
# 列出项目环境
apifox environment list --project <projectId>

# 获取环境详情
apifox environment get <environmentId> --project <projectId>
```

- 创建/更新前先通过 `cli-schema get` 获取结构定义
- 敏感变量（token、密码等）不要在回复中展示

## Mock 配置

Mock 是独立于环境的功能，需要在接口层级配置 Mock 规则或期望。

- 先确认接口已有响应定义，再配置 Mock
- Mock 未配置可能导致接口测试返回 404 或异常响应
- 区分：接口测试失败 ≠ 接口定义未保存，也可能是 Mock/环境未配置

## 运行环境建议

- 运行测试时建议显式带 `--environment`
- CI 场景 token 通过 secret 注入，不要写入仓库

## 被测服务本地启动（强制）

接口级测试（功能验证/回归/Bug 验证/上线门禁的接口部分）默认以本地服务为被测对象。

### Apifox 三环境约定（开发/测试/正式）

Apifox 新建项目默认自带三个环境：**开发环境（Development）、测试环境（Test）、正式环境（Production）**。规则如下：

| 环境 | agent 是否可选 | baseUrl 约定 | 说明 |
|------|---------------|--------------|------|
| **开发环境（Development）** | ✅ **默认测试执行环境** | `http://127.0.0.1:<项目端口>` | API 调试与接口级测试的唯一允许环境，等同于"local" |
| 测试环境（Test） | ❌ **禁止选用** | 指向 test 服务 | 已存在但 agent 不得选择；仅由人/CI 使用 |
| 正式环境（Production） | ❌ **禁止选用** | 指向 prod 服务 | 已存在但 agent 不得选择；仅由人/CI 使用 |

- **开发环境即 local 环境**：baseUrl 固定指向 `http://127.0.0.1:<项目端口>`（或 `http://localhost:<port>`），环境名沿用 Apifox 自带的「开发环境」即可，无需改名为 local
- **测试/正式环境保留但不碰**：不删除、不修改、不选用；运行测试时显式 `--environment <开发环境Id>` 防止误选

### 默认创建/确认开发环境（强制）

新项目接入 apifox 或项目无可用开发环境时：

1. **先查**：`apifox environment list --project <projectId>` 列出项目环境
2. **已有「开发环境」** → 修改其 baseUrl 为 `http://127.0.0.1:<项目端口>`（若 baseUrl 已是本机地址则跳过）
3. **无「开发环境」** → **默认创建**：环境名「开发环境」，baseUrl 固定 `http://127.0.0.1:<项目端口>`
4. **登记环境 ID**：`apifox environment get <environmentId>` 取 ID，回填到项目根 `PROJECT_TEST.md` 的「本地测试环境」表（环境名/环境ID/baseUrl/端口），后续运行测试显式指定
5. **配置环境变量（强制）**：在测试流程中同步补齐开发环境所需的环境变量（详见下节「开发环境环境变量（强制）」），保证用例运行时签名、登录、鉴权参数齐备
6. `<项目端口>` 取项目后端本地启动端口（`config_local*`、docker-compose、启动脚本声明的端口）；项目端口未知时先查项目启动配置或询问用户，不要猜测
7. 测试前必须先确认被测服务已在本地启动且端口可访问（`curl http://127.0.0.1:<port>/health` 或等价可达检查）

### 开发环境环境变量（强制）

> 接口用例运行常依赖环境变量承载的鉴权/登录/签名参数。**开发环境创建或确认后，必须同步配置齐备的环境变量**，否则用例运行必失败（401/403/签名错误），再排查半天才发现是环境变量缺失。

**必须配置的变量类别**（按项目实际情况覆盖，缺一即视为开发环境未就绪）：

| 类别 | 典型变量 | 用途 |
|------|----------|------|
| **鉴权签名** | `apiKey` / `apiSecret` / `appId` / `nonce` / `signature` 等 | 请求头/参数签名（如 X-Api-Key、X-Signature、timestamp+sign），签名接口必需 |
| **默认测试登录** | `testUsername` / `testPassword`（或 `loginAccount` / `loginPwd`） | 登录接口取 token 用，登录后经 extractor 提取 token（`shareScope=PROJECT`）供后续用例；**测试默认用管理员账号**，权限最全 |
| **Token/会话** | `token`（登录后提取回写） | 鉴权头 `Authorization: Bearer {{token}}`；由登录用例 extractor 写入，不必手工填；**过期快时用前置脚本自动续期（见 `modules/test-auth.md` 方案 B）** |
| **登录地址** | `loginUrl` | 登录接口地址（如 `http://127.0.0.1:<端口>/api/v1/login`），供前置续期脚本调用 |
| **项目约定参数** | 租户 ID、商户号、环境标识等 | 业务请求的公共参数 |

**取值来源（强制）**：

- 签名密钥、登录账号密码等**只从项目 local 本地配置取**（`config_local*`、`.env.local`、`.env.development`、启动脚本），或由用户直接提供
- **禁止**从 test/prod/staging 配置取环境变量值（与本地环境红线一致）
- 项目 local 配置缺失时，询问用户提供，不要猜测或编造密钥

**敏感变量处理（强制）**：

- `apiSecret`、密码、token 等敏感变量**值不得回显**：不出现在回复、日志、聊天摘要、`PROJECT_TEST.md` 中
- `PROJECT_TEST.md` 只登记**变量名 + 用途 + 来源**，不登记值（见模板「环境变量登记」表）
- 值写入 apifox 环境变量时用 CLI 写入，避免中间输出暴露

**登记**：环境变量清单（名称/用途/来源）回填到项目根 `PROJECT_TEST.md` 的「环境变量登记」表，后续会话按表核对是否齐备。

**token 自动续期（强制，过期快的系统必读）**：token 过期快（分钟级/小时级）时，仅配置变量不够——必须在测试流程内**自动获取/续期**：登录用例 extractor 提取（方案 A）+ 前置脚本自动重登（方案 B，preProcessor customScript 检查 JWT exp 快过期则重登写回 token）+ 本地脚本构造（方案 C）+ 全局身份认证（方案 D）。完整方案、脚本模板与排查指引见 `modules/test-auth.md`。

### 运行环境红线

- 禁止新建指向 `test` / `prod` / `staging` / `pre` / `release` 的 environment，禁止把 baseUrl 指向非 local 服务（判定标准是配置归属，与 `test-strategy-rules` 的本地环境红线一致）
- 禁止选用项目已存在的「测试环境」「正式环境」执行接口级测试——即使它们 baseUrl 恰好指向本机，也以**环境名/配置归属**判定（`test`/`prod` 归属一律禁止）
- 运行测试显式带 `--environment <开发环境Id>`，避免默认环境漂移
- 数据构造仍从 local 数据库取真实样本（来源优先级见 `modules/test-data-and-judgement.md`），不得连非 local 服务取数

## 不可违反规则

1. 敏感变量（apiSecret/密码/token）值不要出现在最终回复、日志、聊天摘要或 `PROJECT_TEST.md` 中，只登记名称/用途/来源
2. 运行测试建议显式指定 `--environment`，避免默认环境变化
3. 不要在未确认环境的情况下执行有副作用的操作
4. 接口级测试 environment 只允许指向**开发环境**（baseUrl `http://127.0.0.1:<项目端口>`），禁止选用「测试环境」「正式环境」及任何非 local 服务
5. 项目无可用开发环境时必须**默认创建**（baseUrl `http://127.0.0.1:<项目端口>`），不得改用其他环境替代
6. 项目已存在的「测试环境」「正式环境」保留不碰：不删除、不修改、不选用
7. 开发环境必须**配置齐备环境变量**（鉴权签名 apiKey/apiSecret、默认测试登录账号密码等），缺失即视为开发环境未就绪，用例运行失败先查环境变量而非只查接口
8. 环境变量取值只从 local 本地配置或用户提供，禁止从 test/prod/staging 配置取
