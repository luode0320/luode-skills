# 项目历史事件

> 本文件只追加关键历史事件。普通新线程默认不读取，只有历史追问、当前状态不足或真实卡点时才窄检索。

## 事件

- 2026-08-05：完成 CYCLE-PSR-23 config 根加载与结构文件规则。独立后端 `config/load.<ext>` 与 `config/model.<ext>`（同仓后端 `backend/config/...`）成为唯一配置加载/结构落点，Catalog 新增 4 个 pattern 条目并补 Schema 守卫，CLI strict 对 config/ 根两个命名放行、其余拒绝；专项测试 `11/11`、四文件回归 `26/26`、需求/实施/测试/风格四份文档 profile 与 Skill 合规门禁均通过，工作树保持已改动未提交。

- 2026-07-14：完成任务阻断收口与恢复计划。新增唯一 `BLK-*` 共享契约并接入审查、验收、功能验证、Bug 验证、执行失败、运行时恢复和最终总结；真实阻断在最终结尾输出状态、证据、已尝试动作、停止边界、影响、至多三步解决计划和重入点，`limited`/`not_applicable`/P2/P3 不误报。文档门禁 52 项、运行时阻断事实 3 项、七份文档 profile、Python 编译、JSON schema 解析和字典生成均通过；Obsidian 沉淀因固定 vault 未注册而阻断，未执行 Git 历史写入。

- 2026-07-13：完成 Windows PowerShell 环境可靠性升级。RequiredOnly、可选工具降级、精确包源、JSON 状态、WhatIf、profile/Terminal 事务、hash 回滚、Git Bash/WSL 分流和 UTF-8 BOM 兼容均已收口；PowerShell 5.1 与 PowerShell 7 的九项隔离回归、相关文档 profile、两个 Skill quick validator 和字典生成均通过，未执行 Git 历史写入。

- 2026-07-13：完成 Obsidian 知识流跨 Windows/WSL bridge 的 TASK-OBS-08；35/35 离线回归、PowerShell parser、Python 编译、search、长正文双端 readback（13321 chars/LF181/MD5 C46A...）与 append 双端 readback（172 chars/LF11/MD5 27ec...）通过；CYCLE-OBS-02 收口，未执行 Git 历史写入。
- 2026-07-13：完成 CYCLE-OBS-03 TASK-OBS-09~12；字典、项目记忆、周期 strict、验收 profile、当前改动审查和独立最终验收均 PASS，AC-OBS-001~010 全部放行，工作树保持未提交。

- 2026-07-12：补齐 Markdown 图片资产 validator 的文件命名、九字段资产清单一致性、共享引用和 `doc/data/` 根目录错位扫描，新增正反单测后校验器达到 `21/21 PASS`；README、编码总规和最终验收状态同步，真实 imagegen 仍因 `gpt-image-2` 503 / `gpt-image-1.5` 403 保持阻断。

- 2026-07-12：按 `CHG-DOC-IMG-001` 实施 Markdown 图片资产闭环；冻结 `doc/data/images/` 唯一根目录，更新 storage/requirement/implementation/delivery 规则、profile v3、validator 图片与孤儿检查，并将来源需求、验收、实施总览、全量顺序和周期 01 回写为增量执行入口；工作树保持未提交。

