# 测试程序类型与拆分规则

## 真实路径镜像基线

- 所有活动测试代码落在根 `test/`，按被测源码目录镜像；源码 `internal/service/history_client.go` 的测试为 `test/internal/service/history_client_test.go`。
- 单文件测试用 `<名称>_test.<ext>`；目录级测试以被测模块目录镜像并在 README 列出被测文件。
- mock、stub、fake、fixture、数据构造和共享 helper 与测试同目录，或放入 `test/shared/`；不要放入 `doc/5-tests/`。
- `doc/5-tests/YYYY-MM-DD_HHmmss_<任务主题>/README.md` 仅保留目的、命令、样本和结论，`evidence/` 与 `artifacts/` 承接证据和非可执行产物。

## 程序职责

- 正式测试程序：承载断言和验证流程。
- 模拟程序：提供 mock、stub、fake、假服务和假依赖。
- 响应探测脚本：获取第三方接口真实响应样例，作为结构体建模依据。
- 数据构造与初始化/清理脚本：准备和清理 local 环境的测试前置条件。
- 共享测试辅助代码：只抽取稳定重复的断言、构造器、客户端或装配逻辑。

## Go 场景

- 源码目录绝对不允许 `*_test.go`。
- 所有 Go 测试在根 `test/` ASCII 路径中，使用外部 `<target>_test` 包，只调用导出 API。
- 白盒需求先补可外部测试的 seam；黑盒和集成测试同样进入根 `test/`，不存在同包例外。

## 拆分检查

- 一个测试程序只承担一种主职责，不把环境切换、数据构造、断言和报告生成全部混入一个文件。
- 共享辅助逻辑只在重复且稳定时进入 `test/shared/`，不要为一次性测试新增抽象。
- 测试程序执行时输出开始、关键步骤、结束和失败步骤；第三方响应探测必须记录必要脱敏样例。
- 测试代码位置、命名或历史边界不清时，回到 `test-strategy-rules` 的测试资产治理契约处理。
