## 目录用法索引规则

- 稳定决策：package-structure-rules 是目录用法索引的唯一 Owner，通过 Catalog 条目的 related_skills、usage_recipes、package_alias、example_scope 字段关联专业 skill 和 recipe 示例。
- 稳定决策：guide 子命令按 --category、--technology、--language 查询目录用法，支持 category 别名映射（如 json -> serialization、log -> logging、convert/conversion、message/mq、scheduler/cron）。
- 稳定决策：Go recipe 示例统一存放在 package-structure-rules/references/usage-recipes-go.md，首批覆盖 convert、time、cache/redis、json、log、http；Java/Node/Python 后续按需扩展。
- 稳定决策：新增 recipe 时按流程更新 usage-recipes-go.md、Catalog 条目的 usage_recipes 字段、directory-usage-routing.md 索引表，并运行 guide 子命令验证。
- 来源：package-structure-rules/SKILL.md、package-structure-rules/references/placement-catalog.yaml、package-structure-rules/scripts/placement_catalog.py、package-structure-rules/references/directory-usage-routing.md、package-structure-rules/references/usage-recipes-go.md。
- 更新时间：2026-08-08。

# 项目长期记忆

## 编码后验证发散与最小改动的分工边界（2026-09-29 固化）

- 稳定决策：**编码收敛、验证发散，两个阶段两种取向**——`code-quality-rules` 在编码期执行最小改动（收缩改动范围、阻断顺手重构、拒绝发散无关项）；`verify-brainstorm-rules` 在编码完成后执行发散式验证（放开联想、多维度挑刺、主动找更多问题）。二者不是矛盾，而是同一条流水线的前后两个阶段。
- 稳定决策：**发散只发生在“发现问题”这一步（强制铁律）**——`verify-brainstorm-rules` 对代码库只读，**绝不顺手改码**（含“只改一行”的一眼可见问题）；修复动作一律回流 `code-quality-rules` 的最小改动收敛，确认为真缺陷的转 `bug-intake-rules`。
- 稳定决策：**裁决权始终在用户手上**——该 skill 只负责“捞问题”，不决定修哪些；报告必须把“建议优先级”与“用户裁决结论”分开呈现，不得把建议写成既定计划。
- 稳定决策：**发散有界 + 维度穷举**——发散起点为本轮改动点，允许沿调用关系与数据流外扩一层（用户已确认口径），单轮问题上限 15 条并按严重度截断；必须逐维度走完 13 维矩阵（安全、性能、逻辑正确性、边界与空值、并发与竞态、异常与错误处理、数据精度与类型、资源与生命周期、兼容性、可观测性、配置与依赖、业务与用户视角、代码格式与风格），“无问题”也必须写出依据。
- 稳定决策：**代码格式与风格纳入发散，但判据不搬家（2026-09-29 补）**——`verify-brainstorm-rules` 的第 13 维覆盖代码格式与风格偏离（命名、缩进、换行、导入顺序、注释颗粒度、文件落点、无关格式化混入 diff），但风格**判据权威与 `6-review` 的 `STYLE: PASS / FIX_REQUIRED` 判定仍归 `code-style-consistency-rules`**；本 skill 只做偏离发现、默认 P2（仅当直接导致构建 / CI / 工具链失败时才升 P1），不重新定义风格规则、不发起全仓统一格式化。
- 稳定决策：**先收敛后发散**——顺序固定为“功能验证 / Bug 验证 / 回归验证（收敛判据）→ 验证发散（广度挖掘）”；收敛结论缺失时不得用发散结果替代或据此宣称功能可用。
- 稳定决策：**触发口径**——用户提出“验证功能”“验证这个功能”“验证刚刚改动的代码”“验证一下”“再检查一遍”“检查一下”等表达即触发。
- 来源：用户指令（2026-09-29）+ `verify-brainstorm-rules`（`SKILL.md` 与 4 个 references）+ `skill-absorption-rules` 的 `workbuddy-absorption-map.md`（2026-09-29 enhance-verify-mode 裁决）。
- 更新时间：2026-09-29。

## Goal 模式免确认推进与临时产物清理（2026-09-24 固化）

- 稳定决策：**Goal 模式 = 计划已完成，只要结果**——用户当前轮显式用 `/goal` 开启目标模式，或用户已显式确认的 Goal 处于 `active` 时，agent 直接进入实现，不再重复征求计划确认、方案确认或需求澄清。
- 稳定决策：**执行分歧按 agent 推荐方案推进，不要求用户确认**——出现多方案、路径冲突、口径不一致、约束互相牵制时，agent 自行完成对比分析并直接按最推荐方向执行，不抛选择题、不暂停、不等待确认；推荐方向判定顺序为「满足目标与验收条件 > 最小可逆 > 有真实证据 > 守住红线」；无法判定优劣时选最小可逆、最保守、可回滚方案继续，并把分歧与选择写入落盘任务计划文档。
- 稳定决策：**不因免确认放开红线**——系统、平台或工具明确要求的权限审批、高风险或不可逆操作、超出已确认范围且需要扩权的动作、`local` 本地连接调试测试红线、凭据不回显、Git 写历史红线（提交 / 推送仍需当前轮显式授权）、跨项目写入红线与 `WRT-*` 授权边界、个人文件安全与删除保护及实质外部副作用均不放开；成本预警、速率限制、死循环检测、迭代上限等安全熔断继续保留。
- 稳定决策（2026-10-12 补充）：用户显式开启或确认的 Goal 中，目标/计划范围内必需、范围狭窄且限于当前项目工作区（不含兄弟项目与个人文件）、可逆易恢复、无实质外部副作用/额外费用/破坏性数据变更/敏感信息暴露/安全边界变化、且无更高优先级强制审批要求的单项低风险授权可默认通过任务层许可。默认只覆盖该项最小动作，不扩大目标或未来授权；无法确认全部条件时按需审批；低风险默认许可不产生等待用户授权的 `BLK-*`。
- 稳定决策（2026-10-13 补充）：已显式开启或确认且仍 active 的 Goal 执行中，计划文档缺项、过期、冲突或未落盘时，由 agent 依据 Goal、现有计划、项目规则和仓库证据先修复同一文档、记录依据与假设并落盘，然后持续执行；文档问题本身不暂停 Goal 或创建 `BLK-*`。真实权限、安全红线只暂停受影响动作，安全独立步骤继续。
- 已沉淀为 skill: `goal-loop-rules`。
- 稳定决策：**防自我授权边界**——agent 为补建任务投影、异常修复或超时探测而自动 `create_goal` 产生的 Goal **不构成**用户开启的 Goal 模式，仍不自动取得任何实现授权；免确认推进必须建立在用户显式开启或确认的 Goal 之上（原任务投影机制已于 2026-10-31 退役，该边界继续有效）。
- 稳定决策：**临时文件与脚本执行后必须清理**——执行过程中为推进任务临时生成的脚本、临时文件、临时目录、临时服务与后台任务，使用后立即清理，禁止污染项目目录或长期滞留在宿主任务列表；未清理视为任务未完成，收口前按 `runtime-process-cleanup-rules` 的三层清理对象真实回读验证。
- 来源：用户指令（2026-09-24 与 2026-10-12）+ `goal-loop-rules`（`SKILL.md`、`references/safety-mechanisms.md`）+ `autonomous-execution-rules`（`SKILL.md`、`references/continuation-and-pause.md`、`references/execution-authorization-and-plan-boundary.md`）+ `runtime-process-cleanup-rules` + `AGENTS.md` / `CLAUDE.md`。
- 2026-09-27 更新：Goal 模式 Owner 已从 `long-run-loop-rules` 合并至 `goal-loop-rules`（与 `goal__skillhub` 目标方法论合并），旧目录已删除；本条来源路径按新 Owner 理解，原始落盘历史见 `PROJECT_HISTORY.md`。
- 更新时间：2026-10-12。

## 配置文件项禁止多行过程注释与复杂逻辑专门文档规范（2026-09-18 固化）

- 稳定决策：**配置文件项极简目的注释（强制铁律）**——YAML、TOML、JSON 等各类配置文件是环境运行参数与控制开关的直接载体，其受众为开发、运维与交付人员，关注核心是“该配置控制什么行为、取值含义是什么”。配置项上方注释**严格默认单行就近，只写目的与控制边界说明**。
- 稳定决策：**严禁将配置文件当做事故复盘或推演草稿纸**——绝对禁止在配置项上方堆砌内部运行机制细节、状态机分步推演（如“先写待确认、10分钟后复核再升级”）、历史事故渊源（如“某日事故的修复要件”）以及新旧行为对比/关停状态对比等多行过程注释。
- 稳定决策：**复杂逻辑归位功能专门文档记录（强制）**——如果有复杂的业务逻辑、状态流转、多阶段异步任务、速率防护或开关联动机制，**必须在 `doc/` 下建立功能专门的文档记录**（如 `doc/1-架构/<递增序号>-业务链路-<业务名称>.md` 或 `doc/2-需求/` 规格文档），严禁试图在代码或配置文件中用长篇多行注释硬解释机制。代码与配置只留单行目的说明，复杂机制与推演过程全量归位到功能专门文档中。
- 稳定决策：**过程信息分层归位**——事故背景、推演过程与历史版本行为差异一律写入专门功能文档、需求/Bug 文档或 Git 提交说明，配置文件内一行不留，绝不设折中形态。
- 来源：用户指令（2026-09-18，配置文件注释与复杂逻辑专门文档记录要求）+ `comment-rules`（统一硬约束、`comment-placement.md`、`comment-granularity.md`、`comment-examples.md`）+ `architecture-doc-rules` + `code-style-consistency-rules` 反例库 `STYLE-CASE-CFG-001` + `PROJECT_STYLE.md`。
- 更新时间：2026-09-18。

## TAPD 全流程自动化行为与测试人员流转规则（2026-09-16 固化）

- 稳定决策：**Story / Bug / Task 分类自动化处理工作流（2026-09-16 固化）**：
  1. **Story（需求）**：仅处理无子 Story 的叶子需求，包含子 Story 的父需求保持原样不予处理；当叶子 Story 为规划或实现中且名下无未完成子 Task 时（当前开发者名下已完成、他人未完成的不算），自动分析并拆分为可执行子 Task（标题明确、具体实现方案、指派当前开发者、填写合理预估工时）。
  2. **Bug（缺陷）**：由测试人员提交，严禁修改原始描述，也无需创建新任务；直接分析成因并在评论中清晰记录排查结果、解决方案及处理进度。
  3. **Task（任务）**：独立 Task 直接承接，按规划进入开发实现。
- 稳定决策：**TAPD 全流程自动化行为约束（强制）**：
  1. **分析完成自动评论（五要素）**：会话确认完成任务/需求/bug 分析时，必须自动在 TAPD 添加分析评论，严格包含：分析结论、是否可以开始执行、是否缺失材料、是否缺少前置条件、是否需要人工补充缺失信息。
  2. **开始执行追加评论**：分析结论为可直接执行、已添加“可以开始做”评论且会话实际开始执行后，必须及时追加评论：“`agent开始代码实现`”。
  3. **代码完成即提交本地 Git（强制铁律）**：Agent 自行完成的代码实现，**严禁暂存在项目的未提交更改中，完成自测验证后必须立即自动提交到本地 Git 仓库（执行 git commit）**；**提交前缀必须指明 Agent 任务身份（强制格式：`<type>: [agent-<模块/功能>] <改动说明> [TAPD#<ID>]`，例如 `fix: [agent-兑换] 修复SWAPKIT报价解析异常 [TAPD#1162459836001003690]`）**，杜绝改动散落并清晰留痕；**红线边界**：绝对禁止自动 push 到远端仓库，向远端同步必须由用户发起或显式授权。
  4. **代码实现完成总结评论**：代码实现完成并提交本地后，自动添加一条评论说明实现已完成，并按分节骨架总结本次实现内容、验证结果与本地 commit hash。
  5. **收口流转与测试人员指派**：实现完成评论发布后，必须将条目状态流转至「待版本验证」，并将处理人变更为测试人员；每跳流转与处理人变更必须回读核验生效。
- 稳定决策：**TAPD 创建实体真实创建人身份规范（防 tapd_my_token 占位符，2026-09-17 固化）**：
  1. **显式传参**：通过 OpenAPI 创建缺陷（Bug）、需求（Story）或任务（Task）时，**必须显式传入创建人字段**（Bug 为 `reporter`，Story/Task 为 `creator`），绝对禁止漏传或留空。
  2. **唯一真源**：创建人必须是当前 Token 绑定的真实员工身份（优先调用 `GET /users/info` 动态获取 `name`/`nick`，如“罗德”；或读取本机用户真源），**绝对禁止随便取名**（严禁随意填写 `admin`、`agent`、`workbuddy`、`bot` 或虚构姓名）。
  3. **审计只读机制**：若漏传创建人，TAPD 服务端将强制默认回退为凭据名 `tapd_my_token`；且创建后该字段在服务端具备严格只读保护，`update_*` 接口会被静默忽略无法事后修改；一旦误创只能关闭作废并在新单重开。
- 稳定决策：**TAPD 三大核心操作意图与路由分流规则（2026-09-17 固化）**：
  1. **单任务分析（"看一下这个任务 / 看看任务"）**：仅做深度技术与代码可行性调研，不直接开工写代码；必须在 TAPD 上发表标准五要素分析结论评论，保持在分析就绪等待状态。
  2. **任务描述完善（"完善这个任务 / 完善任务"）**：明确说明该任务/需求描述不清楚、背景或信息缺失，需结合代码库现状、关联模型和接口，补充完善需求内容与规格说明（更新 description 或发布完善规格评论）。
  3. **批量扫描清任务流水线（"扫描tapd [xx], 清任务 / 开始做tapd[xx]任务 / 开始做tapd任务"）**：扫描指定项目或当前迭代的需求、任务、Bug，严格按统一优先级排序（缺陷 > 任务，严重度/优先级高 > 低），逐个串行推进状态机：先分析评论是否可做；若可做立即开工走全套流程（追加开工评论 → 编码自测 → 代码完成即本地commit → 总结评论 → 流转待版本验证并指派测试人员杨莹/李红/韩忠宝），闭环一个再做下一个；若不可做则记录缺口并推进下一条。
