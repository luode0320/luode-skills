# source-notes（吸收来源记录）

> 归属 owner：`apifox`。记录本 skill 各模块的能力来源，可回指来源仓库/版本。

## 2026-09-13：内部调整（用户指令规范固化）—— 接口展示与阅读简体中文统一规范（API 路径英文不变）

- **来源**：无外部源。用户明确指示并提供客户端截图红框证据：客户端接口树全是纯英文文件夹（`auth`、`registry`、`tasks`、`policies`、`audit`、`tenants`）和英文接口名称（`GET Health`），导致团队中不熟悉英文的成员无法直接读懂接口文档。指令要求："接口的 API 路径保持原有英文路径不变，但所有用于展示和阅读的内容必须统一使用简体中文，包括接口显示名称、文件夹名称、接口说明文档，以及请求参数和响应字段的注释描述。在通过 skill 生成或更新接口定义时，必须严格按此规范执行，确保团队中不熟悉英文的成员也能直接读懂接口文档。"
- **调整通道**：`skill-absorption-rules` 内部更新通道（用户指令规范固化）。
- **核心变化**：
  1. **明确分离机器调用与人类阅读**：机器调用的 API 路径（URL Path）保持原有英文技术路径不变，确保网络协议与代码契约稳定性；
  2. **展示与阅读内容统一简体中文**：
     - **接口显示名称（name/summary）**：必须为简体中文，禁止直接用英文单词或方法名（如 `健康检查` 代替 `Health`）；
     - **文件夹名称（folder）**：必须为业务领域简体中文（如 `认证授权`、`服务注册`、`任务管理`、`策略配置`、`审计日志`、`租户管理`），严禁创建纯英文文件夹；
     - **接口说明文档（description）**：必须使用简体中文，详述业务背景、功能流程与使用规则；
     - **请求参数注释（params/requestBody properties description）**：Path/Query/Header/Body 每个参数的 description 必须使用简体中文说明；
     - **响应字段注释（responses schema properties/headers description）**：返回体结构与各字段 description 必须使用简体中文说明；
  3. **落地到生成与维护生命周期**：在通过 skill 生成、导入、更新或审计接口定义时，作为硬性前置与即时回读校验标准（A1/A11 动作），杜绝英文展示内容入库。
- **回补落点**：
  - `SKILL.md` ← 「核心共享规则」新增「接口展示与阅读中文规范（强制铁律）」+ 模块按需加载路由表补充中文规范关键词
  - `modules/api-design.md` ← 新增「接口展示与阅读中文规范（强制铁律）」专节（对照表+红框反面案例剖析）+ 「创建接口标准流程」与「不可违反规则」同步
  - `modules/api-folder-organization.md` ← 「核心原则」与「业务模块识别与中文命名规范」明确文件夹必须为简体中文 + 反例与正例对照表 + 不可违反规则第 2 条
  - `modules/api-sync-to-apifox.md` ← 步骤 6 契约校验补充中文展示核验 + 步骤 6.2 folder 中文校验 + 不可违反规则第 9、11、12 条
  - `modules/import-export.md` ← Step 5 增加 tags、folder、summary、description 简体中文校验
  - `modules/project-onboarding-checklist.md` ← 硬动作 A1（接口中文名+说明+参数/响应中文注释）与 A11（业务 folder 简体中文命名与归类）
  - `workbuddy-absorption-map.md` ← 登记本次内部调整裁决与去重扫描
- **同域去重结论**：全量 skill 扫描，中文展示与英文路径分离规范由 `apifox-cli__skillhub` 作为 Apifox 资产单一事实源，与后端代码生成中的 DTO/注释规则分工明确，无跨 skill 污染。**PASS**。

## 2026-08-25：内部调整（用户指示口径调整）—— apifox 测试隔离环境密钥策略放宽

