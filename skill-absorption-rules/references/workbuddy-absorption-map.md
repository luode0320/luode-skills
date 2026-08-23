# 吸收裁决表（workbuddy-absorption-map）

> 归属 owner：`skill-absorption-rules`。登记每次外部 skill 吸收的三态裁决结果，来源可回指。新吸收追加行，不覆盖旧记录。
>
> **防臃肿登记要求（2026-08-19 起）**：每次吸收除记录「合并/保留/拒绝」外，必须记录本次「整理去重」动作（合并了哪些重复段落、消除了哪些冗余引用、删除了哪些过时规则）与「净增体积变化」；无整理动作的写 `N/A + 理由`。只增不减的登记视为不合格。
>
> **同域扫描登记要求（2026-08-20 起）**：每次吸收必须在登记中新增「同域扫描结论」行——扫描范围（本次吸收触达的同域 skill 集合）、发现 X 处冗余（重复段落 / 门控层叠 / 散落产物）、清理 Y 处、PASS/FAIL；「整理去重」动作描述必须包含同域清理位置（哪个 skill、哪个段落、收敛到哪个权威）。缺同域扫描结论的吸收登记视为未完成。
>
> **内部更新通道登记（2026-08-20 起）**：本表同时登记「内部 skill 更新通道」的裁决式调整——来源列写"内部调整：<目标 skill>，<调整诉求>"，其余列（裁决 / 落点 / 整理去重 / 同域扫描结论 / 净增体积）要求与外部吸收完全一致，无外部源可删。

## 2026-08-23：browser-use API + guide 合并吸收（Cloud REST 操作通道）

- **来源**：skillhub 安装源 `browser-use-api__skillhub`（REST v2 API 操作指南，含 `scripts/browser-use.sh`）+ `browser-use-guide__skillhub`（browser-use 完整指南，含开源库/CLI/OpenClaw/云端对比）；两源均同时存在于仓库根与用户级（junction 同一物理目录）。
- **形态**：外部吸收通道（本地安装源吸收模式：读取原文 → 裁决 → 落盘 → 删除源）；吸收触达同域 skill `browser-use-cloud-rules`，按用户决策将两源合并进该 skill（不新建同类目录）。
- **拆解原子规则数**：22 条（来源 A 11 + 来源 B 11）。
- **裁决**：
  - 来源 A（REST API）：v2 端点表、curl 示例、任务状态机、`browser-use.sh` 轮询脚本、credits 查询、定价 → **合并**（本地仅 MCP 路径文档，无 REST 路径）；"When to Use/When NOT" → **保留本地**（`browser-use-cloud-rules` 路由边界 + `mcp-installation-rules/tool-priority.md` 矩阵更强）。
  - 来源 B（指南）：云端 vs 开源对比、模型定价表、应用场景示例、故障排除（API Key/被检测→云端）→ **合并**；密钥配置 → **合并但改写**（按用户新决策统一存 `~/.browser-use/.env`，废弃原"项目代码/配置默认"旧口径）；本地开源库安装、Python Agent 本地代码、CLI 工具、OpenClaw 集成、自定义 Tools、Chrome profile 复用 → **拒绝**（场景不匹配——用户定位是"项目程序操作公网 https 浏览器"；宿主不匹配——OpenClaw 专属形态）。
- **落盘改动**：
  - `browser-use-cloud-rules/references/api-operations.md`（新建）：REST v2 端点/状态机/curl/Python 集成/模型定价/边界，凭据单一权威指向 `~/.browser-use/.env`。
  - `browser-use-cloud-rules/scripts/browser-use.sh`（新建）：从 `~/.browser-use/.env` 读 key + `--check/--balance` 自检（替代源脚本的纯环境变量模式）。
  - `browser-use-cloud-rules/scripts/.env.example`（新建）：密钥模板。
  - `browser-use-cloud-rules/SKILL.md`（修改）：description 触发扩展（项目程序操作公网浏览器）、凭据策略改 `~/.browser-use/.env` 单一权威、新增「REST API 操作通道」「环境自检」小节、References 补 api-operations.md。
  - `browser-use-cloud-rules/references/routing-and-safety.md`（修改）：MCP 配置凭据来源补"值来自 `~/.browser-use/.env`"口径。
