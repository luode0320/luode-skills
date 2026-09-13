# 项目历史事件

> 本文件追加关键历史事件并只保留最近 20 条（按日期倒序、新事件置顶、追加后自动裁剪）；普通启动默认不读取，只有历史追问、当前状态不足或真实卡点时才窄检索。

## 事件

- 2026-09-12：**新增「交付残留自查」收口前横切环节（内部更新通道）**。用户痛点：需求 / Bug / 计划任务执行完成后**再次复查仍能查出该任务残留的新问题**。诊断出六处结构性薄弱环节（均有本仓库实证）：① 收口链为消费型 / 信任型，gate 只消费下游 owner 的 PASS/FAIL，能防「漏执行」防不住「执行得不够」；② 触发靠首条 `闸门预告` 预测后正向对账，缺从真实变更集反推应有 gate 的第二机制；③ `6-review` 被制度性限定只查风格、不判业务正确性与需求覆盖，而仓库已不再自动触发业务审查与最终验收，导致需求覆盖在收口链上**无责任方**；④ 检查单位是单 gate 单维度，无「变更集 → 影响面 / 消费方」横切扫描；⑤ `SUMMARY-GATE-PMW-002` 只查计划内显式登记项，查不到计划外残留；⑥ 验证粒度停留在对象本身，缺「整体重读」，等于把独立复查外包给用户。最强实证：来源映射 v1→v2 升级后监督侧读取方静默降级为 P1，**测试因自带 v1 夹具而全绿**，缺陷对测试套件不可见。用户裁决落成共享 reference + 6 维全部强制。落盘：新建 `skill-execution-compliance-gate-rules/references/delivery-residue-self-check.md`（6 维 = 需求覆盖对账 / 影响面与消费方对账 / 残留物清扫 / 文档与引用一致性 / 口径一致性 / 验证有效性反审；三档触发「中段改码轻量版 → 收口前完整版 → 失败时」；三态处置「已修复 / 显式遗留 / `BLK-*`」；防退化三约束「输入必须是磁盘事实 / 发现项必须落盘 / 二次发现即机制失效回流失败学习」）；`skill-execution-compliance-gate-rules/SKILL.md` 承载（作用条目 + `2.1` + 流程第 2 步 + 阻断级 + 驳回标准 + references 读取规则）；`code-change-finalization-gate-rules/SKILL.md` 消费维度 2 / 3 / 6；`deferred-gate-registry.md` 登记为强制 gate。**形态裁决：不做独立 gate skill**——仓库已有 5 个收口 gate，新增同构 gate 会造成层叠且无法改变「自我声明式 PASS」的失效模式，故落为被消费的横切 reference。验证：双 `quick_validate` PASS；引用链 8 处可达；新 reference CR=0 / LF=101；同域冗余扫描 PASS（1 处「静态验证不能顶替真实运行验证」措辞近似已在同闭环收敛为引用式）；独立 8 维评分 60.3 → 64.0（+3.7，棘轮保留）；补建该 skill 原缺的 `source-notes.md` 与 `workbuddy-absorption-map.md`。**执行踩坑（可复用教训）**：并行对同一文件发多个 Edit 会发生 **lost update**——6 个 Edit 全部返回 `Successfully edited`，回读却只落实 2 处，另有 1 次 `EBUSY: resource busy or locked`；根因是同消息内多 Edit 被并行执行、后写覆盖前写，且工具返回不反映真实落盘结果；处置为整文件重写一次落全 + grep 逐条回读校验。**教训：同一文件的多次修改必须串行，批量修改后必须回读磁盘而非相信工具返回。** 诚实局限（已写入交付说明）：本环节不能消灭残留，只能把「用户复查发现」前移为「agent 收口发现」。记忆维护：`PROJECT_CURRENT.md` 逼近 51,200 上限，压缩最旧 2026-08-23 条目为摘要；`PROJECT_HISTORY.md` 满 20 条，裁剪最旧 2026-08-22「吸收调试」条。改动停在已改动未提交状态。

