# TAPD OpenAPI 调整来源

## 2026-10-13：Bug 版本默认每次查询所属项目当前迭代

- 内部调整来源：用户在完成 NEXCHANGE(DEFI) 报价修复及 TAPD 补录后明确要求：“默认使用当前迭代，不是固定的，每次都需要重新查询该 Bug 所属项目的当前迭代。”
- 当次证据：项目接口存在两个同时标为当前的迭代，不能只取开启状态或最高版本；最终依据 Bug 修复小版本说明选定当次目标，并回读 `iteration_id` 与 `version_report`。该历史选择不是后续任务的固定默认值。
- 落点：主 SKILL 的关键规则 12、[版本规则](bug-version-and-current-iteration.md)、现有 [修复补录入口](completed-fix-and-timesheet.md)。保留该入口已存在的身份、工时和写入失败处理内容，不另复制。
- 同域边界：`tapd-cli` 负责客户端调用；`tapd-task-executor` 负责任务执行；Bug 默认版本策略只归 `tapd-openapi`。`mine` 的便捷当前迭代查询不替代写入裁决。
- 环境依赖：无新增环境配置，继续复用 `tapd-env-bootstrap` 的已有鉴权预检和 TAPD GET 接口；不保存凭据。agent 通用性：通用 HTTP/API、Markdown 规则，不绑定单一宿主。
- 验证与独立评分见 [吸收案例](case-current-bug-version.md)。

## 2026-10-13 已完成修复补录与工时登记

- 来源：本会话 EllipalFinance-go 空主币表修复后的 TAPD 补录，用户要求新增 Bug 并填 1 小时工时，随后授权吸收经验到 TAPD skill。
- 实证：[Bug 1130399328001004055](https://www.tapd.cn/tapd_fe/30399328/bug/detail/1130399328001004055)。创建及 GET 回读确认 reporter/current_owner 为罗德、status=resolved、resolution=fixed，描述含 c58fa653 和 32b3143c；timesheet 1130399328001008070 为 2026-10-13、timespent=1，匹配记录只有一条。
- 边界：代码级回归通过、运行服务未重启且 HTTP 接口未验收。此姓名和项目仅为案例，不是默认值。
- 内部调整：openapi 专用补录流程及状态/工时回读；CLI 只补 Windows/WSL UTF-8 临时脚本调用。身份、凭据和 API 字段仍引用原 Owner，修正 Bug 索引 5 个失效路径，补录与受委派执行分流。
- 语义澄清：本次实例曾同时填 effort=1 和实际 1 小时；后续仅要求已完成修复工时时只填 timespent，明确要求预估时再写 effort，不照抄双填。
- 裁决与验证：[吸收裁决表](../workbuddy-absorption-map.md)、[案例与校验](case-tapd-openapi-absorption.md)。

## 2026-10-19 TAPD 操作统一 CLI 优先

- 来源：用户指出 TAPD 任务误走浏览器并要求修正规则，使 CLI 成为默认通道，只有 CLI 无法处理时再回退。
- 本地现状：`tapd-cli/SKILL.md` 有命令入口；`tapd-openapi/SKILL.md` 曾把单条读取引向 API；`authenticated-url-routing-rules/SKILL.md` 的通用网页默认规则可能覆盖 TAPD；评论与任务执行技能也各自声明通道。
- 裁决与落点：以 `tapd-openapi/SKILL.md` 作为统一路由权威，顺序为 CLI → 直接 OpenAPI → 浏览器；更新 `tapd-cli`、`tapd-addcomment`、`tapd-task-executor` 及 URL 路由例外保持一致。只有 CLI 与 API 均无法满足页面专属操作，或用户明确要求直接操作页面时才用浏览器。
- 整理去重：扫描 `tapd-cli`、`tapd-openapi`、`tapd-addcomment`、`tapd-task-executor`、`authenticated-url-routing-rules`；共发现原有通道说明不一致 3 处，统一为 CLI 优先并保留各 skill 的领域专属补充；无新增重复门控、孤立文件或断链。
- 环境依赖与通用性：无新增环境配置，复用现有 CLI/API 凭据预检，不回显凭据；规则对所有 agent 通用。
- 验证：5 个受影响 skill 的 `quick_validate.py` 均通过；字典已刷新；未执行 TAPD 真实 API/浏览器操作（本轮仅调整规则资产）。
