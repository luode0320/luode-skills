# 案例模板与去重

## Canonical candidate 模板

以下字段是案例笔记的 canonical frontmatter；字段值必须脱敏。没有值时写 `unknown`，不要用猜测填充。动态 candidate/active 必须写入 Obsidian，静态 owner casebook 只保留同结构的种子和回归基线。

```yaml
id: <owner>-<short-slug>-<stable-id>
type: knowledge
title: "执行失败案例：<short-slug>"
knowledge_kind: execution_case
status: candidate
owner_skill: <唯一 owner skill>
storage: obsidian
case_key: <按去重字段规范化后的稳定键>
obsidian_path: 知识库/20-Knowledge/execution-failure-cases/<owner>/<case-id>.md
seed_source: <静态 casebook 路径或 unknown>
aliases: []
tags: [execution-failure]
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
confidence: low | medium | high
mode: prevent | recover | learn
failure_stage: <调用阶段>
category: input-contract | environment | auth | transport | tool-contract | artifact | workflow
environment: local
tool_or_model: <名称与版本摘要>
error_signature: <状态码/退出码/稳定错误特征，不含 secret>
minimal_input: <可复现的非敏感摘要>
root_cause: <已验证根因>
solution: <可执行恢复或预防步骤>
verification:
  command_or_entrypoint: <验证入口>
  success_criteria: <原成功标准>
  result: passed
scope: <适用版本、输入和边界>
avoid: <禁止动作>
source: <任务/日志/案例来源的脱敏标识>
occurrences: 1
first_observed: <YYYY-MM-DD>
last_verified: <YYYY-MM-DD>
replaces: null
related: []
```

## Obsidian 案例正文

每篇动态案例笔记在 frontmatter 后保留以下固定章节，便于检索和读回校验：

- `## 失败特征与反例`：稳定错误信号、错误动作和可观察失败；不得粘贴 secret、完整响应或私有输入。
- `## 正确方案`：已验证的预防/恢复动作，以及必须保持的原输入和成功标准。
- `## 适用范围与禁止动作`：工具/模型版本、local 环境、输入边界、回滚方式和不得执行的动作。
- `## 验证证据`：同输入、同成功标准、local 复验入口和 `verified` 结果；只写最小脱敏证据。
- `## 状态事件`：按时间追加 `candidate`、`active`、`conflicted`、`stale`、`superseded` 或 `rejected` 事件，包含状态、原因、授权/证据引用和时间。最新事件决定当前状态，历史事件不得删除；读取案例时必须 `read` 正文并以最新事件为准，不能只看 frontmatter 初始 `status`。

推荐的状态事件格式：

```text
- 2026-07-14 | status=candidate | reason=<脱敏原因> | evidence=<验证证据标识> | authorization=<授权标识或 N/A>
```

## Bridge 写入流程

1. 运行 `python obsidian-knowledge-flow/scripts/obsidian_cli_bridge.py doctor --json`，确认固定 vault、唯一 selector、`ok=true` 和 `verified=true`。
2. 用 `search`/`search-context` 查询 `case_key`、`owner_skill` 和 `error_signature`，再对精确命中使用 `read`；搜索摘要不能作为状态事实。
3. 无精确命中时用 `create --path <obsidian_path>` 写入完整笔记，并通过 bridge 追加 `知识库/30-MOCs/执行失败案例.md` 的唯一 backlink；命中时只用 `append` 增加 occurrence、验证证据或状态事件，禁止新建同键副本。
4. `create`/`append` 必须返回 `verified=true` 并完成 readback。bridge 失败时案例状态为“未持久化”，报告 `candidate persistence: blocked`，不得写回静态 casebook 或用文件系统 fallback。

## 去重键

先规范化大小写、空白、绝对路径和动态 request id，再用以下字段组合判断重复：

`owner_skill + category + tool_or_model major version + error_signature + normalized minimal_input + scope`

命中同一去重键时更新原案例的验证时间、出现次数和来源，不新增正文。解决方案不同或边界不兼容时保留两条并标记 `conflicted`，等待裁决。

## 写入与引用规则

- candidate 必须经 bridge 创建或追加到 Obsidian 的唯一 owner 案例笔记，不能修改其他 skill 的案例正文。
- 静态 owner casebook 仅作为种子、模板和回归基线；执行期间不得追加 candidate/active，也不得把其状态当作动态事实来源。
- 其他 skill 需要复用时只引用 `owner_skill + id`，不要复制一份案例。
- active 案例必须包含可重复验证入口、禁止动作和适用范围；缺任一项不得晋级。
- 旧方案失效时更新其状态为 `superseded` 或 `stale`，填写 `replaces`/替代案例 ID；不要删除历史证据。
- 无法脱敏、无法复验、owner 不唯一或仅适用于一次性机器状态的记录标记 `rejected`，只保留在当轮诊断输出。

## 最小交付报告

```text
执行失败学习：<observed/classified/...>
失败类别：<category>
Owner：<skill> / <case-id 或无>
根因：<一句话>
恢复与验证：<动作；同输入 + 原成功标准 + local 结果>
案例变更：<candidate/active/stale/conflicted/rejected；路径>
```
