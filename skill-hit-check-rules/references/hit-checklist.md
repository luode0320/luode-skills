# 命中检查清单

## 检查顺序

1. 只基于当前轮用户消息和当前运行环境匹配所有 Skill 的 `description` 与条件路由。
2. 命中判断与领域动作可以同时进行，不需要先产出固定字段。
3. 将执行权交给对应 Owner Skill；本清单不复制其具体执行步骤。

## 注释场景补充

- 用户请求“补充注释”“只改注释”等表达时，至少检查 `comment-rules`（语言表达 / 位置颗粒度 / 补齐闸门三分区）、`code-change-finalization-gate-rules`。
- 函数/方法改动、补丁位点和最终核对清单仍按注释类 Owner Skill 执行，不在命中入口重复定义字段。

## 图片输入场景补充

- 消息包含图片或截图输入时，必须检查并命中 `image-redbox-focus-rules`。
- 不得跳过红框聚焦判断直接进入图片对应的主域任务。

## 项目规则/记忆聚合指令场景补充

- 用户给出“更新md / 更新项目规则md / 更新规则md / 根据 skill 更新项目 md / 补充仓库级规则”等聚合指令，或表达同步、补齐仓库级规则文件与项目 md 的意图时，必须命中 `context-recovery-rules`，并按其 `rule-bootstrap`（规则文件 `AGENTS.md` / `CLAUDE.md`、`.gitattributes`、`.editorconfig`）与 `memory-bootstrap`（`PROJECT_CURRENT.md` / `PROJECT_MEMORY.md` / `PROJECT_HISTORY.md` 骨架）两个条件路由同时验收，不得只完成一组文件就收口。
- 该聚合指令下 `PROJECT_STYLE.md` 联动 `project-style-rules`、四件套事实内容联动 `project-memory-rules`；具体路由、脚本入口和逐文件结果由上述 Owner 定义，本入口只负责不漏触发和三方联动确认。

## 项目记忆/风格跨项目候选场景补充

- 本轮 `project-memory-rules`/`project-style-rules` 写入条目时标记了 `跨项目候选: 是` 时，收口阶段的知识库判断不得停留在 `不适用`，至少需要按 `capture-retrieve-distill.md` 走一次沉淀判断（检索去重后决定是否创建/追加）。
- 具体标准、落点和去重仍由 `knowledge-flow` 的 `references/project-memory-sync.md` 定义，本清单只负责不漏判断信号，不复制其执行细节。

## 任务恢复场景补充

- 新会话、上下文恢复或当前消息包含任意“继续”或恢复意图时，先命中 `context-recovery-rules` 的 `recovery` 路由读取磁盘事实源，再进入主域；至少覆盖“继续”“接着做”“接着执行”“恢复任务”“恢复执行”“按原计划继续”“继续上次任务”“往下做”“继续刚才的工作”及同义自然语言表达。
- 恢复以落盘任务计划文档的状态字段与「下一动作」指针为准；`PROJECT_CURRENT.md` 只提供当前交接点，宿主任务列表只用于重建进度展示。
- 进行中步骤必须先核验磁盘、测试和外部状态；未知或非幂等写操作只查询、不重放。

## Go 测试资产场景补充

- 本轮新增或修改任意 `*_test.go`，或涉及测试程序、mock、fixture、数据构造脚本时，必须检查并命中 `test-program-rules`（含《Go 测试编译路径（强制）》），并按适用性路由到 `test-strategy-rules` 的 test-asset-governance。
- 源码目录禁放、ASCII 镜像、白盒诉求降级、生产代码测试污染判定和测试资产落点由上述专职 Owner 定义；本入口只负责自动触发和联动，不复制其目录清单、扫描命令或整改步骤。

## 代码改动收口场景补充

- 本轮发生代码新增或修改并准备收口时，按 `deferred-gate-registry.md` 加载对应 skill：至少 `comment-rules`、`code-style-consistency-rules` 的 `6-review`、`code-change-finalization-gate-rules`，并按 `reasoning-summary-structure-rules` 输出最终总结（Plan Mode 除外）。
- 具体注释字段、审查步骤和测试证据由各 Owner 定义。

## 代码改动中段场景补充

- 本轮首次发生代码改动时，直接在真实改动处加载代码域 skill（注释、实现自审、收口），不等到最终回复才第一次想起。

## 外部 Skill 吸收场景补充

