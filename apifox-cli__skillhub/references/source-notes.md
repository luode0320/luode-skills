# source-notes（吸收来源记录）

> 归属 owner：`apifox`。记录本 skill 各模块的能力来源，可回指来源仓库/版本。

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
