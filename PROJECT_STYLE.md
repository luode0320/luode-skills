# 项目风格记忆

## 核心风格

### 中文优先表达
- 别名: 中文主表达
- 类型: 文档风格
- 示例: `## 核心风格`、`- 说明:`、`- 更新时间:`、`PROJECT_STYLE.md`
- 说明: 仓库长期维护以中文阅读为主，规则说明、记忆字段和风格字段应优先使用中文，减少理解成本。
- 来源: `README.md`、`project-memory-rules`、`project-style-rules`
- 适用范围: 根目录说明文档与长期记忆文档
- 更新时间: 2026-06-27
- 状态: 启用

### doc 顶层混合命名
- 别名: 文档目录混合命名
- 类型: 目录风格
- 示例: `doc/1-架构/`、`doc/2-需求/`、`doc/3-实施/`、`doc/4-bugs/`、`doc/5-tests/`、`doc/6-审查/`、`doc/7-验收/`
- 说明: `doc/` 根目录保持英文，活动子目录按流程顺序加数字前缀；中文语义目录保留中文，`bugs`、`tests` 这类工程高频词保留英文，避免脚本和协作摩擦。
- 来源: 对话确认、`artifact-storage-rules/references/path-map.yaml`
- 适用范围: 文档目录命名
- 更新时间: 2026-06-28
- 状态: 启用

## 命名与注释

### 根文档命名习惯
- 别名: 仓库入口文档命名
- 类型: 命名风格
- 示例: `README.md`、`编码skill.md`、`字典.md`、`项目设计.md`、`PROJECT_MEMORY.md`、`PROJECT_STYLE.md`
- 说明: 根目录入口文档允许中英文混合命名，但承担长期说明职责的中文语义文档优先使用中文标题与中文内容。
- 来源: 根目录真实文件结构
- 适用范围: 仓库入口文档
- 更新时间: 2026-06-27
- 状态: 启用

### 架构文档中文稳定命名
- 别名: 架构主入口命名, 业务链路文档命名
- 类型: 文档命名风格
- 示例: `doc/1-架构/1-总架构.md`、`doc/1-架构/2-目录树.md`、`doc/1-架构/3-模块职责.md`、`doc/1-架构/4-主要业务链路.md`、`doc/1-架构/5-业务链路-订单支付.md`
- 说明: 架构域四个主入口固定占用序号 `1-4`；业务链路从 `5` 开始按最大编号加一。同一链路保留原编号更新，历史编号不复用、不重排；其他长期专题使用 `附录-<架构中文主题>.md`，不占用业务链路编号。
- 来源: `artifact-storage-rules/references/path-map.yaml`、`architecture-doc-rules`
- 适用范围: `doc/1-架构/`
- 更新时间: 2026-06-28
- 状态: 启用

### 规则调整回写原条目
- 别名: 增量回写
- 类型: 维护风格
- 示例: `- 更新时间: 2026-06-27`、`- 状态: 启用`、`- 变更记录: 直接回写原条目`
- 说明: 长期规则文档追求单一真相源，规则变更应表现为原条目回写，而不是新增平行旧口径。
- 来源: 对话确认、`project-memory-rules`、`project-style-rules`
- 适用范围: `PROJECT_MEMORY.md`、`PROJECT_STYLE.md` 及根目录主入口文档
- 更新时间: 2026-06-27
- 状态: 启用

## 工具调用

### 字典刷新命令
- 别名: skill 字典刷新
- 类型: 工具风格
- 示例: `python skill-dictionary/generate_dictionary.py`
- 说明: 新增、删除或明显调整 skill 后，统一用仓库已有脚本刷新 `字典.md` 与 `skill-dictionary/data.js`，不手工维护统计值。
- 来源: `README.md`
- 适用范围: 字典与统计同步
- 更新时间: 2026-06-27
- 状态: 启用

