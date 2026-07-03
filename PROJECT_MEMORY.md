# 项目长期记忆

## 核心记忆

### 仓库定位
- 别名: skill 仓库, 团队研发协作规则仓库
- 类型: 项目事实
- 定义: 本仓库用于沉淀面向团队研发协作的 Skill、references、脚本和入口文档，目标是让 AI 在需求、Bug、编码、审查、测试、交付流程中按任务内容自动命中规则。
- 来源: `README.md`、`项目设计.md`
- 适用范围: 全仓库
- 更新时间: 2026-06-27
- 状态: 启用

### 根目录主入口
- 别名: 仓库入口文档
- 类型: 文档入口
- 定义: 仓库根目录长期主入口文档包括 `README.md`、`编码skill.md`、`字典.md`、`项目设计.md`、`PROJECT_MEMORY.md`、`PROJECT_STYLE.md`。
- 来源: 根目录真实文件结构
- 适用范围: 全仓库
- 更新时间: 2026-06-27
- 状态: 启用

### 研发产物目录正式口径
- 别名: doc 顶层目录规则
- 类型: 目录规则
- 定义: 正式研发产物目录统一收口到 `doc/` 下；当前正式活动子目录按流程顺序编号为 `doc/1-架构/`、`doc/2-需求/`、`doc/3-实施/`、`doc/4-bugs/`、`doc/5-tests/`、`doc/6-审查/`、`doc/7-验收/`。
- 来源: `artifact-storage-rules/references/path-map.yaml`
- 适用范围: 文档归档与规则引用
- 更新时间: 2026-06-28
- 状态: 启用

### 活动文档命名前缀
- 别名: 来源对象标识, 实施需求标识, 审查时分秒, Bug 进入实施验收
- 类型: 命名规则
- 定义: 需求、实施、Bug、测试、审查、验收等活动产物统一使用 `YYYY-MM-DD_HHmmss` 时间前缀。实施、审查、验收这类下游文档必须在时间后保留来源对象标识，来源可以是需求也可以是 Bug；来源对象标识不重复前置时间戳，优先使用来源中文主干或短 ID，必要时加 `需求-` 或 `Bug-` 类型前缀。典型格式为 `YYYY-MM-DD_HHmmss_<来源对象标识>_实施周期NN_周期说明.md`、`YYYY-MM-DD_HHmmss_<来源对象标识>_<审查中文主题>.md`、`YYYY-MM-DD_HHmmss_<来源对象标识>_最终验收.md`；禁止只写 `时间_阶段_说明.md`、`YYYY-MM-DD_主题.md` 或缺少来源标识的 `YYYY-MM-DD_HHmmss_主题.md`。
- 来源: `artifact-storage-rules/references/path-map.yaml`、`artifact-storage-rules/references/naming-templates.md`
- 适用范围: 需求域、实施域、Bug 域、测试域、审查域、验收域
- 更新时间: 2026-06-29
- 状态: 启用

### 架构专题文档规则
- 别名: architecture-doc-rules, 架构文档目录
- 类型: 文档规则
- 定义: `architecture-doc-rules` 专门负责 `doc/1-架构/` 下的长期架构专题文档。四个有序中文主入口固定为 `1-总架构.md`、`2-目录树.md`、`3-模块职责.md`、`4-主要业务链路.md`；业务链路从序号 `5` 开始，同一链路保留原编号更新，新增独立链路取当前最大业务链路编号加一并回写索引，历史编号不复用、不重排。其他长期专题使用 `附录-<架构中文主题>.md`，不占用业务链路编号。根目录 `项目设计.md` 继续保持项目级总览入口。
- 来源: `architecture-doc-rules/SKILL.md`、`artifact-storage-rules/references/path-map.yaml`
- 适用范围: 架构域、项目设计域
- 更新时间: 2026-06-28
- 状态: 启用

### 需求主动侦察链路
- 别名: 老板式 idea 转需求, idea 侦察, 需求 discovery
- 类型: 流程规则
- 定义: 当用户只提出一句话 idea、粗略想法或老板式方向时，优先由 `requirement-discovery-rules` 主动侦察当前项目代码、文档、数据库线索、上下游服务、第三方调用、关联项目、GitHub、相关网站、官方 API 文档和用户补充路径或 URL，形成有证据来源的需求设计；外部资料默认遵循“官方文档/官网/自有仓库与站点优先，公共 GitHub 与社区资料只作补充”的优先级。已验证可复用的资料位置、数据库、URL、项目路径和侦察经验必须继续通过 `project-memory-rules` 回写长期记忆。
- 来源: 对话确认、`requirement-discovery-rules`
- 适用范围: 需求域
- 更新时间: 2026-06-28
- 状态: 启用

