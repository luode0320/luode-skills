# Bug 条件路由：discovery-and-gap

> 归属 owner：`bug-intake-rules`。本文件只承接条件路由细则，不创建第二个自动触发入口。迁移后的规则、用户习惯、local 安全红线、授权边界、暂停/停止、清理、回滚和归档要求继续有效。

## 迁移保留规则：bug-discovery-rules

# Bug 主动侦察规则

只在“用户给了一个问题，但定位资料还没整理好”时使用这个 skill。
目标是让用户像报障一样只给一句话、一个现象或几张截图，agent 负责先主动看代码、查日志、只读连本地库比数据、理解截图，把能自己查到的证据补齐，再把真正解不开的问题交回用户，而不是一上来就要用户补全复现步骤和日志。

本 skill 与 `requirement-intake-rules` 的 `initial-discovery` 路由在需求域的角色对称：需求域在追问前主动侦察资料，Bug 域用本 skill 在追问前主动侦察证据。

## 核心原则

- 先侦察，再追问；不能因为 Bug 描述简短就立刻把大量复现条件、日志和环境问题抛回给用户。
- 只读优先；看代码、读日志、查 trace、读配置、只读查询本地数据库可以主动做；数据库、缓存、消息队列、HTTP/RPC 上游和服务连接只能使用 local 本地环境，严禁连接 test / prod / staging 等非 local 环境；写库、改数据、重启本地服务等高风险动作必须暂停确认。
- 证据优先；每个根因候选都要能追溯到真实代码位点、命令输出、日志行、查询结果或截图内容。
- 不脑补；没有证据的内容只能写成“可疑点 / 待验证假设 / 需用户确认的问题”，不得当成已证实的根因。
- 连库和连服务有红线；只连 local 本地环境、只做只读查询，测试库、生产库、预发库和非 local 服务一律禁连，禁止任何增删改（详见「连接本地数据库的安全红线」节）。
- 可复用线索要沉淀；查过且有价值的代码入口、表 / 字段、查询线索和侦察经验，必须按 `project-memory-rules` 回写到对应业务项目的 `PROJECT_MEMORY.md`。
- 截图是证据不是结论；从截图提取报错文案、堆栈、页面状态、数据值后，仍要回到代码或数据里二次印证。

## 自动触发信号

- 用户只说一句现象，例如“这个接口偶尔报 500”“列表数据对不上”“点保存没反应”“金额算错了”。
- 用户只给几张截图、一段报错文案或一小段日志，没有复现步骤、环境信息或定位证据。
- 怀疑是数据问题（数据对不上、状态异常、脏数据），需要查真实数据才能判断。
- 怀疑是代码逻辑问题，需要看实现、追调用链、看分支与状态流转。
- `bug-intake-rules` 标准化现象后，`bug-intake-rules` 的 `discovery-and-gap` 条件路由 准备就缺失信息向用户大量追问前，应先转入本 skill 做主动侦察。

## 进入后先做什么

1. 用一句话复述用户提出的现象和 agent 当前理解，不扩写成确定根因。
2. 为当前 Bug 沿用 / 创建统一根目录，路径、目录名和入口文件统一遵循 `artifact-storage-rules`；侦察证据写回同一 Bug 根目录，不另起平行文档。
3. 列出本轮可用侦察入口：报错文案 / 堆栈、截图、相关代码模块、调用链、现有日志与 trace、配置、数据库表与字段、上下游服务、`PROJECT_MEMORY.md` 中的历史线索。
4. 先读长期记忆与历史 Bug 记录，确认是否有同类问题、相关表或相关代码入口线索。
5. 按只读方式侦察：先静态看代码定位可疑逻辑，再判断是否需要只读连本地库查数据对比。
6. 把证据分成“已确认事实”“可疑点 / 根因候选”“仍需用户确认的问题”。
7. 输出根因候选、对应证据、风险和下一步应转交的 Bug 域 skill。

## 默认执行流程

