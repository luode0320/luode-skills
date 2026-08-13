---
name: long-run-loop-rules
description: 【Goal 激活或用户显式 goal 意图即触发】当当前会话的 Goal 处于 active 状态，或用户显式提出 goal / 使用 `/goal` 命令时自动命中——即使当前平台不提供 Goal 目标模式（无 `create_goal` 工具）也应触发并降级到可用的循环机制。负责长任务自动循环重启 + 完成标记验证机制，采用"主 agent 为控制器、子 agent 为工人"的线程接力模式，让 AI 持续工作直到任务真正完成。支持三层递进：L1 内部续跑（复用 autonomous-execution-rules 的单轮内持续推进）、L2 线程接力跑（跨线程自动重启）、L3 自动化监控（集成 continuous-code-quality-supervisor-rules 的监控模式）。不依赖 CLI wrapper，纯 Desktop 环境可用。
---

# 长任务自动循环规则

## 核心概念

### 为什么需要长任务循环

LLM 有一个根本缺陷：它无法准确判断自己的工作是否真正完成。人类的完成标准是客观的——所有测试通过、功能完整可用、代码质量达标。但 AI 只能基于"感觉"来判断。长任务循环的核心思想是：让 AI 在一个循环中工作，每次它想退出时，外部系统检查三个问题——真的完成了吗？符合客观标准了吗？还有没有遗漏？如果没有，就重新注入任务，继续下一轮。

### 控制器模式

本 skill 采用"主 agent 为控制器、子 agent 为工人"的架构：

| 角色 | 职责 | 不负责 |
|---|---|---|
| **主 agent（控制器）** | 解析任务、创建 worker、汇总结果、跟踪进度、决定循环 | 写业务代码、改文件、跑测试 |
| **worker（子 agent）** | 实际执行任务、输出完成标记 | 做循环决策、管理状态 |

主 agent 的 token 只用于管理决策，实际工作由 worker 线程消耗，能跑更多轮次。

## 触发条件

### 触发（硬规则——不自称不命中）

本 skill 有两条独立触发路径，满足任一即必须自动命中：

**路径 A：Goal 模式触发**

1. `create_goal` 已成功执行，Goal 当前为 `active`
2. Goal objective 中包含完成标记（如 `<promise>DONE</promise>`、`COMPLETE`、`##LOOP_DONE##`）

**路径 B：显式 Goal 意图触发**

用户显式提出 goal 或使用 `/goal` 命令（例如"帮我建个 goal 跑这个任务"、"/goal 重构用户认证模块"）。即使当前 agent / 平台不提供 `create_goal` 等 Goal 目标模式，只要用户表达了 goal 意图，也必须触发本 skill，并按 `references/safety-mechanisms.md` 的工具不可用降级表退到可用的循环机制（无线程工具则降级为 L1 内部续跑）。

两条路径都缺时不触发，也不自动进入循环模式。

### 触发后行为

- 解析任务目标中的完成标记；若用户目标里未写完成标记，采用默认标记 `<promise>DONE</promise>` 并明确告知用户
- 进入控制器模式，主 agent 转为循环控制器
- 创建工作线程执行实际任务（无线程工具时降级为 L1 内部续跑）
- 每次 worker 结束，检测完成标记
- 含标记 → 标记 Goal complete（平台无 Goal 模式时以状态文件 `done` 收口）
- 不含标记 → 继续下一轮

### 语义触发示例

只要 Goal 激活且完成标记存在，自动进入循环模式；用户显式提出 goal 或使用 `/goal` 命令也触发。此外用户显式使用以下关键词也触发本 skill：

- "过夜跑 / 跑通宵 / 让它一直跑"
- "循环 / 自动重试 / 接力"
- "Ralph / Ralph Wiggum"
- "持续工作 / 长时间运行"
- "一直做直到完成"
- "建个 goal / 创建目标 / 下个目标 / /goal"

## 三层递进架构

### L1：内部续跑

**机制：** 复用现有 `create_goal` + `autonomous-execution-rules`，在一轮会话内持续推进。

**适用场景：** 单次超长任务，session 不超时，能在同一轮内完成多个子步骤。

**限制：** 一旦 agent 认为"完成了"（调用 `update_goal(complete)`）或预算耗尽，循环就终止了，没有外部重启机制。

### L2：线程接力跑（核心）

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

### L3：自动化监控

**机制：** 集成到 `continuous-code-quality-supervisor-rules` 的监控模式，通过自动化定期唤醒检查。

**适用场景：** 持续代码质量监控、定期重构、批量更新。

## 完成标记规范

### 完成标记格式

完成标记是长任务循环的核心。当 worker 的输出中包含完成标记时，控制器才认为任务真正完成。

推荐格式：

- **`<promise>DONE</promise>`** —— 推荐，XML 包裹式，误匹配概率低，可携带额外信息
- **`##LOOP_DONE##`** —— 简洁，适合简短任务
- **`COMPLETE`** —— 兼容 Ralph Wiggum 生态

### 在 Goal objective 中使用

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

## 执行流程

### 首次命中