### 需求域第一入口
- 别名: 需求 skill 顺序, 需求前置入口
- 类型: 流程规则
- 定义: 当前对外统一流程为 `Idea/Discovery -> Intake -> 条件闸门 -> 验收标准 -> 实施 -> 测试 -> 审查 -> 最终验收`。其中需求域主流程收口到 `Idea/Discovery -> Intake`，条件步骤为 `Gap / Boundary / Splitting / Change`；`acceptance-criteria-rules` 负责前置验收标准，`implementation-planning-rules` 负责独立实施域，`final-acceptance-rules` 负责后置最终验收。内部默认仍以 `requirement-discovery-rules` 为第一入口；`requirement-intake-rules` 负责在 discovery 初稿后立即创建需求主文档，`requirement-gap-rules` 只处理主动侦察后仍无法补齐的关键缺口。需求阶段只允许读仓库、读资料、整理文档；不允许把 agent 猜测写成需求答案，也不允许“先做了再补需求”。需求主文档未真实落盘前，禁止进入实施规划与正式编码。需求、验收标准和实施计划完成后仍不得自动开工，必须等用户明确“开始实施/开始执行”后才能进入正式编码。
- 来源: `requirement-discovery-rules/references/requirement-domain-routing.md`、`编码skill.md`
- 适用范围: 需求域
- 更新时间: 2026-06-30
- 状态: 启用

### 需求临时缺口文档规则
- 别名: gap 临时文档, 缺口阻断文档
- 类型: 流程规则
- 定义: `requirement-gap-rules` 只处理 discovery 之后仍无法补齐的关键缺口；gap 阶段允许在 `doc/2-需求/` 下创建一份临时缺口文档，记录已侦察证据、待确认问题和阻断结论。用户确认并补齐后，必须先把稳定结论回填主需求文档，再删除临时缺口文档；未确认前不得删除，也不得继续进入验收标准、实施或最终验收。

### 双层验收规则
- 别名: 前置验收 + 最终验收, 验收双层机制, Bug 验收
- 类型: 流程规则
- 定义: 验收统一归入“验收”大类，分为前置 `验收标准` 与后置 `最终验收` 两层，来源对象可以是需求也可以是 Bug。前置验收标准由 `acceptance-criteria-rules` 生成并落到 `doc/7-验收/YYYY-MM-DD_HHmmss_<来源对象标识>_验收标准.md`；后置最终验收由 `final-acceptance-rules` 生成并落到 `doc/7-验收/YYYY-MM-DD_HHmmss_<来源对象标识>_最终验收.md`。测试和审查未完成时，最终验收必须阻断。
- 来源: `artifact-storage-rules/references/path-map.yaml`、`acceptance-criteria-rules`、`final-acceptance-rules`
- 适用范围: 验收域
- 更新时间: 2026-06-27
- 状态: 启用

### 实施开工授权与自动推进
- 别名: 开始实施确认, 开工授权, 最小任务自动推进, 长文本执行边界
- 类型: 流程规则
- 定义: 来源对象文档（需求或 Bug）、前置验收标准和实施总览/实施周期即使都已完成，也不构成自动开工授权；必须由用户在当前任务中明确说“开始实施”“开始实现”“开始执行”“直接做”“继续做完”或“按文档实现”，且当前任务已有执行计划、任务完成条件、任务停止 / 结束条件、最大推进边界和验证点，才允许从实施文档切入正式编码。实施规划阶段默认采用只读计划模式：禁止写代码、禁止边计划边试做，只允许读仓库、定依赖、列风险、拆任务、写实施文档。计划开头必须先写 agent 对当前问题的理解，至少交代问题 / 目标、本轮范围、非范围、当前优先闭环和关键假设 / 待确认点，再进入实施周期与最小任务拆分。实施周期是计划管理容器，不是默认执行粒度；真正执行单元必须先拆到最小任务，并优先按“依赖图 + 垂直切片”组织，避免按前端 / 后端 / 数据库水平分层堆计划。单任务尽量单次专注完成，默认控制在约 5 个文件以内；明显超过则继续拆分。凡是代码生成、修改或重构类任务，都必须显式计划真实测试，写清入口、环境、样本 / 数据来源和通过标准，`build`、`lint`、静态检查不算真实测试；只有纯文档、纯注释、纯排版、纯静态资源改名 / 搬运或不会影响运行结果的场景才允许免测；若计划涉及代码生成、修改或重构，“现状与落点”必须给出代码落点目录树，不能只写文件名或普通条目。若用户在当前轮显式提出“怎么做 / 先给计划 / 先出方案 / 先列步骤 / 这个怎么改”这类计划型问题，也必须先命中实施规划规则；若前置条件未齐，则输出受限计划 / 阻断计划，而不是不触发。若运行环境要求用 `<proposed_plan>` 等专用计划包裹输出，包裹层只负责渲染 / 协议，不能覆盖项目内计划结构；正文仍必须遵守 `implementation-planning-rules` 与模板字段。受限计划不得作为实施授权；用户即使明确采纳，agent 也只能先补齐缺失前置条件并将其升级为正式执行计划，未升级前禁止进入编码、改码、重构、测试实施或其他执行动作。若用户给出开工类指令但没有计划或任务停止 / 结束条件，必须先补本轮受限计划并停在计划收口处，不得直接实现或进入长文本无限执行。开工后按 `autonomous-execution-rules` 默认遵循“当前实施周期内最小任务A实现 -> 最小任务A真实测试 -> 最小任务A审查 -> 最小任务A验收 -> 最小任务B…… -> 当前实施周期收口 -> 下一实施周期”的自动串行闭环；每个最小任务都必须先完成自己的真实测试、审查、验收，才允许进入下一个任务。
- 来源: `autonomous-execution-rules`、`implementation-planning-rules`、`team-development-rules/references/routing-rules.md`
- 适用范围: 实施域、测试域、审查域、验收域
- 更新时间: 2026-07-03
- 状态: 启用