### 子 agent 状态公告写法
- 别名: subagent 公告, 逻辑名平台昵称双写
- 类型: 工具风格
- 示例: `Subagent 状态：\n- 已启动：019f...\n- 逻辑名：端到端子代理启动-A\n- 平台昵称：Avicenna\n- 线程：A\n- 执行 skill：subagent-dispatch-rules`
- 说明: 子 agent 公告默认同时写 `逻辑名` 与 `平台昵称`。逻辑名来自脚本或主 agent 计划中的中文任务名，平台昵称来自真实启动工具返回值；完成公告还要补 `回收：已调用 close_agent`。
- 来源: `subagent-dispatch-rules`
- 适用范围: 子 agent 启动、完成、回收进度消息
- 更新时间: 2026-06-29
- 状态: 启用

### 子 agent 完全授权写法
- 别名: subagent 显式授权, 自动授权, 完全授权模式
- 类型: 工具风格
- 示例: `子线程启动:已启动2个/计划2个/实际2个`、`授权:项目级完全授权模式已生效`
- 说明: 本仓库默认完全授权 subagent 自动启动；当任务可切分、写集不冲突、风险可控且环境支持时，主 agent 应将项目级 standing authorization 视为满足工具显式授权条件，不再因为当前轮没逐字说 subagent 而回退。
- 来源: `subagent-dispatch-rules`
- 适用范围: subagent 启动判定、并行回退公告、最终执行证据
- 更新时间: 2026-07-03
- 状态: 启用

### 命中检查可见输出样式
- 别名: skill-hit-check 输出, 首条中间进度样式
- 类型: 工具风格
- 示例: `**Skill 命中检查**`、`命中检查:通过; Git规则:不适用`、`命中技能:skill-hit-check-rules,parallel-task-dispatch-rules`、`并行技能:无`
- 说明: `skill-hit-check-rules` 的首条可见输出使用普通 Markdown 标题 + 行内代码字段行；不得包进 fenced code block 或缩进代码块，避免出现横向滚动代码块和局部自动链接。
- 来源: `skill-hit-check-rules/templates/hit-check-template.md`、用户截图确认
- 适用范围: `skill-hit-check-rules` 首条中间进度和相关输出示例
- 更新时间: 2026-06-30
- 状态: 启用

### 会话标题中文简要写法
- 别名: thread-title 命名, 任务标题自动命名, 会话重命名
- 类型: 工具风格
- 示例: `会话自动重命名规则`、`超大单 sheet 导出`、`稳定币费率异常`、`审查-超大单导出`、`提交-费率修复`
- 说明: 会话标题使用“任务对象 + 动作 / 症状 / 阶段”的 8-24 字中文简要，不默认加项目名，不只写泛化动作。避免 `提交 git`、`开始实施`、`继续做`、`修复 bug`、`更新文档` 这类只表达动作、不表达任务对象的标题。标题变更必须来自真实线程重命名工具；Codex 优先使用 `set_thread_title`，若首屏未直接暴露 `set_thread_title` 或 `list_threads`，先经 `tool_search` 发现线程工具，再决定改名或跳过；Claude Code 仅在存在真实改名工具时执行，Claude Desktop 默认记录“平台无真实自动改名工具”并跳过。工具不可用或标题已准确时只记录跳过。
- 来源: 用户本轮确认、`thread-title-rules/SKILL.md`
- 适用范围: Codex / Claude Code / Claude Desktop 跳过证据 / agent 会话标题、任务检索、最终执行证据
- 更新时间: 2026-07-03
- 状态: 启用

