# 和现有测试域 Skill 集成规则

本文件明确project-release-test-rules和现有测试域其他skill的分工边界、调用关系、数据流转规则，避免职责重叠或冲突。

## 核心分工边界
| Skill名称 | 职责范围 | 和本skill的关系 |
| --- | --- | --- |
| 	est-strategy-rules | 任务级测试的策略规划、优先级、范围 | 本skill是项目级上线测试的策略，不替代任务级测试策略，两者独立执行，可并行 |
| unctional-validation-rules | 任务级的当前改动功能验证 | 本skill可调用它执行单个接口的功能验证，结果纳入本skill的报告，本skill不做单接口的功能验证细节 |
| 	est-regression-rules | 任务级的改动影响面回归验证 | 本skill做全项目核心接口的上线前回归，两者覆盖范围不同，独立执行，可并行 |
| 	est-task-root-layout-rules | 测试目录的创建、结构规范 | 本skill必须遵循它的要求，所有测试资产落地到doc/5-tests/时间戳根目录 |
| 	est-doc-rules | 测试文档的结构、归档规则 | 本skill的报告必须遵循它的要求，中文说明目录只放主README，其他内容放ASCII镜像目录 |
| 	est-program-rules | 测试脚本、资产的组织规则 | 本skill的测试脚本、用例、数据必须遵循它的要求 |
| 	est-naming-rules | 测试目录、文件的命名规则 | 本skill的所有资产命名必须遵循它的要求 |
| 	est-scattered-asset-location-rules | 散落测试资产的收拢规则 | 本skill的测试资产必须全部收拢到对应时间戳根目录，不得散落 |
| inal-acceptance-rules | 最终上线验收 | 本skill的结论是它的输入之一，最终验收必须参考本skill的门禁结论 |
| implementation-review-rules | 实现完成后的代码审查 | 本skill在测试执行前必须确保它已经通过，代码审查不通过不执行测试 |
| project-change-review-rules | 最终上线前的改动总审查 | 本skill的结论是它的输入之一，总审查必须参考测试门禁结论 |

## 联动执行流程
推荐的完整上线前测试流程顺序：
1. 代码实现完成 → 执行implementation-review-rules → 代码审查通过。
2. 执行unctional-validation-rules → 当前改动功能验证通过。
3. 执行	est-regression-rules → 改动影响面回归验证通过。
4. 执行project-release-test-rules → 上线前全项目核心接口测试 → 得到门禁结论。
5. 执行project-change-review-rules → 全量改动总审查，参考测试结论。
6. 执行inal-acceptance-rules → 参考所有测试和审查结论，给出最终验收结论。

## 数据流转规则
1. 本skill的测试目录创建、结构必须完全遵循	est-task-root-layout-rules的要求，不得自定义目录结构。
2. 本skill的测试文档、报告、归档必须完全遵循	est-doc-rules和rtifact-storage-rules的要求。
3. 本skill的接口测试执行可以调用unctional-validation-rules完成，结果直接复用，不需要重复测试。
4. 本skill的回归相关测试可以调用	est-regression-rules完成，结果直接复用。
5. 本skill的最终结论必须输出成inal-acceptance-rules可直接读取的格式，作为验收输入。
6. 本skill维护的项目接口基线可以被所有其他测试skill复用，避免重复梳理接口。

## 冲突处理规则
1. 当本skill的规则和现有其他测试skill的规则冲突时，本skill作为上线门禁优先级更高，按本skill的规则执行。
2. 当测试范围重叠时，以更严格的覆盖要求为准，不需要重复测试，可互相复用结果。
3. 当结论冲突时，以本skill的门禁结论为准，任务级测试结论作为补充。
