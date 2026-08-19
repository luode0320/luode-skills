---
name: test-strategy-rules
description: 当准备进入测试阶段需要确定测试策略、优先级、覆盖范围和待补测风险时触发；当新增或修改测试主文档、验证说明、测试报告、覆盖说明、执行记录，确定根 `test/` 测试代码镜像、`doc/5-tests/` 时间戳测试主文档，或发现测试脚本、fixture、测试 Mock、数据和说明散落时，也自动进入本 owner 的 `test-asset-governance` 条件路由。当本轮新增或修改生产代码、准备为可测性在生产文件中加函数/静态数据/字段/分支/第二构造器，或发现生产符号只被 `test/` 引用时，进入生产代码测试污染判定：完全禁止为测试改动生产代码，按引用面判据判定并由 `scripts/scan_test_pollution.py` 硬阻断，豁免须显式登记。当测试对象是 HTTP 接口（有 method+path，经 HTTP 协议调用）需要执行接口级测试（功能验证、回归、Bug 接口验证、上线门禁的接口部分）时，进入「接口测试执行通道（强制）」：统一走 apifox 测试链路真实测试并落地测试用例到 apifox「AI 团队」对应项目，environment 只允许指向 local（localhost），单元测试/代码级测试保留本地。负责测试策略与测试资产治理的统一主入口，必须以 `artifact-storage-rules` 为中央路径真相，并保留本地环境红线、生产代码不污染、Go 可编译路径和 artifact gate 约束；不要用它代替具体测试程序、功能验证或回归验证。
---

# 测试策略规则

只在需要先回答“这次应该如何设计测试策略”时使用这个 skill。
如果当前已经明确在做功能验证、联调或回归验证，请转交对应测试域 skill；如果只是测试目录、命名、程序或文档问题，请转交测试资源管理类 skill。

## 测试代码与证据双根

- 活动测试代码、mock、stub、fake、fixture、helper 和数据构造只在根 `test/`；源码关联资产必须按被测源码目录镜像，只有跨源码复用资产才进入 `test/shared/`；Python 测试为 `*_test.py`，模拟程序使用 `_mock`、`_stub` 或 `_fake` 后缀。
- `doc/5-tests/` 只保留扁平测试主文档，日志、报告、截图和非可执行证据全部内联进正文；不得新增测试程序或 mock/stub/fake，历史可执行资产按指纹只读，首次修改时迁至 `test/`。
- Go 测试只在根 `test/` 的 ASCII 外部黑盒包中，源码目录不允许 `*_test.go`。

## 测试隔离红线（强制）

> 本节是测试域「测试隔离红线」的单一权威来源。`test-program-rules`、`test-regression-rules`、`functional-validation-rules` 等测试 skill 直接引用本节，不再重复定义，各自只保留本域专属补充（如功能验证的真实运行验证声明）。

- **完全禁止为测试目的改动生产代码**，包括新增测试专用方法、测试专用数据、测试专用结构体字段、仅测试可达分支和测试专用构造器。测试只能验证生产本来就有、生产路径本来就在用的能力。
- 判定采用**引用面判据**，不看写代码时的意图：生产目录中的符号，若全部非定义引用都来自 `test/` 且生产引用数为 0，即判定为测试污染。“将来生产也会用”“这是通用初始化能力”不构成放行理由。
- 五类污染模式（测试专用函数、测试专用静态数据、测试专用字段、仅测试可达分支、测试专用构造器）、Go 正反例、级联污染、白盒不可测的三级替代出路、生产重构的合法条件、豁免登记与存量治理四步，统一见 `references/production-test-pollution.md`。
- 测试辅助能力必须通过根 `test/` 内的脚本、mock、stub、fake、fixture 和数据构造解决，禁止向生产实现注入“仅测试可用”的业务代码，也不得以补 seam 为名在生产代码开测试专用入口。
- 一旦发现污染生产代码的测试改动，立即阻断并回退该改动，再继续后续测试。
- 测试策略只定义验证路径和优先级，不允许把“修改生产代码以便更好测试”纳入策略选项。
- 若某策略依赖生产代码测试污染才能成立，必须直接驳回该策略并改为测试资产侧方案。