- 稳定决策：**测试人员名单持久化配置与记忆**：
  - 测试人员名单落盘配置文件：`<skills>/tapd-task-executor/config/qa-team.json`；
  - 持久化测试人员名单：**杨莹、李红、韩忠宝**；
  - 指派策略：原指定测试优先，未指定时按杨莹、李红、韩忠宝轮询或业务模块负责划分指派；开发完成后禁止处理人留置为开发自身或留空。
- 稳定决策：**新建需求 / 任务默认挂当前迭代（2026-09-29 固化）**：新建的 Story 与子 Task 一律显式传 `iteration_id=<当前迭代id>`，不留 `0`——`iteration_id=0` 的单不进迭代看板，多 workspace 场景下用户默认只看主项目，只给 id 会导致用户根本找不到。子 Task 跟随所属需求的迭代；需求本身没有迭代时，按当天日期取当前迭代。只有用户明确指定其他迭代或要求不挂迭代时才例外。禁止把"当前迭代"写成固定 id 常量（迭代按月滚动、同项目并存多个 open 迭代，只能按日期实时选）。
- 稳定决策：**任务流转完成前必须先登记工时（2026-09-29 固化）**：Task 没有工时记录时 `status=done` 返回成功但回读仍是 `progressing`（静默不生效）。因此 task 的状态机顺序固定为「登记工时 → 改 done → 回读核对」，不得省略回读验证。
- 来源：用户指令（2026-09-16、2026-09-17、2026-09-29）+ `tapd-task-executor`（`SKILL.md`、`config/qa-team.json`、`references/qa-assignment-rules.md`、`references/task-analysis-criteria.md`、`references/story-bug-task-workflow.md`、`references/cli-field-pitfalls.md` §九 / §十、`references/source-notes.md` 第十批）+ `tapd-openapi` + `tapd-addcomment` + 知识库《TAPD创建实体创建人身份规范》。
- 更新时间：2026-09-29。

## TAPD 工具路由优先级（2026-10-19 固化）

- 稳定决策：TAPD 查询与操作默认先使用 `tapd-cli`，单条查询与批量操作均适用；CLI 不支持或不能满足请求时，回退到 `tapd-openapi` 的直接 API 能力；只有 CLI 与 API 都无法提供页面专属能力时才使用浏览器。网页读取失败、浏览器已登录或标签页已打开，均不能单独作为跳过 CLI/API 的理由；凭据缺失或鉴权失败按 TAPD 环境规则阻断，不得静默绕过。
- 来源：用户指令（2026-10-19）+ `tapd-cli/SKILL.md`、`tapd-openapi/SKILL.md`、`authenticated-url-routing-rules/SKILL.md`。
- 更新时间：2026-10-19。

## 待裁定事项建议、选项与默认最安全兜底闭环规则（2026-09-16 固化）

- 稳定决策：**严禁只抛问题不给建议（强制铁律）**——无论是工程执行任务收口、周期/阶段边界、任务中断点，还是独立结论区，凡总结中列出“需用户裁定的事 / 待决策项 / 阻断决策”，绝对禁止只提问题、只陈述矛盾或当传声筒；Agent 作为具备专业判断力的工作搭档，必须体现主见（带着答案回来，而不是带着问题回来）。
- 稳定决策：**待裁定事项四要素闭环**——每一项需用户裁定的事必须严格包含：① 裁定点与影响（精准说明争议焦点、为什么必须此刻定夺及阻塞什么）；② 推荐建议与理由（加粗亮出明确倾向与 1 句硬核技术/业务理由，绝不模棱两可）；③ 选项选择（清晰罗列选项 A/B，标明推荐项，让用户可直接回复“选 A”拍板推进）；④ **默认最安全兜底方案**（明确声明“若未做裁定/直接回复继续，默认按最保守安全方案推进”，并阐明其安全性依据，如防限流、防击穿、防破坏性误删、最小改动等）。
- 稳定决策：**硬闸自检与驳回闭环**——`reasoning-summary-structure-rules` 发送前自检必须逐项核对待裁定事项是否具备加粗推荐建议、选项选择与默认安全兜底方案；缺少任一要素的总结直接判定 FAIL 阻断，禁止发出。
- 来源：用户指令（2026-09-16）+ `reasoning-summary-structure-rules`（`SKILL.md`、`summary-structure-template.md`、`conditional-sections-rules.md`、`output-examples.md`）。
- 更新时间：2026-09-16。

## 代码分解与目录内聚规则（2026-09-14 固化）

- 稳定决策：核心原则为「非必要不突破」。常规业务逻辑代码严格遵守基准线，特殊工程场景有正当理由且留痕时允许受控例外。
- 稳定决策：单个代码文件原则上不超过 200 行，超过时拆分为多个同级 diamond 文件；【特殊场景例外】：纯声明式数据映射表、枚举字典、协议常量表允许突破行数限制。
- 稳定决策：一个同级目录只能包含一种业务逻辑，若拆解后仍归为两种及以上业务，即使很小也必须拆分到不同目录。
- 稳定决策：一个目录只做一件事，若同一业务包含多个处理阶段，拆分为多个同级文件存放。
- 稳定决策：单个代码块或函数原则上不超过 80 行，超出时拆分为多个函数；【特殊场景例外】：① 状态机流转、事件派发主干或巨型 switch 映射（分支执行体抽为子函数）；② 长业务流水线入口编排函数（具体实现细节已全部下沉到各小封装子函数，各子函数严格 ≤ 80 行，仅顶层入口函数因纯步骤编排调度自然突破 80 行，属于正当特例；混杂具体实现细节的长函数一律属于坏味道，必须先拆解下沉，严禁掩盖）。
- 稳定决策：函数参数和返回值原则上均不得超过 2 个，否则优先改用结构体传参或返回；【特殊场景例外】：三方库固定回调契约或底层原子构造函数若封装反造无意义空壳时允许保留原生签名。
- 稳定决策：任何特殊场景例外必须在代码位点添加简短注释留痕（如 `// exemption: [理由]`），并在 `6-review` 阶段复核其必要性与正当性。
- 来源：用户决策（2026-09-14）+ `package-structure-rules` + `code-quality-rules` + `AGENTS.md` / `CLAUDE.md`。
- 更新时间：2026-09-14。

## 凭据持久化与输出脱敏

- 稳定决策：真实凭据原值可有意持久化于代码、配置、普通维护文档和对应 Git 提交；日志、错误、测试报告与证据、终端输出、Agent 回复、会话交接和自动知识摘要不得回显原值。
- 稳定决策：配置 Catalog 的 yaml 条目使用 `allow_plain_secret`（config/yaml/ 唯一配置模式）；`source_policy`、Schema、CLI 参数和返回结构不因该决策改变。

## 跨项目写入授权规则

- 稳定决策：跨项目写入从「绝对禁止、无授权例外」改为「默认只读 + 会话级写入授权」，例外通道为「会话级跨项目写入授权」契约。
- 稳定决策：授权要素 = 目标项目绝对路径 + 授权范围（文件 / 符号 / 模块或整项目）+ 操作类型（文件写入 / 构建测试 / 依赖安装 / Git 写操作）+ 版本冻结（分支 + commit）+ 改动意图 + 验证方式 + 回滚方案；缺任一项不得授权、不得写入。
- 稳定决策：授权记录 `WRT-*` 为会话级，本会话内对目标项目 + 授权范围 + 操作类型持续有效；授权记录留痕在 `PROJECT_CURRENT.md` 或会话内明确声明。
- 稳定决策：授权失效条件 = 会话结束 / 用户撤销 / 目标或范围越界 / 版本冻结漂移；失效后回到默认只读，须重新申请。
- 稳定决策：授权不覆盖的独立红线（非本条子项，仍按各章执行）：`local` 本地连接调试测试红线、凭据不回显、个人文件安全与删除保护、当前项目自身 Git 写入的当轮意图要求。
- 来源：用户决策（2026-09-10，AskUserQuestion 三项确认）+ `AGENTS.md` / `CLAUDE.md`「跨项目写入红线」+ `implementation-planning-rules/references/sibling-project-discovery.md`。
- 更新时间：2026-09-10。

## 本项目 Git 提交即推送规则（2026-10-01 固化）

- 稳定决策：**本仓库（luode-skills）默认「提交即推送」**——用户在本项目提出提交意图（`提交git`、`提交代码`、`commit一下` 等）时，默认把「本地提交 + 推送 `origin` 对应分支」作为同一笔授权闭环执行，不再对推送单独二次确认。
- 稳定决策：**例外只放宽推送授权粒度**——提交前置门禁（pre/post gate、按业务目标拆分提交）继续逐笔执行，不因「提交即推送」降低验收标准。
- 稳定决策：**负向边界绝对优先**——用户当轮显式写出「只提交，不要推送」「不要推送」等限制时，严格停在本地提交并等待后续指令，不得按默认闭环继续推送。
- 稳定决策：**不扩散到其他项目**——其他仓库未显式声明「提交即推送」时仍按逐动作授权，不得把本例外套用到别的仓库。
- 来源：用户指令（2026-10-01「推送, 这个项目提交并推送做为项目规则写进规则md」）+ `AGENTS.md` / `CLAUDE.md`「严禁自动提交 Git」章节 + `context-recovery-rules/scripts/bootstrap_agents.sh` 的 `BODY_NO_AUTO_COMMIT` + `git-collaboration-rules/references/current-turn-authorization.md` 项目级例外节。
- 沉淀状态：已沉淀，通用规则由 `git-collaboration-rules` 承接（`references/current-turn-authorization.md` 项目级例外节 + `SKILL.md` 行 29）；本条目不再重复吸收，后续引用走该 skill。
- 更新时间：2026-10-29。


## 代码项目提交前编译闸门（2026-10-22 固化）

- 稳定决策：**代码项目提交 git 前必须最基本编译通过**——仓库根命中 `go.mod`、`Cargo.toml`、`tsconfig.json`、定义了 `build` 脚本的 `package.json`、`pyproject.toml`、`setup.py` 任一标记即为代码项目，提交前必须真实执行对应编译入口并取得退出码 0。
- 稳定决策：**工具链缺失与超时一律阻断**——命令不存在、node 无法执行、需要联网取包、超过 `COMPILE_GATE_TIMEOUT`（默认 600 秒）都阻断提交，不得静默判成「非代码项目」跳过；TypeScript 只认本地已安装的 `tsc`，禁止 `npx` 联网拉取 registry 上的同名无关包。
- 稳定决策：**编译通过不等于功能可用**——编译只算最低门槛，功能、接口、页面验证仍由测试类 skill 负责，不得用「能编译」宣称「已验证可用」。
- 来源：用户指令（2026-10-22「如果是代码的项目，提交git之前要保证最基本的编译通过才可以提交git」）+ `git-collaboration-rules/SKILL.md` 的「1.0 代码项目最基本编译闸门」+ `git-collaboration-rules/references/baseline-compile-gate.md` + `git-collaboration-rules/scripts/pre_commit_gate.sh` 第 6 步 + `AGENTS.md` / `CLAUDE.md`「代码项目提交前编译闸门」章节。
- 更新时间：2026-10-22。

## 提交前索引漂移识别（2026-10-22 固化）

- 稳定决策：**批量「已暂存删除」先当索引漂移处理，不当用户删除**——判断三条：`D` 条目路径仍在磁盘、内容与 `HEAD:<path>` 一致或仅差 CRLF/LF、`git write-tree` 等于某个历史提交的树。任一命中即证明索引被整体回退，直接提交会静默吞掉期间所有提交的改动。
- 稳定决策：**恢复只用混合重置**——`git reset` 只回写索引、不动工作树；禁止对这类条目用 `git checkout`、`git restore` 或 `rm`，否则会把磁盘上完好的文件真的删掉。
- 来源：2026-10-22 本轮实测（索引树等于 `3a9aa97e`，392 条假删除中 365 条与 HEAD 完全一致，混合重置后真实变更收敛为 106 项）+ `git-collaboration-rules/references/staged-review-and-evidence.md`「索引漂移前置核对」。
- 更新时间：2026-10-22。

## 前端视觉改动对比 Demo 闸门（2026-10-25 固化）

- 稳定决策：**改已有界面的视觉必须先后给新旧对比 demo，用户确认后才动生产代码**——范围含尺寸、间距、颜色、圆角、阴影、字体、布局结构、组件外观、动效参数；未确认前允许写 demo 文件，不允许先改业务文件再补 demo；用户要求调整时回 demo 迭代，不在生产代码上反复试错。
- 稳定决策：**demo 必须长在项目自己的样式上**——样式来源按五档优先级取第一条可行：`<link>` 真实构建产物 CSS → `@import` token 源文件 → 挂进项目跑真实组件 → `M3` 真实页面截图 → `getComputedStyle` 抽取兜底；复用真实 class 名与 DOM 结构，禁止凭记忆写 token 名、肉眼估算色值、默认字体冒充、另起一套 class。
- 稳定决策：**before 版是校准基准**——before 必须与真实页面同尺寸并排校准到无肉眼可见差异后再交付；before 偏了，after 的通过与否都是假象。
- 稳定决策：**免 demo 只有四类且必须写明依据**——用户已给出无歧义目标值、纯内部重构不改渲染结果、看不见的改动（接口接线 / 组件拆分 / 类型修正）、新增页面或组件无 before（走 `M4` 仅 after）。
- 来源：用户指令（2026-10-25「前端改样式、改组件、调 CSS 不能只用文字说明，要给 HTML demo 对比新旧」+ 追加要求「demo 必须继承原项目样式」）+ `frontend-design/references/visual-change-demo.md`（唯一权威细则）+ `frontend-design/SKILL.md` 第 2 步闸门条 + `frontend-ui-visual-rules/SKILL.md` 暂停条件引用 + 知识库笔记 `20-Knowledge/AI协作/前端样式改动先出对比demo.md`。
- 更新时间：2026-10-25。

## 反打补丁与架构优先原则（2026-10-05 固化）

