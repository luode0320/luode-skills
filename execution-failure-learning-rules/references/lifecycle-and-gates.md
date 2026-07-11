# 生命周期与门禁

## 状态机

```text
observed -> classified -> reproduced -> diagnosed -> fixed -> verified -> candidate -> active
                                      |                         |             |
                                      +-> rejected               +-> conflicted +-> stale/superseded
```

- `observed`：有原始失败证据，但尚未分类。
- `classified`：已确定失败类别和唯一 owner。
- `reproduced`：同一输入或最小等价输入稳定复现；偶发抖动不得假定可复现。
- `diagnosed`：根因由错误输出、代码/契约证据或稳定实验支持。
- `fixed`：已应用恢复动作，但尚未按原标准验证。
- `verified`：同输入、同成功标准、local 环境验证通过。
- `candidate`：已脱敏、去重并写入 owner casebook，等待晋级。
- `active`：获得 skill 维护授权，可用于 `prevent`/`recover`。
- `conflicted`：与现有案例或 owner 归属冲突，禁止自动复用。
- `stale`：环境/版本变化使适用性未知；先验证再恢复为 active。
- `superseded`：被更可靠方案替代，保留替代案例 ID。
- `rejected`：未通过门禁或被确认不可复用。

## recover 门禁

1. 保存最小脱敏证据和原成功标准。
2. 读取 owner 的 active 案例；没有精确匹配时只使用诊断，不盲目复制动作。
3. 对同一输入最多进行一次无变化复验。复验仍失败时必须改变假设、收集新证据或停止，不得循环重试。
4. 修复动作必须保持用户目标、数据安全和当前授权不变。
5. 仅在 `verified` 后进入 `learn`；否则保持诊断结果，不写可执行案例。

## learn 门禁

candidate 自动写入前必须全部满足：

- 至少一次稳定复现或有确定性官方契约/代码证据；
- 根因和解决方案可用一句话清楚区分；
- 同输入、同成功标准、local 环境复验通过；
- owner 唯一，字段完整，敏感信息已脱敏；
- 按案例 ID、错误特征、工具/模型版本和适用边界完成去重；
- 方案不是预期负向测试、用户取消、权限阻断或一次性网络抖动。

满足以上条件后，将记录追加为 `candidate`，并在交付报告标注文件变更。owner 没有 casebook 时，只输出结构化交接，不创建无归属文件。

## active 晋级门禁

`candidate -> active` 需要当前轮明确的 skill 维护授权，并满足以下任一复用强度条件：

- 已在不同时间或相同稳定条件下复现至少两次；或
- 首次即有官方契约、确定性代码证据和可重复验证入口。

晋级前再次检查适用边界、禁止动作、版本范围和回滚方式。若新案例与 active 方案冲突，先将关系标记为 `conflicted`，不得静默覆盖；旧方案失效时使用 `superseded` 并记录替代 ID。

## 脱敏与 local-only 门禁

- 保留错误类型、状态码、退出码、工具版本、参数名和最小非敏感输入摘要；删除凭据值、完整响应、私有 prompt/图片、业务数据和绝对本机路径。
- 证据采集、修复和验证均只使用 local 配置。需要写入数据时必须有清理/回滚方案；禁止以“地址是 localhost”为理由使用非 local 配置。
- 案例包含的命令应使用占位符（如 `<workspace>`、`<token>`），不得复制用户原始 secret。

## 边界路由

| 判断结果 | 交付目标 |
| --- | --- |
| 产品/业务行为错误 | `bug-intake-rules` 及相关 `bug-*` 流程 |
| 代码异常处理、重试或错误映射设计 | `error-handling-rules` |
| 需求、规则、触发器或案例库职责缺口 | `skill-evolution-rules` |
| 可跨项目复用的稳定事实/决策 | `obsidian-knowledge-flow`，先检索再沉淀 |
| 执行工具的可复用失败与已验证恢复 | 唯一 owner casebook 的 candidate/active |