1. 读取 Goal objective，提取完成标记
2. 读取 `loop-config-schema.md` 获取默认配置
3. 调用 `scripts/loop_controller.py start` 创建状态文件
4. 创建工作线程（`create_thread`），喂入任务 + 完成标记
5. `wait_threads` 等待 worker 完成
6. 调用 `scripts/check_completion_marker.py` 检测输出
7. 根据检测结果决定继续或停止
8. 调用 `scripts/loop_controller.py record-iteration` 记录状态
9. 每 N 轮调用 `scripts/detect_dead_loop.py` 检查死循环

### 后续轮次

1. 读取当前状态文件
2. 检查迭代次数上限
3. 检查死循环检测结果
4. 创建新 worker 线程，继续
5. 重复检测流程

### 收口

- 完成标记存在 → `update_goal(complete)`，汇总所有轮次成果
- 达到迭代上限 → `update_goal(blocked)`，报告进度和剩余工作
- 死循环检测触发 → `update_goal(blocked)`，报告死循环原因
- 用户中断 → 记录当前状态，保持在 active 状态
- 人工检查点暂停 → 报告当前进度，等待用户确认

## 与其他 Skill 的协作

| Skill | 协作方式 |
|---|---|
| `autonomous-execution-rules` | L1 内部续跑的承载者；本 skill 的 L2 是独立路径，不冲突 |
| `parallel-task-dispatch-rules` | 负责 worker 线程的创建、生命周期管理和回收 |
| `continuous-code-quality-supervisor-rules` | L3 监控模式的可选上游 |
| `skill-hit-check-rules` | 提供 `deferred-gate-registry.md` 触发登记 |
| `reasoning-summary-structure-rules` | 负责最终收口时的总结渲染 |
| `execution-failure-learning-rules` | worker 线程失败时联动恢复 |
| `task-plan-rehydration-rules` | 负责任务投影持久化 |

## 配置参数

### 默认配置

| 参数 | 默认值 | 说明 |
|---|---|---|
| `max_iterations` | 50 | 最大迭代次数，防止无限循环 |
| `checkpoint_interval` | 10 | 每 N 轮暂停一次人工检查点 |
| `dead_loop_window` | 5 | 检测死循环的窗口大小（最近 N 轮） |
| `dead_loop_similarity_threshold` | 0.95 | 死循环判定阈值 |
| `cost_alert_thresholds` | [10, 50, 100] | 成本预警阈值（美元） |
| `rate_limit_per_hour` | 100 | 每小时速率限制 |

### 在 Goal objective 中覆盖

```
<objective --max-iterations 100 --checkpoint-interval 20>
...
</objective>
```

## 状态文件

状态文件固定为 `$CODEX_HOME/state/long-run-loop/<task-sha256>.json`。

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

## 安全机制

### 硬性限制

1. **max_iterations**：必须设置，默认 50，防止无限循环
2. **人工检查点**：每 N 轮暂停，等待用户确认
3. **成本预警**：达到阈值时暂停并通知

### 智能检测

1. **死循环检测**：对比最近 N 轮产出变化，无变化则熔断
2. **速率限制**：每小时最大迭代次数，防止 API 账单爆炸
3. **智能熔断**：连续多次检测到完成标记但未正常退出时强制退出

### 异常处理

- worker 线程创建失败 → 记录失败，尝试重试，3 次失败后标记 blocked
- wait_threads 超时 → 记录超时，重新创建 worker
- 状态文件损坏 → 重建状态文件，标记当前迭代为 limited
- 死循环检测连续触发 → 强制熔断，标记 blocked

详细规范见 `references/safety-mechanisms.md`。

## 通过标准

- 已正确解析任务目标中的完成标记（目标未写标记时已采用默认标记并告知用户）
- 已进入控制器模式，主 agent 不直接写业务代码
- 已创建初始状态文件
- 已至少启动一轮 worker 线程（无线程工具时已降级为 L1 内部续跑）
- 安全机制已正确配置（max_iterations 必须设置）
- 每轮结束已检测完成标记
- 完成标记存在时已正确标记 Goal complete（无 Goal 模式时已用状态文件 `done` 收口）
- 达到上限时已正确标记 Goal blocked

## 不适用场景

- 既无 Goal 模式、用户也未显式提出 goal / `/goal` 意图的普通会话（不触发）
- Goal active 但 objective 中没有完成标记，且用户无显式 goal 意图（不自动循环，skill 仍可用但不触发循环模式）
- Plan Mode 下（不触发）
- 简单一次性任务（不需要循环）
- 需要人类实时判断的探索性任务

## 维护注意事项

- 新增 safety 机制时同步更新 `references/safety-mechanisms.md`
- 修改完成标记检测逻辑时同步更新 `references/completion-marker-pattern.md`
- 修改 default 配置时同步更新 `references/loop-config-schema.md`
- 修改脚本时同步更新本 SKILL.md 的执行流程描述
- 修改后必须运行 `python skill-dictionary/generate_dictionary.py` 刷新 `skill-dictionary/data.js` 与 `字典.md`
