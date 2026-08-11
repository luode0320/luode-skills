---
name: test-regression-rules
description: 当 Bug 修复、原有功能迭代、公共模块修改、共享逻辑调整、接口兼容性变化后准备执行测试时触发。负责判定回归范围、选择回归用例、验证兼容性影响并输出回归结论；必须以 `artifact-storage-rules` 与 `test-strategy-rules 的 test-asset-governance 条件路由` 为基准，把回归结论写回测试主文档，把可执行回归测试、mock、stub、fake、fixture 和 helper 放入根 `test/` 的源码镜像目录，并把详细回归案例、执行证据和补充说明放到同一份 `doc/5-tests/` 测试主文档的证据小节；模拟程序与对应回归测试使用同一源码相对路径，`doc/5-tests/` 仅保存非可执行证据；Go 测试还必须遵循 `test-program-rules` 的《Go 测试编译路径（强制）》；同时强制禁止为了测试目的污染生产代码。不要用它代替 functional-validation-rules、test-strategy-rules 或测试资源管理类规则。
---

# 回归验证规则

只在“这次改动有没有把旧能力带坏”这个问题上使用这个 skill。
如果当前争议是当前需求本身有没有做对，请转交 `functional-validation-rules`；如果当前争议是环境或链路跑不通，请先回到 `test-strategy-rules` 重新分流。

## 测试隔离红线（强制）

> 本节遵循 `test-strategy-rules` 的《测试隔离红线（强制）》单一权威来源：严禁为测试污染生产代码（新增测试专用方法/数据/结构体字段）、不得通过改造生产代码“配合测试”制造回归通过结果、发现污染立即判定回归结论无效并阻断、回归自动化只用 `local` 环境（禁连 `test`/`prod`/`staging` 等非 local 服务）。本 skill 不重复展开，仅承接回归验证侧的落地。

## 活动回归资产落点（强制）

- 回归测试程序、mock、stub、fake、fixture 和 helper 都是活动资产，必须放在根 `test/` 的源码相对路径镜像目录；例如被测 `internal/service/history_client.go` 的回归资产位于 `test/internal/service/`。
- mock、stub、fake 等模拟程序必须与对应回归测试使用同一镜像目录；只有跨多个源码路径稳定复用的模拟能力才可放入 `test/shared/`。
- `doc/5-tests/` 测试主文档 只保存扁平测试主文档，日志、报告、截图和脱敏响应样例等非可执行证据内联进正文，不得放置或复制回归测试程序、mock、stub、fake、fixture 或 helper。

## Skill 作用与适用场景

- 作为测试链路的收尾规则，负责改动后的兼容性与影响面验证。
- 约束回归范围判定、用例选取、结果留痕和待补测记录方式。
- 聚焦 Bug 修复、原有功能迭代、公共模块修改、共享逻辑调整和接口兼容变化后的影响扩散。
- 防止把“当前功能验证”与“历史能力回归”混成一件事。
- 保证回归结论先通过中文测试主文档 对外说明；可执行回归测试放在根 `test/`，详细证据只进入 `doc/5-tests/` 测试主文档的证据小节。

## 自动触发信号

- Bug 修复、原有功能迭代、公共模块修改、共享逻辑调整、接口兼容性变化后准备执行测试。
- 当前功能验证已经完成，需要继续确认旧逻辑、已有流程、上下游依赖和兼容行为是否被破坏。
- 变更涉及公共方法、公共组件、共享配置、基础库或复用链路。
- 用户明确要求确认“修了这个问题，会不会影响别的地方”。
- 发现回归结论准备记录到 `testing/`、`analysis/`、中文测试主文档之外的随意位置或其他非中央约定时间戳测试主文档位置。

## 进入后先做什么

1. 先确认当前需求或当前 Bug 的功能验证已经基本完成，不带着明显未收敛的新问题做回归。
2. 确认当前回归验证已经对应到中央约定的测试主文档，并核对回归测试、mock、stub、fake、fixture 和 helper 是否位于对应源码相对路径镜像；需要连接本地真实环境（数据库、缓存、消息队列、HTTP/RPC 上游等）做回归时，按 `test-strategy-rules` 的「本地环境配置发现与连接」去本地 `local` 配置文件读取连接信息，并遵守其隔离安全约束；不得改用 `test` / `prod` / `staging` 等非 local 环境连接。
3. 梳理本次改动的直接影响点、共享依赖、上下游链路和主要兼容风险。
4. 判断本轮回归属于局部回归、链路回归还是公共能力回归。
5. 决定哪些内容写入中文测试主文档，哪些详细案例、日志、截图和执行明细内联进测试主文档正文，并链接根 `test/` 回归测试文件。