### 普通说明不用代码围栏
- 别名: text 代码块禁用, 普通 Markdown 输出
- 类型: 输出风格
- 示例: `发现:`、`- [P1] 文件:行 - 问题标题`、`后续内容:`、`1. ...`
- 说明: 普通说明、方案、流程、总结、审查报告、线程拆分和状态回报使用 Markdown 段落、列表、表格或引用块；不得用 ` ```text `、无语言代码围栏、缩进代码块或 HTML 包裹整段自然语言。代码围栏只用于真实代码、命令、配置、日志、JSON/YAML 等需要等宽保真的片段。
- 来源: 用户截图确认、`reasoning-summary-structure-rules`、`project-agents-bootstrap`
- 适用范围: 最终回复、中间进度、审查报告、线程拆分、仓库规则文件模板
- 更新时间: 2026-06-30
- 状态: 启用

### Windows 命令分层写法
- 别名: Windows 普通命令优先 bash, Git Bash 优先, 执行类再 wsl.exe
- 类型: 工具风格
- 示例: `普通命令: 在 Git Bash / bash 下经 //wsl.localhost/<distro>/home/<user>/<project> 或等价 Windows 可访问路径执行 rg、git status、读写文件；执行类命令: wsl.exe --cd /home/<user>/<project> go test ./...；PowerShell: 仅用于 .ps1、Windows 专用 cmdlet、profile / 编码初始化或用户明确要求`
- 说明: Windows + WSL 规则文案要先写清“普通命令”和“执行类命令”的分层。Windows 下搜索、读写文件、规则检查、普通 git 盘点默认优先使用 Git Bash / bash；只有编译、运行、启动程序、测试、调试和执行类依赖安装才切到 `wsl.exe --cd`；PowerShell 只作为 Windows 专项入口保留。同时明确纯 Windows 项目或本轮不执行程序时不要误触发 WSL；面向用户展示的项目内文件引用必须另按用户访问环境输出，不沿用执行命令里的 `/home/...`。
- 来源: 用户本轮确认、`windows-wsl-execution-rules/SKILL.md`、`windows-encoding-rules/SKILL.md`、`AGENTS.md`
- 适用范围: `AGENTS.md`、环境规则 skill、命令模板、推荐工作流文档
- 更新时间: 2026-07-02
- 状态: 启用

### 项目内文件引用路径写法
- 别名: WSL 文件引用展示, 用户可打开路径, UNC 路径输出
- 类型: 输出风格
- 示例: `推荐: \\wsl.localhost\Ubuntu-24.04\home\luode\code\ellipal_admin\doc\6-审查\a.md；禁止: /home/luode/code/ellipal_admin/doc/6-审查/a.md`
- 说明: 凡回复中引用项目内文件，都按用户当前客户端可打开的路径输出。项目在 Windows 本地盘就输出 Windows 本地路径；项目在 WSL 且用户从 Windows / Codex Desktop / Claude Desktop 访问时，Markdown 链接、普通文本路径、审查证据路径、截图说明和最终总结中的项目内文件路径都使用 `\\wsl.localhost\<distro>\home\<user>\<project>\...`。`/home/<user>/<project>` 只用于命令参数、WSL shell 上下文和日志原文。
- 来源: 用户本轮确认、`windows-wsl-execution-rules/references/path-mapping.md`
- 适用范围: 最终回复、中间进度、审查报告、证据路径、截图说明、Markdown 链接和普通文本文件路径
- 更新时间: 2026-07-02
- 状态: 启用

### 文件写入显式 UTF-8
- 别名: UTF-8 写文件, 禁止默认编码, 跨平台编码写法
- 类型: 工具风格
- 示例: `PowerShell: Set-Content -Encoding UTF8 <path> <content>`、`Python: open(path, "w", encoding="utf-8")`、`Node: fs.writeFileSync(path, content, "utf8")`
- 说明: 写代码、文档、配置、脚本、测试资产和生成文本时，优先选择能显式声明 UTF-8 的命令或 API；禁止依赖 GBK、ANSI、系统默认编码、编辑器默认编码或 shell 默认编码。写入后回读关键文件并检查 `git diff`，确认中文、编码和换行都符合预期。
- 来源: 用户本轮确认、`AGENTS.md`、`windows-encoding-rules/SKILL.md`
- 适用范围: 文件写入命令、脚本生成文档、规则文件维护、Windows / WSL / Linux 协作开发
- 更新时间: 2026-07-02
- 状态: 启用

### 实施计划按垂直切片书写
- 别名: 依赖图优先, 垂直切片计划, 单任务约5文件
- 类型: 文档风格
  - 示例: `最小任务A: 支付路由闭环`、`依赖: 配置 -> 接口 -> 页面`、`预计文件数: 4`、`闭环: 实现 -> 真实测试 -> 审查 -> 验收`