### 污染扫描（硬阻断）

本轮存在生产代码新增或修改时，收口前必须执行扫描并消费其结论：

```bash
python test-strategy-rules/scripts/scan_test_pollution.py --root . --diff-only
```

- `POLLUTION: PASS`（退出码 0）：放行。
- `POLLUTION: FAIL`（退出码 1）：**阻断收口**，必须先按 `references/production-test-pollution.md` 的治理四步迁移到 `test/`，或在项目根 `.test-pollution-allowlist` 登记豁免并写明理由；不得以“下次再改”“不影响功能”跳过。
- `SUSPECT` / `ORPHAN` 为提示级，不阻断，交 `6-review` 判断。
- 存量治理用全量扫描（去掉 `--diff-only`）；脚本只提供引用面证据，最终裁决仍由模型判断并在归属不清时向用户确认。
- 当前仓库所有自动化测试、运行时调试、启动联调和本地查询默认都属于**本地测试**：只能使用 `local` 环境信息、`config_local*` / `.env.local` / `.env.development` / 本地开发配置中的连接信息执行验证；禁止改动 `test` 环境配置，禁止连接 `test` / `prod` / `production` / `staging` / `pre` / `release` 等非 local 环境的数据库、缓存、消息队列、HTTP/RPC 上游或其他服务。
- `test` 环境与本地测试是两个隔离概念：即使项目中存在 `config_test*` 或测试环境数据库，也不得把它当成本地自动化测试的默认连接目标。

## Skill 作用与适用场景

- 为当前任务选择合适的测试类型和优先级。
- 平衡功能验证、联调验证、回归验证和资源限制。
- 明确哪些路径必须覆盖，哪些风险只能记录为待补测。
- 避免测试阶段一上来就铺满所有用例，导致成本失控。
- 强制策略输出与新的时间戳测试主文档结构对齐，避免后续执行落点混乱。

## 自动触发信号

- 编码审查通过后，准备进入测试但还没有明确测试重点。
- 变更涉及多条链路、多种风险层级或多种测试方式。
- 时间、环境或资源有限，需要明确先测什么。
- 团队对当前应做功能验证、联调验证还是回归验证优先存在争议。
- 发现测试策略摘要准备记录到非 `artifact-storage-rules` 约定的测试根目录位置。
- 新增或修改测试主文档、验证说明、测试报告、覆盖说明或测试执行记录。
- 需要确定当天时间戳测试主文档的命名，或 ASCII 真实代码路径镜像。
- 发现测试脚本、fixture、mock、测试数据或说明资产散落在中央测试根目录之外。
- 需要统一测试名称、时间戳测试主文档、中文测试主文档或真实代码路径镜像命名。
- 为了让某段生产代码可测，准备在生产文件中新增函数、静态数据、结构体字段、分支或第二构造器。
- 发现生产代码中的符号只有 `test/` 在调用，或出现 `Seed`、`ForTest`、`TestOnly`、`Fixture` 等测试语义命名。

## 进入后先做什么

1. 先确认本次任务类型、改动范围和主要风险来源。
2. 先判断当前命中的是 `specialized-lifecycle` 策略路由，还是 `test-asset-governance` 资产治理路由；命中后读取对应 reference，不再启动已退役的独立入口。
3. 确认测试策略摘要最终会写回 `artifact-storage-rules` 约定的测试主文档。
4. 判断哪些测试类型必须出现，哪些可以降级或后补。
5. 如果需要拆成多轮独立测试，直接给出多个时间戳测试主文档方案，而不是在一个目录中混放多轮任务。
6. 明确后续应分流到哪个具体测试 skill 执行。

## 默认执行流程

