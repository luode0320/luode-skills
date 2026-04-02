# 第 5 轮：删除后冒烟验证

## 执行方式

- 删除旧 `code-comment-rules` 后，运行 `run_codex_trigger_checks.ps1 -Phase post-delete`。
- 目标是确认新 skill 集合独立存在时，自动触发仍然稳定。

## 结果汇总

| 用例 | 预期 | 实际命中 | 结论 |
|---|---|---|---|
| `T5-01` | `comment-placement-granularity-rules`，且不得出现 `code-comment-rules` | `comment-placement-granularity-rules` | 通过 |
| `T5-02` | `comment-completion-gate-rules`，且不得出现 `code-comment-rules` | `comment-completion-gate-rules`、`comment-placement-granularity-rules`、`chinese-comment-rules`、`skill-compliance-gate-rules` | 通过 |
| `T5-03` | `chinese-comment-rules`，且不得出现 `code-comment-rules` | `chinese-comment-rules` | 通过 |

## 结果解读

- `T5-01` 证明 placement skill 已能单独承接“注释该不该写、放在哪里”的核心场景。
- `T5-02` 证明补注释场景已经切到双 comment skill + chinese + compliance 的新入口组合，不再依赖旧 skill。
- `T5-03` 证明语言边界场景仍能准确落到 `chinese-comment-rules`，没有被两个新 comment skill 抢走。

## 详细证据

- `test/2026-04-03_012320/skills/code-comment-rules/outputs/summary-post-delete.md`

## 结论

通过