- 说明: 实施计划正文先写 agent 对当前问题的理解，再按依赖关系与端到端垂直切片组织最小任务，不按前端 / 后端 / 数据库水平分层堆任务。问题理解至少交代问题 / 目标、本轮范围、非范围、当前优先闭环和关键假设 / 待确认点。每个最小任务默认单次专注完成，预计触达文件数尽量控制在约 5 个以内，并显式拆开写自己的任务完成条件、任务停止 / 结束条件、真实测试、审查、验收闭环后再进入下一任务；涉及代码生成、修改或重构时，还要补上真实测试入口、环境、样本 / 数据来源和通过标准；“现状与落点”还必须补出代码落点目录树，不能只写文件名清单。若运行环境要求用 `<proposed_plan>` 等专用计划包裹输出，外层只作为渲染层，正文仍必须保持这套项目内计划结构，不得退化成 3-5 条通用摘要 bullet，且输出前必须按 `implementation-planning-rules/references/plan-output-gate.md` 做字段矩阵检查。Plan Mode 正文禁止以 `Summary`、`Key Changes`、`Public Interfaces`、`Test Plan`、`Assumptions` 作为主结构；出现这类通用工程计划壳，或缺 agent 理解、范围、非范围、当前优先闭环、实施周期、阶段计划、最小任务、真实测试、完成条件、停止 / 结束条件、最大推进边界等核心字段时，必须按实施规划模板重写。若用户本轮显式索要计划，但前置条件未齐，风格上也必须给出“受限计划 / 阻断计划”结构，而不是一句“先补需求”结束；并且要明确写出“受限计划不得作为实施授权”，未升级为正式执行计划前不得进入编码、改码、重构、测试实施或其他执行动作。
- 来源: `implementation-planning-rules`、对话确认
- 适用范围: `doc/3-实施/` 文档、实施总览与实施周期计划
- 更新时间: 2026-07-04
- 状态: 启用

### 需求问题只写真实缺口
- 别名: 单关键问题不猜需求, 缺口式提问
- 类型: 文档风格
- 示例: `待确认: 成功标准缺失`、`待确认: 异常分支口径未提供`、`禁止写法: 你应该是想要A还是B`
- 说明: 需求阶段的一次一个关键问题，只能围绕已识别的真实缺口提问；不允许把 agent 的业务猜测包装成待确认答案，更不允许以“先做一版看看”替代需求主文档落地。
- 来源: `requirement-discovery-rules`、`requirement-intake-rules`、对话确认
- 适用范围: `doc/2-需求/` 文档、需求澄清与 gap 说明
- 更新时间: 2026-06-30
- 状态: 启用

### 需求文档正文摘要加附录详解
- 别名: 指标术语逻辑附录, 正文摘要附录详解, requirement appendix style
- 类型: 文档风格
- 示例: `正文: 只写最小必要定义与结论`、`附录5.1: 指标名/口径/公式/数据来源/适用范围`、`附录5.2: 术语/别名/定义/易混点`、`附录5.3: 逻辑主题/触发条件/判定规则/异常例外`
- 说明: 需求主文档默认采用“正文摘要 + 附录详解”。正文只保留当前评审、实现和验收需要立刻读懂的最小指标说明、术语定义和主链路逻辑；核心指标的统计口径、公式、数据来源、适用范围，关键术语的别名与易混点，以及核心逻辑的判定条件、优先级、例外和边界统一沉到附录。若正文已经引用这些概念，但附录没有补齐详解，视为需求文档未收口。
- 来源: `requirement-intake-rules`、`requirement-gap-rules`、对话确认
- 适用范围: `doc/2-需求/` 主需求文档、需求接入自审、需求 gap 判定
- 更新时间: 2026-07-03
- 状态: 启用

