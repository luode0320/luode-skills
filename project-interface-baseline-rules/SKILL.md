---
name: project-interface-baseline-rules
description: 当需要建立、刷新或核对项目接口事实基线时触发，包括扫描接口路由/controller、维护 Swagger/OpenAPI 双索引一致性、构建 provider/consumer 依赖图、管理参数来源与可复用参数的生命周期状态、判定基线是否漂移。负责在 `doc/5-tests/基线/` 长期资产库里持续沉淀接口清单、依赖图、参数来源和可复用参数；本 skill 只消费 `project-interface-release-execution-rules` 统一执行内核（`release_test_engine`）产出的运行结果，不持有该内核的实现，也不负责执行测试、判定接口响应或输出上线放行结论。
---

# 项目接口事实基线规则

只在“需要确认或刷新项目当前接口事实、维护长期基线资产库”时使用这个 skill。
如果需要执行测试、判定接口响应、输出上线放行结论，转交 `project-interface-release-execution-rules`；如果是任务级功能验证或改动影响面回归，分别转交 `functional-validation-rules`、`test-regression-rules`；如果是测试文档组织或目录结构，转交 `test-strategy-rules 的 test-asset-governance 条件路由`、`test-strategy-rules 的 test-asset-governance 条件路由`。

本 skill 与 `project-interface-release-execution-rules` 是同源拆分：本 skill 负责“接口事实是什么”，对方负责“测试怎么跑、结果是否通过”。共享执行内核 `scripts/release_test_engine/` 已物理迁移至 `project-interface-release-execution-rules/scripts/`，`project-interface-release-execution-rules` 是其唯一行为 owner；本 skill 只读取该内核产出的基线资产文件，不复制、不重写其代码。

## 测试隔离红线（强制，和现有测试域规则一致）
- 严禁为了测试目的改动生产代码语义，包括但不限于新增测试专用方法、测试专用数据、测试专用结构体字段。
- 接口基线扫描必须基于真实业务实现完成，禁止通过向生产代码注入测试专用能力来“制造基线”。
- 一旦发现生产代码测试污染，基线结论直接无效并阻断，先回退污染改动再重新扫描。
- 基线扫描和资产维护也属于**本地自动化测试**范畴：只能使用 `local` 环境信息执行，不得改动 `test` 配置文件，不得连接 `test` / `prod` / `staging` 环境数据库、缓存、消息队列、HTTP/RPC 上游或其他非 local 服务。

## Skill 作用与适用场景
- 维护项目级接口事实基线：接口清单、参数来源、依赖图、可复用参数生命周期、可复用场景、脚本适配声明和历史执行摘要。
- 将 `swag/.swag-manifest.yaml` 与 `doc/5-tests/基线/interface-inventory.yaml` 视为当前代码接口事实的双索引；任一缺失、陈旧或接口集合不一致时，必须先从当前代码刷新两边。
- 强制每次上线测试前先扫描当前项目接口事实，发现新增接口、删除接口和接口信息漂移后，先更新基线再交给执行组做测试计划。
- 对已构造且测试通过的参数样本执行可复用生命周期管理：可优先复用，但必须支持复验、过期、失效、隔离和持续更新，状态只允许 `candidate`、`reusable`、`stale`、`invalid`、`quarantined`、`retired`。
- 将 `doc/5-tests/基线/` 作为长期测试资产库，持续沉淀而不是每次上线重新梳理接口。

## 自动触发信号
- 项目首次触发本 skill，或 `doc/5-tests/基线/interface-inventory.yaml` 不存在。
- 接口基线需要刷新：项目代码发生接口新增、删除或结构变化。
- Swagger/OpenAPI 双索引不一致，或需要判定基线是否漂移。
- `project-interface-release-execution-rules` 在执行测试前需要确认接口基线是否最新。

## 首次触发冷启动规则（强制）
- 若项目从未触发过本 skill，或 `doc/5-tests/基线/interface-inventory.yaml` 不存在，必须自动进入冷启动流程。
- 冷启动时不得因为“没有现成测试产物”直接阻断；必须先扫描项目路由、controller/handler、Swagger/OpenAPI、现有测试、README 和接口文档，生成第一版接口基线。
- 冷启动时必须同时初始化 `doc/5-tests/基线/` 基线资产库，至少包含 `interface-inventory.yaml`、`dependency-graph.yaml`、`parameter-sources.yaml`、`reusable-params.yaml`、`scenario-catalog.yaml`、`script-adapter.yaml`、`execution-history.yaml`、`baseline-change-log.md` 和 `README.md` 的骨架。
- 第一版接口基线允许存在 `待确认项`，但每个待确认项都必须记录发现来源、证据和缺失原因，禁止伪装成完整基线。
- 冷启动涉及创建测试任务根目录、生成初版测试计划骨架时，联动 `test-strategy-rules 的 test-asset-governance 条件路由` 和 `project-interface-release-execution-rules` 完成对应骨架，本 skill 只负责基线资产骨架本身。