- 2026-09-11：**代码质量九维治理：四项规则缺口补齐（内部更新通道）**。用户提出 AI 辅助开发瓶颈已从「逻辑正确性」转向「代码质量」，列出九维（架构与模块划分 / 编写习惯与风格 / 注释与定义位置与命名 / 引用方式与包别名 / 静态风格命名与位置 / 函数签名 / 结构体按作用分层 / 纯转换工具函数落点 / 工具函数索引文档规范），要求系统化治理。用户裁决保守节奏「先补规则内容，后处理编排时机」+ 三项口径（函数参数=语义优先、定义位置=开头集中、结构体分层=按语言生态）。逐项闭环（落地→校验→索引→登记），四项全部完成：① 新建 `code-quality-rules/references/function-signature-rules.md`（参数顺序 ctx→必填→可选；数量语义优先，同源≥3 建议收、含可选/扩展字段必收；单参数与结构体取舍判据；命名 `XxxParams`/`XxxOptions`）；② 新建 `code-quality-rules/references/definition-placement-rules.md`（局部变量函数开头集中、包级变量常量顶部集中、函数追加末尾；与 `code-style-consistency-rules` 的「声明形式」约定配套）；③ 新建 `package-structure-rules/references/struct-role-layering.md`（角色谱系与落点表 + 引用面从小到大判定顺序 + Go/Java/TS/Python 生态差异 + 按角色注释颗粒度）；④ 新建 `common-util-rules/references/util-index-doc-contract.md` + `util-placement.md` 新增「纯转换工具函数的落点（点名判据）」小节——**关键落点发现**：公共工具索引唯一合法落点为 `doc/1-架构/3-模块职责.md` 的「公共工具索引」小节，原候选 `utils/<pkg>/README.md`（Catalog `allowed_extensions` 只含源码扩展名，`.md` 不在列）与 `doc/` 新建子目录（doc 子目录已由 Catalog 固定）**全被 Catalog 否掉**。附带：补建 `common-util-rules` 登记文件 2 个（该 skill 原缺 source-notes + absorption-map）；顺手修复 `package-structure-rules/references/directory-usage-routing.md` 第 19 行表破损（`utils/decimal/` 与 `utils/cache/redis/` 挤成一行）。验证：4 个新 reference 引用链 grep 一致；`package-structure-rules` 测试 7/7 PASS（含覆盖索引文件的 `backend_utils_usage_routing_test.py`）；同域冗余扫描 PASS；字典重跑 exit 0（implemented 65 / planned_missing 8 / seed 113）；全仓 runner 因缺 `pyyaml`（既有环境基线）无法整体启动。登记：4 个 skill 的 source-notes + absorption-map、当日工作日志、PROJECT_CURRENT。改动停在已改动未提交状态。
- 2026-09-10：**跨项目写入红线改造：绝对禁止 → 默认只读 + 会话级写入授权（用户决策）**。原规则「其他项目绝对只读、不存在取得用户授权后即可执行的例外」阻断多项目功能对接。经 AskUserQuestion 三项确认：① 授权粒度=**会话级**（本会话内一次确认对目标项目持续有效，会话结束 / 撤销 / 越界 / 版本漂移即失效）；② 操作范围=**全权限**（文件写入、构建测试、依赖安装、Git 提交推送）；③ 不设绝对禁止子项。落盘 6 处：`AGENTS.md` 与 `CLAUDE.md`「跨项目写入红线」同文改写（新增「例外通道（会话级跨项目写入授权）」+ `WRT-*` 授权记录契约 + 生效 / 失效条件 + 未授权唯一出口）；`implementation-planning-rules/references/sibling-project-discovery.md`「绝对禁止」节改「默认只读 + 会话级写入授权」、「需要改动兄弟项目时的唯一出口」改「未获授权时的唯一出口」；`cross-session-plan-execution-contract.md` 补 `EXT-*` 涉及修改时的 `WRT-*` 前置；`codegraph-analysis-rules/SKILL.md` 兄弟项目 `codegraph init` 由「一律禁止」改「授权覆盖下可执行」；`bug-intake-rules/references/discovery-and-gap-bug-discovery-rules-evidence-and-db-readonly.md` 对照项目由「绝对只读」改「默认只读 + 授权例外」。保留独立红线（非本条子项）：`local` 连接红线、凭据不回显、个人文件安全、当前项目 Git 当轮意图。校验：AGENTS.md / CLAUDE.md 双文件 blob 一致（`ee7d3b84`）、6 文件手术式 diff 无越界、未改 `description` 与 `##` 标题故无需重跑字典。改动停在已改动未提交状态。

- 2026-09-10：**补齐 `doc/` 文档生命周期与退场规则（`artifact-storage-rules` 内部更新通道）**。用户发现 `code/EllipalFinance-go/doc/` 约 180 份、本仓库 `doc/` 约 145 份过程文档长期无人清理。根因是规则缺位：`knowledge-flow` 侧早有知识笔记三档退场机制，而 `artifact-storage-rules` 只覆盖存储的空间维度（落点 / 命名 / 复用），时间维度完全缺失，既有清理条款（`.gap.md`、图片旧版本、迁移后旧目录、`test/{skill}/temp`）全为事件驱动。用户拍板：落点扩展 `artifact-storage-rules`、时间阈值半个月（15 天）、处置「沉淀知识库后删除老文档」（删除档，不设归档目录）。落盘：新增 `references/lifecycle-policy.md`（四道前置守卫：沉淀·引用·闭环·可恢复）；`SKILL.md` 新增「文档生命周期与退场（强制）」章节并扩 `description`；`path-map.yaml` 新增 10 个 `process_doc_*` 键；`update-policy.md` / `skill-integration.md` / `root-directories.md` 补策略摘要与引用入口；重跑字典刷新 `data.js` 与 `字典.md`。验证：`quick_validate.py` `Skill is valid!`；YAML 解析通过（version 10，11 键回读一致）；同域扫描 7 个 skill 0 冗余 PASS。登记 absorption-map + source-notes + 当日日志。**本轮同时修复 PROJECT_HISTORY 两处既有锚点缺陷**（补「吸收 EllipalNodeSync 同事 tapd 资产」缺失锚点、补全被截断的「记忆使用计数与高频条目自动吸收」锚点 title 与 4 个计数字段）。改动停在已改动未提交状态。

