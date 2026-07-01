---
name: project-release-test-rules
description: 当需要做上线前项目级全接口测试、替代人工接口回归验证、生成上线接口测试门禁结论时触发。负责在每次执行前扫描并更新项目接口基线、规划测试范围、执行接口验证、给出 agent 判定的接口级结果和上线放行结论；所有测试资产落地到 `doc/5-tests/` 对应时间戳根目录，强制要求请求参数和简要响应为 JSON 字符串，禁止接口明细输出为 Markdown 表格。
---

# 项目上线接口测试门禁规则

只在“上线前需要统一做项目级接口测试、替代人工全接口验证、输出上线准入结论”时使用这个 skill。
如果是任务级功能验证、改动影响面回归，分别转交 `functional-validation-rules`、`test-regression-rules`；如果是测试文档组织、目录结构，转交 `test-doc-rules`、`test-task-root-layout-rules`。

## 测试隔离红线（强制，和现有测试域规则一致）
- 严禁为了测试目的改动生产代码语义，包括但不限于新增测试专用方法、测试专用数据、测试专用结构体字段。
- 接口测试必须基于真实业务实现和测试资产完成，禁止通过向生产代码注入测试专用能力来“制造通过”结果。
- 一旦发现生产代码测试污染，测试结论直接无效并阻断，先回退污染改动再重测。
- 当前仓库上线前接口测试也属于**本地自动化测试**：只能使用 `local` 环境信息执行，不得改动 `test` 配置文件，不得连接 `test` / `prod` / `staging` 环境数据库、缓存、消息队列、HTTP/RPC 上游或其他非 local 服务。

## Skill 作用与适用场景
- 作为上线前的项目级接口质量门禁，统一规划全项目接口测试范围、选择必测接口、执行验证、输出可决策的结论。
- 维护项目级接口测试基线，沉淀可复用的接口定义、参数规则、判定标准，避免每次上线重新梳理接口。
- 强制每次执行前先扫描当前项目接口事实，发现新增接口、删除接口和接口信息漂移后，先更新基线再做测试计划。
- 自动由 agent 判定接口响应是否符合预期，替代人工逐一查看响应结果。
- 输出标准化的测试报告，明确给出是否允许上线的结论，作为 `final-acceptance-rules` 的输入之一。
- 强制所有测试资产落地到 `doc/5-tests/` 下的时间戳根目录，遵循现有测试域的归档规则。

## 自动触发信号
- 上线前需要做全项目接口回归验证。
- 需要替代人工做接口测试和响应判断。
- 需要输出上线接口测试准入结论。
- 项目迭代后需要验证所有核心接口是否正常。
- 用户明确要求做“项目级接口测试”“上线前全接口测试”“接口测试门禁”。

## 首次触发冷启动规则（强制）
- 若项目从未触发过本 skill，或 `doc/5-tests/基线/interface-inventory.yaml` 不存在，必须自动进入冷启动流程。
- 冷启动时不得因为“没有现成测试产物”直接阻断；必须先扫描项目路由、controller/handler、Swagger/OpenAPI、现有测试、README 和接口文档，生成第一版接口基线。
- 第一版接口基线允许存在 `待确认项`，但每个待确认项都必须记录发现来源、证据和缺失原因，禁止伪装成完整基线。
- 冷启动时必须联动 `test-task-root-layout-rules` 建立测试任务根目录、中文说明目录、ASCII 镜像目录和主 `README.md` 骨架。
- 冷启动时必须同时生成初版测试计划骨架与测试产物骨架，保证后续测试和门禁结论有正式落点。

## 接口基线扫描规则（强制）
- 每次执行本 skill 前，都必须先做一次接口基线扫描；首次触发执行全量建基线，后续执行默认做增量扫描。
- 扫描来源至少覆盖：路由声明、controller/handler、Swagger/OpenAPI、现有接口测试、项目 README/接口文档，以及当前待上线改动对应的 diff。
- 扫描不是可选优化，而是门禁前置步骤；未完成扫描不得直接进入测试范围筛选和门禁结论阶段。
- 若扫描发现新增接口、删除接口、路径变更、HTTP 方法变更、鉴权变更、请求/响应结构漂移，必须先更新基线，再生成测试计划。
- 若当前代码与基线冲突且无法自动判定，以 `待确认` 标记差异并阻断该接口的自动放行判断。