- 稳定决策：**核心红线：严禁为少改代码打补丁破坏架构**——改动、改 Bug、改需求严禁用打补丁的方式实现；明显的为了不改动太多 / 控制 diff 行数 / 避开动旧逻辑而选择打补丁（如在外围堆砌特判 flag、搞新老双轨分流兼容、套壳胶水绕道、下游 try-catch 吞异常或坏数据兜底）是绝对不可取的，会严重破坏代码可读性与既有架构设计。
- 稳定决策：**正向准则：流程遗漏直接在主流程补齐**——排查发现是主流程确实遗漏了必要步骤（如缺少状态转移分支、缺少必要前置校验、未处理边界返回值），允许且应当直接在原主干流程中补齐，保持业务流水线单一自洽。
- 稳定决策：**架构与可读性优先**——系统架构与代码可读性永远高于局部 diff 最小化；遇到新旧规则冲突，宁可正向演进模型统一承接，绝不搞双轨历史包袱。
- 来源：用户指令（2026-10-05）+ `code-quality-rules/references/no-patchwork-architecture-discipline.md` 与 `SKILL.md` + `code-generation-style-rules` + `bug-fix-proposal-rules` + `implementation-planning-rules` + `code-style-consistency-rules/references/user-style-feedback-library.md`（STYLE-CASE-ALL-004）。
- 更新时间：2026-10-05。

## 窗口与应用截图取证双轨机制（2026-10-05 固化）

- 稳定决策：**自身可控渲染应用优先走应用内自渲染（app-internal-screenshot-rules）**——对 Godot、自研游戏、浏览器 CDP、Electron 等可控渲染应用，通过自身渲染通道（视口纹理 `get_image()`、CDP `Page.captureScreenshot`、Electron `capturePage()`）抓取，天然只含目标应用且不串味、不依赖前台、不出现黑屏或陈旧帧。
- 稳定决策：**系统级第三方窗口走定向截屏与受控交互（window-scoped-capture）**——对普通操作系统窗口，使用 `PrintWindow`（`PW_CLIENTONLY`）锁定客户区截屏，使用 `PostMessage` 投递后台按键与比例坐标点击，避免全屏截图串味、不抢前台焦点、不动系统真实鼠标。
- 来源：新增技能 `app-internal-screenshot-rules/SKILL.md` 与 `window-scoped-capture/SKILL.md`。

## 本地项目浏览器调试优先使用 Agent 内置浏览器（2026-10-13 固化）

- 稳定决策：需要在浏览器中调试本地项目页面时，优先使用当前 agent 宿主提供的内置浏览器通道；统一矩阵以 `Chrome DevTools MCP` 作为标准调试能力映射，只有宿主未提供该通道且任务不依赖 DevTools 专属能力时才条件回退到基础浏览器自动化。依赖用户真实 profile 中**已有**的标签页、登录态、Cookie 或扩展时仍使用 `Chrome Plugin`；HAR/性能/trace 和 Cloud 场景按各自专属路由承接。
- 稳定决策：**「页面需要登录」本身不构成回退 Chrome Plugin 的理由（2026-10-15 固化）**——回退判据是「必须复用用户真实 Chrome profile 里已经存在的认证态」，不是「页面需要登录」。本地调试系统（`localhost` / `127.0.0.1` 等 local 环境）的登录凭据由调试侧提供，属于可自行注入的授权，应由内置浏览器通道自行完成登录；只有真实账号会话、SSO、企业内部系统、第三方托管文档等难以自行获取的授权态才回退 Chrome Plugin。
- 来源：用户指令（2026-10-13、2026-10-15）+ `mcp-installation-rules/references/tool-priority.md`。
- 更新时间：2026-10-15。
- 更新时间：2026-10-05。

## 生图生成后符合度自检与不符合即重做（2026-10-05 固化）

- 稳定决策：**生图出图不等于任务完成**——每次生成或编辑后，必须对照用户原始提示词与本轮约束逐条给出 `符合 / 不符合 / 无法判定` 的验收结论，不能以"已生成"代替"已达标"。
- 稳定决策：**验收清单至少覆盖十个维度**——主体与数量、风格与媒介、构图与取景、颜色与配色、尺寸与比例、画面内文字、禁止项、透明底与色度键、参考图角色、输入图不可变项。
- 稳定决策：**不符合即重做**——任一验收项为"不符合"时不得交付，须按不符合项定向修改（已符合项保持不变并在新 prompt 中复述关键约束防漂移），重新生成新图；同一资产多轮优化按 `v1`、`v2`、`v3` 递增命名，禁止覆盖旧版本，多问题时一次只改一个重点。
- 稳定决策：**连续 3 轮不达标即停止自动重试**——改为向用户报告差距、已尝试的修改与候选方向，交回用户决策。
- 来源：用户指令（2026-10-05）+ `imagegen/SKILL.md` 核心规则与工作流第 5/6/7 步 + `imagegen/references/prompting.md`「生成后符合度自检」节。
- 更新时间：2026-10-05。

## 生图配置统一目录（2026-10-19 固化）

- 稳定决策：**生图配置唯一目录为 `~/.imagegen/`**，主配置固定 `~/.imagegen/config.json`，覆盖 `base_url`、`model`、`model_priority`、`api_key`、`api_keys` 全部字段；不再新增或回退 `~/.ai-hive/` 等其它配置目录。
- 稳定决策：**两条 CLI 通道共用同一份配置**，`imagegen.py init` 写入时合并保留既有 `api_keys`、`model`、`model_priority`，不得用整文件覆盖冲掉多 Key 池。
- 稳定决策：仅运行时覆盖可走环境变量（`IMAGEGEN_*`、`AI_HIVE_API_KEY`、`PROJECT_IMAGE_*`）；需要长期保存的配置一律写回统一目录。
- 来源：用户指令（2026-10-19）+ `imagegen/SKILL.md`「统一配置目录」+ `imagegen/scripts/imagegen.py`。
- 更新时间：2026-10-19。

## 记忆文件超长主动整理规则

- 稳定决策：`PROJECT_CURRENT.md` 的 UTF-8 字节数上限为 51,200；`PROJECT_HISTORY.md` 只保留最近 20 条事件。当任务执行中发现这两个文件超长（CURRENT 接近 51KB / HISTORY 超过 20 条），AI 应主动裁剪过期旧记录，无需等待用户指令。
- 稳定决策：裁剪原则——CURRENT 删除最旧的任务条目（按时间戳判断，保留最近完成的条目）；HISTORY 按「日期倒序、新事件置顶、追加后自动裁剪」规则只保留最近 20 条，被裁剪事件的计数锚点随事件一起删除。裁剪后记录到当日工作日志。
- 稳定决策：本规则是对 `project-memory-rules/SKILL.md` 写入规则中 CURRENT 51,200 字节闸门和 HISTORY 20 条上限的补充执行约定——之前一直存在"超限只提示阻断，未要求 AI 主动裁剪"的缺口，本规则要求 AI 自行判断并执行裁剪。
- 来源：2026-09-07 用户指令吸收 + `project-memory-rules/SKILL.md` 写入规则。
- 更新时间：2026-09-07。

## Decimal 目录规则

- 稳定决策：`utils/decimal/` 是 Decimal 高精度数值类型封装唯一目录，Catalog ID `backend.utils.decimal`，Go 包别名 `decimalUtil`。
- 稳定决策：Decimal 能力覆盖 sql.Scanner、driver.Valuer、ToFloat64、String、Add/Sub/Mul/Div、Cmp/Equals、IsZero/IsPositive/IsNegative、Abs/Round/Max/Min 与四个构造函数（NewDecimalFromFloat64、NewDecimalFromString、NewDecimalFromInt64、NewDecimalFromDecimal）。
- 稳定决策：关联 skill 为 `common-util-rules`、`database-query-rules`、`database-schema-rules`，recipe 索引为 `usage-recipes-go.md#decimal`。
- 来源：`package-structure-rules/references/placement-catalog.yaml`、`package-structure-rules/references/usage-recipes-go.md`、`package-structure-rules/references/backend-util-layout.md`、`package-structure-rules/references/directory-usage-routing.md`、`package-structure-rules/references/project-layout-v2.md`。
- 更新时间：2026-08-09。


## Apifox 测试分离库规则（config.apifox.yaml）

- 稳定决策：接口测试（功能验证/回归/Bug 验证/上线门禁的接口部分）的服务侧配置统一走 `config/yaml/config.apifox.yaml`（同仓后端 `backend/config/yaml/config.apifox.yaml`），被测服务以 `-env apifox` 启动；项目无此文件时从 `config.local.yaml` **复制**生成，业务配置保持一致。
- 稳定决策：**数据库分离（强制阻断）**——`config.apifox.yaml` 的 MySQL 数据库必须使用**独立的 apifox 测试专用库**，**库名约定为 `apifox`、由开发人员手动创建并配置**，**禁止与 `config.local.yaml` 使用同一库**；库名相同必须**阻断**测试流程，等待用户部署 apifox 测试专用库并回填配置后再继续。目的：apifox 测试数据与本地开发数据隔离，避免测试污染 local 库。
- 稳定决策：**数据基准（local → apifox 测试库，强制）**——**apifox 以 local 数据库数据为基准**（local 库通常同步正式环境线上数据，测试更准确）；「默认 apifox 环境」仅指被测服务启动环境，**不代表禁止使用 local 配置/数据**，数据可从 local 单向流通到 apifox 供测试使用。**数据准备优先级**：① apifox 库无数据且 local 有 → **优先**从 `config.local.yaml` 指向的 local 库**单向灌数据**到 apifox 测试库（默认路径，不限于旧接口）；② apifox 与 local 都无数据 → **apifox 自行创造测试数据**。约束不变：local 库**只读源**（仅 SELECT、禁止写入/删除）、**禁止反向回灌**、禁止从 test/prod/staging 取数、脱敏并记录来源库/表、条数、时间（可追溯）。与库分离不冲突：分离管「测试写入不污染 local」，灌数据是「初始化 apifox 库数据」。
- 稳定决策：apifox 环境属接口测试专用，不改变 `local`/`test`/`prod` 既有语义；`test`/`prod`/`staging` 配置一律不用于本地接口测试（环境红线不变）。
- 稳定决策：**被测服务 environment 白名单只允许 `local` 与 `apifox`，选择优先级按项目配置决定**——项目**存在 `config/yaml/config.apifox.yaml`（含同仓 `backend/config/yaml/config.apifox.yaml`）时默认使用 `apifox` 环境**（被测服务 `-env apifox` 启动）；项目**没有 apifox 环境配置时默认使用 `local` 环境**；`test`/`prod`/`staging`/`pre`/`release` 等非 local 环境一律禁止用于本地测试与接口测试。
- 稳定决策：**apifox 测试专用项目直接 `main` 分支操作**——用户为 apifox 测试**单独创建的项目**（项目级隔离已足够），apifox 项目内**接口文档操作、测试、补充测试用例直接在 `main` 分支（如 `1.main`）操作**，**不新开 AI 分支 / api 分支，不做「开分支 → 自动化测试 → 合并回 main」的多余操作**；仅当目标项目不是 apifox 测试专用项目（如共享主项目）或 main 分支受保护不可直接写时，才走 AI 分支兜底（`ai/年月日-...` + pick-to + 合并）。
- 稳定决策：**临时库特权（apifox 环境，强制）**——**前提是项目已提供 apifox 环境配置**（有 `config/yaml/config.apifox.yaml` + 对应 apifox 测试专用库）。模型测试需要**宽泛权限**（建表/复杂数据构造/大范围写操作等超出 apifox 专用库约束的场景）时，**允许 apifox 环境自行新建临时库测试使用**：① 临时库名必须以 **`tmp` 前缀**标识（如 `tmp_<测试用途>`），用于与正常库区分；② **生命周期（建→用→删，强制）**：测试完成后**必须删除**（`DROP DATABASE`），删除动作记录到 `PROJECT_TEST.md`（库名/用途/删除时间）；③ **删除边界**：只有 `tmp` 前缀临时库允许删除，**正常库（非 `tmp` 前缀，含 apifox 测试专用库、local 库）一律禁止删除**——即使 apifox 环境具备连接权限也不得删除。与库分离不冲突：分离管「apifox 专用库 ≠ local 库」，临时库是在 apifox 专用库之外额外创建的生命周期库，用完即删。
- 来源：`package-structure-rules/references/configuration-layout.md`、`package-structure-rules/references/placement-catalog.yaml`、`package-structure-rules/SKILL.md`、`apifox-cli__skillhub/modules/environment.md`、`apifox-cli__skillhub/SKILL.md`、`test-strategy-rules/SKILL.md`、用户需求确认（2026-08-21 重新规划 apifox 测试分离库方案）。
- 更新时间：2026-08-21。

## Apifox 接口展示与阅读简体中文统一规范（API 路径英文不变）

- 稳定决策：**机器调用走英文，人类阅读全中文（强制铁律）**——团队成员背景多元，接口文档是团队协作与联调的核心资产。规范强制要求：**API 路径保持原有英文路径不变，但所有用于展示和阅读的内容必须统一使用简体中文**。在通过 skill 生成、导入或更新接口定义时，必须严格按此规范执行，确保团队中不熟悉英文的成员也能直接读懂接口文档。
- 稳定决策：**API 路径英文保持**——接口 URL Path（如 `/health`、`/api/v1/auth/login` 等）作为网络协议契约，严格保持原有英文路径不变，禁止翻译为中文拼音或汉字。
- 稳定决策：**接口显示名称中文化**——接口显示名称（name / summary / title）必须统一为规范业务简体中文（如：`健康检查`、`用户登录认证`），严禁直接用英文单词、缩写或方法名作为显示名称。
- 稳定决策：**文件夹名称中文化**——接口目录（folder name）必须统一使用业务领域简体中文命名（如：`认证授权`、`服务注册`、`任务管理`、`策略配置`、`审计日志`、`租户管理`），严禁在左侧文档树中创建或保留 `auth`、`registry`、`tasks` 等纯英文文件夹。
- 稳定决策：**接口说明文档中文化**——接口说明（description）必须使用简体中文，详述业务背景、调用时机、调用限制与操作指引。
- 稳定决策：**请求参数与响应字段注释中文化**——Path、Query、Header、Body 每个参数以及响应 JSON Schema 与响应头的每个属性 `description`，必须统一使用非空简体中文注释说明其业务含义、约束与取值范围。
- 稳定决策：**即时审计硬动作**——在通过 skill 生成、更新或同步接口定义后，必须立即执行硬动作 A1（接口中文名+说明+参数/响应中文注释审计）与 A11（业务 folder 归类与中文命名审计），不合格项必须当轮修复归零，不得以英文或空注释草率收口。
- 来源：用户指令（2026-09-13）+ 客户端截图红框证据 + `apifox-cli__skillhub/SKILL.md` + `apifox-cli__skillhub/modules/{api-design,api-folder-organization,api-sync-to-apifox,import-export,project-onboarding-checklist}.md`。
- 更新时间：2026-09-13。