- **整理去重**：browser-use 凭据来源策略收敛为单一权威——`browser-use-cloud-rules` 旧口径"项目代码/配置默认"更新为 `~/.browser-use/.env`；同域 `authenticated-url-routing-rules/SKILL.md` 两处旧口径（L30 配置位置、L115 凭据来源）同步收敛为引用；两源合并后拒绝约 60% 开源库/OpenClaw 内容，未产生整段重复。
- **同域扫描结论**：范围 = browser-use-cloud-rules、authenticated-url-routing-rules、mcp-installation-rules（tool-priority）、browser-session-automation-rules、browser-advanced-testing-rules、README.md、编码skill.md；发现 = 2 处门控层叠（authenticated-url-routing L30/L115 旧凭据口径与新版冲突）+ 1 处引用链缺口（routing-and-safety MCP 凭据来源未指向 .env）；清理 3 处；**PASS**（其余引用为中性表述，兼容）。
- **环境依赖登记**：1 项——`路径: ~/.browser-use/.env`（junction → `D:\谷歌云盘\browser-use`，Google Drive 同步），已登记至 `workbuddy-env-manifest.md` 第 9 项；自检能力 = `scripts/browser-use.sh --check`（SKILL.md「环境自检」小节三行命令）。
- **净增体积**：+约 12KB（api-operations.md ~6KB + browser-use.sh ~4KB + .env.example ~0.2KB + SKILL.md/routing 增量 ~2KB）；两源合计 ~11KB，合并后净增约 +1KB 等价（含拒绝内容约 6.5KB 未入）。
- **棘轮验证**：`quick_validate.py` PASS；`bash -n browser-use.sh` 语法 PASS；`--check` 真实环境自检 PASS（正确报 key 缺失）；Python 集成密钥读取三场景（.env 读取 / env 覆盖 / 双缺失抛错）全部 PASS（隔离 HOME + 哨兵 key）；UTF-8 与引用链复核 PASS（api-operations → SKILL.md 2 处、browser-use.sh → SKILL.md 3 处、.env.example → SKILL.md 环境自检 1 处、manifest 第 9 项 → SKILL.md 权威）。
- **源清理**：吸收完成后删除本地安装源 `browser-use-api__skillhub` 与 `browser-use-guide__skillhub`（仓库根 + 用户级 junction 双路径各删一份，共 4 目录）。

## 2026-08-23：内部更新——环境依赖吸收（跨机器自愈）

- **来源**：内部调整：`skill-absorption-rules`（吸收方法论）+ WorkBuddy 平台配置事实（官方文档 env-vars + 现网部署），调整诉求 = "吸收 skill 时不能只吸收规则正文，还要吸收环境配置 / hook / 依赖；换电脑或新环境缺失时自动检测并自动补齐"。
- **形态**：内部更新通道（无外部源可删；平台配置事实来自官方文档与现网部署，已入知识库）。
- **裁决**：
  - 环境依赖成为吸收一等公民 → 合并进 `skill-absorption-rules/SKILL.md` 默认流程第 4 步（环境依赖登记 + manifest 写入）+ 收口说明（依赖登记数量 / 自检能力数量 / 净增体积）+ 通过/驳回标准（环境类条目未登记依赖驳回、有依赖无自检/自动配置能力驳回）+ references 读取规则 3 条。
  - 单一权威 manifest → 新建 `references/workbuddy-env-manifest.md`（8 项 WorkBuddy 平台配置，每项含检测方式 / 配置方法 / 验证方式 / 来源证据）。
  - 环境依赖吸收指引 → 新建 `references/env-dependency-absorption.md`（五类依赖：环境变量 / 宿主配置 / hook·插件·MCP / 依赖安装 / 路径引用；裁决表加「环境依赖」列，无依赖写 `N/A + 理由`；复杂依赖须提供 `--check/--dry-run/--fix` 自检）。
  - 跨机器自检自愈 → 新建 `scripts/env-bootstrap-check.py`（三模式，merge / 追加 / 备份 / 幂等策略，Windows 用 `setx` 写 `HKCU\Environment`）。
  - hook 资产副本 → 新增 `assets/hooks/summary-check.py` + `assets/hooks/ralph-stop.py`（md5 与用户级现网脚本一致，仓库即备份源）。
- **落盘改动**：`skill-absorption-rules/SKILL.md` 4 处升级（设计内核 / 默认流程第 4 步 / 收口说明 / 通过驳回标准）；新增 2 reference + 1 脚本 + 2 hook 资产副本，共 5 文件。
- **整理去重**：环境配置表述收敛到 `workbuddy-env-manifest.md` 单一权威——此前平台配置散落在工作日志与知识库，仓库侧无权威清单，本次收敛为"同一环境依赖只允许在一个 manifest 定义、其他 skill 只引用"，消除配置漂移源；hook 资产以现网 md5 为准副本化，消除"仓库与现网两处漂移"。
- **同域扫描结论**：范围 = 吸收域（skill-absorption-rules）+ 环境依赖触达域（reasoning-summary-structure / context-compression / autonomous-execution / task-plan-rehydration，均与 SUMMARY-GATE-PMW-002 / 平台压缩配置相关）；发现 = 0 处重复段落、0 处门控层叠、0 处散落产物（manifest 为配置事实权威 vs 各 skill 为使用方引用，非冗余）；清理 0 处；**PASS**。
- **净增体积**：+42035 bytes（manifest 5543 + 指引 4341 + 自愈脚本 14376 + hook 资产副本 17775）；hook 副本为现网脚本资产化，非规则正文膨胀。
- **棘轮验证**：`env-bootstrap-check.py` 语法 PASS、六场景单测 6/6 PASS、真实环境 `--check` 8/8 完备、UTF-8 7 文件 PASS、引用链 12 本 skill + 3 跨 skill 全部可达、同域扫描 0 扩散、登记文件与知识库收口补齐。

