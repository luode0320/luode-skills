---
name: code-review-automation-rules
description: 当用户主动提出“审核代码”“review 当前分支提交”“审查最近提交”时触发。负责读取项目 `main` 分支最近一条提交时间，并仅审查当前分支在该时间之后且尚未并入 `main` 的提交，逐条输出中文结构化结果（致命/严重/中等/建议），再将汇总报告保存到 `artifact-storage-rules` 约定的 `doc/审查/` 主文档位置（同主题覆盖或按中央模板更新）；禁止跨提交混审，禁止把非当前 commit 引入的问题混入结论；不因本轮已有代码改动或准备最终收口而自动触发，这类场景由 `project-change-review-rules` 承接。
---

# 提交级代码审核规则

只在需要对“当前分支最近提交”做自动化代码审核时使用这个 skill。
如果用户只是做实现自检，不需要按 commit 逐条审查，请转实现审查类 skill。

## Skill 作用与适用场景

- 读取 `main` 最近一条提交时间，筛选当前分支在该时间之后的提交并逐条审查。
- 每个 commit 独立审查，避免跨提交混分析。
- 每个 commit 固定输出中文章节：审核摘要、致命、严重、中等、建议。
- 生成统一汇总报告并落盘到 `artifact-storage-rules` 约定的 `doc/审查/`，不再写入项目根目录固定文件名。

## 触发信号（显式）

- 用户明确说“审核代码”“review 当前分支”“审查最近提交”。
- 用户要求“按 commit 逐条审查并输出报告”。
- 用户明确要看“当前分支相对 `main` 的提交级问题清单”。
- 仅因本轮有代码改动、准备测试或准备最终收口，不触发本 skill。

## 进入后先做什么

1. 确认被审核项目根目录（即当前审核项目路径），并据此解析 `doc/审查/` 的报告落盘位置。
2. 获取当前分支名：`git rev-parse --abbrev-ref HEAD`。
3. 读取 `main` 最近提交时间并筛选当前分支有效 commit（时间正序审查）。
4. 对每个 commit 按固定提示词独立审核并汇总。
5. 将报告写入 `artifact-storage-rules` 约定的审查主文档位置，并根据主题复用或覆盖同一份报告。

## 默认执行流程

1. 默认先读 `references/review-workflow.md`。
2. 每个 commit 的提示词和输出格式读 `references/review-prompt-template.md`。
3. 报告落盘规则读 `references/report-and-wecom.md`。
4. 进入最终回复前，联动 `artifact-delivery-gate-rules` 核对审查报告是否已经真实落到 `doc/审查/`。

## 强制规则

- 分支必须是“当前分支”，不接收外部分支参数。
- 审核范围固定为：`main` 最新提交时间之后，当前分支且未并入 `main` 的提交。
- 不拉取远端、不解析远端引用。
- 不上报企业微信，仅本地生成报告。
- 每个 commit 必须完整输出：`审核摘要`、`致命`、`严重`、`中等`、`建议`。
- 即使无问题，也要在各级别写“无”。
- 禁止读取 `.gitignore` 忽略的文件和目录。
- 提交级审查报告的正式长期目录固定为 `doc/审查/`；禁止再写入项目根目录 `code_review_result.md` 一类平行入口。

## 权责边界与不负责事项

- 只负责提交级审查，不做自动修复。
- 不把历史问题错误归因到当前 commit。
- 不输出跨 commit 归因结论，除非能证明由该 commit 直接引入。
- 不参与默认自动审查链；当前 diff 总审查由 `project-change-review-rules` 承接，测试前实现闸门由 `implementation-review-rules` 承接。

## 执行结果归档要求

- 提交级审查报告必须归档到 `artifact-storage-rules` 约定的 `doc/审查/` 主文档位置，命名遵循中央模板，不再使用项目根目录固定文件名。
- 报告中至少包含时间、分支、项目路径、被审查 commit 列表，以及逐 commit 的中文结构化结论。
- 如果同一审查主题反复执行，应按 `../artifact-storage-rules/references/update-policy.md` 复用或覆盖同一份审查主文档，避免平行多份结果。
- 进入最终回复前，必须联动 `artifact-delivery-gate-rules`，核对当前提交级审查报告是否已经真实落到 `doc/审查/`；未落盘不得判定本轮提交级审查完成。

## 执行通过 / 驳回标准

- 通过：`main` 时间锚点之后的有效提交逐条审查完成，结构完整，报告已真实落盘到 `doc/审查/` 对应主文档。
- 驳回：漏审提交、输出结构缺失、或混入非当前 commit 引入的问题。

## references 读取规则

- 默认先读 `references/review-workflow.md`。
- 审核提示词固定读 `references/review-prompt-template.md`。
- 报告落盘规则读 `references/report-and-wecom.md`。