## 计划输出完整性规则

- 稳定决策：`implementation-planning-rules` 的正式实施计划必须零决策完整落盘；plan-structure-template.md 禁止在最终输出时压缩或省略思考阶段已形成的任何落点、文件/符号、命令、断言、回滚和完成条件。
- 稳定决策：宿主外层包裹（如 `<proposed_plan>`）的简洁/3-5小节要求仅影响包裹层，不得删减计划正文中的任务字段、细节或零决策事项；仓库模板完整度优先于宿主简洁要求。
- 稳定决策：plan-output-gate.md 硬失败结构包含内容密度 hard-fail：最小任务缺少零决策字段（文件/符号、操作、禁止触碰、精确测试命令、断言、清理、回滚、完成条件、停止条件中任一项）或出现"见上文""后续再定""若干文件""TBD""TODO""实现时再看"等占位词时直接不合格。
- 稳定决策：正式实施计划的主章节仅包含章节标题、各任务缺少可执行具体字段内容即为无效计划；代码变更类计划必须给出代码落点目录树（text 代码块）。
- 稳定决策：正式计划必须跨会话自包含：冻结主项目地址、仓库类型、代码基线、新会话接手第一步、当前周期/任务、local 环境入口和中断点核验顺序；计划不得依赖思考过程、悬浮窗或隐含工作目录。
- 稳定决策：引用其他项目代码必须逐项提供 `EXT-*`、可复现地址、版本/提交、项目根相对路径、文件/符号、用途、许可证/复制边界、可达性失败停止条件和验证回指；无外部引用必须写 `N/A + 原因 + 证据`。
- 来源：`implementation-planning-rules/references/plan-structure-template.md`、`plan-output-gate.md`、`plan-review-checklist.md`、`minimum-task-execution-contract.md`、`implementation-overview-template.md`、`implementation-cycle-template.md`、`plan-entry-checklist.md`、`cross-session-plan-execution-contract.md`、`agents/openai.yaml`、`AGENTS.md`、`CLAUDE.md`、`test/implementation-planning-rules/plan_output_contract_test.py`、`doc/3-实施/2026-08-09_190217_REQ-PLAN-DETAIL-COMPLETE-002_实施总览.md`。
- 更新时间：2026-08-09。


## 会话交接与新任务接续规则

- 稳定决策：`session-handoff-rules` 是会话迁移唯一 Owner；命中“开新会话继续”“新会话中继续”“新会话继续”“会话太长”“归档旧会话”“迁移任务”“接续任务”“提取会话压缩信息”“唤起另一个会话”等语义时，先提取当前目标、范围、已完成、进行中、下一步、阻断、验证和关键决策，再生成脱敏交接包。
- 稳定决策：交接包使用 `codex-session-handoff` v1 JSON 契约，字段白名单、UTF-8、24,576 字节上限、`next_steps` 非空和敏感字段 / 绝对路径拒绝由 `session-handoff-rules/scripts/validate_handoff_packet.py` 校验；交接包不得保存 `session_id`、`thread_id`、prompt、完整日志或凭据。
- 稳定决策：新任务必须先用 `codex_app__list_projects` 精确匹配当前保存项目，再用 `codex_app__create_thread` 的同项目 `environment: local` 创建；创建返回真实 `threadId` 后才可调用 `codex_app__wait_threads`，`clientThreadId` 只能报告 setup pending，不得当作真实线程 ID。
- 稳定决策：新任务首轮必须重新命中 `skill-hit-check-rules`、读取项目四件套、按自身 `session_id` 校验或建立 projection，并核验进行中断点；交接不复制旧任务 UI 状态、执行授权或未知非幂等操作。
- 稳定决策：v1 归档策略固定为 `manual_only`。新任务 ready 后只提示用户人工归档旧任务，不自动调用 `codex_app__set_thread_archived`；创建失败、项目不确定或 setup pending 时不改变旧任务状态。
- 来源：`session-handoff-rules/SKILL.md`、`session-handoff-rules/references/handoff-packet-contract.md`、`session-handoff-rules/references/codex-thread-routing.md`、`session-handoff-rules/scripts/validate_handoff_packet.py`、本轮用户确认的触发词。
- 更新时间：2026-08-02。


## Plan Mode 决策选择框永久等待规则

- 稳定决策：Plan Mode 决策型 `request_user_input` 必须完全省略 `autoResolutionMs`；选择框未得到用户选择时保持 `WAITING_DECISION`，没有等待时间或重发次数上限，宿主空答案不代表取消、授权、默认选择或完成。
- 稳定决策：`answers:{}`、答案缺失、缺少预期问题 ID、`null`/空返回和宿主隐式超时的下一动作只能是立即串行重发同一未决选择框；重发保持问题 ID、选项、推荐标记和冻结文案，部分答案只保存并重发剩余问题，每次只保留一个活动选择框。
- 稳定决策：未决循环期间禁止冻结集合 `commentary`、`limited_plan`、`pending_summary`、`proposed_plan`、`final`、`summary`、`final_answer`、`task_complete`、`result_and_conclusion` 及中文“结果与结论”输出；也不得自动采用推荐项、创建 Goal、恢复任务投影或触发自动升级；总结消费方必须拒绝任何未决 `request_user_input` / `WAITING_DECISION`。
- 稳定决策：只有用户完成全部选择、明确授权“你来定/按推荐”、明确要求停止，或工具明确不可恢复且无法再次调用时才离开等待；工具故障仍保持未决并报告宿主阻断。上下文压缩或会话恢复必须保留问题身份、选项、已选答案和等待状态。
- 来源：`implementation-planning-rules/SKILL.md`、`implementation-planning-rules/references/plan-question-coverage.md`、`implementation-planning-rules/references/plan-output-gate.md`、`reasoning-summary-structure-rules/SKILL.md`、`doc/4-bugs/2026-07-26_040639_PlanMode选择框永久等待/README.md`、`doc/7-验收/2026-07-26_040639_BUG-PLAN-WAIT-20260726-001_验收标准.md`、`doc/5-tests/2026-07-26_040607/plan_mode_wait_loop/test_plan_mode_wait_loop.py`。
- 更新时间：2026-07-26。


## 六域 Skill 精简与自动触发保护规则

- 稳定决策：需求、实施、测试、Bug 与 `6-review` 风格回归精简时，用户习惯、自动触发、授权、安全、local、输出协议、暂停与停止边界均为保护语义；可以迁移位置，不得删除或弱化。独立业务审查与后置验收不再是活动域。
- 稳定决策：同生命周期收敛为单主入口加条件路由；主 Skill 保留触发摘要和职责边界，重复细则下沉 references。
- 稳定决策：退役旧 Skill 前必须具备 source-target mapping、trigger contract、protected semantic IDs、active consumers、physical asset owner、baseline hashes、rollback locator 与正负 post-delete 证据；缺任一项保持 `hold`。
- 稳定决策：`implementation-planning-rules` 保持 Plan Mode 唯一入口，只做正文去重和 references 化，不拆为竞争入口。
- 稳定决策：历史归档不批量回写旧名称；活跃资产必须完成引用切换。
- 来源：`doc/2-需求/2026-07-21_221037_六域Skill结构精简与自动触发保持.md`、`doc/7-验收/2026-07-21_221037_六域Skill结构精简与自动触发保持_验收标准.md`。
- 更新时间：2026-07-21。


## 白话文档与附录分层规则

- 需求、实施、Bug、测试、`6-review`、架构、交付和工作报告采用同一信息分层：H1 后单段正文固定说明结论、影响、范围、非范围、变化、完成标准、术语说明和验证状态；文件、命令、稳定 ID、追踪矩阵和证据分别进入执行附录或追踪附录。
- 新活动文档不再使用 `review_acceptance_gates`；完成条件写入实施计划，真实测试产生 `TEST` 证据，`6-review` 只产生 `STYLE: PASS/FIX_REQUIRED`。历史审查和验收文件保留该字段时只读兼容。
- 新文档以 `reader_level: business_general`、`writing_style: plain_chinese`、`appendix_policy: preserve_existing_or_one_terminal_appendix` 启用机器门禁；受管模板由 `plain-language-template-registry.yaml` 统一登记并逐项测试；未修改历史文档不批量迁移。
- 功能验证、浏览器联调和第三方验证按各自测试规则处理；后置审查和最终验收不再构成活动放行分支。

## 配置环境来源契约

- 稳定决策：`package-structure-rules` 的 loader 条目必须记录统一环境来源优先级 `-env > APP_ENV > ENV > local`；reference 正文、Catalog、Schema 和活动契约测试必须保持同一表达。该契约只描述配置 loader 的来源识别，不改变 yaml/ 私密边界或真实项目迁移授权。
- 稳定决策：`config/yaml/` 是唯一配置模式，只存放配置数据，允许有意持久化真实密钥、密码、token、私钥原值、默认不依赖环境变量，但 Agent 输出、日志、README、错误和测试报告不得泄露原值。`config/embedded/` 已废弃：strict 下存在即报错，adoption 下须登记 `legacy_source_roots` 才能继续维护。环境配置文件统一使用点中缀命名 `config.<env>.yaml`（Go 生态主流，如 `config.local.yaml`，兼容 `.yml`）。Go 项目由 `config/load.go` 通过 `//go:embed yaml/config.*.yaml` 编译期嵌入并按环境读取；非 Go 语言从文件系统读取 `yaml/config.<env>.yaml`。YAML 条目标记 `yaml_mutually_exclusive` 字段保留（元数据，脚本不消费）。该模型取代旧的“embedded/YAML 二选一互斥、推荐 embedded”口径。
- 来源：`package-structure-rules/references/configuration-layout.md`、`package-structure-rules` Catalog/Schema 改动和配置契约测试。
- 更新时间：2026-08-13。
- 来源：`artifact-delivery-gate-rules/references/plain-language-document-contract.md`、`artifact-delivery-gate-rules/references/review-acceptance-gate-contract.md`、`artifact-delivery-gate-rules/scripts/validate_engineering_docs.py`。
- 更新时间：2026-07-14。

## WorkBuddy 官方市场规则吸收整理补充

- 稳定决策：吸收官方市场同类 skill 时以「整理补充」为原则，不是无限制累加，也不是整套复制。本地规则已经更完整的方向只做归纳；官方真正更优的少量动作才吸收进既有 skill 的 `references/`；不新建同类 skill，不复制官方工作流、问答链或目录结构。
- 稳定决策：需求域吸收官方 100 分质量门，落为 `requirement-intake-rules/references/workbuddy-quality-gate.md`；实施域吸收「编码前先探索代码库」，落为 `implementation-planning-rules/references/pre-implementation-code-exploration.md`；Bug 域吸收「修复前先分级风险并确认」，落为 `bug-fix-proposal-rules/references/fix-risk-grading-and-confirmation.md`；测试域吸收「风险分层后给出明确测试结论」，落为 `test-strategy-rules/references/risk-based-test-conclusion.md`。
- 来源：`implementation-planning-rules/references/workbuddy-absorption-map.md`、四个 skill 的 references、`doc/2-需求/2026-08-13_110000_WorkBuddy官方市场规则吸收整理补充.md`。
- 更新时间：2026-08-13。

## 项目级 Skill 自动沉淀落点规则

- 稳定决策：项目级 skill 统一落地用户级 `~/.workbuddy/skills/project-<项目slug>-<topic>-rules/`（junction 与 luode-skills 仓库物理同址），不再使用项目根 `skill/`（非标准加载路径、不会被自动命中、历史零落地）。
- 稳定决策：`project-local-skills-rules` 是项目级 skill 自动沉淀唯一 Owner，description 语义命中双通道触发（任务收口自动评估 + 用户点名）；自动评估聚焦项目写操作，触发条件为 5+ tool call / 踩坑解法 / 用户纠正 / 复用 workflow；不沉淀一次性任务、用户拒绝、纯闲聊。
- 稳定决策：quick_validate.py 要求 description 不得含尖括号（< >），模板占位符用自然语言描述。
- 来源：`project-local-skills-rules/SKILL.md`、`project-local-skills-rules/references/auto-trigger-and-evaluation.md`、`references/dedup-and-update.md`、`references/workbuddy-absorption-map.md`、`references/source-notes.md`。
- 更新时间：2026-08-19。

## 低分 Skill 优化 SOP 规则

- 稳定决策：评分巡检中低分 skill 的优化统一按 `skill-absorption-rules/references/low-score-skill-optimization-sop.md` 八步闭环执行（基线核验→市场检索→同域对照→裁决确认→落盘→机器校验→独立复评→闭环修复+沉淀）；市场检索为低收益动作（八轮 28+ 组关键词 0 候选），重点放在同域对照与「让脚本兑现宣称」。
- 稳定决策：优化闭环收口必须含独立子代理 7 维复评（固定输出格式 `skill|D1..D7|总分|短板`）+ 维度 8 本机实测；复评发现问题按「本侧修正」原则闭环修复，不跨 skill 修改成熟资产。
- 稳定决策：工具类 skill 的「隐性失实」短板（宣称"开箱即用"但框架依赖未装、宣称"免费无 key"但数据源不可达）→ 修复模式为「去框架依赖 + 数据源诚实声明 + `--check` 探测命令」，而非换源重写；DNS 解析到私有网段（172.x/10.x）+ TLS 握手失败 = 域名级不可达判据（free-api-50__skillhub 轮沉淀）。
- 来源：`skill-absorption-rules/references/low-score-skill-optimization-sop.md`。
- 更新时间：2026-08-26。

## 任务阻断收口与恢复规则

