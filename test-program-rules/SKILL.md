---
name: test-program-rules
description: 当新增或修改测试程序、模拟程序、验证脚本、数据构造脚本、测试辅助代码（mock、stub、fake、fixture）时触发；当 Go 测试路径进入编译链路、出现源码目录 `*_test.go`、中文可编译路径或白盒同包测试诉求时，也由本 skill 统一处理。负责测试程序职责拆分、辅助代码边界、长期保留策略，以及 Go 测试可编译路径必须保持 ASCII、源码目录禁放 `*_test.go`、白盒诉求改 seam 的强制约束；必须以 `artifact-storage-rules` 与 `test-strategy-rules 的 test-asset-governance 条件路由` 为落点真相，把真实测试代码、脚本、mock、fixture 和执行产物统一落在中央约定的测试时间戳根目录下的 ASCII 真实代码路径镜像目录中；若资产散落在 `doc/5-tests/` 根目录之外，先按同一条件路由收拢；第三方 API 文档缺失响应模型时，必须先用测试脚本探测真实响应，再反推结构体定义；强制禁止为了测试目的污染生产代码（新增测试专用方法、测试专用数据、测试专用结构体字段等）。测试脚本建议输出关键过程日志便于定位失败，但过程日志完整性默认为自查项、非放行硬阻断。不要用它代替 `test-strategy-rules`、功能验证规则或回归验证规则。
---

# 测试程序规则

只在“测试程序本身应该怎么拆、怎么组织职责”这个问题上使用这个 skill。
如果当前争议是测试目录放哪里、目录散落到错误位置、测试名称怎么起或补测试文档，请统一转交 `test-strategy-rules 的 test-asset-governance 条件路由`。

**重要：本 skill 只处理真实测试资产。中文说明目录只放 `README.md`，不放任何 `.go`、`.py`、`.sh`、mock、fixture 或截图；所有真实测试资产都必须落在同一时间戳根目录下的 ASCII 真实代码路径镜像目录中。**

## 测试隔离红线（强制）

> 本节遵循 `test-strategy-rules` 的《测试隔离红线（强制）》单一权威来源：严禁为测试污染生产代码（新增测试专用方法/数据/结构体字段）、测试能力一律走测试目录内脚本/mock/fixture/seam、发现污染立即阻断回退、自动化测试只用 `local` 环境（禁连 `test`/`prod`/`staging` 等非 local 服务）。本 skill 不重复展开，仅承接测试程序侧的落地。

## Skill 作用与适用场景

- 作为测试资源管理链的第三道规则，在落点和命名稳定后统一测试程序结构。
- 统一正式测试程序、mock、stub、fake、数据构造脚本、初始化脚本和共享测试辅助代码的职责边界。
- 统一 Go 白盒/黑盒/集成测试的程序落点矩阵，避免出现“白盒例外”。
- 防止临时验证代码、一次性排障脚本和测试辅助逻辑混入生产目录。
- 防止把中文目录名带入 Go 可编译路径，破坏 `go test ./...` 或 import path。
- 提升测试程序的可读性、可维护性和可追溯性。
- 统一测试脚本的控制台日志输出，让执行过程可见、失败位置可快速定位。
- 在第三方 API 文档不完整时，提供“先脚本探测响应 -> 再结构体建模”的标准流程。

## 自动触发信号

- 新增或修改测试程序、mock server、stub、fake、数据构造脚本、初始化脚本、清理脚本。
- 需要决定某段验证逻辑应该进入正式测试代码、共享测试辅助代码还是一次性调试资产。
- 发现测试程序准备放到 `testing/`、仓库根目录、业务目录、中文说明目录或其他非中央约定时间戳根目录位置。
- 发现 Go 测试目录准备使用中文路径，可能直接导致工具链失败。
- 发现 Go 白盒单测诉求，准备在源码目录创建同包 `*_test.go`。
- 发现一个测试脚本同时承担环境初始化、数据构造、执行、断言、报告生成等多种职责。
- 发现测试脚本只有最终成功/失败结果，没有关键过程控制台日志，导致测试过程不可见。
- 接入第三方 API 时只有 curl 示例，缺少响应结构文档，需要先探测真实返回体。