- **来源**：无外部源。用户明确指示"apifox 环境允许 agent 自行填入，不需要用户手动，因为环境本身是隔离的，无需保密密钥安全，这个要吸收到 apifox skill 中"。触发场景：11 个用例依赖 `v2ApiSecret`，原 skill 强制"agent 不代填、必须用户手动在客户端填"，在隔离测试项目里造成无谓阻塞。
- **调整通道**：`skill-absorption-rules` 内部更新通道（用户指示口径调整，非外部吸收）
- **核心变化**：敏感变量/凭据策略从"一律不代填"改为**按 apifox 环境隔离等级两档分流**——默认档（共享/正式 apifox 项目）保持"值不回显 + agent 不代填"；隔离档（apifox 测试专用隔离项目）密钥低敏、**agent 可经 Apifox 开放 API 直接代填**，脱敏红线收窄为"值不扩散到仓库文档/git/聊天摘要/PROJECT_TEST.md"。
- **新增技术通道**：Apifox 开放 API `PUT/GET /api/v1/projects/{projectId}/environments/{id}` 可读写 `variables`（CLI 2.2.9 仍读写不到），鉴权 `Authorization: Bearer <Access Token>` + `X-Apifox-Api-Version: 2024-03-28`，body 的 `variables` 为序列化 JSON 字符串；代填后 GET 回读核对。
- **回补落点**（详见 `workbuddy-absorption-map.md` 2026-08-25 续3 段）：
  - `modules/environment.md` ← 敏感变量节改两档分流 + 「agent 代填通道」小节 + 不可违反规则第 1 条补隔离档口径
  - `modules/test-auth.md` ← 凭据处理红线按档分流 + CLI 事实表第一行补开放 API 通道 + 不可违反规则第 4 条
  - `modules/ai-team-project.md` ← 步骤 5 加注隔离档 agent 可代填
  - `SKILL.md` ← 权限豁免节补充"密钥类变量值在隔离体内低敏" + 鉴权自动化路由行同步
  - `references/project-test-md-template.md` ← **存量纠错**："用 CLI 写入避免暴露"（做不到的规则）改为"开放 API 代填（隔离档）/ 人工填（默认档）"
  - `references/case-getactivityexposure-gap-backfill.md` ← 79/83 行加注 2026-08-25 口径更新指针
- **拒绝的记录**：无（用户指示全部合并）。
- **同域去重结论**：全量 skill 扫描"不代填/只能人工/客户端自行填"关键词，仅 apifox skill 内部命中（默认档分支 + case 加注），无跨 skill 污染。**PASS（0 处需清理）**。
- **口径演进链**：2026-08-21 从"CLI 写入"（做不到）纠错为"人工在客户端填" → 2026-08-25 隔离档放宽为"agent 经开放 API 代填"。教训：apifox 是云端 SaaS 的保密推理只适用于**共享/正式项目**，测试专用隔离项目应优先判定隔离档。

## 2026-08-24：内部调整（执行中 gap 回补）—— 调试用例与测试用例是两套资源

- **来源**：无外部源。EllipalFinance-go 项目为 5 个活动曝光管理接口建完 21 个 test-case 并跑绿后，用户截图指出客户端接口树下的「成功」用例 Body 仍是空的。查证发现本 skill 有**两条与实测相反的论断**，导致参数完整性闸门给出**假通过**（CLI 侧全绿、交付物空壳）。
- **调整通道**：`skill-absorption-rules` 执行中 gap 回补通道（阻断级：不补会持续测错方向）。
- **缺口类型**：判定标准错误 + 闸门缺失。
- **纠错的两条错误论断**：
  1. `modules/test-case.md`「接口用例 = 调试入口」节原写"接口树里接口下方的成功/失败子项 = 接口用例（test-case）""不存在把测试用例复制到调试用例这个操作" → 实测两者是**两套独立资源**（`api.cases[]` 的 `type=DEBUG_CASE`/`categoryId=0` vs `apiTestCaseCollection`），`test-case list --endpoint` 拿不到前者。
  2. 同文件规则 T-2 修复路径原写"用 `endpoint update` 接口更新为真实示例" → 实测写 `requestBody.example` 报 `success: true` 但回读为空（与 `environment update` 的 `variables` 同型的假成功）。