### 通用结束信号
- 别名: 结束即停, 不扩散下一步, 停止建议, 三类合法后续
- 类型: 流程规则
- 定义: 当用户明确表达“结束”“停止”“到此为止”“不要继续”“不要下一步建议”“不要扩散”等结束指令，或不存在三类合法后续时，该指令对 Codex、Claude Code、浏览器 agent、子 agent 或其他长文本 agent 通用；agent 必须停止自动继续、工具执行和扩散性后续建议，只保留必要的最小收口结论。最终收口只允许三类合法后续：原执行计划内未完成必需项、阻断项、用户显式要求的建议/backlog。可选优化、额外整理、未来迭代、体验提升、文档再润色等内容，若不属于原计划必需项，不得作为默认后续内容输出。无下一步时强制不输出“下一步状态”“下一步建议”“等待用户新指令”“无需继续动作”等占位文案，避免循环 loop 会话误触发。Codex goal 仅是运行时状态收口机制的一种特例；若当前环境存在 goal / plan / task 等显式状态机制，且已满足完成或阻断条件，必须按真实机制完成状态收口。
- 来源: `autonomous-execution-rules`、`reasoning-summary-structure-rules`、`skill-compliance-gate-rules`、`AGENTS.md`
- 适用范围: 多 agent 收口、最终总结、连续执行、skill 合规闸门
- 更新时间: 2026-06-29
- 状态: 启用