## 2026-08-22：调试（awesome-ai-agent-skills）

- **来源**：marketplace 安装源 `debugging-skillhub__skillhub`（仓库根 + 用户级 junction 同一物理目录，git 未跟踪，version 1.0.0，作者 awesome-ai-agent-skills contributors）。
- **形态**：外部吸收通道（本地安装源吸收模式：读取原文 → 裁决 → 落盘 → 删除源）。
- **拆解原子规则数**：20 条。

| # | 外部精华 | 本地现状 | 裁决 | 落点 / 理由 |
|---|---------|---------|------|------------|
| 1 | 复现：确认可观察可重复 + 收集错误/堆栈/日志 + 最小输入 + 间歇记录频率环境 | intake 收集 + reproduction-template 步骤 + feedback-loop 复现三确认 + stability-checks 频率条件 | 保留本地 | 全覆盖 |
| 2 | 隔离：堆栈/错误/代码结构缩小范围 + 从失败点向后追踪数据流 | static-analysis-path「顺着调用链往内收窄」「对照关键状态/分支/数据转换」 | 保留本地 | 数据流收窄已覆盖 |
| 3 | 隔离战术：stub/bypass 排除无关路径 + 禁用一半系统二分定位 | static-analysis-path 无此战术；feedback-loop 的二分是自动化回路语境（不同） | 合并 | 补 static-analysis-path.md |
| 4 | 常见根因类别清单（输入假设/并发状态/缓存过期/运算符优先级/缺失 await/依赖版本） | root-cause-evidence 有证据标准，无「可能是什么」类别清单 | 合并 | `bug-root-cause-rules/references/root-cause-catalog.md`（新建） |
| 5 | 区分根因与症状（NPE 是症状，根因可能在三跳前） | root-cause-evidence「常见误判」已有「只看堆栈忽略前置状态」 | 保留本地 | 同义且更强 |
| 6 | 修复：最小改动 + 共享接口追踪调用者 + 防御性修复 | fix-proposal「根因修复优先 + 最小改动协调 + 反打补丁式修复」 | 保留本地 | 本地更强 |
| 7 | 验证：重跑复现 + 回归测试 + 既有测试 + 关键路径监控 | validation 闭环 + correct-seam（失败测试+重跑原始）+ post-mortem | 保留本地 | 本地更强 |
| 8 | 堆栈阅读纪律：从下往上、根因在深层应用帧、框架帧可跳过 | static-analysis-path 有「看报错位置」，无阅读顺序纪律 | 合并 | 补 static-analysis-path.md |
| 9 | 一次只改一件事 | runtime-observation-methods「诊断手段服务于当前假设」 | 保留本地 | 与 diagnose #10 同义，已裁决 |
| 10 | 战略日志：入口/出口插日志，修复后移除 | debug-log-placement「决策点/状态点/边界/异常处」⊇ 入口出口 | 保留本地 | 本地更强 |
| 11 | 先查最近变更：git bisect / review diff 常是最快路径 | feedback-loop 有二分 harness（自动化回路），无「先查最近提交」快速纪律 | 合并 | 补 static-analysis-path.md |
| 12 | 修复前先复现，不可复现不修 | feedback-loop 复现三确认 + reproduction 暂停条件 | 保留本地 | 全覆盖 |
| 13 | 每个修复产出失败→通过回归测试 | correct-seam「修复前失败测试 + 重跑原始场景」 | 保留本地 | 本地更强（含正确接缝检查） |
| 14 | Heisenbug：调试工具附加改变时序掩盖竞态 → 日志/追踪 + race detector | runtime-observation-methods 无 Heisenbug 专项 | 合并 | 补 runtime-observation-methods.md |
| 15 | 环境特定 bug：生产才出现 → 问环境细节 + 匹配约束复现（Docker 内存限制） | stability-checks 有「网络波动」、feedback-loop 有「索要环境」，无匹配复现战术 | 合并 | 补 stability-checks.md |
| 16 | 第三方库 bug：升级/workaround/pin + 查 changelog/issue tracker | 本地无 | 合并 | 并入 root-cause-catalog.md |
| 17 | 编译器/runtime bug：穷尽应用层解释再测不同 runtime | 本地无 | 合并 | 并入 root-cause-catalog.md |
| 18 | 损坏状态：数据与代码一起查 + 要样本数据 | 本地无 | 合并 | 并入 root-cause-catalog.md |
| 19 | 跨语言工具参考表（stack trace/debugger/profiling/memory/concurrency） | runtime-observation-methods 有手段分类，无工具名清单 | 合并 | 补 runtime-observation-methods.md |
| 20 | 示例 2 个（race condition / memory leak 教学代码） | 精华已提取为根因类别条目（并发共享可变状态 / 无界内存容器） | 拒绝 | 一次性教学示例形态 |