- 2026-07-11：确认采用“项目本地四件套 + Obsidian 选择性知识流”方案；项目当前状态与稳定规则分离维护，历史事件保持追加式记录。
- 2026-07-11：完成四件套规则闭环；同步 Obsidian、项目记忆、自举脚本、仓库规则和字典，验证缺失创建、幂等运行、历史追加保护、current 超限阻断及固定 vault CLI 沉淀。
- 2026-07-12：完善 `windows-wsl-execution-rules` 的跨环境命令失败恢复闭环；新增脱敏去重案例库、PowerShell/WSL/JSON/编码恢复路由和收口前自动回写规则，刷新字典并完成 UTF-8、内容存在性和差异检查。
- 2026-07-12：为权威 `imagegen` skill 增加错误案例持续迭代规则与脱敏案例库，收录 gpt-image-2 参数、透明背景、依赖/鉴权和瞬态网络错误，刷新字典并完成本地 dry-run/check、UTF-8 与敏感信息检查。
- 2026-07-12：完成 imagegen 错误案例演进的当前改动总审查，收窄瞬态重试案例到 `generate-batch` 实际覆盖范围，并通过本地伪客户端重试验证；改动保持未提交。
- 2026-07-12：按用户授权完成 imagegen 实现与审查文档提交，提交为 `26f763a` 与 `83e9576`；随后同步项目当前状态。
- 2026-07-12：按用户确认计划新增 `execution-failure-learning-rules` 元 Skill，统一 prevent/recover/learn、唯一 owner、candidate/active 授权、脱敏去重和冲突门禁；接入首批高风险 owner，完成字典刷新与 AC-001 至 AC-008 前向行为验证，改动保持未提交。
- 2026-07-12：完成执行失败持续学习与主动预防的当前改动总审查和最终验收，结论通过；Obsidian 知识笔记与 INDEX 已通过 CLI 沉淀，Git 提交仍未执行。
- 2026-07-12：按用户要求升级需求、验收和实施文档交接规则，新增 L1-L4 极致完整性标准、零决策执行契约、实施总览/周期/任务卡模板、图形化标准和文档 profile 校验器；新增需求与实施基线文档及正反验证，四类 Skill 自检和文档 profile 均通过，未执行本轮 Git 历史写入。
- 2026-07-12：通过固定 `D:\\obsidian_data` vault 的 Obsidian CLI 检索并沉淀“需求与实施文档零决策交接”知识笔记，创建 `知识库/INDEX.md` 入口，未使用文件系统读写替代 CLI。
- 2026-07-12：复核并统一三份实施文档的权威来源 ID 为 `REQ-DOC-20260712-033322`，将已落盘入口的状态从历史占位语义修正为真实状态，五类文档 profile、单元测试、Skill 校验、字典生成和差异检查再次通过。
- 2026-07-12：完成需求与实施文档极致完备化周期 01-04 收口并启动周期 05；补齐周期 04 当前 profile 所需章节，创建周期 05 全局同步/最终验收实施文档与测试入口，后续以全量回归、审查和验收证据作为最终放行依据，改动保持未提交。
- 2026-07-12：完成周期 05 全局同步与最终验收；更新旧的当前改动总审查和最终验收文档，补齐 C02-C05 证据互链及最终验收一致性断言；九份文档 profile、校验器单测 7/7、周期 02/03/04/05 测试、四个 Skill quick validator、Mermaid 真解析、字典和固定 Obsidian CLI 均通过，工作树保持未提交。
- 2026-07-12：完成最终注释双 skill 闸门与实现审查收口；为校验器、测试函数和 C05 集成测试补齐中文函数头、步骤编号及补丁原因注释，修正最终验收的周期 05 测试口径为 6/6，重跑单测、集成测试、编译、quick validator 和差异检查均通过，未执行 Git 历史写入。
- 2026-07-12：修复严格文档校验器的 JSON 集合序列化、正文回指污染周期归属和“禁用”规范词误报；补齐周期 01 任务级验收证据与 `--root .` 严格命令，需求/验收 strict 报告均为 `status: PASS`，校验器单测更新为 9/9，工作树保持未提交。
- 2026-07-12：执行 Markdown 图片资产闭环的真实 imagegen 验证；`gpt-image-2` 返回 HTTP 503 `model_not_found`，回退 `gpt-image-1.5` 返回 HTTP 403 权限错误。未生成伪图，临时资产已清理；机器校验、回归测试和审查保持通过，C05/最终验收状态改为 `blocked`，工作树未提交。
- 2026-07-12：记录 Windows Python 默认编码导致 quick validator 解码失败的可复用恢复方案；使用 `python -X utf8` 对同一输入复验通过，并按 `WSL-006` 以 `candidate` 写入跨环境命令失败案例库。
- 2026-07-12：按用户授权完成 Windows PowerShell 环境准备：安装并验证 PowerShell 7.6.3，设置 Windows Terminal 用户级默认 profile，初始化 PowerShell 5.1/7 UTF-8 profile，安装并验证 manifest 工具；7z/tlrc 因管理员权限阻断，未绕过 UAC。
- 2026-07-12：完成 Windows PowerShell Skill 的 Audit、JSONC Apply、重复 Apply 幂等、Rollback、quick validator、字典刷新和 WSL 原生工具路径复核；WSL PATH 无 `/mnt` 且无 Windows `.exe` 误走，改动保持未提交。
- 2026-07-12：按用户要求升级 Windows PowerShell Skill 的自动迭代闭环；新增 SessionEnsure 会话 TTL/原子锁、RecoverCommand/wrapper 命令缺失恢复、精确 package 映射、verified discovered-tools、脱敏 failure casebook、Windows/WSL owner 分流和真实失败恢复测试。PS5/PS7 解析、两个 Skill quick validator、原有环境测试、新增恢复测试、字典、UTF-8 与 diff 检查通过；7z/tlrc 权限阻断保留，未执行 Git 历史写入。
- 2026-07-12：针对通用上线测试引擎并行补丁后的 `23 passed, 2 errors, 1 failure` 真实状态，新增受限修订版全量实施计划，冻结 R1 回归恢复、C02-C08 垂直切片、local-only、真实测试、停止/回滚和 C08 证据门禁；本轮未获得代码实施授权，未执行 Git 历史写入。
- 2026-07-12：按修订版上线测试引擎计划完成 R1 与 C02-C08 窄闭环实现；修复 gRPC discovery、RPC local provenance、CLI 兼容、参数位置/provider、doctor 矩阵、协议判定、报告/基线产物和 v1 migration CLI。旧轮 27/27、本轮新增 11/11 测试通过；C08-03 因非 HTTP local runtime 与最终验收输入缺失保持 BLOCKED，未执行 Git 历史写入。
- 2026-07-12：将通用上线测试引擎修订计划升级为极致完整执行契约；校正当前证据目录为 `2026-07-12_191712`，新增 C09 双索引、C10 真实 local runtime、C11 P0/P1 全量门禁、C12 跨项目复用与证据互链任务，strict implementation validator PASS；本轮只更新计划，未授权继续编码或 Git 历史写入。

