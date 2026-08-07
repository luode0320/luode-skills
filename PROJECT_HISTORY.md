- 2026-08-08：实施计划落盘：实施总览 IMP-RUNTIME-MOCK-20260808 和周期文档 CYCLE-RUNTIME-MOCK-01 已创建，implementation_overview 与 implementation_cycle profile 均 alid: true。所有 6 个最小任务 T01-T06 均已完成闭环。改动停在已改动未提交状态。

- 2026-08-08：需求文档 REQ-RUNTIME-MOCK-20260808-01 的 Mermaid 图前注释修复（图形目的 + 关联 ID），requirement profile 校验 PASS。改动停在已改动未提交状态。

# 项目历史事件

> 本文件追加关键历史事件并只保留最近 20 条（按日期倒序、新事件置顶、追加后自动裁剪）；普通启动默认不读取，只有历史追问、当前状态不足或真实卡点时才窄检索。

## 事件

- 2026-08-08：完成运行时 Mock 与测试 Mock 分离规则。根 `mock/` 作为运行时 Mock 唯一合法目录，按被测源码相对路径镜像，`//go:build mock` 构建标签保护。已同步 `test-program-rules`、`artifact-storage-rules`、`test-strategy-rules`、`package-structure-rules` 的 SKILL.md 与 references，Catalog 新增 2 个 mock 条目，人工目录树更新，`AGENTS.md`/`CLAUDE.md` 及 `PROJECT_MEMORY.md` 已同步，新增 `runtime-mock-pattern.md` 参考文档，完整测试覆盖 `13/13` 通过，package-structure-rules 全量回归 `26/26` 通过，根 Python 测试 `287/289` 通过（2 个既有失败与本次无关）。改动停在已改动未提交状态，未执行 Git 历史写入。

- 2026-08-06：用户明确配置安全边界：`embedded/` 是同一环境的主来源，`yaml/` 仅作回退来源；YAML 禁止秘密原值，embedded 允许源码私密值。已同步 Catalog、Schema、reference、Skill、活动测试、测试 README、`6-review` 与项目四件套；配置专项 `11/11`、目录回归 `26/26`、test/style 文档 profile 和差异检查通过，未执行 Git 历史写入。
- 2026-08-06：协同完成 Binance CYCLE-11 环境来源识别契约；`package-structure-rules` 的 loader Catalog、Schema、reference 与配置专项测试同步 `-env > APP_ENV > ENV > local`，11/11 通过，未执行 Git 历史写入。
- 2026-08-05：Obsidian 知识库从只增量补充改为可迭代更新：写入前必须判定补充、矛盾未裁决或取代三态，判为取代按剩余价值分三档处置旧笔记（标记取代 / 归档到 90-Archive / 删除进回收站），接替关系双向写入；bridge 白名单从 8 个扩到 16 个，新增读属性、读整篇属性、写属性、移动、删除、反向链接、枚举文件、枚举孤儿；三类写操作各带回读验证，delete 固定进回收站，执行案例目录禁止 move/delete；新增只读巡检脚本；契约测试 40 项、总结契约 20 项全绿；六份研发文档 profile 全部 PASS；`6-review STYLE: PASS`；顺带修复 bridge stdout 编码与机器索引区一处既有缩进缺陷；未批量清理现存孤儿笔记，未执行 Git 历史写入。
- 2026-08-05：完成 CYCLE-PSR-23 config 根加载与结构文件规则。独立后端 `config/load.<ext>` 与 `config/model.<ext>`（同仓后端 `backend/config/...`）成为唯一配置加载/结构落点，Catalog 新增 4 个 pattern 条目并补 Schema 守卫，CLI strict 对 config/ 根两个命名放行、其余拒绝；专项测试 `11/11`、四文件回归 `26/26`、需求/实施/测试/风格四份文档 profile 与 Skill 合规门禁均通过，工作树保持已改动未提交。
- 2026-08-05：最终总结新增条件小节「知识引用」，用「本轮引用」与「本轮沉淀」两张表逐条列出本轮读过与写过的 Obsidian 笔记；原先「方案与根因」和「结果与结论」的两处单行摘要口径作废。
- 2026-08-05：`obsidian-knowledge-flow` 新增引用台账契约：每次 read/create/append 返回 verified=true 后立即登记六字段，只有真实 read 成功的笔记可入引用表，笔记名禁用 CLI 回显文本。
- 2026-08-05：契约测试 20 项全绿、字典刷新退出码 0、四份研发文档 profile 全部 PASS、`6-review STYLE: PASS`；固定 vault 已恢复可用，实机 read 与 create 均 verified=true。
- 2026-08-05：本周期未改桥接脚本与笔记字段定义，未执行 Git 历史写入；根测试启动器与两个既有测试的失败已用干净基线复跑证明与本轮无关。
- 2026-08-04：用户确认独立后端项目关联工具统一落在 `common/util/`，与根 `utils/<package>/` 的项目无关工具包职责分离；已同步 `package-structure-rules` 的目录树、Catalog、Schema、CLI、相邻 `common-util-rules` 和活动测试，旧源码根 `util/` 保留为 adoption legacy 迁移边界，当前改动未提交。
- 2026-08-03：已新增 `REQ-PSR-CONFIG-SECRET-001`、CYCLE-19、Catalog/Schema 策略字段和专项断言；本轮未执行 Git 历史写入，未连接外部服务。
- 2026-08-03：独立后端 `config/embedded/` 与同仓后端 `backend/config/embedded/` 已明确允许源码直接配置私密值，源码优先且默认不依赖环境变量；YAML 与外部输出继续禁止秘密原值。
- 2026-08-03：配置专项 `7/7`、package-structure-rules 子目录回归 `16/16`、根 `test/` 子目录逐项回归 `212/212`、五类工程文档 profile、Skill quick validation、Python 编译和 `git diff --check` 均通过。
- 2026-08-03：CYCLE-19 需求、实施、测试、`6-review` 与项目记忆已完成脱敏收口；未连接外部服务、未执行 Git 历史写入，Obsidian 固定 vault 未注册。
- 2026-08-03：fullstack、backend、frontend 的活动测试代码统一落在项目根 `test/`；独立后端不建立 `backend/test/`，前后端同仓不建立 `backend/test/` 或 `frontend/test/`；`doc/5-tests/` 继续只保存说明和非可执行证据。
- 2026-08-03：Catalog、人工目录树、skeleton、query、render、init 和根目录契约测试已同步；根目录专项 `4/4`、入口回归 `5/5`、配置回归 `7/7`、根 Python 测试 `212/212`、测试 README profile、Skill 校验和 `6-review STYLE: PASS` 均通过。
- 2026-08-03：本周期未迁移真实项目、未连接外部服务、未执行 Git 历史写入；Obsidian 固定 vault 未注册，沉淀按 bridge 规则阻断。
- 2026-08-02：最终收口复验：实施总览、实施周期和 `6-review` profile 均返回 `valid: true`，根 Python 测试 `203/203` 通过，`git diff --check` 无错误；当前会话投影随后按 session 精确失活，未执行 Git 历史写入。
- 2026-08-02：继续回合复核发现 CYCLE-16 周期文档和项目当前状态残留旧的 `in_progress/pending/待执行` 文案；已按现有验证证据同步为 `accepted/completed`，未扩大用户范围或执行 Git 历史写入。
