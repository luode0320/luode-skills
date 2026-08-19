# 测试策略维度

- 任务类型：新需求、Bug 修复、配置变更、公共能力调整。
- 风险类型：功能正确性、联调链路、兼容性回归、性能或安全影响。
- 资源条件：时间、环境、数据、上下游可用性、自动化基础。
- 交付要求：是否必须给出明确关闭口径或上线前结论。
- 任务拆分：是否需要把本次测试拆成多个独立时间戳测试主文档。
- 记录落点：测试策略摘要必须统一回写到 `doc/5-tests/yyyy-MM-DD_HHmmss_<测试任务中文主题>.md`；活动测试代码与运行所需 fixture、mock、stub、fake、helper 留在根 `test/`，源码关联资产按被测源码路径镜像。
- **可选专项维度**（吸收自 API测试自动化专家版，按需启用，非默认必测）：
  - 契约维度：上线门禁或跨团队接口需要防漂移时启用 → 按 `apifox-cli__skillhub/modules/test-contract.md` 建结构断言用例。
  - 性能维度：接口响应慢、上线前需要性能基线时启用 → 按 `apifox-cli__skillhub/modules/test-performance.md` 落地（apifox 重复执行 + 响应时间断言，不做 JMeter 级压测）。
  - 健康评分维度：上线前需要整体健康度或定期巡检时启用 → 按 `apifox-cli__skillhub/modules/test-health-score.md` 五层评分；安全/稳定维度无数据源时按 0 计并明示。
  - YAML 定义维度：大批量接口需要系统化定义测试时启用 → YAML 仅作设计表达，执行统一走 apifox（`apifox-cli__skillhub/modules/test-yaml-definition.md`）。