- 2026-07-12：完成研发文档白话化与附录分层规则。新增共享契约并接入需求、实施、Bug、测试、审查、验收、架构、交付和报告类 Skill；校验器新增正文/附录门禁与八类文档 profile，`26/26` 单测通过。不适用的第三方审查或验收需记录原因和依据但不再默认阻断；本轮未执行 Git 历史写入。
- 2026-07-13：完成文档白话化与审查验收条件化门禁升级收口；六类代表性 profile 全部 `PASS`，校验器单测 `30/30 PASS`，Python 编译、技能字典生成和 `git diff --check` 均通过。保留现有标题结构，不新增独立 Skill；不适用验证不阻断，受限验证可继续但不正式放行，明确必需且无替代验证才阻断；本轮未执行 Git 历史写入。
- 2026-07-13：按审计结果修复白话契约绕过、HEAD 标题编号比较、通用 profile 空壳和 `limited` 顶层状态误报；补齐新旧文档兼容、审查提交边界、最终验收 N/A 依据和项目记忆索引。校验器单测 `37/37 PASS`，六类代表性 profile、编译、字典和差异检查通过；本轮未执行 Git 历史写入。
- 2026-07-15：按用户要求补充 `code-generation-style-rules` 的局部一致性与接口实现对照规则；统一局部上下文只做必要模板替换，接口实现优先参考既有实现，风格契约记录局部证据、参考实现、最小新增内容和禁用写法；同步需求/验收/实施文档与项目记忆，当前改动未提交。
- 2026-07-15：完成局部一致性与接口实现规则收口；TEST-06 至 TEST-11、五个工程文档 profile、字典、UTF-8、差异、实现自审、当前改动总审查、skill 合规和最终验收均通过；通过 Obsidian bridge 新增规则知识笔记并更新 INDEX，未执行 Git 历史写入。
- 2026-07-16：按用户要求升级代码注释双 skill，明确超过 5 行非空代码/注释行的函数/方法体、闭包体和连续控制流代码块必须在块内就近补顶层步骤注释；同步项目风格、项目记忆与字典，规则一致性和机器索引校验通过，未执行 Git 历史写入。

- 2026-07-17：按冻结的 Skill 体积治理与职责拆分计划完成 `TASK-SPLIT-01-01`。修正测试目录日期 rollover 与中文说明/ASCII 资产布局，统计正式字典 84 个 skill、磁盘 111 个 skill 目录和 27 个扩展种子；生成体积报告并通过 JSON、UTF-8、哈希、负向退出、实现审查及需求/验收/实施文档门禁，未修改 skill 资产、字典或 Git 历史。
- 2026-07-17：按冻结计划完成 `TASK-SPLIT-01-02`。冻结 `candidate-matrix.yaml`（84 个正式条目、27 个扩展种子、7 个候选顺序、4 个正式二分候选），修正正式/磁盘/扩展种子统计口径和 `TEST-SPLIT-002` 入口冲突；四份工程文档与周期 01 profile、矩阵 YAML/哈希/名称集合断言均通过，skill 资产、字典和 Git 历史保持未修改。
- 2026-07-17：进入并实现 `TASK-SPLIT-01-03`。新增五类 Skill 拆分验证入口、PowerShell `-CasesRoot` 转发和仓库/fixture 路径边界；Python/PowerShell 正向模式、编译和越界负向测试已通过，计划文档与项目当前状态同步，真实 skill、字典和 Git 历史保持未修改；审查与验收待当前周期收口。
- 2026-07-17：完成 `TASK-SPLIT-01-03` 的当前改动总审查与任务验收。审查报告结论通过，需求/验收/实施总览/周期 01/测试 README 和审查 profile 均通过；周期 01 三个任务全部完成四项闭环并收口，CYCLE-SPLIT-02 保持未进入，真实 skill、字典和 Git 历史保持未修改。

- 2026-07-21：用户确认继续精简需求、实施、测试、Bug、审查、验收六域 Skill，并冻结“六域总方案分周期、回归通过后真实删除、单主入口加条件路由、用户习惯与自动触发不可删除”的来源对象。已持久化需求、验收标准、全量顺序方案、实施总览和六份实施周期文档；尚未修改 Skill 资产、字典或 Git 历史。

- 2026-07-21：完成 `CYCLE-SS-01`。冻结 36 个目标 Skill、11 个拟退役候选、source-target manifest、保护语义、资产 SHA-256、活跃消费者、72 条触发 fixtures 和 baseline validator；Python 编译、baseline、PowerShell wrapper、越界与非法阶段负向测试、测试文档 profile、周期 profile、审查与任务验收均通过。未修改真实 Skill、字典或 Git 历史。

- 2026-07-21：完成 `CYCLE-SS-02` 需求域 discovery 第一个候选的 owner 合并、9 个 live consumer 迁移、scoped pre-delete/post-delete、真实删除和字典刷新；新增增量删除验证器生命周期，保留历史归档与未迁移候选边界，未执行 Git 历史写入。
## 2026-07-21：CYCLE-SS-03 实施与测试域结构收敛完成

- `implementation-planning-rules` 与 `project-interface-release-execution-rules` 完成 references 化，保留原自动触发和执行契约。
- 四个测试资产入口合并到 `test-strategy-rules` 的 `test-asset-governance` 条件路由，并在迁移验证后真实删除旧目录。
- 活跃消费者、资产冻结记录、字典、触发 fixtures、测试/审查/验收证据完成收口；字典 `planned_missing=0`。
- 本周期未执行 Git 历史写入；`.codex/config.toml` 继续排除；Obsidian 仍因 `VAULT_NOT_REGISTERED` 阻断。

## 2026-07-21：CYCLE-SS-04 Bug 域入口收敛完成

