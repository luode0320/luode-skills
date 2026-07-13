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
- `candidate`：已脱敏、去重并写入 Obsidian 的唯一 owner 案例笔记，等待晋级。
- `active`：获得 skill 维护授权，可用于 `prevent`/`recover`。
- `conflicted`：与现有案例或 owner 归属冲突，禁止自动复用。
- `stale`：环境/版本变化使适用性未知；先验证再恢复为 active。
- `superseded`：被更可靠方案替代，保留替代案例 ID。
- `rejected`：未通过门禁或被确认不可复用。

## 动态持久化

动态案例状态以 Obsidian 为唯一事实来源；静态 owner casebook 只读，作为种子、模板和离线回归基线。案例笔记固定落在：

`D:\obsidian_data\知识库\20-Knowledge\execution-failure-cases\<owner>\<case-id>.md`

所有检索、读取、创建和追加都必须经 `obsidian-knowledge-flow/scripts/obsidian_cli_bridge.py` 的公开 allowlist：

1. 写入前执行 `doctor --json`，断言固定 `vault_root`、非空 selector、`ok=true` 和 `verified=true`。
2. 以去重键执行 `search` 或 `search-context`，再对精确命中执行 `read`；从正文最后一个状态事件确定当前状态，不能只凭搜索摘要或 frontmatter 初始状态判断，也不能覆盖案例。
3. 未命中时使用 `create` 写入完整案例，并通过 bridge 追加 `知识库/30-MOCs/执行失败案例.md` 的唯一 backlink；命中时使用 `append` 追加 occurrence、验证证据或状态事件，不创建同键副本。
4. `create`/`append` 必须返回 `verified=true` 并完成 readback；任何 doctor、检索、写入或 readback 失败都停止持久化，保留结构化脱敏交接并报告 `candidate persistence: blocked`。
5. 状态变更采用正文中的追加式“状态事件”记录；不得直接重写或删除历史证据，也不得把动态状态同步回静态 casebook。

Obsidian bridge 故障本身按 `obsidian-knowledge-flow` 的 `recover` 路由处理；不得对同一 bridge 输入无变化重试，不得使用文件系统读写或静态 casebook 作为 fallback。

## recover 门禁

1. 保存最小脱敏证据和原成功标准。
2. 读取 owner 的 active 案例；没有精确匹配时只使用诊断，不盲目复制动作。
3. 对同一输入最多进行一次无变化复验。复验仍失败时必须改变假设、收集新证据或停止，不得循环重试。
4. 修复动作必须保持用户目标、数据安全和当前授权不变。
5. 仅在 `verified` 后进入 `learn`；否则保持诊断结果，不写可执行案例。

## 不可恢复时的阻断交接

当无变化复验已用尽、改变假设后仍无法满足原成功标准、恢复预算耗尽，或继续动作需要未获得的权限、外部依赖、不可逆操作时，当前 owner 必须停止自动尝试并生成一个 `BLK-*` 事实。该事实遵循 `../../artifact-delivery-gate-rules/references/task-blocker-closure-contract.md`，并至少写明失败类别和脱敏证据、已尝试动作、停止原因、对原任务的影响、责任方明确的恢复计划以及使用原输入和原成功标准的重入验证。

同一根因的去重键为“稳定错误码 + 关联证据”。`limited`、用户取消、预期负向测试和一次性未复验的抖动只保留当轮诊断，不得写成任务阻断或生成恢复计划。

## learn 门禁

candidate 自动写入前必须全部满足：

- 至少一次稳定复现或有确定性官方契约/代码证据；
- 根因和解决方案可用一句话清楚区分；
- 同输入、同成功标准、local 环境复验通过；
- owner 唯一，字段完整，敏感信息已脱敏；
- 按案例 ID、错误特征、工具/模型版本和适用边界完成去重；
- 方案不是预期负向测试、用户取消、权限阻断或一次性网络抖动。

满足以上条件后，按“动态持久化”流程在 Obsidian 创建或追加 `candidate`，并在交付报告标注案例路径和 readback 证据。静态 casebook 是否存在不影响动态写入；静态内容仅作为迁移种子和回归基线。owner 归属不唯一或无法建立安全案例路径时，只输出结构化交接，不创建无归属文件；若 bridge 未返回 `verified=true`，不得把案例标记为已写入，也不得在静态 casebook 中补写。

## active 晋级门禁

`candidate -> active` 需要当前轮明确的 skill 维护授权，并满足以下任一复用强度条件：

- 已在不同时间或相同稳定条件下复现至少两次；或
- 首次即有官方契约、确定性代码证据和可重复验证入口。

晋级前再次检查适用边界、禁止动作、版本范围和回滚方式。若新案例与 active 方案冲突，先将关系标记为 `conflicted`，不得静默覆盖；旧方案失效时使用 `superseded` 并记录替代 ID。

晋级只通过 Obsidian 案例笔记追加 `active` 状态事件，并在 readback 中确认状态事件、授权依据和验证证据均存在。静态 casebook 不承载晋级结果；其 `active` 示例只代表迁移前种子或回归输入。

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
| 执行工具的可复用失败与已验证恢复 | Obsidian 中唯一 owner 案例笔记的 candidate/active；静态 casebook 仅作种子/基线 |
