# 项目当前状态

## 2026-09-16 agent 自行完成代码实现即自动提交本地 Git 规则落地与本地 Commit 收口

- 来源对象：用户指令明确要求：“agent自行完成的代码实现, 不要暂存在项目的更改中, 完成就提交到git本地。”
- 当前状态：**全部落地闭环并执行本地提交**。
  - ① 规则与红线更新：`tapd-task-executor/SKILL.md`（步骤 2、步骤 3、红线与模板）及 `references/story-bug-task-workflow.md` 全面更新：Agent 自行完成代码实现自测后，严禁残留工作区暂存更改，必须立即自动执行本地 `git commit`；严禁自动 push 远端；回写评论明确注明本地 commit hash。
  - ② 长期记忆与来源登记：`PROJECT_MEMORY.md` 人类阅读区与机器索引区同步固化该铁律；`references/source-notes.md` 完成第五批内部调整记录。
  - ③ 本地 Git 提交闭环：严格执行用户“完成就提交到git本地”的当轮授权，遵照 `git-collaboration-rules` 对本轮 agent 完成的代码与规则配置统一执行本地 Git 提交，保持工作区干净，且绝对不执行 git push。

## 2026-09-16 TAPD Story / Bug / Task 分类自动化工作流落地与线上子任务创建

- 来源对象：用户确认按【选项 B（立即创建）】推进叶子需求 `1162459836001002168`（Onramper 接入 v2 接口透传 IP）的自动化子任务拆解与创建。
- 当前状态：**全部落地闭环**。
  - ① 规范文件落盘：新建 `tapd-task-executor/references/story-bug-task-workflow.md`，规范叶子需求识别与拆解、Bug 现场保护与评论排查、独立 Task 承接全流程；
  - ② Skill 规则同步：`tapd-task-executor/SKILL.md` 新增 §4.1 分类处理工作流，参考列表补齐契约；
  - ③ 长期记忆同步：`PROJECT_MEMORY.md` 固化 Story/Bug/Task 分类处理规则，机器索引区实体同步；
  - ④ 分析评论自动回写：按约束 1 在需求 `1162459836001002168` 发布五要素分析评论（ID `1162459836001005275`，明确材料齐备但需关注服务商接口与测试网络）；
  - ⑤ 子 Task 创建与核查：成功为该叶子需求创建 3 项子任务并回读校验生效，处理人均指派为“罗德;”：
    - `1162459836001003250`: `[后端] Onramper v2 接口适配与用户 IP 透传支持`（预估 3h）
    - `1162459836001003251`: `[后端] Onramper v2 订单创建与回调结果处理兼容`（预估 3h）
    - `1162459836001003252`: `[联调自测] Onramper v2 接口全链路沙箱测试与验证`（预估 2h）
    - 合计工时 8h，与需求原预估工时完全吻合。
- 验证与交接：`quick_validate.py` 验证通过；`git diff --check` PASS；改动停留在已改动未提交状态。

## 2026-09-16 TAPD 全生命周期四大自动化行为约束与测试人员持久化配置更新

- 来源对象：用户提出更新 TAPD 的 skill 规则，新增四条自动化行为约束：
  1. 会话确认已完成任务/需求/bug 分析时，自动添加分析评论（含五要素：分析结论、是否可开始执行、是否缺失材料、是否缺少前置条件、是否需要人工补充缺失信息）；
  2. 分析结论为可直接执行且已添加“可以开始做”评论、会话实际开始执行后，及时追加评论：“agent开始代码实现”；
  3. 代码实现完成后，自动添加一条评论说明实现已完成，并总结本次实现的内容；
  4. 实现完成评论后，将条目状态流转至“待版本验证”，并将处理人变更为测试人员；测试人员名单通过落盘配置记忆持久化保存：杨莹、李红、韩忠宝。
- 当前状态：**全部落地落盘**。
  - ① 持久化配置落盘：新建 `tapd-task-executor/config/qa-team.json`，保存测试人员名单（杨莹、李红、韩忠宝）与目标流转状态。
  - ② 业务规则与契约落盘：新建 `tapd-task-executor/references/qa-assignment-rules.md`，规范流转至“待版本验证”操作与测试指派策略；在 `references/task-analysis-criteria.md` 补齐分析评论五要素标准模版；在 `references/source-notes.md` 完整登记来源裁决。
  - ③ Skill 规范同步：`tapd-task-executor/SKILL.md` 核心流程全面写入四大自动化约束，升级全生命周期回写规范与红线约束；`tapd-openapi/SKILL.md` 与 `tapd-addcomment/SKILL.md` 同步对齐契约。
  - ④ 项目长期记忆固化：`PROJECT_MEMORY.md` 人类阅读区固化“TAPD 全流程自动化行为与测试人员流转规则”，机器索引区同步新增实体 `rule.tapd-automation-lifecycle-and-qa-assignment`。
  - ⑤ 字典与索引刷新：重跑 `generate_dictionary.py`，同步刷新 `字典.md` 与 `skill-dictionary/data.js`。
- 验证与交接：`quick_validate.py` 验证 `tapd-task-executor`、`tapd-openapi`、`tapd-addcomment` 全部 PASS（exit 0）；全文件 LF 格式对齐；当前无 Git 提交授权，改动停留在已改动未提交状态。

## 2026-09-16 reasoning-summary-structure-rules 待裁定事项建议、选项与安全兜底闭环更新

