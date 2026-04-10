# 命中检查清单

## 检查顺序

1. 读取当前用户提问。
2. 对照 skill `description` 的触发信号逐条匹配。
3. 记录命中的 skill 名称。
4. 输出命中结果后再进入主执行。

## 注释场景补充

- 当用户请求“补充注释”或“只改注释”时，命中列表至少包含：`comment-placement-granularity-rules`、`comment-completion-gate-rules`、`chinese-comment-rules`、`skill-compliance-gate-rules`。

## 图片输入场景补充

- 当检测到消息包含图片输入（例如 `<image ...>`）时，必须强制检查并命中 `image-redbox-focus-rules`。
- 在图片输入场景下，不得跳过该命中检查直接进入主任务执行。

## 代码改动收口场景补充

- 当本轮发生代码新增或修改，且准备输出最终回复时，命中列表必须包含：`comment-placement-granularity-rules`、`comment-completion-gate-rules`、`skill-compliance-gate-rules`。
- 当本轮发生代码新增或修改，且准备输出最终回复时，命中列表还必须包含：`cleanup-format-review-rules`、`syntax-check-review-rules`。
- 即使用户没有显式提到“注释”或“格式”，也不能跳过上述收口 skill。
- 若缺少任一 skill，先补命中并完成收口检查，再输出最终回复。

## 代码改动中段场景补充

- 当本轮首次发生代码新增或修改时，下一条中间进度消息就必须补做一次注释相关命中检查，不得等待最终回复。
- 当本轮执行链路较长并出现中间阶段总结时，必须再次复检注释相关命中状态，避免“前改后补”。
- 中段复检与最终收口复检都必须保留；两者不可相互替代。

## 判定原则

- 优先使用“是否满足触发条件”判定，而不是主观猜测。
- 可以多 skill 同时命中。
- 本 skill 不计入“业务命中 skill 列表”。

## Git 短指令场景补充

- 当用户输入执行型 Git 指令（如“提交git”“提交 git”“git提交”“commit一下”“帮我提交代码”）时，必须优先命中 `git-collaboration-rules`。
- 对“执行提交”和“审查提交”做意图区分：
  - 执行提交：命中 `git-collaboration-rules`。
  - 审查提交（如“review commit”“审核最近提交”）：命中 `code-review-automation-rules`。
- 不允许要求用户额外补充“测试已完成”“准备交付”这类描述后才触发 Git 提交流程。

## 自主执行场景补充

- 当任务是多步骤链路，且当前阶段完成后存在可直接执行的下一步（非关键决策/高风险节点），必须检查并命中 `autonomous-execution-rules`。
- 该检查不仅在最终回复前做；中间阶段切换时也要做，避免“停在建议下一步”。
- 若命中条件成立，不得输出“如果需要我可以继续”这类停顿话术。

## 漏触发防护

- 若不确定是否命中，先保守标记“候选命中”，再在输出中说明依据。
- 不允许跳过命中检查直接进入主任务。
- 不允许在已发生代码改动的情况下，直到最终回复才首次声明注释相关 skill 命中。
- 不允许在多步骤任务已具备继续条件时，遗漏 `autonomous-execution-rules` 并提前停顿。