- **落盘改动**：
  - 新增 `bug-root-cause-rules/references/root-cause-catalog.md`，并在 SKILL.md 默认执行流程第 3 步 + references 读取规则登记。
  - 补 `bug-root-cause-rules/references/static-analysis-path.md`（堆栈阅读纪律 + 先查最近变更 + 二分隔离/stub 排除三节）。
  - 补 `bug-intake-rules/references/runtime-diagnostics-bug-runtime-debug-rules-runtime-observation-methods.md`（Heisenbug 节 + 跨语言工具参考表）。
  - 补 `bug-reproduction-rules/references/stability-checks.md`（环境特定 Bug 匹配复现节），并同步 SKILL.md 两处引用描述。
- **整理去重**：修复 `bug-reproduction-rules/SKILL.md` 默认执行流程编号重复（两个「3.」→ 1-6 顺排，上轮 feedback-loop 插入遗留的格式瑕疵）；无同义重复段落可合并（本地五件套为引用式结构，本轮为补缺增量）。
- **同域扫描结论**：范围 = Bug 域 5 skill（intake/reproduction/root-cause/fix-proposal/validation）+ 测试域 3 skill（strategy/program/regression）；发现 = 0 处重复段落、0 处门控层叠、0 处散落产物（root-cause-catalog 为假设生成候选池 vs hypothesis-ranking 为排序纪律，阶段互补；stability-checks 环境匹配 vs feedback-loop 索要环境，分属复现判定与回路构建两阶段；static-analysis-path 禁用一半系统 vs feedback-loop 二分 harness，静态排除战术 vs 自动化回路工具）；清理 1 处（SKILL.md 编号格式）；**PASS**。
- **净增体积**：+5005 bytes（1 个新 reference 2549 + 3 处补丁 992/479/985），引用式接入无膨胀。
- **棘轮验证**：3 个 skill `quick_validate.py` 全部 PASS；4 个落盘文件 UTF-8 无乱码；引用链可达（root-cause-catalog→SKILL.md 2 处、stability-checks→bug-reproduction SKILL.md 2 处、runtime-observation-methods→runtime-diagnostics.md 路由、static-analysis-path→SKILL.md 默认第 1 步）。
- **源清理**：吸收完成后删除本地安装源 `debugging-skillhub__skillhub`（仓库根目录，junction 双路径同一物理目录）。

## 2026-08-22：diagnose（mattpocock/skills）

- **来源**：marketplace 安装源 `diagnose`（仓库根 + 用户级 junction 同一物理目录，`_skillhub_meta.json` skillId `skill_2057443344813191168`，version 1.0.0，homepage `https://github.com/mattpocock/skills`）。
- **形态**：外部吸收通道（本地安装源吸收模式：读取原文 → 裁决 → 落盘 → 删除源）。
- **拆解原子规则数**：18 条。

| # | 外部精华 | 本地现状 | 裁决 | 落点 / 理由 |
|---|---------|---------|------|------------|
| 1 | 反馈回路是调试核心：先构建快速确定性 agent 可运行 pass/fail 信号，再谈定位 | reproduction 有最小复现路径、runtime-diagnostics 有受控观察，但无「反馈回路优先」元方法论 | 合并 | `bug-reproduction-rules/references/feedback-loop.md`（新建） |
| 2 | 构建回路 10 种方式清单（failing test/curl/CLI fixture/headless/replay trace/harness/fuzz/bisection/differential/HITL） | 本地无系统化回路构建清单 | 合并 | 并入 feedback-loop.md |
| 3 | 迭代回路三问：更快/信号更尖锐/更确定性 | stability-checks 有稳定性判断，无「回路本身可优化」概念 | 合并 | 并入 feedback-loop.md |
| 4 | 非确定性 Bug：目标是提高复现率（loop 100×、并行、加压力、窄化时序窗口） | stability-checks 有「是否每次出现/特定条件」，无提高复现率战术 | 合并 | 并入 feedback-loop.md |
| 5 | 无法构建回路：停下明说、列尝试、索要环境访问/捕获产物/临时插桩权限 | reproduction 有暂停条件，缺「索要三样东西」清单 | 合并 | 并入 feedback-loop.md |
| 6 | 复现三确认：用户描述的现象/跨多次可复现/捕获确切症状 | reproduction 有「记录复现结果、稳定性、失败差异」，缺「确认是用户描述的现象」 | 合并 | 并入 feedback-loop.md |
| 7 | 测试前生成 3-5 个排序假设；单假设锚定 | root-cause 有「多个假设都成立」暂停条件，缺排序纪律 | 合并 | `bug-root-cause-rules/references/hypothesis-ranking.md`（新建） |
| 8 | 假设必须可证伪：陈述预测 If X then changing Y | root-cause-evidence 有「能解释为什么」，缺可证伪预测格式 | 合并 | 并入 hypothesis-ranking.md |
| 9 | 排序列表给用户看（领域知识可重排），不阻塞 | fix-proposal 有「是否需用户确认」（修复阶段），假设阶段给用户看是新增量 | 合并 | 并入 hypothesis-ranking.md |
| 10 | 探针映射 Phase 3 预测 + 一次只改一个变量 | runtime-observation-methods 已有「诊断手段服务于当前假设」「不做全链路无差别打印」 | 保留本地 | 本地更强（含 local 只读约束） |
| 11 | 工具偏好：debugger > 定向日志 > 绝不 log everything | runtime-observation-methods 已有「先最小侵入、先观察关键状态点」 | 保留本地 | 本地同义且更强 |
| 12 | 调试日志唯一前缀标签（[DEBUG-xxxx]）→ 一次 grep 清理 | debug-log-placement 有「输出字段最小集合」、cleanup 有「默认删除」，缺唯一前缀标签机制 | 合并 | 补进 `bug-intake-rules/references/runtime-diagnostics-bug-debug-log-rules-debug-log-placement.md` |
| 13 | Perf 分支：先建基线测量再 bisect，先测量后修复 | 本地无性能回归专项方法论 | 合并 | 并入 feedback-loop.md「性能回归」节 |
| 14 | 修复前写回归测试——仅当有正确接缝（correct seam）；接缝太浅给虚假信心 | test-regression 有回归范围判定，缺「正确接缝」概念 | 合并 | `test-regression-rules/references/correct-seam.md`（新建） |
| 15 | 无正确接缝本身就是发现：架构阻碍锁定 bug，标记给下一阶段 | 本地无此概念 | 合并 | 并入 correct-seam.md |
| 16 | 最小化复现→失败测试→修复→通过→重跑原始未最小化场景 | validation 有验证闭环、regression 有流程，缺「重跑原始场景」收尾 | 合并 | 并入 correct-seam.md |
| 17 | 收尾清单：原复现不再复现/回归通过/DEBUG 移除/一次性原型删除/正确假设写 commit message | debug-log-cleanup 有日志清理，缺「原型删除 + 正确假设写 commit」 | 合并 | 并入 correct-seam.md「修复收尾清单」 |
| 18 | post-mortem：修复后问「什么能阻止这个 Bug」，架构建议在修复后给 | 本地无 post-mortem 概念 | 合并 | `bug-validation-rules/references/post-mortem.md`（新建） |

