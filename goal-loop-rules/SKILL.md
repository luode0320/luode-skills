---
name: goal-loop-rules
description: 目标方法论与工程循环控制的统一入口。当用户需要设定个人或职业目标、写 SMART 目标、设计 OKR、规划习惯养成体系、拆解大目标、做周/月/季度复盘时走目标方法论分支；当用户显式提出 goal、使用 /goal 命令、Goal 处于 active 状态、或涉及长任务循环 / 完成标记 / 线程接力时走工程循环控制分支。负责 SMART/OKR/习惯/拆解/动机/复盘框架速查，以及 Goal 生命周期、循环控制器、完成标记验证、死循环防护与临时产物清理。目标模糊时先拆解再进入循环；Goal 激活即视为计划已完成，执行分歧由 agent 自行裁决并按推荐方向推进。
license: MIT
allowed-tools: Read, Write, Bash
metadata:
  displayName: "目标与循环"
  version: "2.0.0"
  author: "luode-skills"
  category: "orchestration"
  tags: [goal-setting, smart-goals, okr, habits, loop, long-run, completion-marker, orchestration]
---

# 目标与循环规则（goal-loop-rules）

> 本 skill 由 `goal__skillhub`（目标设定方法论）与 `long-run-loop-rules`（工程循环控制）合并而成。
> 两个域共享一个入口但职责独立：目标方法论不负责平台 Goal 生命周期；工程循环控制不负责个人目标管理理论。

## 域路由（先判断再执行）

进入本 skill 后必须先按用户意图选择分支，禁止两个分支同时执行：

| 用户意图 | 走哪一节 |
|---|---|
| 设定个人 / 职业目标、写 SMART / OKR、习惯养成、目标复盘 | 第一节「目标方法论参考」 |
| 显式提出 goal / 使用 `/goal` 命令 / Goal 处于 active / 长任务循环 / 过夜跑 | 第二节「工程循环控制」 |

当用户目标仍然模糊（无法写出完成标记，如"想转行""想把技能体系做好"）时，先在第一节完成拆解，再把产物输入第二节作为 goal objective。

## 第一节：目标方法论参考

> 吸收自 `goal__skillhub`（BytesAgain，MIT）。脚本入口：`scripts/script.sh`（支持任意 cwd 以绝对路径调用；bash 不可用时按下方框架要点现场输出，不阻塞任务）。

目标方法论顾问：提供 SMART/OKR/习惯养成/复盘等被验证的框架速查，帮助把模糊愿望变成可执行、可跟踪、可复盘的目标体系。

### 适用边界

- **做**：目标框架速查（SMART/OKR/习惯/拆解/动机/复盘/常见陷阱）、目标体系设计建议。
- **不做（转交）**：平台内 Goal 生命周期 → 走第二节；目标跟踪的自动提醒/定时任务 → 交给自动化能力（如 `automation_update` 定时任务），本节只给方法论。

### 工作流（4 步）

1. **识别目标场景**：判断场景类型——设定新目标（走 SMART/OKR）、习惯养成（走 habits）、大目标拆解（走 planning）、目标进展停滞（走 motivation + review）。
2. **选择并取用框架**：执行对应命令取用参考内容，或直接按框架要点现场输出。
3. **落地执行与跟踪**：把目标拆成可测量的关键结果与日常行动项，明确复盘节奏（周/月/季）；目标量级大时先确认投入边界。
4. **复盘与调整**：按 review 框架复盘——哪些达成、哪些偏离、原因是什么、如何纠偏。

### 命令速查表

| 命令 | 用途 |
|---|---|
| `intro` | 目标设定基础：为什么目标有效、常见陷阱、研究依据 |
| `smart` | SMART 框架：Specific/Measurable/Achievable/Relevant/Time-bound + 示例 |
| `okr` | OKR 框架：目标与关键结果、评分、节奏、对齐 |
| `habits` | 习惯养成：提示-行动-奖励、原子习惯、执行意图 |
| `planning` | 目标拆解：大目标 → 里程碑 → 冲刺 → 每日行动 |
| `motivation` | 动机科学：内在/外在动机、克服平台期 |
| `review` | 复盘系统：周/月/季复盘、纠偏、庆祝 |
| `pitfalls` | 常见目标设定错误与对策 |
| `help` / `version` | 帮助 / 版本 |

### 边界条件

- 框架不适用：用户只是随手记录想法时，先帮其澄清意图，不强行套 SMART/OKR。
- 脚本不可用：bash 缺失或执行失败时，降级为直接按框架要点现场输出。
- 目标冲突：多个目标互抢资源时，先确认优先级排序，不默认全做。
- 过度承诺：目标明显超出可执行范围时，提示拆小步或延长时间窗，不附和空头承诺。

### 约束