- 真实阻断唯一使用 `artifact-delivery-gate-rules/references/task-blocker-closure-contract.md` 的 `BLK-*` 记录，至少包含任务状态、阻断阶段、依据与证据、已尝试动作与停止边界、影响、至多三步解决计划、恢复后重入点、去重键和必填字段“用户授权操作”。
- 稳定决策：真实阻断收口必须展示“用户授权操作”，用户只需回复“同意授权”即可授权执行最近一条、唯一有效、仍未解除的 `BLK-*` 记录列明的恢复动作，回复“暂不授权”保持阻断；授权后必须执行原恢复步骤并通过原验证入口，验证失败保持阻断；授权不构成跨任务、跨会话或未来任意写入的通用许可。
- 审查、验收、功能验证、Bug 验证、执行失败和运行时恢复只生产或校验阻断事实；`reasoning-summary-structure-rules` 是唯一面向用户渲染“任务阻断收口”的 owner，避免多处输出冲突计划。
- 仅 `blocked` 与 `manual_handoff` 触发任务阻断收口。`limited`、`not_applicable`、P2/P3、用户取消和预期负向测试不得生成 `BLK-*` 或写成任务已阻断。
- 阻断计划最多三步；每步必须包含责任方、前置条件、动作、完成判据和验证入口。恢复后从原测试、复审、重验或健康检查的重入点继续。
- 文档校验的正文 `N/A` 规则忽略 fenced code、示例与 Mermaid 内容，避免图中“不适用”分支被误判；正文声明仍必须给出原因或证据。
- 来源：`artifact-delivery-gate-rules/references/task-blocker-closure-contract.md`、`reasoning-summary-structure-rules/SKILL.md`、`artifact-delivery-gate-rules/scripts/validate_engineering_docs.py`、`doc/2-需求/2026-08-09_214745_REQ-BLK-AUTH-001_任务阻断授权操作提示.md`、`test/artifact-delivery-gate-rules/blocker_authorization_contract_test.py`。
- 更新时间：2026-08-09。

## Windows PowerShell 环境可靠性规则

- `windows-powershell-environment-rules` 的会话默认策略是 `RequiredOnly`：`ready` 和 `degraded` 可以继续，只有 `blocked`、`busy`、`failed`、`rollback_refused` 不能作为已准备好结论。
- 包恢复只接受 manifest 或调用方提供的精确 source/package ID；未知命令不搜索猜包。Git Bash 只能从 Git 安装根目录的 `bin\\bash.exe` 加 `MINGW|MSYS` 身份识别，WSL 原生命令不再由 `windows-wsl-execution-rules` 承接（该 skill 已删除，由 `wsl-windows-bridge` 提供 WSL↔Windows 工具桥）。
- profile 与 Terminal 的 Apply/Rollback 由事务、备份和 after hash 保护；WhatIf 不写用户状态，hash 漂移时必须拒绝覆盖。含中文的 PowerShell 5.1 脚本使用 UTF-8 BOM，避免被默认 ANSI 解码。
- 验证固定为临时目录 fixture：PowerShell 5.1 与 PowerShell 7 都要通过 TEST-PSENV-001 至 TEST-PSENV-009；不连接网络、不安装软件、不改真实用户配置。
- 稳定决策：任何一次调用 PowerShell 命令（不是进入交互式终端）都必须显式使用 `-NoProfile -ExecutionPolicy Bypass -Command`；5.1 回退路径还要先在命令体设置 `[Console]::OutputEncoding = [System.Text.Encoding]::UTF8`，7 路径继续优先 `pwsh -NoLogo -NoProfile -ExecutionPolicy Bypass -Command`。标准调用前缀唯一真源随 `windows-wsl-execution-rules` 删除而撤销，现以 `windows-encoding-rules/SKILL.md` 内联前缀为唯一真源，`windows-encoding-rules` 与 `windows-powershell-environment-rules` 只做交叉引用。
- 来源：`windows-powershell-environment-rules/SKILL.md`、`references/runtime-state-contract.md`、`windows-encoding-rules/SKILL.md`、`doc/2-需求/2026-08-14_223800_PowerShell控制继续优化.md`、`doc/3-实施/2026-08-14_223800_PowerShell控制继续优化_实施总览.md`、`doc/3-实施/2026-08-14_223800_PowerShell控制继续优化_实施周期01_标准调用前缀与三skill衔接.md`。
- 更新时间：2026-08-14。

## 统一智能体运行期自恢复规则

- 稳定决策：`agent-runtime-recovery-rules` 是厂商无关的运行期恢复唯一 owner，覆盖 MCP、插件、浏览器会话、工具 transport 和智能体宿主；安装/注册仍由安装类 skill 负责，失败分类与案例生命周期仍由 `execution-failure-learning-rules` 负责。
- 稳定决策：恢复动作必须通过真实 adapter capability 准入，能力等级为 L0 观测、L1 探针、L2 重连、L3 重载、L4 受控重启、L5 检查点恢复与任务续接；无 L5 lifecycle API 时不得宣称任务自动续接。
- 稳定决策：运行期恢复固定使用单飞锁、一次不变复验、每层最多一次动作、默认 600 秒冷却、幂等性分类和脱敏 checkpoint；非幂等或幂等性未知的写操作只允许查询状态并转人工交接。
- 稳定决策：当前仓库只提供标准库状态原语 `agent-runtime-recovery-rules/scripts/recovery_state.py` 与 local 契约测试；真实平台插件重载、宿主重启和 L5 resume 由外部 adapter 提供，不能由规则猜测或伪造。
- 来源：`agent-runtime-recovery-rules/SKILL.md`、`references/adapter-contract.schema.json`、`doc/2-需求/2026-07-12_210000_统一智能体运行期自恢复规则.md`。
- 更新时间：2026-07-12。

## 通用上线测试（apifox 链路）

> 原 `project-interface-release-execution-rules`（含 `release_test_engine` 引擎）已于 2026-08-18 退役并并入 apifox 测试链路（`apifox-cli__skillhub/modules/`）。

- 稳定决策：上线接口测试统一走 apifox：范围选择 `test-selection-policy.md`（P0/P1/P2）、用例生成 `test-case-generation.md`、数据构造与响应判定 `test-data-and-judgement.md`、陷阱规避 `testing-pitfalls.md`；`apifox test-case run` / `test-suite run` 为执行入口。
- 稳定决策：所有运行连接只来自 `local` 配置；普通业务写接口允许执行，DROP/TRUNCATE/破坏性 ALTER、源码/基础设施删除等极端操作由安全 denylist 阻断。
- 稳定决策：接口级结果固定为 `PASS`、`EXPECTED_FAIL`、`UNEXPECTED_FAIL`、`PENDING`；P0 入口任意非 `PASS` 阻断项目放行，项目门禁输出 `PASS`/`FAIL`/`PARTIAL`。
- 稳定决策：项目接口事实基线仍由 `project-interface-baseline-rules` 沉淀在 `doc/5-tests/基线/`；apifox 执行前确认基线最新，执行后回写新发现接口与参数来源。
- 稳定决策：报告明细的 request/response 固定为脱敏 JSON 字符串，`responses.json` 保留脱敏对象；基线以 append-only 事件和 v2 原子投影为事实源。
- 稳定决策（2026-08-19 扩展）：接口级测试执行通道从「上线门禁专用」扩展到「所有接口级测试」——接口功能验证、回归、Bug 接口验证、上线门禁的接口部分统一走 apifox 真实测试并落地用例到 apifox「AI 团队」对应项目（`apifox test-case run` / `test-suite run`），环境只允许指向 local（localhost）；单元测试/代码级测试保留本地 go test/pytest。权威节为 `test-strategy-rules` 的《接口测试执行通道（强制）》；apifox skill 新增 `modules/ai-team-project.md`（AI 团队项目 projectId 解析与登记）与 `modules/api-sync-to-apifox.md`（接口新增/更新同步 apifox 强制流程，swag 生成仍归 swag-openapi-maintainer-rules）。
- 稳定决策（2026-08-20）：测试域单一事实源为项目根 `PROJECT_TEST.md`（Apifox 项目绑定 + 覆盖度铁律，团队/projectId/默认分支只登记一次）；任何 apifox 操作前先读该文件，未登记则阻断并要求用户指明。`AGENTS.md`/`CLAUDE.md` 仅保留指向 `PROJECT_TEST.md` 的一行指针，不重复写 projectId（避免多工具口径漂移）。
- 稳定决策（2026-08-20）：apifox 环境三约定——默认测试执行环境 = apifox「开发环境」（baseUrl `http://127.0.0.1:<项目端口>`，即 local）；测试环境/正式环境保留存在但 agent 禁止选用（不删除、不修改、不选用，仅由人/CI 使用）。项目无可用开发环境时按 `modules/environment.md` 默认创建，环境 ID 回填 `PROJECT_TEST.md` 的「本地测试环境」表。
- 稳定决策（2026-08-20）：开发环境必须**配置齐备环境变量**（鉴权签名 apiKey/apiSecret、默认测试登录账号密码、token 等），清单回填 `PROJECT_TEST.md`「环境变量登记」表（只登记名称/用途/来源，敏感值不落文档）；用例运行 401/403/签名错误先查环境变量缺失再查接口，不算接口失败。
- 稳定决策（2026-08-20）：鉴权自动化四方案（`apifox-cli__skillhub/modules/test-auth.md`）——A 登录用例+extractor 提取（默认）；B 前置脚本自动续期（token 过期快必用，preProcessor customScript 查 JWT exp 快过期重登）；C 本地脚本构造（JWT 自签/批量预取）；D 全局身份认证（优先启用，D+B 组合最稳）。测试默认用管理员账号；token 必须自动获取/续期，禁止手工复制粘贴。
- 稳定决策（2026-08-20）：**apifox CLI 是硬依赖（强制）**——任何 apifox 操作前先 `apifox --version`，未安装必须立即安装（`npm install -g apifox-cli`，慢则切 `--registry=https://registry.npmmirror.com/`），装完验证版本并登录；不得以"CLI 未安装"跳过任务。完整流程见 apifox skill SKILL.md「安装（强制，最高优先级）」节。
- 稳定决策（2026-08-20）：apifox 开发环境必须配置齐备环境变量（鉴权签名 apiKey/apiSecret、默认测试登录账号密码、登录后提取的 token 等），缺失即视为开发环境未就绪；用例运行失败（401/403/签名错误）先查环境变量。取值只从 local 配置或用户提供；敏感变量值不落文档（`PROJECT_TEST.md` 只登记名称/用途/来源）。清单见 `PROJECT_TEST.md`「环境变量登记」表。

## 核心记忆

### 仓库定位
- 别名: skill 仓库, 团队研发协作规则仓库
- 类型: 项目事实
- 定义: 本仓库用于沉淀面向团队研发协作的 Skill、references、脚本和入口文档，目标是让 AI 在需求、Bug、编码、实施计划、真实测试、`6-review` 和交付流程中按任务内容自动命中规则。
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
- 定义: 正式研发产物目录统一收口到 `doc/` 下；当前活动子目录按流程顺序编号为 `doc/1-架构/`、`doc/2-需求/`、`doc/3-实施/`、`doc/4-bugs/`、`doc/5-tests/`、`doc/6-review/`；`doc/6-审查/` 与 `doc/7-验收/` 仅作为历史只读归档。
- 来源: `artifact-storage-rules/references/path-map.yaml`
- 适用范围: 文档归档与规则引用
- 更新时间: 2026-06-28
- 状态: 启用

### 过程产物退场规则
- 别名: doc 文档生命周期, 长期文档清理, 过程产物退场, 半个月阈值
- 类型: 目录规则
- 定义: `doc/3-实施/`、`doc/4-bugs/`（限已闭环）、`doc/5-tests/`（不含 `基线/`）、`doc/6-review/` 是过程产物，最后修改超过 15 天（半个月）仅构成退场候选，不构成退场理由。必须同时满足四道前置守卫：沉淀守卫（可复用结论已真实进入知识库笔记且可检索，判定由 `knowledge-flow` 负责）、引用守卫（全仓库引用数为 0）、闭环守卫（来源对象已闭环且无未决 P0/P1、无未关闭 gap、无进行中实施周期）、可恢复守卫（已被 Git 跟踪且历史提交存在）。四道守卫全满足并经用户明确确认后，以 `git rm` 删除，不保留并行归档副本、不新建归档目录，单批次不超过 10 个文件。`doc/1-架构/`、`doc/2-需求/`、`doc/5-tests/基线/`、`doc/6-审查/`、`doc/7-验收/` 与根目录 `项目设计.md` 属长期资产，不适用时间退场。
- 来源: `artifact-storage-rules/SKILL.md`、`artifact-storage-rules/references/lifecycle-policy.md`、`artifact-storage-rules/references/path-map.yaml`
- 适用范围: doc 产物归档治理、长期过程文档清理与退场判定
- 更新时间: 2026-09-10
- 状态: 启用

### 活动文档命名前缀
- 别名: 来源对象标识, 实施需求标识, 风格回归时分秒, Bug 进入实施计划
- 类型: 命名规则
- 定义: 需求、实施、Bug、测试和 6-review 活动产物统一使用 `YYYY-MM-DD_HHmmss` 时间前缀。实施与 6-review 等下游文档必须在时间后保留来源对象标识，来源可以是需求也可以是 Bug；历史审查/验收文件只读保留。禁止只写 `时间_阶段_说明.md`、`YYYY-MM-DD_主题.md` 或缺少来源标识的 `YYYY-MM-DD_HHmmss_主题.md`。
- 来源: `artifact-storage-rules/references/path-map.yaml`、`artifact-storage-rules/references/naming-templates.md`
- 适用范围: 需求域、实施域、Bug 域、测试域、6-review 风格回归域
- 更新时间: 2026-06-29
- 状态: 启用

### Skill 体积治理统计基线
- 别名: Skill 体积预算, 规则文档体积基线, 默认文本包
- 类型: 统计口径
- 定义: 截至 2026-07-17，正式字典主规划包含 84 个 skill；仓库根目录实际存在 111 个带 `SKILL.md` 的目录，其中 27 个属于扩展种子，不纳入主规划拆分基线。默认文本包定义为单个 skill 的 `SKILL.md` 加 `references/` 下全部文本资源的原始字节数。预算等级固定为 `normal`、`review`、`split_candidate`、`hard_warning`：`normal` 不超过 `SKILL.md` 16,000 B、单 reference 最大 12,000 B、默认文本包 48,000 B；超过建议值进入 `review`，超过 SKILL.md 20,000 B、单 reference 16,000 B 或默认文本包 64,000 B 进入 `split_candidate`，SKILL.md 超过 24,000 B 进入 `hard_warning`。
- 来源: `doc/5-tests/2026-07-17_155229/skill-split-validation/skill-size-report.py`、`doc/5-tests/2026-07-17_155229/skill-split-validation/skill-size-report.json`、`字典.md`、`doc/2-需求/2026-07-16_114619_Skill体积治理与拆分.md`
- 适用范围: Skill 体积盘点、候选冻结和后续职责拆分复评
- 更新时间: 2026-07-17
- 状态: 启用