- 2026-08-28：**吸收 EllipalNodeSync 同事 tapd 资产（外部吸收）**。用户指向 `EllipalNodeSync/.claude/skills/tapd-openapi` + `.tapd/`。裁决：合并 2（新版 tapd_client_stdlib.py 545 行全文替换本地 287 行，新增 mine 子命令/with_ancestors 父需求树/status_map/resolve_iteration/download_entity_images 等 15 函数；SKILL.md 新增「输出规范」章节）；拒绝 3（SKILL.md 其余段本地 env-bootstrap 联动更优、search_wiki.py/hooks.json 与本地一致、.tapd/ 壳项目级参考不落盘）。关键适配：外部变量名 TAPD_ACCESS_TOKEN/TAPD_API_BASE_URL → 本地 TAPD_TOKEN/TAPD_API_ENDPOINT，_get_headers/_get_base_url/_is_cloud 三处 or 回退。联动增强：tapd-task-executor 第 3 步优先 mine。验证：真实 API 冒烟 mine 输出父需求树（兑换→兑换提供外部服务-对接开放接口），quick_validate 双 valid，同域 0 冲突。改动停在已改动未提交状态。

- 2026-08-28：**新建 tapd-task-executor skill（用户指令）**。用户要求：说「找 tapd 的任务做」等主动领取语义即自动触发，拉取当前用户名下未完成任务+bug，分析描述清楚度与可实现性，可执行项在当前会话项目内自行实现修复，无可执行项时列 3 条高优先级待完善。经 AskUserQuestion 确认 4 项决策：独立 skill（执行编排层，复用 tapd 四兄弟能力不重复造轮子）、只筛当前会话项目（跨项目一律忽略，符合 AGENTS.md 跨项目写入红线）、完成回写=领取置处理中+评论执行摘要+终态交人工、兜底仅当前用户范围。落盘：`tapd-task-executor/SKILL.md` + `references/task-analysis-criteria.md`（描述清楚度/可实现性判定标准）。验证：quick_validate `Skill is valid!`（exit 0）；同域触发扫描（全仓 grep「找任务做/tapd做」）0 抢触发 PASS；冒烟 TAPD_TOKEN len=40 已注入、tapd-cli.cjs/add_comment.py 存在。环境观察：TAPD_WORKSPACE_IDS 运行时为 `62459836,30399328`（env-bootstrap 记录 3 个、少 36150079，待核对）。登记：知识库《TAPD任务自动执行skill-20260828》+ source-notes + 工作日志。改动停在已改动未提交状态。

- 2026-08-28：**skill-absorption-rules 新增「优化 XX skill」泛化触发模板（内部更新通道）**。用户诉求：只要提出「优化 <?> skill」（<?> 为任意 skill 名）就走固定优化流程。落盘：description 追加泛化触发短语（646→约710字符，<1024 合规）；自动触发信号第 7 条追加模板说明（与列举式合并去重）+ 新增第 8 条按基线分流路由（有 8 维评分基线→`low-score-skill-optimization-sop.md` 八步闭环；无基线→内部更新通道同闭环 + `quick_validate.py` 结构校验替代棘轮）。关键坑：① description 含尖括号被 quick_validate 拒绝（`Description cannot contain angle brackets`），占位符统一改「XX」文字表达；② Git Bash 双引号内嵌 python -c 长字符串时反引号被 bash 命令替换篡改文本（source-notes 两处反引号片段被剥离，已 Edit 修复）。验证：quick_validate `Skill is valid!`（exit 0）；同域扫描（全仓 grep「优化.*skill|skill.*优化」）0 抢触发 PASS；知识库沉淀《WorkBuddy官方市场skill吸收整理补充》追加「泛化触发模板」节 + updated 刷新，`knowledge_index.py check` 268 链接 0 死链 exit 0；登记 source-notes + absorption-map + 工作日志。改动停在已改动未提交状态。

- 2026-08-28：**tapd-env-bootstrap SKILL.md 路径去用户名化（用户指令）**。用户指出本机 TAPD 凭据配置路径不应写死 `C:\Users\luode`、`/home/luode`，改用 `~/` 用户路径。落盘：真源文件（Windows/WSL）两行改 `~/.tapd/env.sh`（Windows 注明即 `$env:USERPROFILE\.tapd\env.sh`）；更新凭据流程第 1 步同改；第 2 步 WSL 同步命令改为 PowerShell 双行（`$env:USERPROFILE` → WSL 内 `wslpath` 解析 → `cp` 到 `~/.tapd/env.sh`）。关键实测坑：`wsl -e bash -lc` 下 `$USERPROFILE` 为空（WSL 默认不注入 Windows 环境变量）；Git Bash 侧无 `wslpath`；沙箱拦截 Bash 调 `cmd.exe`；最终链路 `(wsl -e bash -lc "wslpath '$env:USERPROFILE'").Trim()` 实测 EXISTS。验证：grep 零残留（`C:\Users\luode`/`/home/luode`/`/mnt/c/Users/luode`），tapd 系列其他 skill 无同类硬编码。观察项：quick_validate.py 允许键不含 `agent_created`（既有基线）。改动停在已改动未提交状态。