1. 默认先读 `references/strategy-dimensions.md`，梳理测试策略要考虑的维度。
2. 如需继续展开，再读 `references/priority-model.md`，给测试路径排优先级。
3. 需要统一模板或正反例时，再读 `references/strategy-template.md`。
4. 输出测试策略摘要、优先级排序和测试任务拆分建议。
5. 若命中 `test-asset-governance`，读取 `references/test-asset-governance.md`，按其中的文档、命名、根布局和散落资产规则执行；该路由统一承接原四类测试资产治理职责。
6. 策略确定后，再分流到 `functional-validation-rules`、`test-regression-rules`、统一浏览器工具路由矩阵以及测试资源管理类 skill 执行；浏览器执行工具由矩阵按任务能力选择，遇到跨环境或跨系统问题时，先回到测试策略重新拆分。

## 权责边界与不负责事项

- 只负责测试大盘策略，不代替具体执行验证。
- 不负责测试程序、功能验证或回归结论；测试目录、命名、测试文档和散落资产治理由本 owner 的 `test-asset-governance` 条件路由承接；涉及 Go 可编译路径时还必须服从 `test-program-rules` 的《Go 测试编译路径（强制）》。
- 不把所有路径都定义成必须全测，必须服从风险和资源现实。
- 不在需求或修复目标尚未收敛时硬做测试策略。
- 不为同一轮测试额外创建策略 markdown；策略摘要固定落在测试主文档中。

## 需要暂停并确认的条件

- 需求目标、修复目标或影响范围还没稳定。
- 关键测试环境、数据或上下游条件完全不具备。
- 团队对主风险来源判断分歧过大，当前策略无法落地。
- 当前策略试图覆盖全量测试，却没有匹配资源。

## 执行通过 / 驳回标准

- 通过：能够说明本次应采用哪些测试类型、优先测哪些路径、哪些可延后，以及这些选择背后的风险依据；并能明确对应到一个或多个时间戳测试主文档；涉及生产代码改动时污染扫描为 `POLLUTION: PASS`，或命中项已登记豁免且理由成立。
- 驳回：策略仍停留在“都测一下”，没有优先级、没有范围收口，也没有和测试目录拆分方案对应；或策略包含通过新增测试专用方法、测试专用数据、测试专用结构体字段来降低测试成本的做法；或污染扫描 FAIL 却未整改也未登记豁免。

## 执行结果归档要求

- 将测试策略摘要统一记录到 `artifact-storage-rules` 约定的测试主文档。
- 摘要至少包含任务类型、风险来源、测试类型选择、优先级和待补测说明。
- 如果策略结果拆成多个独立测试任务，应明确对应的多个时间戳测试主文档建议，并在后续各自目录中承接执行记录。
- 如果后续策略调整，应在测试主文档中保留变更原因，避免执行口径漂移。
- 进入最终回复前，必须联动 `artifact-delivery-gate-rules`，核对测试策略摘要、拆分建议和待补测说明是否已经真实落到对应测试主文档；未落盘不得判定测试策略完成。

## 条件路由：test-asset-governance

当任务命中测试文档、测试命名、测试任务根布局或测试资产散落任一信号时，唯一进入 `test-strategy-rules` 的 `test-asset-governance` 路由；先读取 `references/test-asset-governance.md`，再按“中央测试根目录 -> 当天时间戳测试主文档 -> 中文测试主文档 -> ASCII 真实代码镜像 -> 资产归档与 artifact gate”顺序执行。该路由保留原有正负触发、目录命名、本地环境、禁止污染生产代码、暂停、驳回、清理和回滚边界。

自动触发别名包括：`测试主文档`、`测试说明`、`测试文档`、`测试命名`、`时间戳测试主文档`、`测试脚本散落`、`fixture 散落`、`迁移散落测试资产`、`新建测试主文档`、`测试资产镜像`。这些别名只路由到本 owner 的条件细则，不再产生独立 Skill 入口。

## references 读取规则

