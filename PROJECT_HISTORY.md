# 项目历史事件

> 本文件追加关键历史事件并只保留最近 20 条（按日期倒序、新事件置顶、追加后自动裁剪）；普通启动默认不读取，只有历史追问、当前状态不足或真实卡点时才窄检索。

## 事件

- 2026-08-12：完成知识库死链闸门与落点瘦身（IMP-KB-DEADLINK-20260812）。第五轮检查发现一类比零使用更有害的形态：「规则声明了但落点从未创建」——布局规则目录树声明 9 个目录，`00-Inbox`、`10-Sessions`、`40-Entities`、`Attachments`、`Templates` 五个从未创建过，而落点规则给每一个都写了明确用途。它不只是机制空转，还会主动诱导写入者产出坏数据：规则要求实体建 `40-Entities/` 笔记，写入者照做写下 `[[实体名]]`，目录不存在，8 处链接指向空气。同源问题还有 `type` 枚举声明 6 类实际只用 3 类，多出的三类正对应那三个不存在的落点。连带查出全库 160 条双链里有 18 处死链（11%）长期零告警——已建成的四类机器校验（头部契约、接替关系、孤儿、冲突归组）唯独漏了双链有效性，而双链是这套知识库的核心导航机制。修法：删五个落点规则并把实体导航交给上一轮建的两张项目地图 MOC；`type` 枚举收窄、`entities` 契约由 wikilink 改纯文本；18 处死链按五类清零；`check` 新增 `check_dead_links()` 作第四类校验，并把别名解析抽成 `build_alias_map()` 供接替校验共用（删掉内联的第二份实现）。关键细节：检测器必须排除围栏代码块与行内代码——上一轮口头判断「无新增死链」时，实际是自己写的一处双链格式示例造成误报，人工判断根本没发现。用注入探针验证闸门真会失败（注入不合规、清理后恢复合规），已检双链 147 条与全库 148 条的差额恰是被正确剔除的那处示例。结果：死链 18→0 处、布局声明 9→4 个目录，99 项测试全绿，6-review `STYLE: PASS`。沉淀 1 篇补充（模式四：诱导型零使用；判断规则去留要同时问「有没有被执行」和「照它执行会不会产出坏结果」）。改动停在已改动未提交状态。

- 2026-08-12：完成知识库 iterate 环节激活（IMP-KB-ITERATE-20260812）。第四轮检查把重心从「要不要沉淀」移到「沉淀之后」，实测确认 `iterate`（三态判定 → 分级处置 → 双向接替）自知识库建立至今零执行：全库 status 为 58 active + 3 test-fixture + 3 candidate，`supersedes`/`superseded_by` 全库出现 0 次，5 组冲突候选长期无人裁决。这是继 `bridge_candidate`、`project-rules/` 之后的第四个零使用机制，病根同为「触发条件是主观描述、漏做不报错」。连带查出巡检默认只扫 `20-Knowledge`（42/63）而 `SKILL.md` 给的命令不带 `--all`，导致上一轮「孤儿 0 篇」结论失真（全库实际 5 篇）；以及 `90-Archive/` 被 check 整体豁免，3 篇非法状态 `test-fixture` 与 2 篇无 frontmatter 长期零告警。修法：三态判定改硬信号并规定巡检强制触发时机；`check` 补齐 `note-schema` 已声明未实现的双向接替与状态互斥校验；巡检默认改全库并加导航笔记、已双向关联两类归组豁免；5 组存量逐组读正文裁决全判「补充」并补齐双向关联；删除 5 篇 obsidian CLI 桥接时代夹具，状态值合法性校验收窄为对全库生效。过程中靠真跑连出两个静默缺陷——判「补充」不留机器可识别痕迹会让同一组每轮重报，以及 `- "[[目标]]"` 写法漏剥 YAML 引号让痕迹判定失效。结果：冲突候选 6→0 组、孤儿 5→0 篇、非当前有效状态 3→0 篇、不可读 2→0 篇，94 项测试全绿，6-review `STYLE: PASS`。沉淀 1 篇补充（机制零使用的深层原因是非正式替代路径成本更低）。改动停在已改动未提交状态。

