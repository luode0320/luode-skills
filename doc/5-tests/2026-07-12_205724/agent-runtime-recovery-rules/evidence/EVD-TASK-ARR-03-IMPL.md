# EVD-TASK-ARR-03-IMPL

## 实现

- `recovery_state.py` 实现原子 checkpoint、白名单字段、`scope_hash`、`expires_at`、损坏/过期拒绝和单飞锁。
- checkpoint 不保存原始 scope、业务数据、prompt、response、token 或凭据；状态支持 `resumed -> healthy`。

## 追踪

`SRC-ARR-003 -> DEC-ARR-002 -> REQ-ARR-002 -> AC-ARR-003/004 -> CYCLE-ARR-02 -> TASK-ARR-03 -> TEST-ARR-03 -> EVD-TASK-ARR-03-*`
