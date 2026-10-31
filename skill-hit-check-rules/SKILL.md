---
name: skill-hit-check-rules
description: 每轮任务开始时用于判断本轮应加载哪些 skill。触发条件覆盖：用户消息出现 Git 意图（提交/推送/看状态/看改动及同义表达）、需要判断知识库是检索还是沉淀、以及不确定边界场景（图片输入、逆向工程、测试资产、外部 skill 吸收、任务恢复）该命中哪个 skill 时。本 skill 只做一次轻量路由，不产出打卡字段、不登记延迟 gate、不阻断执行。
---

# Skill 命中判断

本轮开始时按 `description` 匹配该加载的 skill，然后把执行权交给对应 Owner。宿主已有按描述自动匹配的机制，这里只补宿主容易漏掉的边界判断。

## 三条固定判断

1. **Git 意图只看当前轮**：消息出现 `git`/`commit`/`push`/`pull`/`rebase`/`merge`/`stash`/`status`/`diff`/`log`，或「提交/推送/拉取/合并/变基/暂存/看下改动/同步到远端」时加载 `git-collaboration-rules`。历史轮次的授权不继承。
2. **知识库四态**：依赖历史决策或长期偏好 → 检索；形成可复用事实/决策/流程 → 沉淀；都不成立 → 不适用；目录不可读或写入后回读不一致 → 阻断。检索与沉淀加载 `knowledge-flow`。
3. **Plan Mode**：计划型请求加载 `implementation-planning-rules` 作为计划外壳，再按需回流需求、Bug、拆分等域；命中列表不得包含 `reasoning-summary-structure-rules`，计划出口由 `implementation-planning-rules` 独占。

## 容易漏触发的场景

- 消息含图片或截图 → `image-redbox-focus-rules`（有红框时优先看红框）。
- 逆向、反编译、脱壳、ASAR 拆包、APK/IPA 分析、PCAP/HAR 协议逆向 → `rea`。
- 新增或修改 `*_test.go`、测试程序、mock、fixture → `test-program-rules`，按需联动 `test-strategy-rules`。
- 用户说「吸收/借鉴/融合某个 skill」→ `skill-absorption-rules`。
- 新会话或消息含「继续/接着做/恢复任务」→ 先读 `PROJECT_CURRENT.md` 确认上次停在哪。
- 用户说「更新 md / 更新项目规则 / 补充仓库级规则」→ `context-recovery-rules`。

## 漏触发防护

- 宿主只显示名称不显示 `description` 时，名称相关的先读 frontmatter 再判定。
- 追问轮与普通轮同等判定；上一轮遗留待办不能吸收本轮新触发词。
- 「只命中名称」不算已执行，必须完成 Owner 的必需动作。
