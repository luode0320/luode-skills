---
name: project-release-test-rules
description: 当需要做上线前项目级全接口测试、替代人工接口回归验证、生成上线接口测试门禁结论时触发。负责在每次执行前扫描并持续更新项目基线资产库（接口清单、Swagger/OpenAPI 双索引、参数来源、依赖图、可复用参数、场景目录、脚本适配和历史结论）、规划测试范围、按依赖图构造请求参数并执行接口验证、给出 agent 判定的接口级结果和上线放行结论；所有测试资产落地到 `doc/5-tests/` 对应时间戳根目录，强制要求请求参数和简要响应为 JSON 字符串，禁止接口明细输出为 Markdown 表格。
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
- 将每个项目的 `doc/5-tests/基线/` 作为长期测试资产库，持续沉淀接口清单、参数来源、依赖图、可复用参数、可复用场景、脚本适配和历史执行摘要。
- 将 `swag/.swag-manifest.yaml` 与 `doc/5-tests/基线/interface-inventory.yaml` 视为当前代码接口事实的双索引；任一缺失、陈旧或接口集合不一致时，必须先从当前代码刷新两边，再进入上线测试。
- 对之前已经构造且测试通过的参数样本执行可复用生命周期管理：可优先复用，但必须支持复验、过期、失效、隔离和持续更新。
- 强制每次执行前先扫描当前项目接口事实，发现新增接口、删除接口和接口信息漂移后，先更新基线再做测试计划。
- 当目标接口参数无法直接确定时，必须先从基线资产、已成功 provider 接口响应、本地 local 数据库 / 缓存、fixture 或规则中解析，禁止凭空构造必填参数。
- 优先复用 `project-release-test-rules/scripts/` 的通用脚本工具箱；已有能力能覆盖时不得每轮重复生成同类脚本。
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
- 冷启动时必须同时初始化 `doc/5-tests/基线/` 基线资产库，至少包含 `interface-inventory.yaml`、`dependency-graph.yaml`、`parameter-sources.yaml`、`reusable-params.yaml`、`scenario-catalog.yaml`、`script-adapter.yaml`、`execution-history.yaml`、`baseline-change-log.md` 和 `README.md` 的骨架。
- 第一版接口基线允许存在 `待确认项`，但每个待确认项都必须记录发现来源、证据和缺失原因，禁止伪装成完整基线。
- 冷启动时必须联动 `test-task-root-layout-rules` 建立测试任务根目录、中文说明目录、ASCII 镜像目录和主 `README.md` 骨架。
- 冷启动时必须同时生成初版测试计划骨架与测试产物骨架，保证后续测试和门禁结论有正式落点。

## 接口基线扫描规则（强制）
- 每次执行本 skill 前，都必须先做一次接口基线扫描；首次触发执行全量建基线，后续执行默认做增量扫描。
- 扫描来源至少覆盖：路由声明、controller/handler、Swagger/OpenAPI、现有接口测试、项目 README/接口文档，以及当前待上线改动对应的 diff。
- 扫描不是可选优化，而是门禁前置步骤；未完成扫描不得直接进入测试范围筛选和门禁结论阶段。
- 若扫描发现新增接口、删除接口、路径变更、HTTP 方法变更、鉴权变更、请求/响应结构漂移，必须先更新基线，再生成测试计划。
- 若当前代码与基线冲突且无法自动判定，以 `待确认` 标记差异并阻断该接口的自动放行判断。

