# 现有 Skill 并行映射表

本表只提供常见 skill 的并行参考，不是白名单。主 agent 必须基于当前任务结构自主识别可并行子任务；项目分析、找 Bug、需求完善侦察、资料/日志/调用链证据收集等任务，即使没有出现在本表，也应按独立问题、独立证据来源、独立目录、独立模块或独立文件集尝试拆分。本仓库完全授权模式下，任务可切分且环境支持时应真实委派 subagent。

## 可并行

- `comment-completion-gate-rules`
  - 做什么：补齐函数、方法、字段、补丁位点相关注释。
  - 建议：可并行，只要每个线程拥有不重叠的文件集。
- `comment-placement-granularity-rules`
  - 做什么：判断注释该补在哪里、补多细、哪些位点必须补。
  - 建议：可并行，当注释补充发生在不同文件或不同模块时。
- `functional-validation-rules`
  - 做什么：验证功能行为、交互结果和输出是否满足需求。
  - 建议：可并行，当验证目标是独立模块或独立场景时。
- `implementation-review-rules`
  - 做什么：检查实现是否符合可读性、命名、结构、格式、语法/类型/引用和归位收口要求。
  - 建议：可并行，只要 review 范围不重叠且已指定统一收口线程。
- `code-style-consistency-rules`
  - 做什么：统一代码风格、局部写法和团队约定。
  - 建议：可并行，只要每个线程处理的文件集不重叠。
- `code-readability-rules`
  - 做什么：提升函数结构、表达顺序和局部可读性。
  - 建议：可并行，只要受影响模块彼此独立。
- `skill-audit-rules`
  - 做什么：并发审计主任务是否漏触发 skill，以及已触发 skill 是否还有未执行完的规则。
  - 建议：可并行，只读审计，不改代码、不写文件，适合和主线程同时跑；只看当前轮次和主线程已声明 skill，不靠历史记忆。
- `code-review-automation-rules`
  - 做什么：自动审查当前分支提交，输出致命/严重/中等/建议问题。
  - 建议：可并行，只读审查，适合和实现线程同时跑。
- `project-change-review-rules`
  - 做什么：对当前工作区 diff 做总审查，补抓边界、风险、遗漏和阻断项。
  - 建议：可并行，只读审查；若与主线程同时跑，必须指定单一收口线程统一汇总结论。
- `bug-regression-risk-rules`
  - 做什么：审查 Bug 修复可能带来的回归风险、兼容性风险和验证优先级。
  - 建议：可并行，只读审查，适合和修复线程并发跑。
- `mcp-installation-rules` / `plugin-installation-rules` / `thread-title-rules` 的 provisioning **检测**
  - 做什么：只读探测依赖是否安装、目标 config 是否已含对应表 / 键、工具是否已暴露、项目结构标记等。
  - 建议：可并行，多个独立工具的检测扇出为互不重叠的只读线程；存在只读探测入口时优先使用（如 `bootstrap.mjs --check`）。检测子 agent 禁止任何写动作，细则见 `provisioning-delegation.md`。

## 条件并行

- `test-regression-rules`
  - 做什么：判断修复或改动后需要补哪些回归测试。
  - 建议：条件并行，仅在回归覆盖范围能按模块或服务稳定拆分时。
- `parallel-task-dispatch-rules`
  - 做什么：判断是否需要派发子代理，并定义子任务边界。
  - 建议：条件并行，它是分发器，不是执行器；应与本 skill 配合使用。
- `acceptance-criteria-rules`
  - 做什么：把“做到什么算完成”写成可验证、可测试、可复核的标准。
  - 建议：条件并行，它更适合作为前置门槛，而不是和实现同线程混跑。

## 必须串行

- `bug-root-cause-rules`
  - 做什么：定位 bug 根因、调用链和影响面。
  - 建议：根因裁决必须串行；调用链、日志、复现样例、近期改动和影响面等证据收集可在边界清晰时条件并行，最终由主 agent 统一归纳裁决。
- `bug-intake-rules` 的 `discovery-and-gap` 条件路由
  - 做什么：识别 Bug 描述中缺少的复现条件、环境信息、日志和影响范围。
  - 建议：必须串行，它负责先补齐信息缺口，再进入后续分析。
- `bug-fix-proposal-rules`
  - 做什么：形成修复方案、评估风险和备选路径。
  - 建议：必须串行，当修复方案会改同一条代码路径或共享抽象时。
- `requirement-intake-rules`（`gap-routing`）
  - 做什么：识别需求描述里的缺口、歧义和未收敛项。
  - 建议：必须串行，它负责先把需求补完整，再进入后续工作。
- `requirement-boundary-rules`
  - 做什么：定义需求边界、范围、排除项和优先级。
  - 建议：必须串行，它负责为下游工作定边界。
- `api-endpoint-rules`
  - 做什么：约束 HTTP 接口、路由、方法和入口职责。
  - 建议：必须串行，接口未冻结前不要并行展开下游实现。
- `database-schema-rules`
  - 做什么：定义或修改数据库表、字段、索引和迁移顺序。
  - 建议：必须串行，schema 归属和迁移顺序未冻结前不要并行。
- `skill-execution-compliance-gate-rules`
  - 做什么：在最终收口前检查已命中 skill 是否完整执行，汇总计划内未完成必需项与阻断候选。
  - 建议：必须串行，它是执行合规闸门，不适合并行跑。
- `code-change-finalization-gate-rules`
  - 做什么：在最终收口前检查代码/测试改动是否完成注释、测试、真实运行验证与提交前风格闸门。
  - 建议：必须串行，它是代码收口闸门，不适合并行跑。
- `mcp-installation-rules` / `plugin-installation-rules` / `thread-title-rules` 的 provisioning **写 config 安装 / 注册**
  - 做什么：向 config 文件写入 / 补齐 MCP、插件、工具的注册表项。
  - 建议：必须串行，集中到单一“安装子 agent”独占对应 config 文件的写；同一时刻至多一个安装子 agent 活跃，绝不并行两个 config 写入者。目录级、写集互斥的 `npm ci` 等可并行，但任何 config 写不得并发。细则见 `provisioning-delegation.md`。

## 分发建议

- `parallel-task-dispatch-rules` 在一个入口内完成并行判定、线程规划、授权确认、真实启动、回收与关闭；不得只做规划而跳过生命周期证据。
- 注释补充、实现自审和当前 diff 总审查这类工作，只有在文件归属明确后才并行。
- 只读审查可以并行检查同一批文件；真正的代码修改、注释补写和格式修正仍要按文件写入串行。
- 同一文件内的代码修改和注释修改必须串行，不能拆成多个线程同时写。
- 先做根因、契约定义、schema 决策，再分发下游任务。
- 分析、侦察、分诊类任务优先拆只读 sidecar；最终根因、需求边界、契约、schema 和架构方向仍由主 agent 串行裁决。
- 如果两个候选 skill 都要修改同一个文件，直接收回为一个串行线程。
