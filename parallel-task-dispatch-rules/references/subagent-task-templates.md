# 子代理任务模板

## 主 agent 启动公告模板（强制）

```text
Subagent 状态：
- 已启动：<subagent-id 或昵称>
- 逻辑名：<任务简要中文-线程标识>
- 平台昵称：<spawn 返回昵称；没有则写未提供>
- 执行 skill：<skill-name>
- 任务：<一句话任务摘要>
```

## 主 agent 完成公告模板（强制）

```text
Subagent 状态：
- 已完成：<subagent-id 或昵称>
- 逻辑名：<任务简要中文-线程标识>
- 平台昵称：<spawn 返回昵称；没有则写未提供>
- 执行 skill：<skill-name>
- 结果：<一句话结果摘要>
- 回收：<已调用 close_agent / 回收失败原因>
```

## 模板 1：只读核查任务

```text
任务目标：
- <一句话目标>

输入范围：
- 文件/目录：<path1>, <path2>
- 规则依据：<skill-name / reference>

已知上下文：
- 已确认事实：<只写完成任务必需的事实>
- 无需重复阅读：<主 agent 已经收敛、subagent 不必再通读的文件或背景>

输出要求：
- 仅输出发现的问题与建议
- 按严重级别排序
- 给出文件路径和行号
- 若发现仍需通读大范围共享上下文，先回报主 agent 缩窄范围，不要自行扩读整个仓库
```

## 模板 2：单写集改动任务

```text
任务目标：
- <一句话目标>

写集边界：
- 仅允许修改：<file-a>, <file-b>
- 禁止修改：写集外所有文件

已知上下文：
- 已确认事实：<主 agent 已确认的约束、接口、边界>
- 无需重复阅读：<已经收敛的长文档、长调用链、无需再次扫描的目录>

约束：
- 不回退他人改动
- 不做无关重构
- 输出变更摘要与验证结果
- 若为了完成任务必须重新通读大范围共享上下文，先回报主 agent，避免为小改动支付高额启动成本
```

## 模板 3：并行多子任务（互斥写集）

```text
子任务 A：
- 目标：<A 目标>
- 写集：<A files>

子任务 B：
- 目标：<B 目标>
- 写集：<B files>

整合要求：
- 主 agent 统一整合结果
- 若冲突，优先保留主路径正确性
```

## 模板 4：provisioning 只读检测（只读、可并行）

```text
任务目标：
- 只读探测 <工具/MCP/插件名> 的 provisioning 现状，不做任何写动作。

只读范围：
- 检查项：依赖是否安装（如 node_modules）、目标 config 是否已含对应表 / 键、工具是否已暴露、项目结构标记。
- 优先入口：存在只读探测命令时使用（如 `node bootstrap.mjs --check`），禁止装依赖 / 写 config / 备份。
- 规则依据：parallel-task-dispatch-rules/references/provisioning-delegation.md

输出要求：
- 输出状态 JSON 或结构化结论：deps、registered、exposed、configPath 等真实现状。
- 多工具检测时各线程写集互不重叠，结果回主 agent 汇总。
- 严禁任何写动作；若发现只读入口缺失，回报主 agent，不得擅自改写。
```

## 模板 5：安装子 agent（单实例、串行、独占 config 写）

```text
任务目标：
- 完成 <工具/MCP/插件名> 的安装 / 注册，独占写目标 config 文件。

写集边界：
- 允许写：<目标 config 文件绝对路径>（单一文件，单写者）。
- 允许的目录级安装：<各工具目录内 npm ci 等互斥写集>。
- 禁止：并发任何其它 config 写入者；改写集外文件。

强制流程：
- 写前备份目标 config；幂等追加（已存在则判为 already，不重复写）。
- 写后回读校验：表头唯一、备份存在、幂等复跑为 already。
- UTF-8 无 BOM 写入；完成后回报主 agent 收口，等待关闭回收。
- 规则依据：parallel-task-dispatch-rules/references/provisioning-delegation.md

同时刻不变量：
- 至多一个安装子 agent 活跃；多个工具的 config 注册由这一个安装子 agent 顺序完成。
```

## 回收结果最小清单

- 子任务是否完成目标。
- 是否修改了写集外文件。
- 是否提供了可验证证据（命令输出/文件 diff/测试结论）。
- 是否存在需要主 agent 决策的冲突项。
- 主 agent 是否已输出启动公告与完成公告。
- 主 agent 是否已记录逻辑名、平台昵称和 agent_id 的映射。
- 主 agent 是否已调用 `close_agent` / 等价关闭工具完成回收。

## 启动计划脚本约定

- 批量委派前，优先运行 `scripts/generate_subagent_plan.py` 生成启动计划。
- `agent_name` / `logical_agent_name` 默认使用“任务简要中文 + 线程标识”，用于主 agent 侧的中文逻辑命名。
- 平台 UI 昵称以真实启动工具返回值为准；若工具未提供命名参数，不能强制改成中文。
- 主 agent 使用脚本输出的 `message` 作为真实子 agent 委派消息草案；当前轮授权或项目级完全授权允许时，调用真实 subagent / multi-agent / thread 工具。
