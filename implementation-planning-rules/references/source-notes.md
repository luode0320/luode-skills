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

## 当前改写策略

- 不保留外部种子为长期独立 skill，直接吸收到你们自有体系。
- 保留"编码前先写实施规划、先锁定文件落点、计划要可执行可验证"的核心思路。
- 去掉过重的时间分箱、超细模板和执行编排绑定。
- 改写为适合你们仓库长期维护、自动触发优先的中文版本。
