# EVD-RT-C17-03-IMPL

## 结论

C17-03 已完成场景硬门禁切换规则。场景门禁只有在最近连续三次 local 运行满足 P0/P1 覆盖完整、场景全部 PASS、清理无失败且无未解释差异时才可放行；硬切后请求 legacy 会被固定阻断。

## 实现范围

- `gate.py` 新增连续窗口资格计算和硬切模式约束。
- `cli.py` 新增 `gate_history`、`gate_state` 读取和 `SCENARIO_CUTOVER_NOT_READY` / `LEGACY_FALLBACK_FORBIDDEN` 阻断。
- 兼容 CLI 新增 `release-run` 别名和 `--gate-mode/--scenario-catalog/--gate-history/--gate-state`。

## 安全边界

门禁历史、状态和场景目录都必须位于项目根内；非 local 或路径越界直接阻断，不自动回退旧门禁。

