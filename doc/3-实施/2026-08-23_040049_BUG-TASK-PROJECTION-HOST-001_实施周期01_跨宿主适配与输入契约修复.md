# 实施周期 01：跨宿主适配与输入契约修复

- 对应需求文档：`doc/4-bugs/2026-08-23_040049_任务投影跨宿主适配缺陷.md`
- 来源对象标识：`BUG-TASK-PROJECTION-HOST-001`
- 对应实施总览：`doc/3-实施/2026-08-23_040049_BUG-TASK-PROJECTION-HOST-001_实施总览.md`
- 周期文档命名主干：`2026-08-23_040049_BUG-TASK-PROJECTION-HOST-001_实施周期01_跨宿主适配与输入契约修复`
- 当前周期序号 / 大进度定位：实施周期01 / 第一期（唯一一期）
- 当前周期目标：修复 `ensure-start` 输入契约（缺 `trigger` 默认补 `start`）、扩展会话解析 WorkBuddy 回退链、落地跨宿主分级阻断语义，并完成全量回归与 6-review 收口
- 当前周期只做这一件事：把任务投影从 Codex 专属硬闸门改造为跨宿主分级适配
- 当前周期进入条件：Bug 主文档 + 实施总览已落盘；AC-1~AC-5 冻结；用户已授权并行执行
- 当前周期收口条件：AC-1~AC-5 全部满足；全量单元测试 0 失败；quick_validate 退出码 0；6-review 记录 `STYLE: PASS`
- 当前周期最小任务清单：
  - TASK-RTP-C01-A：ensure-start 合成上下文缺 `trigger` 默认补 `start`（脚本 + 测试）
  - TASK-RTP-C01-B：`resolve_session_id` 扩展 WorkBuddy 会话来源回退（脚本 + 测试）
  - TASK-RTP-C01-C：task-plan-rehydration-rules SKILL.md 与契约文档跨宿主化（规则文档）
  - TASK-RTP-C01-D：5 个上层规则文件同步分级阻断语义（规则文档）
  - TASK-RTP-C01-E：全量回归、quick_validate、6-review 与记忆收口（主线程）
- 当前周期内最小任务执行顺序：A → B → C → D → E（A/B 由 Worker A 顺序闭环，C 由 Worker B，D 由 Worker C，E 由主线程）
- 每个最小任务的闭环状态或计划闭环顺序：

| 任务 | 实施计划完成条件 | 实现 | 真实测试 | 6-review | 负责人 |
| --- | --- | --- | --- | --- | --- |
| TASK-RTP-C01-A | 缺 trigger 默认 start；timeout 仍拒绝；synthesize 严格必填 | Worker A | TEST-1 | 收口阶段 | Worker A |
| TASK-RTP-C01-B | 会话回退链生效；冲突拒绝；全缺失失败 | Worker A | TEST-2 | 收口阶段 | Worker A |
| TASK-RTP-C01-C | 两文档声明跨宿主作用域与分级阻断 | Worker B | TEST-4（免真实测试，理由见任务卡） | 收口阶段 | Worker B |
| TASK-RTP-C01-D | 6 个文件同步分级语义；Grep 无绝对化残留 | Worker C | TEST-4（免真实测试） | 收口阶段 | Worker C |
| TASK-RTP-C01-E | AC-1~AC-5 满足；0 失败；STYLE: PASS | 主线程 | TEST-3/4 | 主线程 | 主线程 |

- 当前周期步骤顺序：
  1. 步骤 1（阶段 1）：Worker A 实现 TASK-RTP-C01-A → 跑 TEST-1 → 实现 TASK-RTP-C01-B → 跑 TEST-2
  2. 步骤 2（阶段 2）：Worker B 实现 TASK-RTP-C01-C（与步骤 1 并行，write set 互斥）
  3. 步骤 3（阶段 3）：Worker C 实现 TASK-RTP-C01-D（与步骤 1/2 并行，write set 互斥）
  4. 步骤 4（阶段 4）：主线程回收三 worker 后执行 TEST-3、TEST-4、6-review 与记忆收口
- 当前周期验证点：
  - 验证点 1（步骤 1 内）：TEST-1、TEST-2 断言通过
  - 验证点 2（步骤 4）：全量测试 0 失败；quick_validate 退出码 0；Grep 无残留绝对化表述
  - 验证点 3（收口）：6-review 记录 `STYLE: PASS`；记忆与日志已更新