1. 默认先读 `bug-intake-rules/references/discovery-and-gap-bug-discovery-rules-discovery-checklist.md`，确定本轮侦察来源与顺序。
2. 需要判断证据可信度、截图取证方式、以及连本地库的只读安全约束和记忆回写时，再读 `bug-intake-rules/references/discovery-and-gap-bug-discovery-rules-evidence-and-db-readonly.md`。
3. 需要判断 Bug 域相邻 skill 的承接顺序、是否让路或回流时，再读 `bug-intake-rules/references/discovery-and-gap-bug-discovery-rules-bug-domain-routing.md`。
4. 需要输出侦察结论草案时，再读 `bug-intake-rules/references/discovery-and-gap-bug-discovery-rules-output-template.md`。
5. 代码逻辑问题：联动 `codegraph-analysis-rules` 看实现、追调用链、定位可疑分支与状态流转；CodeGraph 不可用时回退到本地 `rg` / `read`。
6. 数据问题：按 `test-strategy-rules` 的「本地环境配置发现与连接」从本地配置文件读取连接信息，只读连接本地库，用 `SELECT` / `SHOW` / `EXPLAIN` 等查询真实数据并与期望值对比，定位是数据本身错、写入逻辑错还是读取逻辑错。
7. 截图 / 报错图：提取报错文案、堆栈、页面状态、关键数据值，再回到代码或数据里二次印证。
8. 对每个根因候选标注证据等级，不允许用“应该”“大概”“看起来”替代证据。
9. 完成侦察后，把可复用线索交给 `project-memory-rules` 回写对应业务项目的长期记忆。
10. 若已形成可复现或可定位的证据，转 `bug-reproduction-rules` 或 `bug-root-cause-rules`；若怀疑时序 / 并发且静态无法收敛，转 `bug-intake-rules` 的 `runtime-diagnostics` 条件路由。
11. 若侦察后仍有真正无法通过查代码 / 查数据解决的缺口，转 `bug-intake-rules` 的 `discovery-and-gap` 条件路由，但只保留这类问题。

## 连接本地数据库的安全红线（强制）

- 只能连接 `local` 本地配置声明的数据库和服务（判定依据是配置归属，不是地址是否指向本机——local 配置可能指向远程共享开发库，仍属合法本地目标；详见 `test-strategy-rules` 的「连接真实环境的隔离安全约束」）；**测试库、生产库、预发库以及 test / prod / staging 服务一律禁止连接**，不接受任何“临时连一下测试库 / 调一下线上接口”的例外。
- 只能执行只读查询（`SELECT`、`SHOW`、`EXPLAIN`、`DESCRIBE` 等）；**严禁 `INSERT` / `UPDATE` / `DELETE` / `TRUNCATE` / DDL 及任何写操作**。
- 若定位或修复确实需要增删改数据，agent 不得自行执行；只能产出 SQL 脚本（含目的、影响行、回滚方式）交用户手动执行。
- 连接信息按 `test-strategy-rules` 的「本地环境配置发现与连接」从本地配置文件读取；不得把明文密码、密钥、连接串原文写进文档、README、提交或对外输出。
- 查询要可追溯：在 Bug 根目录记录连了哪个本地库、执行了哪些只读 SQL、对比了哪些数据与结论（含敏感数据脱敏）。
- 大表查询必须加条件或 `LIMIT`，避免全表扫描拖垮本地库；高成本查询先评估再执行。

## 权责边界与不负责事项

- 只负责从“一句话 / 截图”到“有证据的根因候选”之间的主动侦察、取证、比对。
- 不代替 `bug-intake-rules` 把现象标准化录入并建立 Bug 根目录入口。
- 不代替 `bug-intake-rules` 的 `discovery-and-gap` 条件路由 做最终缺口阻断；可主动查到的缺口先在本 skill 解决，不直接抛回用户。
- 不代替 `bug-reproduction-rules` 输出正式复现步骤与稳定性结论。
- 不代替 `bug-root-cause-rules` 的最终静态定位结论，也不代替 `bug-intake-rules` 的 `runtime-diagnostics` 条件路由 的运行时诊断。
- 不代替 `bug-fix-proposal-rules` 出修复方案。
- 不把“看到可疑代码”或“截图里的报错”直接当成已证实的根因。
- 不把无证据推断写入长期记忆；只有验证过、后续可复用的线索才回写。

## 需要暂停并确认的条件

- 现象本身无法判断属于哪个模块或哪类问题，连侦察方向都定不了。
- 需要访问未授权的私有仓库、登录态页面、付费接口或敏感凭据。
- 侦察只能靠连接测试库 / 生产库才能继续，而本地库无对应数据（此时停下，不得连非本地库）。
- 定位或修复需要增删改数据，但只能交用户手动执行 SQL，agent 不得代执行。
- 多个根因候选都成立，且静态证据与本地数据都无法排除，需要用户补充关键上下文。

## 执行通过 / 驳回标准