## 基线漂移处理规则（强制）
- 新增接口：必须补入基线，至少写明风险等级、发现来源、发现证据、完整度和待确认项。
- 删除或废弃接口：必须更新基线状态，不得继续按有效接口纳入门禁。
- 接口路径、HTTP 方法、鉴权方式、请求参数 schema、响应结构摘要、成功/失败判定规则发生变化时，必须先更新基线，再决定测试集合。
- 若某接口的历史测试结论已被当前代码变更推翻，必须将该接口标记为待重测，不得沿用旧结论。
- 若基线漂移会影响 `final-acceptance-rules` 的输入完整性，必须阻断最终自动放行。

## 进入后先做什么
1. 先确认当前项目是否已存在接口基线；若不存在，则进入冷启动。
2. 无论是否已存在基线，都先按 `references/interface-inventory-schema.md` 扫描并对账当前接口事实。
3. 按 `references/inventory-reconcile-rules.md` 输出新增、删除、变更和待确认清单，并先更新接口基线。
4. 确认本次上线的改动范围、影响模块，按 `references/test-selection-policy.md` 筛选本次必测接口集合。
5. 按 `test-task-root-layout-rules` 创建或复用本次测试的时间戳根目录、中文说明目录和 ASCII 镜像目录。
6. 明确本地测试环境、鉴权信息、依赖数据要求，准备测试前置条件；连接信息必须来自 `local` 配置，若接口依赖外部服务，只能使用本地代理、本地 mock 或本地启动配置中的代理设置（如 `httpConfig.proxy`），不得直连 test / prod / staging 服务。
7. 按 `references/test-data-construction-rules.md` 查询本地 `local` 环境对应数据库获取真实数据，识别接口对应的数据库表，为每个必测接口构造请求参数。
8. 按 `references/agent-response-judgement.md` 定义判定规则，确保 agent 可以独立判断接口是否通过。
9. 按 `references/report-format.md` 和 `references/output-artifacts.md` 定义输出格式与产物清单。

## 默认执行流程
1. 默认先执行接口基线扫描：首次触发执行全量扫描，后续执行默认做增量扫描。
2. 若当前项目尚无接口基线，按 `references/bootstrap-workflow.md` 生成初版 `doc/5-tests/基线/interface-inventory.yaml`。
3. 按 `references/inventory-reconcile-rules.md` 将扫描结果与现有基线对账，输出新增、删除、变更和待确认清单，并更新基线。
4. 调用 `test-task-root-layout-rules` 创建本次项目级接口测试的时间戳根目录，中文说明目录命名为上线前项目接口测试，包含主 `README.md`，ASCII 镜像目录存放真实测试脚本、原始响应和证据文件。
5. 按 `references/test-selection-policy.md` 筛选本次必测接口、可选测接口、跳过接口，明确每个接口的选择/跳过理由。
6. 为每个必测接口准备测试用例：按 `references/test-data-construction-rules.md` 查询本地 `local` 环境数据库获取最近真实记录，构造请求参数、预期语义规则、环境依赖和清理方式；不得用不存在的数据测试并接受失败为通过。
7. 执行接口测试，记录每个接口的请求参数（JSON 字符串）、简要响应（JSON 字符串，脱敏）、完整响应（落盘到 ASCII 镜像目录）。
8. 按 `references/agent-response-judgement.md` 由 agent 独立判断每个接口是否通过，给出判定理由，不依赖人工判断。
9. 按 `references/report-format.md` 生成接口测试明细报告，每个接口使用块状格式，不使用 Markdown 表格。
10. 按 `references/execution-gate.md` 输出最终门禁结论：PASS / FAIL / PARTIAL，明确是否允许上线、阻断原因和风险项。
11. 按 `references/output-artifacts.md` 将测试计划、接口清单、报告、结论、完整响应、执行日志、请求样本等产物归档到对应时间戳根目录。
12. 将本次测试结论同步到接口基线，更新对应接口的最近扫描时间、最近测试时间和测试结论。
13. 将最终结论同步到 `final-acceptance-rules`，作为最终验收的输入之一。