- **回补落点**：
  - `modules/test-case.md` ← 「两类用例是两套资源」节（**重写原错误段**，含对照表 + CLI 能力边界 + 双路验收）、规则 T-3（调试用例请求示例，含 example 层级 YAML 示例与两条修复路径）、T-2 修复路径**纠错**、不可违反规则新增第 5/6 条
  - `modules/project-onboarding-checklist.md` ← 硬动作 A12（导入后 `export --format apifox` 查 `api.cases[].requestBody.data` 非空）+ 映射表一行
  - `modules/api-sync-to-apifox.md` ← 不可违反规则第 10 条（OpenAPI 必须带请求 example 且放 MediaType 层级）
  - `SKILL.md` ← `modules/test-case.md` 路由行补 T-3 与「两套资源」关键词
- **关键实测事实（example 放错层级静默失效）**：`example` 必须放 `content."application/json".example`（MediaType 层级，与 `schema` 同级）；放进 `schema.example` **无效**——实测删接口重导后调试用例 body 覆盖 0/5，改到 MediaType 层级后 5/5 生效。OpenAPI 两处都合法，apifox 只认前者。
- **拒绝的记录**：项目侧事实（endpointId `505895223~505895227`、21 个 caseId、fixture 主键）不进全局 skill，留在项目 `PROJECT_TEST.md`。
- **同域去重结论**：扫描范围 `SKILL.md` + `modules/{test-case,project-onboarding-checklist,api-sync-to-apifox,import-export,branch}.md`。权威正文（对照表 / YAML 示例 / 判定标准 / 修复路径）**只在 `test-case.md` 一处**，checklist 与 api-sync 均为触发点/一句话规则并回指 T-3，`branch.md` 的 `--include-endpoint-cases` 已在新节中被解释归位。**PASS（0 处需清理）**。
- **净增体积**：新增约 62 行（T-3 规则 + 两套资源对照表 + A12 + 两条不可违反规则），其中约 12 行是**替换**原错误论断而非纯增；无可删除的过时内容（原段落是纠错重写，不是叠加）。
- **实战证据**：项目内 `PROJECT_TEST.md`「Apifox CLI 已验证事实」表新增 5 行；case study 见 `case-debug-case-vs-test-case.md`。

## 2026-08-21（续2）：内部调整 —— 接口归类与持续维护（folder 组织）

- **来源**：无外部源。用户指明"apifox 的接口生成也记得归类，后续也可以持续整理接口的位置，不是生成了就不用调整"，附截图反面案例：全部接口堆在「默认模块 / 接口」平铺层，未按业务模块（交易所 / 兑换活动 / 币种 / 翻译…）归类。
- **调整通道**：`skill-absorption-rules` 内部更新通道（非外部吸收，无外部源可删）
- **回补落点**（详见 `workbuddy-absorption-map.md` 2026-08-21 续2 段）：
  - `modules/api-folder-organization.md`（**新建**）← folder 三级深度、业务模块识别法、持续维护工作流（迁移/合并/拆分/归档）、定期审计命令集、与 tags 的关系、不可违反规则
  - `modules/api-design.md` ← 「folder 选择规范（强制）」小节 + 创建接口标准流程第 2 步强化
  - `modules/api-sync-to-apifox.md` ← 步骤 6.2「folder 归类校验」+ 不可违反规则第 9 条
  - `modules/import-export.md` ← Step 5 强化为「tags、folder 和可读性」双重校验
  - `modules/project-onboarding-checklist.md` ← 硬动作 A11（folder 归类即时校验）+ 批量修复命令集第 9 项 + 不可违反规则第 6 条 + 关联文档
  - `SKILL.md` ← 模块路由表新增 `api-folder-organization.md` 入口行、api-design 行补 folder 关键词、A11 加入硬动作清单