## 进入后先做什么

1. 先确认测试资产落点和命名已经遵循 `test-strategy-rules 的 test-asset-governance 条件路由` 与 `test-strategy-rules 的 test-asset-governance 条件路由`；若资产原本散落，还需先完成 `test-strategy-rules 的 test-asset-governance 条件路由` 的迁移。
2. 确认当前真实测试资产位于中央约定的测试时间戳根目录下的 ASCII 真实代码路径镜像目录中，而不是中文说明目录中。
3. 找出当前测试程序对应的真实代码路径，例如源文件是 `internal/service/history_client.go`，则测试资产默认镜像到当前测试时间戳根目录下的 `internal/service/`。
4. 区分当前对象属于正式测试文件、mock / stub / fake、数据构造脚本、初始化脚本、清理脚本还是共享测试辅助代码。
5. 判断当前代码是长期保留的正式测试资产，还是只用于临时定位问题的调试资产。
6. 检查脚本是否定义了最小控制台过程日志（开始、关键步骤、结束、失败点）。
7. 若第三方 API 响应结构不明确，先规划“调用脚本 + 原始响应留痕 + 结构体草模”三步。
8. 若测试程序或数据构造脚本需要连接本地真实环境（数据库、缓存、消息队列、HTTP/RPC 上游等），按 `test-strategy-rules` 的「本地环境配置发现与连接」去本地 `local` 配置文件读取连接信息，并遵守其隔离安全约束；不得回退为读取 `test` / `prod` / `staging` 等非 local 环境配置。

## 默认执行流程

1. 默认先读 `references/program-types-and-splitting.md`，确认测试程序类型和拆分原则。
2. 再读 `../artifact-storage-rules/references/path-map.yaml`、`../artifact-storage-rules/references/naming-templates.md` 与 `../artifact-storage-rules/references/update-policy.md`，确认测试时间戳根目录、中文主说明 `README.md`、ASCII 镜像路径和同一轮测试是否继续复用同一根目录。
3. 如果发现测试程序与生产代码、调试代码或文档职责混用，再读 `references/program-boundaries.md`。
4. 对 Go 项目必须应用白盒/黑盒/集成测试同一落点矩阵：无论类型都不得在源码目录落地 `*_test.go`；白盒诉求改 seam。
5. 如果需要判断当前拆分方式是否合理，再读 `references/program-examples.md` 对照正反例。
6. 为测试脚本补齐控制台过程日志：至少包含测试开始、关键步骤、步骤结果、测试结束；失败时打印失败步骤与错误摘要。
7. 若第三方 API 响应结构不明确，先产出探测脚本并执行，记录原始响应（必要脱敏）和响应样例来源，再回流编码阶段定义结构体。
8. 若无法通过文档或探测脚本确认响应结构，暂停并反馈用户提供响应结构说明，不进入盲写解析阶段。
9. 输出推荐的程序拆分方案、镜像路径建议、控制台日志建议、禁止保留的临时实现和最小改动建议。
10. 测试程序结构未稳定前，不进入 `test-strategy-rules 的 test-asset-governance 条件路由`、`functional-validation-rules` 和 `test-regression-rules`。

## 权责边界与不负责事项

- 只负责测试程序的职责划分和辅助代码边界，不负责决定测试目录落点，那属于 `test-strategy-rules 的 test-asset-governance 条件路由`；散落资产治理属于 `test-strategy-rules 的 test-asset-governance 条件路由`，Go 可编译路径约束见本 skill《Go 测试编译路径（强制）》节。
- 只负责测试程序结构，不负责测试目录和文件命名，那属于 `test-strategy-rules 的 test-asset-governance 条件路由`。
- 不负责测试文档章节和记录方式，那属于 `test-strategy-rules 的 test-asset-governance 条件路由`。
- 不负责功能是否通过验证，也不负责回归范围判定，那属于 `functional-validation-rules` 和 `test-regression-rules`。
- 如果当前代码只是为定位问题而临时加的日志、断言、探针或一次性脚本，应优先转交 Bug 域或联调域 skill。