- **落盘改动**：
  - 新增 `bug-reproduction-rules/references/feedback-loop.md`，并在 SKILL.md 默认执行流程第 2 步 + references 读取规则登记。
  - 新增 `bug-root-cause-rules/references/hypothesis-ranking.md`，并在 SKILL.md 默认执行流程第 3 步 + references 读取规则登记。
  - 修改 `bug-intake-rules/references/runtime-diagnostics-bug-debug-log-rules-debug-log-placement.md`（补唯一前缀标签机制）。
  - 新增 `test-regression-rules/references/correct-seam.md`，并在 SKILL.md 默认执行流程第 2 步 + references 读取规则登记。
  - 新增 `bug-validation-rules/references/post-mortem.md`，并在 SKILL.md 默认执行流程第 7 步 + references 读取规则登记。
- **整理去重**：N/A + 理由：本地五件套为引用式结构，无同义重复段落可合并；本次为纯方法论增量（反馈回路/假设排序/正确接缝/复盘四块本地确实缺失），无存量冗余可清。
- **同域扫描结论**：范围 = Bug 域 5 skill（intake/reproduction/root-cause/fix-proposal/validation）+ 测试域 3 skill（strategy/program/regression）；发现 = 初判 0 处重复段落、0 处门控层叠、0 处散落产物（feedback-loop 与 reproduction-template 为方法层 vs 格式层互补，post-mortem 与 validation-checklist 为阶段前后互补，均非冗余）；清理 0 处；**PASS**。
- **净增体积**：+9292 bytes（4 个新 reference + 1 处小补丁），引用式接入无膨胀。
- **棘轮验证**：5 个 skill `quick_validate.py` 全部 PASS；4 个新文件 UTF-8 无乱码；引用链可达（5 处 SKILL.md 引用 + 1 处跨 skill 引用 post-mortem→correct-seam 均可达）。
- **源清理**：吸收完成后删除本地安装源 `diagnose`（仓库根目录，junction 双路径同一物理目录）。

## 2026-08-19：java-story-develop__skillhub