- 当前周期阻断项：任一测试失败未定位即阻断对应任务；规则文档口径与冻结口径不一致即阻断该任务
- 本轮是否"补充需求、实施文档"：否（新建实施周期，首次落盘）

## 冻结口径（Worker 必须严格遵守，禁止漂移）

### 口径 1：ensure-start 输入契约

- `ensure-start` 收到合成上下文且缺 `trigger` 时，默认按 `trigger=start` 处理（该入口本身表达"开始"语义）。
- `ensure-start` 显式传入 `trigger=timeout` 仍拒绝（timeout 只属异常修复入口）。
- 直接调用 `synthesize` 命令时保持严格必填（`start|continue|timeout`），不放宽。

### 口径 2：会话解析来源链

优先级固定为：显式 `--session-id` > `CODEX_THREAD_ID` > WorkBuddy 宿主元数据（`CODEBUDDY_MCP_CONFIG` 中 `mcpServers.*.headers["X-WorkBuddy-Session-Id"]` 唯一值，或 `WORKBUDDY_SESSION_ID` 环境变量唯一值）。

- 多来源同时存在且不一致 → 抛 `ProjectionContractError` 失败关闭，不猜测归属。
- 全部缺失 → `required` 语义失败关闭，不写盘、不创建投影。
- WorkBuddy 元数据解析不得打印 `CODEBUDDY_MCP_CONFIG` 全文或 token 原值。

### 口径 3：分级阻断语义（规则层）

| 条件 | 语义 |
| --- | --- |
| 投影持久化失败（原子写失败、超限、UTF-8 损坏） | 硬阻断，原文件不变 |
| 会话归属冲突 / 不确定（多来源不一致、无匹配投影） | 硬阻断，禁止错投 |
| 执行状态不明（进行中步骤无法核验） | 硬阻断，禁止重放未知写操作 |
| 仅 UI 同步通道不可用（`update_plan` 工具缺失/调用失败，但磁盘投影已成功且会话归属明确） | 降级继续：保留磁盘投影 + 继续领域执行 + 下一检查点重试 UI + 如实说明 |
| WorkBuddy 宿主 | UI 通道使用宿主任务列表工具（任务条目协议）；与 Codex `update_plan` 互斥不双写 |
| 无任务 UI 宿主 | 只保留磁盘投影，不伪造 UI 同步成功 |

### 口径 4：作用域声明

- `task-plan-rehydration-rules` 作用域从"Codex Desktop"扩展为"跨宿主（Codex Desktop / WorkBuddy Desktop / 无任务 UI 宿主）"，Codex 专属路径 `CODEX_THREAD_ID + update_plan` 保留为适配层之一。

## 执行附录

- 并行分派：3 个 worker（A/B/C），write set 互斥；主线程负责回收、回归与收口。
- Worker A write set：`task-plan-rehydration-rules/scripts/task_plan_projection.py`、`test/task-plan-rehydration-rules/task_plan_projection_test.py`
- Worker B write set：`task-plan-rehydration-rules/SKILL.md`、`task-plan-rehydration-rules/references/task-plan-projection-contract.md`
- Worker C write set：`skill-hit-check-rules/SKILL.md`、`autonomous-execution-rules/SKILL.md`、`autonomous-execution-rules/references/continuation-and-pause.md`、`context-compression-rules/SKILL.md`、`session-handoff-rules/SKILL.md`、`agent-runtime-recovery-rules/references/platform-capability-matrix.md`
- 测试命令：`python -X utf8 -B test/task-plan-rehydration-rules/task_plan_projection_test.py`
- 校验命令：`python -B .system/skill-creator/scripts/quick_validate.py task-plan-rehydration-rules`
- 语义 Grep：`Grep "UI_SYNC_BLOCKED|禁止继续领域写入|update_plan.*不可用" --glob "**/*.md"`
- 回滚：未提交改动按文件回退（需用户显式授权）；测试临时目录自清理。

## 追踪附录

- 周期内追踪矩阵见实施总览「追踪附录」；本周期为唯一周期，CYCLE 列统一为 `周期01`。
