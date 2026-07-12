# EVD-TASK-ARR-01-IMPL

## 实现

- 新增 `agent-runtime-recovery-rules/SKILL.md`、状态机、能力矩阵和平台无关 adapter 契约。
- 冻结 L0-L5、`manual_handoff`/`blocked`、一次 probe + 一次不变复验、L2-L4 分级动作和非幂等保护。

## 追踪

`SRC-ARR-001/002 -> DEC-ARR-001/003 -> REQ-ARR-001/RULE-ARR-001 -> AC-ARR-001/002 -> CYCLE-ARR-01 -> TASK-ARR-01 -> TEST-ARR-01 -> EVD-TASK-ARR-01-*`
