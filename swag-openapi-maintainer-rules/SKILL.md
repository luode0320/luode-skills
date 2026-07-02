---
name: swag-openapi-maintainer-rules
description: 当用户要求生成、补齐、刷新、维护项目 swag、更新 swag、导出 Apifox/OpenAPI/Swagger 接口文档，或需要让项目所有 HTTP 接口持续同步为 YAML 文档时触发。负责从真实路由、controller、请求 DTO、响应 DTO、统一响应包装和鉴权中间件读取接口契约，生成或更新项目根目录 swag/ 下的全量接口 OpenAPI/Swagger YAML；每个接口单独一个 YAML，同时维护一个包含所有接口的总 YAML。不要用它代替业务接口实现、接口需求设计、功能测试或线上联调。
---

# Swag / OpenAPI 全量维护规则

只在维护项目全量 HTTP 接口 OpenAPI/Swagger 资产时使用本 skill。它不是临时导出用户点名的几个接口，而是负责让项目当前代码中的所有 HTTP 接口持续同步到 `swag/`。

## Skill 作用与适用场景

- 从真实路由、route group、middleware、controller、请求 DTO、响应 DTO、统一响应包装和鉴权中间件读取接口契约。
- 生成或刷新项目根目录 `swag/` 下的全量 OpenAPI/Swagger YAML 资产。
- 每个接口生成一个可单独导入 Apifox 的完整 YAML 文件，不生成不可独立使用的片段。
- 维护一个包含所有接口的总文件 `swag/openapi.yaml`。
- 维护 `.swag-manifest.yaml`，记录路由到文件的映射、来源文件、更新时间和是否由本 skill 生成。
- 支持“更新 swag”场景：每次都全量重扫当前代码，刷新新增、变更、删除接口。
- 支持与 `project-release-test-rules` 联动：刷新 `.swag-manifest.yaml` 后，必须同步或提示同步 `doc/5-tests/基线/interface-inventory.yaml`，避免接口文档索引与上线测试索引漂移。

## 自动触发信号

- 用户说“生成 swag”“更新 swag”“刷新 swag”“补齐 swag”。
- 用户要求导出 Apifox、OpenAPI、Swagger 接口文档或 YAML。
- 用户要求让项目 HTTP 接口持续同步为接口文档。
- 当前改动新增、删除或修改 HTTP 路由、controller、请求 DTO、响应 DTO、统一响应包装或鉴权中间件，并要求同步接口文档。

## 核心约束

- 当前代码是唯一真相源；禁止凭历史记忆、旧文档或猜测补字段。
- 覆盖系统所有 HTTP 接口，不只覆盖用户本轮点名的接口。
- `swag/` 是唯一正式输出目录；不得在其他目录生成并行正式 OpenAPI 产物。
- `swag/openapi.yaml` 是全量总文件；其余 YAML 是单接口完整文件。
- 删除接口后，对 `.swag-manifest.yaml` 中标记为本 skill 生成的旧单接口 YAML 默认清理。
- 只删除 manifest 标记为本 skill 生成的文件，禁止清理用户手写或来源不明的 YAML。
- 不代替业务接口实现、接口需求设计、功能测试或线上联调。
- 不代替上线测试执行；但刷新 swag 后必须让上线测试双索引同步规则有可用的最新 manifest。

## 默认执行流程

1. 扫描路由入口：从 router、route group、middleware 中真实读取所有 HTTP method + path。
2. 追 controller：每个 route 追到 controller 方法，读取请求绑定、响应返回、错误返回和鉴权要求。
3. 追 DTO / model：读取 request DTO、response DTO、repository model、统一响应包装；字段必须来自真实代码。
4. 构建接口索引：记录 method、path、operationId、tag、summary、router 来源、controller 来源、request schema、response schema、auth / headers 和输出文件名。
5. 生成单接口 YAML：每个接口一个完整 OpenAPI 文档，可单独导入 Apifox。
6. 生成总 YAML：`swag/openapi.yaml` 包含所有接口，components 做去重。
7. 更新 manifest：`.swag-manifest.yaml` 记录本次生成覆盖的接口、来源文件和更新时间。
8. 清理过期文件：当前路由已不存在且 manifest 标记为本 skill 生成的单接口 YAML，默认删除。
9. 若项目存在 `doc/5-tests/基线/`，联动 `project-release-test-rules` 的双索引同步规则刷新或提示刷新 `interface-inventory.yaml`。
10. 校验：运行 `scripts/validate_openapi_yaml.py`，并执行 `git diff --check`。

## 进入后先做什么

1. 先读 `references/discovery-rules.md`，确认当前项目的路由、controller、DTO 发现策略。
2. 再读 `references/naming-rules.md`，确定 `swag/` 文件命名、manifest 和过期清理规则。
3. 生成 YAML 前读 `references/schema-rules.md`，确认 OpenAPI 版本、字段、components 和 `$ref` 规则。
4. 收口前读 `references/validation-rules.md`，按清单完成校验。

## 执行通过 / 驳回标准

通过：

- `swag/openapi.yaml` 存在并覆盖当前系统所有 HTTP 接口。
- 每个接口都有独立完整 YAML，可单独导入 Apifox。
- 文件命名符合 path 下划线规则，method 冲突处理稳定。
- “更新 swag”会重扫当前代码并刷新新增、变更、删除接口。
- 请求 / 响应字段都有真实代码来源。
- `.swag-manifest.yaml` 记录路由、文件、来源和生成标记。
- 若项目存在上线测试基线，已同步或明确提示同步 `doc/5-tests/基线/interface-inventory.yaml`。
- YAML 可解析，OpenAPI / Swagger 版本合法，`$ref` 无并列字段，`git diff --check` 通过。

驳回：

- 只生成用户点名接口，不覆盖系统全集。
- 单接口 YAML 不能独立导入 Apifox。
- `swag/` 外还有并行正式 OpenAPI 产物。
- 删除接口后旧 YAML 长期残留。
- 字段来自猜测、历史记忆或旧文档而非当前代码。
- 总 YAML path 数、单接口 YAML 数和当前扫描接口数不一致。

## references 读取规则

- 默认先读 `references/discovery-rules.md`。
- 生成或清理文件前必须读 `references/naming-rules.md`。
- 生成 OpenAPI / Swagger 内容前必须读 `references/schema-rules.md`。
- 最终收口前必须读 `references/validation-rules.md`。

## scripts

- `scripts/validate_openapi_yaml.py`：校验 `swag/` 下 YAML 可解析、OpenAPI / Swagger 版本、总文件路径数、单接口文件数、manifest 映射和 `$ref` sibling。