### 上线测试脚本工具箱写法
- 别名: release test scripts, 基线资产脚本, 可复用参数脚本, 双索引同步脚本
- 类型: 工具风格
- 示例: `python project-release-test-rules/scripts/generate_release_test_plan.py sync-interface-contract-assets --project-root . --manifest swag/.swag-manifest.yaml --inventory doc/5-tests/基线/interface-inventory.yaml --output doc/5-tests/<时间戳>_上线前项目接口测试/ascii-artifacts/interface-sync-report.yaml`
- 说明: 上线测试通用脚本优先沉淀为 `project-release-test-rules/scripts/generate_release_test_plan.py` 的子命令；项目差异写入项目 `doc/5-tests/基线/script-adapter.yaml` 或当轮测试目录，不写死进通用脚本。连续复用且变复杂的能力再拆成独立脚本，但必须保持总入口可发现、可复用、`--help` 可验证。`swag/.swag-manifest.yaml` 与 `interface-inventory.yaml` 的双索引同步也走同一总入口子命令，并固定输出 `interface-sync-report.yaml`。
- 来源: `project-release-test-rules/references/reusable-script-toolbox.md`、`project-release-test-rules/scripts/generate_release_test_plan.py`
- 适用范围: 上线接口测试脚本、基线初始化、依赖图、参数解析、基线回写
- 更新时间: 2026-07-02
- 状态: 启用

### Swag OpenAPI 资产写法
- 别名: swag 目录, OpenAPI YAML, Apifox 导入文件, swag manifest
- 类型: 文档资产风格
- 示例: `api_buySell_sell_getHistory_卖出历史.yaml`、`supported_onramps_all_法币渠道列表.yaml`、`Authorization -> 签名鉴权值`
- 说明: OpenAPI / Swagger 正式产物固定写入项目根目录 `swag/`；单接口文件按 path 去掉开头 `/`、`/` 替换 `_`、保留原 path 大小写命名，同一路径多 method 时先追加小写 method，再拼中文简要说明后缀。中文后缀优先取显式 `summary`，缺失时允许基于 path 动词、controller 名、DTO 名和 route 上下文做受控推导；仍无法稳定得到时回退纯路径文件名，并在 manifest 记录 `summary_source: unresolved`。单接口 YAML 默认不通过 `tags` 制造 Apifox 父目录，总 YAML 可保留 `tags` 做全量分组。头部、请求参数、响应字段都必须补齐中文说明；源码注释不足时允许基于字段名、DTO 名、route 上下文做受控推导，但不得编造业务规则。校验脚本放在对应 skill 的 `scripts/validate_openapi_yaml.py`，生成逻辑第一版可由 agent 读代码生成，但收口必须脚本校验。
- 来源: `swag-openapi-maintainer-rules/SKILL.md`、`swag-openapi-maintainer-rules/references/naming-rules.md`
- 适用范围: Swagger/OpenAPI 导出、Apifox YAML、swag 资产维护
- 更新时间: 2026-07-03
- 状态: 启用

## 废弃写法

### 并行旧目录口径
- 别名: 旧文档目录兼容壳
- 类型: 废弃风格
- 示例: `doc/old-requirements/` + `doc/2-需求/` 并存、旧跳转壳 `old-requirements -> 2-需求`
- 说明: 这类并行旧口径会让 skill、入口文档和长期记忆再次失真，迁移完成后不应继续保留。
- 来源: 对话确认、`artifact-storage-rules`
- 适用范围: 文档目录迁移
- 更新时间: 2026-06-28
- 状态: 废弃

## 变更记录