## 接口基线扫描规则（强制）
- 每次执行本 skill 前，都必须先做一次接口基线扫描；首次触发执行全量建基线，后续执行默认做增量扫描。
- 扫描来源至少覆盖：路由声明、controller/handler、Swagger/OpenAPI、现有接口测试、项目 README/接口文档，以及当前待上线改动对应的 diff。
- 扫描不是可选优化，而是门禁前置步骤；未完成扫描不得让执行组直接进入测试范围筛选和门禁结论阶段。
- 若扫描发现新增接口、删除接口、路径变更、HTTP 方法变更、鉴权变更、请求/响应结构漂移，必须先更新基线，再交由执行组生成测试计划。
- 若当前代码与基线冲突且无法自动判定，以 `待确认` 标记差异并阻断该接口的自动放行判断。

## Swagger/OpenAPI 双索引同步规则（强制）
- 当前代码是接口事实的唯一真相源；`swag/.swag-manifest.yaml` 与 `doc/5-tests/基线/interface-inventory.yaml` 只是两个视图，不允许长期独立漂移。
- 正常项目中两者理论上都不应缺失；如果任一文件缺失，不能只补缺失一边，必须判定为接口契约资产不完整，先触发 `swag-openapi-maintainer-rules` 全量刷新 `swag/`，再刷新上线测试接口基线。
- 每次上线测试前必须对比三方接口集合：当前代码扫描结果、`swag/.swag-manifest.yaml`、`interface-inventory.yaml`；三方的 `HTTP method + path` 必须一致。
- 若当前代码有接口但 swag manifest 或 interface inventory 缺失，必须先补齐两边；若当前代码已无接口但两边仍存在，swag 清理生成文件，interface inventory 标记废弃或待确认；若 schema hash 变化，interface inventory 标记 `schema_changed`，相关可复用参数标记 `stale`。
- 双索引同步报告落盘为 `interface-sync-report.yaml`；报告显示仍需双刷新、仍有待确认差异或 P0/P1 schema 漂移未处理时，不得让执行组继续给出自动上线放行结论。

## 基线漂移处理规则（强制）
- 删除或废弃接口：必须更新基线状态，不得继续按有效接口纳入门禁。
- 接口路径、HTTP 方法、鉴权方式、请求参数 schema、响应结构摘要、成功/失败判定规则发生变化时，必须先更新基线，再由执行组决定测试集合。
- 若某接口的历史测试结论已被当前代码变更推翻，必须将该接口标记为待重测，不得沿用旧结论。
- 若接口 schema、请求参数、响应结构、鉴权或业务成功判定发生漂移，必须将相关 `reusable-params.yaml` 参数样本标记为 `stale`，复用前必须复验。
- 若基线漂移会影响 `final-acceptance-rules` 的输入完整性，必须阻断最终自动放行。

## 基线资产库持续更新规则（强制）
- 每次上线测试前必须先读取 `doc/5-tests/基线/` 中的长期资产；缺失时先初始化，不能直接进入一次性测试。
- `interface-inventory.yaml` 记录接口清单和契约；`parameter-sources.yaml` 记录请求参数来源；`dependency-graph.yaml` 记录 provider / consumer 依赖关系；`reusable-params.yaml` 记录已验证可复用参数；`scenario-catalog.yaml` 记录已验证可复用场景；`script-adapter.yaml` 记录项目对通用脚本的适配；`execution-history.yaml` 记录历次摘要。
- 通过过的参数可以复用，但必须记录 `first_verified_at`、`last_verified_at`、`success_count`、`fail_count`、`status`、`ttl`、来源证据和失效原因。
- P0 / P1 接口、写接口、状态敏感接口在复用历史参数前必须做轻量复验；复验失败时不得继续使用该参数，必须更新状态并回退到参数来源解析流程（复验和解析动作由执行组在测试执行时完成，本 skill 只定义状态字段与生命周期规则）。
- 每次测试后，执行组必须回写新发现接口、参数来源、依赖边、可复用参数、可复用场景、失效参数和本轮历史摘要到本资产库；本 skill 定义资产结构，不负责运行时回写代码。
- 基线资产禁止保存明文 token、密码、手机号、身份证号、银行卡号、密钥和非 local 环境连接信息；真实值只能通过本地安全引用、当轮测试产物或 local 环境重新解析获得。

