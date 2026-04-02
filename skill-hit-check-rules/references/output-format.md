# 输出格式

每轮输出前先给出命中检查：

```text
Skill 命中检查：
- 命中 skill：`skill-a`、`skill-b`
```

如果未命中：

```text
Skill 命中检查：
- 命中 skill：无
- 原因：当前请求不满足任何已定义 skill 的触发条件
```

格式要求：

- 命中 skill 必须使用真实 skill 名称。
- 若命中多个，按相关度从高到低列出。
- 命中检查区块必须出现在本轮回复开头。

代码改动收口示例：

```text
Skill 命中检查：
- 命中 skill：`skill-hit-check-rules`、`comment-placement-granularity-rules`、`comment-completion-gate-rules`、`skill-compliance-gate-rules`
- 原因：本轮存在代码改动，且即将进入最终回复前收口，需执行注释补齐与完整性闸门检查
```