- `bug-intake-rules` 增加 `discovery-and-gap` 与 `runtime-diagnostics` 条件路由，完整承接主动侦察、缺口、运行时断点、临时日志与诊断断言规则。
- 五个重复 source 完成资产迁移、活跃消费者切换、scoped pre-delete/post-delete 和真实删除；冻结 SHA-256、rollback locator、迁移 map 与任务级测试/审查/验收证据均保留。
- route validator、五个 scoped post-delete、字典生成和工程文档收口通过；字典 `implemented_total=76`、`planned_missing=0`。未执行 Git 历史写入；`.codex/config.toml` 保持排除；Obsidian 仍因 `VAULT_NOT_REGISTERED` 阻断。

## 2026-07-21：CYCLE-SS-05 审查与验收域引用化完成

- 四个保留自动触发的 owner 已将重复证据、归档、暂停和阻断细则下沉到各自 `shared-evidence-and-specialized-contracts.md`；原 description、trigger aliases、阶段职责、用户习惯、授权、安全、停止、输出和证据归档保持可验证。
- `code-review-automation-rules` 明确保留 `specialized-lifecycle`，未被合并或删除。
- CYCLE-SS-05 baseline/route、全量 baseline/trigger、字典和工程文档 profiles 通过。
- CYCLE-SS-06 全链路 post-delete 随后发现 `requirement-gap-rules` 仍存在，说明此前 `CAND-SS-REQUIREMENT-04` 的 merge_retire 未闭环；六域总体放行保持阻断。

## 2026-07-21：CYCLE-SS-06 全链路收口与六域最终验收

- 全量 post-delete 发现并纠正 `requirement-gap-rules` 漏删：细则迁入 `requirement-intake-rules` 的 `gap-routing`，旧 source 真实删除，active-consumers、asset inventory、manifest 和根规划同步。
- 全量 baseline、trigger、post-delete 和字典通过；六域最终审查与最终验收文档已落盘。

## 2026-07-22：总控层 Skill 单向路由精简与两组合并

- 将并行分类与子代理真实生命周期合并到 `parallel-task-dispatch-rules`，迁移脚本、references、examples 和 Agent 元数据后删除 `subagent-dispatch-rules`。
- 将规则文件和项目记忆骨架自举合并到 `project-rule-file-bootstrap-rules` 的 `rule-bootstrap` / `memory-bootstrap`，迁移模板后删除 `project-memory-file-bootstrap-rules`。
- 修复压缩恢复无条件调用新会话预热的冲突；入口、阶段、自治、Git、实现审查、合规、代码收口、注释和最终输出完成引用化去重。
- 14 个最小任务均完成 TEST / REVIEW / ACCEPT；总控 validator 的 baseline、trigger、post-delete、15 个 quick validate、11 个工程文档 profile、字典和活跃消费者清零检查通过。
- 字典从 75 降为 73，`planned_missing=0`；当前轮没有 Git 写历史授权，改动保持未提交；Obsidian 仍因 `VAULT_NOT_REGISTERED` 仅阻断 vault 沉淀。
- 最终收口复验：独立当前改动审查 P0=0、P1=0，review 与 final_acceptance 严格 profile 均 PASS；子代理生命周期为计划/启动/完成/关闭 6/6/6/6、最大同时活跃 4；项目当前状态更新为全部完成且无待办。

## 2026-07-22：最终总结 Mermaid 图形化任务转为保留交接

- `reasoning-summary-structure-rules` 的图形化实现、Quick Validate、YAML、基础差异和字典已完成；当时尚待 Mermaid CLI 真实解析、独立只读审计、Obsidian 判断和最终验收。
- 当前需求域精简任务接管 `PROJECT_CURRENT.md` 前，已将上述未完成项保留为独立交接事实；本轮不回退、不覆盖其现有未提交改动，也不把它伪报为已经最终放行。

## 2026-07-22：模型无关会话重命名工具落地

- 保留 `thread-title-rules` 为唯一自动触发 Owner，新增 `rename_current_thread` 本地 MCP 工具；模型只传 `title`，当前线程 ID 由可信 MCP 元数据解析。
- 工具通过 Codex App Server 的 `thread/name/set` 改名，禁止线程列表、路径、时间或标题相似度猜测，并保留 `set_thread_title` 单次兼容回退。
- 修复 Skill 联接路径与真实仓库路径不一致导致 MCP 入口未启动的问题；新增 stdio 握手回归，自动化测试 13/13 通过。
- 全局 `thread_session` MCP 已注册；持久化 `codex exec` 真实发现并调用返回 `RENAMED`，当前任务改名为“模型无关会话重命名”并经 `thread/read` 回读一致；一次性测试任务已归档。
- 非 GPT 工具调用模型当前未配置，因此跨模型实机验证未执行；Obsidian bridge 仍因 `VAULT_NOT_REGISTERED` 阻断沉淀，不影响本地实现。

## 2026-07-23：模型无关会话重命名工具最终放行

- 使用正式 `codex mcp add` 注册 `thread_session`，新持久化 Codex App 任务真实发现 `rename_current_thread`，schema 仅包含 `title`，调用返回 `RENAMED`，App 立即回读标题一致；两次一次性测试任务均已归档。
- Windows 清理改为等待真实退出并使用 `taskkill /t /f` 终止完整进程树；增加真实后代进程测试。JSON-RPC 解析拒绝合法 JSON 非对象响应，避免未捕获异常。
- `_meta` 明确仅属于 Codex App 宿主适配器信任边界，移除未声明的 turn metadata `threadId` 别名；活动旧原生优先路由清零，首次 `INVALID_TITLE` 重试与原生回退次数已消除歧义。
- MCP 自动化 16/16、Node 语法、Quick Validate、npm audit、UTF-8/YAML、字典、四个工程文档 profile 和 `git diff --check` 均通过；独立最终复审 P0/P1/P2 均为 0，Skill 合规与项目改动审查 PASS。
- 当前模型选择器仅提供 GPT 系列，因此非 GPT 实机验证继续标记为环境不具备；本结论只放行 Codex App 第一版，不扩展到其他宿主。