- 默认先读 `references/strategy-dimensions.md`；命中测试资产治理时追加读取 `references/test-asset-governance.md`。
- 本轮涉及生产代码新增或修改，或需要判定某个符号是否属于测试污染时，必须读 `references/production-test-pollution.md`，并执行 `scripts/scan_test_pollution.py`。
- 在决定测试主文档、主说明文件和多轮测试拆分方式时，先读 `../artifact-storage-rules/references/path-map.yaml` 与 `../artifact-storage-rules/references/update-policy.md`。
- 只有在需要确定测试优先级和覆盖收口时，再读 `references/priority-model.md`。
- 只有在需要模板和正反例时，再读 `references/strategy-template.md`。
- 只要创建或修改测试策略主文档，必须同时读取 `../artifact-delivery-gate-rules/references/plain-language-document-contract.md`，让策略结论、影响、范围、变化和完成标准先以白话开场，技术步骤与证据保留在既有技术章节或附录。
- 只要涉及浏览器联调或第三方验证，必须同时读取 `../artifact-delivery-gate-rules/references/review-acceptance-gate-contract.md`。
## 项目联调条件化规则

### 触发规则补充（强制）

- 前后端同时存在不等于浏览器联调必需。只有来源对象明确要求且当前必须完成时，才把浏览器联调列为正式放行条件。
- 浏览器联调、授权环境或第三方接口不适用时，记录 `not_applicable`、原因和依据，不阻断测试策略或本地验证；条件不足但已有替代验证时记录 `limited`，允许继续准备，但不能写成正式放行。
- 只有 `browser_integration` 门禁为 `applicable` 且当前必须完成时，才要求在 `local` 环境完成真实浏览器联调。

### 执行要求补充（强制）

1. 联调前先确认服务可访问（前端页面可打开、后端接口可达）。
2. 使用统一浏览器工具路由矩阵选定的执行工具，完成至少一次真实用户路径的页面交互验证（打开页面、关键操作、结果确认）。
3. 需要授权且浏览器联调门禁适用时，才必须先完成授权注入或登录流程；不适用或受限场景记录替代验证和人工补验方式。
4. 最终结论必须基于联调证据（至少包含 URL/页面状态与关键结果），不能仅基于代码推断给出“已验证通过”。
5. 若联调启动了前端或后端进程，完成后必须关闭并核验进程状态，禁止遗留后台进程。

## 本地环境配置发现与连接（强制）

本节是「本地环境配置发现与连接」的单一真相源。当测试启动、需求侦察、Bug 复现或定位需要连接本地真实环境（数据库、缓存、消息队列等）或读取本地环境信息时，统一遵循本节；其他测试 / 需求 / Bug skill 直接引用本节，不重复定义。

### 发现本地环境配置

- 需要本地环境连接信息时，必须先到项目约定的「本地配置文件」位置读取，不要凭空假设连接串、也不要直接要求用户重复提供已在配置里的信息。
- 通用发现方式：在仓库内按命名模式搜索本地 / 开发环境配置，常见命名含 `local` / `dev` / `.env`，例如 `*config*local*`、`*local*config*`、`config.local.*`、`*_local_*`、`.env.local`、`.env.development`。
- 若同时存在 `config_local*` 与 `config_test*`，本地自动化测试、启动调试和查询必须优先且仅允许读取 `local` 配置；`test` 配置只代表隔离测试环境，不属于当前本地自动化测试输入来源。
- 典型示例（仅示例，具体以各项目实际为准）：`backend/configs/config.local.yaml`、`go-admin/config/config_local_yaml.go`。
- 在某业务项目里确认到真实本地配置位置后，必须按 `project-memory-rules` 回写到「该业务项目」的 `PROJECT_MEMORY.md`，作为长期记忆，后续直接复用，避免每次重新搜索。

### 连接真实环境的隔离安全约束（强制）