- 用户表达"吸收/借鉴/融合/采纳 某个 skill 的精华到我们的 skill""这个 skill 能不能吸收""把 XX skill 的思路用起来""优化我们的 skill 让它更强大""把外部精华沉淀成规则"等意图时，必须命中 `skill-absorption-rules`，按"获取原文 -> 三态裁决 -> 落点简化 -> 8维评分棘轮验证 -> 登记"闭环执行。
- 提供外部 skill 的 URL / GitHub / 市场页面 / SKILL.md 原文时，先由 `skill-absorption-rules` 抓取并拆解；本入口不复制其裁决步骤。
- 外部种子场景由 `skill-absorption-rules` 总承接。

## 逆向工程场景补充

- 只要当前用户请求或上下文意图涉及：无源码应用逆向、二进制逆向、反编译、脱壳、代码抽取、ASAR 拆包、Electron 应用解构、APK/IPA 包体分析、WebAssembly/WASM 检查、Go/Rust 二进制编译器信息与依赖抽取、.NET/PE 程序集元数据审查、数据包 PCAP/HAR 协议逆向或功能实现原理逆向等，**必须自动联动命中 `rea`**，不得等用户额外点名输入 `/rea`。
- 命中后优先执行 `rea --version` 检查环境；若本地尚未安装或命令未找到，必须立即输出官方 Release 页面 [https://github.com/morluto/rea/releases](https://github.com/morluto/rea/releases) 与安装命令 `npm install -g rea-agents`，阻断未安装状态并引导安装，严禁凭空脑补逆向结论。
- 对拥有完整源码的常规仓库分析、重构和实现，使用常规代码检索工具，不触发 `rea`。

## 判定原则

- 以触发条件为准，不以“任务简单”“已经知道怎么做”或“用户没点名”为由跳过。
- 可以多 Skill 同时命中；`skill-hit-check-rules` 是总控入口，不算业务 Owner。
- 任务可切分、写集不冲突且环境支持时优先并行推进；单一根因、需求边界、接口契约等需统一裁决的主路径保持串行。用户禁止或环境不支持时串行执行。
- 仓库任务执行知识库选择性判断：依赖历史知识或用户长期偏好时为 `检索`，形成可复用知识时为 `沉淀`，无价值时为 `不适用`，知识库目录不存在或不可读、路径不合法、写入后回读不一致且影响动作时为 `阻断`。仅 `检索` 或 `沉淀` 联动 `knowledge-flow`。所有知识库读写必须限定在知识库根目录内操作，写入后回读校验。
- Skill 资产新增或修改时联动 `code-change-finalization-gate-rules`；description 或触发条件变化追加 `skill-absorption-rules`。
- 非预期执行失败联动 `execution-failure-learning-rules`；预期负向测试、用户取消、权限阻断和业务 Bug 分别交给其专属 Owner。

## Git 短指令场景补充

- Git 意图包括显式关键词 `git/commit/push/pull/rebase/merge/cherry-pick/stash/status/diff/log`，中文动作词“提交/推送/拉取/合并/变基/暂存”，以及“提交git/帮我提交/给我推上去/看下改动/同步到远端”等语义等价表达。
- Git 意图只认当前轮；历史轮次的提交或推送要求不得继承。
- 执行 Git 协作命中 `git-collaboration-rules`；本轮不再存在独立提交级审查 Skill，提交动作仍只处理 Git 边界。
- 不得要求用户额外补“测试已完成”后才触发 Git 路由，也不得由本入口直接实施提交步骤。

## 自主执行场景补充

- 多步骤任务存在完成原始目标仍必需且可直接执行的下一步时，检查 `autonomous-execution-rules`。
- 用户明确暂停、停止或结束时，停止自动继续和扩散输出；不得把建议项升级成新目标。

## 子代理分发场景补充

- 子代理判断按 `parallel-task-dispatch-rules` 处理。
- 共享写集、统一裁决主路径或上下文重复读取成本过高时保持串行。
- 若计划并行但未真实启动，必须报告回退原因，不能把计划数当作实际启动数。

## 漏触发防护

- 不确定时可标记候选命中并继续核验，不得跳过命中检查。
- 宿主技能列表只显示名称、未显示 `description` 时，不得把“看不到描述”当作“不命中”：名称与当前请求语义相关的，必须先读取其 `SKILL.md` frontmatter 再判定。
- 追问轮、延续轮与普通轮同等判定：上一轮遗留的待办不得吸收当前轮新出现的触发词。
- 不得把“只命中名称”当作已执行；必须完成 Owner Skill 的必要动作。
- 不得在代码已改动后直到最终回复才首次补声明注释或收口 Skill。
- 不得整轮实质任务到最终回复才首次意识到应命中任何延迟触发 skill（`reasoning-summary-structure-rules`、注释、`6-review`、收口、合规等）。
- 不得遗漏用户明确的停止、安全、授权、清理、回滚和输出协议。