## 2026-07-22：需求域 Skill 精简、旧路由收口与职责归位完成

- 保留 `requirement-intake-rules`、`requirement-boundary-rules`、`requirement-splitting-rules`、`requirement-change-rules` 四个独立自动触发 Owner；discovery 与 gap 继续作为 Intake 内部 `initial-discovery` / `gap-routing` 条件路由，不恢复退役顶层 Skill。
- 新增需求域共享契约和三个直接 Gap 支持 reference，删除 `initial-discovery-domain-routing.md` 与 `gap-routing-source/` 迁移快照；13 个冻结活跃消费者全部迁移，两个旧名称的活跃命中均为 0。
- 专项验证器补齐真实自然语言路由、重复 fixture 与名称自证负向、LF/CRLF 工作树指纹、6 个候选 worktree hash、消费者/保护契约精确集合、22 个 reference 精确集合与递归可达性、唯一 Agent、无 scripts 以及拆分/变更全树职责负向门禁。
- baseline、trigger、consumer、reference、post-cleanup 五阶段全部 `valid=true`；九个相关 Skill Quick Validate、十二个工程文档严格 profile、UTF-8/YAML/JSON/Python AST、字典和 `git diff --check` 通过，字典保持 `implemented_total=73`、`planned_missing=0`；共享工作树当前 `seed_total=34`，范围外新增种子未改变需求域 Owner 数量。
- 十二个最小任务完成实现、真实测试、审查和验收闭环；最终独立只读复审 P0=0、P1=0，最终当前改动审查和最终验收均 PASS。当前轮未授权 Git 写历史，改动保持未提交；Obsidian 因 `VAULT_NOT_REGISTERED` 只阻断 vault 沉淀。

## 2026-07-23：Codex Desktop 任务悬浮窗断点恢复进入真实重启验收

- 新增 `task-plan-rehydration-rules`，以 `PROJECT_CURRENT.md` 唯一托管区保存当前周期步骤、顺序和三态状态；恢复时由 Agent 真实调用 `update_plan` 重建悬浮任务列表。
- 投影脚本完成严格 UTF-8、字段白名单、敏感字段拒绝、SHA-256 指纹、51,200 字节闸门、原子替换、失活和五个 CLI 子命令；17 项单元测试通过。
- 项目记忆、自举、连续执行、上下文恢复和运行时恢复完成职责接入；UI 重建不恢复执行授权，也不等同于 L5 resume，进行中步骤必须先核验。
- 六个受影响 Skill quick validate、临时目录自举幂等、字典生成和 `git diff --check` 通过；严格追踪修复定向回归 3/3 通过。
- `TASK-RTP-01` 至 `TASK-RTP-07` 已完成阶段审查与验收；活动投影推进到 `TASK-RTP-08 in_progress`，等待用户真实关闭并重开 Desktop 后完成首次继续回合验收。

- 2026-07-25：完成 CYCLE-RTP-06 长任务自动 Goal 优先升级实现。新增无写入 `probe-timeout`、严格 600 秒边界、Goal 单次创建/复用/失败降级、脱敏摘要与跨项目 standing authorization；63 项回归、Skill 校验、字典、严格文档门禁、真实 Goal 工具链和测试投影清理通过。Computer Use 禁止自动操作 Codex 应用，独立视觉确认保持 LIMITED；Obsidian 沉淀因固定 vault 未注册而阻断，工作树保持未提交。

- 2026-07-26：确认 `BUG-PLAN-WAIT-20260726-001` 的原会话时间线：Plan Mode 决策选择框返回 `{"answers":{}}` 后错误进入“结果与结论”总结并结束任务。冻结永久等待状态契约：决策调用完全省略 `autoResolutionMs`；空答案、缺失答案和宿主隐式超时只能立即串行重发同一选择框；部分答案保留并只重发剩余问题；未决期间禁止总结、`final_answer`、`task_complete`、默认选择、Goal 和任务投影恢复。
- 2026-07-26：完成 `CYCLE-PMW-01` 的文档与规则切片：新增 Bug、验收、实施总览、周期和专项测试资产；`implementation-planning-rules`、`reasoning-summary-structure-rules` 与 Agent 提示加入 `RULE-PMW-001..004`、`AC-PMW-001..007`、`SUMMARY-GATE-PMW-001`。专项行为回归 10/10、四份工程文档 profile、Skill quick validate、UTF-8、Python AST 和 `git diff --check` 通过；真实 Desktop 两个以上空答案周期尚未验证，整体状态保持 `LIMITED`，未执行 Git 历史写入。
- 2026-07-26：本轮 Obsidian bridge `doctor` 返回 `VAULT_NOT_REGISTERED`，固定 vault `D:\obsidian_data` 检索/沉淀按规则阻断，未使用文件系统 fallback；该限制不影响项目本地四件套和本地回归证据。

