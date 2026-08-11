# 回归验证边界

## 用途

用于区分回归验证与功能验证、联调验证、测试策略、测试资源管理之间的职责。

## 属于回归验证域

- 修复某个 Bug 后，确认同类旧路径和关联链路未被破坏。
- 修改共享逻辑后，确认主要调用方和兼容行为仍然正常。
- 调整原有功能后，确认旧入口、旧流程、旧结果未异常退化。
- 把回归结论写入中文测试主文档；活动回归测试、mock、stub、fake、fixture 和 helper 放入根 `test/` 的源码相对路径镜像，详细回归证据放入 `doc/5-tests/` 的非可执行证据路径。

## 不属于回归验证域

- 当前需求是否首次实现正确。
- 上下游系统、环境、协议、trace 链路是否打通。
- 测试优先级大盘如何排、是否需要全量测试策略调整。
- 测试目录、命名、程序和文档如何组织。

边界说明：测试资源落点由测试资源管理类 skill 统一决定；本 skill 产生或引用的活动回归测试、mock、stub、fake、fixture 和 helper 仍必须位于根 `test/` 的源码相对路径镜像，`doc/5-tests/` 只承载非可执行证据。

## 回流规则

- 当前功能本身未验证通过，先回流 `functional-validation-rules`。
- 现象更像环境或链路异常，先回到 `test-strategy-rules` 重新分流。
- 回归范围过大、资源不足、优先级存在争议，升级到 `test-strategy-rules`。
- 发现明确回归失败项，回流编码域或 Bug 域修复。
- 如果回归说明和证据落点不符合新结构，回流 `test-strategy-rules 的 test-asset-governance 条件路由`、`test-strategy-rules 的 test-asset-governance 条件路由` 或 `test-strategy-rules 的 test-asset-governance 条件路由` 调整。
