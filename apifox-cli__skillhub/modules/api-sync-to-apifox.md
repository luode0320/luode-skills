# 接口新增/更新同步到 apifox（强制）— import / endpoint / test-case

> 本模块覆盖「代码实现完成后，把接口新增/更新同步到 apifox 并落地测试用例」的强制流程。已从 SKILL.md 继承：写入标准流程、AI 分支说明、分支参数规则、必须询问用户。
>
> 边界：本模块只负责「导入 apifox 及之后」的动作；swag/OpenAPI YAML 的生成归 `swag-openapi-maintainer-rules`，本模块不重复生成 spec。

## 何时加载

- 接口新增、更新、删除后需要同步到 apifox
- 代码实现完成，需要让接口在 apifox 中可测
- 导入 OpenAPI 后需要校验契约与落地用例
- 用户要求「接口的新增、更新都在 apifox 中进行」

## 强制同步流程

0. **确认 apifox CLI 已安装（强制前置）**：`apifox --version`；未安装则立即按 SKILL.md「安装（强制，最高优先级）」安装（npm install -g apifox-cli，慢则切 npmmirror），装完验证版本并确认登录；CLI 不可用则**阻断**同步任务，不得跳过
1. **代码实现完成**：接口、DTO、注解已落地（接口契约以代码为准）。
2. **生成 swag YAML**：交由 `swag-openapi-maintainer-rules` 刷新 `swag/` 下的 OpenAPI 资产；本模块不重复生成。若 swag 缺失或接口集合不一致，先回流 `swag-openapi-maintainer-rules`。
3. **确认目标项目**：按 `modules/ai-team-project.md` 解析「AI 团队」项目 projectId，确认 `--project <projectId>`。
4. **创建/确认 AI 分支**：默认走 AI 分支（命名 `ai/年月日-from-来源分支名-接口同步`）；已有接口先 `branch pick-to` 导入，新建接口不需要。
5. **导入 OpenAPI**：
   ```bash
   apifox import --project <projectId> --branch <aiBranchName> --format openapi --file swag/openapi.yaml
   ```
   导入前必须按 `modules/import-export.md` 输出质量指标（paths/operations/schemas/writes/withBody/emptyObjectBodies）；导入后检查 `ignoreCount`，大量 ignore 是风险信号，不得忽略。
6. **契约校验（含字段说明完整性）**：`apifox endpoint list/get` 确认 method+path+schema 已同步，与代码对账；同时检查参数/请求体/响应/头部每个字段的 `description` 是否非空——**缺失则回流 `swag-openapi-maintainer-rules`（`references/description-rules.md`）在代码侧补中文注释 → 重新生成 swag → 重新导入**，接口侧与代码侧两边都要补，不要遗漏；校验不通过先修正再继续。
7. **落地/更新测试用例**：按 `modules/test-case-generation.md` 的「覆盖度铁律」（每接口必须有 正向+负向+边界值 三类用例，POST 等非 GET 接口必须有完整用例）补全，按 `modules/test-case.md` 标准流程创建（先 `test-case category` 获取有效 categoryId，再 cli-schema get/validate，创建后 `get` 回读验证）。**不要在只补 1 个分页正向用例时就宣称覆盖到位**。
8. **运行验证**：`apifox test-case run <caseId> --project <projectId> --branch <aiBranchName> --environment <开发环境Id>`，确认真实通过（判定规则见 `modules/test-data-and-judgement.md`）。
9. **合并**：`merge-request preview` 让用户确认 → 用户确认后 `create merge-request` 或 `merge`。
10. **同步接口基线**：提示 `project-interface-baseline-rules` 更新 `doc/5-tests/基线/` 接口清单，保持基线资产与 apifox 一致。

## 与 swag-openapi-maintainer-rules 的边界

| 环节 | 归属 |
|------|------|
| 代码 → swag/OpenAPI YAML 生成 | `swag-openapi-maintainer-rules` |
| YAML → apifox 导入、契约校验、用例落地、运行 | 本模块 |
| 接口事实基线维护 | `project-interface-baseline-rules` |

- 若接口同步后发现 swag 与代码不一致，回流 `swag-openapi-maintainer-rules` 修正后再导入
- 本模块不修改代码侧 Swagger 注解，也不生成 swag 资产

## 不可违反规则

1. 接口变更后不同步到 apifox 即视为接口同步缺口，不得以「本地调试过」替代
2. 不跳过导入前质量指标
3. 不忽略大量 `ignoreCount`
4. 不要跳过导入后的 endpoint 契约校验
5. 不要在分支任务中省略 `--branch`，不要直接污染主分支
6. 不修改 swag 生成逻辑，swag 资产归 `swag-openapi-maintainer-rules`
7. 接口变更后，字段说明（参数/响应/头部 `description`）必须随接口同步更新，不允许只改字段不改说明
