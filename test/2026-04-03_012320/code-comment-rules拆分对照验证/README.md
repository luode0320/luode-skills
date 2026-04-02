# `code-comment-rules` 拆分对照验证

## 测试目的

验证旧 `code-comment-rules` 作为冻结基线保留时，新拆分出的 `comment-placement-granularity-rules` 与 `comment-completion-gate-rules` 是否能够在多轮不同模式测试中完整承接原有规则，并在删除旧 skill 后仍保持自动触发能力。

## 测试对象

- 旧 skill：
  - `code-comment-rules`
- 新 skill 集合：
  - `comment-placement-granularity-rules`
  - `comment-completion-gate-rules`
  - `chinese-comment-rules`

## 真实测试资产入口

- 轮次 1：`test/2026-04-03_012320/skills/code-comment-rules/round1-static-coverage.md`
- 轮次 2：`test/2026-04-03_012320/skills/code-comment-rules/round2-auto-trigger-cases.md`
- 轮次 3：`test/2026-04-03_012320/skills/code-comment-rules/round3-combined-routing-cases.md`
- 轮次 4：`test/2026-04-03_012320/skills/code-comment-rules/round4-real-code-drill.md`
- 轮次 5：`test/2026-04-03_012320/skills/code-comment-rules/round5-post-delete-smoke.md`
- 触发验证脚本：`test/2026-04-03_012320/skills/code-comment-rules/run_codex_trigger_checks.ps1`
- 真实样本代码：`test/2026-04-03_012320/skills/code-comment-rules/sample_comment_target.go`

## 执行前置条件

- 旧 `code-comment-rules` 在对照验证阶段保持冻结，不继续新增规则。
- 两个新拆分 skill 均已创建 `SKILL.md`、`agents/openai.yaml` 与 `references/`。
- 验证脚本使用本地 `codex exec` 读取当前仓库 skill 元数据，按提示词做真实命中检查。

## 执行方式

- 第 1 轮使用静态覆盖对照与结构校验。
- 第 2 轮使用真实 `codex exec` 提示词执行自动触发检查。
- 第 3 轮使用复合提示词验证多 skill 协同与边界路由。
- 第 4 轮使用真实样本代码做旧 skill 冻结基线对照与新 skill 集合承接验证。
- 删除旧 `code-comment-rules` 后，再补一轮删除后冒烟验证，确认新 skill 集合单独可用。

## 依赖数据与环境

- 仓库路径：`C:\Users\Administrator\.codex\skills`
- 执行环境：Windows PowerShell + 本地 `codex exec`
- 时间戳根目录：`test/2026-04-03_012320`

## 覆盖范围

- 旧规则零丢失映射
- 新 skill description 自动触发能力
- 复合场景下的多 skill 协同命中
- 真实代码样本上的注释放置、补齐闸门和中文表达边界
- 删除旧 skill 后的入口切换与自动触发冒烟验证

## 验证步骤摘要

1. 对照拆分预案，逐条检查旧规则映射与新 skill 落点。
2. 运行 `quick_validate.py` 校验新 skill 结构。
3. 执行 `run_codex_trigger_checks.ps1` 采集真实提示词命中结果。
4. 对照旧 skill 冻结基线与新 skill 集合输出，确认无规则丢失。
5. 删除旧 `code-comment-rules` 并更新外部依赖入口。
6. 再补删除后冒烟验证，确认新 skill 集合独立可用。

## 实际结果

- 第 1 轮静态覆盖对照通过：`code-comment-rules` 拆出的 15 条原规则均已映射到 `comment-placement-granularity-rules`、`comment-completion-gate-rules` 与 `chinese-comment-rules`，且相关 skill 结构校验通过。
- 第 2 轮与第 3 轮在旧 skill 冻结保留阶段共执行 9 个提示词场景，其中 5 个直接通过，4 个暴露出旧 `code-comment-rules` 抢补注释入口、`comment-completion-gate-rules` description 边界偏弱的问题。
- 针对上述缺口，已补强 `comment-completion-gate-rules` description，并把 `skill-hit-check-rules`、`skill-compliance-gate-rules`、`implementation-review-rules`、`code-readability-rules`、`code-minimal-change-rules`、`team-development-rules` 等入口切到双 comment skill。
- 第 4 轮真实代码样本演练通过：旧 `code-comment-rules` 基线指出的 4 类关键规则缺口，已能由新 skill 集合在同一样本上完整覆盖，不存在关键结论丢失。
- 第 5 轮删除后冒烟验证通过：3 个删除后提示词场景全部通过，且结果中不再出现 `code-comment-rules`，证明新 skill 集合已能独立自动触发。

## 未通过项 / 风险项

- 预删轮的失败项已经通过入口调整和旧 skill 删除后的冒烟验证完成回补，但仍建议后续继续补更多自然语言变体提示词，覆盖更口语化、更模糊的用户表达。
- `codex exec` 命中验证已是真实本地代理运行，不是纯文档推演；但它仍属于提示词级自动触发验证，不等于平台更高层策略的所有优先级都已穷尽。

## 详细证据路径

- `test/2026-04-03_012320/skills/code-comment-rules/`
- `test/2026-04-03_012320/skills/code-comment-rules/outputs/summary-pre-delete.md`
- `test/2026-04-03_012320/skills/code-comment-rules/outputs/summary-post-delete.md`

## 结论

通过

## 下一步流转建议

1. 当前拆分与删除收口已经闭环，可以把后续验证重点转到新增提示词样本扩容，而不是继续保留旧 skill。
2. 若后续再补 comment 相关规则，优先落到两个新 skill 或 `chinese-comment-rules`，不要重新引入大而全的单体 comment skill。
