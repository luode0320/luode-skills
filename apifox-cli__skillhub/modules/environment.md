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

### Apifox 本地测试配置（config/yaml/config.apifox.yaml，强制）

> 本地接口测试的**服务侧配置统一来源**是项目 `config/yaml/config.apifox.yaml`（同仓后端 `backend/config/yaml/config.apifox.yaml`），被测服务以 `-env apifox` 启动加载它；不再散读 `config_local*` / `.env.local` 猜测端口与数据源。

- **生成规则**：项目无 `config.apifox.yaml` 时，从 `config.local.yaml` **复制**生成，业务配置保持一致；生成前先确认，生成后登记到 `PROJECT_TEST.md`「本地测试环境」表。
- **数据库分离（强制阻断）**：`config.apifox.yaml` 的 MySQL 数据库必须使用**独立的 apifox 测试专用库**，**库名约定为 `apifox`，由开发人员手动创建并配置**。配置后必须先校验：**apifox 库名与 `config.local.yaml` 的库名相同 → 阻断**测试流程，等待用户部署 apifox 测试专用库并回填配置后再继续；禁止用 local 同一库跑接口测试（会污染本地开发数据）。
- **数据基准（local → apifox，强制）**：apifox 测试专用库是独立新库，**以 local 数据库数据为基准**——local 库通常同步正式环境线上数据（测试更准确）；「默认 apifox 环境」仅指被测服务启动环境，**不代表禁止使用 local 配置/数据**。**apifox 库无数据且 local 库有数据 → 优先从 local 库单向灌数据到 apifox 测试库**（默认路径，不限于旧接口）；**apifox 与 local 都无数据 → apifox 自行创造测试数据**。local 库只读源（仅 SELECT）、脱敏、记录来源/条数/时间，见 `modules/test-data-and-judgement.md`；**禁止反向回灌**，禁止从 test/prod/staging 取数灌入。
- **临时库特权（apifox 环境可自建，强制）**：**前提是项目已提供 apifox 环境配置**（有 `config/yaml/config.apifox.yaml` + 对应 apifox 测试专用库）。模型测试需要**宽泛权限**（建表/复杂数据构造/大范围写操作等超出 apifox 专用库约束的场景）时，**允许 apifox 环境自行新建临时库测试使用**：
  - **命名标识（强制）**：临时库名必须以 **`tmp` 前缀**标识（如 `tmp_<测试用途>`），用于与正常库区分；非 `tmp` 前缀的库一律视为正常库。
  - **生命周期（建→用→删，强制）**：临时库**测试完成后必须删除**（`DROP DATABASE` 清理），不得遗留；删除动作记录到 `PROJECT_TEST.md`（库名/用途/删除时间）。
  - **删除边界（强制）**：只有 **`tmp` 前缀的临时库**允许删除；**正常库（非 `tmp` 前缀，含 apifox 测试专用库、local 库）一律不允许删除**——即使 apifox 环境具备连接权限，也不得删除正常库。
  - 与库分离不冲突：库分离管「apifox 专用库 ≠ local 库」；临时库是在 apifox 专用库之外**额外创建的生命周期库**，用完即删，不影响 apifox 库与 local 库。
- 端口探测、环境变量取值、数据源连接均以 `config.apifox.yaml` 为准；`test` / `prod` / `staging` 配置一律不用于本地测试（环境红线不变）。
- **环境选择（强制，优先级默认值）**：模型测试/接口级测试的**默认启动环境按项目配置决定**——项目**存在 `config/yaml/config.apifox.yaml`（含同仓 `backend/config/yaml/config.apifox.yaml`）时默认使用 `apifox` 环境**（被测服务 `-env apifox` 启动）；项目**没有 apifox 环境配置时默认使用 `local` 环境**（`config.local.yaml`）；除 `local` 与 `apifox` 之外的环境（`test` / `prod` / `staging` / `pre` / `release` 等）**一律禁止**用于被测服务启动与测试执行。
- apifox 环境属接口测试专用，与 `local`/`test`/`prod` 既有语义无关；目录树落点见 `package-structure-rules/references/configuration-layout.md`。

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
6. `<项目端口>` 按「本地服务端口探测（强制）」三级链确定（见下节），**以实际监听端口为最终裁决**，禁止凭 `PROJECT_TEST.md` 静态登记值直接开测
7. 测试前必须先确认被测服务已在本地启动且端口可访问（`curl http://127.0.0.1:<port>/health` 或等价可达检查）；连接拒绝（ECONNREFUSED）时按三级链重新探测真实端口并纠偏，不要在原端口上硬跑

