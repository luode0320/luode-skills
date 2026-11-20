# 任务阶段的 skill 时机

不需要在开头预告本轮会触发什么。按真实发生的事，到点加载对应 skill 即可。

| 时机 | 加载 |
|---|---|
| 本轮有代码或测试改动，准备收口 | `code-change-finalization-gate-rules` |
| 本轮改了代码，需要风格回归 | `code-style-consistency-rules`（`6-review`） |
| 本轮新增或修改了注释位点 | `comment-rules` |
| 本轮会产出需求/实施/Bug/测试文档 | `artifact-delivery-gate-rules` |
| 工具、命令、API、环境出现非预期失败 | `execution-failure-learning-rules` |
| 准备 `git commit` | `git-collaboration-rules` |

补充两条：

- Bug 修复后验证是否真修好、有无副作用 → `bug-validation-rules`。
- 新功能或改动后验证行为是否符合需求 → `functional-validation-rules`。
