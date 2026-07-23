---
name: project-change-review-rules
description: 当前改动总审查 skill。两类场景自动成立：用户明确点名 `$project-change-review-rules`、`project-change-review-rules`、说出“审核当前改动/当前 diff”，或本轮存在代码改动且准备最终收口。负责只读审查当前项目未提交改动、已暂存改动和可见新增文件，覆盖需求边界、缺陷、遗漏、安全风险、重复逻辑、未按已命中 skill 规则实现、注释缺失或乱码、日志打印不合规、工具包/公共方法复用不足、代码可读性差、补丁式修补、测试与验证缺口；输出按严重级别排序的问题清单，不直接改代码、不格式化、不提交。
---

# 项目当前改动总审查规则

## 目标

把“审查当前项目改动”收口成一个统一总审查入口。进入后先界定当前 diff，再用代码审查视角找问题：边界是否跑偏、实现是否有缺陷、是否漏测漏改、是否有安全和日志风险、是否重复造轮子、是否违反项目已启用的 skill 规则，以及代码是否像临时补丁。

本 skill 是总审查闸门，只读、不修复、不提交。发现问题后输出可执行回改建议；默认直接基于当前代码与已命中主 skill 判定，不依赖一组镜像 review skill 才能成立。

## 快速流程

1. 读取项目规则文件：优先 `AGENTS.md`，不存在再读 `CLAUDE.md`。
2. 盘点当前改动：
   - `git status --short`
   - `git diff --stat`
   - `git diff --name-only`
   - `git diff --cached --stat`
   - `git diff --cached --name-only`
   - 对未跟踪文本文件，按风险和相关性抽样读取。
3. 确定审查边界：本轮只审查当前可见改动，不顺手审历史遗留；若改动依赖历史上下文，只读必要调用方、被调用方和配置。
4. 按审查矩阵逐项检查，必要时只建议回到对应主 skill 处理。
5. 输出发现优先的审查报告。若无问题，明确写“未发现阻断项”，并说明剩余风险和未执行验证；P0/P1 造成真实阻断时，按 `../artifact-delivery-gate-rules/references/task-blocker-closure-contract.md` 在报告中创建或引用去重的 `BLK-*`，记录最小回改计划与复审入口。
6. 用户显式要求审查当前改动，或非 Git 提交的最终收口前自动总审查，必须归档到 `doc/6-审查/`；禁止因为“未发现阻断项”而省略审查文档落盘。
7. Git 提交所需的基础代码核查或轻量审查不自动触发本 skill 的完整总审查：仅按 `git-collaboration-rules` 对当前 staged 改动完成必要审查、验收与放行步骤，不生成 `doc/6-审查/` 审查文档，也不以既有审查文档作为前置条件。当前轮用户明确点名本 skill 或明确要求总审查时，仍按显式总审查处理并归档。

## 审查矩阵

必须覆盖以下维度：

- 需求边界：是否扩大范围、改了无关文件、引入新行为但没有需求依据、修改公共行为却没有兼容路径。
- 缺陷风险：空值、边界条件、错误处理、状态顺序、并发、缓存、事务、幂等、时区、分页、排序、权限、异常分支。
- 遗漏风险：只改上游未改下游，只改请求未改响应，只改实现未改文档/Swagger/配置/迁移/测试，只改主路径未改失败路径。
- 安全风险：鉴权绕过、权限粒度变宽、敏感信息日志、SQL/命令/路径注入、XSS、CSRF、SSRF、反序列化、密钥落盘、调试入口暴露。
- 重复逻辑：同语义工具函数重复封装、业务文件内复制已有 util、同一判断/映射/转换在多个位置复制。
- skill 合规：当前改动是否漏触发或漏执行相关 skill，尤其是注释、日志、可读性、目录归位、接口请求/响应、Swagger、数据库、测试、格式和语法检查。
- 注释质量：只要本轮存在代码改动，就必须按 `comment-placement-granularity-rules` 与 `comment-completion-gate-rules` 完整检查并阻断不合规项；新增/修改函数、方法、字段定义、结构体字面量字段映射、关键配置对象、补丁位点都必须满足中文 UTF-8、函数头 `[参数]` / `[返回]` / `最近修改时间` / 本次改动原因、步骤编号 `1/2/3` 就近注释、字段/字段组中文说明以及补丁“做了什么 + 为什么要加”注释，任一缺失都不能以“通过审查”收口。
- 日志与追踪：是否用正式 logger；是否存在 console/print 临时输出；日志是否有业务上下文、脱敏、trace/span、错误对象和排障字段。
- 工具包使用：是否优先复用项目已有公共方法、成熟依赖和框架能力；是否绕过封装直接拼低层实现。
- 可读性与补丁感：是否控制流跳跃、嵌套过深、硬编码、魔法值、临时分支堆叠、函数过长、文件持续膨胀、命名含糊、局部修补破坏整体结构。
- 测试与验证：是否有必要测试；测试目录、命名、fixture、执行方式是否符合项目规则；验证结果是否能覆盖改动风险。

## 专门 Skill 联动

根据问题类型回流对应主 skill：

- 需求边界不清或范围跑偏：回到 `requirement-boundary-rules`
- 实现质量、补丁感、格式、语法、目录归位：回到 `implementation-review-rules`
- 注释缺口：回到 `comment-placement-granularity-rules`、`comment-completion-gate-rules`
- 日志、trace、审计、脱敏：回到 `logging-trace-rules`
- API 请求/响应/Swagger：回到 `api-request-rules`、`api-response-rules`、`api-swagger-rules`
- 数据库、SQL、事务、schema：回到 `database-query-rules`、`database-schema-rules`
- 回归风险和验证缺口：回到 `test-strategy-rules`、`test-regression-rules`、`functional-validation-rules`
- 已命中 skill 是否执行完整：`skill-audit-rules`、`skill-execution-compliance-gate-rules`

如果某个主 skill 的 `SKILL.md` 尚未读取，不得声称已按该 skill 逐条完成审查；只能写“建议回到对应主 skill 处理”。若已经读取并执行其检查，必须在报告中给出对应证据。
若本轮存在代码改动，则 `comment-placement-granularity-rules` 与 `comment-completion-gate-rules` 不再是“可建议回流”的弱提示，而是当前总审查的必读必查项；未实际核验字段注释、函数头注释、步骤注释、补丁注释、`最近修改时间` 与改动原因前，不得给出“审查结论: 通过”。

## 共享证据和专属契约

- 本入口仍只承接显式“当前改动总审查”和非 Git 提交最终收口前的自动总审查；不得与 `implementation-review-rules` 的测试前自审或 `code-review-automation-rules` 的提交级审查混淆。
- 读取当前 diff、形成问题等级、输出审查报告、归档、声明通过/阻断或处理剩余风险前，必须读取 `references/shared-evidence-and-specialized-contracts.md`。
- 该引用保留证据读取、P0-P3、注释双 skill、报告字段、阻断、归档和相邻 gate 的完整细则；本文件保留自动触发、审查矩阵与条件路由。

## references 读取规则

- 读取顺序遵循「共享证据和专属契约」：先读 `references/shared-evidence-and-specialized-contracts.md`，再按其中路由读取 `references/checklist.md`、`references/report-template.md` 与 artifact-delivery-gate 共享契约。
