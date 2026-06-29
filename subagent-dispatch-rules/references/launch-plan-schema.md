# 子 agent 启动计划 Schema

`subagent-dispatch-rules` 在需要批量启动子 agent 时，先运行：

```bash
python subagent-dispatch-rules/scripts/generate_subagent_plan.py --input <plan-input.json>
```

脚本只负责生成“启动计划 JSON”，不直接调用平台工具。
真实启动仍由主 agent 读取脚本输出后，再调用真实的 subagent / multi-agent / thread 工具。

## 输入 JSON

```json
{
  "task_summary": "补充子代理启动计划脚本并测试",
  "execution_skill": "subagent-dispatch-rules",
  "shared_constraints": [
    "不要回退他人改动",
    "不要修改写集外文件"
  ],
  "threads": [
    {
      "thread": "A",
      "goal": "编写子 agent 计划脚本",
      "write_scope": [
        "subagent-dispatch-rules/scripts/generate_subagent_plan.py"
      ],
      "read_scope": [
        "subagent-dispatch-rules/SKILL.md"
      ],
      "expected_output": "输出脚本变更摘要与自测结果",
      "agent_type": "worker",
      "extra_constraints": [
        "保持 UTF-8 编码"
      ]
    }
  ]
}
```

## 输入字段说明

- `task_summary`
  - 必填。
  - 主任务摘要。
  - 脚本会从这里提取“任务简要中文”，作为各子 agent 名称前缀。
- `execution_skill`
  - 选填。
  - 默认 `subagent-dispatch-rules`。
- `shared_constraints`
  - 选填。
  - 所有子 agent 共用的约束。
- `threads`
  - 必填、非空数组。
  - 每项代表一个计划线程。

## 线程对象字段

- `thread`
  - 必填。
  - 线程标识，如 `A`、`B`、`Review`。
- `goal`
  - 必填。
  - 子任务目标。
- `expected_output`
  - 必填。
  - 对该线程的最小交付要求。
- `write_scope`
  - 选填。
  - 写集边界；有写集时默认推断为 `worker`。
- `read_scope`
  - 选填。
  - 补充读取范围。
- `agent_type`
  - 选填。
  - 允许值：`worker`、`explorer`、`default`。
  - 未提供时：有 `write_scope` 则默认为 `worker`，否则默认为 `explorer`。
- `extra_constraints`
  - 选填。
  - 线程级额外约束。

## 输出 JSON

```json
{
  "task_name": "补充子代理启动计划",
  "task_summary": "补充子代理启动计划脚本并测试",
  "execution_skill": "subagent-dispatch-rules",
  "planned_thread_count": 1,
  "generated_at": "2026-06-29 22:10:00",
  "threads": [
    {
      "thread": "A",
      "agent_name": "补充子代理启动计划-A",
      "logical_agent_name": "补充子代理启动计划-A",
      "agent_type": "worker",
      "goal": "编写子 agent 计划脚本",
      "expected_output": "输出脚本变更摘要与自测结果",
      "write_scope": [
        "subagent-dispatch-rules/scripts/generate_subagent_plan.py"
      ],
      "read_scope": [
        "subagent-dispatch-rules/SKILL.md"
      ],
      "shared_constraints": [
        "不要回退他人改动",
        "不要修改写集外文件"
      ],
      "extra_constraints": [
        "保持 UTF-8 编码"
      ],
      "message": "..."
    }
  ]
}
```

## 输出约束

- `task_name`
  - 默认从 `task_summary` 提取“任务简要中文”。
  - 优先保留中文字符；没有中文时再回退到字母数字。
  - 当前默认截断到 10 个字符。
- `agent_name`
  - 固定格式：`<任务简要中文>-<线程标识>`。
  - 这是主 agent 计划中的中文逻辑名，不等于平台实际显示昵称。
- `logical_agent_name`
  - `agent_name` 的显式语义化别名，便于主 agent 在启动、完成和回收阶段统一跟踪。
  - 当前脚本会同时输出 `agent_name` 与 `logical_agent_name`，两者值相同。
- `message`
  - 直接用于真实 `spawn_agent` / 等价平台工具的委派消息草案。

## 主 agent 使用方式

1. 先运行脚本生成计划。
2. 读取输出 JSON。
3. 用 `threads[*].agent_name` 或 `threads[*].logical_agent_name` 作为中文逻辑任务名，写入主 agent 的启动/完成公告。
4. 用 `threads[*].message` 作为子 agent 委派消息。
5. 逐个调用真实 subagent / multi-agent / thread 工具，并记录工具返回的 `nickname` 作为平台昵称。
6. 建立运行时映射：`logical_agent_name -> platform_nickname -> agent_id`。
7. 启动后核对：
   - `planned_thread_count`
   - 实际成功启动的线程数
   - 未启动线程及原因
8. 结果收回后，立即调用 `close_agent` / 等价关闭工具，并核对“已关闭线程数”与“已完成线程数”一致。

## 平台昵称说明

- 当前脚本只能稳定生成中文逻辑任务名，不能直接决定平台 UI 的显示昵称。
- 若启动工具本身不提供自定义昵称参数，则 UI 中出现英文昵称属于平台分配行为，不代表脚本命名失败。
- 因此主 agent 汇报时必须同时带出：
  - 中文逻辑任务名
  - 平台返回昵称
  - agent_id
