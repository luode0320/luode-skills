---
schema_version: 1
template_version: 1
doc_id: "STYLE-ABSORB-20260901-001"
doc_type: style_regression
source_ids:
  - "SKILL-ABSORB-INTERFACE-CASES-20260901"
status: accepted
version: "v1.0"
current_slice: "TASK-07"
updated_at: "2026-09-01 15:10:00"
reader_level: business_general
writing_style: plain_chinese
appendix_policy: preserve_existing_or_one_terminal_appendix
---

# 6-review 风格回归：从 GitHub 吸收接口用例精华补强 apifox 接口用例覆盖

结论：本轮仅核对规则文档、模块落点和字典产物的写法与归位；影响：不代替业务正确性判断和发布放行；范围：`apifox-cli__skillhub`（SKILL.md + 8 个模块 + 2 个登记文件 + 新增 debug-case.md）、`doc/3-实施/`、`doc/6-review/`、`skill-dictionary/`；非范围：业务运行时正确性、发布放行、其他兄弟 skill、apifox CLI 凭据验证；变化：接口用例（DEBUG_CASE）从只有 test-case.md 规则 T-3 一处专属规则，升级为独立路由可命中的 `modules/debug-case.md` 唯一权威（覆盖度铁律 + 创建/维护/批量工具链 + 字段规范 + 失败排查 8 级），并补强 6 个既有模块、SKILL.md 用例任务门禁、onboarding-checklist 硬动作 A13 与不可违反规则第 7 条；完成标准：STYLE: PASS；术语说明：接口用例 = 接口树下调试用例（`api.cases[]` type=DEBUG_CASE）；6-review 是对规则文档、模块和字典资产写法的检查；验证状态：本次相关真实测试（结构断言 + 字典脚本）全部通过后执行。

## 文档信息

| 字段 | 内容 |
| --- | --- |
| 关联任务 | 接口用例专项外部吸收（skill-absorption-rules 外部吸收通道） |
| 关联真实测试 | TASK-01~07 结构断言 + `generate_dictionary.py` exit 0 |
| 检查时点 | 7 任务全部实现并跑完真实测试后 |

## 检查范围

本轮检查：

- `SKILL.md` 路由表「调试用例/接口用例」入口行、description「接口用例/调试用例」、核心共享规则「用例任务门禁」、onboarding-checklist 路由行 A13 是否四处一致且无格式问题；
- 新增 `modules/debug-case.md` 是否 UTF-8、中文无乱码、章节结构（owner/何时加载/边界/引用 case study/铁律/工具链/字段规范/失败排查 8 级）完整、无 TASK 占位残留；
- 6 个增强模块（test-contract/test-case/testing-pitfalls/test-case-from-requirement/test-selection-policy/project-onboarding-checklist）新增节是否与既有章节衔接、无重复、无占位词；
- 字典刷新是否可重复，`data.js` / `字典.md` 是否同步；
- 吸收登记（absorption-map / source-notes）格式是否符合既有条目规范（含 agent 通用性列）。

### 范围外说明

不迁移历史 `doc/3-实施/` 文档、不执行 Git 提交、不改动其他兄弟 skill（test-strategy-rules 等只读）、不触碰 `.workbuddy/skills` junction；apifox export 抽查因无凭据记为「环境阻断」，用结构断言替代。

## 真实测试前置证据

TASK-01~07 结构断言全部通过：`grep` 命中 37 处关键词（debug-case/覆盖度铁律/契约专项维度/用例任务门禁/失败排查 8 级/风险反向覆盖/A13）；字典 `python -X utf8 -B skill-dictionary/generate_dictionary.py` exit 0，`data.js` 已含「接口用例/调试用例」；登记文件可查（absorption-map 300 行、source-notes 119 行）。

## 6-review 结论

STYLE: PASS

本轮未发现需要修复的风格问题。`modules/debug-case.md` 章节结构与 modules/ 既有惯例一致（owner/何时加载/边界/关联参考/正文节），引用 case study 第八/九节且无 TASK 占位残留；SKILL.md 路由/description/门禁/A13 四处一致；6 个增强模块新增节均与既有章节衔接（test-contract 契约专项维度挂在检查清单前、test-case 无条件断言响应头挂在断言速查后、testing-pitfalls 反模式清单挂在使用方式前、test-case-from-requirement 可执行性节挂在 Step 6 前、test-selection-policy 风险反向覆盖挂在 P0/P1/P2 分级后、onboarding-checklist A13 挂在 A12 后）；吸收登记含 agent 通用性列，遵循 skill-absorption-agent-genericity-rule；文件编码 UTF-8、中文无乱码、字典刷新成功。

### 完成标准

