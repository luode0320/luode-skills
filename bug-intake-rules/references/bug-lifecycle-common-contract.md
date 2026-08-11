# Bug 生命周期公共契约

本契约只承接所有 Bug 阶段共同的保护语义：只使用 local 配置、侦察优先只读、临时日志/断言/断点必须可清理、结论写回同一份 Bug 主文档、修复必须针对根因。它不替代复现、根因、修复建议、风险分级或验证的专属入口。

- 一句话 Bug、截图与信息缺口进入 `discovery-and-gap`；静态证据不足且需要观察状态时进入 `runtime-diagnostics`。
- 非 local 环境、写数据、无目标调试、将临时诊断保留为业务逻辑均为停止条件。
- Bug 是否关闭由 `bug-validation-rules` 判断；旧能力回归由 `test-regression-rules` 判断。