## 权责边界与不负责事项
- 负责项目级上线前接口测试，不替代任务级 `functional-validation-rules` 的当前改动功能验证。
- 不替代 `test-regression-rules` 的改动影响面回归验证，两者可并行执行但覆盖范围不同。
- 不负责测试文档的结构和归档规则，必须遵循 `test-doc-rules` 和 `artifact-storage-rules` 的要求。
- 不负责测试目录的创建和结构，必须遵循 `test-task-root-layout-rules` 的要求。
- 测试执行如果涉及单接口功能验证，可调用 `functional-validation-rules` 完成，结果纳入最终报告。
- 若涉及回归验证，可调用 `test-regression-rules` 完成，结果纳入最终报告。

## 需要暂停并确认的条件
- 本地 `local` 环境不可用、鉴权信息缺失、依赖数据无法准备，导致无法执行测试。
- 外部服务连接超时或失败，且未确认是否因代理未配置导致；必须先排查代理配置后再判定接口结果。
- 扫描后仍无法确认大量接口的入口、鉴权方式或成功/失败判定规则。
- agent 无法判断接口是否通过，缺少判定依据，需要补充规则。
- 出现大量接口异常，无法确定是实现问题还是本地环境问题。
- 最终结论为 PARTIAL，需要用户确认是否接受风险上线。

## 执行通过 / 驳回标准
- 通过：每次执行前都已完成接口基线扫描和基线对账；所有必测 P0 接口全部通过；P1 接口无阻断级失败；风险项已明确说明；报告与测试资产符合格式要求；结论清晰可决策。
- 驳回：未先扫描基线就直接筛选测试范围；存在 P0 接口失败；接口新增/漂移未回写基线；报告不符合格式要求（例如接口明细使用 Markdown 表格）；请求参数或简要响应不是 JSON 字符串；agent 未给出独立判定理由；结论不清晰；缺少关键证据文件。

## 执行结果归档要求
- 测试主结论写入 `doc/5-tests/YYYY-MM-DD_HHmmss_上线前项目接口测试/README.md`，包含：测试范围、必测接口总数、通过数、失败数、待确认数、门禁结论、风险项、阻断原因（如果有）。
- 接口测试明细报告写入 ASCII 镜像目录下的 `interface-test-results.md`，每个接口按块状格式输出，不使用 Markdown 表格。
- 每个接口的完整响应、简要响应、请求样本、测试脚本、依赖数据、执行日志全部归档到 ASCII 镜像目录，按模块或接口路径组织。
- 项目接口基线更新到 `doc/5-tests/基线/interface-inventory.yaml`，跨项目迭代复用。
- 所有归档遵循 `artifact-storage-rules` 和 `test-doc-rules` 的要求，中文说明目录只放主 `README.md`，其他内容全部放入 ASCII 镜像目录。

## references 读取规则
- 默认先读 `references/interface-inventory-schema.md`，确认接口基线字段结构。
- 首次触发或缺少基线时，追加读取 `references/bootstrap-workflow.md`。
- 每次扫描后对账时，追加读取 `references/inventory-reconcile-rules.md`。
- 筛选测试范围时读 `references/test-selection-policy.md`。
- 判定接口响应时读 `references/agent-response-judgement.md`。
- 输出报告时读 `references/report-format.md`。
- 输出门禁结论时读 `references/execution-gate.md`。
- 确认和现有测试 skill 集成关系时读 `references/existing-test-skill-integration.md`。
- 明确应产出的测试资产时读 `references/output-artifacts.md`。
- 构造测试请求参数时读 `references/test-data-construction-rules.md`。