### 硬动作 A2：创建/更新开发环境后立即探测端口（强制）

> 把端口三级链从"测试前"前置到"创建/更新环境时立即执行"——环境刚建好端口就错会导致后续所有用例必然失败，等到测试时才发现代价高。如图 5 显示的「环境 baseUrl 是 `127.0.0.1:18080` 与实际后端端口不一致」即为典型反面案例。

**触发时机**：

- **创建开发环境后立即**（步骤 3 默认创建 / 项目接入 apifox 第一次配置）
- **更新开发环境 baseUrl 时立即**
- **项目交付/调试切换不同服务实例时**

**执行命令**：按下节「本地服务端口探测（强制）」的三级链逐级执行（L1 读启动配置声明 → L2 实测监听端口 → L3 登记值兜底），命令与平台差异不在本节重复。

**通过标准**：L2 探测到的实际监听端口（必须属于本项目后端服务）→ 与计划写入 apifox「开发环境」的 baseUrl 端口一致。

**不通过则必须纠偏**（用户已确认"自动纠偏+回写"）：

- 探测到的真实端口 ≠ 准备写入 baseUrl 的端口 → 自动更新 apifox「开发环境」baseUrl + 回写 `PROJECT_TEST.md`「本地测试环境」表「项目端口」列 + 在回复中说明依据（如 `ss -tlnp` 输出）
- 纠偏后必须重跑端口可达检查（`curl http://127.0.0.1:<新端口>/health`）确认通
- 全部探测不到本项目服务 → 判定「服务未启动」：先启动本地服务再配环境，不要在错端口上硬跑

**WSL2 跨系统适配**：地址路径按上「WSL2 跨系统网络访问（环境适配）」小节表（WSL 内用 `127.0.0.1` / Windows 访问 WSL 用 `localhost` 或 WSL IP / WSL 访问宿主用网关 IP 或 `host.docker.internal`）。

**批量修复**：见 `project-onboarding-checklist.md` 「现有项目批量修复命令集」第 6 项。

### 本地服务端口探测（强制）

> `<项目端口>` 不能靠猜、也不能靠静态登记值。测试执行前必须按三级链确认**实际监听端口**；登记值与实际不一致时自动纠偏，否则测试必然不通或连错服务。

**三级探测链（逐级推进，实际监听为最终裁决）**：

| 级别 | 探测方式 | 说明 |
|------|----------|------|
| L1 启动配置声明 | 读 `config/yaml/config.apifox.yaml`（本地接口测试专用配置，优先）、`config_local*`、docker-compose、启动脚本（Makefile / package.json scripts / run.sh 等）中的端口声明 | 给出期望端口与端口名（如 backend/8000），作为第一候选 |
| L2 实际监听探测 | `ss -tlnp`（Linux/WSL）/ `netstat -ano \| findstr LISTENING`（Windows）/ `lsof -iTCP -sTCP:LISTEN`（macOS），按进程名/项目名/端口名过滤 | 找出**真实 LISTEN 端口**；同一进程监听多个端口时按 L1 声明优先匹配 |
| L3 已登记值兜底 | 项目根 `PROJECT_TEST.md`「本地测试环境」表登记的端口 | 仅作参考，**必须经 L2 验证**后才能用 |

**执行规则（强制）**：

1. 先按 L1 找声明端口 → 按 L2 验证该端口是否真实在听
2. L2 验证通过 → 以该端口为准；与 `PROJECT_TEST.md` 登记值一致则继续，不一致则走纠偏闭环
3. L1 无声明或 L2 探测不到 → 全量扫 LISTEN 端口（`ss -tlnp` / `netstat -ano`），按进程名/项目名归属被测服务
4. 全部探测不到被测服务 → 判定「服务未启动」：先启动本地服务再测，**不要改端口硬试**
5. 同一机器跑多个项目/多实例时，以**进程归属**（进程名/工作目录/启动参数）区分服务，不凭端口号猜测

