---
name: test-program-rules
description: 当新增或修改测试程序、模拟程序、验证脚本、数据构造脚本、测试辅助代码时触发。负责统一测试程序职责拆分、辅助代码边界和长期保留策略；必须以 `test-location-rules` 为基准，把真实测试代码、脚本、mock、fixture 和执行产物统一落在 `test/yyyy-MM-DD_HHmmss/<ASCII 真实代码路径镜像>/` 下，并避免中文进入会被 Go 工具链编译的路径；不要用它代替 test-location-rules、test-naming-rules、test-doc-rules、bug-runtime-debug-rules 或功能验证规则。
---

# 测试程序规则

只在“测试程序本身应该怎么拆、怎么组织职责”这个问题上使用这个 skill。
如果当前争议是测试目录放哪里，请转交 `test-location-rules`；如果是测试名称怎么起，请转交 `test-naming-rules`；如果只是补测试文档，请转交 `test-doc-rules`。

**重要：本 skill 只处理真实测试资产。中文说明目录只放 `README.md`，不放任何 `.go`、`.py`、`.sh`、mock、fixture 或截图；所有真实测试资产都必须落在同一时间戳根目录下的 ASCII 真实代码路径镜像目录中。**

## Skill 作用与适用场景

- 作为测试资源管理链的第三道规则，在落点和命名稳定后统一测试程序结构。
- 统一正式测试程序、mock、stub、fake、数据构造脚本、初始化脚本和共享测试辅助代码的职责边界。
- 防止临时验证代码、一次性排障脚本和测试辅助逻辑混入生产目录。
- 防止把中文目录名带入 Go 可编译路径，破坏 `go test ./...` 或 import path。
- 提升测试程序的可读性、可维护性和可追溯性。

## 自动触发信号

- 新增或修改测试程序、mock server、stub、fake、数据构造脚本、初始化脚本、清理脚本。
- 需要决定某段验证逻辑应该进入正式测试代码、共享测试辅助代码还是一次性调试资产。
- 发现测试程序准备放到 `testing/`、仓库根目录、业务目录、中文说明目录或其他非 `test/` 时间戳根目录位置。
- 发现 Go 测试目录准备使用中文路径，可能直接导致工具链失败。
- 发现一个测试脚本同时承担环境初始化、数据构造、执行、断言、报告生成等多种职责。

## 进入后先做什么

1. 先确认测试资产落点和命名已经遵循 `test-location-rules` 与 `test-naming-rules`。
2. 确认当前真实测试资产位于 `test/yyyy-MM-DD_HHmmss/<ASCII 真实代码路径镜像>/` 下，而不是中文说明目录中。
3. 找出当前测试程序对应的真实代码路径，例如源文件是 `internal/service/history_client.go`，则测试资产默认镜像到 `test/yyyy-MM-DD_HHmmss/internal/service/`。
4. 区分当前对象属于正式测试文件、mock / stub / fake、数据构造脚本、初始化脚本、清理脚本还是共享测试辅助代码。
5. 判断当前代码是长期保留的正式测试资产，还是只用于临时定位问题的调试资产。

## 默认执行流程

1. 默认先读 `references/program-types-and-splitting.md`，确认测试程序类型和拆分原则。
2. 如果发现测试程序与生产代码、调试代码或文档职责混用，再读 `references/program-boundaries.md`。
3. 如果需要判断当前拆分方式是否合理，再读 `references/program-examples.md` 对照正反例。
4. 输出推荐的程序拆分方案、镜像路径建议、禁止保留的临时实现和最小改动建议。
5. 测试程序结构未稳定前，不进入 `test-doc-rules`、`functional-validation-rules` 和 `test-regression-rules`。

## 权责边界与不负责事项

- 只负责测试程序的职责划分和辅助代码边界，不负责决定测试目录落点，那属于 `test-location-rules`。
- 只负责测试程序结构，不负责测试目录和文件命名，那属于 `test-naming-rules`。
- 不负责测试文档章节和记录方式，那属于 `test-doc-rules`。
- 不负责功能是否通过验证，也不负责回归范围判定，那属于 `functional-validation-rules` 和 `test-regression-rules`。
- 如果当前代码只是为定位问题而临时加的日志、断言、探针或一次性脚本，应优先转交 Bug 域或联调域 skill。

## 需要暂停并确认的条件

- 当前程序既像正式测试资产，又像一次性排障脚本，保留策略不清。
- 一个脚本承担过多职责，拆分后会影响大量既有引用，但影响面尚未确认。
- 当前镜像路径无法对应到真实代码路径，导致测试资产归属不清。
- 计划把中文目录用于 Go 可编译路径，可能直接破坏自动化测试链路。

## 执行通过 / 驳回标准

- 通过：正式测试程序、mock、数据构造脚本和辅助代码职责清晰，且都落在 `test/yyyy-MM-DD_HHmmss/<ASCII 真实代码路径镜像>/` 下；会被 Go 编译的目录保持 ASCII；没有把测试逻辑混入生产目录或中文说明目录。
- 驳回：测试程序继续散落在业务目录、仓库根目录、中文说明目录或随意目录中；或把中文引入 Go 可编译路径；或临时调试脚本长期滞留并伪装成正式测试资产。

## 执行结果归档要求

- 将测试程序拆分结论记录到 `test/yyyy-MM-DD_HHmmss/测试任务中文简介/README.md` 中。
- 在 README 中写清真实测试资产所在的 ASCII 镜像路径，例如 `test/yyyy-MM-DD_HHmmss/internal/service/history_client_test.go`。
- mock、fixture、脚本、截图、日志等都归档在同一时间戳根目录下的 ASCII 真实代码路径镜像目录中。
- 如果同一需求需要多轮独立测试程序或多次独立验证，应分别创建多个时间戳根目录，而不是持续往一个根目录中堆叠。

## references 读取规则

- 默认先读 `references/program-types-and-splitting.md`。
- 只有在职责边界混淆时，再读 `references/program-boundaries.md`。
- 只有在需要正反例时，再读 `references/program-examples.md`。