## 需要暂停并确认的条件

- 当前程序既像正式测试资产，又像一次性排障脚本，保留策略不清。
- 一个脚本承担过多职责，拆分后会影响大量既有引用，但影响面尚未确认。
- 当前镜像路径无法对应到真实代码路径，导致测试资产归属不清。
- 计划把中文目录用于 Go 可编译路径，可能直接破坏自动化测试链路。
- 计划通过在源码目录新增 `*_test.go` 来满足白盒诉求，而不是先补 seam。
- 第三方 API 的响应结构既无文档也无法通过探测脚本获得，继续编码将只能基于猜测写 map 解析。

## 执行通过 / 驳回标准

- 通过：正式测试程序、mock、数据构造脚本和辅助代码职责清晰，且都落在中央约定的测试时间戳根目录下的 ASCII 真实代码路径镜像目录中；会被 Go 编译的目录保持 ASCII；Go 白盒/黑盒/集成都未在源码目录落地 `*_test.go`；（建议）测试脚本输出关键过程日志便于定位失败；第三方 API 文档缺失响应模型时，已通过探测脚本获取真实响应并形成结构化建模依据；没有把测试逻辑混入生产目录或中文说明目录。
- 驳回：测试程序继续散落在业务目录、仓库根目录、中文说明目录或随意目录中；把中文引入 Go 可编译路径；通过源码目录 `*_test.go` 处理白盒诉求而不补 seam；临时调试脚本长期滞留并伪装成正式测试资产；第三方 API 响应结构不明时直接跳过探测脚本、盲写 map 解析；或为测试目的向生产代码新增测试专用方法、测试专用数据、测试专用结构体字段。

## 执行结果归档要求

- 将测试程序拆分结论记录到 `artifact-storage-rules` 约定的测试任务主说明 `README.md` 中。
- 在 README 中写清真实测试资产所在的 ASCII 镜像路径。
- mock、fixture、脚本、截图、日志等都归档在同一时间戳根目录下的 ASCII 真实代码路径镜像目录中。
- 测试任务主说明位置、目录命名模板和同一轮测试的复用策略统一遵循 `../artifact-storage-rules/references/path-map.yaml`、`../artifact-storage-rules/references/naming-templates.md` 与 `../artifact-storage-rules/references/update-policy.md`。
- 如果同一需求需要多轮独立测试程序或多次独立验证，应分别创建多个时间戳根目录，而不是持续往一个根目录中堆叠。
- 进入最终回复前，必须联动 `artifact-delivery-gate-rules`，核对测试程序拆分结论、ASCII 镜像路径和相关资产落点是否已经真实记录到测试任务 `README.md` 并归位到对应目录；未落盘不得判定测试程序整理完成。

## references 读取规则

- 默认先读 `references/program-types-and-splitting.md`。
- 在定位测试时间戳根目录、中文主说明 `README.md`、ASCII 镜像路径或判断是否继续沿用同一轮测试根目录时，先读 `../artifact-storage-rules/references/path-map.yaml`、`../artifact-storage-rules/references/naming-templates.md` 与 `../artifact-storage-rules/references/update-policy.md`。
- 只有在职责边界混淆时，再读 `references/program-boundaries.md`。
- 只有在需要正反例时，再读 `references/program-examples.md`。

## Go 测试编译路径（强制）

> 本节收编原 `go-test-compile-path-rules` 的强制约束（该独立 skill 已 merge_retire 并入本 skill）；只在“Go 测试路径会影响编译和扫描链路”这个问题上适用。