- 参考内容基于目标设定与行为科学主流研究（Locke & Latham 等），输出时标注依据，不编造数据。
- 所有建议必须落到可执行的下一步行动，不止于理论。
- 涉及行为改变类建议，先说明预期成本（意志力/时间/社交影响），再给方案。

## 第二节：工程循环控制

> 吸收自 `long-run-loop-rules`。本节负责平台 Goal 生命周期与长任务循环执行机制，不依赖 CLI wrapper，纯 Desktop 环境可用。

### 范式定位

AI 编程范式三阶段演进：**Prompt Engineering**（人工逐条提示、模型单次执行、人判结果）→ **Harness Engineering**（为单 Agent 搭受限环境，带预检/修复/hook，仍靠人触发）→ **Loop Engineering**（多 Agent 编排 + 决策 + 自主循环，长期自驱动）。本 skill 是 Loop Engineering 阶段在桌面平台的落地实现。

### 为什么需要长任务循环

LLM 无法准确判断自己的工作是否真正完成。长任务循环的核心思想：让 AI 在一个循环中工作，每次它想退出时，外部系统检查三个问题——真的完成了吗？符合客观标准了吗？还有没有遗漏？如果没有，就重新注入任务，继续下一轮。

### 控制器模式

本 skill 采用"主 agent 为控制器、子 agent 为工人"的架构：

| 角色 | 职责 | 不负责 |
|---|---|---|
| **主 agent（控制器）** | 解析任务、创建 worker、汇总结果、跟踪进度、决定循环 | 写业务代码、改文件、跑测试 |
| **worker（子 agent）** | 实际执行任务、输出完成标记 | 做循环决策、管理状态 |

### 触发条件

**路径 A：Goal 模式触发**

1. `create_goal` 已成功执行，Goal 当前为 `active`
2. Goal objective 中包含完成标记（如 `<promise>DONE</promise>`、`COMPLETE`、`##LOOP_DONE##`）

**路径 B：显式 Goal 意图触发**

用户显式提出 goal 或使用 `/goal` 命令。即使平台不提供 `create_goal`，只要用户表达了 goal 意图，也必须触发本节，并按 `references/safety-mechanisms.md` 的降级表退到可用的循环机制。

两条路径都缺时不触发，也不自动进入循环模式。

### 触发后行为

- 若目标仍为模糊大目标，先按 `references/goal-breakdown-before-loop.md` 倒推法拆解（澄清目标与 deadline → 拆 3 层动作 → 标出首个最小可行步），拆解产物作为 goal objective 输入后再继续。
- 解析任务目标中的完成标记；若未写完成标记，采用默认标记 `<promise>DONE</promise>` 并明确告知用户。
- 进入控制器模式，主 agent 转为循环控制器。
- 创建工作线程执行实际任务（无线程工具时降级为 L1 内部续跑）。
- 每次 worker 结束，检测完成标记。
- 含标记 → 标记 Goal complete（无 Goal 模式时以状态文件 `done` 收口）。
- 不含标记 → 继续下一轮。

### Goal 模式免确认推进（分歧按推荐方案执行）

Goal 模式一旦激活（用户当前轮显式用 `/goal` 开启，或用户已显式确认的 Goal 处于 `active`），即视为**计划阶段已经完成、用户只要结果**，循环执行不再为方案分歧暂停等待用户确认。

- **计划视为已完成**：不重复征求计划确认，不回到需求澄清或方案确认。
- **分歧自行裁决**：agent 自行完成对比分析，给出最推荐方向并**直接按推荐方向执行**，不抛选择题、不暂停。
- **推荐方向判定顺序**：① 是否满足 goal objective 与验收条件；② 是否最小可逆、改动最小；③ 是否有代码、文档、真实运行结果等证据支撑；④ 是否守住安全与合规红线。
- **证据不足走最安全兜底**：无法判定时选最小可逆、最保守、可回滚的路径继续推进，并把分歧、依据与选择写入状态文件 `worker_summaries`，不停下来问用户。
- **仍不得突破的红线**（不因免确认放开）：系统安全限制与权限审批、高风险或不可逆操作、`local` 连接调试红线、凭据不回显、Git 写历史红线（提交/推送仍需当轮显式授权）、跨项目写入红线与 `WRT-*` 授权边界、个人文件删除保护。人工检查点与成本预警继续保留——它们是安全熔断，不是方案确认。
- **临时产物清理**：循环执行中产生的临时脚本、临时文件、临时目录与后台任务，在收口时必须按 `runtime-process-cleanup-rules` 的三层清理对象清理干净，禁止遗留；未清理视为任务未完成。
- **不适用对象（防自我授权）**：agent 为补建任务投影、异常修复或超时探测而自动 `create_goal` 产生的 Goal，不构成用户开启的 Goal 模式；免确认推进必须建立在用户显式开启或确认的 Goal 之上。
- **边界与退出**：用户显式改变、缩小或撤销目标时回到正常确认流程；Goal 未激活或处于 Plan Mode 时本条不适用。

