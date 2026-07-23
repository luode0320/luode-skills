---
name: git-collaboration-rules
description: 【强制触发】凡当前这轮用户消息出现 Git 协作动作即触发（显式关键词 + 隐式语义），包括“提交git/帮我提交/commit一下/推送代码/看下状态/看下改动”等；新会话第一条也必须触发。触发后必须与 skill-hit-check-rules 联动命中。默认执行“最小可执行闭环”：短清单 + 阻断脚本 + 统一证据模板。每次 `git commit` 前必须以当前 staged 改动为准完成基础代码核查：格式、注释、安全性、并发安全性、系统崩溃风险和边界条件；不得以最近审查文档替代或阻断该核查。用户明确请求“提交git”时，目标是清空当前全部未提交改动（staged、unstaged、untracked），允许按业务拆分多次提交，不要求一次提交完成，但必须循环到 `git status --short` 为空（除阻断项外）。
---

# Git 协作规则（最小闭环版）

## -1.4 极简硬闸门（新增，强制）

首条命中检查、允许的预检查命令和违规阻断统一引用 `skill-hit-check-rules/SKILL.md`；本 Skill 不重复固定行文本或模板格式。

## -1.5 首条输出收敛（新增，强制）

首条中间进度的字段、顺序和 Markdown 形式以 `skill-hit-check-rules/templates/hit-check-template.md` 为唯一来源。本 Skill 只要求 Git 意图被正确联动，不定义第二套首条协议。

## -1.6 违规自恢复（新增，强制）

未完成首条命中检查就执行 Git 命令时，按 `skill-hit-check-rules/SKILL.md` 的违规处理停止并重走命中检查；不得在本 Skill 维护重复恢复步骤。

## -1. 触发确认（强制）

当前轮用户消息包含 Git 协作关键词或等价语义时自动触发；授权只基于当前轮，不得继承历史轮次。完整授权契约见 `references/current-turn-authorization.md`。

## -1.8 当前轮次授权边界（新增，强制）

- `status/diff/log` 等只读意图只授权对应盘点范围。
- `commit/push/pull/rebase/merge` 等写历史或同步动作必须由当前轮明确意图授权。
- 当前轮未授权时必须停止；Obsidian 判断、历史指令、已进入 Git 流程或上一轮提交均不构成授权。

细则见 `references/current-turn-authorization.md`。

## -1.0 新会话首轮保障（强制）

新会话与普通轮次使用同一触发和首条协议；统一引用 `skill-hit-check-rules`，不在此复制固定格式。

## -1.1 语义触发扩展（强制）

以下均视为 Git 协作：提交、推送、拉取、合并、变基、暂存、查看状态、查看差异、查看提交记录，以及“把改动交了”“同步到远端”等语义等价表达。

## -1.2 联动前置（强制）

本 Skill 命中时必须联动 `skill-hit-check-rules`。首条字段和允许的前置盘点动作完全引用该 Owner，不在此重复。

## -1.3 口语与缩写兜底（强制）

`提交git`、`git提交`、`commit下`、`push下`、`提一下`、`交一下`、`推一下`、`拉一下`、`同步代码` 等口语不得漏判。

## -1.7 用户显式放行未由代理改动文件（新增，强制）

默认保护非本轮代理产生的改动；只有用户当前轮明确表示“一起提交 / 都提交”才允许纳入，并在最终证据中列明。详细边界见 `references/current-turn-authorization.md`。

## 0. 首条中间进度（强制）

统一执行 `skill-hit-check-rules/SKILL.md` 与其模板；本 Skill 不拥有固定首条格式。

## 1. 执行短清单（强制按顺序）

1. 盘点工作树、staged、unstaged、untracked 与当前分支。
2. 按 `references/commit-scope-and-clean-tree.md` 冻结提交域和清空目标。
3. 每次提交前按 `references/staged-review-and-evidence.md` 对当前 staged 改动完成基础代码核查与基础验收。
4. 写入 README 提交日志并设定合规标题。
5. 按 `references/pre-post-gates.md` 执行 pre gate。
6. 执行 `git commit`，正文使用真实换行，禁止字面量 `\n`。
7. 按 `references/pre-post-gates.md` 执行 post gate，失败时修正当前提交。
8. 用户目标为“提交git”时按提交域循环，直到 `git status --short` 为空或出现明确阻断。
9. 按证据模板列出本轮所有 commit、核查范围、验证结果、放行文件和阻断项。

## 1.1 脚本查找与缺失回退（强制）

脚本归属、查找优先级、pre/post 检查和等价回退均由 `references/pre-post-gates.md` 定义。现有 `scripts/pre_commit_gate.sh` 与 `scripts/post_commit_gate.sh` 保持本 Skill 所有，不迁移、不复制。

## 2. 阻断条件（脚本化/回退等价）

- 当前轮授权不足或试图继承历史授权。
- 用户未放行却准备纳入非代理改动。
- 标题、README 日志、提交域隔离、测试落点或服务层落点不合规。
- staged 基础核查发现 P0/P1、格式、注释、安全、并发、崩溃、边界或验证阻断。
- pre/post gate 或等价回退未完整通过。
- 最新 commit 正文含字面量 `\n`。

详细机械条件见 `references/pre-post-gates.md`，人工核查条件见 `references/staged-review-and-evidence.md`。

## 3. 统一证据输出（强制）

最终证据使用 `templates/evidence-template.md`；首条命中证据不重复定义。提交、基础核查、基础验收和不适用原因的填写规则见 `references/staged-review-and-evidence.md`。

## 4. 通过标准

- 当前轮授权与实际 Git 动作一致。
- 每个 commit 只覆盖一个提交域；测试不与实现混提。
- 每次提交的 staged 基础核查和基础验收通过或有明确不适用依据。
- pre/post gate 均通过；脚本缺失时等价回退完整通过并标注。
- “提交git”场景最终工作树为空，除非存在已明确报告的阻断项。
- 最终证据列出全部 commit、用户放行文件、验证结果和阻断项；不因提交动作自动生成审查或验收文档。

## 5. 执行文件

- `scripts/pre_commit_gate.sh`
- `scripts/post_commit_gate.sh`
- `templates/evidence-template.md`
- `references/current-turn-authorization.md`
- `references/commit-scope-and-clean-tree.md`
- `references/pre-post-gates.md`
- `references/staged-review-and-evidence.md`
