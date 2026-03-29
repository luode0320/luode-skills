---
name: test-regression-rules
description: 当 Bug 修复、原有功能迭代、公共模块修改、共享逻辑调整、接口兼容性变化后准备执行测试时触发。负责判定回归范围、选择回归用例、验证兼容性影响并输出回归结论；必须以 `artifact-storage-rules` 与 `test-location-rules` 为基准，把回归结论统一写回中央约定的测试任务主说明 `README.md`，并把详细回归案例、执行证据和补充说明放到同一时间戳根目录下的 ASCII 真实代码路径镜像目录中；不要用它代替 functional-validation-rules、test-strategy-rules 或测试资源管理类规则。
---

# 回归验证规则

只在“这次改动有没有把旧能力带坏”这个问题上使用这个 skill。
如果当前争议是当前需求本身有没有做对，请转交 `functional-validation-rules`；如果当前争议是环境或链路跑不通，请先回到 `test-strategy-rules` 重新分流。

## Skill 作用与适用场景

- 作为测试链路的收尾规则，负责改动后的兼容性与影响面验证。
- 约束回归范围判定、用例选取、结果留痕和待补测记录方式。
- 聚焦 Bug 修复、原有功能迭代、公共模块修改、共享逻辑调整和接口兼容变化后的影响扩散。
- 防止把“当前功能验证”与“历史能力回归”混成一件事。
- 保证回归结论先通过中文 README 对外说明，再用 ASCII 镜像路径承载详细证据。

## 自动触发信号

- Bug 修复、原有功能迭代、公共模块修改、共享逻辑调整、接口兼容性变化后准备执行测试。
- 当前功能验证已经完成，需要继续确认旧逻辑、已有流程、上下游依赖和兼容行为是否被破坏。
- 变更涉及公共方法、公共组件、共享配置、基础库或复用链路。
- 用户明确要求确认“修了这个问题，会不会影响别的地方”。
- 发现回归结论准备记录到 `testing/`、`analysis/`、中文说明目录之外的随意位置或其他非中央约定时间戳根目录位置。

## 进入后先做什么

1. 先确认当前需求或当前 Bug 的功能验证已经基本完成，不带着明显未收敛的新问题做回归。
2. 确认当前回归验证已经对应到中央约定的测试时间戳根目录。
3. 梳理本次改动的直接影响点、共享依赖、上下游链路和主要兼容风险。
4. 判断本轮回归属于局部回归、链路回归还是公共能力回归。
5. 决定哪些内容写入中文 README，哪些详细案例、日志、截图和执行明细放入 ASCII 镜像路径。

## 默认执行流程

1. 默认先读 `references/regression-scope-selection.md`，确定回归范围和用例选取方式。
2. 再读 `../artifact-storage-rules/references/path-map.yaml`、`../artifact-storage-rules/references/naming-templates.md` 与 `../artifact-storage-rules/references/update-policy.md`，确认测试时间戳根目录、中文主说明 `README.md`、ASCII 镜像路径和同一轮回归是否继续复用同一根目录。
3. 如果问题归属不清，可能混入功能验证或联调问题，再读 `references/regression-boundaries.md`。
4. 输出回归结论、风险项和未覆盖说明时，再读 `references/regression-template-and-examples.md`。
5. 给出回归通过、驳回或待补测结论，并明确是否需要回流编码域、Bug 域、联调域或测试策略域。
6. 回归范围未稳定前，不直接宣告任务具备交付条件。

## 权责边界与不负责事项

- 只负责旧能力兼容性与影响面验证，不负责当前需求本身是否实现正确，那属于 `functional-validation-rules`。
- 不负责测试优先级大盘设计和资源收口，那属于 `test-strategy-rules`。
- 不负责联调环境、上下游协议和链路打通问题定位，这类问题应先回到 `test-strategy-rules` 重新拆分验证路径。
- 不负责测试目录、命名、程序和文档如何组织，但必须服从 `test-location-rules` 的新结构。
- 如果回归无法开展，是因为需求、Bug 定义或改动本身尚未收敛，应先回流对应上游 skill。

## 需要暂停并确认的条件

- 当前功能验证尚未通过，直接做回归会掩盖主问题。
- 本次改动影响面不清，难以合理界定回归范围。
- 当前回归环境、历史数据或关键链路依赖不具备，结论可信度不足。
- 回归范围已经扩张到全量测试计划，需要升级到 `test-strategy-rules` 重新收口。

## 执行通过 / 驳回标准

- 通过：本次改动涉及的旧能力、关联链路、共享依赖和兼容行为在已判定回归范围内未发现新的破坏性问题；中文 README 已能清楚说明结论，详细案例和证据已落入 ASCII 镜像路径并可追溯。
- 驳回：本次改动引入了旧能力回退、兼容性破坏、公共链路异常，或关键回归范围未验证，无法证明“没有带坏别的地方”；或回归留痕继续散落在错误目录中。

## 执行结果归档要求

- 将回归结论统一记录到 `artifact-storage-rules` 约定的测试任务主说明 `README.md`。
- README 至少包含改动类型、回归范围、选取用例、执行环境、结论、未覆盖项和遗留风险。
- 详细回归案例、执行日志、截图、补充说明统一放到中央约定的测试时间戳根目录下的 ASCII 真实代码路径镜像目录中。
- 测试任务主说明位置、目录命名模板和同一轮回归的复用策略统一遵循 `../artifact-storage-rules/references/path-map.yaml`、`../artifact-storage-rules/references/naming-templates.md` 与 `../artifact-storage-rules/references/update-policy.md`。
- 如果同一需求存在多轮独立回归验证，应分别创建多个时间戳根目录，而不是把所有回归轮次混在一个目录里。

## references 读取规则

- 默认先读 `references/regression-scope-selection.md`。
- 在定位测试时间戳根目录、中文主说明 `README.md`、ASCII 镜像路径或判断是否继续沿用同一轮回归根目录时，先读 `../artifact-storage-rules/references/path-map.yaml`、`../artifact-storage-rules/references/naming-templates.md` 与 `../artifact-storage-rules/references/update-policy.md`。
- 只有在功能验证、联调验证、回归验证边界不清时，再读 `references/regression-boundaries.md`。
- 只有在需要回归结论模板和样例时，再读 `references/regression-template-and-examples.md`。