### 普通 Markdown 输出规则
- 别名: text 代码块禁用, 自然语言不用代码围栏, 输出格式规则
- 类型: 输出规则
- 定义: 普通说明、方案、流程、总结、审查报告、线程拆分和状态回报必须使用普通 Markdown 段落、列表、表格或引用块；不得用 ` ```text `、无语言代码围栏、缩进代码块或 HTML 包裹整段自然语言输出。代码围栏只用于真实代码、命令、配置片段、日志片段、JSON/YAML 等需要等宽保真的内容。该规则由 `reasoning-summary-structure-rules` 负责收口检查，并由 `project-agents-bootstrap` 同步进 `AGENTS.md` / `CLAUDE.md` 的“输出格式规则”章节。
- 来源: 用户截图确认、`reasoning-summary-structure-rules`、`project-agents-bootstrap`、`PROJECT_STYLE.md`
- 适用范围: 最终回复、中间进度、审查报告、线程拆分、仓库规则文件模板
- 更新时间: 2026-06-30
- 状态: 启用

### 并行执行闭环规则
- 别名: 并行识别必须真启动, 规划器加执行器, 子线程启动证据
- 类型: 流程规则
- 定义: `parallel-task-dispatch-rules` 只负责并行判定与线程拆分，不再允许单独停留在“识别出可并行”。本仓库默认处于 subagent 完全授权模式：用户已明确允许 agent 在任务可切分、写集不冲突、风险可控且环境支持时自动启动 subagent / delegation / parallel agent work；该项目级 standing authorization 视为满足工具显式授权条件。当并行判定为可并行或条件并行且无任务阻断时，必须继续联动 `subagent-dispatch-rules` 做真实启动判定并发起真实子线程 / 子代理执行，同时核对计划线程数、实际启动线程数与关闭/回收线程数。仅输出线程分配文案、`并行技能` 列表或口头启动说明，不视为真正并行已生效。并行识别不以固定 skill 映射为白名单；项目分析、找 Bug、需求完善侦察、资料/日志/调用链证据收集等任务，只要能拆成独立问题、独立证据来源、独立目录、独立模块或独立文件集，主 agent 必须优先形成只读 sidecar 子任务计划并在授权成立时真实委派。单一根因、需求边界、接口契约、schema 或架构方向等最终裁决仍由主 agent 串行负责。
- 来源: `parallel-task-dispatch-rules`、`parallel-task-dispatch-rules/references/task-classification.md`、`subagent-dispatch-rules`、`subagent-dispatch-rules/references/delegation-decision-matrix.md`
- 适用范围: 并行开发、并发审查、项目分析、需求侦察、Bug 分诊、sidecar 子任务分发
- 更新时间: 2026-06-30
- 状态: 启用

### 子 agent 启动计划脚本
- 别名: generate_subagent_plan, 批量委派计划, 中文任务名子 agent
- 类型: 工具规则
- 定义: `subagent-dispatch-rules` 在批量委派前优先运行 `subagent-dispatch-rules/scripts/generate_subagent_plan.py` 生成结构化启动计划。脚本只负责输出计划 JSON，不直接调用平台工具；真实启动仍由主 agent 读取计划后调用 subagent / multi-agent / thread 工具。脚本生成的 `agent_name` / `logical_agent_name` 默认使用“任务简要中文 + 线程标识”，用于主 agent 侧的中文逻辑命名与计划线程数核对；平台 UI 实际昵称仍以启动工具返回值为准。
- 来源: `subagent-dispatch-rules`
- 适用范围: 批量子任务委派、并行线程规划
- 更新时间: 2026-06-29
- 状态: 启用

### 子 agent 生命周期回收
- 别名: close_agent 回收, 子代理关闭, 已完成子线程释放
- 类型: 流程规则
- 定义: subagent 启动成功后，即使执行已完成，仍会继续占用并发槽位；主 agent 在结果回收并完成整合后，必须继续调用真实 `close_agent` / 等价关闭工具完成释放。`subagent-dispatch-rules` 的通过标准需要同时核对计划线程数、实际启动线程数与实际关闭线程数。
- 来源: `subagent-dispatch-rules`
- 适用范围: 所有真实子 agent / 并行代理执行场景
- 更新时间: 2026-06-29
- 状态: 启用

### 审查体系收口
- 别名: 审查链路
- 类型: 流程规则
- 定义: 默认审查链收口为 `implementation-review-rules`、`project-change-review-rules`、`artifact-delivery-gate-rules`、`skill-compliance-gate-rules`；实现自审与当前改动总审查在收口前必须真实落盘到 `doc/6-审查/`，不再允许仅在最终回复中口头保留通过结论。
- 来源: `README.md`、`项目设计.md`
- 适用范围: 审查域
- 更新时间: 2026-06-27
- 状态: 启用

### 提交前审查闸门与统一判定字段
- 别名: 审查闸门, 审查文档判定字段, 提交前审查检查
- 类型: 流程规则
- 定义: 执行 `git commit` 前，`pre_commit_gate.sh` 第 5 步校验 `doc/6-审查/` 下最近一份审查文档，要求文档包含统一判定字段：`审查结论: 通过`、`审查范围: <文件列表或等价范围说明>`、`是否允许提交: 是`、`阻断问题: <P0/P1 摘要，没有则写无>`；审查文档缺失、审查结论非通过、不允许提交或存在未解决 P0/P1 时阻断提交。审查文档由 `implementation-review-rules` 和 `project-change-review-rules` 在归档时写入统一判定字段。
- 来源: `git-collaboration-rules/SKILL.md`、`pre_commit_gate.sh`、`implementation-review-rules/SKILL.md`、`project-change-review-rules/SKILL.md`
- 适用范围: 提交流程、审查域
- 更新时间: 2026-07-01
- 状态: 启用

### README 改动日志时间戳格式
- 别名: README 日志格式, 提交日志时间戳
- 类型: 格式规则
- 定义: 根目录 `README.md` 改动日志每条记录格式固定为 `yyyy-MM-dd HH:mm:ss 提交标题`，时间戳使用当前北京时间；始终追加到改动日志末尾，不按时间回插旧位置。`pre_commit_gate.sh` 校验时剥除时间戳前缀后再与提交标题比较。
- 来源: `git-collaboration-rules/SKILL.md`、`branch-and-commit.md`
- 适用范围: 提交流程、README 维护
- 更新时间: 2026-07-01
- 状态: 启用

### 文档落盘闸门
- 别名: 归档闸门, 收口前落盘检查
- 类型: 流程规则
- 定义: 需求、Bug、测试、审查任务在最终收口前必须联动 `artifact-delivery-gate-rules`，核对主文档、配套 SVG、README 和证据路径是否已经真实落盘到 `doc/2-需求/`、`doc/4-bugs/`、`doc/5-tests/`、`doc/6-审查/`；未落盘不得判定任务完成。
- 来源: `artifact-delivery-gate-rules`、`README.md`
- 适用范围: 需求域、Bug 域、测试域、审查域
- 更新时间: 2026-06-27
- 状态: 启用

### 中间链路也受落盘闸门约束
- 别名: 中段归档闸门, 非主入口也要落盘
- 类型: 流程规则
- 定义: 文档落盘闸门不只约束需求入口、Bug 入口、测试总结和总审查入口；需求补齐/边界/拆分/变更、Bug 复现/根因/运行时诊断/修复建议/回归风险、测试策略/命名/程序/目录/散落资产治理等中间链路，只要已经形成应持久化结论，最终收口前同样必须联动 `artifact-delivery-gate-rules`。
- 来源: 本轮 skill 修订、`README.md`
- 适用范围: 需求域、Bug 域、测试域、审查域
- 更新时间: 2026-06-27
- 状态: 启用

### 提交级审查正式归档位置
- 别名: commit review 归档口径, 提交级专项审查出口
- 类型: 审查规则
- 定义: `code-review-automation-rules` 的正式长期输出已统一收口到 `doc/6-审查/`，文件名遵循 `artifact-storage-rules` 中央模板；不再写入项目根目录固定文件名 `code_review_result.md` 一类平行入口。
- 来源: `code-review-automation-rules`、`artifact-storage-rules/references/path-map.yaml`
- 适用范围: 审查域
- 更新时间: 2026-06-27
- 状态: 启用

### 记忆与风格更新方式
- 别名: 长期规则回写方式
- 类型: 维护规则
- 定义: 当用户后续调整某个指标、命名、目录口径或风格偏好时，必须更新原有记忆或风格词条，不新增同义冲突条目，也不保留并行旧口径。
- 来源: 对话确认、`project-memory-rules`、`project-style-rules`
- 适用范围: 长期文档维护
- 更新时间: 2026-06-27
- 状态: 启用

### Windows / WSL 执行边界
- 别名: Windows 普通命令优先 bash, Git Bash 优先, 执行类动作才进 WSL
- 类型: 环境规则
- 定义: 当项目代码位于 WSL 文件系统内且 agent 运行在 Windows 时，搜索、读写文件、规则检查、普通 git 盘点等非执行动作默认优先使用 Git Bash / bash；PowerShell 不作为普通仓库命令入口，只在 `.ps1`、Windows 专用 cmdlet、PowerShell profile / 编码初始化或用户明确要求时使用。只有编译、运行、启动程序、测试、调试，以及会真实启动运行时的依赖安装，才通过 `wsl.exe --cd /home/<user>/<project> <command>` 进入 WSL。面向用户输出的项目内文件引用按用户当前环境可打开的路径输出；项目在 WSL 且用户从 Windows 桌面访问时，Markdown 链接、普通文本路径、审查证据路径、截图说明和最终总结中的项目内文件路径都使用 `\\wsl.localhost\<distro>\home\<user>\<project>\...`，只有命令参数、WSL shell 上下文和日志原文保留 `/home/<user>/<project>`。纯 Windows 项目，或当前任务本身不需要启动/执行程序时，不应误触发 WSL 执行规则。
- 来源: 用户本轮确认、`windows-wsl-execution-rules/SKILL.md`、`windows-encoding-rules/SKILL.md`、`AGENTS.md`
- 适用范围: Windows + WSL 协作开发、仓库级执行规则、命令模板
- 更新时间: 2026-07-02
- 状态: 启用

### 项目内文件引用路径
- 别名: 用户可访问路径, WSL 文件引用, UNC 路径展示
- 类型: 输出规则
- 定义: agent 回复中凡引用项目内文件，都必须使用用户当前客户端可打开的项目访问路径，而不是机械沿用执行环境路径。项目在 Windows 本地盘时使用 Windows 本地路径；项目在 WSL 文件系统且用户通过 Windows / Codex Desktop / Claude Desktop 访问时，项目内文件引用统一使用 `\\wsl.localhost\<distro>\home\<user>\<project>\...`；`/home/<user>/<project>` 只用于 WSL 内命令、`wsl.exe --cd` 参数、WSL shell 日志或必须保留原文的执行上下文。
- 来源: 用户确认、`windows-wsl-execution-rules/references/path-mapping.md`
- 适用范围: 最终回复、中间进度、审查报告、证据路径、截图说明、Markdown 链接和普通文本文件路径
- 更新时间: 2026-07-02
- 状态: 启用

### 文件写入统一 UTF-8
- 别名: 跨平台 UTF-8 写入, 禁止 GBK/ANSI 落盘, 文件编码规则
- 类型: 环境规则
- 定义: 仓库所有代码、文档、配置、脚本、测试资产和生成类文本文件，新增或修改时默认使用 UTF-8 编码；Windows、Linux、WSL、容器和远程服务器上都必须保持同一口径，禁止用 GBK、ANSI、系统默认编码、编辑器默认编码或 shell 默认编码落盘。命令行写文件必须显式指定 UTF-8，写后回读关键文件并检查 `git diff`，确认中文未乱码、编码未漂移、换行未被意外批量转换。
- 来源: 用户本轮确认、`AGENTS.md`、`windows-encoding-rules/SKILL.md`、`windows-wsl-execution-rules/SKILL.md`
- 适用范围: 全仓库文件写入、规则文件自举、Windows / WSL / Linux 协作开发
- 更新时间: 2026-07-02
- 状态: 启用

### 会话自动重命名规则
- 别名: thread-title-rules, 会话标题自动更新, 任务中文简要
- 类型: 工作台规则
- 定义: 当前 Codex / Claude / agent 会话进入明确需求、Bug、实施、审查、测试、提交或其他可命名任务，且标题为空泛、过时、泛称或不匹配当前任务时，必须自动命中 `thread-title-rules`；由 agent 生成 8-24 字中文简要标题，并调用当前环境真实线程重命名工具更新当前会话标题。Codex 环境优先使用真实 `set_thread_title`。任务主题尚未稳定、标题已准确、工具不可用、无法可靠确定当前会话 ID 或用户明确禁止时跳过并说明原因；禁止用正文伪造工具调用或猜测结果宣称已改名。
- 来源: 用户本轮确认、`thread-title-rules/SKILL.md`、`project-agents-bootstrap/SKILL.md`
- 适用范围: 会话管理、任务检索、总控层自动触发、仓库规则自举
- 更新时间: 2026-07-02
- 状态: 启用

### 本地连接调试测试红线
- 别名: 只连 local, 禁连 test/prod, 本地服务联调, local 数据库
- 类型: 环境安全规则
- 定义: 需求侦察、Bug 复现 / 定位 / 运行时调试、功能验证、回归测试、上线接口测试、浏览器联调、启动前后端服务或执行测试脚本时，所有数据库、缓存、消息队列、HTTP/RPC 上游、前端 / 后端服务连接都只能使用 local 本地环境。`test`、`prod`、`production`、`staging`、`pre`、`release` 等非 local 环境一律禁止连接；即使用户提供临时连接信息或授权，agent 也不得直接连接，只能记录为环境阻断并要求改用 local。本地配置缺失、local 数据不足或本地服务未启动时，只能补齐 local 环境或阻断，不得回退到 test / prod。
- 来源: 用户本轮确认、`AGENTS.md`、`test-strategy-rules/SKILL.md`、`project-agents-bootstrap/SKILL.md`、`project-agents-bootstrap/scripts/bootstrap_agents.sh`
- 适用范围: 需求域、Bug 域、测试域、运行时调试、浏览器联调、Windows / WSL 执行命令
- 更新时间: 2026-07-01
- 状态: 启用

### URL 认证浏览器默认路由
- 别名: authenticated-url-routing-rules, 已登录 Chrome 路由, URL 默认 Chrome Plugin
- 类型: 浏览器路由规则
- 定义: 当用户提供任意 URL、链接或网页地址，并要求打开、读取、分析、总结、截图、提取内容、排查页面、查看文档、理解网页、检查资料、访问在线文档或处理已在浏览器登录过的页面时，默认优先触发 `authenticated-url-routing-rules`，并优先使用 `chrome:control-chrome` 接管用户已登录的真实 Chrome profile，复用登录态、扩展、权限和已打开标签页；只有 Chrome Plugin 不可用时，才回退到 `agent-browser --auto-connect`、state、profile 或 session。遇到登录页、权限页、验证码或人机验证时，不得用 `web`、搜索引擎、第三方转载或无登录态浏览器绕过权限。若 Chrome 已成功认领用户标签页但浏览器安全策略拒绝读取正文，必须停止绕过尝试，只报告 URL / 标题 / 认领状态和策略阻断事实，并将标签页保留为 handoff。后续执行中遇到并确认解决的 URL 认证、真实 Chrome 接管、登录态复用、权限页、正文读取策略或 handoff 问题，必须按“触发条件 -> 允许动作 -> 禁止动作 -> 收口证据”回写本 skill。
- 来源: 用户确认、`authenticated-url-routing-rules/SKILL.md`
- 适用范围: URL 分析、在线文档读取、浏览器权限页面、企业系统资料访问
- 更新时间: 2026-07-02
- 状态: 启用

## 术语表

### doc 顶层混合命名
- 别名: 中文语义优先命名
- 类型: 术语
- 定义: `doc/` 根目录保留英文，活动子目录采用“编号顺序 + 中文语义优先 + 工程通用域保留英文”的混合方案：`1-架构`、`2-需求`、`3-实施`、`4-bugs`、`5-tests`、`6-审查`、`7-验收`。
- 来源: 对话确认、`artifact-storage-rules`
- 适用范围: 文档目录命名
- 更新时间: 2026-06-28
- 状态: 启用

## 业务约束

### 旧目录处理规则
- 别名: 不保留兼容层
- 类型: 迁移约束
- 定义: 当目录迁移完成且用户未要求保留兼容入口时，应删除旧目录、旧占位文件和旧跳转文档，不保留并行旧包或兼容壳。
- 来源: 对话确认、`artifact-storage-rules`
- 适用范围: 目录迁移与收口
- 更新时间: 2026-06-27
- 状态: 启用

## 变更记录

- 2026-06-27：初始化根目录长期记忆文档，补齐 doc 顶层目录口径、审查链收口和长期规则回写约束。
- 2026-06-27：新增需求主动侦察链路，明确老板式 idea 先由 agent 查项目、数据、代码、上下游和补充路径，再形成需求设计并回写可复用侦察线索。
- 2026-06-27：明确 `requirement-discovery-rules` 是需求域第一入口，现有需求 skill 暂不合并为大 skill，改为通过路由 reference 收敛职责重叠。
- 2026-06-27：新增统一文档落盘闸门，明确需求、Bug、测试、审查收口前必须先核对正式文档已真实落盘；同时取消审查域“轻量通过可不落盘”的旧口径。
- 2026-06-27：补充“中间链路也必须过文档落盘闸门”的长期口径，并明确提交级专项审查正式归档到 `doc/6-审查/`，不再写项目根目录固定文件名。
- 2026-06-28：明确“需求/验收标准/实施计划完成不等于自动开工”，必须等用户明确“开始实施/开始执行”后才能进入编码；一旦开工，后续按实施周期自动串行推进实现、测试、审查与验收闭环。
- 2026-06-30：统一实施执行口径为“最小任务闭环优先于实施周期浏览”，并统一主执行链术语为“实现 -> 真实测试 -> 审查 -> 验收”。
- 2026-06-29：将实施执行粒度从“实施周期闭环”细化为“最小任务闭环”；实施周期继续作为文档管理容器，真正执行顺序改为每个最小任务依次完成实现、真实测试、审查、验收后再进入下一个最小任务。
- 2026-06-29：补充长文本执行边界；“开始实施/开始实现/开始执行/直接做/继续做完/按文档实现”等开工词必须有执行计划、任务完成条件、任务停止 / 结束条件和最大推进边界，缺少时先补受限计划并停在计划收口处，不得直接实现。
- 2026-06-29：新增并行执行闭环口径，明确 `parallel-task-dispatch-rules` 判定可并行后必须继续联动 `subagent-dispatch-rules` 做真实启动判定，不能只停留在文本规划；2026-06-30 补充工具授权优先级，真实启动需服从工具元数据。
- 2026-06-29：新增 `generate_subagent_plan.py` 启动计划脚本，明确批量委派先生成计划 JSON，再由主 agent 读取计划并真实启动；子 agent 名称默认使用任务简要中文。
- 2026-06-29：补充子 agent 生命周期口径，明确中文任务名属于主 agent 逻辑名，平台 UI 昵称由启动工具返回；结果收回后仍必须调用 `close_agent` 完成回收。
- 2026-06-30：扩展并行识别口径，明确并行不再依赖固定 skill 映射白名单；主 agent 在项目分析、找 Bug、需求完善侦察、证据收集等任务中必须自主识别可委派的只读 sidecar 子任务并优先尝试真实 subagent 并行。
- 2026-06-30：修正 subagent 自动启动口径，明确自动的是委派判定；真实启动必须服从当前工具元数据和授权策略。若工具要求用户显式授权，先检查当前轮授权与项目级完全授权；仅两者均不存在时，才回退本地执行并记录实际启动数为 0。
- 2026-06-30：根据用户确认启用 subagent 完全授权模式；项目级 standing authorization 视为满足工具显式授权条件，不再因缺少逐次 subagent 指令而回退本地执行。
- 2026-06-28：将正式活动文档目录迁移为 `doc/1-架构/` 到 `doc/7-验收/` 的编号顺序，并新增 `architecture-doc-rules` 承接长期架构专题文档。
- 2026-06-28：固定架构域四个中文主入口，补齐目录树、模块职责、主要业务链路示例，并明确单条业务链路的新增与更新策略。
- 2026-06-28：架构域文件改为固定顺序编号，基础入口占用 `1-4`，业务链路从 `5` 开始按最大编号加一，历史编号不复用、不重排。
- 2026-06-29：新增通用结束信号口径，明确“结束即停”不只适用于 Codex goal，也适用于 Claude Code、浏览器 agent、子 agent 等长文本收口场景。
- 2026-06-29：统一活动文档命名前缀为 `YYYY-MM-DD_HHmmss`，并要求实施、审查、验收等下游文档保留来源对象标识；来源可以是需求或 Bug，避免只看见阶段或审查主题而看不出来源对象。
- 2026-06-29：收紧无下一步收口口径，最终后续内容只允许原执行计划内未完成必需项、阻断项、用户显式要求的建议/backlog，其他可选优化不得默认输出。
- 2026-06-30：新增普通 Markdown 输出规则，明确自然语言结构化输出不得包进 ` ```text ` 等代码围栏，应使用 Markdown 段落、列表、表格或引用块。
- 2026-06-30：收紧需求阶段口径，明确“一次只推进一个关键问题”只允许基于真实缺口，不允许夹带 agent 猜测；需求主文档未真实落盘前，禁止进入实施规划与正式编码。
- 2026-06-30：收紧实施规划口径，明确计划阶段只读、最小任务优先按依赖图与垂直切片组织、单任务默认控制在约 5 个文件以内，且每个最小任务都必须先完成真实测试、审查、验收闭环后再进入下一个任务。
- 2026-07-01：历史上曾收紧为 PowerShell UTF-8 后承接普通命令；2026-07-02 已按新确认口径替换为 Windows 下普通仓库命令优先 Git Bash / bash，PowerShell 仅用于专项场景，执行类动作才进入 WSL。
- 2026-07-01：恢复 README 改动日志时间戳格式为 yyyy-MM-dd HH:mm:ss 提交标题；新增提交前审查闸门，pre_commit_gate.sh 校验 doc/6-审查/ 下审查文档的审查结论、是否允许提交、阻断问题；两个审查 skill 归档时统一写入判定字段。
- 2026-07-01：新增本地连接调试测试红线，明确需求、Bug、测试、运行时调试、启动联调和浏览器验证只能连接 local 本地数据库与本地服务，禁止连接 test / prod / staging 等非 local 环境。
- 2026-07-01：补充计划型提问入口，明确用户只要显式索要“怎么做/先给计划/先出方案/先列步骤”，就必须先命中实施规划规则；若前置条件未齐，也要输出受限计划 / 阻断计划，而不是表现成计划规则未触发。
- 2026-07-01：补充受限计划授权边界，明确受限计划不得作为实施授权；即使用户明确采纳，也必须先补齐前置条件并升级为正式执行计划，未升级前禁止进入编码、改码、重构、测试实施或其他执行动作。
- 2026-07-03：补充 Plan Mode 包裹口径，明确运行环境若要求用 `<proposed_plan>` 等专用计划包裹输出，包裹层不改变项目内计划格式；计划正文仍必须遵守 `implementation-planning-rules` 与模板结构。
- 2026-07-02：新增文件写入统一 UTF-8 口径，明确代码、文档、配置、脚本、测试资产和生成文本跨 Windows / WSL / Linux 默认 UTF-8，禁止 GBK / ANSI / 默认编码落盘，命令行写入后必须回读并检查 diff。
- 2026-07-02：新增会话自动重命名规则，明确任务主题稳定且标题泛化、过时或不匹配时自动命中 `thread-title-rules`，调用真实线程重命名工具改为 8-24 字中文简要；标题已准确、工具不可用或用户禁止时跳过。
- 2026-07-02：新增 URL 认证浏览器默认路由，明确用户提供 URL 时默认优先通过 Chrome Plugin 复用用户真实 Chrome 登录态，避免隔离浏览器或 `web` 丢失权限；补充 Chrome 安全策略拒绝正文读取时只报告阻断事实并 handoff，不做绕过；执行中已确认解决的问题必须继续回灌到 skill。
- 2026-07-02：补充项目内文件引用路径规则，明确 Windows 桌面访问 WSL 项目时，所有面向用户的项目内文件引用都用 `\\wsl.localhost\...`，`/home/...` 仅保留给 WSL 命令与日志上下文。
- 2026-07-02：更新上线接口测试门禁规则，新增项目基线资产库、参数依赖解析、可复用参数生命周期、失效持续更新和通用脚本复用优先口径。
- 2026-07-02：新增 Swag OpenAPI 全量维护规则，明确 `swag/` 为唯一正式输出目录，单接口完整 YAML、总 YAML 与 `.swag-manifest.yaml` 持续维护。
- 2026-07-02：补充上线测试与 Swag OpenAPI 双索引同步规则，明确 `swag/.swag-manifest.yaml` 与 `doc/5-tests/基线/interface-inventory.yaml` 理论上都不应缺失；任一缺失或三方接口集合不一致时，从当前代码刷新 swag 与测试基线两边。
- 2026-07-03：收紧 Swag OpenAPI 导入口径，明确单接口 YAML 导入 Apifox 时默认直入目标目录，不通过 `tags` 额外创建父目录；头部、请求参数、响应字段都必须有中文说明，源码注释不足时只允许受控推导。
- 2026-07-03：补充单接口 Swag 文件命名规则，默认采用“路径名 + 中文简要说明”格式；中文说明优先取显式 `summary`，缺失时允许受控推导，仍无法稳定得到时回退纯路径文件名并在 manifest 记录 `summary_source: unresolved`。