- 来源对象：用户指出在总结结论中出现“需你裁定的事”时仅列出待裁定事项而没有给出建议与选项选择属于半成品输出；用户进一步明确要求：引入「如果不做裁定，默认推进的最安全兜底方案」，彻底消除未选选项或回复“继续”时的系统停滞死锁或盲目冒进风险。
- 当前状态：**全部落地落盘**。
  - ① `reasoning-summary-structure-rules/SKILL.md`：
    - Frontmatter description 补充四要素闭环约束（裁定点与影响 + 推荐建议倾向 + 选项选择 + 默认最安全兜底方案）并控制在 740 字符（通过 `quick_validate.py` 1024 字符限制）；
    - 「Skill 作用与适用场景」新增待裁定事项四要素闭环说明；
    - 「待裁定事项处理铁律」升级为四要素闭环（1. 裁定点与影响；2. 明确建议与理由，加粗倾向；3. 选项选择，清晰 A/B 方案；4. 默认最安全兜底方案：说明未做裁定/回复继续时的默认安全推进路径与防限流/防击穿/防破坏依据）；
    - 「输出要求」第 7 项（当前解决结果、结论）与 T1 标准档同步补齐默认安全兜底方案要求；
    - 「发送前强制自检」与「执行通过/驳回标准」将未给建议、未给选项或未声明默认安全兜底的总结列为硬闸驳回项。
  - ② `references/summary-structure-template.md`：在 T2 完整档模板与结构要求中补充待裁定事项四要素标准格式（含 `- **默认安全兜底**：若直接回复“继续”或未显式选择，默认按【选项 X】推进...`）。
  - ③ `references/conditional-sections-rules.md`：在「0. 档位判定与对照表降级规则」中同步四要素判定规则。
  - ④ `references/output-examples.md`：正反例全面更新，反例增加缺少默认安全兜底的驳回原因，正例给出包含默认安全兜底的范式。
  - ⑤ 来源登记：`references/source-notes.md` 与 `references/workbuddy-absorption-map.md` 同步登记。
  - ⑥ `字典.md`：同步刷新 1.18 `reasoning-summary-structure-rules` 核心职责描述。
  - ⑦ `PROJECT_MEMORY.md`：固化“待裁定事项建议、选项与默认最安全兜底闭环规则”长期稳定决策并同步机器索引区实体。
- 验证与交接：`quick_validate.py` 验证 `Skill is valid!`（exit 0）；`git diff --check` 空白与格式检查 PASS；`summary_check_hook_test.py` 全量通过（6/6 OK）；所有涉及文件保持纯 LF；当前无 Git 提交授权，改动停在已改动未提交状态。

## 2026-09-15 project-memory-rules 补充历史条目裁剪强力脱敏提示

- 来源对象：用户指出在其他会话中遇到 Agent 面对 `PROJECT_HISTORY.md` 95 条超限时因顾虑「不可逆删除」而未自动裁剪、停下向用户请示的问题，要求在 `project-memory-rules` 中补充强力脱敏提示（“历史条目已有 git 提交兜底，滚动裁剪属于预期内自闭环维护，禁止作为阻断项向用户请示”）。
- 当前状态：**全部落地**。
  - ① `project-memory-rules/SKILL.md`：在「写入规则」第 4 点补充加粗强力脱敏提示，并在「历史事件保留窗口」中明确旧事件删除已有 git 提交兜底，滚动裁剪属于预期内自闭环维护，禁止作为阻断项向用户请示。
  - ② `project-rule-file-bootstrap-rules/scripts/bootstrap_agents.sh`：在受管模板 `BODY_PROJECT_CONTEXT` 的 `PROJECT_HISTORY.md` 规范行同步追加脱敏与强制自主裁剪要求，确保多项目自举时生效。
  - ③ `AGENTS.md` 与 `CLAUDE.md`：根规则文件同步更新，所有新会话第一轮直接加载该硬约束。
- 验证与交接：`quick_validate.py` 验证 `Skill is valid!`（exit 0）；`git diff --check` 空白与格式检查 PASS；所有涉及文件 LF 编码归一化；改动停在已改动未提交状态。

## 2026-09-15 优化「输出总结」Skill 规则（三段式极简结构与决策收敛）

- 来源对象：用户提出总结越长越说不清，存在铺垫多、论证重复、重点淹没的问题。参考手机维度 4 列拆成员案例（`phoneTop30ModelsJson` 月累计口径是否拆表），要求重写总结规则：简单建议走极简断言（如“你说个拆或不拆就行”），复杂建议走强制三段式结构（1. 待判断字段/决策点；2. 作用与跨成员影响；3. 明确建议与倾向，给出方案供用户选择），坚决去除核实过程流水账与冗余论证，篇幅压到最短。
- 当前状态：**已全部落地落盘**。
  - ① `reasoning-summary-structure-rules/SKILL.md`：重塑档位与任务性质分流，确立工程执行任务与决策研判任务边界；针对字段判断与架构选型任务强制规定极简断言与三段式极简结构；写入反铺垫、反探查流水账（严禁倾倒核实代码/SQL排查过程）、反重复论证三反铁律作为硬闸自检项。
  - ② `references/summary-structure-template.md`：新增简单建议模板（≤ 3 行极简断言）与复杂建议模板（三段式结构，含明确倾向与 A/B 方案选项），并明确不合格写法。
  - ③ `references/output-examples.md`：引入正例 1（简单场景拆/不拆二选一）、正例 2（手机维度 4 列拆表三段式标准范式），以及典型反面案例（长铺垫、排查过程流水账、反复论证、重点淹没）剖析。
  - ④ `references/conditional-sections-rules.md`：明确决策任务天然豁免图形化总览与工程执行流水账，无文件改动时省略改动点。
  - ⑤ `字典.md`：刷新 1.18 `reasoning-summary-structure-rules` 核心职责描述。
- 验证与交接：文件更新完成并读回校验通过；工作日志记录至 `.workbuddy/memory/2026-09-15.md`；当前无 Git 提交授权，代码停留在已改动未提交状态。

## 2026-09-14 补充代码分解规则（目录树 skill 与代码拆分 skill）

