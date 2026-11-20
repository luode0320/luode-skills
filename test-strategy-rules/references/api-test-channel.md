# 接口测试执行通道（强制）

> 本节是「接口级测试执行通道」的单一权威来源。接口功能验证、接口回归、Bug 接口验证、上线门禁的接口部分统一遵循本节；`functional-validation-rules`、`test-regression-rules`、`bug-validation-rules` 直接引用本节，不重复定义执行细节。

### 判定边界：代码级 / 接口级 / 页面前端级 三条通道

- 测试对象是函数/方法/模块/纯逻辑 → **代码级测试** → 保留本地 `go test` / pytest，不切换。
- 测试对象是 **HTTP 接口**（有 method+path，经 HTTP 协议调用）→ **接口级测试** → 必须走 apifox 真实测试并落地用例。
- 测试对象是**前端页面 / 组件 / 路由 / 用户交互路径** → **页面前端级测试** → 走《页面/UI 级测试执行通道（强制）》，不属本通道。
- 同一轮验证可能同时含代码级、接口级与页面前端级测试：按测试对象分类各自执行，不得把整轮验证一刀切；三层证据分列，**任一层不得顶替另一层**。

### 接口级测试强制走 apifox（强制）

- 接口功能验证、回归、Bug 接口验证、上线门禁的接口部分，统一用 `apifox test-case run` / `test-suite run` 在 apifox「AI 团队」对应项目中执行，并**落地测试用例保存到 apifox**（用例保留即落地，必要时并入 test-suite 回归）。
- **apifox 测试专用项目（用户为 apifox 测试单独创建的项目）直接在 `main` 分支操作**：接口文档操作、测试、补充测试用例全部直接落在 main 分支，**不新开 AI 分支 / api 分支，不做「开分支 → 自动化测试 → 合并回 main」的多余操作**（项目级隔离已足够）。
- **任何本地测试形态都不构成豁免（强制，2026-09-01 实操补强）**：不得只做本地验证后不落地用例。「本地」包括但不限于 shell/curl、Python/Node 脚本（`urllib`/`requests`/`axios` 直调接口）、`go test` / pytest 外部黑盒包、`test/` 下的接口对照脚本。**「本地脚本已经覆盖了同样的断言」是最常见的漏触发借口，明确不成立**——本地脚本证明的是「这一次逻辑正确」，apifox 用例是团队可复用、可回归、可进 CLI/CI 的资产，二者验证目标不同，不可互相替代。原条款只列了 shell/curl，导致本地 Python 接口脚本在字面上不被覆盖而被自我判定为「已满足接口级测试」，故扩展为形态无关表述。
- **接口实现改动即触发（强制）**：只要本轮改动触达接口可见行为（新增/修改 handler、路由、请求或响应 DTO、参数校验、字段白名单、排序/筛选/分页口径、错误码与错误文案），无论是否新增接口，都必须走本通道；「只是给已有接口加了两个字段」「只是加了个排序参数」同样触发。**与页面前端级的联动（强制）**：该接口若存在前端调用面（检索口径见《页面/UI 级测试执行通道（强制）》的「接口调用面检索」），本轮**同时触发**页面前端级测试；接口级用例全绿不构成前端点击验证的替代证据。
- 目标项目解析与接口同步流程见 `apifox-cli__skillhub/modules/ai-team-project.md` 与 `modules/api-sync-to-apifox.md`；swag/OpenAPI 生成归 `swag-openapi-maintainer-rules`。

### 环境红线不变（强制）

- **被测服务 environment 白名单（强制）**：本地测试与接口级测试的被测服务启动环境**只允许 `local` 与 `apifox`** 两个环境（对应 `config/yaml/config.local.yaml` 与 `config/yaml/config.apifox.yaml`）；**选择优先级按项目配置决定**——项目**存在 apifox 环境配置（`config/yaml/config.apifox.yaml`，含同仓 `backend/config/yaml/config.apifox.yaml`）时默认使用 `apifox` 环境**（被测服务 `-env apifox` 启动）；项目**没有 apifox 环境配置时默认使用 `local` 环境**；`test` / `prod` / `staging` / `pre` / `release` 等非 local 环境**一律禁止**用于本地测试与接口测试。
- apifox environment 的 baseUrl 只允许指向 **local**（localhost / 本地开发配置声明的服务），禁止指向 `test` / `prod` / `staging` / `pre` / `release`；判定标准仍是「配置归属」而非物理地址，与「本地环境配置发现与连接」一致。
- 运行测试显式带 `--environment <localhost环境Id>`，避免默认环境漂移。

### 前置条件