## Swagger/OpenAPI 双索引同步规则（强制）
- 当前代码是接口事实的唯一真相源；`swag/.swag-manifest.yaml` 与 `doc/5-tests/基线/interface-inventory.yaml` 只是两个视图，不允许长期独立漂移。
- 正常项目中两者理论上都不应缺失；如果任一文件缺失，不能只补缺失一边，必须判定为接口契约资产不完整，先触发 `swag-openapi-maintainer-rules` 全量刷新 `swag/`，再刷新上线测试接口基线。
- 每次上线测试前必须对比三方接口集合：当前代码扫描结果、`swag/.swag-manifest.yaml`、`interface-inventory.yaml`；三方的 `HTTP method + path` 必须一致。
- 若当前代码有接口但 swag manifest 或 interface inventory 缺失，必须先补齐两边；若当前代码已无接口但两边仍存在，swag 清理生成文件，interface inventory 标记废弃或待确认；若 schema hash 变化，interface inventory 标记 `schema_changed`，相关可复用参数标记 `stale`。
- 双索引同步报告必须落盘为 `interface-sync-report.yaml`；报告显示仍需双刷新、仍有待确认差异或 P0/P1 schema 漂移未处理时，不得继续给出自动上线放行结论。

## 基线漂移处理规则（强制）
- 新增接口：必须补入基线，至少写明风险等级、发现来源、发现证据、完整度和待确认项。
- 删除或废弃接口：必须更新基线状态，不得继续按有效接口纳入门禁。
- 接口路径、HTTP 方法、鉴权方式、请求参数 schema、响应结构摘要、成功/失败判定规则发生变化时，必须先更新基线，再决定测试集合。
- 若某接口的历史测试结论已被当前代码变更推翻，必须将该接口标记为待重测，不得沿用旧结论。
- 若接口 schema、请求参数、响应结构、鉴权或业务成功判定发生漂移，必须将相关 `reusable-params.yaml` 参数样本标记为 `stale`，本轮复用前必须复验。
- 若基线漂移会影响 `final-acceptance-rules` 的输入完整性，必须阻断最终自动放行。

## 基线资产库持续更新规则（强制）

- 每次上线测试前必须先读取 `doc/5-tests/基线/` 中的长期资产；缺失时先初始化，不能直接进入一次性测试。
- `interface-inventory.yaml` 记录接口清单和契约；`parameter-sources.yaml` 记录请求参数来源；`dependency-graph.yaml` 记录 provider / consumer 依赖关系；`reusable-params.yaml` 记录已验证可复用参数；`scenario-catalog.yaml` 记录已验证可复用场景；`script-adapter.yaml` 记录项目对通用脚本的适配；`execution-history.yaml` 记录历次摘要。
- 通过过的参数可以复用，但必须记录 `first_verified_at`、`last_verified_at`、`success_count`、`fail_count`、`status`、`ttl`、来源证据和失效原因；状态只允许 `candidate`、`reusable`、`stale`、`invalid`、`quarantined`、`retired`。
- P0 / P1 接口、写接口、状态敏感接口在复用历史参数前必须做轻量复验；复验失败时不得继续使用该参数，必须更新状态并回退到参数来源解析流程。
- 每次测试后必须回写新发现接口、参数来源、依赖边、可复用参数、可复用场景、失效参数和本轮历史摘要；不得只生成当轮报告而不更新长期基线。
- 基线资产禁止保存明文 token、密码、手机号、身份证号、银行卡号、密钥和非 local 环境连接信息；真实值只能通过本地安全引用、当轮测试产物或 local 环境重新解析获得。

## 参数依赖与复用规则（强制）

- 目标接口存在未知必填参数时，agent 必须按顺序尝试 `reusable_param -> upstream_api -> local_database -> local_cache -> openapi_example -> fixture -> rule`，禁止直接手写猜测值；OpenAPI 示例只作为参数形状和示例格式候选，不能替代真实业务数据复验。
- `upstream_api` 来源必须先成功执行 provider 接口，再按 `response_path`、`selector` 和 `extract` 解析候选值。
- 已解析参数必须写入 `dependency-trace.json`，至少包含目标接口、参数名、来源类型、来源接口或来源表、响应文件、提取路径、选择规则和是否成功解析。
- provider 接口失败时，依赖它的 consumer 接口标记为 `BLOCKED_BY_DEPENDENCY`；provider 成功但必填参数无法提取时，标记为 `PARAM_UNRESOLVED`；不得误判为目标接口自身失败。

