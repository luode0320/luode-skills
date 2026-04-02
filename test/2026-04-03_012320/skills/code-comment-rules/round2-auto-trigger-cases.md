# 第 2 轮：自动触发与路由验证

## 执行方式

- 使用 `run_codex_trigger_checks.ps1` 的 `pre-delete` 阶段执行 6 个单场景提示词。
- 旧 `code-comment-rules` 此时仍保留，作为冻结基线参与对照。

## 结果汇总

| 用例 | 预期 | 实际命中 | 结论 |
|---|---|---|---|
| `T2-01` | `comment-placement-granularity-rules` | `skill-hit-check-rules`、`comment-placement-granularity-rules` | 通过 |
| `T2-02` | `comment-completion-gate-rules` | `code-comment-rules`、`chinese-comment-rules`、`skill-compliance-gate-rules` | 未通过 |
| `T2-03` | `comment-completion-gate-rules` | `code-comment-rules` | 未通过 |
| `T2-04` | `chinese-comment-rules` | `chinese-comment-rules` | 通过 |
| `T2-05` | `api-swagger-rules` | `api-swagger-rules` | 通过 |
| `T2-06` | `comment-completion-gate-rules` + `comment-placement-granularity-rules` | `code-comment-rules`、`comment-completion-gate-rules`、`comment-placement-granularity-rules`、`chinese-comment-rules`、`skill-compliance-gate-rules` | 通过 |

## 发现的问题

1. `T2-02` 暴露出补注释场景仍被旧 `code-comment-rules` 抢入口，`comment-completion-gate-rules` 没有稳定自动触发。
2. `T2-03` 暴露出“普通流程注释是否必须改为编号步骤注释”这一场景在新 gate skill 的 `description` 中还不够突出。

## 修正动作

1. 扩写 `comment-completion-gate-rules` 的 `description`，明确把“函数头元信息补法”“步骤编号是否必须”“普通流程注释是否必须改写”写进触发条件。
2. 将 `skill-hit-check-rules` 从单体 `code-comment-rules` 切换为 `comment-placement-granularity-rules` + `comment-completion-gate-rules` + `chinese-comment-rules` + `skill-compliance-gate-rules` 的新入口组合。

## 详细证据

- `test/2026-04-03_012320/skills/code-comment-rules/outputs/summary-pre-delete.md`

## 结论

预删轮发现入口缺口，已据此回改