- 2026-07-26：完成 `TASK-PMW-03` 与 `TASK-PMW-04` 的本地收口。专项测试 README 的 `test` profile、最终验收文档 `ACCEPT-PMW-FINAL-001`、实现审查 `REVIEW-PMW-001`、当前改动总审查 `REVIEW-PMW-002` 均已落盘并通过对应门禁；任务投影脚本已将当前会话状态更新为 `TASK-PMW-01/02/03 completed`、`TASK-PMW-04 in_progress`。自动回归仍为 10/10，真实 Desktop `TEST-PMW-013` 尚未执行，周期与最终验收保持 `LIMITED`，未执行 Git 历史写入。
- 2026-07-26：复核 `TASK-PMW-02/03/04` 的任务证据类别并补齐 `EVD-TASK-PMW-*-IMPL/TEST/REVIEW/ACCEPT` 的逐项稳定 ID；实施周期、两份审查和最终验收 strict profile 重新通过，八份工程文档 profile 均为 `valid: true`、`LIMITED`。专项回归保持 10/10，真实 Desktop `TEST-PMW-013` 仍未取得证据，未执行 Git 历史写入。
- 2026-07-26：针对复核发现的冻结集合标识缺口，将 `result_and_conclusion` 与中文“结果与结论”显式同步到规划 Owner、总结 Owner、Agent 提示、专项消费方测试和项目稳定记忆；专项回归仍为 10/10，八份工程文档 strict profile、两个 Skill quick_validate、AST、YAML、UTF-8 与 `git diff --check` 均通过。真实 Desktop `TEST-PMW-013` 仍未执行，周期继续保持 `LIMITED`，未执行 Git 历史写入。
- 2026-07-26：尝试执行真实 Desktop `TEST-PMW-013`；`computer-use` 初始化成功，但安全规则禁止自动化 Codex Desktop/扩展，无法取得宿主空答案周期和最终选择恢复证据。按既定边界保持 `LIMITED/HOST_BLOCKED`，不创建伪造通过证据，也未执行 Git 历史写入。

## 2026-07-26：Browser Use Cloud 专属路由与收费安全能力落地

- 新增 `browser-use-cloud-rules`、只读预检脚本和 local mock 测试，只接 Browser Use Cloud，不安装或接入本地 Browser Use。
- 统一浏览器矩阵新增 Cloud 专属分支；真实 Chrome、DevTools、本地核心自动化和本地高级验证继续由原 Owner 接管，Cloud 不作为故障后备或安全策略绕过手段。
- 每次 `run_session`、`send_task` 前分别检查本机 `BROWSER_USE_API_KEY`、Billing、当前动作可写硬费用上限并取得当次确认；无硬上限默认停止，免费层也不跳过确认。
- 14 个 local mock 单元测试、8 个正负 trigger fixture、7 个相关 Skill 校验和两个实施周期 strict 门禁通过；未配置真实 key、未调用真实 Cloud、未消费额度、未执行 Git 历史写入。

## 2026-07-26：任务悬浮窗首次持久化即同步进入周期 07

- 用户反馈会话约 29 分钟仍未看到任务悬浮窗，确认旧口径把十分钟异常修复误当作正常首显入口；冻结“`confirmed` 后首个领域动作前持久化当前 session，写盘成功后的下一动作立即 `update_plan`”硬闸门。
- 新增 `ensure-start`、显式 `--session-id` 优先与 `CODEX_THREAD_ID` 回退、冲突/缺失失败关闭、payload 返回和一次性完成收口；保留 v1-v4 兼容、`UI_SYNC_BLOCKED`、active/blocked/inactive 可见性和十分钟异常修复边界。
- 新增/更新周期 07、Bug、需求与验收文档；投影专项回归 69/69、三个 Skill 校验、字典、UTF-8、文档 strict profile 和 `git diff --check` 通过；真实 Desktop 首显证据受宿主自动化限制，状态保持 `LIMITED/HOST_BLOCKED`。
- 当前工作树保留未提交状态，未执行 Git 历史写入；Obsidian 固定 vault 未注册，本轮不绕过 CLI 写入。

## 2026-07-26：结果与结论适中详细度切片完成

- 完成 `REQ-SUMMARY-DETAIL-001`：`reasoning-summary-structure-rules` 的结果区默认保持 3 句，复杂、受限或存在关键边界时按事实扩展至 4–5 句，固定覆盖“解决了什么、采用什么方法、结果/验证状态如何”。
- 规则、模板、条件说明、公开示例和专项测试均已同步；空泛“已完成”、超过五句、复制完整测试清单、逐文件改动和执行流水账的候选均有拒绝边界，既有总结顺序、图形化条件和 `WAITING_DECISION` 闸门保持不变。
- 专项回归 9/9、Skill quick_validate、Python 编译、目标差异检查、六份工程文档 strict、实现审查和最终验收均通过；真实模型输出、Desktop UI 和外部服务不在本来源对象范围内。
- 当前会话结果详细度投影已在完成 payload 传递给 `update_plan` 后迁移为 `inactive`，三个任务均为 `completed`；未执行 Git 历史写入，Obsidian 沉淀因固定 vault `VAULT_NOT_REGISTERED` 继续阻断。
- 2026-07-28：完成代码位置目录规则 V2 的微业务 RPC 升级。后端业务域新增按需扁平 `business/<domain>/rpc/`，跨域仅允许精确导入目标域 `rpc/`，请求与响应均为 JSON 字符串并遵循 `Response{code,status,message,data}` 语义。Catalog、CLI、严格检查、`micro_business.py check`、CodeGraph 导入审查与 Go fixture 已同步；本地 unittest 21/21 通过。固定 Obsidian vault 未注册，未进行 vault 沉淀；未执行 Git 历史写入。

