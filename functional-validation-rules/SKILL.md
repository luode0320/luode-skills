---
name: functional-validation-rules
description: 当需要验证新功能、修改后的功能、接口行为、页面交互、输入输出结果是否满足当前需求、当前变更和验收标准时触发。负责界定本次功能验证范围、验证步骤、通过驳回标准和结论留痕；必须以 `artifact-storage-rules` 与 `test-task-root-layout-rules` 为基准，把功能验证结论写回中央约定的测试任务主说明 `README.md`，并把详细执行证据放到同一时间戳根目录下的 ASCII 真实代码路径镜像目录中；若该镜像路径会进入 Go 编译链路，还必须同步遵循 `go-test-compile-path-rules`；同时强制禁止为了测试目的污染生产代码（新增测试专用方法、测试专用数据、测试专用结构体字段等）。不要用它代替 test-strategy-rules、test-task-root-layout-rules 或 test-regression-rules。
---

# 功能验证规则

只在“当前需求或当前修改本身是否做对了”这个问题上使用这个 skill。
如果当前争议是测试资源怎么组织，请转交测试资源管理类 skill；如果当前争议是旧功能有没有被带坏，请转交 `test-regression-rules`。

## 测试隔离红线（强制）

- 严禁为了测试目的改动生产代码语义，包括但不限于新增测试专用方法、测试专用数据、测试专用结构体字段。
- 功能验证必须基于真实业务实现与测试资产完成，禁止通过向生产代码注入测试专用能力来“制造通过”。
- 一旦发现生产代码测试污染，功能验证结论直接无效并阻断，先回退污染改动再重测。

## Skill 作用与适用场景

- 作为测试域中的功能正确性验证规则，直接面向当前需求、当前修改和当前验收标准。
- 约束功能验证范围、验证步骤、通过 / 驳回标准和结果留痕方式。
- 聚焦接口行为、页面交互、输入输出结果和业务逻辑分支是否符合当前预期。
- 防止把测试资源管理、联调排障或历史回归问题误归到功能验证域。
- 保证功能验证结论先通过中文 README 输出，再用 ASCII 镜像路径承接详细执行证据。

## 自动触发信号

- 需要验证新功能、修改后的功能、接口行为、页面交互、输入输出结果是否满足当前需求与验收标准。
- 代码已经完成并通过基础审查，准备判断“这次改动是否正确”。
- 用户要求确认某个接口、某个页面、某个逻辑分支、某个交互链路是否达到当前预期。
- 功能验证失败后，需要明确是实现问题、需求问题还是联调 / 回归问题。
- 发现功能验证结论准备散落到 `testing/`、交付文档、仓库根目录或其他非当前时间戳任务目录位置。

## 进入后先做什么

1. 先确认当前需求、当前修改和验收标准是否已经明确。
2. 明确本轮只验证当前变更本身，不主动扩张到全量历史回归。
3. 提取当前功能验证对象：接口、页面、交互链路、输入输出、异常分支。
4. 确认测试资源、测试文档和执行环境已经具备基本验证条件。
5. 决定哪些结论写入中文 README，哪些详细执行步骤、截图和明细放入 ASCII 镜像路径。

## 默认执行流程

1. 默认先读 `references/validation-scope.md`，确定本轮功能验证的覆盖范围和最小检查清单。
2. 再读 `../artifact-storage-rules/references/path-map.yaml`、`../artifact-storage-rules/references/naming-templates.md` 与 `../artifact-storage-rules/references/update-policy.md`，确认测试时间戳根目录、中文主说明 `README.md`、ASCII 镜像路径和同一轮验证是否继续复用同一根目录。
3. 如果发现问题可能属于联调、回归或需求边界争议，再读 `references/validation-boundaries.md`。
4. 输出验证范围、验证步骤、结果结论和未通过项时，再读 `references/validation-template-and-examples.md`。
5. 给出通过、驳回或待确认结论，并明确是否需要回流编码域、需求域、Bug 域或联调域。
6. 功能验证未通过时，不直接跳到回归验证。

## 权责边界与不负责事项

- 只负责当前需求或当前修改的功能正确性验证，不负责验证范围优先级设计，那属于 `test-strategy-rules`。
- 不负责测试目录、命名、测试程序和测试文档组织，但必须服从 `test-task-root-layout-rules` 的根布局；涉及 Go 可编译路径时还必须服从 `go-test-compile-path-rules`。
- 不负责跨系统、跨环境、上下游协议、trace 断链等联调问题，这类问题应先回到 `test-strategy-rules` 重新拆分验证路径。
- 不负责历史功能兼容性和改动扩散影响，那属于 `test-regression-rules`。
- 如果功能验证无法进行，是因为需求目标、边界或验收标准不清，应回流需求域。

## 需要暂停并确认的条件

- 当前需求、验收标准或预期结果本身不明确。
- 当前功能失败现象更像上下游环境问题或联调问题，无法在单点功能验证中闭环。
- 当前验证范围已经明显扩张成回归检查或全链路稳定性检查。
- 当前测试资源或前置环境尚未准备好，无法得出可信结论。

## 执行通过 / 驳回标准

- 通过：当前需求或当前修改涉及的功能点、输入输出、交互行为和异常处理均符合当前验收标准；中文 README 已写明结论，详细步骤和证据位于 ASCII 镜像路径并可追溯。
- 驳回：当前变更存在与需求或验收标准不符的功能问题；结论无法回溯到明确的测试资产与证据；功能验证留痕继续散落在错误目录中；或为了测试通过向生产代码新增测试专用方法、测试专用数据、测试专用结构体字段。

## 执行结果归档要求

- 将功能验证结论记录到 `artifact-storage-rules` 约定的测试任务主说明 `README.md`。
- README 至少包含验证对象、验证范围、执行环境、步骤摘要、结果结论、未通过项和下一步建议。
- 详细执行步骤、截图、接口返回样例、补充案例和原始日志统一放到中央约定的测试时间戳根目录下的 ASCII 真实代码路径镜像目录中。
- 测试任务主说明位置、目录命名模板和同一轮验证的复用策略统一遵循 `../artifact-storage-rules/references/path-map.yaml`、`../artifact-storage-rules/references/naming-templates.md` 与 `../artifact-storage-rules/references/update-policy.md`。
- 如果结论为待确认，必须说明卡点属于需求澄清、实现修复、联调排障还是回归补测。

## references 读取规则

- 默认先读 `references/validation-scope.md`。
- 在定位测试时间戳根目录、中文主说明 `README.md`、ASCII 镜像路径或判断是否继续沿用同一轮验证根目录时，先读 `../artifact-storage-rules/references/path-map.yaml`、`../artifact-storage-rules/references/naming-templates.md` 与 `../artifact-storage-rules/references/update-policy.md`。
- 只有在职责边界不清或问题归属有争议时，再读 `references/validation-boundaries.md`。
- 只有在需要结论模板和样例时，再读 `references/validation-template-and-examples.md`。
