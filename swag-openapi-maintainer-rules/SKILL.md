---
name: swag-openapi-maintainer-rules
description: 当用户要求生成、补齐、刷新、维护项目 swag、更新 swag、导出 Apifox/OpenAPI/Swagger 接口文档，或需要让项目自有 HTTP 接口与主动调用的上游/第三方出站接口持续同步为 YAML 文档时触发。负责从真实路由、controller、请求 DTO、响应 DTO、统一响应包装和鉴权中间件读取自有接口契约，并从 client、请求构造、base URL、响应消费代码读取上游契约；自有接口生成项目根目录 swag/ 下的全量 OpenAPI/Swagger YAML，上游接口按服务生成 swag/<vendor-slug>/ 下的独立成套文档。每个接口单独一个 YAML，同时维护对应目录的 openapi.yaml 与 manifest。单接口 YAML 默认直导入 Apifox 选中的目录，不额外生成父目录；单接口文件名默认采用“路径名 + 中文简要说明”格式，中文简介后缀必须去掉数字前缀、序号和无业务意义的特殊符号；头部、请求参数、响应字段都必须有中文说明，可在证据充分时做受控推导。本 skill 只生成或维护 swag/ 树下的 YAML 文档产物，不修改后端代码中的 Swagger 注解、框架接入或调试入口（那属于 api-swagger-rules）；不要用它代替 api-swagger-rules、业务接口实现、接口需求设计、功能测试或线上联调。
---

# Swag / OpenAPI 全量维护规则

只在维护项目全量 HTTP 接口 OpenAPI/Swagger 资产时使用本 skill。它不是临时导出用户点名的几个接口，而是负责让项目当前代码中的所有 HTTP 接口持续同步到 `swag/`。

## Skill 作用与适用场景

- 从真实路由、route group、middleware、controller、请求 DTO、响应 DTO、统一响应包装和鉴权中间件读取接口契约。
- 生成或刷新项目根目录 `swag/` 下的全量 OpenAPI/Swagger YAML 资产。
- 每个接口生成一个可单独导入 Apifox 的完整 YAML 文件，不生成不可独立使用的片段。
- 单接口 YAML 默认直导入 Apifox 选中的目标目录，不通过默认 `tags` 额外生成父级目录。
- 单接口文件名默认采用“路径名 + 中文简要说明”格式，兼顾稳定主键与人工可读性；中文简介后缀只保留干净的接口说明，不保留 `1.`、`11.`、`（1）`、`【1】` 等序号噪音。
- 维护一个包含所有接口的总文件 `swag/openapi.yaml`。
- 维护上游/第三方出站接口：扫描 client、请求构造、base URL 和响应消费代码，将每个上游服务独立生成到 `swag/<vendor-slug>/`；上游 manifest 使用 `source_type: upstream`，`coverage: partial` 只表示本项目实际调用子集。
- 维护 `.swag-manifest.yaml`，记录路由到文件的映射、来源文件、更新时间和是否由本 skill 生成。
- 支持“更新 swag”场景：每次都全量重扫当前代码，刷新新增、变更、删除接口。
- 支持与 `project-release-test-rules` 联动：刷新 `.swag-manifest.yaml` 后，必须同步或提示同步 `doc/5-tests/基线/interface-inventory.yaml`，避免接口文档索引与上线测试索引漂移。
- 头部、请求参数、响应字段都必须补齐中文说明；若源码注释不足，可按受控推导规则补齐，但不得编造业务规则。

## 自动触发信号

- 用户说“生成 swag”“更新 swag”“刷新 swag”“补齐 swag”。
- 用户要求导出 Apifox、OpenAPI、Swagger 接口文档或 YAML。
- 用户要求让项目 HTTP 接口持续同步为接口文档。
- 当前改动新增、删除或修改 HTTP 路由、controller、请求 DTO、响应 DTO、统一响应包装或鉴权中间件，并要求同步接口文档。
- 用户要求补齐“第三方接口文档”“上游接口文档”“出站接口文档”，或要求在 `swag/<第三方>/`、`swag/<vendor-slug>/` 下维护接口 YAML。

## 核心约束

