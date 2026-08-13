# 循环配置 Schema

## 目标

定义 long-run-loop-rules 的循环配置参数，包括默认值、覆盖方式和 schema 校验规则。

## 配置文件路径

配置文件有两个来源，优先级从高到低：

1. Goal objective 参数：在 `<objective>` 标签中传入
2. 默认配置：本文件定义的默认值

## 参数 Schema

### 全部参数

| 参数 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| max_iterations | int | 50 | 最大迭代次数，必须为正整数 |
| checkpoint_interval | int | 10 | 每 N 轮暂停一次人工检查点，0 表示不暂停 |
| dead_loop_window | int | 5 | 检测死循环的窗口大小（最近 N 轮） |
| dead_loop_similarity_threshold | float | 0.95 | 死循环判定阈值（0.0-1.0） |
| cost_alert_thresholds | list[int] | [10, 50, 100] | 成本预警阈值，美元 |
| rate_limit_per_hour | int | 100 | 每小时最大迭代次数 |
| max_runtime_minutes | int | 480 | 最大运行时间，分钟（默认 8 小时） |
| worker_timeout_minutes | int | 30 | 单个 worker 线程超时时间 |
| completion_marker | string | 必填 | 完成标记，无默认值 |

### 在 Goal objective 中覆盖

```
<objective --max-iterations 100 --checkpoint-interval 20 --max-runtime 600>
...
</objective>
```

### 校验规则

- max_iterations：1-1000，超出范围使用默认值
- checkpoint_interval：0 表示不检查点，3-50 为有效范围
- dead_loop_window：3-20
- dead_loop_similarity_threshold：0.0-1.0
- cost_alert_thresholds：最多 5 个阈值，每个 >= 1
- rate_limit_per_hour：1-1000
- max_runtime_minutes：1-1440（24 小时）
- worker_timeout_minutes：1-240

## 状态文件 Schema

### 存储路径

`$CODEX_HOME/state/long-run-loop/<task-sha256>.json`

### 字段定义

```
{
  "version": 1,
  "task_sha256": "<task-sha256>",
  "goal_objective": "<Goal 原始目标文本>",
  "completion_marker": "<完成标记文本>",
  "config": {
    "max_iterations": 50,
    "checkpoint_interval": 10,
    "dead_loop_window": 5,
    "dead_loop_similarity_threshold": 0.95,
    "cost_alert_thresholds": [10, 50, 100],
    "rate_limit_per_hour": 100,
    "max_runtime_minutes": 480,
    "worker_timeout_minutes": 30
  },
  "current_iteration": 0,
  "worker_thread_ids": [],
  "worker_summaries": [],
  "total_cost_estimate": 0.0,
  "dead_loop_count": 0,
  "started_at": "2026-08-13T11:00:00+08:00",
  "last_updated": "2026-08-13T11:00:00+08:00",
  "status": "active"
}
```

### 状态枚举

| 状态 | 说明 |
|---|---|
| active | 循环进行中 |
| done | 任务完成，标记已找到 |
| blocked | 任务阻断，达到上限或死循环 |
| limited | 部分完成，状态文件损坏或工具不可用 |

### 状态迁移

```
active -> done: 完成标记存在
active -> blocked: 达到上限 / 死循环 / worker 失败
active -> limited: 状态文件损坏 / 工具不可用
done -> (终态): 不可变
blocked -> (终态): 不可变
limited -> active: 修复后重新激活
```

## 安全参数说明

### max_iterations 选择建议

- 简单任务（小范围重构）：10-20
- 中型任务（模块迁移）：20-50
- 大型任务（全项目重构）：50-100
- 超大型任务（过夜跑）：100-200
- 不建议超过 200，除非有特殊监控

### checkpoint_interval 选择建议

- 过夜跑：10-15（每 10-15 轮暂停一次，人工确认）
- 白天监控：5-8（更频繁的人工检查）
- 完全信任：0（不暂停，仅靠硬限制保护）