### Skill 体积候选冻结
- 别名: Skill 拆分候选矩阵, 候选顺序, 正式/扩展种子双层追踪
- 类型: 拆分决策
- 定义: `TASK-SPLIT-01-02` 将正式 84 个 skill 与扩展种子 27 个分层记录在 `candidate-matrix.yaml`；正式进入拆分的 4 项为 `project-agents-bootstrap`、`skill-compliance-gate-rules`、`project-release-test-rules`、`agent-browser`，每项均有两个独立职责组；`2d-asset-design` 作为 P1 扩展种子例外进入 CYCLE-SPLIT-06；MCP 进入 P2 候选设计，implementation-planning 进入条件复评，其余保持暂缓或不候选。
- 来源: `doc/5-tests/2026-07-17_155229/skill-split-validation/mapping/candidate-matrix.yaml`、`doc/3-实施/2026-07-16_114619_Skill体积治理与拆分_实施周期01_预算与候选冻结.md`、`doc/7-验收/2026-07-16_114619_Skill体积治理与拆分_验收标准.md`
- 适用范围: 后续 CYCLE-SPLIT-02 至 CYCLE-SPLIT-08 的候选进入、职责映射和测试入口选择
- 更新时间: 2026-07-17
- 状态: 启用

### Skill 拆分通用测试入口
- 别名: `TEST-SPLIT-003`, 五类拆分验证, pre/post-delete fixture
- 类型: 测试契约
- 定义: `TASK-SPLIT-01-03` 固化 `validate_skill_split.py` 的 `size`、`mapping`、`trigger`、`pre-delete`、`post-delete` 五类模式，并由 `run_trigger_cases.ps1` 通过 `-CasesRoot` 转发。报告和矩阵路径必须位于仓库根目录内，fixture 根必须位于当前测试时间戳目录内；越界必须非零失败，不删除真实 skill。
- 来源: `doc/5-tests/2026-07-17_155229/技能拆分验证/README.md`、`doc/3-实施/2026-07-16_114619_Skill体积治理与拆分_实施周期01_预算与候选冻结.md`
- 适用范围: CYCLE-SPLIT-02 至 CYCLE-SPLIT-08 的静态覆盖、触发、删除前后和路径边界验证
- 更新时间: 2026-07-17
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
- 定义: 当用户只提出一句话 idea、粗略想法或老板式方向时，优先由 `requirement-intake-rules` 的 `initial-discovery` 路由主动侦察当前项目代码、文档、数据库线索、上下游服务、第三方调用、关联项目、GitHub、相关网站、官方 API 文档和用户补充路径或 URL，形成有证据来源的需求设计；外部资料默认遵循“官方文档/官网/自有仓库与站点优先，公共 GitHub 与社区资料只作补充”的优先级。已验证可复用的资料位置、数据库、URL、项目路径和侦察经验必须继续通过 `project-memory-rules` 回写长期记忆。
- 来源: 对话确认、`requirement-intake-rules/references/initial-discovery-route.md`
- 适用范围: 需求域
- 更新时间: 2026-06-28
- 状态: 启用

### 需求域第一入口
- 别名: 需求 skill 顺序, 需求前置入口
- 类型: 流程规则
- 定义: 当前对外统一流程为 `Idea/Discovery -> Intake -> 条件闸门 -> 实施计划（含 AC 完成条件） -> 实现 -> 真实测试 -> 6-review -> 交付总结`。其中需求域主流程仍收口到 `Idea/Discovery -> Intake`，条件步骤为 `Gap / Boundary / Splitting / Change`；`implementation-planning-rules` 负责把完成条件、异常边界、停止条件和测试映射冻结在实施计划中。内部统一由 `requirement-intake-rules` 作为第一入口；粗略 idea 进入 `initial-discovery` 路由，主入口负责立即创建需求主文档，`requirement-intake-rules` 的 `gap-routing` 只处理主动侦察后仍无法补齐的关键缺口。需求阶段只允许读仓库、读资料、整理文档；不允许把 agent 猜测写成需求答案，也不允许“先做了再补需求”。需求主文档未真实落盘前，禁止进入实施规划与正式编码。实施计划完成后仍不得自动开工，必须等用户明确“开始实施/开始执行”后才能进入正式编码。
- 来源: `requirement-intake-rules/references/requirement-domain-shared-contract.md`、`编码skill.md`
- 适用范围: 需求域
- 更新时间: 2026-07-22
- 状态: 启用

### 需求临时缺口文档规则
- 别名: gap 临时文档, 缺口阻断文档
- 类型: 流程规则
- 定义: `requirement-intake-rules` 的 `gap-routing` 只处理 discovery 之后仍无法补齐的关键缺口；gap 阶段允许在 `doc/2-需求/` 下创建一份临时缺口文档，记录已侦察证据、待确认问题和阻断结论。用户确认并补齐后，必须先把稳定结论回填主需求文档，再删除临时缺口文档；未确认前不得删除，也不得继续进入实施计划。

### 实施计划完成条件规则
- 别名: AC 完成条件, 计划内验收口径, 真实测试映射
- 类型: 流程规则
- 定义: 完成标准不再单独生成验收 Skill 或验收文档；`AC-*` 继续写入实施总览、实施周期或任务卡，冻结成功条件、异常边界、范围外、停止条件、真实测试入口和证据映射。真实测试逐条引用 AC 并产生 `TEST` 证据，测试完成后由 `code-style-consistency-rules` 记录一次 `STYLE: PASS` 或 `STYLE: FIX_REQUIRED`。
- 来源: `implementation-planning-rules`、`artifact-delivery-gate-rules`、`code-style-consistency-rules`
- 适用范围: 实施域、测试域、6-review 风格回归
- 更新时间: 2026-08-01
- 状态: 启用

### 根测试代码与测试证据双根规则
- 别名: 根 test 目录, 测试资产镜像, doc/5-tests 证据根
- 类型: 测试资产目录规则
- 定义: 根 `test/` 是唯一活动测试代码根，测试程序、mock、stub、fake、fixture、helper 与启动脚本按被测源码或 Skill 目录镜像存放；源码关联模拟程序必须与对应测试使用同一源码相对路径，只有跨源码复用的模拟能力才进入 `test/shared/`；Python 统一使用 `*_test.py`，模拟程序使用 `_mock`、`_stub` 或 `_fake` 后缀。`doc/5-tests/` 每轮只保存一份扁平测试主文档 `YYYY-MM-DD_HHmmss_<测试任务中文主题>.md`，日志、报告、截图与非可执行产物内联在正文；`doc/5-tests/基线/` 是唯一豁免子目录，上线接口测试机器产物落在 `test/release-artifacts/`。历史 `doc/5-tests/` 子目录及其中的可执行资产由指纹清单只读保护，首次修改、改名或新增时才迁至根 `test/`；Go 测试仅在根 `test/` 的 ASCII 外部黑盒包中运行，源码目录禁止 `*_test.go`。
- 来源: `artifact-storage-rules/references/path-map.yaml`、`test/shared/layout_policy.py`、`doc/3-实施/2026-08-01_191658_根test目录统一_实施总览.md`
- 适用范围: 新增测试、测试资产迁移、测试策略、测试程序、真实测试归档和 6-review 目录归位
- 更新时间: 2026-08-01
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

- 规则变更的完整历史以 git 提交历史为准；关键事件追加到 `PROJECT_HISTORY.md`（保留最近 20 条）；当前生效口径以对应 skill 的 `SKILL.md` 与 `AGENTS.md` 为事实源。
- 本小节只保留最近 10 条尚未沉降到上述三处的过渡性记录，超出即删除，不做无限堆积。历史上本节曾堆积 75 条日期流水共 19KB，违反本文件「只保存稳定规则、关键决策和少量长期事实」的职责定义，且因缺少上限而持续增长；2026-08-12 已清空，逐条核对其当前口径均已被 skill 文件或 `AGENTS.md` 承接。
- 2026-08-12：变更记录清空并加保留上限；跨项目通用判据迁往知识库，本文件只留本仓库落地口径与指针。


## Skill 体积治理与职责拆分

- 稳定统计口径：正式字典主规划有 84 个 skill，磁盘有 111 个带 `SKILL.md` 的目录，其中 27 个属于扩展种子，不纳入正式预算基线；默认文本包按 `SKILL.md` 与直接 references 文本字节数统计。
- 稳定测试契约：通用入口覆盖 `size`、`mapping`、`trigger`、`pre-delete`、`post-delete` 五类模式；报告和矩阵路径不得越出仓库根目录，fixture 根不得越出当天测试时间戳目录；越界必须非零失败且不得删除真实 skill。
- 当前状态：2026-07-17 已完成周期 01 的三个最小任务；2026-08-01 起闭环口径统一为“实施计划完成条件 -> 实现 -> 真实测试 -> 6-review”。周期 01 已收口，周期 02 尚未进入，真实 skill、字典和 Git 历史保持未修改。
- 证据来源：需求、验收、实施总览、实施周期 01、测试 README、当前改动审查报告和 `validate_skill_split.py` 的本地验证结果。
- 知识库沉淀：`20-Knowledge/codex-skills/skill-体积治理与职责拆分计划.md`，并已更新 `INDEX.md` 导航入口。
- 更新时间：2026-07-17。

## 需求与实施文档极致完备化规则

- 需求、验收、实施总览、实施周期和最小任务卡均采用 Markdown + YAML front matter；复杂度为 L2 及以上时，按语义提供 Mermaid 流程图和时序图，L3/L4 追加状态、数据、依赖或故障图。
- 高推理模型冻结业务、技术、测试、回滚、停止和异常决策；普通模型只能按 `REQ -> AC -> PLAN -> CYCLE -> TASK -> TEST -> EVIDENCE` 追踪链执行，不得补默认值或猜测未决决策。
- 每个最小任务必须唯一归属一个实施周期，并完成“实施计划完成条件 -> 实现/落盘 -> 真实测试或有证据的免测 -> 6-review”闭环；缺少任一证据时不得把状态写为已完成。
- `artifact-delivery-gate-rules` 是文档质量唯一机器门禁；profile、严格追踪、N/A 理由、失效链接、Mermaid 语法和 UTF-8 检查失败时必须回开上游文档。
- 实施规划使用单来源实施总览和项目级全量顺序实施方案两层入口；周期状态、任务状态、项目当前状态、真实测试和 6-review 状态必须同步，不能保留已被后续事实超越的旧入口状态。

## 日志使用链路规则

- 读日志侧唯一权威：`log-analysis-rules` 统一承载日志文件定位、DEBUG 级别切换、request-id 反查、取证过滤、调试窗口纪律五项；其它 skill 查日志取证必须引用它，不重复发明读日志步骤。
- 写侧可反查字段：日志必须含 request-id / trace-id / 订单号等可反查稳定标识（纯本地任务用业务键），命名与 `logging-trace-rules` 的 trace-propagation 约定一致。
- apifox 服务端取证：四层诊断无法从响应体定位时进入第 5 步服务端取证，按 request-id 反查服务日志，证据回贴测试主文档；服务日志不可达记 `ENV_LOG_BLOCKED`。
- 测试脚本过程日志：默认放行项（默认必须输出 7 项最小过程日志），实施计划冻结可升级硬判。
- 决策来源：`REQ-LOG-20260825-001`；更新时间 2026-08-25。

## Windows PowerShell 环境自动迭代规则

- `windows-powershell-environment-rules` 的新会话入口是 `initialize_windows_powershell.ps1 -Mode SessionEnsure`；通过用户级 TTL marker 和原子锁避免重复准备，Apply journal 不完整时写 `complete=false`，不得伪造健康状态。
- Windows PowerShell 命令缺失统一经 `recover_windows_command.ps1` / `RecoverCommand` 路由；canonical manifest 或显式精确 `PackageId` 才能安装，未知命令不执行 `winget search` 猜包。
- 安装并真实版本探针验证成功的非 canonical 工具写入用户级 `discovered-tools.json`，仅 `verified=true` 且通过 ID/命令/source 白名单的记录在后续会话合并读取；canonical `tool-manifest.yaml` 不运行时修改。
- 失败摘要写入用户级 `failure-cases.json`，必须 UTF-8、原子替换、去重、限长、脱敏；PowerShell Windows owner 与 WSL 原生 shell/`127` owner 分离。
- 当前 runtime 不提供任意 agent shell 调用的全局失败拦截；自动恢复范围仅限显式 wrapper 或未来接入 runtime hook 的路径。

- 2026-07-21：六域 Skill 精简采用“单主入口 + 条件路由”；需求 discovery 已迁移到 `requirement-intake-rules` 的 `initial-discovery`，自动触发、local 安全、证据、记忆回写、输出和停止边界保持不变。

## 总控层单向路由与合并规则

- 稳定决策：`skill-hit-check-rules` 是每轮唯一首入口；它只确认联动，不复制 Git、失败恢复、并行或 Skill 资产 Owner 的执行细则。
- 稳定决策：`parallel-task-dispatch-rules` 是并行分类与子代理生命周期的唯一 Owner，一次状态机完成串行/条件并行/可并行判定、上下文成本、互斥写集、系统能力与授权、真实启动、主路径继续、结果回收、关闭和回退；计划、启动、完成、关闭数量必须可核对。
- 稳定决策：`context-recovery-rules` 是项目自举唯一 Owner，内部保留 `rule-bootstrap` 与 `memory-bootstrap` 两个自举路由；规则文件非受管内容、UTF-8、`PROJECT_CURRENT.md` 51,200 字节、机器索引和 `PROJECT_HISTORY.md` 追加后只保留最近 20 条（自动裁剪）均为保护语义。
- 稳定决策：压缩恢复先执行共享 `context-recovery-contract`；只有 `recent_context_state=missing` 才条件进入 `warmup` 路由，新会话预热、压缩恢复和明确历史回忆三个入口保持独立。
- 稳定决策：注释细则由注释 Owner 定义，上层审查和收口只消费 PASS/FAIL、缺口与证据；执行合规和代码收口只产生状态，不重复定义最终 Markdown；`reasoning-summary-structure-rules` 唯一渲染阻断、合法后续和无下一步收口。
- 稳定决策：退役总控 Skill 前必须有 protected semantic mapping、trigger fixtures、active consumer 清零、physical asset owner、baseline tree、rollback locator、生命周期证据和 post-delete PASS；失败候选保持 HOLD，不为目标数量强删。
- 来源：`doc/2-需求/2026-07-22_223221_总控层Skill精简合并与单向路由.md`、`doc/5-tests/2026-07-22_223221/control-plane-streamlining/`。
- 更新时间：2026-07-22。