## 进入后先做什么
1. 先确认当前项目是否已存在接口基线；若不存在，则进入冷启动。
2. 先按 `references/baseline-asset-rules.md` 读取或初始化 `doc/5-tests/基线/` 长期资产库。
3. 无论是否已存在基线，都先按 `references/interface-inventory-schema.md` 扫描并对账当前接口事实。
4. 按 `references/openapi-inventory-sync-rules.md` 对账当前代码、`swag/.swag-manifest.yaml` 与 `interface-inventory.yaml`，缺任一方或三方不一致时先双刷新。
5. 按 `references/inventory-reconcile-rules.md` 输出新增、删除、变更和待确认清单，并先更新接口基线。
6. 若接口事实漂移影响参数来源或响应结构，先将相关可复用参数标记为 `stale`。
7. 按 `references/dependency-graph-rules.md` 读取或生成 provider / consumer 依赖图，供执行组筛选测试范围和排定执行顺序使用。

## 默认执行流程
1. 默认先执行接口基线扫描：首次触发执行全量扫描，后续执行默认做增量扫描。
2. 若当前项目尚无接口基线资产库，按 `references/bootstrap-workflow.md` 与 `references/baseline-asset-rules.md` 生成初版 `doc/5-tests/基线/`。
3. 按 `references/openapi-inventory-sync-rules.md` 对账当前代码、`swag/.swag-manifest.yaml` 与 `interface-inventory.yaml`；任一缺失或接口集合不一致时先刷新 swag 与接口基线，并输出 `interface-sync-report.yaml`。
4. 按 `references/inventory-reconcile-rules.md` 将扫描结果与现有基线对账，输出新增、删除、变更和待确认清单，并更新基线。
5. 按接口漂移结果更新 `parameter-sources.yaml`、`dependency-graph.yaml` 和 `reusable-params.yaml` 中受影响项；受影响可复用参数先标记 `stale`。
6. 基线刷新完成后交给 `project-interface-release-execution-rules` 继续测试范围筛选、执行、判定、报告和放行流程。

## 权责边界与不负责事项
- 负责项目级接口事实基线，不负责测试执行、接口响应判定或上线放行结论，这些由 `project-interface-release-execution-rules` 负责。
- 不替代 `functional-validation-rules` 的当前改动功能验证，不替代 `test-regression-rules` 的改动影响面回归验证。
- 不负责测试文档的结构和归档规则，必须遵循 `test-strategy-rules 的 test-asset-governance 条件路由` 和 `artifact-storage-rules` 的要求。
- 不负责测试目录的创建和结构，必须遵循 `test-strategy-rules 的 test-asset-governance 条件路由` 的要求。
- 不持有 `scripts/release_test_engine/` 的实现或运行时写权限，只读取其产出的基线资产文件。

## 需要暂停并确认的条件
- 基线资产结构损坏、可复用参数未脱敏、脚本适配配置缺失关键字段，导致无法安全复用历史资产。
- 扫描后仍无法确认大量接口的入口、鉴权方式或成功/失败判定规则。
- Swagger/OpenAPI 双索引长期无法对齐，且无法确定是代码问题还是文档滞后。

## 执行通过 / 驳回标准
- 通过：每次执行前都已完成接口基线扫描、双索引同步和基线对账；`swag/.swag-manifest.yaml` 与 `doc/5-tests/基线/interface-inventory.yaml` 均存在且接口集合一致；已读取并按需更新 `doc/5-tests/基线/` 长期资产；接口漂移已回写基线并标记受影响可复用参数。
- 驳回：未先扫描基线就直接交给执行组筛选测试范围；缺少 swag manifest 或 interface inventory 却未双刷新；接口新增/漂移未回写基线；基线资产保存了明文敏感信息。

## 执行结果归档要求
- 项目长期测试资产更新到 `doc/5-tests/基线/`，至少维护 `interface-inventory.yaml`、`dependency-graph.yaml`、`parameter-sources.yaml`、`reusable-params.yaml`、`scenario-catalog.yaml`、`script-adapter.yaml`、`execution-history.yaml` 和 `README.md`。
- 双索引同步报告 `interface-sync-report.yaml` 的字段结构由本 skill 定义，实际执行和落盘由 `project-interface-release-execution-rules` 完成。
- 所有归档遵循 `artifact-storage-rules` 和 `test-strategy-rules 的 test-asset-governance 条件路由` 的要求。

## references 读取规则
- 默认先读 `references/interface-inventory-schema.md`，确认接口基线字段结构。
- 每次执行前必须读 `references/baseline-asset-rules.md`，确认基线资产库结构、可复用参数生命周期和持续更新策略。
- 首次触发或缺少基线时，追加读取 `references/bootstrap-workflow.md`。
- 每次进入测试计划前必须读 `references/openapi-inventory-sync-rules.md`，确认 Swagger/OpenAPI 双索引同步和三方对账规则。
- 每次扫描后对账时，追加读取 `references/inventory-reconcile-rules.md`。
- 构建 provider / consumer 依赖和参数绑定时读 `references/dependency-graph-rules.md`。
- 确认和现有测试 skill 集成关系时读 `references/existing-test-skill-integration.md`。