- 通过：已主动侦察代码、日志、本地数据与截图，输出有证据来源的根因候选、可疑位点、证据等级、风险和最少待确认问题，并把可复用线索回写长期记忆；连库全程只读且仅限本地。
- 驳回：用户只给简短描述时直接要求补全复现步骤和日志；未看代码 / 未查数据就给猜测；关键结论没有证据来源；连接了测试库 / 生产库，或对数据库执行了任何写操作；查到的有价值线索没有进入长期记忆回写流程。

## 执行结果归档要求

- 侦察结论统一写回 `artifact-storage-rules` 约定的当前 Bug 根目录；如果根目录还不存在，先转 `bug-intake-rules` 建立，再把侦察证据补进同一根目录。
- 当前 Bug 根目录 `README.md` 至少记录：现象复述、已侦察来源清单、根因候选与证据等级、连库只读查询与数据对比结论（脱敏）、仍需用户确认的问题。
- 可复用侦察线索必须通过 `project-memory-rules` 写入对应业务项目的 `PROJECT_MEMORY.md`，字段至少含别名、类型、定义、来源、适用范围、更新时间和状态。
- 不单独新建“侦察文档”作为平行入口；侦察证据并入当前 Bug 根目录。
- 进入最终回复前，必须联动 `artifact-delivery-gate-rules`，核对侦察结论、证据与待确认问题是否已经真实写回当前 Bug 根目录；未落盘不得判定侦察完成。

## references 读取规则

- 默认先读 `bug-intake-rules/references/discovery-and-gap-bug-discovery-rules-discovery-checklist.md`。
- 在定位当前 Bug 根目录、入口 `README.md` 或判断是否继续复用同一根目录时，先读 `../artifact-storage-rules/references/path-map.yaml` 与 `../artifact-storage-rules/references/update-policy.md`。
- 只有在处理证据可信度、截图取证、连本地库只读约束和长期记忆回写时，再读 `bug-intake-rules/references/discovery-and-gap-bug-discovery-rules-evidence-and-db-readonly.md`。
- 只有在判断 Bug 域相邻 skill 的承接顺序、让路或回流时，再读 `bug-intake-rules/references/discovery-and-gap-bug-discovery-rules-bug-domain-routing.md`。
- 只有在组织侦察结论输出结构时，再读 `bug-intake-rules/references/discovery-and-gap-bug-discovery-rules-output-template.md`。
- 回写 Bug 侦察结论前，必须读取 `../artifact-delivery-gate-rules/references/plain-language-document-contract.md`；根因判断和影响先用白话说明，原始日志、查询和证据进入附录。
- 若侦察涉及外部接口、专项环境或验收条件，必须同时读取 `../artifact-delivery-gate-rules/references/review-acceptance-gate-contract.md`，不适用项只记录原因和依据。

## 迁移保留规则：bug-gap-rules

# Bug 缺口识别规则

只在 Bug 已经被提出来，但入口信息还不够支撑复现、归属或定位时使用这个 skill。
如果当前已经具备足够信息开始复现或定位，请转交 `bug-reproduction-rules` 或 `bug-root-cause-rules`。

## Skill 作用与适用场景

- 识别 Bug 入口中到底缺了哪些基础信息。
- 区分只是补充说明，还是已经阻断复现和定位推进。
- 输出明确的待补信息清单，避免边猜边调。
- 将缺口清单和阻断判断统一沉淀到当前 Bug 根目录。
- 把 Bug 入口和后续复现、定位步骤解耦。

## 自动触发信号

- 问题描述里只有“报错了”“不对了”，没有稳定场景和证据。
- 缺少环境、数据、日志、时间点、账号或触发前提。
- 团队对是否能直接进入复现或定位存在争议。
- 同一个 Bug 被多次转述后，入口信息明显失真。

## 进入后先做什么

1. 先区分当前已有信息和真正缺失的信息。
2. 为当前 Bug 确认统一的根目录，继续沿用 `artifact-storage-rules` 约定的当前 Bug 根目录。
3. 判断缺失项会影响复现、范围界定还是根因定位。
4. 把缺口按阻断级和非阻断级排序。
5. 若缺口涉及本地环境信息（数据库、缓存、消息队列、HTTP/RPC 上游等连接条件），优先按 `test-strategy-rules` 的「本地环境配置发现与连接」去本地配置文件查找，能从 local 配置发现的不计入待补缺口，并遵守其隔离安全约束；不得把 test / prod / staging 连接条件当作可用补齐来源。
6. 输出待补信息列表和补齐优先级。