- **来源**：LobeHub 安装包 `java-story-develop__skillhub`（工作区 `D:\谷歌云盘\luode-skills\java-story-develop__skillhub\`，用户级 `C:\Users\luode\.workbuddy\skills\java-story-develop__skillhub\`），版本以安装包 `_meta.json` 为准。
- **形态**：本地安装源吸收（先安装 → 分析吸收 → 删除源）。
- **拆解原子规则数**：14 条。

| # | 外部精华 | 本地现状 | 裁决 | 落点 / 理由 |
|---|---------|---------|------|------------|
| 1 | 环境探测：扫描 pom.xml/go.mod/package.json 探测运行时、Web 框架、ORM、业务框架、工具库、数据库、前端栈 | `project-memory-rules` 有四件套记忆但无环境探测清单机制 | 合并 | `project-memory-rules/references/environment-probe.md`（新建），含探测维度表 + 命令示例 + 记忆固化格式 |
| 2 | 记忆优先恢复环境，命中则跳过探测 | `project-memory-rules` 启动读 PROJECT_CURRENT/PROJECT_MEMORY | 保留本地 | 本地更强 |
| 3 | 环境记忆持久化格式（project-env-{projectName}） | `project-memory-rules` 机器索引区 | 合并 | 并入 environment-probe.md 的记忆固化格式 |
| 4 | 前端检测 + devMode 问询（FULLSTACK/BACKEND） | `package-structure-rules` 已能自动判断前后端同仓 | 拒绝 | 与本地「能自动判断就不问」习惯冲突 |
| 5 | SIMPLE/QUICK/FULL 三档分档路由 + 状态机 | `team-development-rules` 阶段路由、`requirement-splitting-rules` 复杂度拆分 | 合并 | `requirement-intake-rules/references/workload-mode-routing.md`（新建），与极致完整性标准调和 |
| 6 | context.json 状态机（currentPhase/phases/todos） | `task-plan-rehydration-rules` 投影 + AGENTS.md 追踪链 | 拒绝 | 机制形态不迁移，本地投影已覆盖 |
| 7 | 四轮小步迭代（骨架→填充→复盘→风险） | `artifact-delivery-gate-rules`（6-review）、`code-change-finalization-gate-rules` | 保留本地 | 本地更强 |
| 8 | 角色互搏（开发/产品双角色） | `adversarial-gap-interview.md` 已有对抗式缺口追问 | 合并 | `adversarial-gap-interview.md` 追加「设计阶段双角色自检」小节 |
| 9 | 异常恢复指引（6.1-6.5） | `agent-runtime-recovery-rules`、`session-handoff-rules`、`task-plan-rehydration-rules` | 保留本地 | 本地更强 |
| 10 | 11 条编码规范 | `code-generation-style-rules`、`code-quality-rules`、`error-handling-rules`、`logging-trace-rules`、`database-query-rules`、`naming-rules` 等十几条细分 | 保留本地 | 本地更细且 Go 生态适配 |
| 11 | 文档编号规则（1-Requirement/2-Analysis/3-Design） | `artifact-storage-rules`（doc/1-架构 2-需求 3-实施）+ 稳定 ID | 保留本地 | 本地更强 |
| 12 | TODO 分类规范（[临时]/[技债]/[外部依赖]/[逻辑补全]/[暂不明确]） | `task-blocker-closure-contract.md` 已有遗留项处理语义 | 拒绝 | 与本地闸门重叠，避免为吸收而吸收 |
| 13 | 核心变量命名（storyNameCN/ID/Branch） | `naming-rules`、`git-collaboration-rules` | 保留本地 | — |
| 14 | 子任务调度策略（并行分析/设计） | `parallel-task-dispatch-rules` | 保留本地 | 本地更强 |

- **落盘改动**：
  - 新增 `project-memory-rules/references/environment-probe.md`，并在 `project-memory-rules/SKILL.md` 适用场景追加引用。
  - 新增 `requirement-intake-rules/references/workload-mode-routing.md`，并在 `requirement-intake-rules/SKILL.md` References 追加引用。
  - 修改 `requirement-intake-rules/references/adversarial-gap-interview.md`，追加「设计阶段双角色自检」小节。
- **源清理**：吸收完成后删除本地安装 `java-story-develop__skillhub`（工作区 + 用户级两份）。
- **评分**：见对应 case study（`references/case-java-story-develop-absorption.md`，如需）。

## 2026-08-20：内部更新——需求 / 实施 / Bug 三域收敛去重

- **来源**：内部调整：三域 skill 体系（13 个 skill），调整诉求 = "整理一下需求、实施、bug 的 skill"（延续测试域收敛）。
- **形态**：内部更新通道（无外部源可删）。
- **拆解原子条目数**：13 个 skill 逐域盘点。

### 裁决与落点

| 域 | skill | 裁决 | 落点 / 理由 |
|---|---|---|---|
| 需求域 | intake / boundary / change / splitting | 保留现状 | 4 个 SKILL.md 均已"单一权威 + 引用"（shared-contract 76 行承载保护语义，各 SKILL.md 仅 1-2 句精简落地提示）；图片规则在 references 内为不同语境落地项（清单/检查/模板），非硬冗余 |
| 实施域 | delivery-gate | 调整合并 | step4 测试域细则（ASCII 镜像 / release-artifacts / apifox caseId）与 test-strategy 完全重复 → 收敛为引用 test-asset-governance + 《接口测试执行通道》 |
| 实施域 | implementation-planning | 保留现状 | 22 refs 主题区分度高（模板/门禁/契约/流程），按需加载是优点非膨胀；RULE-PMW / 跨会话契约红线不动 |
| 实施域 | storage / rehydration | 保留现状 | 职责独立，仅划界 |
| Bug 域 | intake 等 5 个 | 部分调整 | output-template 重命名规范化（→ bug-discovery-output-template.md）；11 个旧命名空间文件经全量复核为活跃路由资产（被 discovery-and-gap / runtime-diagnostics 引用），保留不删；五份 SKILL.md 已引用式（local 0 处展开复述），bug-lifecycle-common-contract 已为共享契约，C2-C5 保留现状 |

- **整理去重**：delivery-gate SKILL.md L62 测试域细则 → 引用 test-strategy（-约 80 字节展开）；Bug 模板重命名 + 注册表 TPL-PLAIN-BUG-002 path 同步 + discovery-and-gap.md L15 引用同步（消除旧命名空间文件名）。
- **同域扫描结论**：范围 = 需求域 4 + 实施域 4 + Bug 域 5（13 个 skill）；发现 = 探索初判 6 处冗余（需求图片规则 / 实施 refs 膨胀 / Bug 骨架同构等），实测后**3 处为误判**（已引用式 / 模块化设计 / 独立成文模板句），**1 处为误删**（Bug 旧命名文件实为活跃资产，已从 git 恢复 11 个 + 修复引用）；真实冗余 = delivery-gate 测试域细则 1 处 + 旧命名模板名 1 处；清理 2 处；**PASS**（引用链全量复核无死引用）。
- **净增体积**：-约 200 字节（收敛展开 + 重命名），无新增内容。
- **棘轮验证**：体积下降、UTF-8 全通过、全量回归无新增失败、引用链无断链——评分不降。

## 2026-08-20：内部更新——Skill 治理域盘点（保留现状）

- **来源**：内部调整：Skill 治理域（9 项），调整诉求 = "还有哪个域需要整理？→ 用户选 Skill 治理域"。
- **形态**：内部更新通道（只读盘点，无改动）。
- **裁决**：全部保留现状。
  - hit-check / audit / compliance-gate / reasoning-summary 四 gate：逐字重复检测 **0 处**；边界已通过"不替代/只负责/统一交给"声明划清（触发检查 / 过程中审计 / 收口闸门 / 总结渲染四阶段时序），合并会破坏触发机制，不整合即最好整理。
  - skill-dictionary：工具资产（generate_dictionary.py + data.js），被 authenticated-url-routing / code-style-consistency / doc 等广泛引用，非 skill 但移动破坏引用链 → 保留。
  - thread-title mcp/node_modules（23MB）：活跃 MCP server 依赖（SKILL.md 引用 bootstrap.mjs / rename_current_thread），删除破坏功能 → 保留；git 卫生（gitignore node_modules）另行处理。
  - evolution / split-preserve / absorption：职责清晰（gap 回补 / 体积拆分 / 外部引入），合并破坏各自触发 → 保留。
- **同域扫描结论**：范围 = 治理域 9 skill；发现 = 探索初判 4 处（门控层叠 3 遍 / dictionary 混入 / node_modules 垃圾 / 生命周期三 skill 归并），实测**全部为误判**（逻辑相似非逐字重复 / 工具资产 / 活跃依赖 / 职责独立）；真实冗余 0 处；清理 0 处；**PASS**。
- **净增体积**：0（只读盘点，零改动）。
- **棘轮验证**：未改动，无评分变化。

## 2026-08-20：内部更新——编码域盘点（保留现状）

- **来源**：内部调整：编码域（24 skill，~700KB），调整诉求 = "按优先级继续 → 编码域"。
- **形态**：内部更新通道（只读盘点，无改动）。
- **裁决**：全部保留现状。
  - 注释三件套（completion-gate / placement-granularity / chinese-comment）：逐字重复 0 处；三者为"补齐闸门 / 放置颗粒度 / 中文表达"三阶段视角，边界已通过"转交"声明划清；"5 行代码块步骤注释 / 结构体字段注释 / 补丁注释"虽在三件套内双写，但一处是"必须补"（闸门视角）、一处是"放哪"（放置视角），互补非冗余，合并会破坏 gate 强制触发语义。
  - 风格四件套（generation-style / minimal-change / readability / style-consistency）：逐字重复仅 1 处无害句（"不替代 style-consistency"）；四者为"写码前契约 / 范围控制 / 可读检查 / 一致性闸门"编码生命周期四阶段，generation-style 的"同时约束命名/结构/注释/日志/错误"是契约覆盖维度（写码前汇总声明），非越界执行，L58-65 边界节已划清。
  - api-* 四件套 / database-* 两件套：职责清晰（请求生命周期 / 结构-访问），保留。
  - 散落产物：无（各目录结构干净）；仓库根 inventory.yaml 是接口基线活跃资产（被 project-interface-baseline-rules 引用），保留。
- **同域扫描结论**：范围 = 编码域 24 skill；发现 = 探索初判 2 组（注释三件套可合一 / 风格四件套越界），实测**误判**（阶段/视角差异非逐字重复，边界已划清）；真实冗余 0 处；清理 0 处；**PASS**。
- **净增体积**：0（只读盘点，零改动）。
- **棘轮验证**：未改动，无评分变化。

## 2026-08-20：内部更新——Agent 运行域盘点（保留现状）

- **来源**：内部调整：Agent 运行域（11 skill，~568KB），调整诉求 = "按优先级继续 → Agent 运行域"。
- **形态**：内部更新通道（只读盘点，无改动）。
- **裁决**：全部保留现状。3 组候选触发重叠实测均为"触发源 / 时间窗 / 机制差异"，非硬冗余：
  1. session-handoff（用户主动换会话 / 归档）vs context-compression（系统被动压缩后的恢复）：触发源不同（用户发起 vs 系统事件）；compression 条件联动的是 recent-context-bootstrap 而非 handoff。
  2. autonomous（任务闭环推进，无 Goal 依赖）vs long-run-loop（Goal active / 显式 goal 意图驱动的长循环）：Goal 有无是关键差异。
  3. history-recall（用户主动问历史，深度回溯）vs recent-context-bootstrap（新会话启动引导，近 3 天）：双向"不要代替"声明已划清（recent 声明不代替 history 深度回忆，history 声明不代替 recent 近期引导）。
  - 逐字重复 0 处；8 个运行 skill 相互边界声明齐全（条件联动 / 不要代替 / 不替代执行授权）。
- **同域扫描结论**：范围 = 运行域 11 skill；发现 = 探索初判 3 组触发重叠，实测**误判**（触发源/时间窗/Goal 机制差异 + 边界声明已划清）；真实冗余 0 处；清理 0 处；**PASS**。
- **净增体积**：0（只读盘点，零改动）。
- **棘轮验证**：未改动，无评分变化。

## 2026-08-20：内部更新——项目记忆知识域盘点（保留现状，体系盘点收官）

- **来源**：内部调整：项目记忆知识域（8 skill，~444KB），调整诉求 = "顺手过一遍（体系盘点最后一个域）"。
- **形态**：内部更新通道（只读盘点，无改动）。
- **裁决**：全部保留现状。7 个 skill 产出物完全不同，职责天然清晰：
  - project-memory（四件套：状态/规则/历史）、project-style（PROJECT_STYLE.md 风格记忆）、project-local-skills（project-* 前缀项目级 skill 沉淀）、project-rule-file-bootstrap（新会话启动读取）、project-timeline（项目历程报告）、project-design-doc（项目设计.md 维护）、knowledge-flow（跨项目 Google Drive 知识库，明确与四件套分层）。
  - 逐字重复 0 处；边界声明齐全：style 不负责生成契约（归 code-generation-style）、local-skills 不代替 knowledge-flow、bootstrap 不替代 memory 事实抽取、timeline 不代替当前交付摘要、design-doc 不代替 recent-context-bootstrap/artifact-storage。
- **同域扫描结论**：范围 = 记忆知识域 8 skill；发现 = 探索初判"四件套 Owner 需划界"，实测**边界已划清**（产出物不同 + 双向声明）；真实冗余 0 处；清理 0 处；**PASS**。
- **净增体积**：0（只读盘点，零改动）。
- **棘轮验证**：未改动，无评分变化。

## 2026-08-20：内部更新——剩余 skill 全量扫描（4 组保留 + 4 个残留清理）

- **来源**：内部调整：8 域之外的剩余 skill 全量扫描，调整诉求 = "其他 skill 还需要整理吗？扫一遍"。
- **形态**：内部更新通道（扫描 + 少量清理）。
- **裁决**：
  - A 类自有规则 4 组候选重叠全部保留现状：浏览器三件套（本地自动化/高级观测/云端能力三层面，重复仅为 agent-browser 工具说明，独立可读需要，低价值不收敛）、安装组（MCP vs 插件，差异明确）、交付报告组（交付总结 vs 周期报告，差异明确）、Windows 组（编码 vs 环境，差异明确）。
  - 独立 A 类 8 个（git-collaboration / swag-openapi-maintainer / authenticated-url-routing / image-redbox-focus / godot-project-bootstrap / game-asset-* 等）职责清晰，保留。
  - B 类工具 skill 39 个（~4.75MB，含 skillhub + doc/pdf/spreadsheet 等）无卫生问题，无需整理。
- **清理（同域扫描发现）**：删除根目录 4 个 0 引用一次性脚本残留（_write_cycle.py / _write_cycle2.py / _write_docs.py / _bm_skillid_migration.json，均 git 跟踪、硬编码 8/8 文档路径，一次性产物）。index.html 保留（11 处引用）。
- **维持**：thread-title mcp/node_modules（活跃 MCP 依赖，gitignore 卫生另行处理）。
- **同域扫描结论**：范围 = 剩余全部 skill（17 A 类 + 39 B 类）；发现 = 4 组候选重叠 + 4 个残留；清理 4 个残留；真实冗余 0（A 类职责差异/低价值说明）；**PASS**。
- **净增体积**：-41KB（删除 4 个脚本）。
- **棘轮验证**：删除不影响任何引用（0 引用复核），评分不降。
