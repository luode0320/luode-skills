- 2026-08-08：完成运行时 Mock 目录树 Skill 升级（REQ-PSR-MOCK-UPGRADE-001/CYCLE-PSR-MOCK-UPGRADE-001）。新增 `runtime-mock-layout-go.md` 专项契约、backend/fullstack 各 5 类 Mock Catalog 元数据、CLI `check_runtime_mock_structure` 只读检查与正反例测试；package-structure-rules 全量回归 36/36，guide runtime-mock 返回 10 条配方，普通/mock 双构建通过，字典与四份文档 profile 均通过，6-review STYLE: PASS；`F:\binance-wangge-go` adoption 既有 `test/` 遗留快照阻断按计划记录不扩大豁免。改动停在已改动未提交状态。

- 2026-08-08: [package-structure-rules 目录用法入口升级] Schema 扩展 4 字段，Catalog 101 条，guide 子命令，六类 Go recipe，5 契约测试全通过
- 2026-08-08：实施计划落盘：实施总览 IMP-RUNTIME-MOCK-20260808 和周期文档 CYCLE-RUNTIME-MOCK-01 已创建，implementation_overview 与 implementation_cycle profile 均 valid: true。所有 4 个最小任务 TASK-1 至 TASK-4 均已完成闭环。改动停在已改动未提交状态。

- 2026-08-08：需求文档 REQ-PSR-MOCK-UPGRADE-001 的 Mermaid 图前注释修复（图形目的 + 关联 ID），requirement profile 校验 PASS。改动停在已改动未提交状态。

# 项目历史事件

> 本文件追加关键历史事件并只保留最近 20 条（按日期倒序、新事件置顶、追加后自动裁剪）；普通启动默认不读取，只有历史追问、当前状态不足或真实卡点时才窄检索。

## 事件

- 2026-08-08：完成 REQ-PSR-MOCK-UPGRADE-001 计划完成度复核。补齐 `owner_skill` 统一、fullstack 不扩散与 Schema 必填断言，修复 `package-structure-rules/SKILL.md` guide 示例代码围栏；`runtime_mock_layout_test.py` 5/5、全量回归 36/36、普通/mock 双构建、字典与四份文档 profile 均通过，adoption 仍只报 2 条既有阻断。改动停在已改动未提交状态。

- 2026-08-08：完成运行时 Mock 与测试 Mock 分离规则。根 `mock/` 作为运行时 Mock 唯一合法目录，按被测源码相对路径镜像，`//go:build mock` 构建标签保护。已同步 `test-program-rules`、`artifact-storage-rules`、`test-strategy-rules`、`package-structure-rules` 的 SKILL.md 与 references，Catalog 新增 2 个 mock 条目，人工目录树更新，`AGENTS.md`/`CLAUDE.md` 及 `PROJECT_MEMORY.md` 已同步，新增 `runtime-mock-pattern.md` 参考文档，完整测试覆盖 `13/13` 通过，package-structure-rules 全量回归 `26/26` 通过，根 Python 测试 `287/289` 通过（2 个既有失败与本次无关）。改动停在已改动未提交状态，未执行 Git 历史写入。

- 2026-08-06：用户明确配置安全边界：`embedded/` 是同一环境的主来源，`yaml/` 仅作回退来源；YAML 禁止秘密原值，embedded 允许源码私密值。已同步 Catalog、Schema、reference、Skill、活动测试、测试 README、`6-review` 与项目四件套；配置专项 `11/11`、目录回归 `26/26`、test/style 文档 profile 和差异检查通过，未执行 Git 历史写入。
- 2026-08-06：协同完成 Binance CYCLE-11 环境来源识别契约；`package-structure-rules` 的 loader Catalog、Schema、reference 与配置专项测试同步 `-env > APP_ENV > ENV > local`，11/11 通过，未执行 Git 历史写入。
- 2026-08-05：Obsidian 知识库从只增量补充改为可迭代更新：写入前必须判定补充、矛盾未裁决或取代三态，判为取代按剩余价值分三档处置旧笔记（标记取代 / 归档到 90-Archive / 删除进回收站），接替关系双向写入；bridge 白名单从 8 个扩到 16 个，新增读属性、读整篇属性、写属性、移动、删除、反向链接、枚举文件、枚举孤儿；三类写操作各带回读验证，delete 固定进回收站，执行案例目录禁止 move/delete；新增只读巡检脚本；契约测试 40 项、总结契约 20 项全绿；六份研发文档 profile 全部 PASS；`6-review STYLE: PASS`；顺带修复 bridge stdout 编码与机器索引区一处既有缩进缺陷；未批量清理现存孤儿笔记，未执行 Git 历史写入。
- 2026-08-05：完成 CYCLE-PSR-23 config 根加载与结构文件规则。独立后端 `config/load.<ext>` 与 `config/model.<ext>`（同仓后端 `backend/config/...`）成为唯一配置加载/结构落点，Catalog 新增 4 个 pattern 条目并补 Schema 守卫，CLI strict 对 config/ 根两个命名放行、其余拒绝；专项测试 `11/11`、四文件回归 `26/26`、需求/实施/测试/风格四份文档 profile 与 Skill 合规门禁均通过，工作树保持已改动未提交。
- 2026-08-05：最终总结新增条件小节「知识引用」，用「本轮引用」与「本轮沉淀」两张表逐条列出本轮读过与写过的 Obsidian 笔记；原先「方案与根因」和「结果与结论」的两处单行摘要口径作废。
- 2026-08-05：`obsidian-knowledge-flow` 新增引用台账契约：每次 read/create/append 返回 verified=true 后立即登记六字段，只有真实 read 成功的笔记可入引用表，笔记名禁用 CLI 回显文本。
- 2026-08-05：契约测试 20 项全绿、字典刷新退出码 0、四份研发文档 profile 全部 PASS、`6-review STYLE: PASS`；固定 vault 已恢复可用，实机 read 与 create 均 verified=true。
