# luode-skills × addy/agent-skills 结合改进方案

> 状态：评审稿（待确认）
> 性质：面向本仓库自身（skill 体系）演进的改进提案
> 参考来源：`github.com/addyosmani/agent-skills`（本地副本 `/d/tmp/agent-skills`，截至 PR #323）
> 编写：基于对 addy 全量 24 skill / 4 persona / 8 command / hooks / references 的深读，以及对本仓库 101 个 skill 的结构勘察

---

## 一、背景与目标

我们维护着一套 **101 个高度细分、强制触发、带 `doc/` 产物体系与字典机制的中文 skill 仓库**。addy 的 `agent-skills` 是 GitHub trending 的英文 skill 包，把研发抽象成 **DEFINE→PLAN→BUILD→VERIFY→REVIEW→SHIP** 六阶段生命周期。

本方案的目标：**在不推翻现有刚性骨架的前提下，把 addy 几个成熟的"认知层"模板嫁接进来**，补齐我们目前偏弱的环节（防偷懒、统一完成标准、多轴审查模板、飞行中质疑、生命周期主线），让 skill 体系既"管得住"又"骗不过去"。

**核心判断：嫁接，不是重构。**

---

## 二、两套体系基因对比

| 维度 | luode-skills（我们） | addy/agent-skills | 结论 |
|------|---------------------|-------------------|------|
| 组织方式 | 101 个原子 skill，按职责细分 | 24 个 skill，按 6 阶段生命周期 | 我们更细，但缺生命周期主线 |
| 触发机制 | 强制命中 + 阻断闸门（skill-hit-check） | 意图映射 + session hook 提示 | 我们刚性强 ✅ |
| 约束哲学 | 制度刚性（"必须做 / 禁止做"） | 认知对抗（"为什么不能偷懒"） | 互补，我们缺认知层 |
| 产物沉淀 | `doc/` 七大目录持久化体系 | `docs/` 轻量 + 内联 | 我们更完整 ✅ |
| 质量证据 | functional-validation 等分散 skill | 每个 skill 强制 Verification 收尾 | 可统一强化 |
| 可发现性 | skill-dictionary 自动字典 | README 表格 | 我们更工程化 ✅ |

**定位**：我们的体系是一台 **刚性约束机器**（管"必须 / 禁止"）；addy 是一套 **认知工作流**（管"如何不偷懒、如何算完成"）。

---

## 三、现状诊断（本仓库）

基于真实勘察（已用 md5/wc 校验，排除读取幻觉）：

- skill 写法为 **章节式 + 强制阻断式 + 中文 + 指向 `doc/` 产物 + 带 `references/` 子目录**（如 `acceptance-criteria-rules` 实为 80 行，含 acceptance-template / testable-criteria-checklist / acceptance-boundaries 三个引用）。
- 已有成熟优势：强制命中闸门、产物落盘闸门（artifact-delivery-gate）、skill 执行收口闸门（skill-compliance-gate）、字典自动生成。
- **相对空白**（对照 addy）：
  1. 缺"防偷懒 / 反借口对照表"这一认知拦截层；
  2. 缺一份"所有改动都要过的项目级固定完成清单（DoD）"；
  3. 审查 skill 偏 commit 粒度，缺"多轴矩阵 + 给结构化改法"统一模板；
  4. 所有 review 都是事后的，缺"建设中即时质疑"机制；
  5. 101 个 skill 缺一条把它们串起来的生命周期主线图。

---

## 四、五个结合点（按 ROI 排序）

### 🥇 结合点 1：注入「防偷懒对照表」（最高 ROI）

**addy 做法**：每个 skill 一张 Common Rationalizations 表，左列=agent 会用的借口，右列=反驳。

**我们现状**：命令式"必须/禁止"，但没有拦截 agent **自我说服跳过**的话术。

**具体改造**：在最容易被偷懒绕过的 skill 里新增固定章节 `## N. 防偷懒对照表`。优先注入对象：