- 当前代码是唯一真相源；禁止凭历史记忆、旧文档或猜测补字段。
- 自有接口覆盖系统所有 HTTP 接口，不只覆盖用户本轮点名的接口；上游接口覆盖当前代码实际调用且契约可确定的接口子集。
- `swag/` 树是唯一正式输出目录；根目录保存自有接口，上游服务保存于一层 `swag/<vendor-slug>/` 子目录，不得在其他目录生成并行正式 OpenAPI 产物。
- `swag/openapi.yaml` 是自有接口全量总文件，不聚合上游；每个上游子目录都维护自己的独立 `openapi.yaml`、manifest 和单接口完整文件。
- 单接口 YAML 默认不得依赖 operation `tags` 做目录分组，避免 Apifox 导入时自动新增父目录；总 YAML 可保留 tags 供全量文档分组使用。
- 单接口文件名中的路径部分是稳定主键，中文简要说明是可读后缀；`operationId` 仍保持 path + method 规则，不混入中文说明。
- 单接口文件名优先使用显式中文 `summary`；缺失时允许按受控推导生成短中文说明；若仍无法稳定得到中文说明，可回退到纯路径文件名，但必须在 manifest 中记录 `summary_source: unresolved`。
- 中文简要说明进入文件名之前，必须先剥离数字前缀、序号包裹符号和无业务意义的开头特殊符号；文件名后缀只保留接口中文简介本体。
- 头部、请求参数、响应字段的中文说明是强制要求，不允许因为“源码无注释”而长期留空；只能按受控推导规则补齐或阻断通过。
- 删除接口后，对 `.swag-manifest.yaml` 中标记为本 skill 生成的旧单接口 YAML 默认清理。
- 只删除 manifest 标记为本 skill 生成的文件，禁止清理用户手写或来源不明的 YAML。
- 清理必须按目录和 `source_type` 隔离：根 manifest 只能清理根目录裸文件，上游 manifest 只能清理自身 vendor 目录内裸文件，不得跨目录删除。
- 只产出或更新 `swag/` 目录下的 OpenAPI/Swagger YAML 文档，不改动 controller、路由、DTO 中的 Swagger 注解与框架代码；后端代码侧的 Swagger 框架接入、注解与调试入口属于 `api-swagger-rules`。
- 不代替业务接口实现、接口需求设计、功能测试或线上联调。
- 不代替上线测试执行；但刷新 swag 后必须让上线测试双索引同步规则有可用的最新 manifest。

## 默认执行流程

1. 扫描路由入口：从 router、route group、middleware 中真实读取所有 HTTP method + path。
2. 扫描出站调用：从 client、请求 builder、SDK wrapper、base URL 和响应解码代码发现上游 method + path、服务 slug、请求/响应消费字段与来源符号。
3. 追 controller：每个自有 route 追到 controller 方法，读取请求绑定、响应返回、错误返回和鉴权要求。
4. 追 DTO / model：读取 request DTO、response DTO、repository model、统一响应包装；字段必须来自真实代码；上游只记录实际消费字段，按真实上游包装表达。
5. 构建接口索引：自有接口记录 router/controller 来源，上游接口记录 `source_client_file`、`source_symbols`、`base_url`、`upstream` 和 `discovery_confidence`。
6. 按 `references/description-rules.md` 补齐头部、请求参数、响应字段中文说明；上游优先使用代码消费结构体和离线受控资料，源码注释不足时仅允许受控推导。
7. 按 `references/naming-rules.md` 生成单接口文件名和 B1 目录：基础路径名在前，中文简要说明在后；中文后缀需先去掉数字前缀、序号和无业务意义的特殊符号，再做字符清洗与长度截断。
8. 生成单接口 YAML：每个接口一个完整 OpenAPI 文档，可单独导入 Apifox，默认不写 operation `tags`，避免新增父目录。
9. 生成自有总 YAML：`swag/openapi.yaml` 包含所有自有接口，components 做去重；总 YAML 可保留 tags 供全量文档分组，不聚合上游。
10. 生成上游独立成套文档：每个 `swag/<vendor-slug>/` 包含自己的 openapi、manifest 和单接口 YAML，manifest 标记 `source_type: upstream` 与 `coverage: partial`。
11. 更新 manifest：记录本次生成覆盖的接口、来源文件、`summary`、`summary_source` 和更新时间；上游额外记录 base URL、消费来源和发现置信度。
12. 若中文简要说明变化导致文件名变化，且旧文件由本 skill 生成，则在对应目录刷新后删除 manifest 指向的旧文件。
13. 清理过期文件：当前接口已不存在且对应 manifest 标记为本 skill 生成的单接口 YAML，按根/上游目录隔离清理。
14. 若项目存在 `doc/5-tests/基线/`，自有接口继续联动 `project-release-test-rules` 的双索引同步规则；上游子集不并入自有接口基线，除非项目另有明确接入规则。
15. 校验：运行 `scripts/validate_openapi_yaml.py --swag-dir swag` 递归校验根与上游子目录，并执行 `git diff --check`。