## 代码位置目录规则 V2

- 稳定决策：`package-structure-rules` 是三类项目的代码位置、查找与引用唯一 Owner；人工目录树、JSON 兼容 YAML Catalog、CLI 和相邻 Skill 必须保持一致。
- 稳定决策：后端项目无关、可独立复制的技术工具、SDK 和服务注册发现统一位于项目根 `utils/<package>/`；`utils/` 仅允许工具包子目录且不得直接存放文件，服务发现只允许 `utils/discovery/polaris/`、`utils/discovery/nacos/`，不得使用 `infrastructure/`、根 `util/`、`utils/graphql/`、`utils/asyncapi/`、`utils/avro/` 或 `utils/api/http/`。需要引用项目其他包但不承载业务流程的高关联工具统一位于独立后端 `common/util/`，直接存放当前语言文件且禁止子目录；源码根 `util/` 为废弃位置。
- 稳定决策：前后端同仓、独立后端和独立前端项目根都直接保存 `AGENTS.md`、`CLAUDE.md`、`PROJECT_CURRENT.md`、`PROJECT_MEMORY.md`、`PROJECT_HISTORY.md`；`PROJECT_STYLE.md` 是条件文件。`AGENTS.md` 与 `CLAUDE.md` 正文必须一致，分别供 Codex 与 Claude Code 读取。Catalog 将六项建模为 `.md` 文件节点，`init` 只创建五个必需文件位置，且仅在显式启用时创建 `PROJECT_STYLE.md`，不负责或覆盖各 Owner 的文件正文；strict 仅只读拒绝双文件正文漂移。
- 稳定决策：`database/connection/` 是关系型数据库、Redis、Mongo 等数据存储服务的连接、连接池与客户端初始化入口；`database/model/` 只允许 `db/`、`redis/`、`mongo/` 子目录。`database/migration/` 是自动迁移生产源码，字段和索引均按 CRUD 分类；手工执行脚本统一进入 `database/scripts/`，按执行文件类型分子目录（独立 SQL 仅在 `database/scripts/sql/ddl/`、`database/scripts/sql/index/` 与 `database/scripts/sql/field/{create,update,delete}/`，Mongo shell 脚本在 `database/scripts/js/`，Redis 执行脚本在 `database/scripts/lua/`），每个脚本叶子目录只直接保存声明扩展名文件，且与迁移源码严格隔离；旧 `database/sql/` 已废弃，命中即禁止。
- 稳定决策：后端项目根不建立 `data/`、`data/business/`、`data/project/` 或 `data/seed/`；Catalog 将根 `data` 作为禁止路径，query、init 与 strict 必须失败关闭。该限制不影响前端 `src/data/`、业务域数据或 `doc/data/`。
- 稳定决策：旧项目不自动迁移。每个独立项目以 `doc/1-架构/3-目录规则收敛清单.yaml` 人工登记 `adopted_paths` 与 `legacy_source_roots`；已采纳 V2 目录可按 Catalog 扩展，遗留快照只允许维护已登记的源码文件和目录。新业务、新模块与可独立演进逻辑必须使用 V2 唯一位置，`check --policy adoption` 全程只读且不得成为绕过禁止路径的通道。
- 稳定决策：独立后端的默认二进制入口固定为根 `main.<ext>`，仅当存在额外 binary 时使用 `cmd/<binary>/main.<ext>`；前后端同仓的后端对应固定为 `backend/main.<ext>` 与 `backend/cmd/<binary>/main.<ext>`。根 `cmd/main.<ext>`、同仓根 `main.<ext>`、同仓根 `cmd/` 和 `backend/cmd/main.<ext>` 都是非法入口；Catalog 以动态 pattern 建模，`init` 显式启用时必须失败关闭且不得创建占位路径。
- 稳定决策：独立后端配置唯一根为 `config/`，前后端同仓的后端配置唯一根为 `backend/config/`；`config/yaml/` 是唯一配置模式（`config/embedded/` 已废弃，strict 下存在即报错，adoption 下登记 `legacy_source_roots` 后才可继续维护）。常见多环境 YAML 使用点中缀命名 `yaml/config.local.yaml`、`yaml/config.test.yaml`、`yaml/config.prod.yaml`（Go 生态主流，兼容 `.yml`），保持外部配置文件形态、不加 `_yaml` 后缀；环境集合可扩展，不要求所有环境齐全。Go 项目由 `config/load.go` 通过 `//go:embed yaml/config.*.yaml` 编译期嵌入并按环境读取（无 build tag）；非 Go 语言（Java/Node/Python）的 `load.<ext>` 从文件系统读取 `yaml/config.<env>.yaml`。`check` 只读，`init` 不生成动态环境配置文件。YAML 允许有意持久化真实密钥、密码、token、私钥原值、默认不依赖环境变量，但 Agent 输出、日志、README、错误和测试报告不得泄露原值。config/ 根允许直接存放 `load.<ext>`（配置加载与解析入口）与 `model.<ext>`（配置结构定义）两个源码文件，条件提交且 `init` 不创建；`config/yaml/` 只存放配置数据。
- 稳定决策：fullstack、backend、frontend 三类项目统一使用项目根 `test/` 作为活动测试代码唯一入口；独立后端使用根 `test/`，不建立 `backend/test/`；前后端同仓也不建立 `backend/test/` 或 `frontend/test/`。Catalog 的测试目录 Owner 为 `test-strategy-rules`，`doc/5-tests/` 只保存测试说明和非可执行证据，不能替代根 `test/`。
- 稳定决策：前后端同仓、独立后端、独立前端三类项目根都必须直接保存并提交 `Dockerfile`。Catalog 以 `project-governance/dockerfile` 的必需文件条目建模，`init` 自动创建空文件位置；`strict` 只读拒绝缺失或被目录占用，`adoption` 保持旧项目渐进采纳，不强制补迁移文件。
- 稳定决策：业务域直连源码根 `<source-root>/<domain>/`，去掉 `business/` 中间层；业务相关逻辑完全通过版本目录 `<v?>`（`v1` 起，命名 `v[0-9]+`）隔离，`router/`、`controller/`、`entity/`、`service/` 下沉到版本目录内（`service/` 必建），`api/`、`base/`、`constant/`、`util/`、`crontask/` 为跨版本通用业务逻辑。域级初始化入口为单文件 `init.<ext>`（`<ext>` 为语言扩展名），全量注册本域所有版本路由并以 `/v1`、`/v2` 前缀区分、多版本并存对外，旧版本不因新版本诞生而下线、也不冻结。目录树用 `<source-root>` 占位符多语言统一（Go=`internal/`、Java=`src/main/java/<包>`、Node=`src/`、Python=`src/<包>`），不单为 Go 定 `internal/` 树。
- 稳定决策：完全移除 `rpc/` 跨业务公开入口；业务域之间禁止直接 import 对方任何目录（无 rpc 例外），跨域共享结构仅走根 `common/` 与 `global/` 非业务运行引用。机器事实源 `placement-catalog.yaml` 的 `router`/`controller` 已改版本级条目（含 `<source-root>`/`<domain>`/`<v?>` 占位符与 `requires_domain`）、`business-rpc` 条目已删除；`micro_business.py` 提供 `scaffold <域>`（建版本骨架 + 单文件 `init.go`）、`check`（校验域间禁止直连）、`check --detect-new`（候选新项目三态判定）。
- 稳定决策：后端根级任务入口有三类，按触发机制区分——`crontask/` 承载时间驱动（cron 表达式/固定间隔）的周期任务；`cachetask/` 承载缓存过期驱动的异步重建任务（Stale-While-Revalidate：缓存 TTL 到期后先返回旧数据、再异步重建新缓存，典型如 60s 级短 TTL 内存缓存）；`async/` 承载消息/队列驱动的 Worker 与消费者。缓存读写技术适配归 `utils/cache/`（Redis/Mongo 客户端封装），`cachetask/` 只承载过期后的业务重建逻辑入口，不重复实现缓存读写；三目录均为条件提交、`cachetask/<task>/` 单任务入口。
- 来源：`package-structure-rules/SKILL.md`、`package-structure-rules/references/project-layout-v2.md`、`package-structure-rules/references/placement-catalog.yaml`。
- 更新时间：2026-08-27。

## 非 Plan Mode 最小计划分级规则

- 稳定决策：计划任何时候都需要，只是确认方式不同——Plan Mode 下先出计划、等用户明确确认后再执行；非 Plan Mode 下先出最小计划、默认直接执行，不必逐条等待确认。
- 稳定决策：`implementation-planning-rules` 新增 `minimum-plan-grading` 条件路由，按改动量把非 Plan Mode 任务分三级：微小（预计 1 个文件、数行以内、无分支）沿用 Karpathy 硬闸门隐性收敛，不强制可见计划；中等（预计 2-5 个文件，或存在分支/方案选择、影响面不完全确定）编码前必须先输出一段对话内可见的最小计划（改动目标、方案、影响范围、验证方式），输出后默认直接执行；重量级（命中原有多文件/多模块/多接口触发条件，或 Plan Mode）沿用完整实施总览/实施周期/Plan Mode 流程。
- 稳定决策：Bug 域的同等分级义务固定交给 `bug-fix-proposal-rules` 及其 `references/confirm-before-coding.md`，`minimum-plan-grading` 不重复接管，避免同一次修复被两套分级规则同时套用。
- 稳定决策：中等分级的最小计划默认不必写入 `artifact-storage-rules` 的正式实施文档；若执行中发现改动量超出预期（触达文件明显超过 5 个或触及公共模块），必须停下重新评估分级并按需升级为重量级。
- 来源：对话确认、`implementation-planning-rules/SKILL.md`、`implementation-planning-rules/references/minimum-plan-grading.md`、`bug-fix-proposal-rules/references/confirm-before-coding.md`。
- 更新时间：2026-07-29。

## 三类项目 doc 目录收敛规则

- 稳定决策：fullstack、backend、frontend 的活动研发目录统一为 `doc/1-架构/`、`doc/2-需求/`、`doc/3-实施/`、`doc/4-bugs/`、`doc/5-tests/`、`doc/6-review/`；条件图片与截图统一放 `doc/data/images/`。
- 稳定决策：`doc/6-审查/`、`doc/7-验收/` 只作为历史只读归档，不再进入人工活动骨架、Catalog skeleton 或新初始化结果。
- 稳定决策：独立前端不建立根 `data/business/<domain>/`、`data/project/` 原始静态数据树；源码域 `src/modules/<domain>/data/` 和 `doc/data/images/` 不受影响。
- 稳定决策：后端独立项目的 `doc/` 必须展开完整活动子树，注释使用“后端”；同仓目录使用工作区语义；`6-review` 说明为“测试后的风格回归记录”。
- 来源：`package-structure-rules/references/project-layout-v2.md`、`package-structure-rules/references/placement-catalog.yaml`、`doc/2-需求/2026-07-28_014412_代码位置目录规则V2.md`、`doc/3-实施/2026-08-02_192314_REQ-PSR-DOC-LAYOUT-001_实施周期16_三类项目doc目录收敛.md`。
- 更新时间：2026-08-02。

## 总结知识引用清单规则

- 稳定决策：`reasoning-summary-structure-rules` 的最终总结新增条件小节 `## 📚 知识引用`，用「本轮引用」三列表与「本轮沉淀」四列表承载知识库事实；原先分散在「方案与根因」和「结果与结论」的两处单行摘要口径已作废。
- 稳定决策：无真实阻断时末尾顺序按引用台账分流——台账非空由知识引用收尾、改动点紧邻其前；台账为空由改动点收尾；真实阻断时两者都在阻断收口之前。
- 稳定决策：`knowledge-flow` 每次读取、创建、追加笔记成功后必须立即登记引用台账（笔记名、所在目录、本轮用途、`status`、操作、回读结果六字段）；台账是会话内事实，不写入知识库、不落盘项目文件。
- 稳定决策：只有真实读取成功的笔记可进引用表，检索命中未读取的一律不得入表；引用小节每一行都必须能回指一次成功返回的文件读/写调用。
- 稳定决策：笔记名一律取自读写笔记时所用相对路径的文件名部分。（原附带的「禁止使用 CLI 回显文本，因官方 CLI 回显中文乱码」理由已于 2026-08-12 随 CLI 链路废除而失效）
- 事实更新：知识库根目录已迁至 `D:\谷歌云盘\知识库\`，读写均通过标准文件工具直接完成，不再依赖任何 CLI 前置注册。
- 来源：`reasoning-summary-structure-rules/SKILL.md`、`references/summary-structure-template.md`、`references/conditional-sections-rules.md`、`knowledge-flow/references/capture-retrieve-distill.md`、`doc/2-需求/2026-08-04_总结知识引用清单_Obsidian引用可视化.md`、`doc/3-实施/2026-08-04_总结知识引用清单_实施周期21_Obsidian引用可视化.md`。
- 更新时间：2026-08-04。

## 总结异步任务分流规则（2026-08-21）

- 稳定决策：`reasoning-summary-structure-rules` 最终总结新增条件小节 `## 🔄 后台异步任务`——本轮启动了后台异步任务（`run_in_background` 轮询 / CI 等待 / 长任务后台执行）时必选，位于「结果与结论」之后、「后续内容」之前；逐项写明任务标识、任务类型、轮询节奏、预计完成信号、结果回流渠道（系统通知 / 下一会话 / 用户指令）与用户等待语义。
- 稳定决策：该小节是「同步已完成 + 异步在跑」的收口信号——不是"任务未完成"、不是 `blocked`/`manual_handoff`、不触发「后续内容」、不让用户误判会话被阻断；`Stop` hook 校验认该小节为异步收口信号，缺失视为未收口。
- 稳定决策：WorkBuddy hooks 可提高本 skill 触发准确率——`UserPromptSubmit` 注入 `additionalContext` 软提醒 + `Stop` 事件 exit code 2 硬校验（stderr 注入下一条消息强制补总结）；hook 配置在 `~/.workbuddy/settings.json` 或项目 `.workbuddy/settings.json` 的 `hooks` 字段，配置与脚本见 `reasoning-summary-structure-rules/references/hook-integration.md`；hook 支持需真实任务实测（文档列了不等于桌面版真的触发）。
- 稳定决策（2026-08-21 追加）：异步任务（轮询 / CI 等待 / 异步下载 / 异步发布 / 异步构建 / 异步子会话）必须**执行期登记宿主任务列表**——启动时 `TaskCreate`（条目描述三段式：做什么 + 任务标识 + 何时查看），启动/等待/回收三阶段用 `TaskUpdate` 推进（pending → in_progress → completed），禁止裸 `run_in_background` 当唯一进度可见手段；执行期契约在 `autonomous-execution-rules`，收口期渲染与登记校验在 `reasoning-summary-structure-rules`（「🔄 后台异步任务」小节增加「宿主任务列表」映射字段）。「任务列表 UI 常驻未完成会话底部」属宿主产品诉求，不在规则仓库范围。
- 来源：`reasoning-summary-structure-rules/SKILL.md`、`references/summary-structure-template.md`、`references/conditional-sections-rules.md`、`references/hook-integration.md`、`autonomous-execution-rules/SKILL.md`、WorkBuddy 官方 hook 文档（`workbuddy.cn/docs/ide/Features/Hooks`）。
- 更新时间：2026-08-21。