### 上线接口测试门禁规则
- 别名: project-release-test-rules, 上线测试门禁
- 类型: 测试域核心规则
- 定义: 上线前项目级全接口测试门禁，替代人工接口回归验证，输出上线准入结论。每个业务项目必须在 `doc/5-tests/基线/` 长期维护接口清单、参数来源、依赖图、可复用参数、场景目录、脚本适配、执行历史和变更日志；同时将 `swag/.swag-manifest.yaml` 与 `doc/5-tests/基线/interface-inventory.yaml` 作为当前代码接口事实的双索引，任一缺失、陈旧或接口集合不一致时，先刷新 swag 与测试基线两边。若目标接口参数无法直接确定，agent 必须按 `reusable_param -> upstream_api -> local_database -> local_cache -> openapi_example -> fixture -> rule` 解析，并把来源写入依赖追踪；已测试通过的参数可持续复用，但必须有 `candidate/reusable/stale/invalid/quarantined/retired` 生命周期、复验、失效归因和持续回写机制。已有通用脚本能力优先复用，缺能力时扩展 `project-release-test-rules/scripts/generate_release_test_plan.py` 的通用子命令，不为每次上线重复生成一次性脚本。
- 来源: `project-release-test-rules/SKILL.md`、`project-release-test-rules/references/baseline-asset-rules.md`、`project-release-test-rules/scripts/generate_release_test_plan.py`
- 适用范围: 全项目上线前接口测试、回归验证、上线准入判定
- 更新时间: 2026-07-02
- 状态: 启用