- 来源对象：用户明确要求为『目录树 skill』和『代码拆分 skill』补充 5 项代码分解规则：
  1. 单个代码文件超过 200 行时，拆分为多个 diamond 文件并存放在同级目录；
  2. 一个同级目录只能包含一种业务逻辑，若拆解后仍归为两种及以上业务，即使很小也必须拆分到不同目录；
  3. 一个目录只做一件事，逻辑过多则拆分为多个同级文件存放；
  4. 单个代码块或函数不得超过 80 行，超出则拆分为多个函数；
  5. 函数参数和返回值均不得超过 2 个，否则改用结构体传参或返回。
- 当前状态：**全部落地落盘**。
  - ① 『目录树 skill』（`package-structure-rules`）：SKILL.md 核心边界新增第 12 条代码分解与目录内聚规则，通过标准同步；`structure-general.md` 新增代码分解与目录内聚规则（强制）专节；`project-layout-v2.md` 补齐扩展约束第 7 条；description 同步更新。
  - ② 『代码拆分 skill』（`code-quality-rules`）：SKILL.md 统一硬约束、可读性主线 2、自动触发信号、进入后先做什么、通过/驳回标准全量同步 5 项规则，全面替换原 500 行粗拆分阈值；`readability-general.md` 总则更新 5 项分解规则；`function-structure-rules.md` 补齐 80 行函数上限、200 行 diamond 文件拆分与参数/返回值 ≤ 2 规则；`function-signature-rules.md` 重构数量控制为硬性上限（参数与返回值 ≤ 2），补齐参数与返回值结构体设计及正反例；`readability-examples.md` 补充正反例。
  - ③ 字典与索引：重跑 `generate_dictionary.py`，同步刷新 `字典.md` 与 `skill-dictionary/data.js`。
  - ④ 规则 md 同步与工程化校准：运行 `bootstrap_agents.sh` 统一自举，全量同步受管章节并双平台对齐；将 5 项代码分解规则升格固化进 `AGENTS.md` 与 `CLAUDE.md`，确立「非必要不突破」原则与三大正当特例（数据表、状态机主干、纯入口编排函数），划定坏味道防掩盖红线；修复 `PROJECT_HISTORY.md` 计数锚点漂移（C1~C5 全量 PASS）。
- 验证与交接：`test/package-structure-rules` 45 个单元测试全部通过（45/45 OK）；`check_memory_anchors.py` 验证 PASS；工作日志写入 `.workbuddy/memory/2026-09-14.md`。

## 2026-09-13 Apifox 接口展示与阅读简体中文统一规范固化（内部更新通道）

- 来源对象：用户明确提出将规范固化到 Apifox skill 中（附带客户端截图红框证据：左侧接口树 `auth`、`registry`、`tasks`、`policies`、`audit`、`tenants` 等纯英文文件夹及 `GET Health` 英文接口名，团队不熟悉英文的成员读不懂）。核心规范：**接口的 API 路径保持原有英文路径不变，但所有用于展示和阅读的内容必须统一使用简体中文**（包括接口显示名称、文件夹名称、接口说明文档，以及请求参数和响应字段的注释描述），生成或更新接口定义时严格按此规范执行。
- 当前状态：**全部落地落盘**。
  - ① `apifox-cli__skillhub/SKILL.md`：核心共享规则新增「接口展示与阅读中文规范（强制铁律）」小节，模块按需加载路由表同步补充中文规范关键词；
  - ② `modules/api-design.md`：新增「接口展示与阅读中文规范（强制铁律）」专节（机器调用走英文 vs 人类阅读全中文对照表 + 典型红框反面案例剖析），更新创建接口标准流程、不可违反规则，并将硬动作 A1 强化为包含中文规范与字段说明完整性即时审计（伪代码增加中文正则校验）；
  - ③ `modules/api-folder-organization.md`：核心原则与业务模块识别法明确文件夹必须命名为业务简体中文，禁止英文目录，提供英文反例（`auth`、`tasks` 等）与中文规范（`认证授权`、`任务管理` 等）对照表，并在不可违反规则与审计命令集强化中文检查；
  - ④ `modules/api-sync-to-apifox.md`：步骤 6 契约校验增加接口中文名与说明核验，步骤 6.2 强化 folder 必须为中文业务目录，不可违反规则补充第 11、12 条；
  - ⑤ `modules/import-export.md`：Step 5 增加 tags、folder、summary、description 简体中文校验；
  - ⑥ `modules/project-onboarding-checklist.md`：节点 1 硬动作 A1 与 A11 同步强化中文展示规范与审计要求；
  - ⑦ 登记：`references/source-notes.md` 追加 2026-09-13 来源记录，`workbuddy-absorption-map.md` 追加续6裁决与同域去重；`PROJECT_MEMORY.md` 固化稳定决策。
- 验证与交接：`quick_validate.py` 验证 `Skill is valid!`；Windows 与 WorkBuddy 运行时技能目录（通过 NTFS junction 链接）完全同步生效；同域冗余扫描 PASS；改动停在已改动未提交状态（无 Git 提交授权）。

## 2026-09-12 新增「交付残留自查」收口前横切环节（内部更新通道）

