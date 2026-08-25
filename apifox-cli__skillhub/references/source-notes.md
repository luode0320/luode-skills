# source-notes（吸收来源记录）

> 归属 owner：`apifox`。记录本 skill 各模块的能力来源，可回指来源仓库/版本。

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