## 可复用脚本工具箱优先规则（强制）

- 每次上线测试前必须先检查 `project-release-test-rules/scripts/` 是否已有扫描、对账、依赖图、参数解析、可复用参数复验、基线回写、执行、判定或报告脚本。
- 已有脚本能覆盖时必须复用；缺能力时优先扩展已有通用脚本；项目专属适配写入项目 `doc/5-tests/基线/script-adapter.yaml` 或当轮测试任务目录，不写死到通用脚本。
- 连续两次复用的项目适配逻辑，应抽象为通用脚本参数或插件点。
- 统一可执行内核位于 `scripts/release_test_engine/`；兼容入口 `scripts/generate_release_test_plan.py doctor/run` 必须优先委派到 `release_test_engine.cli.run_doctor/run_pipeline`，旧十个资产命令在内核不可用时才回退旧逻辑。
- 内核支持矩阵由 adapter 声明并随运行结果输出；未识别协议、缺少适配器或缺少 local 配置必须输出 `PENDING`/`BLOCKED` 与证据，禁止把未知入口计入通过数。
- 接口级结果只允许 `PASS`、`EXPECTED_FAIL`、`FAIL`、`PENDING`、`BLOCKED`；项目门禁仍输出 `PASS`、`FAIL` 或 `PARTIAL`，其中 P0 入口任意非 `PASS` 都阻断自动放行。
- 通用规则不得出现项目专属实体、表名、错误码或业务字段；此类内容只能放在项目 `script-adapter.yaml`、参数来源或接口基线中。

## 进入后先做什么
1. 先确认当前项目是否已存在接口基线；若不存在，则进入冷启动。
2. 先按 `references/baseline-asset-rules.md` 读取或初始化 `doc/5-tests/基线/` 长期资产库。
3. 无论是否已存在基线，都先按 `references/interface-inventory-schema.md` 扫描并对账当前接口事实。
4. 按 `references/openapi-inventory-sync-rules.md` 对账当前代码、`swag/.swag-manifest.yaml` 与 `interface-inventory.yaml`，缺任一方或三方不一致时先双刷新。
5. 按 `references/inventory-reconcile-rules.md` 输出新增、删除、变更和待确认清单，并先更新接口基线。
6. 若接口事实漂移影响参数来源或响应结构，先将相关可复用参数标记为 `stale`。
7. 按 `references/dependency-graph-rules.md` 读取或生成 provider / consumer 依赖图。
8. 确认本次上线的改动范围、影响模块，按 `references/test-selection-policy.md` 筛选本次必测接口集合。
9. 按 `test-task-root-layout-rules` 创建或复用本次测试的时间戳根目录、中文说明目录和 ASCII 镜像目录。
10. 明确本地测试环境、鉴权信息、依赖数据要求，准备测试前置条件；连接信息必须来自 `local` 配置，若接口依赖外部服务，只能使用本地代理、本地 mock 或本地启动配置中的代理设置（如 `httpConfig.proxy`），不得直连 test / prod / staging 服务。
11. 按 `references/test-data-construction-rules.md` 与 `references/dependency-graph-rules.md` 解析每个必测接口的请求参数，优先复用已验证参数，失效后持续更新。
12. 按 `references/agent-response-judgement.md` 定义判定规则，确保 agent 可以独立判断接口是否通过。
13. 按 `references/report-format.md` 和 `references/output-artifacts.md` 定义输出格式与产物清单。