- **拒绝的记录**：无（内部规则沉淀，全部合并）。
- **同域去重结论**：`project-interface-baseline-rules` 的"目录/分组"命中均为 `doc/5-tests/基线/` 基线资产目录（不同主题）；`artifact-storage-rules` 零命中 folder 关键词。**PASS（0 处需清理）**。

## 2026-08-21（续）：内部调整 —— 鉴权链路补齐实战

- **来源**：无外部源。用户指出上一轮"没有配置鉴权的步骤"，查证发现 53 个 swag YAML 全量把自定义 md5 签名写成 `BearerAuth: http bearer`，apifox 侧鉴权组件/用例签名/鉴权用例整条缺失。
- **回补落点**：
  - `modules/test-auth.md` ← 「鉴权配置必须进 apifox（强制，即使本地免签）」三件齐清单 + 凭据处理红线 + 签名脚本模板 + 两条 CLI 事实（环境变量读写不到、operation security 不绑定接口）+ 不可违反规则第 0 条
  - `modules/api-sync-to-apifox.md` ← 步骤 6.1「安全方案必须与真实机制一致」+ 不可违反规则第 8 条
  - `modules/testing-pitfalls.md` ← 陷阱 12-1（runner 结果统计口径，grep 数 √/× 会漏计失败）、18-2（上游无权限被静默降级成空值）
  - `modules/test-case.md` ← 运行规则「结果统计口径（强制）」
  - `modules/environment.md` ← **纠错**：删除做不到的"值写入 apifox 环境变量时用 CLI 写入"，改为"人工在客户端填 + agent 只建脚本 + CLI 无此能力"
  - `swag-openapi-maintainer-rules/SKILL.md`（跨 skill，生成侧真相源）← `securitySchemes` 必须按真实校验方式生成；口径变更属全量重生成范围
- **拒绝的记录**：密钥来源名/库名/caseId 等项目事实留在项目 `PROJECT_TEST.md`；密钥值不落任何文档。
- **实战证据**：项目内 `doc/5-tests/2026-08-21_160751_getActivityExposure接口apifox测试.md`（含鉴权补齐追加节）；case study 第七节。

## 2026-08-21：内部调整（执行中 gap 回补）—— /getActivityExposure 联调实战

- **来源**：无外部源。EllipalFinance-go 项目 `POST /api/swap/v2/getActivityExposure` 首次接入 apifox 的真实联调（导入 spec → 10 用例 → 43 断言全绿），过程暴露 5 类本 skill 未覆盖场景，按 `skill-absorption-rules` 的「执行中 gap 回补通道」回补。
- **回补落点**（详见 `workbuddy-absorption-map.md` 2026-08-21 段）：
  - `modules/test-case.md` 参数完整性节 ← header-only 接口空 body 例外（阻断级：原口径会误判合法接口的用例无效）
  - `modules/test-case-generation.md` 规则 E-1 ← header-only 接口的正向分层与 L4 免除
  - `modules/environment.md` ← 「服务重启与关停核验」（包装式启动派生子进程）+ 不可违反规则第 15 条
  - `modules/testing-pitfalls.md` ← 陷阱 18-1（缓存 TTL 掩盖数据变更）、22-1（伪造来源头改变鉴权判定）、32（重启未生效）、#23 精化
  - `modules/test-auth.md` ← 「免签分支与来源头耦合」
  - `modules/test-data-and-judgement.md` ← 期望值必须实测、数据变更后生效确认、「二之二 fixture 优先级反向设计」
- **拒绝的记录**：项目侧事实（caseId / endpointId / apifox 库缺 v1 老表现象）不进全局 skill，留在项目 `PROJECT_TEST.md`。
- **实战证据**：项目内 `doc/5-tests/2026-08-21_160751_getActivityExposure接口apifox测试.md`（含 runner 原始输出与两处执行期发现）。

## 2026-08-19：API测试自动化专家版 v1.5.0（api-test-automation-pro__skillhub）

