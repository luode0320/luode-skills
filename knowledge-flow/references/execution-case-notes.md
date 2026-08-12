# 执行失败案例笔记

## 案例结构

每篇执行失败案例笔记使用追加式状态事件，包含正反例、验证证据和状态事件。

## 目录位置

- 固定目录：`20-Knowledge/execution-failure-cases/<owner>/<case_id>.md`
- owner 为负责该案例的 skill 名（如 `execution-failure-learning-rules`）
- case_id 为 ASCII slug

## 文件保护

- 该目录下的文件禁止移动和删除
- 仅允许追加内容（Add-Content）
- 巡检脚本跳过该目录（不参与状态分级处置）

## 状态事件

案例状态通过追加式状态事件记录：

```text
### 2026-08-12 | active | re-verified
- status: active
- event: re-verified
- 原因：同输入 local 复验通过
- 证据：验证命令输出
- 验证时间：2026-08-12
- scope: 适用范围
```

## 状态转换

- candidate: 候选，尚未验证
- active: 已验证且仍有效
- stale: 过期，需重新验证
- conflicted: 与其他案例冲突
- superseded: 已被新案例取代
- rejected: 已拒绝

状态事件格式为标题 `时间 | 状态 | 事件类型`，并在事件块内写入机器可读的 `status: <状态>` 与 `event: <事件类型>`；事件只追加不覆盖。允许转换：

| 当前状态 | 可追加状态 | 触发条件 |
| --- | --- | --- |
| `candidate` | `active` | 确定性证据或两次稳定 local 复验 |
| `candidate` | `stale` / `conflicted` / `rejected` | 证据过期、冲突未裁决或方案被证伪 |
| `active` | `stale` / `conflicted` / `superseded` | 版本/范围变化、冲突或被新方案替代 |
| `stale` | `active` | 重新按当前 scope 完成同输入 local 复验 |
| `conflicted` | `active` / `rejected` | 权威证据裁决其中一方 |
| `superseded` / `rejected` | 不自动恢复 | 需要创建新的 `case_key` 或人工裁决 |

`candidate` 阶段即可追加 `conflicted`：去重命中但方案不兼容时保留两条并双向标记，这与 `execution-failure-learning-rules` 的 `SKILL.md` 与 `case-template.md` 口径一致。

状态事件必须说明原因、证据、验证时间和 scope；不得只追加一个孤立状态词。