### Swag OpenAPI 全量维护规则
- 别名: swag-openapi-maintainer-rules, 更新 swag, OpenAPI YAML 资产
- 类型: API 文档资产规则
- 定义: 当用户要求生成、补齐、刷新、维护项目 swag，或导出 Apifox / OpenAPI / Swagger YAML 时，触发 `swag-openapi-maintainer-rules`。该 skill 负责从当前代码真实路由、controller、请求 DTO、响应 DTO、统一响应包装和鉴权中间件读取接口契约，维护项目根目录 `swag/` 作为唯一正式输出目录；每个接口一个可独立导入 Apifox 的完整 YAML，同时维护 `swag/openapi.yaml` 全量总文件和 `swag/.swag-manifest.yaml` 路由到文件映射。单接口 YAML 默认不写 operation `tags`，导入 Apifox 时直接进入用户选中的目录；单接口文件名默认采用“路径名 + 中文简要说明”格式，中文说明优先取显式 `summary`，缺失时允许受控推导，仍无法稳定得到时回退纯路径文件名并在 manifest 记录 `summary_source: unresolved`。总 YAML 可保留 `tags` 做全量分组。头部、请求参数、响应字段都必须补齐中文说明，源码注释不足时允许受控推导，但不得编造业务规则。当前代码是唯一真相源，禁止凭历史记忆或旧文档补字段；若项目存在上线测试基线，刷新 swag 后必须同步或提示同步 `doc/5-tests/基线/interface-inventory.yaml`。
- 来源: `swag-openapi-maintainer-rules/SKILL.md`
- 适用范围: HTTP API 文档导出、Swagger/OpenAPI 资产维护、Apifox YAML 导入
- 更新时间: 2026-07-03
- 状态: 启用
