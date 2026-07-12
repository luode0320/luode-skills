# EVD-TASK-ARR-04-IMPL

## 实现

- `recovery_engine.py::RecoveryEngine.recover` 实现 adapter contract、组件 scope/capability 准入、一次 probe/复验、L2-L4 每层一次动作和 `wait_ready`。
- 支持只读/幂等安全恢复、非幂等 `manual_handoff`、缺能力 `blocked`、L5 checkpoint/resume 和原成功标准验证。

## 追踪

`SRC-ARR-002/003 -> DEC-ARR-002/003 -> REQ-ARR-003/REQ-ARR-NFR-003 -> AC-ARR-005/006 -> CYCLE-ARR-02 -> TASK-ARR-04 -> TEST-ARR-04 -> EVD-TASK-ARR-04-*`
