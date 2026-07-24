# provisioning 子代理委派契约

本文件是 provisioning（MCP / 插件 / 工具的**检测与安装**）子代理委派的唯一事实来源。`mcp-installation-rules`、`plugin-installation-rules`、`thread-title-rules` 只引用本文件，不各自复制策略正文，避免多副本漂移。

本契约只约束 provisioning 阶段（检测 / 安装 / 注册 / 首次可用性验证）的执行编排；已配置工具在任务运行期的失活、超时、断开等故障不归本文件，统一路由 `agent-runtime-recovery-rules`。

## 唯一入口与授权顺序

- provisioning 的检测与安装统一经 `parallel-task-dispatch-rules` 的统一状态机委派，不另开第二个分发入口。
- 授权判定顺序固定：系统与开发者规则 > 平台真实工具元数据与能力 > 用户当前轮明确允许 / 禁止 > 项目级 standing authorization > 默认本地串行回退。
- 触发默认：凡进入 MCP / 插件 / 工具的检测或安装，默认委派 subagent，**含单工具、单条命令的 trivial 场景**（本项为 provisioning 专项 standing preference，覆盖 `parallel-task-dispatch-rules` 通常的成本门槛）。系统规则、工具元数据、用户当前轮禁止仍高于该默认。
- 用户当前轮明确禁止子代理、或环境无真实子代理工具时，回退主 agent 本地串行，并如实输出回退原因；不得用计划文本冒充已启动。

## 三种角色

### 检测子 agent（只读、可并行）

- 只做只读探测：检查依赖是否安装（如 `node_modules`）、目标 config 是否已含对应表 / 键、工具是否已暴露、项目结构标记等。
- 多个独立工具的检测并行扇出，每个检测线程范围互不重叠；检测结果回主 agent 汇总。
- 检测子 agent 禁止任何写动作（不装依赖、不写 config、不备份）。存在只读探测入口时优先使用（如 `bootstrap.mjs --check`）。

### 安装子 agent（单实例、串行、独占 config 写）

- 所有写 config 文件的注册 / 补齐集中到**单一**安装子 agent，串行独占对应 config 文件的写。
- 同一时刻至多一个安装子 agent 活跃；多个工具的 config 注册由这一个安装子 agent 顺序完成，不得并发。
- 写前备份、幂等追加、写后回读校验由安装子 agent 执行；完成后由主 agent 回收关闭。
- 目录级、写集互斥的安装动作（如各工具自身目录内的 `npm ci`）可作为独立写集并行，但**任何 config 文件写不得并发**。

### 主 agent（收口）

- 冻结主 / 子职责与互斥写集；同一 config 文件是单写者写集，绝不并行两个写入者。
- 汇总检测结论、裁决冲突、对安装结果做收口校验（表头唯一、备份存在、幂等复跑为 already）。
- 输出 `计划线程数 / 实际启动数 / 完成数 / 关闭数 / 回退原因`。

## 写目标（随 skill 而定）

- `thread-title-rules`（`thread_session`）：写全局 `~/.codex/config.toml`（`CODEX_HOME` 优先）。
- `mcp-installation-rules`：写项目级 `./codex/config.toml` 或 `./.codex/config.toml`。
- `plugin-installation-rules`：按插件官方方式（多为平台命令 / 项目级配置），config 写按同一"单写者"不变量处理。
- 单写者不变量按"每个 config 文件"成立：不同文件可由不同批次处理，同一文件任意时刻只允许一个写入者。

## 生命周期

1. 主 agent 冻结边界与写集，生成启动计划。
2. 检测子 agent（可并行）先行探测，结果回主 agent 汇总。
3. 需要写 config 时，启动单一安装子 agent 串行执行；主 agent 不空等，推进不重叠的本地工作。
4. 主 agent 回收安装子 agent 结果，做收口校验与冲突裁决。
5. 结果收回且不再使用时立即关闭子 agent 或执行平台等价回收。

## 重载限制（不可消除）

- 安装子 agent 完成 MCP 注册后，新 MCP 仍需宿主重载 / 新任务后才会暴露给主 agent；委派不消除这一物理约束。
- 因此 provisioning 委派的正常收尾是"已完成注册 → 提示重载 → 本轮跳过对该工具的调用"，而不是宣称本轮已可用。

## 运行期恢复分工

- 已配置工具在运行期的 timeout / EOF / 断开 / 失活等故障不属于 provisioning，统一转 `agent-runtime-recovery-rules`。
- provisioning 阶段的安装 / 注册 / 首次连接失败先联动 `execution-failure-learning-rules`，改变方法后再恢复，不做无变化重试。