- 2026-08-27：**新增根级 `cachetask/` 缓存重建任务目录进目录树（内部更新通道）**。用户提出：`crontask/` 是定时任务目录，但存在"类定时任务"——缓存更新（缓存 60s 到期后先返回旧数据、再异步更新新缓存，Stale-While-Revalidate），希望专属目录 `cachetask/` 承载并说明用处。落盘：`project-layout-v2.md` 后端目录树加 `cachetask/` 条目（[条件·提交]、`cachetask/<task>/` 单任务入口）+ 正文「三类根级任务入口」说明（crontask 时间驱动 / cachetask 缓存过期驱动 SWR / async 消息驱动；缓存读写技术适配归 `utils/cache/`，cachetask 只承载重建逻辑）；`SKILL.md` description 补"缓存任务" + 核心边界第 2 条根级唯一位置；`structure-general.md`/`node-python-module-layout.md`/`java-layer-layout.md` 根级目录列表同步；`placement_catalog.py` `ADOPTION_V2_SOURCE_ROOTS["backend"]` 加 cachetask；`work-report-summary-rules/scripts/generate_git_report.py` MODULE_LABELS 补 `"cachetask": "缓存任务"`。顺手修复：`configuration_layout_test.py` `standard_environments` 断言同步 apifox（2026-08-21 引入的标准环境扩展，测试基线未同步的既有漂移）。验证：adoption/strict 双策略 check 临时项目（含 cachetask/coin_price/refresh.go）均 exit 0；package-structure-rules 45 项测试全通过；字典重跑 exit 0；知识库沉淀《cachetask缓存重建任务目录》与《配置表驱动缓存五件套》双向关联、`knowledge_index.py check` exit 0（254 链接 0 死链）；6-review `STYLE: PASS`。全量 400 测试 12 失败/13 错误均为既有环境性基线（缺 Go 工具链、git 环境、台账断言等），失败文件与本轮改动无交集。登记 absorption-map + source-notes + PROJECT_MEMORY（人类区稳定决策 + 机器索引 rule.cachetask-root-task-entry）。改动停在已改动未提交状态。
- 2026-08-26：**字段三件套（NOT NULL + DEFAULT + COMMENT）吸收进 `database-schema-rules`（内部更新通道）**。用户规则指令「数据库表字段必须 NOT NULL 并且需要有 DEFAULT 默认值、COMMENT 说明」。落盘：SKILL.md 铁律 1 重写为三件套（+description 与触发信号/权责边界/暂停确认/通过驳回/归档要求共 6 处 DDL 完整性位点统一补 NOT NULL，消除"如果适用"弱化口径）；`schema-boundaries.md` 新增「铁律：字段三件套」小节（例外仅 AUTO_INCREMENT 主键自增隐式默认、TEXT/BLOB/JSON 无默认值能力类型；存量表新增字段可空过渡最终收口三件套）+ DDL 完整清单第 2 项强化 + 检查清单项 + 完整 DDL 示例 `remark` 改 NOT NULL；`schema-examples.md` 正例 1 `remark` 改 NOT NULL + 正例 5 补「最终态收口三件套」注记 + 反例 5 问题列表补缺 NOT NULL；`table-design-standards.md`「必须声明」改三件套口径 + 配置驱动/多对多/审计日志表 5 处示例补 NOT NULL + DEFAULT（JSON 列注明无默认值例外）；登记 absorption-map + source-notes。知识库《数据库表设计规范.md》第五节强化三件套 + updated 刷新 + 关联行更新，回读校验一致。验证：quick_validate `Skill is valid!`（exit 0）、knowledge_index check PASS、同域扫描（database-query-rules/comment-rules）0 重复、git diff 90+/23-。改动停在已改动未提交状态。
- 2026-08-26：**低分 skill 批量优化第十一轮（9 个，A+B+D 裁决，36.9-49.2 → 61.2-67.5）**。用户点名评分报告最低 9 个 skill「按顺序一个一个优化，默认 A+B+D（内容+交叉引用+版本环境）」。逐 skill 八步闭环：self-ent-tech-database-design 36.9→63.3（frontmatter 空键致 YAML 解析失败实锤 + 补触发词/4 步工作流/交叉引用）、goal 37.7→62.8（纯命令入口补流程边界与降级）、golang 46.0→66.1（**真实 bug**：script.sh 12 个命令分支在 case 顶层误用 `local` 导致全部带参写入报错，sed 修复后 12 命令实测全通过；宣称"构建工具"实为日志工具，诚实化定位）、frontend-design 46.7→61.2（补 5 步流程 + 2 确认检查点 + 删 comment-rules 三连重复）、tg 48.6→66.5（发送/回复强制逐字确认闸门 + 异常处理）、file-organize 48.7→67.5（补个人文件操作安全红线：扫描只读→逐项确认→分批≤10→不删除；新建 references/category-map.md）、skill_2054901716814716928 48.8→63.3（frontmatter 8 违规键合规化 + 删营销签名 + 补流程检查点）、cryptocurrency-data-api 49.0→66.1（工具表去重 + **修 search_schools 高考志愿复制残留** + 补错误处理）、ip 49.2→64.6（**修脚本路径断链** `skills/ip/ip.py`→本目录 `ip.py` + ip.py 去 requests 改标准库 urllib，无 key/缺参/非法 JSON/假 key 联网 4 分支实测通过 + name 合规化 ip-query）。验证：9×quick_validate valid；统一独立子代理复评全部高于基线（+14.5 ~ +26.4，棘轮保留）；报告 9 行更新，总平均 60.6→61.7，新最低 pdf 50.1（原最低 36.9 出列），Node+Python 双端校验一致；登记 source-notes + absorption-map + 知识库沉淀。改动停在已改动未提交状态。
- 2026-08-26：**版本化目录导入别名对齐规则吸收进 `package-structure-rules`（代码实测 gap → 内部更新通道）**。来源：ellipal_finance 实测——`swapList "ellipal_finance/internal/service/v1/list"` + `v2list` 不对称，v1/v2 各持一份主币缓存只调了 v1（`swapList.ClearSwapListCache()`），v2 主币列表停留旧过滤结果直到 600 秒 TTL 兜底且不报错。根因：语义别名让版本信息从名字消失，多版本并存无法从调用处辨识版本。落盘：`package-structure-rules/SKILL.md` 核心边界第 6 条补强制句（导入别名必须与版本目录名对齐 `v1<后缀>`/`v2<后缀>`，禁止语义别名；SKILL 正文是动作前必读位置，拦截力最强）+ `references/lookup-and-reference-contract.md` 新增「版本化目录导入别名对齐（强制）」小节（正例 `v1list`/`v2list`、反例 `swapList`、原因、成对调用要求）；新建 `workbuddy-absorption-map.md` + `references/source-notes.md` 登记。知识库沉淀《版本化目录导入别名对齐.md》（frontmatter 合规、双链正常），与《版本化接口DTO的文件组织与落点》双向关联（文件粒度 vs 导入别名，互补）。验证：quick_validate `Skill is valid!`（exit 0）；同域冗余扫描 4 项 PASS（naming-rules 只约束通用驼峰、本规则归属 package-structure-rules 引用契约，0 重复）。遗留：知识库 8 篇历史笔记缺 frontmatter 未处理；ellipal_finance 侧代码对齐（`swapList`→`v1list` + 补 v2 清理调用）属跨项目只读边界，改动计划已给。改动停在已改动未提交状态。SOP 固化后首轮完整执行（八步闭环验证可用）。短板实锤：SKILL.md 28 行**完全无 frontmatter**（校验器 `No YAML frontmatter found`，D1=1 根因）+ 纯双语宣传壳零流程；脚本 china_free_api.py 30KB/54 命令内容充实被埋没；**宣称与实现不符（重大）**——① 依赖 `clawhub` 框架未安装（"开箱即用"失实）；② 宣称"无密钥"，但 53/54 命令依赖的木小果 API 本机实测不可达（DNS→内网 `172.29.1.188` + TLS 握手失败，baidu/github 对照均 200），仅 wttr.in 可用。市场结论：3 组关键词（free-api/免费api/api工具）0 可吸收候选；同域 apifox-cli/api-contract-rules/cryptocurrency-data-api 均"专用/管理"定位，"免费聚合"互补不重叠。落盘（A+B+D）：脚本去 clawhub 依赖改纯 argparse CLI（886 行、54 命令保留原名 + `--check` 数据源探测/`--list`/`--version`），requirements 仅留 requests，start.sh 透传；SKILL.md 重构 104 行（frontmatter 合规 + 数据源状态表诚实声明 [wttr.in 实测可用/木小果需 --check 探测] + 4 步流程 + 命令速查表 + 适用边界 + 验收清单 + 环境自检 + 交叉引用）；metadata.version→1.1.0。实测：维度 8 全命令 54/56 ok、0 Traceback；修 2 个自引 bug（`_coerce` 手机号误转 int、`self.name` 遮蔽同名方法）；木小果不可达命令优雅降级 `❌ 查询失败`（预期行为）。复评：独立子代理 `1|5|4|4|6|8|4 → 9|9|8|8|9|7|8`（+29.2）；闭环修复 2 处（命令数口径 53/52 → 54/53 与 --list 实测对齐、脚本 10 处「【新增】」历史注释清理），quick_validate 复验 valid 回归无破坏。核心经验：**「依赖未装 + 数据源不可达」是工具类 skill 的隐性失实点，优化方向是「去框架依赖 + 数据源诚实声明 + --check 探测」而非换源重写**；DNS→私有网段 + TLS 失败 = 域名级不可达判据。知识库沉淀追加 1 段（0 死链）。改动停在已改动未提交状态。
- 2026-08-26：**低分 skill 优化 SOP 固化（八轮经验总结 → 吸收进 skill-absorption-rules）**。用户指令「总结经验和步骤，后续评分巡检中低分 skill 都按这个流程优化，经验吸收进吸收 skill 的 skill」。八轮优化闭环（基线核验→市场检索→同域对照→裁决确认→落盘→机器校验→独立复评→闭环修复+沉淀）已稳定复用 8 次、7 个低分 skill 全闭环（+30.4 ~ +41.5）。落盘：`skill-absorption-rules` 新增 `references/low-score-skill-optimization-sop.md`（6306B：触发信号 + 八步闭环表 + 短板类型学 7 类映射 [壳/薄/变现/宣称不符/断链/空洞/违规] + 市场检索规律 [八轮 28+ 组关键词 0 有效候选、解药在仓库内] + 验证纪律 [独立子代理 7 维固定格式/维度 8 本机实测/本侧修正/棘轮/早停] + 实操坑 [尖括号/平台 sed/连续大写 kebab-case/EBUSY/断言笔误/安全策略拦截] + 单轮收口清单 + 边界声明）；SKILL.md 自动触发信号 +1 条 + references 读取规则 +1 条；score-inspection-workflow.md 短板识别节补衔接句——"打分发报告"与"低分优化"上下游闭环。验证：quick_validate `Skill is valid!`（exit 0）；同域冗余扫描 4 项 PASS（SOP vs score-inspection 引用式衔接无重复）；独立子代理覆盖度审查 PASS（对照知识库八轮记录逐节核对：无漏项、无失实，修正 2 处轻微表述 + 补入"复评确定性小问题顺手修复"经验）；知识库沉淀追加 1 段（223 链接 0 死链）；登记 source-notes.md + workbuddy-absorption-map.md。核心结论：低分根因多在"路由缺失"而非"内容少"（内容有、路由无），修复主模式是"内容消化成内联速查/决策表 + 决策路由 + 脚本自定位"；市场检索是低收益动作（八轮 28+ 组关键词 0 候选），同域对照与"让脚本兑现宣称"才是高分杠杆。改动停在已改动未提交状态。
- 2026-08-26：**低分 skill 优化第八轮：vue-component-generator__skillhub（33.4 → 63.8/75，实测全通过）**。短板实锤：SKILL.md 118 行功能宣传 +「变现思路」节（销售模板/企业服务/培训）与功能零关联；**宣称与实现严重不符**——SKILL.md 宣称 `--api/--typescript/--scss/--output` 4 选项，实测脚本仅 22 行只认 `$1` 组件名、其余参数静默忽略，生成空壳模板；无流程/边界/检查点；frontmatter 已合规（八轮中首例无需修 frontmatter）。市场结论：4 组关键词（vue/component/组件/generator）0 个 Vue 组件生成候选，授权安装验证无对象；同域 vue-best-practices/vue__skillhub/vue-router-best-practices 均"规范"定位，生成器定位互补不重叠。落盘：A1 删变现节（短板直接修复）；A2 脚本 22 → 186 行兑现全部宣称参数（--api 三风格/--typescript/--scss/--output/--help/--version/PascalCase 校验/完整 props-emits-样式模板/SCRIPT_DIR 自定位）；A3-A6 SKILL.md 重构（适用边界 + 4 步流程带输入输出 + 能力矩阵 + 3 API 内联模板速查 + 7 项验收清单 + 环境自检 + 交叉引用三兄弟）；D1 metadata.version→1.1.0；D2 环境依赖 bash+sed 附自检。校验器拦截 1 次（description 尖括号 `<script setup>` 违规）→ 改"script setup 语法"。复评：独立子代理 `6|4|3|3|6|5|4 → 9|8|9|8|9|9|8`（+30.4）；维度 8 实测全通过（6 组合生成 + 4 错误分支 exit 1 + kebab-case 转换 + 断言核对）。闭环修复 3 处（SED_I 平台分支 GNU/BSD、连续大写 kebab-case MyAPIClient→my-api-client、补 script-setup 内联模板），顺手补流程输入/输出定义，quick_validate 复验 valid 回归无破坏。同域冗余扫描 PASS。知识库沉淀回读一致（223 链接 0 死链）。改动停在已改动未提交状态。
- 2026-08-26：**低分 skill 优化第七轮：shell__skillhub（31.0 → 69.0/75，实测全通过）**。短板实锤：SKILL.md 111 行纯命令链接壳（9 入口全裸相对路径 `scripts/script.sh <cmd>`），脚本 587 行 8 大模块内容充实被埋没——"内容有、路由无"结构性缺陷再现；frontmatter 6 违规键（author/category/homepage/source/tags/version）校验器实测确认。断链真因：脚本本体实测可执行（10 命令 exit 0），"断链"= 裸相对路径脱离 skill 根失效 + 知识全锁脚本无内联承载。市场结论：6 组关键词（shell/bash/scripting/脚本/linux/terminal/command line）0 个 shell 候选，授权安装验证无对象；同域 `bash__skillhub`（79 行陷阱速查）定位"速查 vs 手册"互补，拒绝合并留档体系审计。落盘：SKILL.md 重构为 4 步工作流（识别场景→查速查→调脚本→分阶段验收）+ 8 大陷阱内联速查（引用/三件套/子壳/数组/参数展开/信号/退出码/工具，全"问题-修复"对）+ script.sh 加 `SCRIPT_DIR` 自定位（+1 行）+ 双调用方式（cd 相对 / 任意 cwd 绝对）+ frontmatter 合规化 + 环境自检（bash 缺失 4 级降级链）+ 交叉引用 bash/linux/powershell + 版本 1.1.0。复评：独立子代理 `7|4|2|2|5|2|5 → 9|9|9|9|10|9|9`（+38.0）；维度 8 实测全通过（10 命令 exit 0 / 子壳陷阱 count=0→2 / `${#arr[@]}`=2 / `${var:-default}`=DEFAULT / 双调用方式均通）。闭环修复 3 处（SCRIPT_DIR 自定位、检查点分写前/写后、bash 缺失降级链），quick_validate 复验 valid。同域冗余扫描 4 项 PASS。知识库沉淀回读一致（223 链接 0 死链）。改动停在已改动未提交状态。
- 2026-08-25：**打通日志使用链路（REQ-LOG-20260825-001，用户确认落盘推进）**。新建 `log-analysis-rules` 作为读日志侧唯一权威（SKILL.md + 5 references：log-file-location / log-level-switching / request-id-traceback / log-fetch-and-filter / debug-window-discipline）；联动四处：`logging-trace-rules` 补可反查稳定标识字段（request-id/trace-id/订单号，纯本地用业务键）、`bug-root-cause-rules` 与 `bug-intake-rules` 查日志取证显式指向读侧、apifox `testing-pitfalls.md` 四层诊断补第 5 步服务端取证（request-id 反查 + 证据回贴测试主文档 + ENV_LOG_BLOCKED 阻断归因）、`test-program-rules` 写接口过程日志从自查项升级为默认放行项（计划冻结可升级硬判）。落盘：需求 `doc/2-需求/2026-08-25_REQ-LOG-20260825-001_日志链路打通.md`（valid:true）+ 实施总览 + 6-review（STYLE: PASS）；字典重跑 seed 92；知识库沉淀 1 篇并更新 INDEX.md；PROJECT_MEMORY 补稳定决策。验证：quick_validate PASS、三份工程文档机器校验 valid:true、语义 grep 全部命中（写侧 4 处 / bug 域 2 处 / 取证 7 处 / 升级 3 处）、全量 400 测试失败 14/错误 13 与改动前基线一致（缺 Go 等既有环境项，无新回归）、knowledge_index 0 死链。改动停在已改动未提交状态。
- 2026-08-23：**实施「任务投影跨宿主适配」修复（BUG-TASK-PROJECTION-HOST-001，用户 /goal 授权并行）**。将任务投影从 Codex 专属硬闸门改造为跨宿主分级适配：① 脚本层 task_plan_projection.py 新增 _resolve_workbuddy_session_id 与三级会话回退链（显式 --session-id > CODEX_THREAD_ID > WorkBuddy 元数据，任意来源冲突/全缺失失败关闭），ensure-start 合成上下文缺 trigger 默认补 start（synthesize 保持严格必填）；② 规则层 task-plan-rehydration-rules SKILL.md 与契约文档跨宿主化（Codex/WorkBuddy/无任务 UI 宿主三档通道 + 互斥不双写），UI_SYNC_BLOCKED 改分级语义——持久化失败/会话冲突/状态不明硬阻断，仅 UI 通道不可用降级继续；③ 上层联动 6 文件（skill-hit-check / autonomous-execution x2 / context-compression / session-handoff / platform-capability-matrix）同步分级语义，PROJECT_MEMORY 三处稳定决策与定义/scope 更新。执行：3 worker 并行（write set 互斥），首次因网关 502 失败，探测恢复后重试成功。验证：单元测试 73/73 OK、quick_validate PASS、实施总览与周期01 文档校验 valid:true、语义 Grep 无绝对化残留、6-review STYLE: PASS。落盘：Bug 主文档 + 实施总览 + 实施周期01 + 测试主文档 + 6-review 记录。改动停在已改动未提交状态。
- 2026-08-22：**「项目根 `skills/` 加载声明」补进 bootstrap 受管章节 + 规则 md**。用户质疑「项目根级 skills/ 目录下的 skill 也会被加载，这个规则 md 中有了吗？同步规则脚本了吗？」——核查确认**没有**：`project-local-skills-rules` 第 26 行规定「命中方式 = 由项目级规则文件（AGENTS.md/CLAUDE.md）显式声明引用 `skills/` 目录」，但该声明从未进入 `bootstrap_agents.sh` 的受管章节模板，其他项目 bootstrap 后规则文件无 skills/ 加载条款，项目本地 skill 无法稳定命中（与 usage_tracking 计数条款缺口同构）。修复：`BODY_SKILL_AUTO` heredoc 新增「### 项目本地 skill 目录（强制）」子节（项目根 `skills/` 下 `project-<slug>-<topic>-rules/` 会被自动加载/扫描、跨工具通用、`~/.workbuddy/skills/` 等工具专属路径非落点规则；会话开始须按声明扫描命中；创建/查重/吸收由 `project-local-skills-rules` 与 `memory-usage-tracking-rules` 管理）；跑 `bootstrap_agents.sh --repo . --target both` 同步根 AGENTS.md + CLAUDE.md（字节一致 49778，双平台无漂移）。验证：临时项目端到端（新建路径含子节 + 重跑幂等 grep -c=1）、bash -n PASS、quick_validate PASS、UTF-8 OK。副作用提示：bootstrap 递归同步了 2 个 skillhub 第三方资产目录的 AGENTS.md（proactive-agent__skillhub/assets、vercel-react-best-practices，设计行为）。改动停在已改动未提交状态。
- 2026-08-22：**bootstrap schema 变更强制检查固化进 `project-rule-file-bootstrap-rules/SKILL.md`**。承接上轮「usage_tracking 三处同步断点」教训（新建路径 `create_project_memory_file` 内嵌模板 / 补齐路径幂等补丁 / 规则文件受管章节 heredoc，端到端真实自举才抓到），用户确认把教训补为规则强制项。SKILL.md 新增「## Schema 变更强制检查（强制）」章节：模板三路联动（新建 + 补齐 + 受管章节及模板索引，缺一即阻断，漏改新建路径是最高频断点）、真实自举兜底（临时项目跑 `bootstrap_agents.sh --repo $TMP --target default` 验证新建与幂等两路径 + `grep -c` 不重复，`bash -n` 不算兜底）、仓库模板回写四件套模板、缺项阻断；「统一执行步骤」追加第 9 条强制引用。验证：quick_validate PASS、UTF-8 OK、frontmatter 完整。改动停在已改动未提交状态。
- 2026-08-22：**项目本地 skill 落点回归项目根 `skills/`**（用户纠正 + git 历史证实）。初版 `project-local-skills-rules`（91357e8）落点即项目根 `skill/`，2b0b251 吸收 skill-autosave 时被"路径适配 WorkBuddy 环境"改为用户级 `~/.workbuddy/skills/` 并新增"勿在项目根另建 skill/"条款；而 `artifact-storage-rules/references/path-map.yaml` 的 `project_local_skills` 一直是 `skill`，两条规则长期矛盾。本次统一：落点 = **项目根目录 `skills/`**（复数，用户拍板），命中由项目级 `AGENTS.md` / `CLAUDE.md` 显式声明引用（不依赖任何工具专属路径）；luode-skills 仓库特例直接落仓库根（仓库根即 skill 资产库）。修正范围：`project-local-skills-rules`（SKILL.md description+5 处落点、dedup-and-update.md 落点节/查重/init 路径、project-skill-template、scope-and-splitting、priority-and-roadmap、agents/openai.yaml）、`artifact-storage-rules`（SKILL.md、path-map.yaml `skill`→`skills` 两处、root-directories、naming-templates、update-policy、skill-integration）、`memory-usage-tracking-rules`（SKILL.md 查重/落点、absorption-trigger 查重/落点、scan_absorption_candidates.py 三处+existing_project_skills 三路查重、source-notes 登记）、字典.md / 编码skill.md / README.md 登记行。验证：3 skill quick_validate 全绿、path-map yaml 解析正确、scan 脚本自测通过（项目根 skills/ + 仓库根特例 + 用户级兼容三路查重）、19 文件 UTF-8 OK、"勿在项目根 / 项目根 `skill/`（单数）/ 写入用户级 skill"全仓清零。改动停在已改动未提交状态。