- 判定"是否本地环境"的唯一标准是**连接信息的配置归属**，不是连接地址是否指向本机：只要连接信息来自 `local` 配置（`config_local*` / `.env.local` / `.env.development` 等本地开发配置），即属于允许连接的本地环境，即使它指向远程服务器、团队共享开发库或非 `localhost` 地址，也是合法的本地测试 / 调试目标。
- `localhost` / `127.0.0.1` / 本机端口 / 本机开发容器只是 local 配置的常见形态之一，既不是判定本地环境的必要条件，也不是充分条件；不得因为某连接指向本机就认定为 local，也不得因为某 local 配置指向远程主机就拒绝连接。
- 反过来，`test` / `prod` / `production` / `staging` / `pre` / `release` 配置里声明的连接信息一律禁止使用，即使它们恰好指向 `localhost` / `127.0.0.1` / 本机端口也不例外；严禁连接生产环境、测试环境、预发环境或其他非 local 配置声明的服务。本地(local)服务 ≠ test 服务 ≠ prod 服务，区分依据始终是配置归属而非物理地址。
- 仅按本地配置文件已声明的连接信息连接；严禁为测试在生产代码里新增测试专用连接分支、字段或 `if isTest` 之类条件（与「测试隔离红线」一致）。
- 严禁为方便测试去修改 `config_test*`、切换到 test 数据库账号、或临时把脚本默认环境改为 `test`；如果本地 `local` 配置不可用，应记录为本地环境阻断，而不是回退去使用 `test` 环境。
- 即使用户提供了 `test` / `prod` / `staging` 连接串、账号、token、接口地址或临时授权，agent 也不得直接连接或调用；必须记录为非 local 环境阻断，并要求改用 local 本地数据库和服务。
- 若 local 数据不足、local 服务未启动或本地依赖不可达，只能补齐 / 启动 local 环境，或记录为本地环境阻断；不得为了补证据连接 test / prod 数据库、缓存、消息队列、外部服务或线上接口。
- 对真实环境产生的写入 / 变更，测试结束后必须清理（事务回滚或 cleanup 脚本），不得遗留测试数据。
- 本地配置常含敏感信息（数据库密码、密钥）：代码、配置、普通维护文档和 Git 提交允许有意持久化原值；测试主文档、测试证据、控制台、对外输出和项目记忆不得回显原值。

## 接口测试执行通道（强制）

> 本节是「接口级测试执行通道」的单一权威来源。接口功能验证、接口回归、Bug 接口验证、上线门禁的接口部分统一遵循本节；`functional-validation-rules`、`test-regression-rules`、`bug-validation-rules` 直接引用本节，不重复定义执行细节。

### 判定边界：接口级 vs 代码级

- 测试对象是 **HTTP 接口**（有 method+path，经 HTTP 协议调用）→ **接口级测试** → 必须走 apifox 真实测试并落地用例。
- 测试对象是函数/方法/模块/纯逻辑 → **代码级测试** → 保留本地 `go test` / pytest，不切换。
- 页面交互/浏览器联调 → 浏览器链路，不属本通道。
- 同一轮验证可能同时含接口级与代码级测试：按测试对象分类各自执行，不得把整轮验证一刀切。

### 接口级测试强制走 apifox（强制）

- 接口功能验证、回归、Bug 接口验证、上线门禁的接口部分，统一用 `apifox test-case run` / `test-suite run` 在 apifox「AI 团队」对应项目中执行，并**落地测试用例保存到 apifox**（用例保留即落地，必要时并入 test-suite 回归）。
- 不得只在本地 shell/curl 验证后不落地用例；「本地调试过」不构成跳过 apifox 落地的理由。
- 目标项目解析与接口同步流程见 `apifox-cli__skillhub/modules/ai-team-project.md` 与 `modules/api-sync-to-apifox.md`；swag/OpenAPI 生成归 `swag-openapi-maintainer-rules`。

### 环境红线不变（强制）

- apifox environment 的 baseUrl 只允许指向 **local**（localhost / 本地开发配置声明的服务），禁止指向 `test` / `prod` / `staging` / `pre` / `release`；判定标准仍是「配置归属」而非物理地址，与「本地环境配置发现与连接」一致。
- 运行测试显式带 `--environment <localhost环境Id>`，避免默认环境漂移。

### 前置条件