## 默认执行流程

1. 默认先读 `references/regression-scope-selection.md`，确定回归范围和用例选取方式。
2. 再读 `../artifact-storage-rules/references/path-map.yaml`、`../artifact-storage-rules/references/naming-templates.md` 与 `../artifact-storage-rules/references/update-policy.md`，确认根 `test/` 镜像、测试主文档、测试主文档、证据目录和同一轮回归是否继续复用同一证据根目录。
3. 如果问题归属不清，可能混入功能验证或联调问题，再读 `references/regression-boundaries.md`。
4. 输出回归结论、风险项和未覆盖说明时，再读 `references/regression-template-and-examples.md`。
5. 给出回归通过、驳回或待补测结论，并明确是否需要回流编码域、Bug 域、联调域或测试策略域。
6. 回归范围未稳定前，不直接宣告任务具备交付条件。

## 权责边界与不负责事项

- 只负责旧能力兼容性与影响面验证，不负责当前需求本身是否实现正确，那属于 `functional-validation-rules`。
- 不负责测试优先级大盘设计和资源收口，那属于 `test-strategy-rules`。
- 不负责联调环境、上下游协议和链路打通问题定位，这类问题应先回到 `test-strategy-rules` 重新拆分验证路径。
- 不负责测试目录、命名、程序和文档如何组织，但必须服从 `test-strategy-rules 的 test-asset-governance 条件路由` 的新结构；涉及 Go 可编译路径时还必须服从 `test-program-rules` 的《Go 测试编译路径（强制）》。
- 如果回归无法开展，是因为需求、Bug 定义或改动本身尚未收敛，应先回流对应上游 skill。

## 需要暂停并确认的条件

- 当前功能验证尚未通过，直接做回归会掩盖主问题。
- 本次改动影响面不清，难以合理界定回归范围。
- 当前回归环境、历史数据或关键链路依赖不具备，结论可信度不足。
- 回归范围已经扩张到全量测试计划，需要升级到 `test-strategy-rules` 重新收口。

## 执行通过 / 驳回标准

- 通过：本次改动涉及的旧能力、关联链路、共享依赖和兼容行为在已判定回归范围内未发现新的破坏性问题；中文测试主文档 已能清楚说明结论，根 `test/` 回归测试、同源码镜像的 mock/stub/fake 与证据路径均可追溯。
- 驳回：本次改动引入了旧能力回退、兼容性破坏、公共链路异常，或关键回归范围未验证，无法证明“没有带坏别的地方”；回归留痕继续散落在错误目录中；或为了测试通过而在生产代码中新增测试专用方法、测试专用数据、测试专用结构体字段。

## 执行结果归档要求

- 将回归结论统一记录到 `artifact-storage-rules` 约定的测试主文档。
- 测试主文档至少包含改动类型、回归范围、选取用例、执行环境、结论、未覆盖项和遗留风险。
- 详细回归案例、执行日志、截图、补充说明统一以代码围栏内联进测试主文档正文；正文只保存非可执行证据，不得与根 `test/` 的可执行回归测试或模拟程序混放。
- 测试任务主说明位置、目录命名模板和同一轮回归的复用策略统一遵循 `../artifact-storage-rules/references/path-map.yaml`、`../artifact-storage-rules/references/naming-templates.md` 与 `../artifact-storage-rules/references/update-policy.md`。
- 如果同一需求存在多轮独立回归验证，应分别创建多个时间戳测试主文档，而不是把所有回归轮次混在一个目录里。
- 进入最终回复前，必须联动 `artifact-delivery-gate-rules` 核对回归测试主文档、根 `test/` 测试文件与证据是否已经真实落盘；未落盘不得判定回归验证完成。

## references 读取规则

- 默认先读 `references/regression-scope-selection.md`。
- 在定位根 `test/` 镜像、测试主文档、测试主文档、证据目录或判断是否继续沿用同一轮回归根目录时，先读 `../artifact-storage-rules/references/path-map.yaml`、`../artifact-storage-rules/references/naming-templates.md` 与 `../artifact-storage-rules/references/update-policy.md`。
- 只有在功能验证、联调验证、回归验证边界不清时，再读 `references/regression-boundaries.md`。
- 只有在需要回归结论模板和样例时，再读 `references/regression-template-and-examples.md`。