### 语义触发示例

只要 Goal 激活且完成标记存在，自动进入循环模式。以下关键词也触发本节：

- "过夜跑 / 跑通宵 / 让它一直跑"
- "循环 / 自动重试 / 接力"
- "Ralph / Ralph Wiggum"
- "持续工作 / 长时间运行"
- "一直做直到完成"
- "建个 goal / 创建目标 / 下个目标 / /goal"
- "拆解目标 / 怎么实现 / 大目标太小步 / OKR"（目标模糊需先拆解再执行时）

### /loop 定时循环映射（平台无原生 /loop 时的等价）

本平台的 `/goal` 语义对应本节的目标驱动路径。`/loop`（定时重复执行）语义在本平台等价映射为：

- **定时触发**：`automation_update`（rrule 定时），对应模式库「巡逻循环」。
- **两者共用约束**：完成条件必须客观可验证（文件存在、测试通过、指标达标）；无终止条件 = 无限循环，属反模式。

### 循环模式选择

> 8 种模式库见 `references/loop-patterns-library.md`。

- 本节主路径 = 模式 5「目标驱动探索」（Goal 触发 + 完成标记 + 线程接力）。
- 定时巡检类 = 模式 1「巡逻循环」（配合 automation 定时触发）。
- 其余模式按模式库选择指南调整循环设计。

### 三层递进架构

#### L1：内部续跑

**机制：** 复用现有 `create_goal` + `autonomous-execution-rules`，在一轮会话内持续推进。

**适用场景：** 单次超长任务，session 不超时，能在同一轮内完成多个子步骤。

**限制：** 一旦 agent 认为"完成了"或预算耗尽，循环就终止了，没有外部重启机制。

#### L2：线程接力跑（核心）

**机制：** 主 agent 作为控制器，创建工作线程执行实际任务，每次 worker 结束后检测完成标记，未完成则创建新 worker 继续。

```
主 agent（控制器）
  ├── 解析任务，提取完成标记
  ├── 创建 worker 线程（create_thread），喂入任务+标记
  ├── wait_threads 等待 worker 结束
  ├── 跑脚本检测输出中是否含完成标记
  ├── 含标记 → 标记 Goal complete，结束
  ├── 不含标记 → 迭代+1，检查上限
  │     ├── 未达上限 → 创建新 worker 线程，继续
  │     └── 达上限 → 标记 Goal blocked，汇总报告
  ├── 每轮汇总 worker 结果，写入状态文件
  └── 每 N 轮（可配置）暂停，等待人工确认是否继续
```

**适用场景：** 需要过夜跑、跨 session 的长时间任务；大规模重构、测试迁移、批量添加类型。

**安全机制：** max_iterations 上限、死循环检测、成本预算告警、人工检查点。

#### L3：自动化监控

**机制：** 集成到 `continuous-code-quality-supervisor-rules` 的监控模式，通过自动化定期唤醒检查。

**适用场景：** 持续代码质量监控、定期重构、批量更新。

### 完成标记规范

推荐格式：

- **`<promise>DONE</promise>`** —— 推荐，XML 包裹式，误匹配概率低
- **`##LOOP_DONE##`** —— 简洁，适合简短任务
- **`COMPLETE`** —— 兼容 Ralph Wiggum 生态

在 Goal objective 中使用：

```
<objective>
# 任务：重构用户认证模块

1. 将身份验证逻辑从 monolith 中提取到独立服务
2. 所有测试通过
3. 文档更新完成

当所有工作完成且测试通过后，输出：<promise>DONE</promise>
</objective>
```

详细规范见 `references/completion-marker-pattern.md`。

### 执行流程

#### 首次命中

1. 读取 Goal objective，提取完成标记
2. 读取 `references/loop-config-schema.md` 获取默认配置
3. 调用 `scripts/loop_controller.py start` 创建状态文件
4. 创建工作线程（`create_thread`），喂入任务 + 完成标记
5. `wait_threads` 等待 worker 完成
6. 调用 `scripts/check_completion_marker.py` 检测输出
7. 根据检测结果决定继续或停止
8. 调用 `scripts/loop_controller.py record-iteration` 记录状态
9. 每 N 轮调用 `scripts/detect_dead_loop.py` 检查死循环

#### 后续轮次

1. 读取当前状态文件
2. 检查迭代次数上限
3. 检查死循环检测结果
4. 创建新 worker 线程，继续
5. 重复检测流程

#### 收口