- Go 源码目录绝对不允许出现 `*_test.go`。
- 会被 Go 编译链路扫描的测试目录路径必须保持 ASCII，禁止中文进入 `go test ./...` 或 import path。
- 白盒同包诉求不是例外通道：统一先改 seam，再把测试资产放回 `doc/5-tests/<时间戳>/` 的 ASCII 真实代码路径镜像。
- 若测试文件既违规落在源码目录，又属于散落资产，同时转交 `test-strategy-rules 的 test-asset-governance 条件路由` 处理迁移。
- 通过：源码目录无 `*_test.go`、Go 可编译测试路径为 ASCII、白盒诉求已改 seam、测试资产回到中央测试根目录正确镜像路径；驳回：源码目录保留 `*_test.go`、中文进入 Go 可编译路径，或把白盒同包落地当长期特例。

## 写接口测试脚本的过程日志约定（默认自查，非放行硬阻断）

> 本节是写接口（createTransaction、createOrder、cancelOrder、refund 等）测试脚本推荐的最小控制台过程日志规范。过程日志能显著缩短失败定位时间，但默认为**模型自查项、非放行硬阻断**；仅当实施计划把它冻结为放行必须项、或用户明确要求时，才升级为硬判。

### 一、最小过程日志清单（强制）

写接口测试脚本在控制台必须按以下顺序输出：

1. `开始`：测试开始时输出，包含测试脚本名、本轮测试时间戳、目标接口。
2. `样本来源`：从 `orderUser` 等业务表读取的样本总数 + 4 类样本各自的数量 + 通道/链/币种分布。
3. `每个样本执行前`：样本 ID（脱敏后）、请求参数、HTTP 状态码、业务码、判定分类（`PASS` / `EXPECTED_FAIL` / `UNEXPECTED_FAIL` / `PENDING`）。
4. `每个样本执行后`：响应时间、错误信息关键词（如 `insufficient fee` / `Token under maintenance` 等）、数据落库状态。
5. `门禁汇总`：4 类样本分布、矩阵完整性、`UNEXPECTED_FAIL` 数量、`EXPECTED_FAIL` 比例。
6. `结束`：测试结束时间、耗时、最终结论（PASS / FAIL / PARTIAL / PENDING）。
7. `失败点`：任意样本判定为 `UNEXPECTED_FAIL` 时，立即打印失败步骤与错误摘要，包含 HTTP 状态码、错误信息原文片段（截断到 80 字符）、堆栈首行（如有）。

### 二、日志格式要求

- 每条日志必须带 ISO 时间戳（精确到毫秒），便于按时间序列回放。
- 敏感字段（userId、token、手机号、身份证号、银行卡号、地址、订单号）必须脱敏（用 `***` 代替末四位）。
- 日志必须可机读：建议使用 JSON 行格式或带前缀的 key=value 格式，避免纯自由文本。
- 错误信息原文片段必须截断到 80 字符以内，避免日志被超长响应体淹没。

### 三、与既有"测试脚本控制台日志"的关系

- 本节是 `test-program-rules` 上文"控制台过程日志"的写接口场景特化，必须同时满足。
- 写接口脚本必须同时输出本节的 7 项过程日志和上文的最小过程日志（开始、关键步骤、结束、失败点），不得遗漏任一项。
- 缺过程日志的写接口脚本默认提示补齐（自查项），不单独作为放行硬阻断；仅在计划冻结或用户明确要求时，才必须补齐后再进入正式测试。

### 四、失败样本的回放要求

- 任意 `UNEXPECTED_FAIL` 样本必须输出"可重放"信息：完整请求参数（脱敏后）、目标 URL、目标接口标识、调用时间。
- 重放信息落到 `artifacts/<时间戳>/repro/` 目录，便于后续手工复现或脚本回放。
- 多个 `UNEXPECTED_FAIL` 样本时，按样本执行时间顺序输出，便于定位时间窗口内的环境变化。