- **来源**：本地安装 skillhub 包（`api-test-automation-pro__skillhub`，v1.5.0，MIT，category=backend-testing），安装时用户级 + 工作区双副本。
- **来源能力**：REST/GraphQL 功能测试、Spring Doc/OpenAPI 解析、YAML 测试定义、性能测试、契约测试、测试点分析、180 陷阱知识库（Python 工具库形态，约 1 万行脚本 + 18 references）。
- **吸收落点**（详见 `workbuddy-absorption-map.md`）：
  - `modules/test-contract.md` ← contract_guide.md（契约方法论）
  - `modules/test-performance.md` ← performance_guide.md（性能方法论）
  - `modules/test-yaml-definition.md` ← yaml_test_guide.md（YAML 定义方法论）
  - `modules/test-health-score.md` ← health_report.md（五层健康评分）
  - `modules/testing-pitfalls.md` 七~十二节 ← SKILL.md（四层诊断/8 类 Fallback）+ security_checker 分类 + test_pitfalls_checklist.md（Top20/优先级表/高价值陷阱）
  - `modules/test-case.md` 断言顺序/速查 ← SKILL.md 约束 + Assertions 分类
  - `SKILL.md` 路由表 + 三重门控 ← SKILL.md 检查点（Inversion 门控）
  - `test-strategy-rules/SKILL.md` + `references/strategy-dimensions.md` ← 策略级引用与可选维度
- **已删除的源**：吸收确认后删除源 skill 双副本（用户级 + 工作区），内容已全部吸收或登记。
- **整体拒绝的记录**：
  - 22 个 Python 脚本（约 1 万行）：脚本实现层与本地红线"接口级测试必须 apifox 落地、禁本地 shell/curl 代替"冲突，整体拒绝，仅吸收方法论与检查清单。
  - README 提及但实际缺失的 5 个 references（smart_parser_guide.md / diagnostic_guide.md / template_loader_guide.md / memory_system.md / security_checks.md）：均为脚本层专属文档且未落地，拒绝；其分类精华从 README/SKILL.md 可读描述吸收。
  - HTTP 全表参考：低频冗余，本地 troubleshooting/test-case 已覆盖场景。
- **历史吸收（早于本次）**：`modules/testing-pitfalls.md` 原 31 条陷阱与 `modules/test-case-generation.md` 三类用例方法论亦标注吸收自 API 测试类 skill（含本源的 180 陷阱库），本次为补缺式二次吸收。

---

## 2026-08-30：外部吸收 `comprehensive-test-case-writer`（全面测试用例编写器）

