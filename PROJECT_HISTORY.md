- 2026-08-08：完成运行时 Mock 目录树 Skill 升级（REQ-PSR-MOCK-UPGRADE-001/CYCLE-PSR-MOCK-UPGRADE-001）。新增 `runtime-mock-layout-go.md` 专项契约、backend/fullstack 各 5 类 Mock Catalog 元数据、CLI `check_runtime_mock_structure` 只读检查与正反例测试；package-structure-rules 全量回归 36/36，guide runtime-mock 返回 10 条配方，普通/mock 双构建通过，字典与四份文档 profile 均通过，6-review STYLE: PASS；`F:\binance-wangge-go` adoption 既有 `test/` 遗留快照阻断按计划记录不扩大豁免。改动停在已改动未提交状态。

- 2026-08-08: [package-structure-rules 目录用法入口升级] Schema 扩展 4 字段，Catalog 101 条，guide 子命令，六类 Go recipe，5 契约测试全通过
- 2026-08-08：实施计划落盘：实施总览 IMP-RUNTIME-MOCK-20260808 和周期文档 CYCLE-RUNTIME-MOCK-01 已创建，implementation_overview 与 implementation_cycle profile 均 valid: true。所有 4 个最小任务 TASK-1 至 TASK-4 均已完成闭环。改动停在已改动未提交状态。

- 2026-08-08：需求文档 REQ-PSR-MOCK-UPGRADE-001 的 Mermaid 图前注释修复（图形目的 + 关联 ID），requirement profile 校验 PASS。改动停在已改动未提交状态。

# 项目历史事件

> 本文件追加关键历史事件并只保留最近 20 条（按日期倒序、新事件置顶、追加后自动裁剪）；普通启动默认不读取，只有历史追问、当前状态不足或真实卡点时才窄检索。

## 事件

- 2026-08-10：完成 PROJECT_CURRENT 最近 5 个同项目会话快照功能全量收口（CYCLE-CUR-RECENT-02）。新增快照脚本与契约（周期01），修改 bootstrap 模板、AGENTS.md/CLAUDE.md 触发规则、PROJECT_CURRENT.md 迁移（周期02）；快照 26/26 与 bootstrap 1/1 测试通过，投影 validate 通过，字典刷新退出码 0，周期01/02 文档门禁 PASS，6-review STYLE: PASS；改动停在已改动未提交状态。
- 2026-08-09：完成 `REQ-PSR-CONFIG-SECRET-002 / CYCLE-PSR-24-001` 的规则与测试同步，确立“允许有意持久化凭据、禁止过程性输出回显”口径；未执行 Git 提交或推送。

- 2026-08-09：完成计划输出完整性与跨会话独立执行升级（REQ-PLAN-DETAIL-COMPLETE-002/CYCLE-PD-02）。新增 `cross-session-plan-execution-contract.md`，同步模板、闸门、自审、入口清单与 Agent 提示词的跨会话与 `EXT-*` 契约，修正阶段字段错位与正式字段矩阵；测试资产从 `doc/5-tests/2026-07-26_plan-output/` 迁至根 `test/implementation-planning-rules/` 并扩展到 15 项；落盘需求、实施总览、实施周期、测试 README 与 6-review 五份文档，四档严格 profile 全 PASS；字典生成退出码 0 且与基线一致，`git diff --check` 无错误，临时投影输入已清理；改动停在已改动未提交状态。

- 2026-08-09：完成 Decimal 目录规则收录到 package-structure-rules。Catalog 新增 `backend.utils.decimal` 条目，`utils/decimal/` 加入后端目录树，guide 查询返回 decimalUtil 别名，参考文档（backend-util-layout.md、project-layout-v2.md、directory-usage-routing.md、usage-recipes-go.md）同步更新，guide 专项测试 5/5 通过，全量回归 36 测试 28/28 通过（8 个既有配置 `source_policy` 字段未同步失败与本次无关）。改动停在已改动未提交状态。

- 2026-08-08：完成 REQ-PSR-MOCK-UPGRADE-001 计划完成度复核。补齐 `owner_skill` 统一、fullstack 不扩散与 Schema 必填断言，修复 `package-structure-rules/SKILL.md` guide 示例代码围栏；`runtime_mock_layout_test.py` 5/5、全量回归 36/36、普通/mock 双构建、字典与四份文档 profile 均通过，adoption 仍只报 2 条既有阻断。改动停在已改动未提交状态。

