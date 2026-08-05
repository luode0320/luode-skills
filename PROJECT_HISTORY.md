# 项目历史事件

> 本文件追加关键历史事件并只保留最近 20 条（按日期倒序、新事件置顶、追加后自动裁剪）；普通启动默认不读取，只有历史追问、当前状态不足或真实卡点时才窄检索。

## 事件

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
- 2026-08-02：独立后端配置固定在 `config/`，同仓后端配置固定在 `backend/config/`；`yaml/` 使用 `config_<env>.yaml|yml`，Go `embedded/` 使用 `config_<env>.go`，明确 `local/test/prod` 常见环境示例、可扩展环境和 YAML/embedded 可不配对。
- 2026-08-02：`check` 保持只读，`init` 不生成动态环境配置文件；旧式 `config_test_yaml.go` 拒绝，秘密原值不进入提交资产。配置专项 `6/6`、目录 `2/2`、入口 `5/5`、根 Python `209/209`、文档 profile、Python 编译、Skill quick validation、CodeGraph sync 与 `git diff --check` 均通过。
- 2026-08-02：当前会话投影 `REQ-PSR-CONFIG-ENV-001/CYCLE-17` 的五个任务已完成并按 session 精确失活；Obsidian 固定 vault 未注册，本轮未执行 vault 沉淀或 Git 历史写入。
- 2026-08-02：用户确认独立后端 `config/embedded/` 与同仓后端 `backend/config/embedded/` 允许源码直接配置 API key、密钥、密码等私密信息，源码配置为主且默认不依赖环境变量。
- 2026-08-02：YAML 仍禁止秘密原值；允许源码内秘密不扩大到 Agent 输出、日志、README、错误、测试报告或知识库，所有证据继续使用脱敏占位符。