- 2026-08-12：完成知识库分层边界与流水清理（IMP-KB-LAYERING-20260812）。第三轮检查发现三个上轮未覆盖的问题：ⓐ 跨项目知识双写——`bridge_candidate` 标记零使用、`project-rules/` 落点从未创建，通用判据全堆在 175KB 的 `PROJECT_MEMORY.md`（启动必读）；ⓑ「变更记录」75 条日期流水占 19KB，违反本文件「不承载历史流水」职责且无裁剪；ⓒ 孤儿笔记 45%。修法：`project-memory-sync.md` 的四条主观测试改为硬信号加排除清单，并新增「判定通过后必须抽象化改写、项目记忆只留指针」硬要求；四处通用判据迁往知识库（其中「共用定义放被依赖方」原无承接，先抽象化新建 `规则与共用定义的落点决定其有效性` 再迁）；变更记录逐条核对现行口径已被 skill 与 `AGENTS.md` 承接后清空并加保留上限，同时把上限写进 `project-memory-rules`；`PROJECT_HISTORY.md` 结构重组（5 条错位条目归位、按日期倒序、裁剪到 20 条上限）；新建 2 张项目地图与 3 组双向链接，孤儿率 45%→0%。项目记忆人类区 84984→61314 字节（降 27%）。81 项测试全绿，6-review `STYLE: PASS`。机器索引区 90KB 明确未动。改动停在已改动未提交状态。

- 2026-08-12：完成知识库沉淀侧优化（IMP-KB-CAPTURE-20260812）。实测推翻上一轮「沉淀侧尚可」的判断，定位三个「漏做不报错」的缺陷：① 沉淀触发是主观描述，速率断崖（38 篇/12 天 → 6 篇/25 天，同期 6 个大任务未沉淀）；② 头部契约无机器强制（必填字段填充率 70%~82%、三套 schema 并存、状态枚举漂移 2 个值）；③ 冲突检测信噪比极低（8 组 30 对几乎全误报），并因此让取代/分级处置机制零使用（接替字段 0 处）。修法：沉淀触发改六条硬信号加四条排除项且只要求写明依据；新增 `knowledge_index.py check` 校验必填字段与状态枚举（不合规返回非零退出码，归档区豁免），补齐 12 篇存量并归一三套 schema，违规 15→0；归组条件收紧为「同主题且共享标签≥2 或标题相似达阈值」，候选 30→6 对且全为真候选，降噪 80%；主题推导下移到巡检脚本供索引单向复用。过程中修出 BOM 让头部契约校验本身失真、以及补齐脚本混淆「补缺失」与「覆盖分叉值」两个隐蔽缺陷。新增 13 项断言，6 个测试文件共 81 项全绿，6-review `STYLE: PASS`，沉淀 1 篇姊妹笔记并与检索篇双向链接。改动停在已改动未提交状态。

- 2026-08-12：完成知识库检索准召优化（IMP-KB-RETRIEVAL-20260812）。定位到检索侧真实缺陷：手写 `INDEX.md` 只覆盖 34%（21/61）、`30-MOCs` 全部 11 篇是历史 blog 导入且零覆盖活跃主题、孤儿笔记占 46%，检索实际退化成靠猜关键词全文扫描；根因是落点规则里 `20-Knowledge/topic/` 的 `topic` 为自由变量，长出 17 个目录含 4 对语义重复，同一主题散落 5 处。修法：主题收敛为 7 个固定中文主题 + 3 个契约固定落点（英文例外），搬迁 32 篇并同轮改写 39 处带路径 wikilink，死链 0 新增；新增 `knowledge_index.py` 生成 `_index.json` 机器索引与 `query` 入口，覆盖率 34%→100%，索引过期自动重建。过程中实测暴露并修复两个静默降低召回的缺陷：纯 frontmatter 索引漏检「正文讲了但标签没写」的笔记（查「代码风格」2 篇 vs 全文 4 篇），以及 `parse_list_field` 对无引号行内数组解析失败导致别名整段丢失。新增 13 项索引契约测试与 3 项主题合规断言（阻断新造目录），6 个测试文件共 69 项全绿，6-review `STYLE: PASS`，字典 diff 仅时间戳。沉淀流程本轮未动。改动停在已改动未提交状态。

- 2026-08-12：完成 agents 配置行尾 CRLF 违规修复与全仓库常驻回归扩面（STYLE-AGENTS-EOL-LF-001）。8 份 `agents/openai.yaml`（5 份在 `.system/` 下、被 `.gitignore` 忽略但本机真实生效）从 CRLF 还原为 LF，用 `read_bytes`/`write_bytes` 二进制替换避开 Windows 上 `write_text` 把 LF 转回 CRLF 的坑；控制字符扫描为空，未复现历史 `\x07` 问题，8 份全部 `yaml.safe_load` 通过，6 份已跟踪文件 `git diff --numstat` 为空反证只改行尾。新增 `test/shared/asset_eol_health_test.py`（4 用例），把行尾断言扩到全仓库 `.sh`/`.bash`/`.yaml`/`.yml`、把可解析性与控制字符断言扩到全仓库 `agents/` 配置，并加"扫描范围非空"防空跑断言；经 CRLF 探针注入验证确会 FAIL、清理后 PASS。仓库既有 4 个测试失败已用移除新增文件后复跑交叉验证为无关。`doc/5-tests/` 下 3 份 CRLF yaml 属只读历史归档且受指纹基线锁定，明确排除不改。6-review STYLE: PASS，style_regression profile 校验 valid: true。因 `PROJECT_CURRENT.md` 已达 51,006 字节（上限 51,200）且其内容属另一进行中任务的交接，本轮未覆盖写入当前状态。改动停在已改动未提交状态。