## 知识库可迭代更新规则

- 稳定决策：知识库从只增量补充改为可迭代更新。写入前必须显式判定 `补充` / `矛盾未裁决` / `取代` 三态之一；判为取代必须在同一轮内处置旧笔记，只写新笔记不处置旧笔记是禁止行为。
- 稳定决策：取代按旧笔记剩余价值分三档——仍有历史参考价值改 `status: superseded` 并标 `superseded_by`；完全失效且反向链接为 0 改 `status: archived` 后移动到 `90-Archive/`；内容错误或有害 `delete` 进回收站并在新笔记记录旧错误说法。
- 稳定决策：三档处置前必须先用 Grep 扫 `[[笔记名]]` 统计反向链接，引用数不为 0 时不得移动或删除，只能降级为标记取代；接替关系必须双向写入 `supersedes` 与 `superseded_by`，只写一侧视为治理未闭环。
- 稳定决策：`superseded` 与 `archived` 状态的笔记不得作为当前事实，检索命中时顺着 `superseded_by` 跳到接替笔记；执行失败案例笔记不适用三档处置，仍只能追加状态事件，禁止对该目录做移动与删除。
- 稳定决策：三档处置由 agent 自动执行，但每次改属性、移动、删除都必须在最终总结的知识引用小节如实登记。
- 已取代（2026-08-12）：原 bridge 16 命令白名单（`property-read`/`properties`/`property-set`/`move`/`delete`/`backlinks`/`files`/`orphans` 等）随 CLI 链路整体废除，改由标准文件工具完成；frontmatter 属性用 YAML 解析读写，反向链接与孤儿笔记用 Grep 扫 `[[wikilink]]` 统计。
- 已取代（2026-08-12）：CLI stdout 编码归因与 bridge `reconfigure(encoding="utf-8")` 修复随 bridge 脚本删除而失效；当前所有笔记读写显式指定 UTF-8。
- 已取代（2026-08-12）：`properties` 严格模式探测口径随 CLI 废除失效；文件存在性直接由文件系统判断。
- 关键事实：读取笔记元信息直接解析文件头部的 YAML frontmatter；部分笔记没有 frontmatter，取不到状态字段时按无状态处理。
- 来源：`knowledge-flow/references/conflict-staleness.md`、`references/capture-retrieve-distill.md`、`references/note-schema.md`、`scripts/audit_vault_knowledge.py`、`doc/2-需求/2026-08-05_知识库可迭代更新_冲突取代与废弃治理.md`。
- 更新时间：2026-08-05。

## PROJECT_MEMORY / PROJECT_STYLE 到知识库的选择性沉淀规则

- 稳定决策：`PROJECT_MEMORY.md`/`PROJECT_STYLE.md` 与知识库的"本地上下文 vs 跨项目知识库"边界不变；新增的是一条"单条可复用事实"选择性通道，不是整份文件同步或镜像备份，核心标准定义在 `knowledge-flow/references/project-memory-sync.md`。
- 稳定决策：判断是否跨项目可复用采用两层分工——初判层由 `project-memory-rules`/`project-style-rules` 在写入条目的同一步骤完成，标准是"通用性删除测试"（去掉项目名、具体表名/字段名、具体服务名等专属信息后条目是否仍然成立）叠加类型白名单、适用范围显式标注为通用、状态为启用四条，全部满足才追加可选字段 `bridge_candidate: true` / `跨项目候选: 是`；这一步不写入知识库，不产生知识库副作用。
- 稳定决策：复核与落地层由 `knowledge-flow` 在既有"总结阶段捕获流程"（会话总结、阶段收口或最终回复前）完成，把候选条目作为新增信息来源纳入既有扫描，套用既有排除规则二次核验后，选择性沉淀到 `20-Knowledge/project-rules/`（来自 project-memory-rules）或 `20-Knowledge/code-style/`（来自 project-style-rules）；不新增知识库四态之外的第五种状态，只是"沉淀"分支下的新增信息来源。
- 稳定决策：去重固定为"先检索、命中则追加、未命中才新建"，知识库侧笔记只保留脱敏后的通用表述与 `source_refs` 来源引用，不摘录项目原文；`skill-hit-check-rules` 的命中清单同步补充识别信号，避免候选标记被漏判为"不适用"。
- 来源：`knowledge-flow/references/project-memory-sync.md`、`knowledge-flow/SKILL.md`、`knowledge-flow/references/capture-retrieve-distill.md`、`knowledge-flow/references/knowledge-layout.md`、`project-memory-rules/SKILL.md`、`project-memory-rules/references/project-knowledge-source-contract.md`、`project-style-rules/SKILL.md`、`skill-hit-check-rules/references/hit-checklist.md`、用户在 Plan Mode 确认的方案（`C:\Users\luode\.claude\plans\project-memory-md-project-style-md-obsi-fancy-wand.md`）。
- 更新时间：2026-08-05。

## 知识库承载体迁移与路径前缀规则

- 稳定决策：知识库承载体从 Obsidian vault `D:\obsidian_data` 迁移到 Google Drive 同步目录 `D:\谷歌云盘\知识库\`，多端同步交给 Google Drive 客户端。选择这条路线的原因是 Obsidian 的同步不如谷歌云硬盘方便，且知识库退化成普通 Markdown 文件夹后不再依赖 Obsidian 应用运行。
- 稳定决策：CLI 桥接层整体废除。`obsidian_cli_bridge.py`、`obsidian_cli_windows.ps1`、`distill_vault.py` 已删除，所有笔记的检索、读取、创建、追加、移动、删除统一改用标准文件工具，写入后回读校验取代原 `verified=true` 判据。原「不得用 `rg`/`Get-Content`/`Set-Content` 冒充 vault 操作」这条禁令方向已完全反转——文件工具现在是唯一正确通道。
- 稳定决策：笔记路径基准是**相对知识库根的裸相对路径**（如 `20-Knowledge/topic/note.md`），**禁止再加 `知识库/` 前缀**。根目录本身已经是 `知识库`，前缀叠加会生成嵌套目录 `D:\谷歌云盘\知识库\知识库\`。这正是 2026-08-12 发现嵌套目录的根因，且该错误约定在 Obsidian 时代就已存在（原 `D:\obsidian_data\知识库\知识库\` 同样是它的产物）。知识库现有 `INDEX.md` 的 wikilink 一直用的就是裸相对路径，是正确写法的既有证据。
- 稳定决策：`obsidian-knowledge-flow` skill 更名 `knowledge-flow`；每轮首条中间进度的状态字段由 `Obsidian:<检索/沉淀/不适用/阻断>` 改为 `知识库:<检索/沉淀/不适用/阻断>`。四态语义保留，只有 `阻断` 判据改为「知识库目录不存在或不可读 / 路径不合法 / 写入后回读不一致」。
- 关键事实：知识库内容治理同步完成——嵌套层 1 篇实质笔记合并回 `20-Knowledge/研发流程/`，4 篇已作废 Obsidian CLI 笔记与 Obsidian 默认欢迎页删除，2 处散落文件归位到标准布局，`INDEX.md` 死链与过期措辞清理，笔记总数 65→59，全库 wikilink 无新增死链。blog-data 系列笔记里的 "Obsidian vault" 是源 vault 的真实来源事实，按历史事实保留不改。
- 来源：`knowledge-flow/SKILL.md`、`knowledge-flow/references/file-operations.md`、`knowledge-flow/references/knowledge-layout.md`、`AGENTS.md`、`CLAUDE.md`、`context-recovery-rules/scripts/bootstrap_agents.sh`、用户在 Plan Mode 确认的方案（`C:\Users\luode\.claude\plans\d-mellow-hippo.md`）。
- 更新时间：2026-08-12。

## 知识库检索准召与主题收敛规则

- 跨项目判据见知识库笔记 `知识库检索失效的三种模式与修法`（手写导航覆盖率必然衰减、分类目录自由生长会散落同一主题、纯结构化索引会漏检正文、索引新鲜度要自动处理）。
- 本仓库落地：检索第一跳固定为 `python knowledge-flow/scripts/knowledge_index.py query --keyword "<词>"`，覆盖全库，按六类结构化字段加正文匹配并返回命中原因；索引 `_index.json` 是可再生成物，过期自动重建。
- 本仓库落地：`20-Knowledge` 固定 7 个中文主题（项目、代码规则、工程实践、研发流程、AI协作、数据清洗、开发环境）加 3 个契约固定落点（`execution-failure-cases`、`project-rules`、`code-style`，保留英文因被其它 skill 硬编码引用）；有常驻断言锁定「实际目录 ⊆ 声明清单」。
- 本仓库落地：笔记路径一律为相对知识库根的裸相对路径，禁止带 `知识库/` 前缀（会生成嵌套目录）。
- 更新时间：2026-08-12（判据已迁知识库，此处只留本仓库落地口径）。


## 知识库沉淀触发与契约强制规则

- 跨项目判据见知识库笔记 `知识库沉淀失效的三种模式与修法`（触发条件不能是主观描述、契约要有机器强制、下游机制零使用往往是上游输入不可信、BOM 会让头部判定静默失效等）。
- 本仓库落地：沉淀触发硬信号清单在 `knowledge-flow/references/capture-retrieve-distill.md` 的「沉淀触发硬信号」；判断依据写进状态字段（如 `知识库:沉淀（命中信号2 推翻旧归因）`），只要求写明依据、不要求每轮必须有沉淀。
- 本仓库落地：头部合规入口是 `python knowledge-flow/scripts/knowledge_index.py check`，校验活动区必填六字段与状态枚举，不合规返回非零退出码可当闸门；`90-Archive/` 按只读归档豁免。
- 本仓库落地：冲突候选归组条件为「(同主题 且 共享标签 ≥2) 或 标题相似度 ≥ 0.72」，下限常量 `MIN_SHARED_TAGS` 有断言锁定；标题相似度是跨主题例外通道。
- 更新时间：2026-08-12（判据已迁知识库，此处只留本仓库落地口径）。


## 代码风格规则生效层级规则

- 跨项目判据见知识库笔记 `规则与共用定义的落点决定其有效性`（规则要落在动作前会被读取的入口才生效，四层落点效力分层）。
- 本仓库落地：写码前强制加载入口是 `code-style-consistency-rules/references/user-style-feedback-library.md` 的 active 条目；Go 改动默认补读 `references/go-coding-rules.md`。只写 `SKILL.md` 正文或 `consistency-examples.md` 等于放在事后复盘层，拦不住生成。
- 本仓库分流：跨项目通用偏好走 `style-feedback-workflow.md` 的 candidate→用户确认→active 流程写入全局反例库；项目专属一次性约定才走 `PROJECT_STYLE.md`（边界依据 `project-style-rules/SKILL.md:51`）。
- 更新时间：2026-08-12（判据已迁知识库，此处只留本仓库落地口径）。


## 代码质量九维治理规则（吸收优先）

- 稳定口径：AI 辅助开发的代码质量治理按九维落点分流（架构与模块划分 / 编写习惯与风格 / 注释与定义位置与命名 / 引用方式与包别名 / 静态风格命名与位置 / 函数签名 / 结构体按作用分层 / 纯转换工具函数落点 / 工具函数索引文档规范）；发现内容缺口时**吸收优先**——补 reference，不新建 skill（依 `编码skill.md` 第十八条）；节奏为「先补规则内容，后处理 6-review 编排时机」。
- 本仓库落地：函数签名 `code-quality-rules/references/function-signature-rules.md`（参数顺序 ctx → 必填 → 可选；数量语义优先，同源 ≥3 建议收、含可选/扩展字段必收；命名 `XxxParams` / `XxxOptions`）；定义位置 `code-quality-rules/references/definition-placement-rules.md`（局部变量函数开头集中、包级变量与常量顶部集中、函数追加末尾，与 `code-style-consistency-rules` 的「声明形式」约定配套）；结构体角色分层 `package-structure-rules/references/struct-role-layering.md`（角色谱系与落点表 + 引用面从小到大判定 + 按语言生态 Go/Java/TS/Python 差异）。
- 本仓库落地：**公共工具索引唯一合法落点 = `doc/1-架构/3-模块职责.md` 的「公共工具索引」小节**（契约 `common-util-rules/references/util-index-doc-contract.md`）。`utils/<pkg>/README.md` 不可用（Catalog `allowed_extensions` 只含源码扩展名）；`doc/` 新建子目录不可用（doc 子目录与 `doc/1-架构/` 序号由 Catalog 与 `artifact-storage-rules` 固定）。纯转换函数（确定性 / 无副作用 / 无 IO / 无项目依赖）必进根 `utils/<pkg>/`，一旦需项目依赖降级 `common/util/<函数>.<ext>`。
- 更新时间：2026-09-11。