**纠偏闭环（自动，强制）**：

- 实际监听端口 ≠ `PROJECT_TEST.md` 登记端口时：
  1. 更新 apifox「开发环境」baseUrl 为 `http://127.0.0.1:<实际端口>`
  2. 回写 `PROJECT_TEST.md`「本地测试环境」表「项目端口」列，更新登记时间
  3. 回复中说明「端口由 <旧值> 纠偏为 <新值>（依据：<探测证据，如 ss -tlnp 输出>）」
- **端口可达 ≠ 端口正确**：curl 通了但响应与预期不符（404/网关/像是别的服务），也要回到 L2 验证端口归属，确认端口上确实是本项目服务再测
- 纠偏后仍不通 → 按「WSL2 跨系统网络访问（环境适配）」（见下节）检查地址路径，不要只怀疑端口

### 服务重启与关停核验（强制）

> 规则权威在 `test-strategy-rules`「项目联调条件化规则」——联调启动的进程完成后必须关闭并核验进程状态。本节只补 apifox 域的执行细节：**为什么"重启过了"经常是假的**。
>
> 反面案例（2026-08-21 实测）：改完配置重启服务，端口照样通、10 个用例照样全绿，但改动其实**一次都没生效**——旧实例始终在跑。`go run main.go -env apifox` 的真实进程是编译产物 `/tmp/go-build*/exe/main -env apifox`，`pkill -f 'main.go -env apifox'` 只杀掉 `go run` 父进程，端口仍被子进程占用；新实例启动即 `bind: address already in use` 后退出，而日志在后台文件里没人看。用例之所以能读到新数据，是因为服务端缓存 TTL 到期自动回库，与"重启"毫无关系。

**包装式启动会派生子进程**——杀父进程不释放端口。常见形态：

| 启动方式 | 真实进程 | 只杀父进程的后果 |
|----------|----------|------------------|
| `go run main.go` | `/tmp/go-build*/exe/main` | 端口不释放，新实例静默退出 |
| `npm run dev` / `nodemon` | `node <entry>` | 同上 |
| `python -m uvicorn` / `--reload` | worker 子进程 | 同上 |
| `mvn spring-boot:run` | `java -jar` fork | 同上 |

**关停三步（缺一不可）**：

1. **按真实进程名结束**：`pkill -f '[e]xe/main -env apifox'`（方括号写法避免 pkill 匹配到执行它的 shell 自身）；拿不准就先 `ps -eo pid,cmd | grep <关键字>` 看真实命令行，或按端口反查 PID（`ss -tlnp | grep :<port>`）
2. **核验端口无监听**：`ss -tln | grep -E ':<主端口>|:<调试端口>'` 无输出（别漏掉 pprof / debug / metrics 等副端口，它们同样会让新实例启动失败）
3. **核验无残留进程**：`ps -eo pid,cmd | grep <关键字>` 无输出

**重启后必须验证改动真的生效**，不能只看"端口通了"：

- 看启动日志有没有 `address already in use`、`exit status 1`（后台启动时日志在重定向文件里，必须主动 `tail`）
- 端口上的 PID 是否是新进程（重启前后 PID 必须变化）
- 至少跑一个能体现本次改动的请求，确认响应符合新行为——若响应变化可以用缓存过期解释，就还不能算重启已生效（见 `modules/testing-pitfalls.md` 陷阱 18-1）

### WSL2 跨系统网络访问（环境适配）

> WSL2 默认 NAT 网络下，`127.0.0.1` 只在单侧系统内自洽，跨系统（WSL ⇄ Windows 宿主）访问需按服务所在侧选择地址。apifox CLI 只是 HTTP 客户端，**跑在能直连被测服务的一侧**，不要从不可达侧硬跑再怀疑端口。