## 计数锚点区

```yaml
version: 1
anchors:
  - title: "跨项目写入红线改造：绝对禁止 → 默认只读 + 会话级写入授权（用户决策）"
    usage_count: 0
    usage_days: 0
    last_used_at: null
    absorbed_to: null
  - title: "补齐 `doc/` 文档生命周期与退场规则（`artifact-storage-rules` 内部更新通道）"
    usage_count: 0
    usage_days: 0
    last_used_at: null
    absorbed_to: null
  - title: "吸收 EllipalNodeSync 同事 tapd 资产（外部吸收）"
    usage_count: 0
    usage_days: 0
    last_used_at: null
    absorbed_to: null
  - title: "新建 tapd-task-executor skill（用户指令）"
    usage_count: 0
    usage_days: 0
    last_used_at: null
    absorbed_to: null
  - title: "skill-absorption-rules 新增「优化 XX skill」泛化触发模板（内部更新通道）"
    usage_count: 0
    usage_days: 0
    last_used_at: null
    absorbed_to: null
  - title: "tapd-env-bootstrap SKILL.md 路径去用户名化（用户指令）"
    usage_count: 0
    usage_days: 0
    last_used_at: null
    absorbed_to: null
  - title: "新增根级 `cachetask/` 缓存重建任务目录进目录树（内部更新通道）"
    usage_count: 0
    usage_days: 0
    last_used_at: null
    absorbed_to: null
  - title: "字段三件套（NOT NULL + DEFAULT + COMMENT）吸收进 `database-schema-rules`（内部更新通道）"
    usage_count: 0
    usage_days: 0
    last_used_at: null
    absorbed_to: null
  - title: "低分 skill 批量优化第十一轮（9 个，A+B+D 裁决，36.9-49.2 → 61.2-67.5）"
    usage_count: 0
    usage_days: 0
    last_used_at: null
    absorbed_to: null
  - title: "版本化目录导入别名对齐规则吸收进 `package-structure-rules`（代码实测 gap → 内部更新通道）"
    usage_count: 0
    usage_days: 0
    last_used_at: null
    absorbed_to: null
  - title: "低分 skill 优化 SOP 固化（八轮经验总结 → 吸收进 skill-absorption-rules）"
    usage_count: 0
    usage_days: 0
    last_used_at: null
    absorbed_to: null
  - title: "低分 skill 优化第八轮：vue-component-generator__skillhub（33.4 → 63.8/75，实测全通过）"
    usage_count: 0
    usage_days: 0
    last_used_at: null
    absorbed_to: null
  - title: "低分 skill 优化第七轮：shell__skillhub（31.0 → 69.0/75，实测全通过）"
    usage_count: 0
    usage_days: 0
    last_used_at: null
    absorbed_to: null
  - title: "打通日志使用链路（REQ-LOG-20260825-001，用户确认落盘推进）"
    usage_count: 0
    usage_days: 0
    last_used_at: null
    absorbed_to: null
  - title: "实施「任务投影跨宿主适配」修复（BUG-TASK-PROJECTION-HOST-001，用户 /goal 授权并行）"
    usage_count: 0
    usage_days: 0
    last_used_at: null
    absorbed_to: null
  - title: "吸收「调试」（awesome-ai-agent-skills v1.0.0）通用调试方法论进 Bug 域"
    usage_count: 0
    usage_days: 0
    last_used_at: null
    absorbed_to: null
  - title: "「项目根 `skills/` 加载声明」补进 bootstrap 受管章节 + 规则 md"
    usage_count: 0
    usage_days: 0
    last_used_at: null
    absorbed_to: null
  - title: "bootstrap schema 变更强制检查固化进 `project-rule-file-bootstrap-rules/SKILL.md`"
    usage_count: 0
    usage_days: 0
    last_used_at: null
    absorbed_to: null
  - title: "项目本地 skill 落点回归项目根 `skills/`"
    usage_count: 0
    usage_days: 0
    last_used_at: null
    absorbed_to: null
  - title: "完成「记忆使用计数与高频条目自动吸收」机制上线"
    usage_count: 0
    usage_days: 0
    last_used_at: null
    absorbed_to: null
```
