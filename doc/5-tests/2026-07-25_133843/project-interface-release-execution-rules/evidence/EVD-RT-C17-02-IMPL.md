# EVD-RT-C17-02-IMPL

## 结论

C17-02 已完成 legacy/shadow 双轨对账。默认 `legacy` 不改变旧接口门禁；显式 `shadow` 加载项目根内的 verified 场景并真实执行；显式 `scenario` 使用场景门禁真值。

## 实现范围

- `gate.py` 新增 P0/P1 场景门禁、覆盖缺口、非通过场景、清理失败和差异分类。
- `cli.py` 新增 `gate_mode`、local 场景目录校验、场景执行和双轨报告透传。
- `scenario_runner.py` 结果携带声明的 `consumers`，供覆盖报告按消费者统计。
- `report.py` 将双轨差异写入 `dual-gate-diff.json`，未配置场景保持 `not_configured`。

## 停止边界

非 local 场景目录、P0/P1 覆盖缺口、场景失败、清理失败或未解释差异均不得报告 shadow PASS。