- 2026-06-27：初始化根目录风格记忆文档，补齐中文优先、doc 顶层混合命名和长期规则增量回写约束。
- 2026-06-27：补充风格记忆示例要求，明确优先记录代码片段、配置片段、命令片段或真实使用片段，不再接受过于抽象的口号式示例。
- 2026-06-27：长期规则文档新增“收口前真实落盘”口径时，直接回写原条目，不保留“轻量场景可不落盘”的平行旧规则。
- 2026-06-28：文档目录风格切换为编号前缀口径，活动目录按 `doc/1-架构/` 到 `doc/7-验收/` 排序。
- 2026-06-28：架构域固定使用 `1-4` 四个有序中文主入口，业务链路从 `5` 开始按最大编号加一维护。
- 2026-06-29：补充子 agent 状态公告风格，要求同时写逻辑中文名、平台昵称与回收状态，避免把平台英文昵称误判成命名失败。
- 2026-06-30：补充子 agent 完全授权写法，明确项目级 standing authorization 满足工具显式授权条件。
- 2026-06-30：补充命中检查可见输出样式，明确使用普通 Markdown 标题和行内代码字段行，禁止代码块包裹。
- 2026-06-30：补充普通说明不用代码围栏风格，明确自然语言结构化输出改用 Markdown 列表、表格或引用块，` ```text ` 不再作为普通回复模板。
- 2026-07-01：历史上曾收紧为 PowerShell UTF-8 后承接普通命令；2026-07-02 已按新确认口径替换为 Windows 下普通仓库命令优先 Git Bash / bash，PowerShell 仅用于专项场景，执行类命令再进 WSL。
- 2026-07-02：新增文件写入显式 UTF-8 风格，明确 PowerShell、Python、Node 等写文件命令必须显式 UTF-8，禁止 GBK / ANSI / 默认编码落盘。
- 2026-07-02：补充项目内文件引用路径写法，明确 Windows 桌面访问 WSL 项目时，所有面向用户的项目内文件引用使用 `\\wsl.localhost\...`，不把 `/home/...` 当作用户可打开路径。
- 2026-07-02：新增会话标题中文简要写法，明确自动重命名标题使用“任务对象 + 动作 / 症状 / 阶段”，避免只写泛化动作，且必须通过真实线程重命名工具执行。
- 2026-07-03：补充会话标题平台能力写法，明确 Codex / Claude Code / Claude Desktop 需要分开描述；Claude Desktop 默认输出跳过证据，不把无真实工具的平台写成“自动成功”。
- 2026-06-30：新增实施计划书写风格，明确依赖图 + 垂直切片优先、单任务约 5 文件、每任务闭环后再进入下一任务。
- 2026-07-01：新增受限计划文风要求，明确受限计划正文必须显式声明“不得作为实施授权”，避免被误读为可直接开工的正式执行计划。
- 2026-06-30：新增需求提问风格，明确一次一个关键问题只允许围绕真实缺口，不允许夹带 agent 猜测。
- 2026-07-03：新增需求文档“正文摘要 + 附录详解”写法，明确核心指标、术语与核心逻辑的详细解释统一沉到附录，正文只保留最小必要摘要。
- 2026-07-02：新增上线测试脚本工具箱写法，明确通用能力优先沉淀为总入口子命令，项目差异通过基线适配文件承接。
- 2026-07-02：新增 Swag OpenAPI 资产写法，明确 `swag/` 唯一输出目录、path 下划线命名和校验脚本收口方式。
- 2026-07-02：补充上线测试与 Swag OpenAPI 双索引同步写法，明确同步入口为 `sync-interface-contract-assets`，固定输出 `interface-sync-report.yaml`。
- 2026-07-03：补充 Swag Apifox 导入口径，明确单接口默认无 `tags` 直导入目标目录，且头部、请求参数、响应字段中文说明必须完整。
- 2026-07-03：补充单接口 Swag 文件名写法，明确默认采用“路径名 + 中文简要说明”格式，并在 manifest 留存 `summary_source` 以支撑回退和增量刷新。
- 2026-07-03：补充单接口 Swag 中文后缀清洗写法，明确接口中文简介进入文件名前要先剥离数字前缀、序号包裹符号和无业务意义特殊符号，不把 `11. 卖出确认` 这类原文直接落盘。
- 2026-07-03：补充 Plan Mode 计划文风写法，明确运行环境即使要求 `<proposed_plan>` 包裹，正文仍必须遵守项目内实施规划结构，不退化成通用摘要 bullet。
- 2026-07-04：补充 Plan Mode 通用计划壳禁用写法，明确 `Summary / Key Changes / Public Interfaces / Test Plan / Assumptions` 作为主结构时必须重写为实施规划模板，并在输出前执行 `plan-output-gate.md` 字段矩阵。
- 2026-07-03：补充审查链注释判定写法，明确代码改动进入实现自审或当前 diff 总审查时，方法头 `[参数]` / `[返回]` / `最近修改时间` / 改动原因、字段/结构体字面量中文说明、步骤编号 `1/2/3` 就近注释、补丁“做了什么 + 为什么要加”注释任一缺失都按未通过处理，不写成温和建议。
- 2026-07-03：补充会话标题执行写法，明确 Codex 下若首屏未直接暴露 `set_thread_title` / `list_threads`，先经 `tool_search` 发现线程工具，再做改名或跳过判断；未做工具发现不能直接写“工具不可用”。
