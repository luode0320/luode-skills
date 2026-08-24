# 来源说明

## 吸收来源

当前 skill 的实施规划工作流主要吸收自：

- `obra/superpowers`
- 参考文件：`skills/writing-plans/SKILL.md`
- `softspark-ai-toolkit-grill-me`（LobeHub，v1.0.1）
  - 吸收落点：`references/plan-devils-advocate-review.md`（方案反方批判）、`references/plan-review-checklist.md`（反方批判检查节）
  - 吸收内容：魔鬼代言人反方批评（挑战方案假设、反方结论、不通过回比选）
- `skillmd.ai/tdd`（SkillMD 生态，Kent Beck / Michael Feathers / Fowler 方法 + Ousterhout 反方）
  - 吸收落点：`references/tdd-workflow.md`（红→绿→重构节奏）
  - 吸收内容：测试先行实现节奏（无失败测试不写生产代码、一次一个行为、三个 TDD pattern、使用/跳过时机、Ousterhout 反方平衡）
- 外部「任务拆解 / 任务拆解规划」skill（目标→可执行计划拆解，SkillHub 生态）
  - 吸收落点：`references/plan-review-checklist.md`（任务表体检节）、SKILL.md（不承诺工期/不指定负责人规则）
  - 吸收内容：重复任务/依赖环/无人负责事项/顺序冲突检查；不凭空承诺工期与负责人
  - 未吸收：预计工时估算（本地刻意去掉时间分箱）、单一责任人分配（本地零决策执行模型）、CSV/JSON 导出（本地落盘文档体系）
- `dw-goal-breakdown`（SkillHub，v1.0.0，作者 Dream，MIT）
  - 吸收落点：`references/goal-breakdown-seed.md`（模糊目标的轻量拆解入口）、SKILL.md（自动触发信号 + references 引用）
  - 吸收内容：倒推法 3 层拆解（澄清目标+deadline → 周→日动作 → 首个最小可行步）、"首个最小可行步"下沉到第一个最小任务
  - 未吸收：源文件排版缺陷（逐字换行乱码、`示例: None` 占位）
  - 方法本体单一权威在 `long-run-loop-rules/references/goal-breakdown-before-loop.md`，本文件只承接工程域使用时机与衔接
- `conductor`（Context-Driven Development，市场 `codebuddy-plugins-official/external_plugins/conductor` 只读缓存，Google Conductor 的 Claude Code 移植版，Apache-2.0）
  - 吸收落点：`references/task-execution-protocol.md`（执行期状态管理协议）、SKILL.md（references 读取规则 1 条）
  - 吸收内容：任务状态标记五态（`[ ]`/`[~]`/`[x]`+SHA/`[-]`/`[!]`）、阶段检查点机制（本地适配版去掉人工审批）、偏差标注格式（DEVIATION/Reason/Impact 三级 + 四类型分层）、按工作单元语义回滚（周期/阶段/任务靠 plan 内 SHA 定位）、任务规模量化指南（2-4 阶段/8-20 任务）、实施前上下文校验、git notes 可选增强
  - 未吸收：阶段检查点的人工审批等待（本地零决策执行模型，放行走既有闸门）、plugin 命令形态、conductor/ 专属目录与 metadata.json（artifact-storage path-map + PROJECT_CURRENT.md 已有等价）、覆盖率 80% 硬目标（test-strategy-rules 管覆盖策略）、上下文反模式清单（project-memory-rules 管记忆维护）

## 当前改写策略

- 不保留外部种子为长期独立 skill，直接吸收到你们自有体系。
- 保留"编码前先写实施规划、先锁定文件落点、计划要可执行可验证"的核心思路。
- 去掉过重的时间分箱、超细模板和执行编排绑定。
- 改写为适合你们仓库长期维护、自动触发优先的中文版本。
