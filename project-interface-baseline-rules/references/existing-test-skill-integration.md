# 和现有测试域 Skill 集成规则

本文件明确 `project-interface-baseline-rules` 与 `project-interface-release-execution-rules` 和现有测试域其他 skill 的分工边界、调用关系与数据流转规则，避免职责重叠或冲突。

## 核心分工边界

| Skill 名称 | 职责范围 | 和本 skill 的关系 |
| --- | --- | --- |
| `test-strategy-rules` | 任务级测试的策略规划、优先级和覆盖范围 | 本 skill 是项目级上线测试门禁，不替代任务级测试策略；两者可并行，但上线门禁前必须先有清晰策略 |
| `functional-validation-rules` | 任务级的当前改动功能验证 | 本 skill 可调用它执行单接口功能验证，结果纳入项目级门禁报告；本 skill 不替代单接口功能语义验证细节 |
| `test-regression-rules` | 任务级的改动影响面回归验证 | 本 skill 关注项目级核心接口的上线前门禁回归，两者覆盖范围不同，可并行并复用结果 |
| `test-task-root-layout-rules` | 测试目录的创建和结构规范 | 本 skill 必须遵循它的要求，所有测试资产落地到 `doc/5-tests/` 的时间戳根目录 |
| `test-doc-rules` | 测试文档的结构和归档规则 | 本 skill 的报告必须遵循它的要求，中文说明目录只放主 `README.md`，其他内容放 ASCII 镜像目录 |
| `test-program-rules` | 测试脚本、测试程序和资产的组织规则 | 本 skill 的测试脚本、用例和数据必须遵循它的要求 |
| `test-naming-rules` | 测试目录和文件命名规则 | 本 skill 的所有资产命名必须遵循它的要求 |
| `test-scattered-asset-location-rules` | 散落测试资产的收拢规则 | 本 skill 的测试资产必须全部收拢到对应时间戳根目录，不得散落 |
| `final-acceptance-rules` | 最终上线验收 | 本 skill 的门禁结论是它的正式输入之一，最终验收必须引用本 skill 的结论 |
| `implementation-review-rules` | 实现完成后的代码审查 | 本 skill 在测试执行前必须确认其已通过，代码审查不通过不得执行门禁测试 |
| `project-change-review-rules` | 最终上线前的改动总审查 | 本 skill 的结论是其输入之一，总审查必须参考测试门禁结论 |

## 联动执行流程

推荐的完整上线前测试流程顺序：

1. 代码实现完成，执行 `implementation-review-rules`，完成测试前静态自审。
2. 执行 `functional-validation-rules`，确认当前改动功能验证通过。
3. 执行 `test-regression-rules`，确认改动影响面回归验证通过。
4. 执行 `project-interface-release-execution-rules`，完成上线前项目级核心接口测试并得到门禁结论。
5. 执行 `project-change-review-rules`，参考测试门禁结论完成全量改动总审查。
6. 执行 `final-acceptance-rules`，综合测试与审查结论给出最终验收结论。

## 数据流转规则

1. 本 skill 的测试目录创建和结构必须完全遵循 `test-task-root-layout-rules` 的要求，不得自定义目录结构。
2. 本 skill 的测试文档、测试报告和归档必须完全遵循 `test-doc-rules` 和 `artifact-storage-rules` 的要求。
3. 本 skill 的接口测试执行可以调用 `functional-validation-rules` 完成，结果直接复用，不需要重复测试。
4. 本 skill 的回归相关测试可以调用 `test-regression-rules` 完成，结果直接复用。
5. 本 skill 的最终结论必须输出成 `final-acceptance-rules` 可直接读取的格式，作为正式验收输入。
6. 本 skill 维护的项目接口基线可以被所有其他测试 skill 复用，避免重复梳理接口。
7. 每次执行本 skill 前都必须先扫描并对账当前接口基线；若发现新增、删除或漂移信息，必须先回写基线再继续门禁测试。

## 冲突处理规则

1. 当本 skill 的规则和现有其他测试 skill 的规则冲突时，本 skill 作为上线门禁优先级更高，按本 skill 的规则执行。
2. 当测试范围重叠时，以更严格的覆盖要求为准，不需要重复测试，但必须明确复用哪一份结果。
3. 当结论冲突时，以本 skill 的门禁结论为准，任务级测试结论作为补充证据。