- 被测服务必须在本地启动且端口可访问（先做可达检查再执行用例）。
- 数据构造按 `apifox-cli__skillhub/modules/test-data-and-judgement.md` 从 local 数据库取真实样本，禁止连非 local 服务取数。

### 标准执行链路

```text
1. 本地启动被测服务，确认端口可访问
2. 解析 apifox「AI 团队」项目 projectId（.apifox/settings.json 或 apifox project list）
3. 确认/创建 localhost environment（baseUrl=http://localhost:<port>）
4. （项目级）project-interface-baseline-rules 刷新接口基线
5. endpoint 定位；不存在 → api-sync-to-apifox 模块先同步
6. 生成/选择 test-case（category → cli-schema get/validate → create）
7. test-case run <caseId> --project <projectId> --environment <localhostEnv>
8. 按 test-data-and-judgement.md 判定 PASS/EXPECTED_FAIL/UNEXPECTED_FAIL/PENDING
9. 用例保留在 apifox（通过即落地），必要时并入 test-suite 回归
10. 结论写回 doc/5-tests/ 测试主文档（内联 caseId/报告链接），必要时回写接口基线
```

### 结论留痕

- 接口验证结论写回 `doc/5-tests/` 测试主文档；用例保存证据（caseId / suiteId / 报告链接）内联进证据小节，不得只写「已测试」无凭据。

## 测试样本分布优先（强制）

> 本节是测试策略中"测什么、用什么样本测"的强制规则，是对上文"测试隔离红线"的补充。任何测试策略、测试大纲、测试摘要，都必须显式回答"测试样本分布"问题。

### 一、为什么必须是真实分布

- 读接口（getHistory、getRateAndRange 等）必须用真实数据验证正常返回，禁止仅用不存在的数据测试并接受失败为"符合预期"。
- 写接口（createTransaction、createOrder 等）必须用 4 级样本矩阵（`historical_succeeded` / `historical_failed_lifecycle` / `historical_inflight` / `current_listing_available`）验证，样本定义见本文件下文"三、写接口样本分布"，数据来源优先级与判定规则见 `apifox-cli__skillhub/modules/test-data-and-judgement.md`。
- 任何"用伪造数据测试 + 接受失败为符合预期"的策略，必须直接驳回。

### 二、读接口样本分布

- 必须从数据库最近 5-10 条记录中提取请求参数。
- 至少覆盖 2 个业务场景或 2 个查询维度。
- 数据库无数据时，必须先尝试插入测试数据（按本地 `local` 配置连接）；完全无法插入时记录为待确认，不得直接判定为通过。

### 三、写接口样本分布（4 级样本矩阵，独立内嵌）

> 原 `project-interface-release-execution-rules/references/test-data-construction-rules.md` 的数据来源优先级与响应判定规则已并入 `apifox-cli__skillhub/modules/test-data-and-judgement.md`；本节的 4 级样本定义保持不变。

- 写接口策略必须显式回答 4 类样本如何获取：
  - `historical_succeeded`：`orderUser` 等业务表中 `status=4`（或其他业务终态成功码）的最近 N 条。
  - `historical_failed_lifecycle`：业务表上 51/52/61-65/70/71 等业务失败终态集合的最近 N 条。
  - `historical_inflight`：业务表上 1/2/22/50 等在途区间的最近 N 条。
  - `current_listing_available`：`getFromPairList` / `getToPairList` / `getMainPairList` 当前可用币对。
- 每一类样本数 N 默认 5，不得低于 3；总样本数不得少于 10。
- 至少覆盖 2 个通道/链/币种。

### 四、与其他测试类型的关系

- 接口测试是验证"接口在真实分布下是否按预期工作"的主要手段，不能用单元测试或代码审查代替。
- 联调测试中遇到写接口时，同样适用 4 级样本矩阵。
- 回归测试中遇到写接口时，至少保证 `historical_succeeded` + `current_listing_available` 2 类样本。

- 基于风险的测试结论分层：`references/risk-based-test-conclusion.md`