| 被测服务所在侧 | 从哪侧访问 | 可用地址 | 说明 |
|------|-----------|----------|------|
| WSL 内（如 `/home/luode/code/...`） | WSL 内跑 apifox CLI | `http://127.0.0.1:<端口>` | 同系统内直连，最稳，优先 |
| WSL 内 | Windows 侧跑 apifox CLI | `http://localhost:<端口>`（WSL 新版 localhost forwarding 自动转发）或 WSL IP（`wsl hostname -I`） | localhost forwarding 未生效时改用 WSL IP |
| Windows 宿主 | WSL 内跑 apifox CLI | `http://<网关 IP>:<端口>`（`ip route show \| grep default` 取网关）或 `http://host.docker.internal:<端口>` | WSL2 NAT 下不能从 WSL 直连宿主 `127.0.0.1` |

- **判定顺序**：先确认被测服务在哪一侧启动（`ss -tlnp` / `netstat` 查监听），再选对应地址；地址不通按上表换地址，**不要无脑改端口**
- apifox「开发环境」baseUrl 填「能直连被测服务的地址」（= 端口探测结果 + 上表地址路径），环境仍只允许 local

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

- 签名密钥、登录账号密码等**只从项目本地测试配置取**：优先 `config/yaml/config.apifox.yaml`（本地接口测试专用配置，无则从 `config.local.yaml` 复制生成），其次 `config_local*`、`.env.local`、`.env.development`、启动脚本，或由用户直接提供
- **禁止**从 test/prod/staging 配置取环境变量值（与本地环境红线一致）
- 项目 local 配置缺失时，询问用户提供，不要猜测或编造密钥

**敏感变量处理（强制）**：

- `apiSecret`、密码、token 等敏感变量**值不得回显**：不出现在回复、日志、聊天摘要、`PROJECT_TEST.md` 中
- `PROJECT_TEST.md` 只登记**变量名 + 用途 + 来源**，不登记值（见模板「环境变量登记」表）
- **值由用户在 apifox 客户端自行填入，agent 不代填**（把密钥/token 输入任何字段属禁止操作，apifox 又是云端 SaaS）。agent 只负责：向用户说明需要哪个变量名与用途、在用例里写好运行时取值的脚本（`pm.environment.get("<变量名>")`）、把变量名登记进 `PROJECT_TEST.md`
- **CLI 读写不到环境变量（2026-08-21 实测 apifox-cli 2.2.9）**：`environment get` 只返回 `id/name/projectId/baseUrls/parameters`；带 `variables` 的 `environment update` 会返回 `success=true` 但回读恒为 `null`。所以不要试图用 CLI 建变量或核对变量是否已填，也不要因为回读为空就反复重试；以"是否有人在客户端填过"为事实来源（详见 `modules/test-auth.md`「两条 CLI 事实」）

**登记**：环境变量清单（名称/用途/来源）回填到项目根 `PROJECT_TEST.md` 的「环境变量登记」表，后续会话按表核对是否齐备。

**token 自动续期（强制，过期快的系统必读）**：token 过期快（分钟级/小时级）时，仅配置变量不够——必须在测试流程内**自动获取/续期**：登录用例 extractor 提取（方案 A）+ 前置脚本自动重登（方案 B，preProcessor customScript 检查 JWT exp 快过期则重登写回 token）+ 本地脚本构造（方案 C）+ 全局身份认证（方案 D）。完整方案、脚本模板与排查指引见 `modules/test-auth.md`。

### 运行环境红线

- **被测服务 environment 白名单只允许 `local` 与 `apifox`**，**选择优先级按项目配置决定**：项目有 `config/yaml/config.apifox.yaml` 配置 → **默认使用 `apifox` 环境**（`-env apifox` 启动）；无 apifox 环境配置 → 使用 `local`；`test` / `prod` / `staging` / `pre` / `release` 一律禁止
- 禁止新建指向 `test` / `prod` / `staging` / `pre` / `release` 的 environment，禁止把 baseUrl 指向非 local 服务（判定标准是配置归属，与 `test-strategy-rules` 的本地环境红线一致）
- 禁止选用项目已存在的「测试环境」「正式环境」执行接口级测试——即使它们 baseUrl 恰好指向本机，也以**环境名/配置归属**判定（`test`/`prod` 归属一律禁止）
- 运行测试显式带 `--environment <开发环境Id>`，避免默认环境漂移
- 数据构造以 **local 数据库为数据基准**（来源优先级见 `modules/test-data-and-judgement.md`）：**apifox 库无数据且 local 有 → 优先从 local 库单向灌数据到 apifox 测试库**（local 只读源、脱敏、可追溯）；**apifox 与 local 都无数据 → apifox 自造测试数据**；不得连非 local 服务取数
- **临时库特权（apifox 环境，强制）**：仅当项目已有 apifox 环境配置时，模型测试宽权限场景允许 apifox 环境自建 `tmp` 前缀临时库，**测试完成必须删除**；正常库（非 `tmp` 前缀，含 apifox 库/local 库）**禁止删除**（见「Apifox 本地测试配置」节）