- 2026-08-08：完成运行时 Mock 与测试 Mock 分离规则。根 `mock/` 作为运行时 Mock 唯一合法目录，按被测源码相对路径镜像，`//go:build mock` 构建标签保护。已同步 `test-program-rules`、`artifact-storage-rules`、`test-strategy-rules`、`package-structure-rules` 的 SKILL.md 与 references，Catalog 新增 2 个 mock 条目，人工目录树更新，`AGENTS.md`/`CLAUDE.md` 及 `PROJECT_MEMORY.md` 已同步，新增 `runtime-mock-pattern.md` 参考文档，完整测试覆盖 `13/13` 通过，package-structure-rules 全量回归 `26/26` 通过，根 Python 测试 `287/289` 通过（2 个既有失败与本次无关）。改动停在已改动未提交状态，未执行 Git 历史写入。

- 2026-08-07：修复 Mermaid 生成规则空白点：`reasoning-summary-structure-rules/SKILL.md` 与 `implementation-planning-rules/references/visualization-standard.md` 新增"节点/边/条件标签内比较运算符（`<`、`>`、`<>` 等）必须转义为 `&lt;`/`&gt;` 或替换为文字/符号表达，禁止裸写"的规则；`artifact-delivery-gate-rules/scripts/validate_engineering_docs.py` 的 `check_mermaid_syntax()` 同步新增机械检测（裸露非 `<br/>` 的 `<` 判定为错误，孤立 `>` 不误伤），并在 `test/artifact-delivery-gate-rules/validate_engineering_docs_test.py` 补充正负例；起因是用户贴出的外部 mermaid 片段因裸写 SQL `<>` 导致落盘后无法渲染，本仓库未涉及该外部片段的落盘文件，只做规则+机器闸门层面的预防；本轮改动后跑通该测试文件 59 项用例（含新增 2 项），另 2 项既有失败（`test_missing_section_is_rejected`、`test_requirement_fixture_passes`，均因历史文件 `doc/7-验收/2026-07-12_033322_需求与实施文档极致完备化_验收标准.md` 缺失导致断链）经 `git stash` 交叉验证为改动前既已存在的仓库既有缺陷，不在本次改动范围内；未执行 Git 历史写入。
- 2026-08-06：用户明确配置安全边界：`embedded/` 是同一环境的主来源，`yaml/` 仅作回退来源；YAML 禁止秘密原值，embedded 允许源码私密值。已同步 Catalog、Schema、reference、Skill、活动测试、测试 README、`6-review` 与项目四件套；配置专项 `11/11`、目录回归 `26/26`、test/style 文档 profile 和差异检查通过，未执行 Git 历史写入。
- 2026-08-06：协同完成 Binance CYCLE-11 环境来源识别契约；`package-structure-rules` 的 loader Catalog、Schema、reference 与配置专项测试同步 `-env > APP_ENV > ENV > local`，11/11 通过，未执行 Git 历史写入。
- 2026-08-05：Obsidian 知识库从只增量补充改为可迭代更新：写入前必须判定补充、矛盾未裁决或取代三态，判为取代按剩余价值分三档处置旧笔记（标记取代 / 归档到 90-Archive / 删除进回收站），接替关系双向写入；bridge 白名单从 8 个扩到 16 个，新增读属性、读整篇属性、写属性、移动、删除、反向链接、枚举文件、枚举孤儿；三类写操作各带回读验证，delete 固定进回收站，执行案例目录禁止 move/delete；新增只读巡检脚本；契约测试 40 项、总结契约 20 项全绿；六份研发文档 profile 全部 PASS；`6-review STYLE: PASS`；顺带修复 bridge stdout 编码与机器索引区一处既有缩进缺陷；未批量清理现存孤儿笔记，未执行 Git 历史写入。
- 2026-08-05：完成 CYCLE-PSR-23 config 根加载与结构文件规则。独立后端 `config/load.<ext>` 与 `config/model.<ext>`（同仓后端 `backend/config/...`）成为唯一配置加载/结构落点，Catalog 新增 4 个 pattern 条目并补 Schema 守卫，CLI strict 对 config/ 根两个命名放行、其余拒绝；专项测试 `11/11`、四文件回归 `26/26`、需求/实施/测试/风格四份文档 profile 与 Skill 合规门禁均通过，工作树保持已改动未提交。
- 2026-08-05：最终总结新增条件小节「知识引用」，用「本轮引用」与「本轮沉淀」两张表逐条列出本轮读过与写过的 Obsidian 笔记；原先「方案与根因」和「结果与结论」的两处单行摘要口径作废。
- 2026-08-05：`obsidian-knowledge-flow` 新增引用台账契约：每次 read/create/append 返回 verified=true 后立即登记六字段，只有真实 read 成功的笔记可入引用表，笔记名禁用 CLI 回显文本。
- 2026-08-05：契约测试 20 项全绿、字典刷新退出码 0、四份研发文档 profile 全部 PASS、`6-review STYLE: PASS`；固定 vault 已恢复可用，实机 read 与 create 均 verified=true。