风格回归完成标准为：模块结构与既有惯例一致、SKILL.md 路由/门禁/A13 四处语义一致、新增节与既有章节衔接无重复、改动最小、全部文件 UTF-8、字典刷新成功、登记格式合规。以上标准全部满足，判定 PASS。

## 检查清单

| 检查项 | 结论 | 依据 |
| --- | --- | --- |
| debug-case 模块结构 | PASS | owner/何时加载/边界/引用 case study/铁律/工具链/字段规范/失败排查 8 级齐，无 TASK 占位残留 |
| SKILL.md 四处一致 | PASS | 路由「调试用例/接口用例」行 + description「接口用例/调试用例」+ 用例任务门禁 + A13 路由行 |
| 6 模块新增节衔接 | PASS | 每处均挂在既有章节后，无重复、无占位词 |
| A13 与不可违反规则 | PASS | 节点 2 A13 可定位（82 行），不可违反规则第 7 条（318 行） |
| 最小改动 | PASS | 仅改 apifox skill 资产 8 文件 + 新增 debug-case.md + 字典 + 2 登记 + 实施/6-review 文档，未新增 skill、未迁移历史文档 |
| 文件编码 | PASS | 新增与修改文件 UTF-8，中文无乱码 |
| 字典刷新 | PASS | `generate_dictionary.py` exit 0，data.js 含「接口用例/调试用例」 |
| 吸收登记 | PASS | absorption-map（300 行）+ source-notes（119 行），含 agent 通用性列 |
| 未引入无关改动 | PASS | 未新增 skill、未执行 Git 提交 |

## 问题与修复

| 序号 | 问题 | 严重度 | 修复动作 | 状态 |
| --- | --- | --- | --- | --- |
| 1 | 字典重跑后 data.js / 字典.md 未含「调试用例/接口用例」关键词 | 低（description 未更新，字典从 SKILL.md frontmatter 提取触发信号） | apifox description 补「接口用例/调试用例」，重跑字典 exit 0，data.js 命中 | 已修复 |
| 2 | 无（结构断言 + 字典全过） | N/A | N/A | 保留 |

图片资产决策：N/A + 原因 + 证据：本轮是规则文档、模块与字典资产改动，没有 UI、截图、原型或位图需要视觉留证。

## 执行附录

### 关键改动

- `apifox-cli__skillhub/SKILL.md`：路由表新增「调试用例/接口用例」入口行；description 补「接口用例/调试用例」；核心共享规则新增「用例任务门禁」（五元组 + 新增/维护二分）；onboarding-checklist 路由行补 A13
- `apifox-cli__skillhub/modules/debug-case.md`（新增）：接口用例唯一权威——覆盖度铁律 + 创建/维护/批量工具链 + 字段规范 + 失败排查 8 级
- `apifox-cli__skillhub/modules/test-contract.md`：契约 7 专项维度 + 四态判定 + 基线语义 + evidence 规则（源1）
- `apifox-cli__skillhub/modules/test-case.md`：无条件断言响应头（源2）
- `apifox-cli__skillhub/modules/testing-pitfalls.md`：反模式清单（源2）
- `apifox-cli__skillhub/modules/test-case-from-requirement.md`：可执行性硬标准 + 跨路径校验（源6）
- `apifox-cli__skillhub/modules/test-selection-policy.md`：风险反向覆盖门禁（源6）
- `apifox-cli__skillhub/modules/project-onboarding-checklist.md`：A13 + 不可违反规则第 7 条
- `apifox-cli__skillhub/workbuddy-absorption-map.md` + `references/source-notes.md`：4 源吸收 + 3 参考 + 1 拒绝登记
- `skill-dictionary/data.js` + `字典.md`：字典重跑
- 仓库级：`doc/3-实施/2026-09-01_000000_SKILL-ABSORB-INTERFACE-CASES-20260901_实施总览.md`（新增）、`PROJECT_CURRENT.md`（任务投影）

### 验证命令

- 结构断言：`grep -n "debug-case\|覆盖度铁律\|契约专项维度\|用例任务门禁\|失败排查 8 级\|风险反向覆盖\|A13" apifox-cli__skillhub/SKILL.md apifox-cli__skillhub/modules/*.md` → 37 处命中
- 字典：`python -X utf8 -B skill-dictionary/generate_dictionary.py` → exit 0

## 追踪附录

- 来源：`SKILL-ABSORB-INTERFACE-CASES-20260901`（用户会话 + GitHub 8 源逐一审）
- 落点：`apifox-cli__skillhub`（workbuddy-absorption-map.md / source-notes.md）
- 知识库：`N/A + 原因（skill 规则资产吸收，无独立可复用事实需沉淀到知识库；既有 apifox 测试链路笔记已覆盖，本轮未新增独立知识点）`
- 风格证据：`STYLE-ABSORB-20260901-001`（本 6-review）