| 目标 skill | 要拦截的典型借口 |
|-----------|----------------|
| `bug-fix-proposal-rules` | "先打个补丁特判一下就好" |
| `bug-root-cause-rules` | "我大概知道原因了，直接改" |
| `test-strategy-rules` | "这个太简单不用测""实现完再补测试" |
| `code-minimal-change-rules` | "顺手把旁边也清理了""一起重构更高效" |
| `implementation-review-rules` | "测试前先不归位，后面再说" |
| `final-acceptance-rules` | "差不多都过了，可以放行" |

**模板示例**（见附录 A）。该层为纯增量，不改现有刚性约束，是 `autonomous-execution-rules` 的天然搭档。

---

### 🥇 结合点 2：新增「项目级固定 DoD 清单」，与 AC 解耦

**addy 做法**：验收分两层——
- Acceptance Criteria（AC）= "做对了吗？"（每任务**变化**）
- Definition of Done（DoD）= "做完了吗？"（项目级**固定**，每个改动都要过）

**我们现状**：已有前置 AC（`acceptance-criteria-rules`）和后置最终验收（`final-acceptance-rules`），但**缺一份固定不变、每个改动都要过的完成清单**。

**具体改造**：新增 `definition-of-done-rules`（或并入 `acceptance-criteria-rules` 作固定章节），内容见附录 B。它与 `artifact-delivery-gate-rules`、`skill-compliance-gate-rules` 直接咬合——后两者已管"产物落盘"和"skill 执行完整性"，DoD 补上"质量/集成/交付"的固定底线。

---

### 🥈 结合点 3：审查升级为「五轴 + 四级 severity + 给改法」

**addy 做法**：五轴（正确性/可读性/架构/安全/性能）× 四级（Critical/Important/Suggestion/Nit）× structural remedy（给结构化改法）+ 必填"做得好的地方"+ change sizing（~100 行优、>1000 行必拆）+ Review tests first。

**我们现状**：已有 `code-review-automation-rules`、`project-change-review-rules`、`implementation-review-rules` 三个审查 skill，已有四级分级（致命/严重/中等/建议）。

**具体改造**：统一三个审查 skill 的输出模板为附录 C；并把 change sizing 写进 `code-minimal-change-rules`。

---

### 🥈 结合点 4：补「飞行中质疑」机制（doubt-driven）

**addy 做法**：`doubt-driven-development` = CLAIM→EXTRACT→DOUBT（新鲜上下文对抗式评审）→RECONCILE→STOP（3 轮上限）。价值在"做的过程中、不可逆决策点之前就便宜地验证"。

**我们现状**：所有 review 都是事后的。

**具体改造**：新增轻量 `doubt-driven-check-rules`，触发条件=高风险节点（引入新分支 / 跨模块 / 不可逆操作 / 不熟悉代码），用 subagent 做一次对抗式新鲜上下文评审，复用 `subagent-dispatch-rules` / `parallel-task-dispatch-rules` 的派发底座。

---

### 🥉 结合点 5：补「生命周期主线」与「并行 fan-out 放行」

**addy 做法**：6 阶段命令给用户清晰主线；`/ship` 并行起 reviewer/security/test 三个 persona 再 merge 出 Go/No-Go。

**我们现状**：101 个 skill 很全，但没有一条串起它们的主线图。

**具体改造**（轻量，不照搬命令）：
1. 在 `skill-hit-check-rules` 或字典里补一张"需求→实施→测试→审查→验收"主线图，标注每阶段默认命中哪些 skill（把 addy 的 `using-agent-skills` meta 地图本地化）；
2. 把 `/ship` 的并行 fan-out + merge 放行模式落进 `final-acceptance-rules`：最终验收时并行起"功能验证 + 回归 + 审查"三路 subagent，主流程汇总出放行/不放行 + 回滚方案。

---

## 五、落地路线（分三批，低风险增量）

| 批次 | 动作 | 涉及 skill | 风险 |
|:---:|------|-----------|:---:|
| **第一批**（纯增量） | ① 防偷懒对照表注入 6 个高频 skill ② 新建项目级 DoD | bug/test/review/验收域 | 极低 |
| **第二批**（模板升级） | ③ 五轴+四级审查统一模板 ④ change sizing 入 minimal-change | 三个 review skill | 低 |
| **第三批**（新机制） | ⑤ doubt-driven 飞行质疑 ⑥ 生命周期主线图 + fan-out 放行 | 新建 2 个 + final-acceptance | 中 |