- 完成标记存在 → `update_goal(complete)`，汇总所有轮次成果
- 达到迭代上限 → `update_goal(blocked)`，报告进度和剩余工作
- 死循环检测触发 → `update_goal(blocked)`，报告死循环原因
- 用户中断 → 记录当前状态，保持在 active 状态
- 人工检查点暂停 → 报告当前进度，等待用户确认

### 与其他 Skill 的协作

| Skill | 协作方式 |
|---|---|
| `autonomous-execution-rules` | L1 内部续跑的承载者；本节的 L2 是独立路径，不冲突 |
| `parallel-task-dispatch-rules` | 负责 worker 线程的创建、生命周期管理和回收 |
| `continuous-code-quality-supervisor-rules` | L3 监控模式的可选上游 |
| `skill-hit-check-rules` | 提供 `deferred-gate-registry.md` 触发登记 |
| `reasoning-summary-structure-rules` | 负责最终收口时的总结渲染 |
| `execution-failure-learning-rules` | worker 线程失败时联动恢复 |
| `task-plan-rehydration-rules` | 负责任务投影持久化 |

### 配置参数

#### 默认配置

| 参数 | 默认值 | 说明 |
|---|---|---|
| `max_iterations` | 50 | 最大迭代次数，防止无限循环 |
| `checkpoint_interval` | 10 | 每 N 轮暂停一次人工检查点 |
| `dead_loop_window` | 5 | 检测死循环的窗口大小（最近 N 轮） |
| `dead_loop_similarity_threshold` | 0.95 | 死循环判定阈值 |
| `cost_alert_thresholds` | [10, 50, 100] | 成本预警阈值（美元） |
| `rate_limit_per_hour` | 100 | 每小时速率限制 |
| `max_runtime_minutes` | 480 | 最大运行时间（分钟，默认 8 小时） |
| `worker_timeout_minutes` | 30 | 单个 worker 线程超时时间 |

#### 在 Goal objective 中覆盖

```
<objective --max-iterations 100 --checkpoint-interval 20>
...
</objective>
```

### 状态文件

状态文件固定为 `$CODEX_HOME/state/goal-loop/<task-sha256>.json`。

字段：
- `goal_objective`：Goal 原始目标文本
- `completion_marker`：完成标记文本
- `max_iterations`：最大迭代次数
- `checkpoint_interval`：人工检查点间隔
- `current_iteration`：当前迭代次数
- `worker_thread_ids`：所有 worker 线程 ID 列表
- `worker_summaries`：每轮 worker 结果摘要
- `total_cost_estimate`：预估总成本
- `dead_loop_count`：连续死循环检测次数
- `status`：状态（active / done / blocked）

### 安全机制

#### 硬性限制

1. **max_iterations**：必须设置，默认 50，防止无限循环
2. **人工检查点**：每 N 轮暂停，等待用户确认
3. **成本预警**：达到阈值时暂停并通知

#### 智能检测

1. **死循环检测**：对比最近 N 轮产出变化，无变化则熔断
2. **速率限制**：每小时最大迭代次数，防止 API 账单爆炸
3. **智能熔断**：连续多次检测到完成标记但未正常退出时强制退出

#### 异常处理

- worker 线程创建失败 → 记录失败，尝试重试，3 次失败后标记 blocked
- wait_threads 超时 → 记录超时，重新创建 worker
- 状态文件损坏 → 重建状态文件，标记当前迭代为 limited
- 死循环检测连续触发 → 强制熔断，标记 blocked

详细规范见 `references/safety-mechanisms.md`。

### 通过标准

- 已正确解析任务目标中的完成标记
- 已进入控制器模式，主 agent 不直接写业务代码
- 已创建初始状态文件
- 已至少启动一轮 worker 线程（无线程工具时已降级为 L1 内部续跑）
- 安全机制已正确配置（max_iterations 必须设置）
- 每轮结束已检测完成标记
- 完成标记存在时已正确标记 Goal complete
- 达到上限时已正确标记 Goal blocked

### 不适用场景

- 既无 Goal 模式、用户也未显式提出 goal 意图的普通会话（不触发）
- Goal active 但 objective 中没有完成标记，且用户无显式 goal 意图（不自动循环）
- Plan Mode 下（不触发）
- 简单一次性任务（不需要循环）
- 需要人类实时判断的探索性任务

## 维护注意事项

- 新增 safety 机制时同步更新 `references/safety-mechanisms.md`
- 修改完成标记检测逻辑时同步更新 `references/completion-marker-pattern.md`
- 修改 default 配置时同步更新 `references/loop-config-schema.md`
- 新增或调整循环模式时同步更新 `references/loop-patterns-library.md`
- 修改脚本时同步更新本 SKILL.md 的执行流程描述
- 修改后必须运行 `python skill-dictionary/generate_dictionary.py` 刷新 `skill-dictionary/data.js` 与 `字典.md`