## 进入后先做什么

1. 先读 `references/discovery-rules.md`，确认当前项目的路由、controller、DTO 发现策略。
2. 若任务涉及上游/第三方出站接口，再读 `references/third-party-discovery-rules.md`，确认 client、base URL、响应消费和离线证据规则。
3. 再读 `references/naming-rules.md`，确定 `swag/` 文件命名、B1 目录、manifest 和过期清理规则。
4. 再读 `references/description-rules.md`，确认中文说明来源、受控推导边界和缺失阻断口径。
5. 生成 YAML 前读 `references/schema-rules.md`，确认 OpenAPI 版本、字段、components、servers 和 `$ref` 规则。
6. 收口前读 `references/validation-rules.md`，按根目录与上游子目录清单完成校验。

## 执行通过 / 驳回标准

通过：

- `swag/openapi.yaml` 存在并覆盖当前系统所有 HTTP 接口。
- 若存在出站调用，已按上游服务生成 `swag/<vendor-slug>/` 独立成套文档；每个 manifest 的 `source_type`、`upstream`、`base_url`、`coverage`、来源文件和发现置信度齐全。
- 上游文档只覆盖本项目实际调用子集，根 `swag/openapi.yaml` 不聚合上游，根与上游清理互不越界。
- 每个接口都有独立完整 YAML，可单独导入 Apifox。
- 单接口 YAML 导入 Apifox 后默认直接落到选中的目录，不额外新增父目录。
- 单接口文件命名符合“路径名 + 中文简要说明”规则；method 冲突处理、数字前缀剥离、字符清洗和长度截断稳定。
- “更新 swag”会重扫当前代码并刷新新增、变更、删除接口。
- 头部、请求参数、响应字段都有真实代码来源或符合受控推导规则的中文说明。
- `.swag-manifest.yaml` 记录路由、文件、`summary`、`summary_source`、来源和生成标记。
- 若项目存在上线测试基线，已同步或明确提示同步 `doc/5-tests/基线/interface-inventory.yaml`。
- YAML 可解析，OpenAPI / Swagger 版本合法，单接口默认无 `tags`，中文说明完整，文件名与 manifest 一致，`$ref` 无并列字段，`git diff --check` 通过。

驳回：

- 只生成用户点名接口，不覆盖系统全集。
- 单接口 YAML 不能独立导入 Apifox。
- 单接口 YAML 导入时默认新增父目录。
- 单接口文件名未追加中文简要说明，或中文后缀仍残留 `1.`、`11.`、`（1）` 之类序号前缀 / 无业务意义特殊符号，或只能靠任意猜测、随机命名或未清洗非法字符得到。
- `swag/` 外还有并行正式 OpenAPI 产物。
- 删除接口后旧 YAML 长期残留。
- 头部、请求参数、响应字段缺中文说明，或说明只能靠随意猜测补齐。
- 字段来自猜测、历史记忆或旧文档而非当前代码。
- 总 YAML path 数、单接口 YAML 数和当前扫描接口数不一致。
- 上游目录缺少独立 manifest/openapi、使用错误的 source_type、跨目录登记裸文件、伪造未消费字段，或无法从代码确定 method/path/base URL 仍声称通过。

## references 读取规则

- 默认先读 `references/discovery-rules.md`。
- 生成或清理文件前必须读 `references/naming-rules.md`。
- 生成字段说明前必须读 `references/description-rules.md`。
- 生成 OpenAPI / Swagger 内容前必须读 `references/schema-rules.md`。
- 最终收口前必须读 `references/validation-rules.md`。

## scripts

- `scripts/validate_openapi_yaml.py`：校验 `swag/` 下 YAML 可解析、OpenAPI / Swagger 版本、总文件路径数、单接口文件数、manifest 映射和 `$ref` sibling。
- `scripts/validate_openapi_yaml.py`：在保留根目录兼容行为的同时，递归编排并校验一层上游服务子目录及其 manifest 元数据。