- **来源**：外部 skill（skillhub 安装源 `functional-use-cases__skillhub`，SKILL.md 8,501 字节，无 references、无脚本）。
- **通道**：外部吸收（本地安装源模式）。**环境依赖**：N/A（纯方法论）。
- **本 skill 落点（仅 1 处）**：`modules/test-case-from-requirement.md` 新增 **Step 3.5 质量维度边界表**（逐条标注 apifox 可落地 / 落地方式 / 转出去向），并附红线：❌ 维度（界面 UI、易用性、客户端兼容性、游戏玩法与联机体验）禁止为凑覆盖矩阵拼成接口用例。
- **同步落点（其他 owner）**：维度定义、黑盒五法、按任务类型裁剪、用例质量四性、游戏测试专项 → `test-strategy-rules/references/test-case-design-methods.md`（测试域单一权威）；下游引用 → `functional-validation-rules/SKILL.md` references 读取规则。
- **拒绝落本 skill 的条目**：用例模板 7 字段与 P0-P3 优先级（本地 12 字段 + 风险导向 P0-P2 更强，防两套模板）；需求驱动 / RTM / 黑盒五法 / 质量检查点（本地已覆盖）；游戏测试专项（玩法与联机体验不属 apifox 承接范围，仅游戏服务端 HTTP 接口可进 apifox）。
- **已删除的源**：吸收确认后删除源 skill 双副本（用户级 `C:\Users\luode\.workbuddy\skills\functional-use-cases__skillhub\` + 工作区 `D:\谷歌云盘\luode-skills\functional-use-cases__skillhub\`）。

## 2026-09-01 内部调整：用例构造四类伪失败（执行中 gap 回补）

- 通道：执行中 gap 回补（无外部源）。
- 来源实操：ellipal_admin 热门列表 8 接口首次接入 apifox（项目 8730939 / folder 94750815 / 场景 8686960），43 用例 + 11 步闭环场景落地过程中的真实踩坑。
- 落点：`modules/test-case.md` 新增规则 T-4（伪失败四坑）+ 硬动作第 7 条；`modules/test-scenario.md` 补 `--sync manual` 副本语义与写库场景连跑两次验收标准；`modules/testing-pitfalls.md` 第七节挂第 0 层指针。
- 裁决表：见本 skill `workbuddy-absorption-map.md` 2026-09-01 条目。

## 2026-09-01：外部吸收 4 源接口用例精华（GitHub，用户指定全部候选逐一审）

- **来源**：GitHub 市场 8 个候选源逐一抓取原文裁决，4 吸收 + 3 只参考 + 1 拒绝，全部为通用形态改写、不绑定任何 agent。workbuddy 市场侧本环境不可查（skillhub.workbuddy.cn TLS 断开；本地 `.workbuddy/skills` 是指向本仓库的 junction）。
- **通道**：外部吸收（网络抓取原文 → 三态裁决 → 落盘）。**环境依赖**：N/A（纯方法论与规则资产）。
- **本 skill 落点（7 处）**：
  1. `SKILL.md`：路由表新增「调试用例/接口用例」入口行 + description 补「接口用例/调试用例」+ 核心共享规则新增「用例任务门禁」（五元组 + 新增/维护二分，吸收自源3）+ onboarding-checklist 路由行补 A13。
  2. 新增 `modules/debug-case.md`（接口用例唯一权威）：覆盖度铁律 + 创建/维护/批量工具链 + 字段规范 + 失败排查 8 级。
  3. `modules/test-contract.md`：契约 7 专项维度 + 四态判定 pass/drift/break + 基线只作比较不作证明 + evidence 规则（吸收自源1）。
  4. `modules/test-case.md`：无条件断言响应头（Content-Type/Cache-Control/Rate-Limit）（吸收自源2）。
  5. `modules/testing-pitfalls.md`：反模式清单（条件性断言、不 mock DB 边界、空壳用例）（吸收自源2）。
  6. `modules/test-case-from-requirement.md`：可执行性硬标准（禁占位符/具体数据/异步判定时限）+ 跨路径校验（编辑/重提绕过）（吸收自源6）。
  7. `modules/test-selection-policy.md`：风险反向覆盖门禁（Critical/High 被 ≥1 用例 risk_ref 覆盖）（吸收自源6）。
- **onboarding-checklist**：节点 2 新增硬动作 A13（接口用例覆盖度铁律）+ 不可违反规则第 7 条。
- **只参考未落盘**：源4 naodeng（PolyForm 非商业）、源5 PramodDutta（Postman/Pact 生态不同）、源7 bestdeejay（Python 脚本定位）——只改写思路不搬原文，无本 skill 落点。
- **拒绝**：源8 open-agent-skills/contract-test-generator（内容近乎为空）。
- **明确跳过**：源6 F7 设计方法选型与黑盒五法重叠（测试域单一权威归 `test-strategy-rules/references/test-case-design-methods.md`）；源3/5/7 脚本层（pytest/mitmproxy）不吸收——接口测试必须经 apifox 落地红线。
- **已删除的源**：无（外部源 GitHub 只读参考，不改写不删除；无本地安装源副本可删）。

## 2026-09-08：外部吸收 `z-dev-unit-mock`（单元测试Mock生成器）

- **来源**：本地已安装 skillhub 源 `z-dev-unit-mock__skillhub`（v1.0.1，MIT，122 installs，slug `z-dev-unit-mock`）。
- **通道**：外部吸收（本地安装源模式）。**环境依赖**：N/A（纯方法论与数据类型映射）。
- **触发场景**：用户指令"吸收到 apifox 的 mock 规则中"。当前 apifox mock.md 有"创建/同步"规则，缺"根据 schema 自动生成 Mock bodyData 的具体映射规则"，`z-dev-unit-mock` 的核心方法论正好是"输入函数签名/类型定义 → 生成测试桩与 Mock 数据"。
- **吸收落点**（详见 `workbuddy-absorption-map.md` 2026-09-08 条目）：
  - `modules/mock.md` ← 新增「Schema 驱动 Mock 数据生成规则」节（类型映射表 12 种 + format 子类 + 语义推断表 20+ 常见关键词 + 生成策略 maxDepth/必填覆盖/非必填比例）
- **核心变化**：兜底 Mock 创建从"bodyData 含全部必填响应字段"升级为**按字段类型和语义精确生成数据**——agent 能根据接口 schema 自动生成视觉真实的 Mock 响应，而非手动填 `"string"` / `123` 占位。
- **拒绝的记录**：
  - 输入函数签名 → 生成测试骨架（单元测试领域，非 apifox 职责）
  - 输出可复制代码片段（脚本层，与 apifox CLI 落地红线冲突）
  - 边界陷阱提示（`test-case.md` 规则 T-4 已覆盖）
- **同域去重结论**：`test-case-generation.md` 的「schema 驱动数据构造规则」表是测试用例侧的**正向/边界/异常值三列**，与本吸收的 Mock 正向值单列**不同职责域**，不冲突不重复。**PASS（0 处需清理）**。
- **已删除的源**：无（外部源 GitHub 只读参考，不改写不删除；无本地安装源副本可删）。

## 2026-09-08：外部吸收 `kunlun-cn-api-mock`（API Mock 与联调助手）

- **来源**：skillhub 安装源 `kunlun-cn-api-mock__skillhub`（v1.0.0，昆仑增长，免费，slug `kunlun-cn-api-mock`）。
- **通道**：外部吸收（本地安装源模式）。**环境依赖**：N/A（纯方法论，无 CLI 依赖 / 工具链安装）。
- **触发场景**：用户指令"吸收一下这个到 apifox 的 mock 规则中"。当前 apifox mock.md 已覆盖 CLI 操作与数据生成规则，但工程实践层面缺少"并行开发联调时的契约先行、异常场景设计、联调清单"等方法论，正好补充。
- **吸收落点**（详见 `workbuddy-absorption-map.md` 2026-09-08 条目）：
  - `modules/mock.md` ← 新增「异常场景 Mock 设计」章节（超时/500/限流/404/无权限/服务降级的 Mock 设计表 + 设计原则）
  - `modules/mock.md` ← 新增「契约先行原则」章节（三种契约状态的 Mock 策略 + 临时 Mock 管理）
  - `modules/mock.md` ← 新增「联调清单」章节（联调前检查清单 8 项 + 联调中排错清单）
- **核心变化**：从"只讲 CLI 创建/更新操作"升级为**覆盖并行开发完整流程**——契约先定 → 创建 Mock → 异常场景设计 → 联调前检查 → 联调中排错。减少前后端联调扯皮。
- **拒绝的记录**：
  - 代码评审/技术方案设计/调试排错/架构权衡（这些是通用工程能力，不属 apifox Mock 范畴，本 skill 不承接）
- **同域去重结论**：无重复内容，所有吸收内容都是对 apifox Mock 工程实践层的补充。**PASS（0 处需清理）**。
- **已删除的源**：无（外部源不改写不删除，本地 skillhub 已安装副本保留供其他 skill 使用）。
- **源处置**：外部源不改写不删除（本地 skillhub 已安装副本，保留供其他 skill 使用）。
