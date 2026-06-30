---
name: project-release-test-rules
description: 当需要做上线前项目级全接口测试、替代人工接口回归验证、生成上线接口测试门禁结论时触发。负责维护项目接口基线、规划测试范围、执行接口验证、给出agent判定的接口级结果和上线放行结论，所有测试资产落地到doc/5-tests/对应时间戳根目录，强制要求请求参数和简要响应为JSON字符串，禁止接口明细输出为Markdown表格，agent负责判定接口是否通过，无需人工参与响应判断。
---

# 项目上线接口测试门禁规则

只在“上线前需要统一做项目级接口测试、替代人工全接口验证、输出上线准入结论”时使用这个skill。
如果是任务级功能验证、改动影响面回归，分别转交unctional-validation-rules、	est-regression-rules；如果是测试文档组织、目录结构，转交	est-doc-rules、	est-task-root-layout-rules。

## 测试隔离红线（强制，和现有测试域规则一致）
- 严禁为了测试目的改动生产代码语义，包括但不限于新增测试专用方法、测试专用数据、测试专用结构体字段。
- 接口测试必须基于真实业务实现和测试资产完成，禁止通过向生产代码注入测试专用能力来“制造通过”结果。
- 一旦发现生产代码测试污染，测试结论直接无效并阻断，先回退污染改动再重测。

## Skill 作用与适用场景
- 作为上线前的项目级接口质量门禁，统一规划全项目接口测试范围、选择必测接口、执行验证、输出可决策的结论。
- 维护项目级接口测试基线，沉淀可复用的接口定义、参数规则、判定标准，避免每次上线重新梳理接口。
- 自动由agent判定接口响应是否符合预期，替代人工逐一查看响应结果。
- 输出标准化的测试报告，明确给出是否允许上线的结论，作为inal-acceptance-rules的输入之一。
- 强制所有测试资产落地到doc/5-tests/下的时间戳根目录，遵循现有测试域的归档规则。

## 自动触发信号
- 上线前需要做全项目接口回归验证。
- 需要替代人工做接口测试和响应判断。
- 需要输出上线接口测试准入结论。
- 项目迭代后需要验证所有核心接口是否正常。
- 用户明确要求做“项目级接口测试”、“上线前全接口测试”、“接口测试门禁”。

## 进入后先做什么
1. 先确认当前项目的接口基线是否存在，不存在则先按eferences/interface-inventory-schema.md扫描生成接口基线。
2. 确认本次上线的改动范围、影响模块，按eferences/test-selection-policy.md筛选本次必测接口集合。
3. 按	est-task-root-layout-rules创建本次测试的时间戳根目录、中文说明目录和ASCII镜像目录。
4. 明确测试环境、鉴权信息、依赖数据要求，准备测试前置条件。
5. 按eferences/agent-response-judgement.md定义判定规则，确保agent可以独立判断接口是否通过。
6. 按eferences/report-format.md定义输出格式，明确禁止接口明细使用Markdown表格，强制使用块状格式，请求参数和简要响应必须为JSON字符串。

## 默认执行流程
1. 首先调用	est-task-root-layout-rules创建本次项目级接口测试的时间戳根目录，中文说明目录命名为上线前项目接口测试，包含主README.md，ASCII镜像目录存放真实测试脚本、原始响应、证据文件。
2. 扫描项目接口（从路由、controller、swagger/openapi、现有测试记录、接口文档提取），生成/更新项目接口基线，落盘到doc/5-tests/基线/interface-inventory.yaml（如果不存在）。
3. 按eferences/test-selection-policy.md筛选本次必测接口、可选测接口、跳过接口，明确每个接口的选择/跳过理由。
4. 为每个必测接口准备测试用例、请求参数、预期语义规则，准备测试环境和鉴权信息。
5. 执行接口测试，记录每个接口的请求参数（JSON字符串）、简要响应（JSON字符串，脱敏）、完整响应（落盘到ASCII镜像目录）。
6. 按eferences/agent-response-judgement.md由agent独立判断每个接口是否通过，给出判定理由，不依赖人工判断。
7. 按eferences/report-format.md生成接口测试明细报告，每个接口使用块状格式，不使用Markdown表格。
8. 按eferences/execution-gate.md输出最终门禁结论：PASS / FAIL / PARTIAL，明确是否允许上线、阻断原因、风险项。
9. 将测试计划、接口清单、报告、结论、证据全部归档到对应时间戳根目录，主结论写入中文说明目录的README.md，明细和证据写入ASCII镜像目录。
10. 将本次测试结论同步到接口基线，更新对应接口的最近测试时间和测试结论。
11. 最终结论同步到inal-acceptance-rules，作为最终验收的输入之一。

## 权责边界与不负责事项
- 负责项目级上线前接口测试，不替代任务级unctional-validation-rules的当前改动功能验证。
- 不替代	est-regression-rules的改动影响面回归验证，两者可并行执行。
- 不负责测试文档的结构和归档规则，必须遵循	est-doc-rules和rtifact-storage-rules的要求。
- 不负责测试目录的创建和结构，必须遵循	est-task-root-layout-rules的要求。
- 测试执行如果涉及单接口功能验证，可调用unctional-validation-rules完成，结果纳入最终报告。
- 若涉及回归验证，可调用	est-regression-rules完成，结果纳入最终报告。

## 需要暂停并确认的条件
- 测试环境不可用、鉴权信息缺失、依赖数据无法准备，导致无法执行测试。
- 接口基线不完整，大量接口缺少定义，无法确定测试范围和判定规则。
- agent无法判断接口是否通过，缺少判定依据，需要补充规则。
- 出现大量接口异常，无法确定是实现问题还是测试环境问题。
- 最终结论为PARTIAL，需要用户确认是否接受风险上线。

## 执行通过/驳回标准
- 通过：所有必测P0接口全部通过，P1接口无阻断级失败，风险项已明确说明，报告符合格式要求，结论清晰可决策。
- 驳回：存在P0接口失败，报告不符合格式要求（使用Markdown表格），请求参数或简要响应不是JSON字符串，agent未给出独立判定理由，结论不清晰，缺少关键证据文件。

## 执行结果归档要求
- 测试主结论写入doc/5-tests/YYYY-MM-DD_HHmmss_上线前项目接口测试/README.md，包含：测试范围、必测接口总数、通过数、失败数、待确认数、门禁结论、风险项、阻断原因（如果有）。
- 接口测试明细报告写入ASCII镜像目录下的interface-test-results.md，每个接口按块状格式输出，不使用Markdown表格。
- 每个接口的完整响应、测试脚本、依赖数据、执行日志全部归档到ASCII镜像目录，按模块或接口路径组织。
- 项目接口基线更新到doc/5-tests/基线/interface-inventory.yaml，跨项目迭代复用。
- 所有归档遵循rtifact-storage-rules和	est-doc-rules的要求，中文说明目录只放主README，其他内容全部放入ASCII镜像目录。

## references 读取规则
- 默认先读eferences/interface-inventory-schema.md，确认接口基线字段结构。
- 筛选测试范围时读eferences/test-selection-policy.md。
- 判定接口响应时读eferences/agent-response-judgement.md。
- 输出报告时读eferences/report-format.md。
- 输出门禁结论时读eferences/execution-gate.md。
- 确认和现有测试skill集成关系时读eferences/existing-test-skill-integration.md。