- 2026-08-12：完成知识库嵌套目录合并与路径前缀根因修复。定位到 `知识库/` 前缀叠加是 `D:\谷歌云盘\知识库\知识库\` 嵌套目录的根因（根已是 `知识库`，规则却仍要求路径带 `知识库/` 前缀），笔记路径基准统一改为相对知识库根的裸相对路径；嵌套层 1 篇实质笔记合并回 `20-Knowledge/研发流程/`，删除 4 篇已作废 Obsidian CLI 笔记与 Obsidian 默认欢迎页，2 处散落文件归位，INDEX.md 死链与过期措辞清理，笔记总数 65→59 且全库 wikilink 无新增死链。同时补完上个会话遗留的迁移收口：9 个联动 skill 共 23 文件、`AGENTS.md`/`CLAUDE.md`/`bootstrap_agents.sh` 三者逐字一致、记忆四件套、状态字段 `Obsidian:` → `知识库:`。改动停在已改动未提交状态。

- 2026-08-11：完成目录树规范语义纠偏（CYCLE-TREE-OPEN-EXT-01）。package-structure-rules 与 micro-business-architecture-rules 共 9 个文件的封闭枚举改为开集表述，project-layout-v2.md 新增「统一规范目录与扩展目录」统一定义；grep 封闭枚举残留为空，字典 diff 仅时间戳，UTF-8 无乱码；改动停在已改动未提交状态。

- 2026-08-11：完成 doc/4-bugs 与 doc/5-tests 文档扁平化（REQ-FLATDOC-20260811-001）。Bug 主文档改为 `doc/4-bugs/YYYY-MM-DD_HHmmss_问题中文简介.md`，测试主文档改为 `doc/5-tests/YYYY-MM-DD_HHmmss_<测试任务中文主题>.md` 且证据内联，取消 evidence/artifacts 子目录；`doc/5-tests/基线/` 登记为唯一豁免，上线接口测试机器产物移到 `test/release-artifacts/`；历史子目录一律只读保留不迁移。path-map.yaml v8→v9，共改 83 个文件，新增 8 个活动测试全通过，全量回归无新增失败，6-review STYLE: PASS。改动停在已改动未提交状态。

- 2026-08-10：完成 PROJECT_CURRENT 最近 5 个同项目会话快照功能全量收口（CYCLE-CUR-RECENT-02）。新增快照脚本与契约（周期01），修改 bootstrap 模板、AGENTS.md/CLAUDE.md 触发规则、PROJECT_CURRENT.md 迁移（周期02）；快照 26/26 与 bootstrap 1/1 测试通过，投影 validate 通过，字典刷新退出码 0，周期01/02 文档门禁 PASS，6-review STYLE: PASS；改动停在已改动未提交状态。

- 2026-08-09：完成 `REQ-PSR-CONFIG-SECRET-002 / CYCLE-PSR-24-001` 的规则与测试同步，确立“允许有意持久化凭据、禁止过程性输出回显”口径；未执行 Git 提交或推送。

- 2026-08-09：完成计划输出完整性与跨会话独立执行升级（REQ-PLAN-DETAIL-COMPLETE-002/CYCLE-PD-02）。新增 `cross-session-plan-execution-contract.md`，同步模板、闸门、自审、入口清单与 Agent 提示词的跨会话与 `EXT-*` 契约，修正阶段字段错位与正式字段矩阵；测试资产从 `doc/5-tests/2026-07-26_plan-output/` 迁至根 `test/implementation-planning-rules/` 并扩展到 15 项；落盘需求、实施总览、实施周期、测试 README 与 6-review 五份文档，四档严格 profile 全 PASS；字典生成退出码 0 且与基线一致，`git diff --check` 无错误，临时投影输入已清理；改动停在已改动未提交状态。

- 2026-08-09：完成 Decimal 目录规则收录到 package-structure-rules。Catalog 新增 `backend.utils.decimal` 条目，`utils/decimal/` 加入后端目录树，guide 查询返回 decimalUtil 别名，参考文档（backend-util-layout.md、project-layout-v2.md、directory-usage-routing.md、usage-recipes-go.md）同步更新，guide 专项测试 5/5 通过，全量回归 36 测试 28/28 通过（8 个既有配置 `source_policy` 字段未同步失败与本次无关）。改动停在已改动未提交状态。

- 2026-08-08：完成运行时 Mock 目录树 Skill 升级（REQ-PSR-MOCK-UPGRADE-001/CYCLE-PSR-MOCK-UPGRADE-001）。新增 `runtime-mock-layout-go.md` 专项契约、backend/fullstack 各 5 类 Mock Catalog 元数据、CLI `check_runtime_mock_structure` 只读检查与正反例测试；package-structure-rules 全量回归 36/36，guide runtime-mock 返回 10 条配方，普通/mock 双构建通过，字典与四份文档 profile 均通过，6-review STYLE: PASS；`F:\binance-wangge-go` adoption 既有 `test/` 遗留快照阻断按计划记录不扩大豁免。改动停在已改动未提交状态。

- 2026-08-08: [package-structure-rules 目录用法入口升级] Schema 扩展 4 字段，Catalog 101 条，guide 子命令，六类 Go recipe，5 契约测试全通过

- 2026-08-08：实施计划落盘：实施总览 IMP-RUNTIME-MOCK-20260808 和周期文档 CYCLE-RUNTIME-MOCK-01 已创建，implementation_overview 与 implementation_cycle profile 均 valid: true。所有 4 个最小任务 TASK-1 至 TASK-4 均已完成闭环。改动停在已改动未提交状态。

- 2026-08-08：需求文档 REQ-PSR-MOCK-UPGRADE-001 的 Mermaid 图前注释修复（图形目的 + 关联 ID），requirement profile 校验 PASS。改动停在已改动未提交状态。

- 2026-08-08：完成 REQ-PSR-MOCK-UPGRADE-001 计划完成度复核。补齐 `owner_skill` 统一、fullstack 不扩散与 Schema 必填断言，修复 `package-structure-rules/SKILL.md` guide 示例代码围栏；`runtime_mock_layout_test.py` 5/5、全量回归 36/36、普通/mock 双构建、字典与四份文档 profile 均通过，adoption 仍只报 2 条既有阻断。改动停在已改动未提交状态。

- 2026-08-08：完成运行时 Mock 与测试 Mock 分离规则。根 `mock/` 作为运行时 Mock 唯一合法目录，按被测源码相对路径镜像，`//go:build mock` 构建标签保护。已同步 `test-program-rules`、`artifact-storage-rules`、`test-strategy-rules`、`package-structure-rules` 的 SKILL.md 与 references，Catalog 新增 2 个 mock 条目，人工目录树更新，`AGENTS.md`/`CLAUDE.md` 及 `PROJECT_MEMORY.md` 已同步，新增 `runtime-mock-pattern.md` 参考文档，完整测试覆盖 `13/13` 通过，package-structure-rules 全量回归 `26/26` 通过，根 Python 测试 `287/289` 通过（2 个既有失败与本次无关）。改动停在已改动未提交状态，未执行 Git 历史写入。

