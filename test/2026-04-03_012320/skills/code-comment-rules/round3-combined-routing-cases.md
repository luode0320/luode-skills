# 第 3 轮：组合场景与多 skill 协同验证

## 执行方式

- 使用 `run_codex_trigger_checks.ps1` 的 `pre-delete` 阶段执行 3 个复合提示词。
- 目的不是只看单一命中，而是验证多个 comment 相关 skill 是否能协同承接。

## 结果汇总

| 用例 | 预期 | 实际命中 | 结论 |
|---|---|---|---|
| `T3-01` | `comment-completion-gate-rules` + `comment-placement-granularity-rules` | `code-comment-rules`、`comment-completion-gate-rules`、`chinese-comment-rules`、`skill-compliance-gate-rules` | 未通过 |
| `T3-02` | `comment-completion-gate-rules` + `chinese-comment-rules` | `code-comment-rules`、`chinese-comment-rules`、`skill-compliance-gate-rules` | 未通过 |
| `T3-03` | `comment-placement-granularity-rules` + `chinese-comment-rules` | `comment-placement-granularity-rules`、`chinese-comment-rules` | 通过 |

## 发现的问题

1. `T3-01` 说明“补注释 + 风险分支是否需要步骤注释”仍会因为旧 skill 抢入口而丢掉 placement 维度。
2. `T3-02` 说明“补注释 + 第三方固定错误原文”场景中，gate skill 还未稳定进入复合命中链路。

## 修正动作

1. 将 `skill-hit-check-rules` 与 `skill-compliance-gate-rules` 的补注释默认命中清单切到双 comment skill 模型。
2. 保留 `chinese-comment-rules` 只承接语言表达，不再让旧 skill 兜底整个场景。

## 结论

预删轮发现复合路由缺口，已据此回改