- 2026-07-28：代码位置目录规则 V2 的微业务 RPC 升级完成最终本地收口。需求、实施、测试、实现审查和最终验收文档 profile 均通过；`package-structure-rules` 与 `micro-business-architecture-rules` 的 `quick_validate.py` 均通过；当前会话 `PSR-RPC-003` 投影已失活。未连接外部服务，未执行 Git 历史写入。

- 2026-07-29：完成代码位置目录规则 V2 的旧项目渐进采纳升级。新增 `adoption` 只读检查与固定收敛清单 `doc/1-架构/3-目录规则收敛清单.yaml`：已采纳 V2 路径可原地扩展，遗留源码只可维护快照，新业务与独立新逻辑必须进入 Catalog 唯一位置。30 项本地行为测试、Python 编译、两个 Skill 快速校验及五类工程文档严格 profile 均通过；未迁移业务项目、未连接外部服务，未执行 Git 历史写入。

## 2026-07-29：后端根治理文件目录规则完成

- 后端独立项目根固定纳入 `AGENTS.md`、`PROJECT_CURRENT.md`、`PROJECT_MEMORY.md`、`PROJECT_HISTORY.md`，并将 `PROJECT_STYLE.md` 设为条件文件；五项均以 Catalog 文件节点登记，`init` 只创建位置且不覆盖正文。
- 规则目录树、Catalog、CLI、测试、需求、实施、审查和验收材料已同步。37 项本地行为测试与 Python 编译通过；未连接外部服务，未执行 Git 历史写入。

## 2026-07-29：三类项目双平台规则文件目录规则完成

- 前后端同仓、独立后端和独立前端项目根均固定纳入 `CLAUDE.md`，其位置由 Catalog 文件节点唯一查询；它与 `AGENTS.md` 同为必需提交文件，正文必须字节一致。
- `init` 只创建五个必需根文件的位置，`check --policy strict` 只读拒绝 `AGENTS.md` 与 `CLAUDE.md` 的正文漂移；`bootstrap_agents.sh --target both` 以 `AGENTS.md` 为同步源，重复执行保持幂等。
- 41 项本地行为测试、Python 编译、五类工程文档严格 profile、两个 Skill 快速校验和 `git diff --check` 均通过；未连接外部服务，未执行 Git 历史写入，Obsidian 固定 vault 仍未注册。

## 2026-07-31：后端数据存储目录扩展完成

- `database/connection/` 明确承载关系型数据库、Redis、Mongo 等数据存储服务的连接、连接池与客户端初始化；`database/model/` 固定只允许 `db/`、`redis/`、`mongo/` 三类模型叶子目录，Java 物理映射同步纠正到这三类目录。
- 独立 SQL 新增 `database/sql/field/{create,update,delete}/`，每个 SQL 叶子只接受直接 `.sql` 文件；自动迁移生产源码仍留在 `database/migration/` 并拒绝 SQL。
- Catalog、CLI、目录树、引用契约、测试、审查与验收已同步。48 项本地行为测试、Python 编译、公开查询、六类文档 profile、Skill 校验和 `git diff --check` 通过；未连接或修改任何真实数据服务，未执行 Git 历史写入。

## 2026-07-31：后端根 data 目录规则删除完成

- 后端根不再定义 `data/`、`data/business/`、`data/project/` 或 `data/seed/`；Catalog 将 `data` 固定为禁止路径，query、init 与 strict 均失败关闭。
- 前端 `src/data/`、业务域数据和 `doc/data/` 未受影响。50 项本地行为测试、Python 编译、根 data 负向 CLI、无写入哈希、审查和验收文档同步通过；未连接外部服务，未执行 Git 历史写入。

## 2026-08-01：研发流程收敛为实施计划、真实测试与 6-review

- 删除 `acceptance-criteria-rules`、`final-acceptance-rules`、`implementation-review-rules`、`project-change-review-rules` 和 `code-review-automation-rules`；活动流程统一为“实施计划（含 AC）-> 实现 -> 真实测试 -> 6-review -> 交付总结”。
- `doc/6-review/` 成为唯一活动风格回归目录，`code-style-consistency-rules` 只输出 `STYLE: PASS` 或 `STYLE: FIX_REQUIRED`；不承担业务正确性、需求覆盖或发布放行判断。
- `doc/6-审查/` 与 `doc/7-验收/` 原地只读保留，未批量改写历史资料；本地专项回归、严格文档 profile、字典生成与差异检查均通过，未连接外部服务且未执行 Git 历史写入。

## 2026-08-01：6-review 共享静态 Owner 路由完成

- `code-style-consistency-rules` 成为共享静态 Owner 路由与来源映射的唯一 Owner；测试后的 `6-review` 只消费风格子集。
- `continuous-code-quality-supervisor-rules` 删除重复路由，只在 Goal active 且用户明确要求“监控代码”时可选消费完整路由，继续负责扫描、脱敏、finding 指纹、去重和通知；它不是 `6-review` Gate。
- 本地共享路由单元测试 `7/7`、监控消费者单元测试 `17/17` 与跨域专项路由脚本通过；未改写历史 `doc/6-审查/`、`doc/7-验收/`，未连接外部服务或写入 Git 历史。

## 2026-08-01：根 test 目录统一完成