**每批收口约束（沿用本仓库既有规矩）**：
- 改 skill 资产 → 必过 `skill-compliance-gate-rules`，给出 PASS/FAIL；
- 改了 description 或新增/修改 `##` 标题 → 重跑 `python skill-dictionary/generate_dictionary.py` 刷新 `data.js` 与 `字典.md`，禁止手改产物；
- 涉及 description/触发条件变更 → 追加 `skill-evolution-rules`。

---

## 六、明确不照搬的部分

- ❌ 不把 101 个 skill 压缩回 24 个生命周期 skill——细分度是优势，压缩会丢强制触发精度。
- ❌ 不引入 slash command 体系——我们已有更强的强制命中 + 阻断闸门，命令层冗余。
- ❌ 不照搬英文术语——新增内容全部沿用中文规范与 `doc/` 产物体系。

---

## 附录 A：防偷懒对照表模板

```markdown
## N. 防偷懒对照表（强制）

| 常见借口（agent 会这样自我说服） | 反驳与正确做法 |
|--------------------------------|---------------|
| "我大概知道根因，直接改" | 直接改的命中率有限，错判会浪费更多时间；必须先给静态证据链 |
| "这个太简单，不用走流程" | 简单逻辑往往成为被复制的模板，省掉的步骤会被放大十次 |
| "先打个补丁特判绕过" | 补丁式修复违反根因修复原则；必须从源头消除 |
| "差不多都过了，可以收口" | "差不多"不是完成判定；必须逐条回执 DoD/AC |
```

## 附录 B：项目级固定 DoD 清单（草案）

```markdown
# Definition of Done（项目级固定完成清单 · 每个改动都要过）

## 正确性
- [ ] 对应 AC 逐条满足
- [ ] 编译/运行通过（附证据）
- [ ] 新行为有测试覆盖，且无回归
- [ ] 边界/异常情况已处理

## 质量
- [ ] 命中 code-readability / code-style 一致性
- [ ] 无重复逻辑、无死代码
- [ ] 注释双闸门通过（placement + completion-gate）

## 集成
- [ ] 与全系统配合，迁移/配置到位
- [ ] 向后兼容（或显式声明破坏性变更）

## 文档
- [ ] doc/ 产物已落盘（联动 artifact-delivery-gate）
- [ ] 架构决策已记录

## 交付就绪
- [ ] 安全审查通过
- [ ] 有可观测性 / 有回滚路径
- [ ] 人工放行（final-acceptance）
```

> 说明：单任务完成时确认前两部分；功能级确认后两部分；发布级全部确认 + shipping 检查。

## 附录 C：五轴审查输出模板

```markdown
## 审查结论：<APPROVE / REQUEST CHANGES>
概述：<一句话总览>

### 逐轴检查
| 轴 | 结论 | 要点 |
|----|------|------|
| 正确性 | | 边界值/错误路径/测试有效性 |
| 可读性 | | 命名/控制流/死代码 |
| 架构   | | 模式一致/边界/抽象层级是否真正减少概念 |
| 安全   | | 输入验证/密钥/鉴权/注入 |
| 性能   | | N+1/无界操作/重渲染 |

### 问题清单（每条含 位置 + severity + 影响 + 具体改法）
- [致命] file.go:42 — <影响> — 改法：<结构化方案，不只指问题>
- [严重] ...
- [中等] ...
- [建议] ...

### 做得好的地方（必填）
- ...

### 验证情况
- 测试 / 构建 / 安全：<证据>
```

---

## 七、下一步

请评审本方案，确认：
1. 是否认可"嫁接而非重构"的总方向；
2. 从哪一批 / 哪个结合点开始动手；
3. 是否需要先出某个具体 skill 的防偷懒表 / DoD 正式草案。

确认后即按本仓库 skill 资产改动闸门（compliance-gate + 字典刷新）落地实现。