- 被测服务必须在本地启动且端口可访问（先做可达检查再执行用例）。
- 被测服务以 `config/yaml/config.apifox.yaml` 启动（无则从 `config.local.yaml` 复制生成），且**库分离校验通过**：apifox 的 MySQL 库名约定为 `apifox`（开发人员手动创建配置），与 `config.local.yaml` 相同必须阻断，等用户部署 apifox 测试专用库后再继续（见 `apifox-cli__skillhub/modules/environment.md`）。
- 数据构造以 **local 数据库为数据基准**（见 `apifox-cli__skillhub/modules/test-data-and-judgement.md`）：**apifox 库无数据且 local 有 → 优先从 local 库单向灌数据到 apifox 测试库**（local 只读源、脱敏、可追溯）；**apifox 与 local 都无数据 → apifox 自造测试数据**；禁止连非 local 服务取数。**模型测试宽权限场景**（建表/复杂数据构造/大范围写操作）：项目已有 apifox 环境配置时，允许 apifox 环境自建 **`tmp` 前缀临时库**测试使用，**测试完成必须删除**；正常库（非 `tmp` 前缀，含 apifox 库/local 库）**禁止删除**（见 `apifox-cli__skillhub/modules/environment.md`「临时库特权」）。

### 标准执行链路

```text
1. 本地启动被测服务，确认端口可访问
2. 解析 apifox「AI 团队」项目 projectId（.apifox/settings.json 或 apifox project list）
3. 确认/创建 localhost environment（baseUrl=http://localhost:<port>）
4. （项目级）project-interface-baseline-rules 刷新接口基线
5. endpoint 定位；不存在 → api-sync-to-apifox 模块先同步
6. 生成/选择 test-case（category → cli-schema get/validate → create）
7. test-case run <caseId> --project <projectId> --environment <localhostEnv>
8. 按 test-data-and-judgement.md 判定 PASS/EXPECTED_FAIL/UNEXPECTED_FAIL/PENDING
9. 用例保留在 apifox（通过即落地），必要时并入 test-suite 回归
10. 结论写回 doc/5-tests/ 测试主文档（内联 caseId/报告链接），必要时回写接口基线
```

### 收口硬闸：接口改动轮必须给出 apifox 证据（强制）

> 本节是「接口级测试收口证据」的判据单一权威；`code-change-finalization-gate-rules` 只引用本节做闸门执行，不重复定义判据。补于 2026-09-01：此前本通道只写了「必须走 apifox」，但收口清单里没有对应的证据项，导致本地测试全绿即被当成可收口，漏触发在收口阶段无人拦截。

- **触发判定**：本轮存在接口实现改动（判据见上方「接口实现改动即触发」）。
- **收口必须给出的证据**（缺任一项即不得宣称「已完成 / 已验证可用」）：
  1. projectId + 接口 endpointId（新接口须说明是 `import` 同步还是 `endpoint create` 直建）；
  2. 用例 / 场景标识（caseId 列表或 scenarioId）与分类分布（正向 / 负向 / 边界值 / 安全性各几条）；
  3. 真实运行结果，按**断言总数 / 失败数**口径给出（不用勾叉计数，理由见 `apifox-cli__skillhub/modules/testing-pitfalls.md` 陷阱 12-1）；
  4. 写接口的数据清理复核结论（残留条数 + 全表行数对照）。
- **本地测试结果不能顶替上述任何一项**：本地脚本断言数可以一并列出，但必须与 apifox 证据分列，禁止合并成一个「测试全过」的笼统结论。
- **允许的例外**：接口无法在 local 环境达成前置条件（上游不可达、依赖外部签名等）时，按环境阻断如实登记（哪几条、阻断原因、补跑命令），**不得默认视为已覆盖**；例外只针对具体用例，不豁免整轮。

### 结论留痕

- 接口验证结论写回 `doc/5-tests/` 测试主文档；用例保存证据（caseId / suiteId / 报告链接）内联进证据小节，不得只写「已测试」无凭据。
- 项目已有 `PROJECT_TEST.md`（测试域 SSOT）时，apifox 侧的接口 id / 用例 id / 场景 id、踩到的用例构造坑与覆盖缺口一并追加到其变更记录，供后续同类模块直接复用。

### 专项方法论按需加载

- 契约测试、性能测试、健康评分、YAML 批量定义等**专项方法论**（吸收自 API测试自动化专家版）按需加载 apifox 对应模块：`apifox-cli__skillhub/modules/test-contract.md` / `test-performance.md` / `test-health-score.md` / `test-yaml-definition.md`。
- 这些专项为**可选策略维度**（见 `references/strategy-dimensions.md`），仅在对应需求出现时启用，不影响本通道的强制执行链路。