## 默认执行流程
1. 默认先执行接口基线扫描：首次触发执行全量扫描，后续执行默认做增量扫描。
2. 若当前项目尚无接口基线资产库，按 `references/bootstrap-workflow.md` 与 `references/baseline-asset-rules.md` 生成初版 `doc/5-tests/基线/`。
3. 按 `references/openapi-inventory-sync-rules.md` 对账当前代码、`swag/.swag-manifest.yaml` 与 `interface-inventory.yaml`；任一缺失或接口集合不一致时先刷新 swag 与接口基线，并输出 `interface-sync-report.yaml`。
4. 按 `references/inventory-reconcile-rules.md` 将扫描结果与现有基线对账，输出新增、删除、变更和待确认清单，并更新基线。
5. 按接口漂移结果更新 `parameter-sources.yaml`、`dependency-graph.yaml` 和 `reusable-params.yaml` 中受影响项；受影响可复用参数先标记 `stale`。
6. 调用 `test-task-root-layout-rules` 创建本次项目级接口测试的时间戳根目录，中文说明目录命名为上线前项目接口测试，包含主 `README.md`，ASCII 镜像目录存放真实测试脚本、原始响应和证据文件。
7. 按 `references/test-selection-policy.md` 筛选本次必测接口、可选测接口、跳过接口，明确每个接口的选择/跳过理由。
8. 按 `references/dependency-graph-rules.md` 构建本轮 provider / consumer 依赖图和场景执行顺序。
9. 为每个必测接口准备测试用例：优先从 `reusable-params.yaml` 取已验证参数；复验失败后，按 `parameter-sources.yaml` 从 provider 接口、本地 local 数据库、缓存、OpenAPI 示例、fixture 或规则重新解析；不得用不存在的数据测试并接受失败为通过。
10. 执行接口测试，记录每个接口的请求参数（JSON 字符串）、简要响应（JSON 字符串，脱敏）、完整响应（落盘到 ASCII 镜像目录）和参数依赖追踪。
11. 按 `references/agent-response-judgement.md` 由 agent 独立判断每个接口是否通过，给出判定理由，不依赖人工判断。
12. 按 `references/report-format.md` 生成接口测试明细报告，每个接口使用块状格式，不使用 Markdown 表格。
13. 按 `references/execution-gate.md` 输出最终门禁结论：PASS / FAIL / PARTIAL，明确是否允许上线、阻断原因和风险项。
14. 按 `references/output-artifacts.md` 将测试计划、接口清单、报告、结论、完整响应、执行日志、请求样本、依赖图、已解析参数和参数复用/失效记录归档到对应时间戳根目录。
15. 将本次测试结论同步到接口基线，更新对应接口的最近扫描时间、最近测试时间和测试结论。
16. 将本次新发现的可复用参数、失效参数、场景结论和历史摘要持续回写 `doc/5-tests/基线/`。
17. 将最终结论同步到 `final-acceptance-rules`，作为最终验收的输入之一。

## 权责边界与不负责事项
- 负责项目级上线前接口测试，不替代任务级 `functional-validation-rules` 的当前改动功能验证。
- 不替代 `test-regression-rules` 的改动影响面回归验证，两者可并行执行但覆盖范围不同。
- 不负责测试文档的结构和归档规则，必须遵循 `test-doc-rules` 和 `artifact-storage-rules` 的要求。
- 不负责测试目录的创建和结构，必须遵循 `test-task-root-layout-rules` 的要求。
- 测试执行如果涉及单接口功能验证，可调用 `functional-validation-rules` 完成，结果纳入最终报告。
- 若涉及回归验证，可调用 `test-regression-rules` 完成，结果纳入最终报告。

## 需要暂停并确认的条件
- 本地 `local` 环境不可用、鉴权信息缺失、依赖数据无法准备，导致无法执行测试。
- 基线资产结构损坏、可复用参数未脱敏、脚本适配配置缺失关键字段，导致无法安全复用历史资产。
- 外部服务连接超时或失败，且未确认是否因代理未配置导致；必须先排查代理配置后再判定接口结果。
- 扫描后仍无法确认大量接口的入口、鉴权方式或成功/失败判定规则。
- agent 无法判断接口是否通过，缺少判定依据，需要补充规则。
- 出现大量接口异常，无法确定是实现问题还是本地环境问题。
- 最终结论为 PARTIAL，需要用户确认是否接受风险上线。

