# WorkBuddy 官方市场规则吸收裁决表

> 本表是“需求、实施、Bug、测试”四域吸收官方精华的唯一裁决依据。吸收原则：只吸收本地缺失或本地更弱的规则；本地已更强时保留本地并记录裁决；不复制官方整套工作流、不新增同类 skill、不引入 `.codebuddy/specs/` 或 `--skip-tests`。

## 裁决结论总览

| 官方来源 | 官方精华 | 本地现状 | 裁决 | 落点 |
| --- | --- | --- | --- | --- |
| `requirements-driven-workflow/commands/requirements-pilot.md` | 需求 100 分质量门（功能清晰 30 / 技术具体 25 / 实现完整 25 / 业务上下文 20），达到 90 分才移交 | 本地需求接入有检查清单与缺口路由，但没有量化门禁 | 合并 | `requirement-intake-rules/references/workbuddy-quality-gate.md` |
| 同一文件 | 实施前先只读扫描代码库，形成上下文报告后再进入需求确认 | 本地实施规划有目录树与落点契约，但没有显式“先探索、总结发现、批准后编码” | 合并 | `implementation-planning-rules/references/pre-implementation-code-exploration.md` |
| 同一文件 | 需求达到 90 分后必须停下等用户显式批准再实施 | 本地已有需求稳定后移交实施规划，但批准闸门不显式 | 合并 | 需求质量门参考与实施规划规则 |
| `feature-dev/commands/feature-dev.md` | 深入理解代码库、识别未定义细节、设计后再实现 | 本地实施规划已覆盖零决策、落点与周期，但“先探索再设计”不显式 | 合并 | `pre-implementation-code-exploration.md` |
| `feature-dev/agents/code-architect.md` | 从最小改动、干净架构、务实平衡三个角度设计方案 | 本地已有多方案收敛与推荐路线要求 | 保留本地 | 无新增 |
| `requirements-driven-workflow/agents/requirements-review.md` | 代码审查按功能、集成、质量、性能评分 | 本地已有 `6-review` 风格回归与实施规划自审 | 保留本地 | 无新增 |
| `requirements-driven-workflow/agents/requirements-testing.md` | 风险导向测试：关键路径优先、真实场景、错误处理与集成验证 | 本地测试策略已有优先级模型与测试隔离红线 | 合并 | `test-strategy-rules/references/risk-based-test-conclusion.md` |
| `requirements-driven-workflow/commands/requirements-pilot.md` | `--skip-tests` 可跳过测试 | 本地 P0：测试不能跳过 | 不吸收 | 无 |
| 同一文件 | `.codebuddy/specs/` 目录落盘整套工作流 | 本地已用 `doc/` 与 skill references 统一管理 | 不吸收 | 无 |
| 同一文件 | `requirements-pilot` 阶段问答链与子代理链 | 本地已有实施规划、测试、审查分工 | 不吸收 | 无 |
| `feature-dev/commands/feature-dev.md` | Feature Dev 阶段问答链（发现、探索、澄清、架构、实现、审查、总结） | 本地四域 skill 已覆盖对应职责，不复制整套流程 | 不吸收 | 无 |
| `requirements-driven-workflow/agents/requirements-generate.md` | 技术规格直接映射文件、函数、接口、配置与验证 | 本地实施总览/周期已要求文件/符号落点与真实测试 | 保留本地 | 无 |

## 吸收后必须保持的边界

- 不新增 Skill 目录，不复制官方插件目录。
- 不引入 `.codebuddy/specs/`、`--skip-tests`、`requirements-pilot` 或 Feature Dev 阶段问答链作为正式入口。
- 本地四类 skill 仍是唯一 Owner；官方精华只作为 references 或正文补充。
- 所有吸收内容必须能回指官方只读路径与本地原规则，避免“为吸收而吸收”。

## 证据与校验

- 官方只读路径：`C:\Users\luode\.workbuddy\plugins\marketplaces\codebuddy-plugins-official\plugins\requirements-driven-workflow\...`、`...\feature-dev\...`。
- 本表与四份新增 reference、四个 `SKILL.md` references 区段保持一致；任一不一致即阻断收口。