## 不可违反规则

1. 敏感变量（apiSecret/密码/token）值不要出现在最终回复、日志、聊天摘要或 `PROJECT_TEST.md` 中，只登记名称/用途/来源
2. 运行测试建议显式指定 `--environment`，避免默认环境变化
3. 不要在未确认环境的情况下执行有副作用的操作
4. 接口级测试 environment 只允许指向**开发环境**（baseUrl `http://127.0.0.1:<项目端口>`），禁止选用「测试环境」「正式环境」及任何非 local 服务
5. 项目无可用开发环境时必须**默认创建**（baseUrl `http://127.0.0.1:<项目端口>`），不得改用其他环境替代
6. 项目已存在的「测试环境」「正式环境」保留不碰：不删除、不修改、不选用
7. 开发环境必须**配置齐备环境变量**（鉴权签名 apiKey/apiSecret、默认测试登录账号密码等），缺失即视为开发环境未就绪，用例运行失败先查环境变量而非只查接口；变量值由用户在客户端填入，**agent 不代填、也不能用 CLI 读写变量**（CLI 无此能力）
8. 环境变量取值只从 local 本地配置或用户提供，禁止从 test/prod/staging 配置取
9. 测试前必须按「本地服务端口探测」三级链验证**实际监听端口**，禁止直接使用 `PROJECT_TEST.md` 静态登记端口开测
10. 登记端口与实际监听端口不一致时**必须自动纠偏**（更新 apifox 开发环境 baseUrl + 回写 `PROJECT_TEST.md`），不得带错端口继续测试
11. 端口可达 ≠ 端口正确：curl 通过但响应不像本项目服务时，必须回到监听探测验证端口归属
12. 被测服务以 `config/yaml/config.apifox.yaml` 启动（无则从 `config.local.yaml` 复制生成）；**apifox 的 MySQL 库名约定为 `apifox`（开发人员手动创建配置），与 `config.local.yaml` 相同必须阻断**，等用户部署 apifox 测试专用库后再继续，禁止用 local 同一库跑接口测试
13. 被测服务 environment 白名单只允许 `local` 与 `apifox`，**选择优先级按项目配置决定**：项目有 `config/yaml/config.apifox.yaml` 配置 → 默认使用 `apifox` 环境（`-env apifox` 启动）；无 apifox 环境配置 → 使用 `local`；禁止使用 `test` / `prod` / `staging` / `pre` / `release` 等非 local 环境启动被测服务或执行测试
14. 数据准备以 **local 库为数据基准**：**apifox 库无数据且 local 有数据 → 优先从 local 单向灌入 apifox 测试库**；**apifox 与 local 都无数据 → apifox 自行创造测试数据**；local 库只读（仅 SELECT，禁止写入/删除），禁止反向回灌，禁止从 test/prod/staging 取数灌入；灌入数据必须脱敏并记录来源库/表、条数、时间
15. 重启或关停被测服务必须按「服务重启与关停核验」三步核验（真实进程名结束 → 端口含副端口无监听 → 无残留进程），并确认改动真的生效；**"端口通了"不等于"新实例在跑"**，包装式启动（`go run` / `nodemon` / `--reload` / `mvn spring-boot:run`）杀父进程不释放端口，用例照样能全绿却测的是旧实例
16. **临时库特权只属于 apifox 环境且必须满足前提**：项目已有 apifox 环境配置（`config/yaml/config.apifox.yaml` + apifox 测试专用库）时，模型测试宽权限场景允许自建 **`tmp` 前缀**临时库，**测试完成后必须删除**；**正常库（非 `tmp` 前缀，含 apifox 测试专用库与 local 库）一律禁止删除**，不得以「有连接权限」「测试需要」为由删除正常库