## 执行通过 / 驳回标准
- 通过：每次执行前都已完成接口基线扫描、双索引同步和基线对账；`swag/.swag-manifest.yaml` 与 `doc/5-tests/基线/interface-inventory.yaml` 均存在且接口集合一致；已读取并按需更新 `doc/5-tests/基线/` 长期资产；未知必填参数已按来源规则解析或明确标记；可复用参数已按风险复验；所有必测 P0 接口全部通过或给出合规阻断归类；P1 接口无阻断级失败；风险项已明确说明；报告与测试资产符合格式要求；结论清晰可决策。
- 驳回：未先扫描基线就直接筛选测试范围；缺少 swag manifest 或 interface inventory 却未双刷新；存在 P0 接口失败；接口新增/漂移未回写基线；未知必填参数凭空构造；历史参数失效后仍继续复用；依赖接口失败却误判目标接口失败；报告不符合格式要求（例如接口明细使用 Markdown 表格）；请求参数或简要响应不是 JSON 字符串；agent 未给出独立判定理由；结论不清晰；缺少关键证据文件。

## 执行结果归档要求
- 测试主结论写入 `doc/5-tests/YYYY-MM-DD_HHmmss_上线前项目接口测试/README.md`，包含：测试范围、必测接口总数、通过数、失败数、待确认数、门禁结论、风险项、阻断原因（如果有）。
- 接口测试明细报告写入 ASCII 镜像目录下的 `interface-test-results.md`，每个接口按块状格式输出，不使用 Markdown 表格。
- 双索引同步报告写入 ASCII 镜像目录下的 `interface-sync-report.yaml`，记录当前代码、swag manifest 与 interface inventory 的三方接口集合、漂移和处理结果。
- 每个接口的完整响应、简要响应、请求样本、测试脚本、依赖数据、执行日志全部归档到 ASCII 镜像目录，按模块或接口路径组织。
- 项目长期测试资产更新到 `doc/5-tests/基线/`，至少维护 `interface-inventory.yaml`、`dependency-graph.yaml`、`parameter-sources.yaml`、`reusable-params.yaml`、`scenario-catalog.yaml`、`script-adapter.yaml`、`execution-history.yaml`、`baseline-change-log.md` 和 `README.md`。
- 所有归档遵循 `artifact-storage-rules` 和 `test-doc-rules` 的要求，中文说明目录只放主 `README.md`，其他内容全部放入 ASCII 镜像目录。

## references 读取规则
- 默认先读 `references/interface-inventory-schema.md`，确认接口基线字段结构。
- 每次执行前必须读 `references/baseline-asset-rules.md`，确认基线资产库结构、可复用参数生命周期和持续更新策略。
- 首次触发或缺少基线时，追加读取 `references/bootstrap-workflow.md`。
- 每次进入测试计划前必须读 `references/openapi-inventory-sync-rules.md`，确认 Swagger/OpenAPI 双索引同步和三方对账规则。
- 每次扫描后对账时，追加读取 `references/inventory-reconcile-rules.md`。
- 筛选测试范围时读 `references/test-selection-policy.md`。
- 构建 provider / consumer 依赖和参数绑定时读 `references/dependency-graph-rules.md`。
- 判定接口响应时读 `references/agent-response-judgement.md`。
- 输出报告时读 `references/report-format.md`。
- 输出门禁结论时读 `references/execution-gate.md`。
- 确认和现有测试 skill 集成关系时读 `references/existing-test-skill-integration.md`。
- 明确应产出的测试资产时读 `references/output-artifacts.md`。
- 构造测试请求参数时读 `references/test-data-construction-rules.md`。
- 调用或新增测试工具脚本前读 `references/reusable-script-toolbox.md`。