- 活动测试代码统一迁入根 `test/` 镜像目录，七组原 `*/tests/` 活动测试已迁移为 `*_test.py`；`doc/5-tests/` 只保留 README、日志、报告、截图和非可执行证据。
- 新增测试资产治理、历史 `doc/5-tests/` 可执行资产指纹清单、统一 Python 入口和 Go 根 `test/` 外部黑盒布局正负例；活动规则、Git 协作、Skill 合规、目录树、字典和项目文档已同步。
- 字典生成成功，全量 Python 测试 `187/187`、测试资产治理 `9/9`、七类严格文档 profile、旧 Go 阻断表达扫描、`git diff --check` 与 `git diff --cached --check` 均通过；Obsidian 固定 vault 未注册，未执行 vault 沉淀或 Git 历史写入。

## 2026-08-02：三类项目 doc 目录收敛

- fullstack、backend、frontend 的活动研发目录统一为 `doc/1-架构/` 至 `doc/6-review/`，条件图片目录统一为 `doc/data/images/`；`doc/6-审查/`、`doc/7-验收/` 保留为历史只读，不再进入活动骨架。
- 独立前端删除根 `data/business/project` 目录事实，后端独立项目补齐完整 `doc/` 子树；新增根目录契约测试和测试 README，CYCLE-15 同仓入口误判以最小分支修复并回归通过。
- 本地目录专项测试 `2/2`、入口回归 `5/5`；本轮未执行 Git 历史写入，Obsidian 固定 vault 未注册。
- 最终收口复验：实施总览、实施周期和 `6-review` profile 均返回 `valid: true`，根 Python 测试 `203/203` 通过，`git diff --check` 无错误；当前会话投影随后按 session 精确失活，未执行 Git 历史写入。
- 继续回合复核发现 CYCLE-16 周期文档和项目当前状态残留旧的 `in_progress/pending/待执行` 文案；已按现有验证证据同步为 `accepted/completed`，未扩大用户范围或执行 Git 历史写入。

## 2026-08-02：环境配置文件命名收敛完成

- 独立后端配置固定在 `config/`，同仓后端配置固定在 `backend/config/`；`yaml/` 使用 `config_<env>.yaml|yml`，Go `embedded/` 使用 `config_<env>.go`，明确 `local/test/prod` 常见环境示例、可扩展环境和 YAML/embedded 可不配对。
- `check` 保持只读，`init` 不生成动态环境配置文件；旧式 `config_test_yaml.go` 拒绝，秘密原值不进入提交资产。配置专项 `6/6`、目录 `2/2`、入口 `5/5`、根 Python `209/209`、文档 profile、Python 编译、Skill quick validation、CodeGraph sync 与 `git diff --check` 均通过。
- 当前会话投影 `REQ-PSR-CONFIG-ENV-001/CYCLE-17` 的五个任务已完成并按 session 精确失活；Obsidian 固定 vault 未注册，本轮未执行 vault 沉淀或 Git 历史写入。

## 2026-08-02：embedded 私密配置边界收敛启动

- 用户确认独立后端 `config/embedded/` 与同仓后端 `backend/config/embedded/` 允许源码直接配置 API key、密钥、密码等私密信息，源码配置为主且默认不依赖环境变量。
- YAML 仍禁止秘密原值；允许源码内秘密不扩大到 Agent 输出、日志、README、错误、测试报告或知识库，所有证据继续使用脱敏占位符。
- 已新增 `REQ-PSR-CONFIG-SECRET-001`、CYCLE-19、Catalog/Schema 策略字段和专项断言；本轮未执行 Git 历史写入，未连接外部服务。

## 2026-08-02：embedded 私密配置边界收敛完成

- 独立后端 `config/embedded/` 与同仓后端 `backend/config/embedded/` 已明确允许源码直接配置私密值，源码优先且默认不依赖环境变量；YAML 与外部输出继续禁止秘密原值。
- 配置专项 `7/7`、package-structure-rules 子目录回归 `16/16`、根 `test/` 子目录逐项回归 `212/212`、五类工程文档 profile、Skill quick validation、Python 编译和 `git diff --check` 均通过。
- CYCLE-19 需求、实施、测试、`6-review` 与项目记忆已完成脱敏收口；未连接外部服务、未执行 Git 历史写入，Obsidian 固定 vault 未注册。

## 2026-08-02：三类项目根 test 目录统一完成

- fullstack、backend、frontend 的活动测试代码统一落在项目根 `test/`；独立后端不建立 `backend/test/`，前后端同仓不建立 `backend/test/` 或 `frontend/test/`；`doc/5-tests/` 继续只保存说明和非可执行证据。
- Catalog、人工目录树、skeleton、query、render、init 和根目录契约测试已同步；根目录专项 `4/4`、入口回归 `5/5`、配置回归 `7/7`、根 Python 测试 `212/212`、测试 README profile、Skill 校验和 `6-review STYLE: PASS` 均通过。
- 本周期未迁移真实项目、未连接外部服务、未执行 Git 历史写入；Obsidian 固定 vault 未注册，沉淀按 bridge 规则阻断。
- 2026-08-04：用户确认独立后端项目关联工具统一落在 `common/util/`，与根 `utils/<package>/` 的项目无关工具包职责分离；已同步 `package-structure-rules` 的目录树、Catalog、Schema、CLI、相邻 `common-util-rules` 和活动测试，旧源码根 `util/` 保留为 adoption legacy 迁移边界，当前改动未提交。