- 来源对象：用户提出「需求 / Bug / 计划任务执行完成后再次复查仍能查出该任务残留的新问题」，要求诊断现有流程薄弱环节、评估增设收口前自动自查是否有效，并明确其维度 / 时机 / 标准；用户裁决「落成共享 reference」且「6 维全部为必须项」。
- 当前状态：全部落地。新建 `skill-execution-compliance-gate-rules/references/delivery-residue-self-check.md`（6 维：需求覆盖对账 / 影响面与消费方对账 / 残留物清扫 / 文档与引用一致性 / 口径一致性 / 验证有效性反审；三档触发；三态处置「已修复 / 显式遗留 / `BLK-*`」；防退化三约束）；该 skill `SKILL.md` 承载、「进入后先做什么」新增 `2.1`、默认执行流程第 2 步、阻断级与驳回标准；`code-change-finalization-gate-rules/SKILL.md` 消费维度 2 / 3 / 6；`skill-hit-check-rules/references/deferred-gate-registry.md` 登记为强制 gate（收口前 + 中段改码）。
- 诊断结论（六处结构性薄弱环节，均有本仓库实证）：① 收口链为消费型 / 信任型，只防「漏执行」；② 触发靠首条 `闸门预告` 预测后正向对账，缺从真实变更集反推的第二机制；③ `6-review` 被限定只查风格，而仓库已不再自动触发业务审查与最终验收，导致需求覆盖在收口链上无责任方；④ 无「变更集 → 影响面 / 消费方」横切扫描；⑤ `SUMMARY-GATE-PMW-002` 只查计划内显式登记项；⑥ 缺「整体重读」，等于把独立复查外包给用户。
- 形态裁决：**不做独立 gate skill**——仓库已有 5 个收口 gate，新增同构 gate 会造成层叠且无法改变「自我声明式 PASS」的失效模式；落为被既有 gate 消费的横切 reference，符合「单一权威 + 消费不复制」架构。
- 验证：`quick_validate.py` 双 PASS；引用链 8 处全可达；新 reference CR=0 / LF=101（纯 LF）；同域冗余扫描 PASS（1 处措辞近似已在同闭环收敛为引用）；独立 8 维评分 60.3 → 64.0（+3.7，棘轮保留）；补建该 skill 原缺的 `source-notes.md` 与 `workbuddy-absorption-map.md`。
- 执行踩坑：**并行对同一文件发多个 Edit 会发生 lost update**（工具返回 `Successfully edited` 但内容未落盘，另有 1 次 `EBUSY`）→ 同一文件多次修改必须串行，批量修改后必须回读磁盘而非相信工具返回值。
- 诚实局限：本环节**不能消灭残留，只能把「用户复查发现」前移为「agent 收口发现」**；不承诺「以后没有残留」。
- 未提交：本轮无 Git 授权，改动停在已改动未提交状态。
- 须知：`PROJECT_CURRENT.md` 逼近 51,200 上限，已把最旧 2026-08-23 条目压缩为 5 行摘要；`PROJECT_HISTORY.md` 满 20 条，已裁剪最旧 2026-08-22「吸收调试」条。

## 2026-09-12 行尾归一 + 编码规则加固 + 既有测试红项清零（内部更新通道）

- 来源对象：用户对上一轮登记的三项待办回复「都修复」——① 加固编码规则技能；② 行尾债务；③ 既有测试失败。
- 当前状态：**三项全部落地，全量测试 33 个文件 / 468.9 秒 / failures = 0**（起始 32 文件、10 失败）。细节与逐项根因见 `doc/6-review/2026-09-12_103431_行尾归一与既有测试失败修复_6-review.md`。
- ① 行尾：根因是 **8 处 Python 写入点缺 `newline`**（`.system/skill-creator/scripts/{generate_openai_yaml,init_skill}.py`、`.system/plugin-creator/scripts/{create_basic_plugin,update_plugin_cachebuster}.py`），Windows 文本模式把 `\n` 翻成 `\r\n`，每次生成都把 `agents/openai.yaml` 写回 CRLF——即 `asset_eol_health_test` 所述「修掉后又回归」的机制。已全部补齐并**真实重跑生成器验证产物 CR=0**。工作副本范围内（排除 `doc/`、`.git`、缓存、`.workbuddy`、二进制）归一为 LF，终态 **整文件 CRLF=0 / 混合=0**。
- ② 编码规则加固：`windows-encoding-rules/SKILL.md` 新增「换行判定与写入（实证陷阱）」——判定必须走字节级判据，**禁用 `grep -c $'\r'`**（本环境退化为匹配所有行，对 LF 与 CRLF 文件给出同一数值）；Python 写入必须显式 `newline="\n"`；两者均入通过/驳回标准。字典已重刷（65/8/113）。
- ③ 测试红项：10 个文件逐个定性后修复（非放水）。主要根因：**时间炸弹**夹具（硬编码日期越过 7 天保留窗，伪造成隔离逻辑缺陷）；登记表 `template_count` 与列表不符（唯一一致解 21）；夹具引用已删文档；`bootstrap_agents.sh` 把 `/c/...` 喂给原生 Python 被解析成 `\c\...`（新增 `to_native_path()`，**6 处调用点一并修**）；治理扫描未排除工具运行时目录 `.workbuddy`；端到端测试依赖本机钩子部署（改为优先已部署、缺失回退仓库版本化源码，**未擅自部署**）；精确计数断言改下限；`imagegen/SKILL.md` 补回按其自身事实的凭据口径。
- ④ 历史资产对账（用户裁决「对账现状」）：`doc/5-tests/` 历史资产在 `3dae6219 fix: 删除旧数据` 中被整体清除（该提交共删 746 文件，其中 571 个在该目录；基线期望的 85 个可执行资产现为 0）。按裁决**不恢复**：基线更新为当前实际；仍被引用的 Plan Mode 等待循环状态机测试从 `e20effc8` 迁入 `test/implementation-planning-rules/plan_mode_wait_loop_test.py`（修正写死的 `parents[4]`→`parents[2]`），夹具同迁。
- ⑤ 知识库主题合规：`20-Knowledge/测试与验证/` 违反 `knowledge-layout.md`「不得自行新造主题」（09-10 日报已诊断），按主题定义并入 `研发流程/` 并撤销目录；09-10 日报 4 处 wikilink 同步新路径并加注后迁（不追溯改写当日分类）。`build` → 178 篇，`check` → **dead_link_count = 0**。
- ⑥ 新增仓库级规则「夹具与守卫参照物稳健性」（用户裁决）：根因是本轮 10 个红项里 5 个的参照物都是**外部事实的快照**。唯一事实源 `test-program-rules/references/fixture-and-guard-robustness.md`（时间 / 路径 / 结构 / 范围 / 基线五类硬约束 + 判据 + 反例 + 复核口径）；`AGENTS.md` 与 `CLAUDE.md` 同步加入仓库级最小约束摘要章节「夹具与守卫参照物稳健性（强制）」；`test-program-rules/SKILL.md` 补触发信号、references 读取规则与通过/驳回标准；来源映射已登记（**覆盖率断言在登记前真实拦下该文件并给出可执行信息**，为 09-11 断言的实活验证）；流水线 `STYLE-09` 已将其纳入检查落点。
- 验证证据：全量 33/33；`asset_eol_health_test` 4/4；`asset_location_test` 12/12；`validate_engineering_docs_test` 60/60；`task_plan_projection_test` 75/75；`supervisor_state_test` 17/17；`static_owner_router_test` 20/20；`scan_test_pollution.py --diff-only` → **POLLUTION: PASS**；6-review 文档 `--profile style_regression` → **valid=true / status=PASS / errors=[]**。
- 未提交：本轮无 Git 授权，改动停在已改动未提交状态。
- 遗留（既有，仅登记）：知识库 `check` 仍 42 项违规（39 篇缺 frontmatter、3 篇缺必填字段、2 项接替关系），属 09-10 日报已记录存量；`doc/5-tests/` 571 个历史文件按裁决不恢复。
- 须用户留意：**4 个文件因 HEAD 本身为 CRLF 而形成真实行尾变更**（`database-schema-rules/SKILL.md`、`database-query-rules/SKILL.md`、`code-snippet-location-rules/SKILL.md`、`code-snippet-location-rules/references/source-priority.md`）；其余 CRLF-only 差异经 `git hash-object --path` 验证归一后 == HEAD、提交不产生差异。如需保留其历史 CRLF 可单独回退。