- 2026-08-07：修复 Mermaid 生成规则空白点：`reasoning-summary-structure-rules/SKILL.md` 与 `implementation-planning-rules/references/visualization-standard.md` 新增"节点/边/条件标签内比较运算符（`<`、`>`、`<>` 等）必须转义为 `&lt;`/`&gt;` 或替换为文字/符号表达，禁止裸写"的规则；`artifact-delivery-gate-rules/scripts/validate_engineering_docs.py` 的 `check_mermaid_syntax()` 同步新增机械检测（裸露非 `<br/>` 的 `<` 判定为错误，孤立 `>` 不误伤），并在 `test/artifact-delivery-gate-rules/validate_engineering_docs_test.py` 补充正负例；起因是用户贴出的外部 mermaid 片段因裸写 SQL `<>` 导致落盘后无法渲染，本仓库未涉及该外部片段的落盘文件，只做规则+机器闸门层面的预防；本轮改动后跑通该测试文件 59 项用例（含新增 2 项），另 2 项既有失败（`test_missing_section_is_rejected`、`test_requirement_fixture_passes`，均因历史文件 `doc/7-验收/2026-07-12_033322_需求与实施文档极致完备化_验收标准.md` 缺失导致断链）经 `git stash` 交叉验证为改动前既已存在的仓库既有缺陷，不在本次改动范围内；未执行 Git 历史写入。
