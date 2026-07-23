# 项目历史事件

> 本文件只追加关键历史事件。普通新线程默认不读取，只有历史追问、当前状态不足或真实卡点时才窄检索。

## 事件

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
