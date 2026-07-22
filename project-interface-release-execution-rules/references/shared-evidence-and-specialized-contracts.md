# shared-evidence-and-specialized-contracts

> 归属 owner：`project-interface-release-execution-rules`。本文件是条件路由的细则承载，不产生独立自动触发入口；所有原有规则、用户习惯、安全边界、授权边界、暂停条件和归档要求在迁移后继续有效。

## 参数依赖与复用规则（强制）
- 目标接口存在未知必填参数时，agent 必须按顺序尝试 `reusable_param -> upstream_api -> local_database -> local_cache -> openapi_example -> fixture -> rule`，禁止直接手写猜测值；OpenAPI 示例只作为参数形状和示例格式候选，不能替代真实业务数据复验。
- `upstream_api` 来源必须先成功执行 provider 接口，再按 `response_path`、`selector` 和 `extract` 解析候选值。
- 已解析参数必须写入 `dependency-trace.json`，至少包含目标接口、参数名、来源类型、来源接口或来源表、响应文件、提取路径、选择规则和是否成功解析。
- provider 接口失败时，依赖它的 consumer 接口标记为 `BLOCKED_BY_DEPENDENCY`；provider 成功但必填参数无法提取时，标记为 `PARAM_UNRESOLVED`；不得误判为目标接口自身失败。
- 复用 `project-interface-baseline-rules` 维护的 `reusable-params.yaml` 参数样本前，P0 / P1 接口、写接口、状态敏感接口必须先做轻量复验；复验失败时更新参数状态并回退到来源解析流程。
## 可复用脚本工具箱优先规则（强制）
- 每次上线测试前必须先检查 `project-interface-release-execution-rules/scripts/` 是否已有扫描、对账、依赖图、参数解析、可复用参数复验、基线回写、执行、判定或报告脚本。
- 已有脚本能覆盖时必须复用；缺能力时优先扩展已有通用脚本；项目专属适配写入项目 `doc/5-tests/基线/script-adapter.yaml` 或当轮测试任务目录，不写死到通用脚本。
- 连续两次复用的项目适配逻辑，应抽象为通用脚本参数或插件点。
- 统一可执行内核位于 `scripts/release_test_engine/`；兼容入口 `scripts/generate_release_test_plan.py doctor/run` 必须优先委派到 `release_test_engine.cli.run_doctor/run_pipeline`，旧十个资产命令在内核不可用时才回退旧逻辑。
- 内核支持矩阵由 adapter 声明并随运行结果输出；未识别协议、缺少适配器或缺少 local 配置必须输出 `PENDING`/`BLOCKED` 与证据，禁止把未知入口计入通过数。
- 接口级结果只允许 `PASS`、`EXPECTED_FAIL`、`FAIL`、`PENDING`、`BLOCKED`；项目门禁仍输出 `PASS`、`FAIL` 或 `PARTIAL`，其中 P0 入口任意非 `PASS` 都阻断自动放行。
- 通用规则不得出现项目专属实体、表名、错误码或业务字段；此类内容只能放在项目 `script-adapter.yaml`、参数来源或接口基线中。
## 进入后先做什么
1. 确认 `project-interface-baseline-rules` 是否已提供最新接口基线；若基线过期或不存在，先转交对方刷新，不自行扫描。
2. 确认本次上线的改动范围、影响模块，按 `references/test-selection-policy.md` 筛选本次必测接口集合。
3. 按 `test-strategy-rules 的 test-asset-governance 条件路由` 创建或复用本次测试的时间戳根目录、中文说明目录和 ASCII 镜像目录。
4. 明确本地测试环境、鉴权信息、依赖数据要求，准备测试前置条件；连接信息必须来自 `local` 配置，若接口依赖外部服务，只能使用本地代理、本地 mock 或本地启动配置中的代理设置（如 `httpConfig.proxy`），不得直连 test / prod / staging 服务。
5. 按 `references/test-data-construction-rules.md` 与基线提供的依赖图解析每个必测接口的请求参数，优先复用已验证参数，失效后持续更新。
6. 按 `references/agent-response-judgement.md` 定义判定规则，确保 agent 可以独立判断接口是否通过。
7. 按 `references/report-format.md` 和 `references/output-artifacts.md` 定义输出格式与产物清单。
## 默认执行流程
1. 调用 `test-strategy-rules 的 test-asset-governance 条件路由` 创建本次项目级接口测试的时间戳根目录，中文说明目录命名为上线前项目接口测试，包含主 `README.md`，ASCII 镜像目录存放真实测试脚本、原始响应和证据文件。
2. 按 `references/test-selection-policy.md` 筛选本次必测接口、可选测接口、跳过接口，明确每个接口的选择/跳过理由。
3. 使用基线提供的 provider / consumer 依赖图构建本轮场景执行顺序。
4. 为每个必测接口准备测试用例：优先从 `reusable-params.yaml` 取已验证参数；复验失败后，按参数来源规则从 provider 接口、本地 local 数据库、缓存、OpenAPI 示例、fixture 或规则重新解析；不得用不存在的数据测试并接受失败为通过。
5. 执行接口测试，记录每个接口的请求参数（JSON 字符串）、简要响应（JSON 字符串，脱敏）、完整响应（落盘到 ASCII 镜像目录）和参数依赖追踪。
6. 按 `references/agent-response-judgement.md` 由 agent 独立判断每个接口是否通过，给出判定理由，不依赖人工判断。
7. 按 `references/report-format.md` 生成接口测试明细报告，每个接口使用块状格式，不使用 Markdown 表格。
8. 按 `references/execution-gate.md` 输出最终门禁结论：PASS / FAIL / PARTIAL，明确是否允许上线、阻断原因和风险项。
9. 按 `references/output-artifacts.md` 将测试计划、接口清单、报告、结论、完整响应、执行日志、请求样本、依赖图、已解析参数和参数复用/失效记录归档到对应时间戳根目录。
10. 将本次测试结论、新发现的可复用参数、失效参数、场景结论和历史摘要回写到 `project-interface-baseline-rules` 维护的 `doc/5-tests/基线/` 长期资产。
11. 将最终结论同步到 `final-acceptance-rules`，作为最终验收的输入之一。
## 权责边界与不负责事项
- 负责项目级上线前接口测试执行与放行，不负责接口事实基线的扫描、初始化或双索引同步，这些由 `project-interface-baseline-rules` 负责。
- 不替代任务级 `functional-validation-rules` 的当前改动功能验证。
- 不替代 `test-regression-rules` 的改动影响面回归验证，两者可并行执行但覆盖范围不同。
- 不负责测试文档的结构和归档规则，必须遵循 `test-strategy-rules 的 test-asset-governance 条件路由` 和 `artifact-storage-rules` 的要求。
- 不负责测试目录的创建和结构，必须遵循 `test-strategy-rules 的 test-asset-governance 条件路由` 的要求。
- 测试执行如果涉及单接口功能验证，可调用 `functional-validation-rules` 完成，结果纳入最终报告。
- 若涉及回归验证，可调用 `test-regression-rules` 完成，结果纳入最终报告。
## 需要暂停并确认的条件
- 本地 `local` 环境不可用、鉴权信息缺失、依赖数据无法准备，导致无法执行测试。
- 外部服务连接超时或失败，且未确认是否因代理未配置导致；必须先排查代理配置后再判定接口结果。
- agent 无法判断接口是否通过，缺少判定依据，需要补充规则。
- 出现大量接口异常，无法确定是实现问题还是本地环境问题。
- 最终结论为 PARTIAL，需要用户确认是否接受风险上线。
## 执行通过 / 驳回标准
- 通过：未知必填参数已按来源规则解析或明确标记；可复用参数已按风险复验；所有必测 P0 接口全部通过或给出合规阻断归类；P1 接口无阻断级失败；风险项已明确说明；报告与测试资产符合格式要求；结论清晰可决策。
- 驳回：存在 P0 接口失败；未知必填参数凭空构造；历史参数失效后仍继续复用；依赖接口失败却误判目标接口失败；报告不符合格式要求（例如接口明细使用 Markdown 表格）；请求参数或简要响应不是 JSON 字符串；agent 未给出独立判定理由；结论不清晰；缺少关键证据文件。
## 执行结果归档要求
- 测试主结论写入 `doc/5-tests/YYYY-MM-DD_HHmmss_上线前项目接口测试/README.md`，包含：测试范围、必测接口总数、通过数、失败数、待确认数、门禁结论、风险项、阻断原因（如果有）。
- 接口测试明细报告写入 ASCII 镜像目录下的 `interface-test-results.md`，每个接口按块状格式输出，不使用 Markdown 表格。
- 双索引同步报告写入 ASCII 镜像目录下的 `interface-sync-report.yaml`，字段结构由 `project-interface-baseline-rules` 定义。
- 每个接口的完整响应、简要响应、请求样本、测试脚本、依赖数据、执行日志全部归档到 ASCII 镜像目录，按模块或接口路径组织。
- 所有归档遵循 `artifact-storage-rules` 和 `test-strategy-rules 的 test-asset-governance 条件路由` 的要求，中文说明目录只放主 `README.md`，其他内容全部放入 ASCII 镜像目录。