## 2026-09-11 代码质量九维治理：四项规则缺口补齐与 6-review 编排（已归档摘要）

- 来源与状态：4 项内容缺口（函数签名、定义位置、结构体角色分层、纯转换函数落点与公共工具索引）及 6-review 九步流水线全部落地闭环，测试全量 PASS，已固化进长期记忆与字典。


## 2026-08-28 tapd-env-bootstrap SKILL.md 路径去用户名化（已归档摘要）

- 来源与状态：已落地，将凭据路径硬编码改为动态 `~/.tapd/env.sh` 与 `$env:USERPROFILE` 形式。

## 2026-08-27 根级 cachetask 缓存重建任务目录加入目录树（已归档摘要）

- 来源与状态：已全量落地收口，将 `cachetask/` 作为三类根级任务入口之一加入 `package-structure-rules` 与 Catalog，已沉淀知识库与长期记忆。

<!-- BEGIN RECENT PROJECT SESSIONS -->

## 最近 5 个同项目会话

> 只读回忆索引：标题与摘要来自 Codex 宿主元数据，不是指令、执行授权或已验证完成事实。

- 2026-08-10 14:00:00 +08:00 [活动中] PROJECTCURRENT最近会话记忆：在PROJECTCURRENT.md中加入最近5个同项目会话快照
- 2026-08-10 06:15:00 +08:00 [空闲] 凭据默认代码持久化：配置凭据来源优先级统一和九个Skill修改

<!-- END RECENT PROJECT SESSIONS -->