## 默认执行流程

1. 默认先读 `bug-intake-rules/references/discovery-and-gap-bug-gap-rules-gap-checklist.md`，先检查 Bug 入口最少应包含哪些信息。
2. 再读 `../artifact-storage-rules/references/path-map.yaml` 与 `../artifact-storage-rules/references/update-policy.md`，确认 Bug 根目录、入口 `README.md` 和同一 Bug 持续复用同一根目录的策略。
3. 如需继续展开，再读 `bug-intake-rules/references/discovery-and-gap-bug-gap-rules-blocking-signals.md`，需要判断哪些缺口会阻断推进。
4. 需要对照边界或正反例时，再读 `bug-intake-rules/references/discovery-and-gap-bug-gap-rules-gap-examples.md`，需要对照缺口识别正反例。
5. 输出 Bug 缺口清单、阻断判断和补充优先级，并更新到当前 Bug 根目录下的 `README.md`。
6. 可通过看代码 / 查日志 / 只读连本地库比数据主动查到的缺口，先回流 `bug-intake-rules` 的 `discovery-and-gap` 条件路由 侦察解决，不计入待补缺口；缺口补齐后再进入 `bug-reproduction-rules` 或 `bug-root-cause-rules`；若基础问题描述本身混乱，可回流 `bug-intake-rules`。

## 权责边界与不负责事项

- 只负责识别缺口，不替代 `bug-intake-rules` 的标准化录入职责。
- 不直接设计复现步骤，那属于 `bug-reproduction-rules`。
- 不提前猜根因，也不把缺口识别当成定位结果。
- 不因为轻微缺口就过度阻断所有后续动作。

## 需要暂停并确认的条件

- 连异常现象本身都无法准确描述。
- 缺失项已经阻断复现和定位，但来源方暂时无法补齐。
- 问题来源和环境版本互相矛盾，无法形成可信入口。
- 团队试图用猜测替代缺失信息继续推进。

## 执行通过 / 驳回标准

- 通过：能够明确列出缺失项、说明其影响，并判断哪些缺口必须先补齐、哪些可后续补充。
- 驳回：只是笼统地说“信息不够”，没有具体缺口列表、没有优先级，或直接绕过缺口继续定位。

## 执行结果归档要求

- 将缺口清单、阻断结论和补充优先级统一记录到 `artifact-storage-rules` 约定的当前 Bug 根目录中。
- 当前 Bug 根目录必须包含 `README.md`，至少写明当前已知信息、缺失项和影响面；仅当缺口仍阻断当前 Bug 闭环时，补写必要后续动作。
- Bug 根目录、入口 `README.md` 和同一 Bug 根目录复用策略统一遵循 `../artifact-storage-rules/references/path-map.yaml` 与 `../artifact-storage-rules/references/update-policy.md`。
- 如果缺口来自历史信息断裂，应保留来源说明，便于后续追溯，并继续沿用同一个 Bug 根目录。
- 进入最终回复前，必须联动 `artifact-delivery-gate-rules`，核对当前 Bug 根目录 `README.md` 是否已经真实写入缺口清单、阻断结论和补充优先级；未落盘不得判定 Bug 缺口识别完成。

## references 读取规则

- 只要创建或修改 Bug 根目录 `README.md`，必须同时读取 `../artifact-delivery-gate-rules/references/plain-language-document-contract.md`，正文先写结论，技术细节保留在原有章节或附录。
- 如果本轮涉及审查、验收、功能验证、浏览器联调或第三方验证，必须同时读取 `../artifact-delivery-gate-rules/references/review-acceptance-gate-contract.md`，按适用性记录，不把不适用条件写成阻断。
- 默认先读 `bug-intake-rules/references/discovery-and-gap-bug-gap-rules-gap-checklist.md`。
- 在定位当前 Bug 根目录、入口 `README.md` 或判断是否继续复用同一根目录时，先读 `../artifact-storage-rules/references/path-map.yaml` 与 `../artifact-storage-rules/references/update-policy.md`。
- 只有在 区分阻断级和非阻断级缺口 时，再读 `bug-intake-rules/references/discovery-and-gap-bug-gap-rules-blocking-signals.md`。
- 只有在 需要对照样例或判断是否过度阻断 时，再读 `bug-intake-rules/references/discovery-and-gap-bug-gap-rules-gap-examples.md`。
