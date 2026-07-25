# EVD-RT-C16-01-IMPL

- 完成 `LocalProbeRegistry`、`state.probe` 分派和 allowlist-only 运行边界。
- 场景禁止携带 SQL、Python、代码或路径读取；探针实现只可由项目运行时注册。
- 外部步骤断言先执行，失败后不运行探针，探针不能把外部 FAIL 改写为 PASS。