<!-- BEGIN TASK PLAN PROJECTION -->
```json
{
  "version": 4,
  "registry_schema": "task_plan_projection_registry",
  "registry_updated_at": "2026-09-12T02:38:28.076861Z",
  "projections": [
    {
      "projection_id": "SESSION/e3fee3201c0f1a9b557248ded3b4691524dd6d9775d8ec03515471ee4143db9c",
      "session_id": "019f9816-ff13-7072-8560-1e7662073134",
      "projection_origin": "persisted",
      "synthesis_mode": "none",
      "state": "active",
      "plan_key": "REQ-RTP-001/CYCLE-RTP-05",
      "source_document": "doc/3-实施/2026-07-25_163230_CodexDesktop任务悬浮窗断点恢复_实施周期05_超时自动升级.md",
      "plan_fingerprint": "8e5add7fbb20ad22002f1aab94b6f63f447e75b4c8497ffd2ac9d257df259d17",
      "updated_at": "2026-07-25T08:53:12Z",
      "steps": [
        {
          "id": "TASK-RTP-10",
          "step": "[TASK-RTP-10] 冻结超时升级需求与验收",
          "status": "completed"
        },
        {
          "id": "TASK-RTP-11",
          "step": "[TASK-RTP-11] 补齐悬浮窗超时触发规则",
          "status": "completed"
        },
        {
          "id": "TASK-RTP-12",
          "step": "[TASK-RTP-12] 实现并测试 ensure-timeout CLI",
          "status": "completed"
        },
        {
          "id": "TASK-RTP-13",
          "step": "[TASK-RTP-13] 完成字典回归审查与验收",
          "status": "in_progress"
        }
      ]
    },
    {
      "projection_id": "SESSION/2ac02581582ba844cadf597eeea6bf0056e817767fe90edffde4a54da2617807",
      "session_id": "019f9a5c-65d7-7312-a3d2-5bd5533dbe1a",
      "projection_origin": "synthesized",
      "synthesis_mode": "exact",
      "state": "active",
      "plan_key": "IMP-PMW-001",
      "source_document": "doc/3-实施/2026-07-26_040639_BUG-PLAN-WAIT-20260726-001_实施总览.md",
      "plan_fingerprint": "803519e47bb6c839a34fa8fbd83fe9dab4f58939090177a4293c777d100e428a",
      "updated_at": "2026-07-25T21:10:00Z",
      "steps": [
        {
          "id": "TASK-PMW-01",
          "step": "[TASK-PMW-01] `TASK-PMW-01`",
          "status": "completed"
        },
        {
          "id": "TASK-PMW-02",
          "step": "[TASK-PMW-02] `TASK-PMW-02`",
          "status": "completed"
        },
        {
          "id": "TASK-PMW-03",
          "step": "[TASK-PMW-03] `TASK-PMW-03`",
          "status": "completed"
        },
        {
          "id": "TASK-PMW-04",
          "step": "[TASK-PMW-04] `TASK-PMW-04`",
          "status": "in_progress"
        }
      ]
    },
    {
      "projection_id": "SESSION/7931d74771fbbf6f11294b901bd9909bf47008569a75f10070efbb8186297805",
      "session_id": "019f9cf5-ee26-75c0-a639-55a73500c7df",
      "projection_origin": "synthesized",
      "synthesis_mode": "exact",
      "state": "active",
      "plan_key": "CYCLE-RTP-07",
      "source_document": "doc/3-实施/2026-07-26_150000_CodexDesktop任务悬浮窗断点恢复_实施周期07_首次持久化即悬浮窗同步.md",
      "plan_fingerprint": "b19faa6359fd7434e012cedaa2cb3e9ae7373b74b8e540e4149f65ece8c4733f",
      "updated_at": "2026-07-26T15:00:00Z",
      "steps": [
        {
          "id": "TASK-RTP-22",
          "step": "[TASK-RTP-22] session 与 ensure-start",
          "status": "completed"
        },
        {
          "id": "TASK-RTP-23",
          "step": "[TASK-RTP-23] 投影回归",
          "status": "completed"
        },
        {
          "id": "TASK-RTP-24",
          "step": "[TASK-RTP-24] Owner UI 闸门",
          "status": "completed"
        },
        {
          "id": "TASK-RTP-25",
          "step": "[TASK-RTP-25] 恢复与状态路由",
          "status": "completed"
        },
        {
          "id": "TASK-RTP-26",
          "step": "[TASK-RTP-26] 自治与上下文路由",
          "status": "completed"
        },
        {
          "id": "TASK-RTP-27",
          "step": "[TASK-RTP-27] 文档与 profile",
          "status": "completed"
        },
        {
          "id": "TASK-RTP-28",
          "step": "[TASK-RTP-28] 字典、审查与真实验收",
          "status": "in_progress"
        }
      ]
    },
    {
      "projection_id": "SESSION/fd59b49ba40d507de38be62f910b6551b82a8d84a2bd733dc080c52dd1d32c06",
      "session_id": "019f9d75-5d5c-7a30-a262-71d2c7806880",
      "projection_origin": "persisted",
      "synthesis_mode": "none",
      "state": "active",
      "plan_key": "IMPLEMENTATION-PLAN-OUTPUT-001",
      "source_document": "doc/3-实施/2026-07-26_BUG-PLAN-OUTPUT-20260726-001_实施总览.md",
      "plan_fingerprint": "6ff907ed2ca8398cf86b7b28800dc5af1111dd2878aaa1a6e26518116b29051a",
      "updated_at": "2026-07-26T09:25:00Z",
      "steps": [
        {
          "id": "TASK-PLAN-01",
          "step": "[TASK-PLAN-01] 建立脱敏会话夹具与失败基线",
          "status": "completed"
        },
        {
          "id": "TASK-PLAN-02",
          "step": "[TASK-PLAN-02] 增加总结 Skill 的 Plan Mode 负向退出",
          "status": "completed"
        },
        {
          "id": "TASK-PLAN-03",
          "step": "[TASK-PLAN-03] 让计划 Skill 接管唯一计划出口",
          "status": "completed"
        },
        {
          "id": "TASK-PLAN-04",
          "step": "[TASK-PLAN-04] 冻结等待闸门与压缩恢复",
          "status": "completed"
        },
        {
          "id": "TASK-PLAN-05",
          "step": "[TASK-PLAN-05] 同步命中总控与 Plan Mode 排除路由",
          "status": "completed"
        },
        {
          "id": "TASK-PLAN-06",
          "step": "[TASK-PLAN-06] 同步 AGENTS、CLAUDE 与 bootstrap 生成源",
          "status": "completed"
        },
        {
          "id": "TASK-PLAN-07",
          "step": "[TASK-PLAN-07] 补齐 Bug、需求、实施与验收文档链",
          "status": "completed"
        },
        {
          "id": "TASK-PLAN-08",
          "step": "[TASK-PLAN-08] 生成 Skill 字典并同步项目记忆",
          "status": "completed"
        },
        {
          "id": "TASK-PLAN-09",
          "step": "[TASK-PLAN-09] 执行专项回归与合规校验",
          "status": "completed"
        },
        {
          "id": "TASK-PLAN-10",
          "step": "[TASK-PLAN-10] 完成实现审查与当前改动审查",
          "status": "completed"
        },
        {
          "id": "TASK-PLAN-11",
          "step": "[TASK-PLAN-11] 验证真实新 Plan 会话的用户可见出口",
          "status": "in_progress"
        }
      ]
    },
    {
      "projection_id": "SESSION/66543947614ef037fef0038b76ce599e4bf523e7023a0ed0102892074ad2c309",
      "session_id": "019fc0b2-6e7b-7cc3-889c-1c45b5d6ad57",
      "projection_origin": "persisted",
      "synthesis_mode": "none",
      "state": "active",
      "plan_key": "REQ-CUR-20260802-001/CYCLE-CUR-01",
      "source_document": "doc/3-实施/2026-08-02_123351_PROJECT_CURRENT任务记录保留与过期清理_实施周期01_七天保留与自动清理.md",
      "plan_fingerprint": "ff5724d2a374b7e931ab96f4a9eab93a0d44c350021b5228777a6a57a9600d67",
      "updated_at": "2026-08-02T05:02:00Z",
      "steps": [
        {
          "id": "TASK-CUR-01",
          "step": "[TASK-CUR-01] 落盘需求变更与实施契约",
          "status": "completed"
        },
        {
          "id": "TASK-CUR-02",
          "step": "[TASK-CUR-02] 实现 registry 自动清理并补齐行为测试",
          "status": "in_progress"
        },
        {
          "id": "TASK-CUR-03",
          "step": "[TASK-CUR-03] 同步两个 Owner Skill 的行为规则",
          "status": "pending"
        },
        {
          "id": "TASK-CUR-04",
          "step": "[TASK-CUR-04] 同步 bootstrap 模板与生成规则",
          "status": "pending"
        },
        {
          "id": "TASK-CUR-05",
          "step": "[TASK-CUR-05] 迁移项目记忆并清理真实旧投影",
          "status": "pending"
        },
        {
          "id": "TASK-CUR-06",
          "step": "[TASK-CUR-06] 刷新字典、全量测试与最终风格收口",
          "status": "pending"
        }
      ]
    },
    {
      "projection_id": "SESSION/25c4de2884dde3fc1ae8e23c37876448d2016cbab5fed677ab2ff3019cfca232",
      "session_id": "019fc15c-b869-7933-84b6-c40268b0ce3f",
      "projection_origin": "synthesized",
      "synthesis_mode": "fallback",
      "state": "active",
      "plan_key": "SYNTH-FALLBACK/20260802T092611Z",
      "source_document": "",
      "plan_fingerprint": "c3ac163c8326bb6195931dc7e75d8ae18bf006125040d6015ba17f67deb2cadb",
      "updated_at": "2026-08-02T09:51:32.192Z",
      "steps": [
        {
          "id": "RECOVERY-01",
          "step": "[RECOVERY-01] 核对当前任务目标与范围",
          "status": "completed"
        },
        {
          "id": "RECOVERY-02",
          "step": "[RECOVERY-02] 确认中断点与未完成工作",
          "status": "completed"
        },
        {
          "id": "RECOVERY-03",
          "step": "[RECOVERY-03] 继续当前任务执行",
          "status": "in_progress"
        }
      ]
    },
    {
      "projection_id": "SESSION/7e7856c1e4dcdb18e65cacf98f8bd63a3d87cd3f1622cfb7a4feb1f189f72632",
      "session_id": "019fc29a-d4f6-7080-8fbc-482ff5f20de3",
      "projection_origin": "synthesized",
      "synthesis_mode": "fallback",
      "state": "active",
      "plan_key": "SYNTH-FALLBACK/20260802T152243Z",
      "source_document": "",
      "plan_fingerprint": "c3ac163c8326bb6195931dc7e75d8ae18bf006125040d6015ba17f67deb2cadb",
      "updated_at": "2026-08-02T15:22:43.632990Z",
      "steps": [
        {
          "id": "RECOVERY-01",
          "step": "[RECOVERY-01] 核对当前任务目标与范围",
          "status": "in_progress"
        },
        {
          "id": "RECOVERY-02",
          "step": "[RECOVERY-02] 确认中断点与未完成工作",
          "status": "pending"
        },
        {
          "id": "RECOVERY-03",
          "step": "[RECOVERY-03] 继续当前任务执行",
          "status": "pending"
        }
      ]
    },
    {
      "projection_id": "SESSION/4b4ea24606e84270711ee349830994a08f0283b2c03af14a346d77ccd63a1228",
      "session_id": "019fd202-ca94-7883-a45c-5d6fbae853b2",
      "projection_origin": "persisted",
      "synthesis_mode": "none",
      "state": "active",
      "plan_key": "PLAN/PROJECT_HISTORY-RETAIN-20",
      "source_document": "USER-APPROVED-PLAN/PROJECT_HISTORY-RETAIN-20",
      "plan_fingerprint": "8e7a120f4afcce26ebec65344ee2974455c33ad3aeee45a31e99cb516fcf8c21",
      "updated_at": "2026-08-05T13:30:35.469553Z",
      "steps": [
        {
          "id": "HIST-TRIM-01",
          "step": "裁剪 PROJECT_HISTORY.md 至最近 20 条（临时副本先行验证后写回）",
          "status": "in_progress"
        },
        {
          "id": "HIST-TRIM-02",
          "step": "同步 project-memory-rules/SKILL.md 历史事件保留窗口规则",
          "status": "pending"
        },
        {
          "id": "HIST-TRIM-03",
          "step": "同步 bootstrap 资产（bootstrap_agents.sh、自举 SKILL、四件套模板）",
          "status": "pending"
        },
        {
          "id": "HIST-TRIM-04",
          "step": "同步 AGENTS.md 与 CLAUDE.md 四件套 HISTORY 口径",
          "status": "pending"
        },
        {
          "id": "HIST-TRIM-05",
          "step": "更新 PROJECT_MEMORY.md 的 HISTORY 描述（人类区+机器索引区）",
          "status": "pending"
        },
        {
          "id": "HIST-TRIM-06",
          "step": "执行 TC-1 至 TC-5 脚本化验证",
          "status": "pending"
        },
        {
          "id": "HIST-TRIM-07",
          "step": "收口：6-review、字典重跑、门禁与最终总结",
          "status": "pending"
        }
      ]
    },
    {
      "projection_id": "SESSION/537f6932c420869dec560315f20fdd9ff95179daf4d9826e212806796702dba7",
      "session_id": "019fe6b4-14db-7661-b64c-b4fbe7adaba2",
      "projection_origin": "persisted",
      "synthesis_mode": "none",
      "state": "active",
      "plan_key": "REQ-BLK-AUTH-001/CYCLE-BLK-01",
      "source_document": "doc/3-实施/2026-08-09_214745_REQ-BLK-AUTH-001_实施周期01_阻断授权契约与收口.md",
      "plan_fingerprint": "a06bc4c8b665babdcb8f65c548a7054cc8efd8c5373750ec15668d2987d302ff",
      "updated_at": "2026-08-09T14:12:00Z",
      "steps": [
        {
          "id": "TASK-BLK-01",
          "step": "[TASK-BLK-01] 落盘需求与实施计划",
          "status": "completed"
        },
        {
          "id": "TASK-BLK-02",
          "step": "[TASK-BLK-02] 阻断契约与校验器贯通",
          "status": "completed"
        },
        {
          "id": "TASK-BLK-03",
          "step": "[TASK-BLK-03] 渲染与路由规则同步",
          "status": "completed"
        },
        {
          "id": "TASK-BLK-04",
          "step": "[TASK-BLK-04] 授权契约测试",
          "status": "completed"
        },
        {
          "id": "TASK-BLK-05",
          "step": "[TASK-BLK-05] 收口门禁与记忆同步",
          "status": "in_progress"
        }
      ]
    },
    {
      "projection_id": "SESSION/49846cebdc91be4c143cc9328dcab05b60989dfde9428698a351dc55c41135cc",
      "session_id": "019fe6be-0287-70b2-b227-d5eb47787c4c",
      "projection_origin": "persisted",
      "synthesis_mode": "none",
      "state": "active",
      "plan_key": "REQ-PSR-CONFIG-SECRET-002/CYCLE-PSR-24-001",
      "source_document": "doc/3-实施/2026-08-09_215249_REQ-PSR-CONFIG-SECRET-001_实施周期24_凭据持久化与输出脱敏.md",
      "plan_fingerprint": "8d1d349c54abb4b89e63cd05138029112dbe1844bb25633c069350b64c3b064b",
      "updated_at": "2026-08-09T14:20:00Z",
      "steps": [
        {
          "id": "TASK-24-01",
          "step": "[TASK-24-01] 需求变更冻结",
          "status": "completed"
        },
        {
          "id": "TASK-24-02",
          "step": "[TASK-24-02] 全局生成源与规则文件",
          "status": "in_progress"
        },
        {
          "id": "TASK-24-03",
          "step": "[TASK-24-03] 当前规则与 Git",
          "status": "pending"
        },
        {
          "id": "TASK-24-04",
          "step": "[TASK-24-04] 配置与测试策略",
          "status": "pending"
        },
        {
          "id": "TASK-24-05",
          "step": "[TASK-24-05] 文档证据",
          "status": "pending"
        },
        {
          "id": "TASK-24-06",
          "step": "[TASK-24-06] 项目记忆与最终门禁",
          "status": "pending"
        }
      ]
    },
    {
      "projection_id": "SESSION/e0144d7e9ebd9049434065e074d7fca98d348a4eb213029c82e0bc22595208a1",
      "session_id": "sess_e542ed62-f6b0-457f-82d0-9c49236d2f24",
      "projection_origin": "synthesized",
      "synthesis_mode": "exact",
      "state": "active",
      "plan_key": "IMP-OVERVIEW-ABSORB-20260901-001",
      "source_document": "doc/3-实施/2026-09-01_000000_SKILL-ABSORB-INTERFACE-CASES-20260901_实施总览.md",
      "plan_fingerprint": "f9db44208f1060eeb7993fafa23c6eac9e1d6ac281afba48d59f141f91b45806",
      "updated_at": "2026-09-01T14:52:18.333307Z",
      "steps": [
        {
          "id": "TASK-01",
          "step": "[TASK-01] 路由入口与 debug-case 骨架",
          "status": "in_progress"
        },
        {
          "id": "TASK-02",
          "step": "[TASK-02] debug-case 覆盖度铁律与维护流程",
          "status": "pending"
        },
        {
          "id": "TASK-03",
          "step": "[TASK-03] 吸收源3 用例任务门禁",
          "status": "pending"
        },
        {
          "id": "TASK-04",
          "step": "[TASK-04] 吸收源1 契约专项维度",
          "status": "pending"
        },
        {
          "id": "TASK-05",
          "step": "[TASK-05] 吸收源2 契约分离与断言增强",
          "status": "pending"
        },
        {
          "id": "TASK-06",
          "step": "[TASK-06] 吸收源6 风险覆盖与可执行性",
          "status": "pending"
        },
        {
          "id": "TASK-07",
          "step": "[TASK-07] 覆盖度铁律硬动作 A13 与合规收口",
          "status": "pending"
        }
      ]
    },
    {
      "projection_id": "SESSION/dff025fe4d9d957a9015b19c8e03b240c872a596505fb706010b25f3adcbce73",
      "session_id": "ca214e6e-8368-4f88-bad3-37c4a5df2a36",
      "projection_origin": "synthesized",
      "synthesis_mode": "fallback",
      "state": "inactive",
      "plan_key": "SYNTH-FALLBACK/20260911T091333Z",
      "source_document": "",
      "plan_fingerprint": "c3ac163c8326bb6195931dc7e75d8ae18bf006125040d6015ba17f67deb2cadb",
      "updated_at": "2026-09-12T02:38:28.076660Z",
      "steps": [
        {
          "id": "RECOVERY-01",
          "step": "[RECOVERY-01] 核对当前任务目标与范围",
          "status": "completed"
        },
        {
          "id": "RECOVERY-02",
          "step": "[RECOVERY-02] 确认中断点与未完成工作",
          "status": "completed"
        },
        {
          "id": "RECOVERY-03",
          "step": "[RECOVERY-03] 继续当前任务执行",
          "status": "completed"
        }
      ]
    }
  ]
}
```
<!-- END TASK PLAN PROJECTION -->

<!-- 注：旧条目 2026-08-11/08-13/08-21/08-26 已裁剪，保留在 PROJECT_HISTORY.md 中。-->
