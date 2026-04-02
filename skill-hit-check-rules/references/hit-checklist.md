# 命中检查清单

## 检查顺序

1. 读取当前用户提问。
2. 对照 skill `description` 的触发信号逐条匹配。
3. 记录命中的 skill 名称。
4. 输出命中结果后再进入主执行。

## 注释场景补充

- 当用户请求“补充注释”或“只改注释”时，命中列表至少包含：`comment-placement-granularity-rules`、`comment-completion-gate-rules`、`chinese-comment-rules`、`skill-compliance-gate-rules`。

## 代码改动收口场景补充

- 当本轮发生代码新增或修改，且准备输出最终回复时，命中列表必须包含：`comment-placement-granularity-rules`、`comment-completion-gate-rules`、`skill-compliance-gate-rules`。
- 即使用户没有显式提到“注释”，也不能跳过上述三个 skill。
- 若缺少任一 skill，先补命中并完成收口检查，再输出最终回复。

## 判定原则

- 优先使用“是否满足触发条件”判定，而不是主观猜测。
- 可以多 skill 同时命中。
- 本 skill 不计入“业务命中 skill 列表”。

## 漏触发防护

- 若不确定是否命中，先保守标记“候选命中”，再在输出中说明依据。
- 不允许跳过命中检查直接进入主任务。
